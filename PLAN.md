# Indie Lane Photography — Squarespace → GitHub/Vercel Migration Plan

This file is the running record for this project: the original plan plus a log of what happens in each session. Update it at the end of every session that touches this migration (new decisions, completed steps, blockers, changes of approach).

## Background

Donna Nugent (Indie Lane Photography) currently runs her site on Squarespace (paid monthly hosting). Her domain (`indielane.com.au`) is registered at GoDaddy, not Squarespace. She approved an Antheon-built static HTML/CSS/JS proposal site (see [index.html](index.html)) and wants to move to it. Plan: host the new static site via a GitHub repo + Vercel (Hobby plan), then cut the live domain over from Squarespace to Vercel, then cancel Squarespace — all while making sure her `hello@indielane.com.au` email is never affected.

Source request: Donna's email "Fwd: Share with Anthony for website build" (2026-08-27). Requested changes: combine Editorial + Lifestyle services, remove Family, add Weddings. Provided Squarespace, GoDaddy, Studio Ninja CRM, and ShootProof credentials. **Explicitly asked to wait for her signal before making changes to the live/proposed site.**

## Roles

- **Claude Code**: codes the site, manages the GitHub repo/Vercel project, prepares exact DNS records needed, documents rollback values.
- **CoWork**: performs the actual GoDaddy DNS edits and the Squarespace cancellation — the high-risk, hard-to-reverse, shared-infrastructure steps affecting Donna's live domain and email.
- **Donna**: confirms final service list/photos, gives the go-ahead signal, provides GitHub access, confirms test email receipt after cutover.

## Phase 0 — Information gathering (before touching anything)

- [ ] Check MX records for `indielane.com.au` to identify current email host (GoDaddy Email / Google Workspace / Squarespace Email).
- [ ] Check current DNS records at GoDaddy (A, CNAME, MX, TXT/SPF/DKIM) and record current TTLs — screenshot/save original values for rollback.
- [ ] Confirm what the Studio Ninja contact-form integration actually posts to, so the static rebuild preserves it (or plan a replacement, e.g. Formspree/Getform, since there's no backend).

## Phase 1 — Content updates to the proposal build (Claude Code)

- [x] Merge Editorial + Lifestyle into one service ("Editorial & Lifestyle").
- [x] Remove Family service (folded out when merging the old "Lifestyle & Family" card).
- [x] Add Weddings service.
- [ ] Get final photo selections from Donna — **placeholder photos reused for now** (see note below), swap once she sends selects.
- [x] Verify contact form still submits correctly; test in browser. **Found: form is front-end-only, does not actually submit to Studio Ninja or anywhere — see note below.**
- [x] Keep all of this on the proposal URL only — no changes to the live `indielane.com.au` site yet.

**Note on photos:** Per instruction to reuse existing photos for now rather than wait, the services grid in [index.html](index.html) was updated using photos already on the page: "Editorial & Lifestyle" reuses the old Lifestyle card's image (`Shaun_Nature...`), and the new "Weddings" card reuses the old standalone Editorial card's image (`Nikki_Soul+Potter...`) since no dedicated wedding photo exists in the current asset set. Flagged with an HTML TODO comment above the services grid. Still waiting on Donna's actual wedding/combined-service photo selections to swap in.

**Note on the contact form:** Confirmed via code (`index.html` around the `bookForm` submit handler) that the form is a static, front-end-only mock — it calls `preventDefault()` and just shows a success message; it does not POST anywhere. This matches this repo's stated convention (forms are demo-only until go-live), but it means the current build does **not** actually integrate with Studio Ninja yet.

**Studio Ninja embed — confirmed feasible now, doesn't need to wait for go-live.** Studio Ninja's contact form is an iframe/script embed generated from Settings → Contact Form in their dashboard; it loads from Studio Ninja's own domain regardless of what URL it's embedded on, so it can be wired into the current proposal build right away (source: [Ninja Academy — embedded Contact Form](https://help.studioninja.co/en/articles/2039694-how-do-i-use-the-embedded-contact-form)). Anthony has access to Donna's Studio Ninja account and is retrieving:
- [ ] Existing embed code for the form already linked from her Squarespace site (reuse it, don't create a new one, so leads keep landing in the same place).
- [ ] The field list on that form's Build tab, to match against our site's form fields.
- [ ] Configure tab: destination pipeline/stage, post-submit redirect/thank-you behavior, notification settings.
- [ ] Update the "Type of Photography" dropdown inside Studio Ninja to match the new service list (Branding Portraits, Commercial, Editorial & Lifestyle, Food & Product, Weddings, Event, Something else).
- [ ] Style tab: whether the embed can be recolored to match the site's dark theme or renders with Studio Ninja's own default styling.
- [ ] The actual embed snippet (safe to share — no credentials in it).

Do not share Donna's Studio Ninja login/password with Claude Code — only the embed snippet and the answers above are needed. Once received, swap the mock form for the real embed and test a live submission end-to-end.

**Update — embed received and integrated (2026-09-01).** CoWork retrieved everything from Studio Ninja:
- Confirmed the live "Contact Form" (not the "Contact Form copy") is the one already linked from Squarespace — edited that one.
- Field order: full name*, company, email*, phone*, type of photography* (dropdown), preferred date, message*, how did you hear about us*.
- New leads land as "NEW LEAD" under Open Leads; no redirect URL (uses inline thank-you text matching our existing messaging); no auto-responder; in-app + email notifications to Donna are on.
- The "Type of Photography" dropdown pulls from Studio Ninja's global Job Types list, not its own options. CoWork added 7 new Job Types (Branding Portraits, Commercial, Editorial & Lifestyle, Food & Product, Weddings, Event, Something else) and pointed the form at only those, leaving the old 8 types untouched for historical jobs.
- Style tab supports full theming (fonts, colors, field/button styling) to eventually match the dark site design.

Claude Code replaced the mock `bookForm` in [index.html](index.html) with the real Studio Ninja iframe embed + its `iframeResizer.js` script, removed the now-dead JS submit handler and the unused `.form-success` CSS rule, and verified both the form endpoint and resizer script return HTTP 200 and render correctly on a local static server. **Kept Studio Ninja's default (unstyled/light) look for now, per instruction** — flagged with a TODO comment in the HTML for a future theming pass using the Style tab. Did not submit a real test enquiry through the embed, since that would create an actual lead in Donna's live Studio Ninja account — if an end-to-end test is wanted, do one deliberate, clearly-labeled test submission and then delete/ignore that lead afterward.

Remaining for this item: theme the embed to match the site's dark design (optional, later); decide before go-live whether to keep the phone note text below the form.

**Update — theming request (2026-09-01).** User compared a screenshot of the live embed (Studio Ninja default light/blue styling) against the site's original dark design and asked for it to match. Confirmed this must be done in Studio Ninja's Style tab, not in our code, since the iframe is cross-origin (our CSS cannot reach inside it). Handed CoWork the exact values pulled from the site's own CSS variables to punch into that tab:

- Page background: `#2B2B2B` (site's `--bg-deep`)
- Label text: `#C9BBA9`, uppercase, small/bold if the font-weight option exists
- Field background: `#363636` (solid equivalent of the site's translucent `rgba(255,255,255,0.05)` on dark)
- Field border: `#565452` (solid equivalent of `rgba(237,230,219,0.22)`)
- Placeholder text: `#7F7C78` (solid equivalent of `rgba(237,230,219,0.4)`)
- Button background: `#B5A89E` (site's `--accent`), button text: `#FFFFFF`, uppercase if available
- Corner style: minimal/sharp, not the default rounded pill (~2-3px radius, matching the site's inputs/buttons)
- Font: Montserrat if selectable, otherwise closest available sans-serif
- Open question for CoWork to check while styling: Studio Ninja's Style tab list didn't mention a separate "field text" (typed value) color option — needs verifying live that typed text stays readable (light, e.g. `#F3ECE1`) against the new dark field background, not defaulting to dark-on-dark.

No further code changes needed on our side once this is set — the same embed snippet already in index.html will simply render with the new styling automatically.

**Update — reverted, important finding (2026-09-01).** CoWork applied the styling above, but it turned out Studio Ninja's Style tab styles the form itself, not a per-embed instance — since we're using the same live "Contact Form" that's already embedded on Donna's actual Squarespace site (confirmed earlier as the correct one to reuse, matching her real leads), restyling it also changed the look of the form on her **currently live, production** site. That's before she's approved anything or before the domain has moved to Vercel, so the style change was reverted back to Studio Ninja's original/default look for now.

**Decision:** leave the embed unstyled (default Studio Ninja look) in the proposal build until the actual go-live/domain cutover (Phase 3 of this plan). Only restyle it at that point, since by then the "live" and "proposal" versions will have merged into one site anyway and there's no longer a risk of the styling change leaking onto a site Donna hasn't approved yet.

**To do next time a "message Donna an update" request comes in:** proactively explain to her why the enquiry form in the proposal currently looks unstyled/off-brand (default Studio Ninja blue/white look instead of the site's dark theme) — it's intentional, not an oversight: that form is the same one already live on her actual site, and styling it early would change her real, currently-working site before she's signed off on the new design or before the domain has moved over. It'll be themed to match the new site properly as part of the final go-live step.

## Phase 2 — Repo & hosting setup (Claude Code)

- [ ] Once Donna signals go-ahead: create a GitHub repo under Donna's GitHub account (she creates account/repo, adds collaborator, or equivalent).
- [ ] Push the static site to that repo.
- [ ] Connect repo to Vercel (Hobby plan) under Donna's Vercel account.
- [ ] Deploy to a `*.vercel.app` preview URL; QA fully (forms, links, mobile, images) before touching DNS.

## Phase 3 — Domain cutover (GoDaddy → Vercel) — executed by CoWork

- [ ] Note: this is a DNS repoint, not a domain transfer — domain stays registered at GoDaddy throughout.
- [ ] Claude Code hands CoWork exact A/CNAME records from the Vercel dashboard.
- [ ] CoWork adds new records in GoDaddy without deleting existing Squarespace records yet.
- [ ] Do NOT touch MX/TXT/SPF/DKIM records — only A/CNAME for root/`www`.
- [ ] Wait for DNS propagation; verify live domain resolves to Vercel, SSL issues correctly, and test email to `hello@indielane.com.au` still works.

## Phase 4 — Squarespace cancellation — executed by CoWork

- [ ] Only after domain + email confirmed working for several days, CoWork cancels/downgrades Squarespace.
- [ ] Re-check email delivery and MX records immediately after cancellation.
- [ ] Keep rollback plan ready: revert GoDaddy DNS to original Squarespace values if anything breaks.

## Session Log

### 2026-09-01
- Drafted full migration plan (this document) based on Donna's 2026-08-27 email. No execution yet — plan only, per user request. Created this PLAN.md to track ongoing session progress automatically.
- Executed Phase 1 content updates on the proposal build only (not live site): merged Editorial + Lifestyle into one "Editorial & Lifestyle" service card, dropped Family, added a new Weddings card; updated the booking form's service dropdown to match. Reused existing site photos as temporary placeholders for the merged and new cards (flagged with a TODO comment in the HTML) since final photo selections from Donna are still pending. Verified structurally in the HTML and via a local static server that the page still renders correctly. Confirmed the booking form is currently a front-end-only mock with no real submission destination — it is not yet wired to Studio Ninja; flagged as an open item for before go-live.
- Researched Studio Ninja's embed mechanism (iframe/script generated from Settings → Contact Form, works on any domain including a not-yet-live one) and handed off a checklist of exactly what to retrieve from Donna's account, to be actioned by CoWork.
- CoWork retrieved the real embed code, field list, pipeline/notification behavior, and added 7 new Job Types in Studio Ninja to back the new service dropdown. Claude Code swapped the mock form in index.html for the real Studio Ninja iframe embed, removed the dead JS handler and unused CSS, and verified both embed URLs return HTTP 200 and render on a local server. Kept Studio Ninja's default unstyled look for now per instruction; theming to match the dark site is a follow-up.
- Provided CoWork an exact color/font/corner spec (pulled from the site's CSS) to theme the embed via Studio Ninja's Style tab. CoWork applied it, but this changed the look of the form on Donna's **currently live** Squarespace site too, since it's the same shared "Contact Form" record in Studio Ninja, not a per-embed style. Reverted back to default styling. Decision: leave it unstyled until the actual domain cutover in Phase 3, to avoid touching Donna's live site before she's signed off. Also need to proactively explain this to Donna in the next client update message, so the unstyled form in the proposal doesn't read as a mistake.
- Logged both rounds of Phase 1 work as client-facing changelog entries (v1.1 services + Studio Ninja connection, v1.2 the form-styling hold explanation) in [dashboard/indielanephotography.html](../../dashboard/indielanephotography.html)'s Changelog section, following the existing entry markup/tone already used as a template in dashboard/index.html. This is the message Donna will see on her dashboard, so v1.2 doubles as the proactive explanation of why the form still looks unstyled.
