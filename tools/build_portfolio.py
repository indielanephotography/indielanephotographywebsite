"""Build the portfolio category pages from Donna's curated selects.

Usage (from the repo root):
    python tools/build_portfolio.py            # process any _incoming/<slug>/ folders, then rebuild every page
    python tools/build_portfolio.py --pages    # skip image processing, rebuild pages from existing manifests

Input:  _incoming/<slug>/*.jpg|jpeg|png|tif   originals downloaded from ShootProof (gitignored)
        _incoming/<slug>/order.txt            optional: one filename per line, in Donna's gallery order
                                              (otherwise files are sorted by name)
Output: assets/portfolio/<slug>/<slug>-NN-sm.webp   <=800px wide, for the grid on phones / homepage
        assets/portfolio/<slug>/<slug>-NN-lg.webp   <=1600px wide, for the grid on desktop + full-screen viewer
        assets/portfolio/<slug>/manifest.json
        portfolio/<slug>/index.html
        index.html  service card covers (data-portfolio-cover) + "Recent work" mix (PORTFOLIO-MIX block)

Header, mobile nav, footer and sticky bar are copied from index.html on every build, so the
category pages stay in sync with the homepage.
"""
import argparse
import html
import io
import json
import os
import re
import shutil
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

from PIL import Image, ImageCms, ImageOps

ROOT = Path(__file__).resolve().parent.parent
INCOMING = ROOT / '_incoming'
ASSETS = ROOT / 'assets' / 'portfolio'
PAGES = ROOT / 'portfolio'
SITE_URL = 'https://www.indielane.com.au'

SIZES = {'sm': 800, 'lg': 1600}
QUALITY = 80
SOURCE_EXTS = {'.jpg', '.jpeg', '.png', '.tif', '.tiff', '.webp'}

# Order matches the services grid on the homepage. `cover` is the 1-based image used on the
# homepage service card; `mix` are the images that feed the homepage "Recent work" grid.
CATEGORIES = [
    dict(slug='branding', title='Branding Portraits', short='Branding',
         seo='Branding Photographer Byron Bay & Surf Coast',
         intro='Headshots and personal brand images that look like you, not a stiff corporate suit. Perfect for your website, LinkedIn and socials.',
         cover=1, mix=[2, 3]),
    dict(slug='commercial', title='Commercial', short='Commercial',
         seo='Commercial Photographer Byron Bay & Surf Coast',
         intro='Documentary style photography for businesses, schools and councils. People, products and spaces, captured with an artistic eye.',
         cover=1, mix=[2, 3]),
    dict(slug='editorial-lifestyle', title='Editorial & Lifestyle', short='Editorial & Lifestyle',
         seo='Editorial & Lifestyle Photographer Byron Bay & Surf Coast',
         intro='Storytelling image sets and relaxed lifestyle sessions full of happy faces and real moments, shot outdoors in beautiful natural light.',
         cover=1, mix=[2, 3]),
    dict(slug='food-product', title='Food & Product', short='Food & Product',
         seo='Food & Product Photographer Byron Bay & Surf Coast',
         intro='Fresh, vibrant images that make your menu and products irresistible, online and in print.',
         cover=1, mix=[2, 3]),
    dict(slug='weddings', title='Weddings', short='Weddings',
         seo='Wedding Photographer Byron Bay & Surf Coast',
         intro='Relaxed, candid wedding day coverage from someone who has shot over 200 weddings, real moments over stiff posing, in beautiful natural light.',
         cover=1, mix=[2, 3]),
    dict(slug='events', title='Events', short='Events',
         seo='Event Photographer Byron Bay & Surf Coast',
         intro='Natural, candid coverage that captures the feeling of the day, from launches to celebrations.',
         cover=1, mix=[2, 3]),
]

SRGB = ImageCms.createProfile('sRGB')
CURRENT = ' aria-current="page"'


# ---------------------------------------------------------------- images

def natural_key(name):
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r'(\d+)', name)]


def source_files(folder):
    files = [p for p in folder.iterdir() if p.suffix.lower() in SOURCE_EXTS]
    order_file = folder / 'order.txt'
    if not order_file.exists():
        return sorted(files, key=lambda p: natural_key(p.name))
    by_name = {p.name.lower(): p for p in files}
    ordered = []
    for line in order_file.read_text(encoding='utf-8').splitlines():
        p = by_name.pop(line.strip().lower(), None)
        if p:
            ordered.append(p)
    # anything not listed in order.txt goes at the end rather than being dropped silently
    return ordered + sorted(by_name.values(), key=lambda p: natural_key(p.name))


def to_srgb(im):
    icc = im.info.get('icc_profile')
    if im.mode == 'CMYK' or icc:
        try:
            src = ImageCms.ImageCmsProfile(io.BytesIO(icc)) if icc else None
            if src is not None:
                return ImageCms.profileToProfile(im, src, SRGB, outputMode='RGB')
        except Exception:
            pass
    return im.convert('RGB')


def process_one(job):
    src, out_dir, base = job
    with Image.open(src) as im:
        im.draft('RGB', (SIZES['lg'] * 2, SIZES['lg'] * 2))  # fast JPEG decode at reduced scale
        im = ImageOps.exif_transpose(im)
        im = to_srgb(im)
        result = {'source': src.name}
        for label, width in SIZES.items():
            w = min(width, im.width)
            h = round(im.height * w / im.width)
            out = im if w == im.width else im.resize((w, h), Image.LANCZOS)
            out.save(out_dir / f'{base}-{label}.webp', 'WEBP', quality=QUALITY, method=5)
            result[label] = [w, h]
        r, g, b = im.resize((1, 1), Image.BOX).getpixel((0, 0))
        result['color'] = f'#{r:02x}{g:02x}{b:02x}'
    return result


def process_category(cat):
    folder = INCOMING / cat['slug']
    files = source_files(folder)
    if not files:
        print(f"  {cat['slug']}: _incoming folder is empty, skipping")
        return
    out_dir = ASSETS / cat['slug']
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True)
    jobs = [(p, out_dir, f"{cat['slug']}-{i:02d}") for i, p in enumerate(files, 1)]
    with ProcessPoolExecutor(max_workers=max(1, (os.cpu_count() or 2) - 1)) as pool:
        results = list(pool.map(process_one, jobs))
    images = [dict(file=job[2], **res) for job, res in zip(jobs, results)]
    (out_dir / 'manifest.json').write_text(json.dumps({'slug': cat['slug'], 'images': images}, indent=1), encoding='utf-8')
    kb = sum(f.stat().st_size for f in out_dir.glob('*.webp')) // 1024
    print(f"  {cat['slug']}: {len(images)} images processed ({kb:,} KB total)")


def load_manifest(slug):
    path = ASSETS / slug / 'manifest.json'
    return json.loads(path.read_text(encoding='utf-8'))['images'] if path.exists() else []


# ---------------------------------------------------------------- pages

def shared_chrome(index_html):
    """Header/mobile nav and footer/sticky bar/toast from index.html, re-pointed from /portfolio/<slug>/."""
    def grab(start, end):
        return index_html[index_html.index(start):index_html.index(end)]
    header = grab('  <!-- ===================== HEADER', '  <main id="top">')
    footer = grab('  <!-- ===================== FOOTER', '  </div><!-- /#site-content -->')
    def repoint(s):
        s = s.replace('href="#', 'href="../../#').replace('src="assets/', 'src="../../assets/')
        return s.replace('href="../../#top"', 'href="../../"')
    return repoint(header), repoint(footer)


def url(cat, img, label):
    return f"../../assets/portfolio/{cat['slug']}/{img['file']}-{label}.webp"


def render_page(cat, images, header, footer):
    e = html.escape
    n = len(images)
    idx = next(i for i, c in enumerate(CATEGORIES) if c['slug'] == cat['slug'])
    prev_cat = CATEGORIES[idx - 1]
    next_cat = CATEGORIES[(idx + 1) % len(CATEGORIES)]
    cover = images[min(cat['cover'], n) - 1]
    og_image = f"{SITE_URL}/assets/portfolio/{cat['slug']}/{cover['file']}-lg.webp"
    canonical = f"{SITE_URL}/portfolio/{cat['slug']}/"
    description = f"{cat['title']} photography by Donna Nugent, Indie Lane Photography. {cat['intro']}"

    tiles = []
    for i, img in enumerate(images, 1):
        sm_w, sm_h = img['sm']
        lg_w, lg_h = img['lg']
        srcset = f"{url(cat, img, 'sm')} {sm_w}w" + (f", {url(cat, img, 'lg')} {lg_w}w" if lg_w > sm_w else '')
        alt = f"{cat['title']} photography by Indie Lane Photography, {i} of {n}"
        loading = 'fetchpriority="high"' if i == 1 else 'loading="lazy"'
        tiles.append(
            f'          <a class="pf-item" href="{url(cat, img, "lg")}" data-w="{lg_w}" data-h="{lg_h}">'
            f'<img src="{url(cat, img, "sm")}" srcset="{srcset}" '
            f'sizes="(min-width: 1200px) 33vw, (min-width: 640px) 50vw, 100vw" '
            f'width="{sm_w}" height="{sm_h}" alt="{e(alt)}" '
            f'{loading} decoding="async" '
            f'style="background:{img["color"]}"></a>'
        )
    cats_nav = '\n'.join(
        f'          <a href="../{c["slug"]}/"{CURRENT if c is cat else ""}>{e(c["short"])}</a>'
        for c in CATEGORIES
    )
    schema = {
        '@context': 'https://schema.org',
        '@type': 'ImageGallery',
        'name': f"{cat['title']} photography | Indie Lane Photography",
        'description': description,
        'url': canonical,
        'image': og_image,
        'author': {'@type': 'Person', 'name': 'Donna Nugent'},
        'publisher': {'@type': 'LocalBusiness', 'name': 'Indie Lane Photography', 'url': f'{SITE_URL}/'},
    }
    return f'''<!DOCTYPE html>
<!-- Generated by tools/build_portfolio.py. Edit the script or index.html, not this file. -->
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
  <title>{e(cat['seo'])} | Indie Lane Photography</title>
  <meta name="description" content="{e(description)}">
  <link rel="canonical" href="{canonical}">

  <meta property="og:title" content="{e(cat['title'])} | Indie Lane Photography by Donna Nugent">
  <meta property="og:description" content="{e(cat['intro'])}">
  <meta property="og:image" content="{og_image}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:type" content="website">

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;0,600;1,300;1,400&family=Montserrat:wght@300;400;500;600&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../../assets/css/site.css">
  <link rel="preload" as="image" href="{url(cat, images[0], 'sm')}" imagesrcset="{url(cat, images[0], 'sm')} {images[0]['sm'][0]}w, {url(cat, images[0], 'lg')} {images[0]['lg'][0]}w" imagesizes="(min-width: 1200px) 33vw, (min-width: 640px) 50vw, 100vw">

  <script type="application/ld+json">
  {json.dumps(schema, indent=2, ensure_ascii=False)}
  </script>
</head>
<body>
  <div id="site-content" class="gw-visible">

{header}
  <main id="top">

    <!-- ===================== INTRO ===================== -->
    <div class="container pf-intro">
      <div class="line"></div>
      <p class="eyebrow reveal">Portfolio</p>
      <h1 class="reveal">{e(cat['title'])}</h1>
      <p class="section-body reveal">{e(cat['intro'])}</p>
      <nav class="pf-cats reveal" aria-label="Portfolio categories">
{cats_nav}
      </nav>
    </div>

    <!-- ===================== GALLERY ===================== -->
    <div class="pf-wrap">
      <div class="pf-grid" id="pfGrid">
{chr(10).join(tiles)}
      </div>
      <div class="pf-pager">
        <a class="prev" href="../{prev_cat['slug']}/">&lsaquo; {e(prev_cat['title'])}</a>
        <a class="next" href="../{next_cat['slug']}/">{e(next_cat['title'])} &rsaquo;</a>
      </div>
    </div>

    <!-- ===================== CTA ===================== -->
    <section class="alt pf-cta">
      <div class="container">
        <div class="line"></div>
        <p class="eyebrow reveal">Love what you see?</p>
        <h2 class="section-headline reveal">Let's create your visual story</h2>
        <p class="section-body reveal">Tell Donna a little about your business, your people or your big day, and she'll be in touch to plan a relaxed, natural light shoot.</p>
        <div class="reveal">
          <a href="../../#book" class="btn btn-primary">Book your shoot</a><a href="../../#services" class="btn btn-outline">All services</a>
        </div>
      </div>
    </section>

  </main>

{footer}
  <!-- ===================== FULL-SCREEN VIEWER ===================== -->
  <div class="pf-lb" id="pfLightbox" role="dialog" aria-modal="true" aria-label="{e(cat['title'])} photo viewer" aria-hidden="true">
    <img class="pf-lb-img" id="pfLbImg" src="data:," alt="">
    <button class="pf-lb-close" id="pfLbClose" aria-label="Close"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"><path d="M6 6l12 12M18 6L6 18"/></svg></button>
    <button class="pf-lb-prev" id="pfLbPrev" aria-label="Previous photo"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"><path d="M15 5l-7 7 7 7"/></svg></button>
    <button class="pf-lb-next" id="pfLbNext" aria-label="Next photo"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"><path d="M9 5l7 7-7 7"/></svg></button>
    <div class="pf-lb-count" id="pfLbCount"></div>
  </div>

  </div><!-- /#site-content -->

  <script src="../../assets/js/portfolio.js"></script>
</body>
</html>
'''


def update_homepage(manifests):
    path = ROOT / 'index.html'
    s = path.read_text(encoding='utf-8')
    for cat in CATEGORIES:
        images = manifests.get(cat['slug'])
        if not images:
            continue
        cover = images[min(cat['cover'], len(images)) - 1]
        src = f"assets/portfolio/{cat['slug']}/{cover['file']}-sm.webp"
        s = re.sub(rf'(<img data-portfolio-cover="{cat["slug"]}" src=")[^"]*(")', rf'\g<1>{src}\g<2>', s)
    mix = [f"assets/portfolio/{c['slug']}/{manifests[c['slug']][i - 1]['file']}-sm.webp"
           for c in CATEGORIES if manifests.get(c['slug'])
           for i in c['mix'] if i <= len(manifests[c['slug']])]
    if mix:
        block = '    var galleryImages = [\n' + ',\n'.join(f'      "{m}"' for m in mix) + '\n    ];\n'
        s = re.sub(r'(// PORTFOLIO-MIX:START[^\n]*\n).*?(    // PORTFOLIO-MIX:END)',
                   lambda m: m.group(1) + block + m.group(2), s, flags=re.S)
    path.write_text(s, encoding='utf-8', newline='')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--pages', action='store_true', help='skip image processing')
    args = ap.parse_args()

    if not args.pages and INCOMING.exists():
        print('Processing images...')
        for cat in CATEGORIES:
            if (INCOMING / cat['slug']).is_dir():
                process_category(cat)

    index_html = (ROOT / 'index.html').read_text(encoding='utf-8')
    header, footer = shared_chrome(index_html)
    manifests = {}
    print('Building pages...')
    for cat in CATEGORIES:
        images = load_manifest(cat['slug'])
        if not images:
            print(f"  {cat['slug']}: no images yet, page not built")
            continue
        manifests[cat['slug']] = images
        out = PAGES / cat['slug'] / 'index.html'
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(render_page(cat, images, header, footer), encoding='utf-8', newline='')
        print(f"  portfolio/{cat['slug']}/  ({len(images)} images)")
    update_homepage(manifests)
    missing = [c['slug'] for c in CATEGORIES if c['slug'] not in manifests]
    if missing:
        print('WARNING: homepage links to pages that do not exist yet: ' + ', '.join(missing))
        sys.exit(1)


if __name__ == '__main__':
    main()
