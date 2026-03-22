# DOCUMENTAIRTRAFFICCONTROL.md — Document Routing for LLM Agents

**Purpose**: This file tells you WHERE to look for WHAT. Read this before opening other files.

Every document in this project has a specific role. This routing guide prevents you from reading the wrong file, trusting stale data, or duplicating work already captured elsewhere. If you're unsure which file to consult, start here.

---

## Tier 1: Read FIRST (Orientation)

These files orient you to the project. Read them in this order at the start of any session.

| File | What It Tells You | When to Read |
|------|-------------------|-------------|
| `CLAUDE.md` | Project architecture, constraints, operating rules, design decisions | Always. This is the entry point. |
| `PHASESTATUS.md` | What happened in prior sessions, current phase, blockers, next steps | Always. Check before starting any work. |
| `DOCUMENTAIRTRAFFICCONTROL.md` | Where to find everything else (this file) | When you're unsure which doc to consult. |

## Tier 2: Read BEFORE Specific Work

These files are authoritative for their domain. Consult the relevant one before touching that area.

| File | Domain | Authoritative For |
|------|--------|------------------|
| `docs/ONTOLOGY.md` | Database | Table schemas, column types, relationships. **Warning**: documents some tables that don't exist yet — look for `[PLANNED]` tags. |
| `docs/PIPELINE.md` | Build system | Script execution order, stage dependencies, full rebuild command. |
| `docs/INTERFACE.md` | Website UI | Page templates, navigation, CSS components, badge colors. |
| `docs/ROADMAP.md` | Project status | What's BUILT vs READY vs BLOCKED vs PLANNED per phase/slice. |
| `EMBLEMGUIDE.md` | Emblem data | All 51 emblems: numbers, mottos, images, stages, sources, refs. **Read this before any emblem work.** |
| `data/emblem_manifest.json` | Emblem identity | Canonical machine-readable index. Single source of truth for image filenames, confirmation status, sources. |
| `docs/WRITING_TEMPLATES.md` | **Content voice + emblem template** | **CANONICAL**: 4-section emblem analysis template (The Plate, Maier's Discourse, De Jong's Sources, Scholarly Perspectives). Museum-level curation standards. Anti-patterns. DB field contracts. **Read this before writing ANY emblem content.** |

## Tier 3: Read FOR Context (Reference)

These files provide background knowledge. Read them when you need deeper understanding, not every session.

| File | What It Contains |
|------|-----------------|
| `SCHOLARSHIPREPORT.md` | Corpus analysis: what's in the 12 source PDFs, ontology design rationale |
| `atalanta_fugiens_seed.json` | Structured seed data for DB ingestion (emblems, authorities, scholars, dictionary, timeline) |
| `docs/SYSTEM.md` | Architecture overview, data flow, provenance model |
| `docs/SCHOLAR_SPEC.md` | Scholar page design specification |
| `docs/TIMELINE_SPEC.md` | Timeline event model |

## Tier 4: Read FOR Lessons Learned

Reports from prior sessions. Read when you're about to repeat work in the same area, or when debugging.

| File | Lesson |
|------|--------|
| `docs/reports/TRIALANDERROR.md` | OCR extraction debugging: dedup bugs, boundary calculations, physical vs logical order |
| `docs/reports/IMAGEFOLLIES.md` | Image sourcing: check Wikimedia first, 8s delays, never deploy unverified data |
| `docs/reports/321BUCKMANCRITIQUE.md` | Why image search failed: no manifest, no single source of truth. Led to emblem_manifest.json |
| `docs/reports/HARDOCRCASES.md` | OCR garbling tiers and recovery strategies |
| `docs/reports/HIRO321TUNEUP.md` | Infrastructure audit: what's built, what's planned, what's drifted |
| `docs/reports/HIROREBUILD.md` | Master rebuild plan: 43 intent atoms across 7 layers |
| `docs/reports/DESIREDIMPROVEMENTS.md` | 20-priority improvement list by website section |
| `docs/reports/PRISPEDAGOGYREPORT.md` | Pedagogical audit of every website section |
| `docs/reports/DOWEREALLYNEEDARAG.md` | Verdict: no RAG needed, corpus fits in 1M context |
| `docs/reports/SWARMWRITING.md` | How to run parallel agent swarms |
| `docs/reports/SwarmContentAudit.md` | Content completeness audit |
| `docs/reports/SwarmSchemaAudit.md` | Schema vs reality audit |
| `docs/reports/SwarmPipelineAudit.md` | Pipeline script audit |
| `docs/reports/SwarmProvenanceAudit.md` | Provenance and data integrity audit |
| `docs/reports/MISSINGEMBLEMS.md` | **OBSOLETE** — all missing emblems were fixed. Historical only. |
| `docs/reports/MOTTO_DISCREPANCY.md` | Motto text discrepancies between sources |
| `docs/reports/HANDOVER.md` | Session handover: orientation, rebuild command, gotchas |
| `docs/reports/DECKARDTILT.md` | Tilton ingestion boundary plan |
| `docs/reports/DECKARDAF1.md` | AI/human boundary decisions for Phase 1 |
| `docs/reports/REFLAYERAF1.md` | Reference layer design |

---

## Routing Rules

### "I need to understand the database schema"
→ Read `docs/ONTOLOGY.md`. Note: tables tagged `[PLANNED]` do not exist in the DB yet. Only tables tagged `[BUILT]` are real.

### "I need to add or modify a pipeline script"
→ Read `docs/PIPELINE.md` for execution order and stage dependencies. Then check `PHASESTATUS.md` for current state.

### "I need to work with emblems (data, images, pages)"
→ Read `EMBLEMGUIDE.md` first, then `data/emblem_manifest.json`. The manifest is the canonical index. Trust `image_confirmed: true` entries. Do not re-source confirmed images.

### "I need to write emblem content (image descriptions, discourse summaries, analysis blocks)"
→ Read `docs/WRITING_TEMPLATES.md` FIRST — it defines the mandatory 4-section template, voice rules, anti-patterns, and DB field contracts. Every emblem analysis must have: (1) The Plate (3-5 sentences visual), (2) Maier's Discourse (3-5 sentences academic summary), (3) De Jong's Source Analysis (3-5 sentences on sources + hidden chemistry), (4) Scholarly Perspectives (1-3 sentences, optional). **Do not write emblem content without reading the template.**

### "I need to write other content (dictionary, essays, scholar profiles)"
→ Read `docs/WRITING_TEMPLATES.md` for voice and structure. Check `docs/reports/DESIREDIMPROVEMENTS.md` for what's needed.

### "I need to extract from the source corpus"
→ Read `docs/reports/TRIALANDERROR.md` for OCR extraction lessons. Read `docs/reports/HARDOCRCASES.md` for garbling patterns. Source files are in `atalanta fugiens/` (read-only).

### "I need to source emblem images"
→ Read `docs/reports/IMAGEFOLLIES.md` FIRST. Then check `data/emblem_manifest.json` for what's confirmed. Wikimedia Commons is the primary source. Use 8-second delays.

### "I need to understand the project architecture"
→ Read `docs/SYSTEM.md` for the full architecture. Short version: `data/emblem_manifest.json` → `seed_identity.py` → SQLite → `build_site.py` → static HTML → GitHub Pages.

### "I need to plan new work"
→ Read `docs/ROADMAP.md` for phase status. Read `docs/reports/HIROREBUILD.md` for the master rebuild plan (43 atoms). Use the PKD Planning Protocol from `C:\Dev\CLAUDE.md`.

### "Something failed and I need to debug"
→ Read `docs/reports/TRIALANDERROR.md` for extraction bugs. Read `docs/reports/IMAGEFOLLIES.md` for image sourcing failures. Check `PHASESTATUS.md` for known blockers.

---

## Data Flow (One Direction)

```
data/emblem_manifest.json    ← CANONICAL SOURCE (agents edit here)
        ↓
seed_identity.py             → emblem_identity table (SQLite)
        ↓
atalanta_fugiens_seed.json   → seed_from_json.py + seed_phase2.py → all other tables
        ↓
extract_dejong.py            → mottos, discourses, scholarly_refs (from OCR)
        ↓
seed_emblem_analyses.py      → analysis_html (assembled from DB fields)
        ↓
build_site.py                → site/*.html (static pages)
        ↓
GitHub Pages                 → https://t3dy.github.io/AtalantaClaudiens/
```

Changes flow ONE direction: manifest/seed → DB → HTML → deploy.
Never edit generated HTML. Never edit the DB directly. Edit the source data, rebuild.

---

## What NOT to Trust

| Source | Problem |
|--------|---------|
| CLAUDE.md file tree | May list scripts that don't exist. Cross-check with `ls scripts/`. |
| ONTOLOGY.md `[PLANNED]` tables | Documented but never created. Don't write scripts that depend on them without migrating first. |
| ONTOLOGY.md `[PLANNED]` columns on `emblems` | ~~`visual_elements`, `fugue_mode`, `fugue_interval`, `epigram_german`~~ **FIXED** — created by `migrate_v4_enrichment.py` (schema v5). |
| ONTOLOGY.md `registers` on `dictionary_terms` | ~~Documented but column never created.~~ **FIXED** — created by `migrate_v4_enrichment.py` (schema v5). |
| PHASESTATUS.md counts | May be from an earlier session. Rebuild and count from DB for ground truth. |
| EMBLEMGUIDE.md image column | May lag behind `data/emblem_manifest.json`. Trust the manifest. |
| MISSINGEMBLEMS.md | Obsolete. All missing emblems were fixed. |
| ROADMAP.md image counts | May not reflect latest Wikimedia downloads. Check `site/images/emblems/` for truth. |

---

## Quick Counts (as of 2026-03-21)

Verify these by rebuilding if they seem wrong.

| Entity | Count | Source of Truth |
|--------|-------|----------------|
| Emblems | 51 (0-50) | `emblems` table |
| Emblem images on disk | 51 | `site/images/emblems/` |
| Images confirmed HIGH | ~24 | `data/emblem_manifest.json` |
| Mottos (English) | 50/50 | `emblems.motto_english` |
| Mottos (Latin) | 50/50 | `emblems.motto_latin` |
| Discourses | 47/50 | `emblems.discourse_summary` |
| Analyses | 50/51 | `emblems.analysis_html` |
| Alchemical stages | 50/50 | `emblems.alchemical_stage` |
| Image descriptions | 23/51 | `emblems.image_description` |
| Scholarly refs | 64 | `scholarly_refs` table |
| Source authorities | 15 | `source_authorities` table |
| Emblem-source links | 134 | `emblem_sources` table |
| Dictionary terms | 73 | `dictionary_terms` table |
| Dictionary definition_long | 73/73 | `dictionary_terms.definition_long` |
| Term-emblem links | 112 | `term_emblem_refs` table |
| Timeline events | 29 | `timeline_events` table |
| Scholars | 11 | `scholars` table |
| Bibliography | 10 | `bibliography` table |
| DB tables (built) | 14 | `sqlite_master` |
| DB tables (documented, unbuilt) | 7 | ONTOLOGY.md `[PLANNED]` |
| Schema version | 5 | `schema_version` table |
| Pipeline scripts | 20 | `scripts/` directory |
| Site pages generated | 129+ | `site/` directory |
