# Indie Lane Photography: build guide

This pack contains two things:

1. **`indie-lane.html`** the live mockup of the new landing page, with a working no-code editor built in. This is what you show Donna. Open it in any browser, double click, done. No internet setup needed (her real photos load from her current site).
2. **This guide** how the mockup translates into a real WordPress build so Donna can edit everything herself without touching code.

---

## 1. What to show Donna

Open `indie-lane.html` and walk her through it:

- The page is the finished design: hero, about, services, portfolio, client gallery callout, testimonials, and a booking enquiry form.
- At the very top is a dark bar: **Indie Lane Editor**. That bar represents what she sees only when she is logged in. The public never sees it.
- Tell her to flip **Edit content** to on.
- Now she can **click any heading, paragraph or button and just type**. Every text block is editable.
- She can **click any photo** and choose a new one from her computer. It swaps instantly. The portfolio also has a **+ Add a photo** tile and a small **x** to remove any image.
- She presses **Save changes** and it sticks. **Reset** puts everything back to the original.

That is the exact experience she gets in the real WordPress build. The mockup is a faithful simulation of it.

> Note: the mockup saves to her own browser, so her edits persist on her machine for the demo. The real WordPress version saves to her website for everyone to see.

---

## 2. How this becomes a real WordPress site

The design above is plain HTML and CSS, which ports cleanly into WordPress. Recommended stack:

**Option A (recommended): Block theme + native editor**
- A lightweight block theme (for example a custom child theme, or a blank starter like **Blockbase / Twenty Twenty-Five**).
- The whole page is built as WordPress **blocks**, so Donna edits text and images directly on the page in the Site Editor, exactly like the mockup. No page-builder licence fees.
- Pros: fast, free, future proof, closest to what she sees in the mockup.

**Option B: Theme + Elementor (or Bricks)**
- If she wants the most visual, drag-and-drop control, install Elementor.
- The mockup design is rebuilt as an Elementor template. She clicks any element to edit text or replace images, plus drag to rearrange.
- Pros: most flexible for a non-technical owner. Cons: a small annual plugin cost.

Either way she gets the click to edit, replace photo, save behaviour shown in the mockup.

### Locking it down so she cannot break it
Give Donna an **Editor** role, not Administrator. Optionally add a plugin so she only edits content areas, not layout or settings. This is what makes it genuinely safe for a non-coder.

---

## 3. The client gallery (her current "Your Gallery")

She specifically wants clients to log in and view or download their photos. In WordPress this is a solved problem. Best fit for a photographer:

- **Pic-Time** or **Pixieset** (external, very polished, what most pros use) linked from the **Access your gallery** button, or
- A WordPress plugin such as **Imagely / NextGEN Pro** if she wants galleries inside the same site.

The button in the mockup (`Access your gallery`) is the entry point. We just point it at whichever system she prefers.

---

## 4. Conversion and ads alignment (your part of the email)

The design is already built around turning visitors into bookings, which is the "conversion-focused front end" you described to Donna:

- One clear primary action everywhere: **Book your shoot**.
- A sticky **Book your shoot** bar appears on mobile as she scrolls. This is the single biggest lever for ad traffic from Instagram and Facebook.
- The enquiry form is the conversion point. When the real site is live, wire it to her email plus a tool like **Fluent Forms** so every lead is captured.
- Tracking ready: drop the Meta Pixel and a Google tag in the WordPress header so your $10 to $20 a day ad spend is measurable from day one.
- SEO basics are in the page already: proper title, meta description, one H1, local business schema, and the Byron Bay, Northern NSW and Gold Coast service areas named in the copy.

---

## 5. Things to confirm with Donna before building

- New service area wording is set to Byron Bay region plus Victoria trips. Confirm exact suburbs she wants named for local SEO.
- Swap the sample testimonials for three real client quotes.
- Decide the gallery tool (Pic-Time vs Pixieset vs in-site).
- Logo: the mockup uses a clean "Indie Lane" wordmark. If she wants her existing stacked logo, drop the file in and we use it as is.

---

## 6. File notes

- The mockup is a single self-contained file. Images are pulled live from her current Squarespace CDN so it looks like her real work. When we build in WordPress, those get re-uploaded to her own media library.
- No em dashes used anywhere, per house style.

---

## The real fix: why your converted HTML themes break, and why this one will not

You said the recurring problem is: build HTML, convert it to a WordPress theme, then it will not let you edit inside WordPress (Classic editor or Elementor) and the theme messes up.

**Root cause.** When you convert static HTML into a theme, the content ends up hardcoded inside the PHP template files (header.php, front-page.php, etc). The WordPress editor does not edit template files. It edits content stored in the database. So when you open the page in the editor there is literally nothing there to click, and Elementor either sees an empty canvas or fights the theme's own markup and layout. That is the "messes up" you keep hitting.

**The fix shipped here is a block theme (Full Site Editing).** Instead of hardcoding the design into PHP, every section is built as native WordPress blocks (Cover, Columns, Group, Heading, Paragraph, Image, Gallery, Buttons). The bespoke look is applied with the theme's stylesheet and `theme.json`, but the content itself lives as editable blocks. That means:

- Donna edits **every** text and photo by clicking it, exactly like writing a document.
- She **drags any block** to reorder sections, service cards or gallery photos. That is the Elementor-style drag and drop, except it is the WordPress editor itself, so there is no plugin licence and nothing to conflict with.
- Nothing is locked in template files, so it cannot become un-editable.

You asked about a separate "editor tool or plugin." With a block theme you do not need one. The built-in block editor **is** the page builder. That is the whole point: fewer moving parts, nothing to break, no yearly Elementor fee.

### What is in `indie-lane-theme.zip`

A complete, installable block theme:

- `style.css` plus `theme.json` (the full warm, natural-light design system, fonts and colour palette)
- `templates/` and `parts/` (header, footer, page templates as editable blocks)
- `patterns/home.php` (the entire homepage as one ready-made pattern Donna can insert and then edit)
- `functions.php` (loads Google Fonts and the design, registers the Indie Lane pattern category)
- `assets/` (light JS for the scroll reveal, sticky mobile CTA and the demo form)

### Install (about 4 minutes)

1. Appearance > Themes > Add New > Upload Theme, choose `indie-lane-theme.zip`, activate.
2. Create a Page called **Home**.
3. In that page open the inserter, go to **Patterns > Indie Lane**, insert **Indie Lane: Full homepage**.
4. Settings > Reading > set the static homepage to **Home**.
5. Appearance > Editor > Navigation to set the menu.

### Two plugins to add (the only things a theme cannot do alone)

- **Enquiry form:** the booking form in the theme is a working demo (shows a thank-you, does not email yet). Drop in **Fluent Forms** or **WPForms** and point it at hello@indielane.com.au for real lead capture. This also makes it trivial to fire a conversion event for your Meta and Google ads.
- **Private client gallery:** WordPress alone is clumsy for this. Use **Pic-Time** or **Pixieset** (galleries, downloads, even print sales) and link it from the "Access your gallery" button. Cleaner for Donna and for her clients.

### Locking it down for Donna

Give her an **Editor** account, not Administrator. She gets full click-to-edit and drag-to-reorder on pages, but cannot touch the theme files, plugins or settings, so she cannot accidentally break the build.

### A note on the photos

Both the mockup and the theme pull Donna's real photos from her current site so everything looks right on day one. Before go-live, re-upload the final images into the WordPress Media Library so the site does not depend on her old host.
