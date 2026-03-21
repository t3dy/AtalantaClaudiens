# PIPELINE.md — AtalantaClaudiens Script Execution Order

## Stage Overview

```
STAGE 1: SCAFFOLD     init_db.py → seed_from_json.py
STAGE 2: EXTRACT      extract_dejong.py → extract_secondary.py
STAGE 3: ENRICH       seed_dictionary.py → seed_timeline.py
STAGE 4: BUILD        build_site.py
STAGE 5: VALIDATE     validate.py
```

## Stage 1: Scaffold

### init_db.py
- **Input**: None (schema hardcoded)
- **Output**: `db/atalanta.db` with 18 empty tables
- **Idempotent**: Yes (`CREATE TABLE IF NOT EXISTS`)
- **Dependencies**: None

### seed_from_json.py
- **Input**: `atalanta_fugiens_seed.json`
- **Output**: Populates `emblems` (51 rows), `source_authorities`, `scholars`, `bibliography`, `scholarly_refs`, `emblem_sources`, `dictionary_terms`, `timeline_events`
- **Idempotent**: Yes (`INSERT OR IGNORE`)
- **Dependencies**: `init_db.py` must have run
- **Source method**: `SEED_DATA`

## Stage 2: Extract

### extract_dejong.py
- **Input**: De Jong markdown file (`atalanta fugiens/Helena Maria Elisabeth Jong...md`, 11,729 lines)
- **Output**: Updates `emblems` with mottos, epigrams, discourse summaries. Populates `scholarly_refs` and `emblem_sources` from De Jong's emblem-by-emblem analysis.
- **Method**: Regex boundary detection (`EMBLEM\s+[IVXLCDM]+`) for emblem sections, then structured extraction within each section.
- **Idempotent**: Yes (updates existing rows, inserts new refs with `INSERT OR IGNORE`)
- **Dependencies**: Stage 1 complete
- **Source method**: `CORPUS_EXTRACTION` for regex-parsed data, `LLM_ASSISTED` for semantic summaries
- **Confidence**: `HIGH` for motto/source identification, `MEDIUM` for discourse summaries

### extract_secondary.py
- **Input**: All other `.md` files in `atalanta fugiens/`
- **Output**: Additional `scholarly_refs` from Tilton, Craven, Wescott, Pagel, Miner, etc.
- **Method**: Source-specific parsing (each file has different structure)
- **Idempotent**: Yes
- **Dependencies**: `extract_dejong.py` (so emblem rows exist to reference)
- **Source method**: `CORPUS_EXTRACTION`
- **Confidence**: `HIGH` for explicit emblem references, `MEDIUM` for thematic matches

## Stage 3: Enrich

### seed_dictionary.py
- **Input**: Dictionary entries from seed JSON + De Jong terminology
- **Output**: `dictionary_terms` (60+ entries), `dictionary_term_links`, `term_emblem_refs`
- **Idempotent**: Yes
- **Dependencies**: Stage 2 (needs emblem IDs for cross-references)
- **Source method**: `SEED_DATA` for initial terms, `LLM_ASSISTED` for definitions

### seed_timeline.py
- **Input**: Timeline events from seed JSON + corpus dates
- **Output**: `timeline_events` (20+ entries)
- **Idempotent**: Yes
- **Dependencies**: Stage 1 (needs scholar/bibliography IDs)
- **Source method**: `SEED_DATA`

## Stage 4: Build

### build_site.py
- **Input**: `db/atalanta.db` (fully populated)
- **Output**: All HTML files in `site/`, plus `site/data.json`
- **Key functions**:
  - `page_shell()` — Wraps all pages with header/footer/nav
  - `nav_html()` — Navigation bar with active state
  - `export_data_json()` — Gallery data for lightbox
  - `build_emblem_gallery()` — Home page with stats
  - `build_emblem_pages()` — 51 comparative-view pages
  - `build_scholars_pages()` — Index + individual scholar pages
  - `build_dictionary_pages()` — Index + individual term pages
  - `build_timeline_page()` — Filterable timeline
  - `build_sources_page()` — Maier's sources by type
  - `build_essay_pages()` — Essay index + individual pages
  - `build_bibliography_page()` — Full citation list
  - `build_about_page()` — Project statistics
- **Idempotent**: Yes (overwrites all generated pages)
- **Dependencies**: All prior stages

## Stage 5: Validate

### validate.py
- **Input**: `db/atalanta.db` + `site/` directory
- **Output**: Validation report (stdout)
- **Checks**:
  1. All 51 emblems have at least one scholarly reference
  2. No duplicate dictionary slugs
  3. No orphaned term links
  4. All scholars have at least one linked work
  5. All bibliography entries have valid `af_relevance`
  6. All emblem HTML files exist in `site/emblems/`
  7. All images referenced in `data.json` exist on disk
  8. No broken internal links in generated HTML
  9. Confidence distribution report
  10. Review status summary
- **Dependencies**: Stage 4

## Full Rebuild Command

```bash
python scripts/init_db.py
python scripts/seed_from_json.py
python scripts/extract_dejong.py
python scripts/extract_secondary.py
python scripts/seed_dictionary.py
python scripts/seed_timeline.py
python scripts/build_site.py
python scripts/validate.py
```
