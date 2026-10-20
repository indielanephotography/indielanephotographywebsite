# Indie Lane Photography website

Static site (HTML/CSS/JS, no framework) for Donna Nugent's Indie Lane Photography, replacing her Squarespace site. Repo: github.com/indielanephotography/indielanephotographywebsite, hosted on Vercel under Donna's account. Built by Anthony (Antheon).

## Start of every session

1. Read [PLAN.md](PLAN.md): the migration plan, open items and the **Session Log**. It's the source of truth for project history and works across devices, unlike local Claude memory.
2. Check `cowork/` for the latest CoWork prompts and whether they've been actioned.

## Logging (required)

At the end of any session that changes something or receives client input, append a dated entry to the PLAN.md **Session Log**. Include what Donna asked for, what was done, decisions and why, open items, and any CoWork hand-offs. Log every client email or feedback round, even small ones. Also update local Claude memory, but PLAN.md is the record that syncs between machines.

## CoWork hand-offs

CoWork is a separate agent with browser access to Donna's accounts (ShootProof, Studio Ninja, GoDaddy, Squarespace, Vercel, GitHub). When a task needs it, write a complete, copy-pasteable prompt and save it as `cowork/YYYY-MM-DD-<task>.md`. Each prompt states the goal, exact steps, exact output locations, what not to touch, and what to report back. Never put credentials in prompts or in the repo.

## Structure

- `index.html`: homepage (single page, section anchors).
- `assets/css/site.css`: all site styles, shared by the homepage and the portfolio pages.
- `assets/js/portfolio.js`: masonry, full-screen viewer and nav for the portfolio pages.
- `portfolio/<slug>/index.html`: one page per category. **Generated, don't hand-edit.**
- `assets/portfolio/<slug>/`: processed WebP images plus `manifest.json`. Generated.
- `tools/build_portfolio.py`: the portfolio pipeline (see below).
- `_incoming/`: original photos from ShootProof (gitignored, large).
- `cowork/`: prompts handed to CoWork.

## Portfolio pipeline

Six categories (slugs): `branding`, `commercial`, `editorial-lifestyle`, `food-product`, `weddings`, `events`. Donna wants all 6 kept, with about 40-60 images each.

1. Put originals in `_incoming/<slug>/`. Add an optional `order.txt` (one filename per line) to keep Donna's gallery order.
2. Run `python tools/build_portfolio.py` (needs Pillow). It outputs sRGB WebP at 800w (`-sm`) and 1600w (`-lg`), writes the manifest, generates the pages, and updates the homepage service-card covers (`data-portfolio-cover`) and the "Recent work" array (`PORTFOLIO-MIX` markers).
3. Use `--pages` to rebuild pages only from the existing manifests, for example after editing the header or footer in `index.html` (the pages copy them from `index.html`).
4. Per-category intro text, SEO titles, cover image and homepage mix are set in `CATEGORIES` at the top of the script.

Preview locally with `python -m http.server` from the repo root, then open `/` and `/portfolio/<slug>/`.

## Rules

- Copy changes from Donna go in word for word. Keep her spelling (Australian English).
- Don't touch DNS, Squarespace or the live Studio Ninja form styling without explicit sign-off (see PLAN.md Phase 3/4).
- Most homepage images are still hotlinked from `images.squarespace-cdn.com`. Those links break when Squarespace is cancelled, so migrate them first.
