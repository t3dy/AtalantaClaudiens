# ROADMAP.md — AtalantaClaudiens Phase Status

*Updated 2026-03-21. See HIROREBUILD.md for detailed next-phase plan.*
*For document routing, see DOCUMENTAIRTRAFFICCONTROL.md.*

## Phase 1: Extraction Core — COMPLETE

| Slice | Status | Notes |
|-------|--------|-------|
| 1A: Schema (v1-v4, 13 tables) | BUILT | init_db → migrate_v2 → migrate_v3 → migrate_v3_identity |
| 1B: Seed ingestion | BUILT | 51 emblems, 10 bib, 15 authorities, 38 dict terms, 29 timeline, 11 scholars |
| 1C: De Jong extraction | BUILT | 49 sections by regex, 50/50 mottos, 50/50 discourses |
| 1D: Pass 2 gap filling | BUILT | Dynamic page ranges, 3 hard cases resolved by end-boundary widening |

## Phase 2: Site Shell — COMPLETE

| Slice | Status | Notes |
|-------|--------|-------|
| 2A: CSS + JS + page_shell | BUILT | Parchment theme, gallery, lightbox, comparative view, badges |
| 2B: Emblem pages (51) | BUILT | Analysis blocks, cross-links to sources + dictionary |
| 2C: Scholar pages (11) | BUILT | Profiles with overviews and linked works |
| 2D: Dictionary (38 terms) | BUILT | Latin forms, AF significance, emblem links |
| 2E: Timeline (29 events) | BUILT | Rich descriptions, Rosicrucian context events |
| 2F: Sources page | BUILT | Rich cards, emblem badges, type-colored borders |
| 2G: Bibliography (10) | BUILT | Annotated entries with relevance badges |
| 2H: Biography page | BUILT | 6 sections on Maier's life |
| 2I: GitHub Pages deploy | BUILT | t3dy/AtalantaClaudiens, CI via Actions |

## Phase 3A: Identity + Enrichment — COMPLETE

| Slice | Status | Notes |
|-------|--------|-------|
| 3A1: Emblem identity layer | BUILT | 51 rows, 51 images on disk (Wikimedia Commons), ~24 HIGH confidence |
| 3A2: Analysis blocks (50/50) | BUILT | Template assembly with cross-links |
| 3A3: Alchemical stage classification | BUILT | 31/50 classified |
| 3A4: Home page intro + Start Here | BUILT | Introductory paragraph + button |

## Phase 3B: Secondary Sources — READY

| Slice | Status | Notes |
|-------|--------|-------|
| 3B1: Tilton extraction (13,881 lines) | READY | Script needed, single-pass LLM read |
| 3B2: Craven extraction (6,483 lines) | READY | Biographical detail for Maier |
| 3B3: Other scholars (Wescott, Pagel, Miner) | READY | Smaller files, targeted extraction |

## Phase 4: Content Enrichment — READY

| Slice | Status | Notes |
|-------|--------|-------|
| 4A: Latin mottos (49/50 missing) | READY | Extract from OCR or seed manually |
| 4B: definition_long (38/38 empty) | READY | Writing swarm for extended definitions |
| 4C: Multi-register definitions | READY | Schema needs `registers` column |
| 4D: Visual element descriptions | BLOCKED | Needs image analysis pipeline or manual |
| 4E: Remaining 19 alchemical stages | READY | Manual/LLM classification |

## Phase 5: Images — MOSTLY COMPLETE

| Slice | Status | Notes |
|-------|--------|-------|
| 5A: Source emblem plate images | BUILT | 51/51 images on disk via Wikimedia Commons (see IMAGEFOLLIES.md for lessons) |
| 5B: Image-emblem verification | READY | ~24 HIGH confidence, remainder need visual verification |
| 5C: Vision analysis pipeline | READY | Needs `analyze_emblem_images.py` script + Claude Vision |

## Phase 6: Pedagogical Layer — PLANNED

| Slice | Status | Notes |
|-------|--------|-------|
| 6A: 5 thematic essays | PLANNED | After Tilton extraction |
| 6B: Source x Emblem matrix visualization | PLANNED | JS + existing data |
| 6C: Thematic browse modes | PLANNED | By stage, source, figure |
| 6D: Search functionality | PLANNED | Client-side JS |
| 6E: Guided pathways ("How to Read") | PLANNED | After essays |

## Reports & Analysis (23 documents)

| Report | Purpose |
|--------|---------|
| HIROREBUILD.md | Master architecture plan (8 layers, 43 atoms) |
| DESIREDIMPROVEMENTS.md | 20-priority improvement list |
| PRISPEDAGOGYREPORT.md | Section-by-section pedagogical audit |
| AFSTYLING.md | Template and style guide |
| DOWEREALLYNEEDARAG.md | RAG analysis (verdict: No) |
| DECKARDTILT.md | Tilton ingestion boundary plan |
| HARDOCRCASES.md | OCR method analysis |
| SWARMWRITING.md | Swarm methodology |
| Swarm*Audit.md (4) | Schema, pipeline, content, provenance audits |
| HIRO321TUNEUP.md | Infrastructure audit |
| Others (7) | TRIALANDERROR, REFLAYERAF1, DECKARDAF1, HANDOVER, etc. |
