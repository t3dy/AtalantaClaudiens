# VALIDATION_ARCHITECTURE.md — Three-Layer Data Integrity System

## Problem Statement

The current system conflates three distinct data layers into the same tables:
1. **Canonical** (scholarly ground truth from De Jong et al.)
2. **Candidate** (regex/LLM-extracted, probabilistic, incomplete)
3. **Published** (what appears on the site)

This means unvalidated regex output is presented as authoritative scholarly content.

## Architecture

```
                CANONICAL LAYER                    CANDIDATE LAYER
              ┌──────────────────┐              ┌──────────────────┐
              │ emblem_desc_     │              │ emblem_desc_     │
              │   scholarly      │              │   candidate      │
              │                  │              │                  │
              │ (De Jong, Tilton,│              │ (regex pass 1/2, │
              │  Craven, etc.)   │              │  LLM fallback,   │
              │                  │              │  future imports)  │
              └────────┬─────────┘              └────────┬─────────┘
                       │                                  │
                       └──────────┬───────────────────────┘
                                  │
                                  ▼
                       ┌──────────────────┐
                       │ emblem_alignment  │
                       │                  │
                       │ similarity_score │
                       │ status:          │
                       │  CONFIRMED       │
                       │  FLAGGED         │
                       │  UNVERIFIED      │
                       └────────┬─────────┘
                                │
                          PROMOTION GATE
                          (rules below)
                                │
                                ▼
                       ┌──────────────────┐
                       │ PUBLISHED LAYER  │
                       │                  │
                       │ emblems (updated)│
                       │ scholarly_refs   │
                       │ emblem_sources   │
                       │                  │
                       │ → build_site.py  │
                       └──────────────────┘
```

## Layer Definitions

### Canonical Layer (`emblem_desc_scholarly`)
- **What**: Structured scholarly descriptions extracted from primary/secondary sources
- **Source**: De Jong's emblem-by-emblem analysis, Tilton, Craven, Wescott, Pagel, Miner
- **Trust level**: HIGH (human scholarship, peer-reviewed)
- **Mutability**: Append-only. Never overwrite. New scholarship adds rows, doesn't replace.

### Candidate Layer (`emblem_desc_candidate`)
- **What**: Machine-extracted or LLM-generated descriptions
- **Source**: regex extraction (pass 1/2), LLM fallback, future OCR improvements
- **Trust level**: UNVERIFIED until compared against scholarly layer
- **Mutability**: Can be regenerated, replaced, or discarded

### Alignment Layer (`emblem_alignment`)
- **What**: Comparison results between candidate and scholarly descriptions
- **Purpose**: Determine whether candidate data is trustworthy enough to publish
- **Output**: CONFIRMED (publishable), FLAGGED (needs review), UNVERIFIED (no comparison yet)

### Published Layer (existing `emblems` + `scholarly_refs` + `emblem_sources`)
- **What**: Only data that has passed the promotion gate
- **Rule**: ONLY promoted data OR seed data appears here
- **Build**: `build_site.py` reads only from this layer

## Comparison Engine

### Method: Keyword Overlap (Phase 1)
No external dependencies. Works with stdlib only.

1. **Tokenize** both scholarly and candidate descriptions
2. **Normalize** (lowercase, strip punctuation, remove stopwords)
3. **Extract key terms** (nouns, proper nouns, alchemical vocabulary)
4. **Compute Jaccard similarity** on term sets: |A ∩ B| / |A ∪ B|
5. **Boost** for matching source authority IDs (weighted heavily)

### Thresholds
| Score | Status | Action |
|-------|--------|--------|
| ≥ 0.4 + authority match | CONFIRMED | Auto-promote to published |
| 0.2 - 0.4 | FLAGGED | Log for human review |
| < 0.2 | UNVERIFIED | Do not promote |
| No scholarly desc exists | UNVERIFIED | Cannot validate, hold in candidate |

### Failure Modes
- **False positive** (CONFIRMED but wrong): Mitigated by authority matching — if candidate cites the same source traditions as scholarly, likely correct
- **False negative** (FLAGGED but correct): OCR noise reduces keyword overlap. FLAGGED items are reviewed, not discarded
- **No comparison possible**: If no scholarly description exists for an emblem, candidate data stays UNVERIFIED permanently

## Promotion Rules

1. **CONFIRMED candidates** may update published tables automatically
2. **FLAGGED candidates** are logged in `emblem_alignment` for human review
3. **UNVERIFIED candidates** never reach published tables
4. **VERIFIED data in published tables is NEVER overwritten** — discrepancies are logged
5. **Seed data** in published tables remains until superseded by CONFIRMED data
6. **Promotion is logged** with timestamp and method in `emblem_alignment`

## Pipeline Stages (Refactored)

```
STAGE 1: SCAFFOLD       init_db.py, migrate_v2.py, migrate_v3.py
STAGE 2: SEED            seed_from_json.py, seed_phase2.py
STAGE 3: SCHOLARLY       ground_scholarly.py        ← NEW
STAGE 4: EXTRACT         extract_dejong.py → emblem_desc_candidate
                         extract_dejong_pass2.py → emblem_desc_candidate
STAGE 5: VALIDATE        validate_alignment.py      ← NEW
STAGE 6: PROMOTE         promote_candidates.py      ← NEW
STAGE 7: BUILD           build_site.py
STAGE 8: AUDIT           validate.py (existing QA)
```

Key change: extract scripts now write to `emblem_desc_candidate`, NOT directly to `emblems`.
`promote_candidates.py` is the only script that writes to `emblems` from extracted data.
