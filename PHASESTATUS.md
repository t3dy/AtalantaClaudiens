# PHASESTATUS.md — Session Discipline Log

## Current Phase: 2 (Site Shell + Emblem Pages)
## Current Slice: 2A complete, 2B in progress
## Schema Version: 2

---

## Session: 2026-03-21 — Full Pipeline Built

### What Was Done
1. Created `init_db.py` — 5-table minimal schema (emblems, bibliography, source_authorities, scholarly_refs, emblem_sources) + schema_version
2. Created `seed_from_json.py` — ingests atalanta_fugiens_seed.json: 51 emblems, 10 bibliography, 15 authorities, 28 scholarly refs, 16 source links
3. Created `extract_dejong.py` — regex-based extraction from De Jong's 11,729-line markdown:
   - 44 emblem sections found
   - 37/50 with mottos, 31/50 with discourse summaries
   - 52 total scholarly refs, 182 emblem-source links
   - 13 emblems still missing (OCR too garbled for regex: X, XIV, XV, XVII, XIX, XXII, XXIV, XXXVI-XXXIX, XLI, XLVII, XLIX)
4. Created `site/style.css` — adapted HPMarginalia CSS (parchment theme, gallery, lightbox, comparative view, badges)
5. Created `site/script.js` — gallery loading, lightbox with keyboard nav
6. Created `build_site.py` — generates index.html (gallery), 51 emblem pages (comparative view), about.html, data.json
7. Verified site renders: gallery with 51 cards, stats, emblem detail pages with left/right panels

### Database Totals
- Emblems: 51 (37 with motto, 31 with discourse)
- Scholarly refs: 52
- Emblem-source links: 182
- Bibliography: 10
- Source authorities: 15

### Pipeline Command
```bash
rm db/atalanta.db
python scripts/init_db.py
python scripts/seed_from_json.py
python scripts/extract_dejong.py
python scripts/build_site.py
```

### Next Steps
1. Improve extraction for 13 missing emblems (LLM-assisted or manual page-range targeting)
2. Build scholars + bibliography pages (needs `scholars` table — schema migration)
3. Build dictionary pages (needs `dictionary_terms` table — schema migration)
4. Build timeline page (needs `timeline_events` table — schema migration)
5. Acquire public domain emblem images
6. Push to GitHub and deploy

### Blockers
- 13 emblems have OCR too garbled for regex extraction
- No emblem images yet (placeholder boxes showing Roman numerals)

### Warning Rules
- De Jong extraction found 37/50 — do NOT mark missing emblems as "no data exists"; the data is there, the OCR just needs different parsing
- CSS is adapted from HPMarginalia — maintain the same variable names for consistency
- All emblem pages exist (51 total including frontispiece) — even those without extracted data show "not yet extracted" message

---

## Session: 2026-03-21b — Extraction Fix: 50/50 Mottos

### What Was Done
1. Fixed dedup bug in `extract_dejong.py` — intro references (pos < 20000) were being chosen over real analysis sections. Now filters by position and sorts by file order.
2. Added garbled-header recovery — `(fig/fie N) MOTTO` pattern catches XXXVI, XLV, XLIX where EMBLEM word itself is OCR-garbled.
3. Made section markers OCR-tolerant — `SU.{0,6}ARY` for SUMMARY, `COM\s*M?\s*ENTARY` for COMMENTARY. Fixed XXXIX and XLI.
4. Replaced hardcoded `EMBLEM_PAGES` in `extract_dejong_pass2.py` with `derive_page_ranges()` — computes page ranges dynamically from actual emblem positions.
5. Added Emblem XVII to `atalanta_fugiens_seed.json` — motto garbled as `M GT1□ 0`, unrecoverable by regex.
6. Full pipeline rebuild: 50/50 mottos confirmed.

### Files Changed
- `scripts/extract_dejong.py` — dedup fix, recovery pass, OCR-tolerant patterns, `int_to_roman()` helper
- `scripts/extract_dejong_pass2.py` — `derive_page_ranges()`, OCR-tolerant SUMMARY pattern
- `atalanta_fugiens_seed.json` — Emblem XVII entry with motto and De Jong scholarly ref

### Database Totals
- Emblems: 51 (50/50 with motto, 34/50 with discourse)
- Scholarly refs: 60
- Emblem-source links: 119
- Dictionary terms: 23 (66 cross-links)
- Timeline events: 20
- Scholars: 11

### Pipeline Command
```bash
rm -f db/atalanta.db && python scripts/init_db.py && python scripts/migrate_v2.py && python scripts/seed_from_json.py && python scripts/seed_phase2.py && python scripts/extract_dejong.py && python scripts/extract_dejong_pass2.py && python scripts/link_dictionary.py && python scripts/build_site.py
```

### Next Steps
1. Fill remaining 16 discourse summaries
2. Create `extract_secondary.py` for Tilton, Pagel, Wescott
3. Improve emblem page scholarly apparatus
4. Essays content (Phase 3)

### Blockers
- 16 emblems still missing discourse summaries (OCR quality in later pages)
- No emblem images yet
- Secondary source extraction not started
