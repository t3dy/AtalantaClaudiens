# ROADMAP.md — AtalantaClaudiens Phase Status

## Phase 1: Extraction Core (Minimal Viable Pipeline)

Goal: init_db → seed → extract_dejong → verify data in SQLite. No site generation yet.

| Slice | Status | Notes |
|-------|--------|-------|
| 1A: Minimal schema (5 tables) | IN PROGRESS | `emblems`, `bibliography`, `source_authorities`, `scholarly_refs`, `emblem_sources` |
| 1B: Seed ingestion (emblems + authorities + bib) | READY | From `atalanta_fugiens_seed.json` — only emblem stubs, authorities, bibliography. Dict/timeline/scholars deferred. |
| 1C: De Jong extraction loop | READY | Parse De Jong .md, populate `scholarly_refs` and `emblem_sources` for all 50 emblems |
| 1D: Extraction verification | READY | SQL queries to verify coverage: refs per emblem, source counts, confidence distribution |

## Phase 2: Site Shell + Emblem Pages

| Slice | Status | Notes |
|-------|--------|-------|
| 2A: CSS + JS + page_shell | DEFERRED | Copy from HPMarginalia after extraction is solid |
| 2B: build_site.py (gallery + emblem pages) | DEFERRED | Needs Phase 1 data |
| 2C: Scholar + bibliography pages | DEFERRED | Needs `scholars` table (not in minimal schema) |

## Phase 3: Reference Apparatus

| Slice | Status | Notes |
|-------|--------|-------|
| 3A: Dictionary (60+ terms) | DEFERRED | Needs `dictionary_terms` table |
| 3B: Timeline (20+ events) | DEFERRED | Needs `timeline_events` table |
| 3C: Sources browsing page | DEFERRED | Source authorities exist in Phase 1; page generation deferred |
| 3D: Secondary scholar extraction | DEFERRED | Needs `scholars` table |

## Phase 4: Essays + Images + Deploy

| Slice | Status | Notes |
|-------|--------|-------|
| 4A: Image acquisition | BLOCKED | Public domain scans from BSB or similar |
| 4B: Essays (5 AI-drafted) | DEFERRED | Needs `essays` table |
| 4C: Validation + about page | DEFERRED | Needs build_site.py |
| 4D: GitHub Pages deploy | DEFERRED | Needs built site |

## Deferred Schema (added when needed)

| Table | Deferred To | Reason |
|-------|------------|--------|
| `scholars` | Phase 2C | Not needed for extraction loop |
| `scholar_works` | Phase 2C | Join table for scholars ↔ bibliography |
| `dictionary_terms` | Phase 3A | Dictionary is downstream of extraction |
| `dictionary_term_links` | Phase 3A | Cross-references between terms |
| `term_emblem_refs` | Phase 3A | Term ↔ emblem links |
| `timeline_events` | Phase 3B | Timeline is downstream |
| `editions` | Phase 3B | Edition history is downstream |
| `alchemical_processes` | Phase 3C+ | Multi-register model, needs extraction first |
| `emblem_processes` | Phase 3C+ | Join table |
| `visual_elements` | Phase 4+ | Image-text concordance, needs images |
| `mythological_figures` | Phase 4+ | Figure entities, needs full extraction |
| `emblem_figures` | Phase 4+ | Join table |
| `essays` | Phase 4B | AI-drafted essays |

## Research Artifacts (Completed)

| Artifact | Status | Location |
|----------|--------|----------|
| SCHOLARSHIPREPORT.md | BUILT | Root directory |
| atalanta_fugiens_seed.json | BUILT | Root directory |
| GPTAF.txt | BUILT | Root directory (prior session) |
| GPTPIPE.txt | BUILT | Root directory (prior session) |
| Furnace & Fugue analysis | BUILT | In conversation history |
| HPMarginalia architecture study | BUILT | In conversation history |
