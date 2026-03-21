# PIPELINE.md — AtalantaClaudiens Script Execution Order

## Stage Overview

```
STAGE 1: SCAFFOLD     init_db.py → migrate_v2.py → migrate_v3.py → seed_from_json.py → seed_phase2.py
STAGE 2: EXTRACT      extract_dejong.py → extract_dejong_pass2.py
STAGE 3: ENRICH       link_dictionary.py → seed_emblem_analyses.py
STAGE 4: BUILD        build_site.py
STAGE 5: VALIDATE     (manual preview verification)
```

## Stage 1: Scaffold

### init_db.py
- **Input**: None (schema hardcoded)
- **Output**: `db/atalanta.db` with 6 core tables
- **Idempotent**: Yes (`CREATE TABLE IF NOT EXISTS`)

### migrate_v2.py
- **Input**: Existing database
- **Output**: Adds 6 Phase 2-3 tables (scholars, dictionary_terms, timeline_events, etc.)
- **Idempotent**: Yes (`CREATE TABLE IF NOT EXISTS`)

### migrate_v3.py
- **Input**: Existing database
- **Output**: Adds content enrichment columns: `emblems.analysis_html`, `dictionary_terms.label_latin`, `source_authorities.description_long`, `timeline_events.description_long`
- **Idempotent**: Yes (checks `PRAGMA table_info` before `ALTER TABLE`)

### seed_from_json.py
- **Input**: `atalanta_fugiens_seed.json`
- **Output**: Populates emblems (51), bibliography (10), source_authorities (15 + description_long), scholarly_refs (29), emblem_sources (16)
- **Idempotent**: Yes (`INSERT OR IGNORE` + conditional `UPDATE`)
- **Source method**: `SEED_DATA`

### seed_phase2.py
- **Input**: `atalanta_fugiens_seed.json`
- **Output**: Populates scholars (11), scholar_works (9), dictionary_terms (23 + label_latin + significance_to_af), term_emblem_refs (47), timeline_events (20 + description_long)
- **Idempotent**: Yes (`INSERT OR IGNORE` + conditional `UPDATE`)

## Stage 2: Extract

### extract_dejong.py
- **Input**: De Jong markdown (11,729 lines)
- **Output**: Updates emblems with mottos, epigrams, discourse summaries. Populates scholarly_refs and emblem_sources.
- **Method**: Regex boundary detection with OCR-tolerant patterns. Recovery pass for garbled headers via `(fig N) MOTTO` pattern.
- **Dedup**: Position-aware filtering (rejects intro-section false matches at pos < 20000)
- **Idempotent**: Yes
- **Source method**: `CORPUS_EXTRACTION`, confidence `HIGH`

### extract_dejong_pass2.py
- **Input**: De Jong markdown (same file)
- **Output**: Fills remaining NULL mottos/discourses using dynamically derived page ranges
- **Method**: `derive_page_ranges()` maps emblem positions to page numbers, extracts from page-range chunks
- **Idempotent**: Yes (only updates NULL fields)
- **Source method**: `CORPUS_EXTRACTION`, confidence `MEDIUM`

## Stage 3: Enrich

### link_dictionary.py
- **Input**: dictionary_terms + emblems in database
- **Output**: dictionary_term_links (cross-references between related terms)
- **Idempotent**: Yes

### seed_emblem_analyses.py
- **Input**: All database tables (emblems, scholarly_refs, emblem_sources, source_authorities, dictionary_terms, term_emblem_refs)
- **Output**: Assembles `analysis_html` for each emblem from DB fields. Template includes: Overview, Maier's Source Texts (cross-linked to sources page), Alchemical Significance, Related Terms (cross-linked to dictionary).
- **Idempotent**: Yes (overwrites analysis_html each run)
- **Source method**: `LLM_ASSISTED` (template assembly, no LLM call)

## Stage 4: Build

### build_site.py
- **Input**: `db/atalanta.db` (fully populated)
- **Output**: All HTML in `site/`, plus `site/data.json`
- **Key outputs**: 51 emblem pages (with analysis blocks), dictionary index + 23 term pages (with Latin), sources page (with rich cards + emblem badges), timeline (with rich descriptions), scholars, bibliography, essays index, about
- **Idempotent**: Yes (overwrites all pages)

## Stage 5: Validate

Manual verification via preview server:
1. `preview_start` → check console errors, network failures
2. Spot-check emblem pages (analysis block, cross-links)
3. Verify dictionary (Latin terms, significance)
4. Verify sources (descriptions, emblem badges)
5. Verify timeline (rich descriptions, sticky years)

## Future Stages (Planned)

### Stage 2b: Secondary Extraction
- `extract_tilton.py` — Parse Tilton (13,881 lines) for emblem-specific commentary
- `extract_secondary.py` — Parse Craven, Wescott, Pagel, Miner for additional refs
- **Method**: Single-pass LLM read (corpus fits in context)

### Stage 3b: Vision Analysis
- `analyze_emblem_images.py` — Batch Claude Vision analysis of emblem plate images
- **Output**: `emblems.visual_elements` (structured JSON of allegorical figures, symbols, composition)
- **Method**: Per-image LLM vision call, validated against De Jong's `image_description`

## Full Rebuild Command

```bash
rm -f db/atalanta.db
python scripts/init_db.py
python scripts/migrate_v2.py
python scripts/migrate_v3.py
python scripts/seed_from_json.py
python scripts/seed_phase2.py
python scripts/extract_dejong.py
python scripts/extract_dejong_pass2.py
python scripts/link_dictionary.py
python scripts/seed_emblem_analyses.py
python scripts/build_site.py
```
