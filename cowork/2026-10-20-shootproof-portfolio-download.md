# CoWork prompt: download Donna's portfolio selects from ShootProof (2026-10-20)

Copy everything below the line into CoWork.

---

You're helping with the Indie Lane Photography website rebuild (client: Donna Nugent). Donna has curated her portfolio photos into one ShootProof gallery. I need every photo from that gallery downloaded to this computer, sorted into one folder per category, so Claude Code can optimise them and build the website's gallery pages.

**Gallery:** https://indielane.shootproof.com/gallery/ce3e86c1-85c1-401a-a190-1d8a595f42f0
(titled "2026 Website - Anthony". The client-view password is in Donna's email of 15 Oct 2026, "Indie Lane Photography - x 3 Gallery of images and Wording changes". You also already have Donna's ShootProof studio login from the original handover.)

The gallery should contain 6 albums (categories) with roughly 40-60 photos each.

## What to do

1. **Download the highest-resolution JPEGs for every album.**
   - Try the studio (photographer) side first: log in to Donna's ShootProof studio, open the gallery "2026 Website - Anthony", and use the gallery/album download option.
   - If that isn't available, use the client gallery link above with the password and its "Download all" option.
   - Download originals/high-res, not web-size or watermarked versions. If only watermarked files are offered, **stop and tell me** rather than downloading them.

2. **Save them into these exact folders**, unzipped, with the image files directly inside each folder (no nested subfolders, no zip files left behind):

   | ShootProof album (approx. name) | Folder |
   |---|---|
   | Branding | `D:\indielanephotographywebsite\_incoming\branding\` |
   | Commercial | `D:\indielanephotographywebsite\_incoming\commercial\` |
   | Editorial & Lifestyle | `D:\indielanephotographywebsite\_incoming\editorial-lifestyle\` |
   | Food & Products | `D:\indielanephotographywebsite\_incoming\food-product\` |
   | Weddings | `D:\indielanephotographywebsite\_incoming\weddings\` |
   | Events | `D:\indielanephotographywebsite\_incoming\events\` |

   If an album name doesn't clearly match one of these, or there are more or fewer than 6 albums, don't guess. Tell me what you found.

3. **Capture Donna's display order.** For each album, check whether the photos in the gallery appear in a custom order (Donna dragged them into an order) or simply sorted by filename/date.
   - If it's a custom order, create `order.txt` in that album's folder with one filename per line, in the exact order the gallery shows them (first photo first). Filenames must match the downloaded files exactly.
   - If it's just filename order, skip `order.txt` and tell me.

4. **Note each album's cover photo** if ShootProof shows one (the album thumbnail). Give me its filename per album.

## Rules

- **Read-only in ShootProof:** don't change any gallery settings, sorting, passwords, watermarks or download permissions, don't email or notify anyone, and don't touch any other gallery.
- Don't paste passwords or login details into your report.
- If you can't write to `D:\indielanephotographywebsite\_incoming\`, save to `Downloads\indielane-portfolio\<folder name>\` with the same structure and tell me the path.

## Report back

For each of the 6 folders: number of images saved, total size, whether `order.txt` was created (custom order) or not (filename order), and the cover photo filename. Also list anything skipped or unclear.
