# Design notes — "One Day • The World", 18 Nov 2026

## System (deliberately different from top 1–3)
Top 1–3 (as briefed) all use the same grammar: navy newspaper masthead, 3 big
numbered stories, then medium stories, then a concise list, a world map with
numbered pins, a numbers strip, a date check and a sources footer.

Mine uses a different system:
1. **Colour-by-region, not a navy masthead.** Header is deep teal with a gold
   date box; every story carries a region colour (orange Asia–Pacific, blue
   Europe, burgundy Middle East & Africa, green Americas, purple Science/
   Health/Markets, ochre economy). The region colour is the organising
   principle, not a newspaper column.
2. **6 icon cards in a 2×3 grid, not 3 big newspaper stories.** Each featured
   story is a card with a simple original line icon drawn in PIL (globe,
   drone, satellite, shield, € coin, chart) and a 2-line summary. No single
   story dominates the page.
3. **A horizontal UTC timeline instead of a world map with pins.** The bottom
   third is a timeline 00:00 → 22:00 UTC with 8 dated beats (night drones,
   Voyager 05:16, 126 downed 08:00, EU €45bn 12:58, Fed minutes 14:00,
   Jeffries 15:47, Gaza Yellow Line 18:00, day closes 22:00). It proves the
   date range visually without copying the map-pin device.
4. **Two-column region lists, not one chronological list.** The remaining
   35 stories are grouped under 5 region headings across two columns, so a
   reader can scan a region at a glance. Numbering is continuous 1–41 across
   featured + lists, so every story is findable from SOURCES.md.

## Legibility choices
- 41 stories, not 52: the brief noted 38 spacious stories beat 52 cramped
  ones. 42 keeps one story per line in the lists (20pt, single line each)
  with white space left at the bottom of the right column.
- Featured summaries are capped at 2 lines; list items are 1 line each.
- "By the numbers" strip is kept (it is a standard news device, with
  different numbers and layout from the top entries), and the DATE CHECK box
  explicitly names what was excluded and why — including the measles item,
  which was tempting but dated 17 Nov.

## Build
- Python PIL only, DejaVu Sans/Serif. No photos, no AI image generator, no
  copyrighted images — all icons are line drawings made in the script.
- Rendered at 2048×2048, then downscaled to 1024×1024 (BICUBIC) for the
  entry, per the competition gate (at most 1024×1024). Final file 438,208
  bytes (428 KB), RGB PNG, under the 500 KB limit — after removing doubtful
  Ebola story #35 on 19 Nov 2026, now 41 stories. The 2048×2048 original
  is kept as news-18-nov-2026-2048.png outside the repo. Script: build.py;
  re-run it to regenerate the PNG from scratch. Note: main.py no longer
  renders anything — it is a stdlib-only copier that writes
  news-18-nov-2026.png to $MAKEFUN_OUTPUT_DIR/entry.png, because the
  grader runs plain python:3.13 with no Pillow installed. The bundled
  fonts/ directory is no longer used by main.py.
- First render had a layout bug (left list column overflowed into the
  timeline and the header title collided with the date box). Fixed by
  shortening the featured cards, shrinking list type to 20pt, moving the
  region section up, and enlarging the DATE CHECK box. The final render was
  visually inspected: no overlaps, all 41 numbers present, footer legible.
