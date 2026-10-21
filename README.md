# Old Oak Tree website redesign

Redesign concept for The Old Oak Tree, South Kilvington, Thirsk (oldoaktreethirsk.co.uk), built 21 October 2026
from the pub's own content and photographs. Live preview: https://claude.ai/artifact/1NKdQcAc49jVhXEHg8qt7w

## What is here

- `index.html` and ten other pages: menu, Sunday lunch, rooms, private dining, race days, local area, news, contact, privacy, terms.
- `images/`: every photograph from the current site, resized and re-encoded (1.7 MB in total). The 527x210 panoramic
  shots are the pub's own slideshow images and are the only photos they have at that size, so they are shown small.
- `build_site.py`: regenerates every page from the content at the top of the script and from `../content/api.json`
  (the pub's WordPress pages, posts and media, pulled from its public API). Run `python3 build_site.py ../content/api.json`.
- `../content/current-site-inventory.md`: a plain-text inventory of the current site, page by page.

## Content notes for the pitch

- Every menu item, price, room rate, fixture date, attraction and news post comes from the current site. Spelling was
  tidied (feta, béchamel, jalapeños); nothing was invented.
- The two closure dates and the Chinese Banquet 2027 notice are live on the pub's site as of 21 October 2026.
- The booking enquiry form is a front-end demo only; it needs a form handler (or an email service) before launch.
- Rooms book through the pub's existing eviivo page (via.eviivo.com/OldYO72NL), which the site links to.
- The privacy policy still cites the Data Protection Act 1998 and should be refreshed for UK GDPR before launch.
- The current site links two Christmas menu PDFs dated 2011; they were left out.
- The old site uses a Google Maps iframe; this version uses the pub's own map image plus an "Open in Google Maps" link,
  so it works anywhere, including inside the preview.
- Photos worth asking the pub for: a few high-resolution shots of the bar, the garden, the rooms and plates of food.
  The current images are small (most are 527x210) and limit how large they can be shown.

## Design

- Palette taken from the pub's existing branding: deep burgundy for actions, cream pages, brass for labels. Both light
  and dark colour schemes are included.
- Type: Cinzel for the wordmark (matching the inscriptional capitals in the pub's logo), Libre Caslon Text for headings,
  Source Sans 3 for text. All from Google Fonts.
- Fully responsive, no horizontal scrolling at phone width, sticky header with a tap-to-call button.
