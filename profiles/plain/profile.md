# Profile: plain

Neutral document profile for English artifacts such as the product story. Built by `profiles/build_reference_docx.py plain`; change the `PROFILES["plain"]` entry there, rebuild, re-measure, and update this file.

## Calibration (the outline's budget uses this line)

**~420 words per page** for prose with `##` headings and a short list; **~400 with one small table**. Table overhead ≈ 15 words per row (header row included), beyond the words inside the table. Advisory: the preview render at step 12 and the final render at step 17 decide.

Measured 2026-09-28 with Word for Mac: 1,316-word English sample with title, five `##` sections and one list → 3.09 filled pages (426 words/page); the same plus a 4-row table → 3.33 pages (406). Words counted with `scripts/wordcount.py`, the same counter the outline caps use.

For a 3-page limit: 3 × 420 = 1,260 words is the ceiling with no slack; plan body caps at about 1,150–1,200 so the title block and one table fit.

Real-run reading (a product-story run): 1,157 prose words with one list → about 2.6 pages, about 445 words/page. 420 stays the planning figure (outline caps); 3 × 420 = 1,260 is the fit guardrail (outline `Fit guardrail:` line), the reading above which a preview is likely to fail; the rendered page count is binding (SKILL.md step 12 preview, step 17); every word-count reading is advisory once a preview passes.

## Minimum body size

**12 pt.** Never reduced to fit; overflow is a content defect.

## Typography and page

| Element | Setting |
|---|---|
| Page | A4, 1 in (2.54 cm) margins all sides |
| Body (Body Text, First Paragraph) | Calibri 12 pt, line 1.1, 6 pt after, left-aligned; keep lines together (E-3: a paragraph never splits across pages) |
| Lists (Compact) | Calibri 12 pt, 3 pt after; keep lines together (E-3) |
| Title (`# Title`) | 18 pt bold |
| Subtitle | 13 pt italic grey (only via a YAML `subtitle:` field; a plain italic line renders as body text) |
| Heading 1 (`##`) | 16 pt bold, keep with next |
| Heading 2 (`###`) | 13 pt bold, keep with next |
| Heading 3 (`####`) | 12 pt bold italic |
| Table | top/bottom rules, light row rules, bold header row, cells kept together on one page when they fit |
| Header | none |
| Footer | centered page number, 9 pt grey |

## Markdown conventions (pandoc)

- The first line `# Title` becomes the document Title (render uses `--shift-heading-level-by=-1`); `##` sections become Heading 1, `###` Heading 2.
- HTML comments (draft and freeze headers) are stripped before conversion and never render.
- Pipe tables become Word tables in the profile's table style. Pandoc does not use the Word "List Paragraph" style: list items are `Compact` (tight lists) or `Body Text` (loose lists) with Word numbering.
- Letter paper: change `page` to `(12240, 15840)` in the builder and re-measure.
