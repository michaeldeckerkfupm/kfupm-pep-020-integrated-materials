# ENGL 020 Integrated Materials

ENGL020 practice materials adapted from Dan Oxley's Integrated Materials packet.

Static HTML, CSS and JavaScript, with local audio and source-page images. Reading answers, flags, vocabulary progress and writing notes are saved in the browser.

Open `index.html` to use the site. No build step is required.

Listening feedback follows the supplied packet keys, with verified corrections for L7.95: question 7 is “loves them”; question 9 is “3 hours”. Earlier first-attempt scores retain their original total. Reading image views show only passages, including continuation pages.

Cloudflare Workers Builds deploys main with `npx wrangler deploy`. The static asset configuration is in `wrangler.jsonc`.

Packet audit (1 November 2026): 42 readings, 668 multiple-choice questions, 671 integrated vocabulary entries and 480 Reading Explorer entries. The cover and standalone key pages are not separate student activities. All 22 picture-choice items display the original picture rows inline. Four reading continuations display as continuous passages. Writing links follow the 020 pacing schedule: reviews in Units 1–2, cause and effect in Units 2–4, for and against in Units 4–6, problem and solution in Units 6–8. Packet writing task names and numbering are retained, although the pacing schedule numbers cause/effect and for/against in the opposite order.

Source image quality (2 November 2026): all 253 original-page images are rendered directly from the matching V8 PDF at 2.4 pixels per PDF point (about 1430 pixels wide), instead of enlarging the earlier 804-pixel images. All 42 readings use 46 dedicated passage-only crops, following the ENGL010 source-rendering approach. Original layout, line numbers, and continuation stacking are retained. Rebuild with `python render_source_images.py "/path/to/ENGL021021 Integrated Materials V8.pdf"` using PyMuPDF and Pillow. The Word text was readable through Drive, but the 311 MB binary exceeded its 256 MB download limit, so rendering uses the companion original PDF.
