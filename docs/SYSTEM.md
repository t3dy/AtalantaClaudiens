# SYSTEM.md — AtalantaClaudiens Architecture

## Data Flow

```
Source Corpus (.md files)
        │
        ▼
  Python Scripts (deterministic parsing + LLM-assisted extraction)
        │
        ▼
  SQLite Database (db/atalanta.db) ◄── Source of Truth
        │
        ▼
  build_site.py (static site generator)
        │
        ▼
  site/ (static HTML + CSS + JS + JSON)
        │
        ▼
  GitHub Pages (t3dy.github.io/AtalantaClaudiens)
```

## Provenance Model

Every generated datum carries three tracking fields:

| Field | Values | Meaning |
|-------|--------|---------|
| `source_method` | `DETERMINISTIC` | Derived from regex, formula, or filename parsing |
| | `CORPUS_EXTRACTION` | Extracted from source text by Python script |
| | `LLM_ASSISTED` | Generated or classified by LLM |
| | `HUMAN_VERIFIED` | Manually confirmed by a human |
| | `SEED_DATA` | Loaded from `atalanta_fugiens_seed.json` |
| `review_status` | `DRAFT` | Not yet reviewed |
| | `REVIEWED` | Reviewed but not verified against sources |
| | `VERIFIED` | Confirmed against primary/secondary sources |
| `confidence` | `HIGH` | Deterministic or verified |
| | `MEDIUM` | LLM-assisted or inferred |
| | `LOW` | Uncertain, needs validation |

### Rules
- LLM-extracted data starts as `DRAFT` / `MEDIUM`
- Deterministic data starts as `DRAFT` / `HIGH`
- Seed data starts as `SEED_DATA` / `MEDIUM`
- Only promote `review_status` forward (DRAFT → REVIEWED → VERIFIED)
- Never overwrite `VERIFIED` data without logging the discrepancy

## Operating Modes

### Mode 1: Pipeline (data ingestion)
Scripts run sequentially: init_db → seed → extract → enrich. See PIPELINE.md.

### Mode 2: Build (site generation)
`build_site.py` reads SQLite, generates all HTML. Deterministic and repeatable.

### Mode 3: Validate (QA)
`validate.py` checks for data completeness, orphaned references, broken links.

## Constraints

1. **Reality over design** — The database is truth. If docs contradict the DB, the DB wins.
2. **Outward not deeper** — Surface existing data before adding new extraction layers.
3. **No new specs without execution** — Build what's designed before designing more.
4. **De Jong is canonical** — Her emblem-by-emblem analysis is the primary anchor. Other scholars supplement.
5. **Emblem identification is deterministic** — Roman numeral patterns (I-L) are reliable across all sources.

## Technology Stack

| Component | Tool | Notes |
|-----------|------|-------|
| Database | SQLite 3 | Python stdlib, no ORM |
| Scripts | Python 3.10+ | Stdlib only (json, sqlite3, re, pathlib) |
| Site | HTML/CSS/JS | Vanilla, no frameworks, no build tools |
| Images | Public domain scans | BSB, Wellcome, or similar |
| Deployment | GitHub Pages | Static files served from `site/` |
| CI | GitHub Actions | On push: build + validate + deploy |

## Reference Projects

- **HPMarginalia** (`C:\Dev\hypnerotomachia polyphili`) — Architecture template. Same patterns: SQLite → Python → static HTML → GitHub Pages.
- **Furnace and Fugue** (`furnaceandfugue.org`) — Digital edition of the primary source. They handle text/image/music; we handle scholarship concordance. Complementary, not competitive.
