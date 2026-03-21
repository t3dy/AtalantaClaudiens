# Claude Code Instructions — AtalantaClaudiens

## Project Summary

Digital humanities website showcasing H.M.E. De Jong's scholarship on Michael Maier's *Atalanta Fugiens* (1618). Architecture replicates HPMarginalia: SQLite source of truth, Python static site generator, vanilla HTML/CSS/JS, GitHub Pages deployment at `t3dy/AtalantaClaudiens`.

## Quick Reference

| Document | Purpose |
|----------|---------|
| `docs/SYSTEM.md` | Architecture, data flow, provenance model |
| `docs/ONTOLOGY.md` | Database schema (18 tables), entity relationships |
| `docs/PIPELINE.md` | Script execution order, stage dependencies |
| `docs/INTERFACE.md` | Website sections, page templates, navigation |
| `docs/ROADMAP.md` | Phase status: BUILT / READY / BLOCKED / SPECULATIVE |
| `PHASESTATUS.md` | Session discipline log — update at end of every session |
| `SCHOLARSHIPREPORT.md` | Corpus analysis, ontology design recommendations |
| `atalanta_fugiens_seed.json` | Structured seed data for database ingestion |

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
├── PHASESTATUS.md                 # Session discipline log
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
│   ├── init_db.py                 # Stage 1: Schema creation
│   ├── seed_from_json.py          # Stage 1: Ingest seed data
│   ├── extract_dejong.py          # Stage 2: Parse De Jong markdown
│   ├── extract_secondary.py       # Stage 2: Parse other scholars
│   ├── seed_dictionary.py         # Stage 3: Populate dictionary
│   ├── seed_timeline.py           # Stage 3: Populate timeline
│   ├── build_site.py              # Stage 4: Generate static HTML
│   └── validate.py                # Stage 5: QA audit
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
│   └── sources/                   # Symlinks to source .md files
├── staging/                       # LLM outputs before promotion
├── site/
│   ├── index.html                 # Gallery home
│   ├── data.json                  # Gallery data (generated)
│   ├── style.css                  # Main styles
│   ├── components.css             # Component styles
│   ├── script.js                  # Gallery + lightbox JS
│   ├── scholars.html
│   ├── bibliography.html
│   ├── timeline.html
│   ├── sources.html
│   ├── about.html
│   ├── emblems/                   # 51 emblem pages
│   ├── scholar/                   # Individual scholar pages
│   ├── dictionary/                # Dictionary index + term pages
│   ├── essays/                    # Essay index + individual essays
│   └── images/emblems/            # Emblem plate images
└── atalanta fugiens/              # Source corpus (read-only)
    ├── *.pdf                      # Original PDFs
    └── *.md                       # OCR markdown conversions
```
