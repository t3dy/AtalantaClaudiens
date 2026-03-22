# Claude Code Instructions — AtalantaClaudiens

## Project Summary

Digital humanities website showcasing H.M.E. De Jong's scholarship on Michael Maier's *Atalanta Fugiens* (1618). Architecture replicates HPMarginalia: SQLite source of truth, Python static site generator, vanilla HTML/CSS/JS, GitHub Pages deployment at `t3dy/AtalantaClaudiens`.

## Document Routing

**Read `DOCUMENTAIRTRAFFICCONTROL.md` when you need to find the right file.** It routes you to the correct document for any task (schema work, emblem work, extraction, debugging, planning) and flags what's stale or unbuilt.

## Quick Reference

| Document | Purpose |
|----------|---------|
| `DOCUMENTAIRTRAFFICCONTROL.md` | **Start here** — routes you to the right doc for any task |
| `docs/SYSTEM.md` | Architecture, data flow, provenance model |
| `docs/ONTOLOGY.md` | Database schema (13 built + 7 planned tables), entity relationships |
| `docs/PIPELINE.md` | Script execution order (13 scripts), stage dependencies |
| `docs/INTERFACE.md` | Website sections, page templates, navigation |
| `docs/ROADMAP.md` | Phase status: BUILT / READY / BLOCKED / PLANNED |
| `PHASESTATUS.md` | Session discipline log — update at end of every session |
| `SCHOLARSHIPREPORT.md` | Corpus analysis, ontology design recommendations |
| `atalanta_fugiens_seed.json` | Structured seed data for database ingestion |

## Swarm Operations

**Read `docs/SWARMGUIDELINES.md` before launching ANY background agents.** Background agents CANNOT run Bash/Python. Use the staging-file pattern or pre-queried data pattern instead. The guidelines document three working patterns and three anti-patterns with concrete examples.

## Emblem Writing Standard

**Read `docs/WRITING_TEMPLATES.md` before writing ANY emblem content.** It defines the canonical 4-section analysis template (The Plate, Maier's Discourse, De Jong's Source Analysis, Scholarly Perspectives) with museum-level curation standards, anti-patterns, and DB field contracts. All emblem descriptions must follow this template.

## Emblem Reference (read these before emblem work)

- **`EMBLEMGUIDE.md`** — Complete agent reference: all 51 emblems table, data flow, how to find/add/update emblem data, image sourcing status, cross-reference patterns
- **`data/emblem_manifest.json`** — Canonical identity index (JSON, machine-readable)

Before working with any emblem, **read `EMBLEMGUIDE.md` first, then `data/emblem_manifest.json`**.
This is the canonical index of all 51 emblems. It contains:
- Emblem number (0-50), Roman numeral, Latin and English mottos
- Confirmed image filename and source (`image_confirmed: true/false`)
- Slots for page mapping, Wikimedia file, and Furnace & Fugue URL

**Rules:**
- If the manifest says an image is confirmed, trust it — do not re-source.
- If `image_confirmed` is false, the emblem needs an image sourced.
- Do NOT guess image mappings — update the manifest only with verified data.
- Any agent working with emblems should read this file FIRST.

## Data Flow Direction

```
data/emblem_manifest.json  ←  AGENTS EDIT HERE (canonical)
        ↓
seed_identity.py           →  emblem_identity table in SQLite
        ↓
build_site.py              →  static HTML (reads from DB)
```

The manifest is the single source of truth for emblem identity. Agents and humans edit the manifest. The pipeline syncs it to SQLite. The build reads from SQLite. Changes flow ONE direction: manifest → DB → HTML.

## Seed Data Structure

Seed data is split into domain-specific files in `data/`:
- `data/emblem_manifest.json` — Emblem identity (canonical, 51 entries)
- `atalanta_fugiens_seed.json` — All other seed data (emblems, bibliography, scholars, dictionary, timeline, source authorities)

When the seed JSON grows beyond manageable size, split further into `data/scholars.json`, `data/dictionary.json`, etc.

## Corpus Reading Pattern (for agents)

When an agent needs to consult the source PDFs/markdown for research:

1. **Grep** for keywords in `atalanta fugiens/*.md` to find relevant passages
2. **Read** the relevant section (with offset/limit to stay focused)
3. **Synthesize** a scholarly paragraph from what was read
4. **Store** with `source_method='LLM_ASSISTED'`, `confidence='MEDIUM'`, `review_status='DRAFT'`

The entire corpus (~547K tokens) fits in Claude's 1M context window. No RAG, no embeddings, no chunking. Just read the files.

## Vision Analysis (on-demand, not every build)

`scripts/analyze_emblem_images.py` (planned) runs Claude Vision on emblem plates to generate visual element descriptions. This script:
- Reads the manifest to find emblems with images but no visual_elements
- Sends each plate to Claude Vision for structured description
- Stores results in `emblems.visual_elements` (JSON)
- Is called EXPLICITLY when new images are added, NOT on every build

## Architecture Constraints

1. **SQLite is the source of truth.** Python scripts generate JSON and static HTML pages. No runtime dependencies.
2. **No frameworks.** Vanilla HTML/CSS/JS only. No React, no build tools, no npm.
3. **Provenance on every datum.** All generated content carries `source_method`, `review_status`, `confidence`. AI-generated content is explicitly marked.
4. **Idempotent scripts.** Every script uses `CREATE TABLE IF NOT EXISTS`, `INSERT OR IGNORE`, and can be re-run safely.
5. **Deterministic before LLM.** Parse structure deterministically first. Use LLM only for semantic extraction. Never trust LLM output without validation.

## Operating Rules

### Before Starting Work
- Check `PHASESTATUS.md` for current phase, prerequisites, blockers
- Check `docs/ROADMAP.md` for what's BUILT vs READY vs BLOCKED
- Read `docs/ONTOLOGY.md` if touching the database

### During Work
- Mark tasks in progress in PHASESTATUS.md
- Don't skip phases — each phase's outputs feed the next
- If schema changes, update `docs/ONTOLOGY.md` immediately
- If pipeline changes, update `docs/PIPELINE.md` immediately

### At End of Session
- Update `PHASESTATUS.md` with: phase status, what changed, next steps, blockers

### Data Integrity Rules
- Never overwrite data with `review_status='VERIFIED'` — log discrepancies instead
- LLM-extracted data starts as `review_status='DRAFT'`, `confidence='MEDIUM'`
- Deterministic data starts as `confidence='HIGH'`
- De Jong is the canonical anchor for emblem analysis — other scholars supplement

## Emblem Identification

The 50 emblems use Roman numerals I-L consistently across all scholars. The frontispiece is modeled as Emblem 0. Identification is deterministic — regex patterns for `EMBLEM\s+[IVXLCDM]+` reliably detect boundaries in De Jong's text despite OCR artifacts.

## Key Design Decisions

- **Comparative view** on emblem pages: original source LEFT, scholarly apparatus RIGHT
- **Multi-register process model**: alchemical processes are symbolic clusters (material, medical, spiritual, cosmological), NOT laboratory steps
- **Source authorities as first-class entities**: De Jong's central contribution is identifying Maier's sources. Each source tradition (Turba, Rosarium, Tabula Smaragdina, etc.) is a navigable entity.
- **Frontispiece as Emblem 0**: The title-page engraving is the interpretive key to the entire work
- **Public domain images**: Emblem plates sourced from BSB or similar, NOT from Furnace & Fugue (CC BY-NC-ND)
- **Essays AI-drafted**: Clearly marked with review badges. 5 topics from corpus synthesis.

## Website Sections

| Tab | Path | Content |
|-----|------|---------|
| Home | `/index.html` | Emblem gallery (51 thumbnails), stats, lightbox |
| Emblems | `/emblems/emblem-01.html` | Comparative view: image+text LEFT, scholarship RIGHT |
| Scholars | `/scholars.html` + `/scholar/*.html` | 11+ scholar profiles with works and emblem coverage |
| Dictionary | `/dictionary/index.html` + `/dictionary/*.html` | 60+ alchemical terms in 6 categories |
| Timeline | `/timeline.html` | Reception history 1568-2020, filterable |
| Sources | `/sources.html` | Maier's source traditions by type, linked to emblems |
| Essays | `/essays/index.html` + `/essays/*.html` | 5 AI-drafted essays, marked as generated |
| Bibliography | `/bibliography.html` | 10+ sources with relevance badges |
| About | `/about.html` | Stats, methodology, provenance, AI disclosure |

## CSS Design System

Replicate HPMarginalia's CSS variables:
```css
--bg: #f5f0e8;           /* Warm parchment */
--bg-card: #fff;
--text: #2c2418;          /* Dark brown */
--text-muted: #6b5d4d;
--accent: #8b4513;        /* Burnt sienna */
--accent-light: #d4a574;  /* Tan highlight */
--header-bg: #2c2418;
--header-text: #f5f0e8;
--border: #d4a574;
```

## Planning Discipline

This project uses the PKD Planning Protocol from the parent workspace (`C:\Dev\CLAUDE.md`):

- **Scope**: `/plan-joe-chip-scope` before new features
- **Slice**: `/plan-runciter-slice` for vertical slices with acceptance gates
- **Park ideas**: `/plan-abendsen-parking` when new ideas emerge during building
- **Gate check**: `/plan-steiner-gate` before starting each new phase

## File Structure

```
C:\Dev\Claudiens/
├── CLAUDE.md                      # This file — project entry point
├── DOCUMENTAIRTRAFFICCONTROL.md   # LLM routing guide — which doc to read for which task
├── PHASESTATUS.md                 # Session discipline log
├── EMBLEMGUIDE.md                 # Agent reference for emblem work (all 51 emblems)
├── README.md                      # Public-facing summary
├── SCHOLARSHIPREPORT.md           # Corpus analysis (research artifact)
├── atalanta_fugiens_seed.json     # Seed data for DB (research artifact)
├── GPTAF.txt                      # Prior ChatGPT extraction (reference)
├── GPTPIPE.txt                    # Pipeline design conversation (reference)
├── requirements.txt
├── .gitignore
├── .github/workflows/deploy.yml
├── .claude/
│   ├── launch.json                # Local preview server config
│   └── settings.local.json        # Permission whitelist
├── db/
│   └── atalanta.db                # SQLite database (generated)
├── scripts/
│   ├── init_db.py                 # Stage 1: Schema creation (v1)
│   ├── migrate_v2.py              # Stage 1: Add Phase 2-3 tables
│   ├── migrate_v3.py              # Stage 1: Content enrichment columns
│   ├── migrate_v3_identity.py     # Stage 1: Emblem identity table
│   ├── seed_from_json.py          # Stage 1: Ingest seed data
│   ├── seed_phase2.py             # Stage 1: Scholars, dictionary, timeline
│   ├── seed_identity.py           # Stage 1: Emblem identity layer
│   ├── extract_dejong.py          # Stage 2: Parse De Jong markdown
│   ├── extract_dejong_pass2.py    # Stage 2: Fill gaps by page range
│   ├── link_dictionary.py         # Stage 3: Cross-link dictionary terms
│   ├── seed_emblem_analyses.py    # Stage 3: Assemble analysis HTML
│   ├── build_site.py              # Stage 4: Generate static HTML
│   └── validate_identity.py       # Stage 5: Identity layer validation
├── docs/
│   ├── SYSTEM.md                  # Architecture + provenance model
│   ├── ONTOLOGY.md                # Database schema catalog
│   ├── PIPELINE.md                # Script execution order
│   ├── INTERFACE.md               # Website sections + templates
│   ├── ROADMAP.md                 # Phase status tracking
│   ├── WRITING_TEMPLATES.md       # Voice rules + page templates
│   ├── SCHOLAR_SPEC.md            # Scholar page specification
│   ├── TIMELINE_SPEC.md           # Timeline event model
│   └── archive/                   # Past planning artifacts
├── data/
│   ├── emblem_manifest.json       # Canonical emblem identity index (agents edit this)
│   └── emblem_identity_seed.json  # Legacy seed (superseded by manifest)
├── staging/                       # Swarm agent outputs before merge
├── site/
│   ├── index.html                 # Gallery home (intro + Start Here)
│   ├── data.json                  # Gallery data (generated)
│   ├── style.css                  # Main styles
│   ├── script.js                  # Gallery + lightbox JS
│   ├── scholars.html
│   ├── bibliography.html
│   ├── biography.html             # Maier biography (6 sections)
│   ├── timeline.html
│   ├── sources.html
│   ├── about.html
│   ├── emblems/                   # 51 emblem pages + index
│   ├── scholar/                   # 11 individual scholar pages
│   ├── dictionary/                # 38 term pages + index
│   ├── essays/                    # Essay index (5 planned)
│   └── images/emblems/            # 51 emblem plate images (Wikimedia Commons)
├── docs/reports/                   # 20 analysis/audit/lesson reports
└── atalanta fugiens/              # Source corpus (read-only)
    ├── *.pdf                      # Original PDFs
    └── *.md                       # OCR markdown conversions
```
