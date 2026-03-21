# HIROREBUILD.md — HiroPlantagenet Decomposition: AtalantaClaudiens Rebuild

**Date**: 2026-03-21
**Scope**: Full architectural rebuild plan covering documentation, schema, data, extraction, interface, and pedagogy.
**Method**: HiroPlantagenet analysis — intent atoms, conflict detection, layered execution, standalone prompts.

---

## 1. Intent Atoms

Every discrete change needed, tagged by type. These are the atomic units of work.

| ID | Atom | Type | Current State | Target State |
|----|------|------|---------------|--------------|
| A01 | Fix CLAUDE.md file tree to match actual 13 scripts | META-CONTROL | Lists 4 phantom scripts, omits 5 real ones | Exact match with `scripts/` directory |
| A02 | Rewrite ROADMAP.md to reflect Phases 1-3 complete | META-CONTROL | Shows Phase 1 "IN PROGRESS", rest "DEFERRED" | Accurate phase status for all 7 phases |
| A03 | Update PHASESTATUS.md with all unlogged sessions | META-CONTROL | Missing v3, identity, enrichment, and audit sessions | Complete session log through 2026-03-21 |
| A04 | Document `emblem_identity` table in ONTOLOGY.md | ONTOLOGY | Table exists in DB but absent from docs | Full column spec documented |
| A05 | Document `schema_version` table in ONTOLOGY.md | ONTOLOGY | Table exists in DB but absent from docs | Full column spec documented |
| A06 | Document `bibliography.annotation` column in ONTOLOGY.md | ONTOLOGY | Column exists but not in docs | Documented |
| A07 | Add `registers` JSON column to `dictionary_terms` table | ONTOLOGY | Documented in ONTOLOGY.md but never created in DB | Column exists and migration script written |
| A08 | Populate `definition_long` for all 38 dictionary terms | EXTRACTION | 0/38 filled | 38/38 filled |
| A09 | Populate `registers` JSON for all 38 dictionary terms | EXTRACTION | Column does not exist | 38/38 filled with 4-register model |
| A10 | Add Latin mottos (`motto_latin`) for 49 missing emblems | EXTRACTION | 1/50 populated | 50/50 populated |
| A11 | Classify all 50 emblems by `alchemical_stage` | EXTRACTION | 0/50 populated | 50/50 classified as NIGREDO/ALBEDO/CITRINITAS/RUBEDO |
| A12 | Extract 3 remaining discourse summaries (XI, XXXVIII, XLVIII) | EXTRACTION | 47/50 | 50/50 via LLM-assisted pass |
| A13 | Clean OCR artifacts in discourse text (run-together words) | EXTRACTION | Raw OCR with "thephilosophers" etc. | Cleaned readable text |
| A14 | Enrich frontispiece (Emblem 0) with analysis content | EXTRACTION | No motto, discourse, or analysis | Gateway emblem fully populated |
| A15 | Split `atalanta_fugiens_seed.json` into domain files | PIPELINE | Single 3000+ line monolith | Separate: `emblems.json`, `scholars.json`, `dictionary.json`, `timeline.json`, `bibliography.json`, `sources.json` |
| A16 | Update seed scripts to read split JSON files | PIPELINE | `seed_from_json.py` and `seed_phase2.py` read one file | Read from `data/seed/` directory |
| A17 | Write `extract_tilton.py` | EXTRACTION | Does not exist | LLM-assisted extraction: 20-40 scholarly_refs, 5-15 terms, 10-20 events |
| A18 | Write `extract_secondary.py` | EXTRACTION | Does not exist | Parse Craven, Wescott, Pagel, Miner |
| A19 | Write `extract_dejong_llm.py` for 3 hard OCR cases | EXTRACTION | Does not exist | LLM pass on known page ranges for XI, XXXVIII, XLVIII |
| A20 | Source remaining 41 emblem images (X-L) | EXTRACTION | 10/51 images | 51/51 from Wikimedia/public domain |
| A21 | Write `analyze_emblem_images.py` (vision pipeline) | EXTRACTION | Does not exist | Batch Claude Vision populating `visual_elements` |
| A22 | Add home page intro text + "Start Here" button | UI-SURFACING | Stats dashboard only, no orientation | Hero section with 2-3 sentences + CTA |
| A23 | Add source x emblem matrix visualization | UI-SURFACING | Sources page has cards only | 50x15 interactive grid |
| A24 | Add client-side search | UI-SURFACING | No search | JavaScript search over data.json + terms |
| A25 | Add Biography tab for Maier to nav bar | UI-SURFACING | Not in nav, biography page exists | Nav link added, page enriched |
| A26 | Show Latin motto alongside English on emblem pages | UI-SURFACING | English only (for 49/50 emblems) | Bilingual motto block |
| A27 | Show epigram by default (remove `<details>` collapse) | UI-SURFACING | Hidden behind collapsible | Visible by default |
| A28 | Add "What You See" visual description section to emblem pages | UI-SURFACING | No visual element descriptions | Description before analysis block |
| A29 | Add thematic connections ("See also") between emblems | UI-SURFACING | No cross-emblem links | Related emblems sidebar |
| A30 | Distinguish MOTTO_SOURCE vs DISCOURSE_CITATION on Sources page | UI-SURFACING | All relationship types displayed identically | Color-coded or sectioned by type |
| A31 | Add era groupings to Timeline | UI-SURFACING | Flat chronological list | Period headers with narrative text |
| A32 | Write 5 thematic essays | UI-SURFACING | Placeholder index, 0/5 written | 5 essays, 1500-3000 words each, AI-drafted |
| A33 | Add "How to Read an Alchemical Emblem" guided pathway | UI-SURFACING | No newcomer orientation | 3-step tutorial: Frontispiece -> Emblem I -> Method |
| A34 | Expand dictionary to 60+ terms | EXTRACTION | 38 terms | 60+ terms from corpus mining |
| A35 | Expand term-emblem links (28 emblems have 0 links) | EXTRACTION | 22/50 have links | 45+/50 have links |
| A36 | Add Rosicrucian manifesto events to Timeline | EXTRACTION | Missing Fama (1614), Confessio (1615), Chemical Wedding (1616) | Key context events added |
| A37 | Document dev pipeline vs deploy pipeline distinction | META-CONTROL | CI only deploys static files, undocumented | PIPELINE.md has clear section |
| A38 | Add `migrate_v3_identity.py` and `seed_identity.py` subsections to PIPELINE.md | META-CONTROL | Listed in overview but no detailed blocks | Full documentation blocks |
| A39 | Update INTERFACE.md with dictionary rename, sources overhaul, timeline improvements | META-CONTROL | Stale | Current |
| A40 | Automate or retire PHASESTATUS.md | META-CONTROL | Manual, always stale | Either script-generated or replaced with ROADMAP.md |
| A41 | Expand bibliography from 10 to 13+ entries | EXTRACTION | 10 entries | All corpus sources represented |
| A42 | Write individual source authority pages | UI-SURFACING | All 15 on single page | Each gets `/sources/{authority_id}.html` |
| A43 | Add scholar emblem coverage map | UI-SURFACING | No per-scholar coverage data | Visual showing which emblems each scholar discusses |

---

## 2. Conflicts & Gaps

### 2a. Conflicts Between Docs and Reality

| Document | Claim | Reality | Resolution |
|----------|-------|---------|------------|
| CLAUDE.md file tree | Lists `scripts/extract_secondary.py` | Does not exist | Remove from tree or mark as PLANNED |
| CLAUDE.md file tree | Lists `scripts/seed_dictionary.py` | Absorbed into `seed_phase2.py` | Remove |
| CLAUDE.md file tree | Lists `scripts/seed_timeline.py` | Absorbed into `seed_phase2.py` | Remove |
| CLAUDE.md file tree | Lists `scripts/validate.py` | Replaced by `validate_identity.py` | Correct |
| CLAUDE.md file tree | Lists 8 scripts | Actual count is 13 | Regenerate from directory listing |
| ROADMAP.md | Phase 1 "IN PROGRESS" | Phase 1 complete | Rewrite entirely |
| ROADMAP.md | Phases 2-4 "DEFERRED" | Phases 2-3 substantially complete | Rewrite entirely |
| ONTOLOGY.md | Documents 18 tables | DB has 13 tables; 5 documented tables never created | Distinguish BUILT vs PLANNED tables |
| ONTOLOGY.md | Documents `registers` column on `dictionary_terms` | Column never created via migration | Write migration, then document |
| ONTOLOGY.md | Does not document `emblem_identity` | Table exists with 51 rows | Add documentation |
| ONTOLOGY.md | Does not document `schema_version` | Table exists with 4 rows | Add documentation |
| PHASESTATUS.md | Pipeline command missing 5 scripts | PIPELINE.md has correct full command | Update PHASESTATUS.md |
| PHASESTATUS.md | Schema Version 2 | Actually v4 (identity layer) | Update |
| PIPELINE.md `seed_emblem_analyses.py` | `source_method='LLM_ASSISTED'` | Uses template assembly, no LLM call | Change to `TEMPLATE_ASSEMBLY` or clarify |

### 2b. Missing Decisions

| Decision | Impact | Suggested Resolution |
|----------|--------|---------------------|
| How to handle 5 ONTOLOGY.md tables that don't exist in DB | Confuses anyone reading schema docs | Mark as PLANNED with a `[NOT YET CREATED]` tag, or remove until needed |
| Whether to keep PHASESTATUS.md at all | Always stale, duplicates ROADMAP.md | Replace with a `## Session Log` section in ROADMAP.md |
| Where biography content lives (About page section vs standalone page) | Nav structure, build_site.py templates | Standalone page at `/biography.html`, linked from nav |
| Whether `staging/` directory has a role in the current pipeline | CLAUDE.md describes it; no scripts use it | Either implement staging workflow or remove from docs |
| How split seed files interact with existing seed scripts | Two scripts read one JSON file | Refactor both scripts or write a new unified seed script |
| Image sourcing strategy after SHI viewer failure | 41 images missing, SHI scan unmappable | Use labeled Wikimedia Commons images with known emblem numbers |
| Whether essays table should store markdown or HTML | Current schema says `body_html` | Keep HTML; generate from markdown in essay writing script |

### 2c. Implicit Assumptions

| Assumption | Risk |
|------------|------|
| De Jong markdown OCR quality is uniform | It degrades significantly after page 200 (Emblem XXXV+) |
| All 50 emblems deserve equal depth on the site | Frontispiece (Emblem 0) is the interpretive key and gets minimal content |
| One `build_site.py` handles all page generation | Script is growing; may need modularization if source pages and biography are added |
| `analysis_html` is regenerated on every rebuild | Means LLM-enriched analysis blocks must be stored elsewhere or the template must incorporate them |
| The 13-script sequential pipeline can be run manually | No orchestration script; easy to skip a step or run in wrong order |
| Background agents have Bash permission | They do NOT in Claude Code sandbox; DB-querying audits fail silently |

---

## 3. Layer Architecture

### Layer 0: DOCUMENTATION RESET
**Purpose**: Eliminate all doc-reality conflicts so subsequent layers start from accurate ground truth.
**Dependencies**: None.
**Atoms**: A01, A02, A03, A04, A05, A06, A37, A38, A39, A40

| Task | Description | Effort |
|------|-------------|--------|
| A01 | Regenerate CLAUDE.md file tree from actual directory listing | 15 min |
| A02 | Rewrite ROADMAP.md: Phases 1-3 BUILT, Phase 4 PARTIAL, Phase 5-7 PLANNED | 30 min |
| A03 | Add missing session entries to PHASESTATUS.md (or merge into ROADMAP.md) | 20 min |
| A04 | Add `emblem_identity` table spec to ONTOLOGY.md | 10 min |
| A05 | Add `schema_version` table spec to ONTOLOGY.md | 5 min |
| A06 | Add `bibliography.annotation` column to ONTOLOGY.md | 5 min |
| A37 | Add "Dev Pipeline vs Deploy Pipeline" section to PIPELINE.md | 10 min |
| A38 | Add detailed blocks for `migrate_v3_identity.py` and `seed_identity.py` in PIPELINE.md | 15 min |
| A39 | Update INTERFACE.md with current page states | 20 min |
| A40 | Decide: merge PHASESTATUS.md into ROADMAP.md or automate | 10 min |

**Total**: ~2.5 hours. Fully deterministic. No LLM needed.

---

### Layer 1: SCHEMA ALIGNMENT
**Purpose**: Make the DB match the documented schema, and the docs match the DB.
**Dependencies**: Layer 0 (docs must be accurate before changing schema).
**Atoms**: A07

| Task | Description | Effort |
|------|-------------|--------|
| A07 | Write `migrate_v4_registers.py`: adds `registers` TEXT column to `dictionary_terms` | 15 min |
| Mark 5 unbuilt ONTOLOGY tables as PLANNED | `alchemical_processes`, `emblem_processes`, `visual_elements`, `mythological_figures`, `emblem_figures`, `editions` | 10 min |

**Total**: ~30 minutes. Deterministic.

**Schema note**: The 5 unbuilt tables (`alchemical_processes`, `emblem_processes`, `visual_elements` [the table, not the column], `mythological_figures`, `emblem_figures`, `editions`) should remain documented but tagged `[PLANNED - NOT YET CREATED]`. They represent a richer data model that becomes relevant when the vision pipeline and process classification are implemented.

---

### Layer 2: SEED DATA REFACTOR
**Purpose**: Break the monolithic `atalanta_fugiens_seed.json` into domain-specific files so agents can work in parallel without merge conflicts.
**Dependencies**: Layer 1 (schema must be stable before restructuring seed data).
**Atoms**: A15, A16

| Task | Description | Effort |
|------|-------------|--------|
| A15 | Split `atalanta_fugiens_seed.json` into `data/seed/` directory: `emblems.json`, `scholars.json`, `dictionary.json`, `timeline.json`, `bibliography.json`, `sources.json`, `emblem_sources.json`, `scholarly_refs.json` | 1 hour |
| A16 | Refactor `seed_from_json.py` and `seed_phase2.py` to read from `data/seed/` | 1 hour |
| Write `scripts/rebuild.sh` orchestration script | Single command runs full pipeline in correct order | 30 min |

**Total**: ~2.5 hours. Deterministic.

**Split strategy**:
```
data/seed/
  emblems.json          ← 51 emblems with mottos, labels, image_descriptions
  bibliography.json     ← 10+ bibliography entries with annotations
  sources.json          ← 15 source_authorities with description_long
  scholarly_refs.json   ← 29+ scholarly references
  emblem_sources.json   ← 16+ emblem-source links
  scholars.json         ← 11 scholar profiles
  dictionary.json       ← 38+ dictionary terms with Latin, significance
  timeline.json         ← 29+ timeline events with description_long
  identity.json         ← 51 emblem identity records (replaces data/emblem_identity_seed.json)
```

Each file is self-contained. Agents writing new dictionary terms edit only `dictionary.json`. Agents adding timeline events edit only `timeline.json`. No merge conflicts.

---

### Layer 3: CONTENT ENRICHMENT (Deterministic)
**Purpose**: Fill data gaps that can be resolved without LLM.
**Dependencies**: Layer 2 (seed files must be split so edits are targeted).
**Atoms**: A36, A41

| Task | Description | Effort |
|------|-------------|--------|
| A36 | Add Rosicrucian manifesto events + Maier publication history to `timeline.json` | 30 min |
| A41 | Add 3+ missing bibliography entries (Kuntz, Basilius Valentinus, De Jong 1965) | 20 min |

**Total**: ~1 hour. Deterministic (known facts, hardcoded data).

---

### Layer 4: CONTENT ENRICHMENT (LLM-Assisted)
**Purpose**: Fill data gaps requiring semantic comprehension.
**Dependencies**: Layer 2 (seed files split), Layer 1 (registers column exists).
**Atoms**: A08, A09, A10, A11, A12, A13, A14, A17, A18, A19, A34, A35

These atoms divide into parallel workstreams:

#### Workstream 4A: De Jong Gap-Fill
| Task | Description | Method | Effort |
|------|-------------|--------|--------|
| A10 | Extract 49 Latin mottos from OCR or reference tables | Regex + LLM cleanup | 2 hours |
| A12 | Extract 3 remaining discourses via `extract_dejong_llm.py` (A19) | LLM on known page ranges | 1 hour |
| A13 | Clean OCR artifacts in all 47 existing discourse summaries | Batch text-cleaning script | 1 hour |
| A14 | Write frontispiece analysis from De Jong's introduction | LLM synthesis | 1 hour |

#### Workstream 4B: Dictionary Enrichment
| Task | Description | Method | Effort |
|------|-------------|--------|--------|
| A08 | Write `definition_long` for 38 terms | LLM swarm (5 agents x 8 terms) | 2 hours |
| A09 | Populate `registers` JSON for 38 terms | LLM swarm (same agents) | Included in A08 |
| A34 | Add 22+ new dictionary terms | LLM mining of De Jong discourses | 2 hours |
| A35 | Expand term-emblem links for 28 unlinked emblems | LLM + regex cross-referencing | 1 hour |

#### Workstream 4C: Secondary Source Extraction
| Task | Description | Method | Effort |
|------|-------------|--------|--------|
| A17 | Write and run `extract_tilton.py` | Deterministic pre-pass + LLM extraction | 3 hours |
| A18 | Write and run `extract_secondary.py` | LLM extraction per source file | 3 hours |

#### Workstream 4D: Alchemical Classification
| Task | Description | Method | Effort |
|------|-------------|--------|--------|
| A11 | Classify 50 emblems by alchemical stage | LLM with De Jong's process analysis as input | 1 hour |

**Total**: ~12-16 hours across workstreams. Workstreams 4A-4D can run in parallel.

---

### Layer 5: INTERFACE IMPROVEMENTS
**Purpose**: Transform the site from reference tool to teaching tool.
**Dependencies**: Layer 4 (richer data enables richer display).
**Atoms**: A22, A25, A26, A27, A28, A29, A30, A31, A42, A43

#### Phase 5A: Quick Wins (modify `build_site.py` only)
| Task | Description | Effort |
|------|-------------|--------|
| A22 | Home page intro text + "Start Here" button | 30 min |
| A25 | Add Biography link to nav bar | 15 min |
| A26 | Show Latin motto alongside English in emblem template | 30 min |
| A27 | Show epigram by default (remove `<details>` collapse) | 15 min |
| A31 | Add era groupings to Timeline with header text | 1 hour |
| A30 | Distinguish MOTTO_SOURCE vs DISCOURSE_CITATION on Sources page | 30 min |

#### Phase 5B: New Features (new templates + JavaScript)
| Task | Description | Effort |
|------|-------------|--------|
| A23 | Source x Emblem matrix visualization (JavaScript + CSS grid) | 3 hours |
| A24 | Client-side search over data.json + term names | 2 hours |
| A28 | "What You See" visual description section on emblem pages | 1 hour (template) |
| A29 | Thematic connections / "See also" links between emblems | 2 hours |
| A42 | Individual source authority pages (`/sources/{id}.html`) | 2 hours |
| A43 | Scholar emblem coverage map | 1 hour |

**Total**: ~14 hours across phases.

---

### Layer 6: PEDAGOGICAL SCAFFOLDING
**Purpose**: Build the teaching layer that transforms browsing into learning.
**Dependencies**: Layers 4-5 (content and interface must be rich enough to support guided pathways).
**Atoms**: A32, A33

| Task | Description | Method | Effort |
|------|-------------|--------|--------|
| A32 | Write 5 thematic essays | LLM swarm (1 agent per essay) | 5 hours |
| A33 | Build "How to Read" guided pathway (Frontispiece -> I -> Method) | Template + content | 2 hours |

**Total**: ~7 hours.

---

### Layer 7: IMAGE PIPELINE
**Purpose**: Complete visual layer.
**Dependencies**: A20 (image sourcing) is external and blocks A21.
**Atoms**: A20, A21

| Task | Description | Method | Effort |
|------|-------------|--------|--------|
| A20 | Source 41 emblem images from Wikimedia Commons / public domain | Manual identification + scripted download | 3-5 hours |
| A21 | Write and run `analyze_emblem_images.py` | Claude Vision batch | 2 hours |

**Total**: ~5-7 hours. Blocked on manual image sourcing.

---

## 4. Rewritten Prompts

### PROMPT L0: Documentation Reset

```
OBJECTIVE: Bring all project documentation into alignment with the actual state
of the AtalantaClaudiens codebase as of 2026-03-21.

SCOPE:
- CLAUDE.md file tree section
- docs/ROADMAP.md (full rewrite)
- PHASESTATUS.md (add missing sessions OR merge into ROADMAP.md)
- docs/ONTOLOGY.md (add emblem_identity, schema_version, bibliography.annotation;
  tag 5 unbuilt tables as [PLANNED])
- docs/PIPELINE.md (add dev-vs-deploy section, add missing script detail blocks)
- docs/INTERFACE.md (update to reflect current page states)

INPUTS:
- Actual directory listing of scripts/ (13 files)
- SwarmSchemaAudit.md (DB tables vs docs)
- SwarmPipelineAudit.md (script inventory)
- HIRO321TUNEUP.md (infrastructure audit)
- Current CLAUDE.md, ROADMAP.md, PHASESTATUS.md, ONTOLOGY.md, PIPELINE.md, INTERFACE.md

OUTPUT CONTRACT:
1. CLAUDE.md file tree matches `ls scripts/` exactly. No phantom scripts.
2. ROADMAP.md has accurate status for every phase/slice. Uses: BUILT / PARTIAL / PLANNED / BLOCKED.
3. ONTOLOGY.md documents all 13 tables that exist in the DB. 5 planned-but-unbuilt
   tables are tagged [PLANNED - NOT YET CREATED].
4. PIPELINE.md has a "Dev Pipeline vs Deploy Pipeline" section explaining that
   CI deploys pre-built static files; the full 13-script pipeline runs locally.
5. Every documentation file updated in this layer has a "Last updated: 2026-03-21"
   line at the top.

DECISION RULES:
- When docs and DB conflict, DB is the source of truth.
- When docs and scripts/ conflict, scripts/ is the source of truth.
- PHASESTATUS.md: if merging into ROADMAP.md, add a ## Session Log section with
  dated entries. If keeping separate, add entries for all sessions since last update.
- Do NOT change any Python code or database state. This layer is docs-only.
```

---

### PROMPT L1: Schema Alignment

```
OBJECTIVE: Align the SQLite database schema with documented ONTOLOGY.md,
adding the one missing column that should exist.

SCOPE:
- Write scripts/migrate_v4_registers.py
- Update docs/ONTOLOGY.md to mark the column as BUILT
- Update docs/PIPELINE.md full rebuild command to include migrate_v4

INPUTS:
- docs/ONTOLOGY.md (documents `registers` TEXT column on dictionary_terms)
- SwarmSchemaAudit.md (confirms column does not exist in DB)
- Existing migration scripts (migrate_v2.py, migrate_v3.py, migrate_v3_identity.py)
  as templates for idempotent migration pattern

OUTPUT CONTRACT:
1. migrate_v4_registers.py:
   - Checks PRAGMA table_info(dictionary_terms) before ALTER TABLE
   - Adds `registers TEXT` column if not present
   - Inserts schema_version row (version=5, description="Add registers column")
   - Uses try/except for idempotency
2. Full rebuild command in PIPELINE.md includes migrate_v4_registers.py
   after migrate_v3_identity.py
3. ONTOLOGY.md dictionary_terms table shows registers column without
   any [PLANNED] tag

DECISION RULES:
- Follow exact pattern of migrate_v3.py for idempotent column addition.
- Do NOT create the 5 planned tables (alchemical_processes, etc.) yet.
  Those are Layer 7+ work.
- The registers column type is TEXT (stores JSON string).
```

---

### PROMPT L2: Seed Data Refactor

```
OBJECTIVE: Split the monolithic atalanta_fugiens_seed.json into domain-specific
seed files and update the ingestion scripts to read from them.

SCOPE:
- Create data/seed/ directory
- Split atalanta_fugiens_seed.json into 8 domain files
- Refactor seed_from_json.py to read from data/seed/
- Refactor seed_phase2.py to read from data/seed/
- Move data/emblem_identity_seed.json into data/seed/identity.json
- Update seed_identity.py to read from new location
- Write scripts/rebuild.sh orchestration script
- Update PIPELINE.md with new file paths

INPUTS:
- atalanta_fugiens_seed.json (current monolith)
- data/emblem_identity_seed.json
- scripts/seed_from_json.py (reads: emblems, bibliography, source_authorities,
  scholarly_refs, emblem_sources from seed JSON)
- scripts/seed_phase2.py (reads: scholars, dictionary_terms, timeline_events,
  scholar_works, term_emblem_refs from seed JSON)
- scripts/seed_identity.py (reads from data/emblem_identity_seed.json)

OUTPUT CONTRACT:
1. data/seed/ contains 9 JSON files, each valid JSON, each self-contained:
   - emblems.json (51 entries)
   - bibliography.json (10+ entries)
   - sources.json (15 entries — source_authorities)
   - scholarly_refs.json (29+ entries)
   - emblem_sources.json (16+ entries)
   - scholars.json (11 entries)
   - dictionary.json (38+ entries with label_latin, significance_to_af)
   - timeline.json (29+ entries with description_long)
   - identity.json (51 entries)
2. seed_from_json.py reads from data/seed/{emblems,bibliography,sources,
   scholarly_refs,emblem_sources}.json
3. seed_phase2.py reads from data/seed/{scholars,dictionary,timeline}.json
4. seed_identity.py reads from data/seed/identity.json
5. scripts/rebuild.sh runs the full 13-script pipeline in correct order
6. Full pipeline rebuild produces identical database to current pipeline
   (regression test: row counts match)

DECISION RULES:
- Each JSON file is an array of objects, not nested under a key.
  Example: dictionary.json is [...] not {"dictionary_terms": [...]}.
- Preserve ALL data from the monolith. No data loss.
- The monolith file (atalanta_fugiens_seed.json) is NOT deleted — it is
  retained as an archive. Add a comment or rename to
  atalanta_fugiens_seed.ARCHIVE.json.
- rebuild.sh should use set -e (exit on first error) and print each
  script name before execution for debugging.
- scholar_works join data goes into scholars.json as a nested array
  on each scholar object, since it's small and tightly coupled.
- term_emblem_refs goes into dictionary.json as a nested array on each term.
```

---

### PROMPT L3: Deterministic Content Enrichment

```
OBJECTIVE: Add known-fact content to seed files that requires no LLM
interpretation — historical dates, publication records, bibliography entries.

SCOPE:
- Add Rosicrucian manifesto events to data/seed/timeline.json
- Add Maier publication history events to data/seed/timeline.json
- Add 3+ missing bibliography entries to data/seed/bibliography.json
- Add missing scholar_works links

INPUTS:
- data/seed/timeline.json (current 29 events)
- data/seed/bibliography.json (current 10 entries)
- DESIREDIMPROVEMENTS.md section 6 (timeline gaps)
- DECKARDTILT.md (Tilton publication details)
- Known historical facts:
  - Fama Fraternitatis (1614, Kassel)
  - Confessio Fraternitatis (1615, Kassel)
  - Chymische Hochzeit (1616, Strasbourg)
  - Atalanta Fugiens (1617/1618, Oppenheim)
  - Maier at Rudolf II's court (~1608-1612)
  - Maier's English sojourn (~1611-1616)
  - Maier's death (1622, Magdeburg)

OUTPUT CONTRACT:
1. timeline.json gains 10-15 new events, all with confidence=HIGH,
   event_type correctly classified
2. bibliography.json gains 3+ new entries with complete metadata
3. All new entries follow existing JSON structure exactly
4. No existing entries modified (additive only)
5. Full pipeline rebuild succeeds with new data

DECISION RULES:
- Only add events with known dates and verifiable facts.
- Timeline events about publications use event_type=PUBLICATION.
- Events about Maier's life use event_type=BIOGRAPHY.
- Events about Rosicrucian context use event_type=PUBLICATION
  (they are publication events of the manifestos).
- New bibliography entries: source_id follows pattern author_year
  (e.g., kuntz_1987, valentinus_golden_tripod).
- Do NOT add events that require interpretation of sources (that's Layer 4).
```

---

### PROMPT L4A: De Jong Gap-Fill

```
OBJECTIVE: Close the remaining data gaps in De Jong extraction: Latin mottos,
3 missing discourses, OCR cleanup, frontispiece enrichment.

SCOPE:
- Extract 49 Latin mottos from De Jong OCR markdown
- Write and run extract_dejong_llm.py for emblems XI, XXXVIII, XLVIII
- Write and run a text-cleaning pass on all 47 discourse summaries
- Write frontispiece (Emblem 0) analysis content

INPUTS:
- atalanta fugiens/H M E De Jong Michael Maier's Atalanta fugiens...md
  (11,729 lines, ~152K tokens)
- HARDOCRCASES.md (analysis of why 3 emblems fail)
- scripts/extract_dejong.py and extract_dejong_pass2.py (existing patterns)
- db/atalanta.db (current state: 50/50 mottos EN, 1/50 mottos Latin,
  47/50 discourses)

OUTPUT CONTRACT:
1. extract_dejong_llm.py:
   - Queries DB for emblems with NULL discourse_summary
   - Reads page range from derive_page_ranges()
   - Sends chunk to LLM with extraction prompt
   - Validates: 50-500 words, no duplicate of existing discourse
   - Stores with source_method=LLM_ASSISTED, confidence=MEDIUM, review_status=DRAFT
2. Latin mottos: 50/50 populated in data/seed/emblems.json
   (source_method=CORPUS_EXTRACTION for regex-found, LLM_ASSISTED for cleaned)
3. OCR cleanup script: fixes run-together words, character substitution artifacts
   in discourse_summary text. Does NOT change meaning, only spacing and
   character-level corrections.
4. Frontispiece: Emblem 0 gains discourse_summary, analysis_html,
   and enriched image_description from De Jong's introduction chapter.

DECISION RULES:
- Latin mottos: De Jong reproduces them in each emblem section. Search for
  patterns near MOTTO headers. Where OCR is too garbled, use LLM to
  reconstruct from context. Mark LLM-reconstructed as confidence=MEDIUM.
- OCR cleanup: use deterministic regex first (fix known patterns like
  "thephilosophers" -> "the philosophers"). Only use LLM for ambiguous cases.
- Frontispiece: De Jong's introduction (pages 1-49) discusses the title-page
  engraving extensively. Extract her analysis, not general knowledge.
- All LLM-generated content carries source_method=LLM_ASSISTED,
  confidence=MEDIUM, review_status=DRAFT.
```

---

### PROMPT L4B: Dictionary Enrichment

```
OBJECTIVE: Populate definition_long and registers for all dictionary terms,
and expand the dictionary with new terms from corpus mining.

SCOPE:
- Write definition_long (3-5 sentences) for 38 existing terms
- Populate registers JSON (alchemical, medical, spiritual, cosmological)
  for all terms where multi-register meaning exists
- Mine De Jong discourses for 22+ new term candidates
- Expand term-emblem links for 28 currently unlinked emblems

INPUTS:
- data/seed/dictionary.json (38 terms with definition_short, label_latin,
  significance_to_af)
- De Jong markdown (discourse sections reference alchemical terminology)
- docs/ONTOLOGY.md (dictionary_terms schema)
- DESIREDIMPROVEMENTS.md section 3 (dictionary gaps + candidate terms)
- PRISPEDAGOGYREPORT.md section on Dictionary (pedagogical requirements)

OUTPUT CONTRACT:
1. All 38 existing terms have definition_long (3-5 sentences covering:
   historical usage, alchemical meaning, scholarly literature context)
2. All applicable terms have registers JSON:
   {"alchemical": "...", "medical": "...", "spiritual": "...", "cosmological": "..."}
   Some registers may be null if the term doesn't operate in that domain.
3. 22+ new terms added to dictionary.json with full schema compliance
   (slug, label, category, label_latin, definition_short, definition_long,
   significance_to_af, source_basis, review_status=DRAFT)
4. term_emblem_refs expanded: 45+/50 emblems have at least one term link
5. All new content carries source_method=LLM_ASSISTED, confidence=MEDIUM,
   review_status=DRAFT

DECISION RULES:
- The multi-register model is De Jong's key insight. Prioritize terms where
  she explicitly discusses multiple registers (coniunctio, nigredo, albedo,
  rubedo, lapis, mercurius, sulphur are strong candidates).
- New term candidates from DESIREDIMPROVEMENTS.md: Aqua Regia, Elixir,
  Tinctura, Projectio, Corpus/Spiritus/Anima, Cauda Pavonis, Vitriol,
  Pelican, Phoenix, Rebis, Draco. Only add if De Jong discusses the term.
- Term-emblem links: mine discourse summaries for term mentions. A term is
  linked to an emblem if the term (or its Latin form) appears in the
  emblem's discourse, motto, or De Jong's commentary.
- Categories must be one of: PROCESS/SUBSTANCE/FIGURE/CONCEPT/MUSICAL/SOURCE_TEXT.
```

---

### PROMPT L4C: Tilton Extraction

```
OBJECTIVE: Extract scholarly content from Tilton's The Quest for the Phoenix
into the AtalantaClaudiens database.

SCOPE:
- Write scripts/extract_tilton.py
- Extract emblem-specific interpretive claims -> scholarly_refs
- Extract dictionary term candidates -> dictionary.json staging
- Extract timeline events -> timeline.json staging
- Enrich Tilton's scholar profile

INPUTS:
- atalanta fugiens/Hereward Tilton The Quest for the Phoenix...md (13,881 lines)
- DECKARDTILT.md (boundary analysis, validation rules, what NOT to do)
- data/seed/scholarly_refs.json (existing 64 refs)
- data/seed/dictionary.json (existing 38+ terms)
- data/seed/timeline.json (existing 29+ events)
- docs/ONTOLOGY.md (scholarly_refs, dictionary_terms, timeline_events schemas)

OUTPUT CONTRACT:
1. extract_tilton.py follows the workflow in DECKARDTILT.md:
   a. Deterministic pre-pass: chapter/section boundaries, emblem number detection
   b. LLM pass: extract interpretive claims, classify types, identify candidates
   c. Validation: emblem numbers in 0-50, length limits, confidence defaults
   d. Database insertion with full provenance
2. Output: 20-40 new scholarly_refs with bib_id=tilton_2003
3. Output: 5-15 dictionary term candidates in staging/tilton_dictionary.json
4. Output: 10-20 timeline events in staging/tilton_timeline.json
5. All outputs: source_method=LLM_ASSISTED, confidence=MEDIUM, review_status=DRAFT
6. NO De Jong data overwritten. Tilton is additive only.

DECISION RULES:
- Follow ALL boundary violations listed in DECKARDTILT.md section 2.
- Do NOT use LLM to parse file structure. Chapter boundaries are syntactic.
- Do NOT store raw LLM output without provenance.
- Do NOT overwrite De Jong data. Tilton supplements, never replaces.
- Do NOT let LLM generate SQL. LLM produces JSON; Python handles DB ops.
- Focus on AF-relevant chapters. Skip extended treatment of Maier's other works
  unless they directly illuminate AF emblems.
- Interpretation types: PHILOSOPHICAL, ROSICRUCIAN, ALCHEMICAL, BIOGRAPHICAL.
```

---

### PROMPT L5A: Interface Quick Wins

```
OBJECTIVE: Improve the website's user experience with template-level changes
to build_site.py that require no new JavaScript or data.

SCOPE:
- Home page: add hero section with intro text + "Start Here" button
- Emblem pages: bilingual motto block (Latin above, English below)
- Emblem pages: show epigram by default (remove <details> wrapper)
- Timeline: add era groupings with period headers
- Sources: distinguish MOTTO_SOURCE vs DISCOURSE_CITATION
- Navigation: add Biography link to nav bar

INPUTS:
- scripts/build_site.py (current templates)
- AFSTYLING.md (design system, card templates, cross-linking conventions)
- DESIREDIMPROVEMENTS.md sections 1-2 (emblem + home page improvements)
- PRISPEDAGOGYREPORT.md (pedagogical priorities)

OUTPUT CONTRACT:
1. Home page has a <section class="hero"> with:
   - 2-3 sentence explanation of AF and the project
   - "Start with the Frontispiece" button linking to /emblems/emblem-00.html
   - Reader-facing stats (replace "64 refs, 134 links" with
     "50 emblems explored, 15 source traditions traced, 38+ terms defined")
2. Emblem pages show motto_latin (when populated) above motto_english
   with a thin divider, styled per AFSTYLING.md
3. Epigram is visible by default, not in <details>
4. Timeline has era groupings: "Maier's Lifetime (1568-1622)",
   "Early Editions (1687-1708)", "Modern Scholarship (1910-present)"
   with brief narrative text between groups
5. Sources page shows relationship_type as a sub-badge on emblem links
   (e.g., "MOTTO" vs "DISCOURSE" badge under each emblem number)
6. Nav bar includes Biography link pointing to /biography.html
7. All changes use existing CSS variables from AFSTYLING.md

DECISION RULES:
- Hero text tone: scholarly but inviting. Not academic jargon, not oversimplified.
- Era groupings are hardcoded year ranges, not computed. Simpler and more intentional.
- Do NOT add JavaScript in this phase. Template-only changes.
- Do NOT modify site/style.css structure — only add new classes if needed.
- Preserve the existing comparative layout on emblem pages.
```

---

### PROMPT L5B: Interface New Features

```
OBJECTIVE: Build new interactive features that deepen exploration capabilities.

SCOPE:
- Source x Emblem matrix visualization
- Client-side search
- "What You See" visual description section on emblem pages
- Thematic connections ("See also") between emblems
- Individual source authority pages
- Scholar emblem coverage map

INPUTS:
- site/data.json (current gallery data)
- db/atalanta.db (emblem_sources, source_authorities tables)
- scripts/build_site.py (page generation templates)
- AFSTYLING.md (design system)
- DESIREDIMPROVEMENTS.md sections 4, 11 (sources, cross-cutting)
- PRISPEDAGOGYREPORT.md section 5 (interface features)

OUTPUT CONTRACT:
1. Source x Emblem matrix: JavaScript component rendering a 50-column x 15-row
   grid. Data embedded in page as JSON. Clicking a cell navigates to the
   emblem page. Color intensity = citation count. Exported as part of
   build_site.py's sources page generation.
2. Search: <input> in nav bar, JavaScript searching data.json + dictionary
   terms. Results shown in a dropdown. No external dependencies.
3. "What You See": new section on emblem pages between image and discourse,
   showing visual_elements or image_description if populated.
4. Thematic connections: "See also" section on emblem pages showing 2-4
   related emblems based on shared source_authorities or dictionary_terms.
   Data computed in build_site.py, not at runtime.
5. Individual source pages: /sources/{authority_id}.html with full description,
   all linked emblems with previews, related dictionary terms.
6. Scholar coverage: on each scholar page, a row of 50 small boxes (colored
   if scholar has a scholarly_ref for that emblem, gray if not).

DECISION RULES:
- Matrix visualization: use CSS grid, not canvas or SVG. Simpler, accessible.
- Search: prefix matching, case-insensitive. No fuzzy matching needed.
- Thematic connections: compute at build time. Store as JSON in each emblem's
  data. Top 4 by Jaccard similarity of source + term sets.
- Source pages: follow the pattern of scholar individual pages in build_site.py.
- No external JavaScript libraries. Vanilla JS only.
- All new pages use existing CSS variables and card templates from AFSTYLING.md.
```

---

### PROMPT L6: Pedagogical Scaffolding

```
OBJECTIVE: Write the essay content and guided pathways that transform the site
from a reference tool into a teaching tool.

SCOPE:
- Write 5 thematic essays (1500-3000 words each)
- Build "How to Read an Alchemical Emblem" guided pathway
- Populate essays table and generate essay pages

INPUTS:
- DESIREDIMPROVEMENTS.md section 9 (essay topics and requirements)
- PRISPEDAGOGYREPORT.md (pedagogical mechanics, reader journey mapping)
- SWARMWRITING.md (swarm architecture for essay generation)
- AFSTYLING.md (voice rules, AI disclosure requirements)
- De Jong markdown + Tilton markdown (source material for essays)
- db/atalanta.db (all populated tables for cross-referencing)

OUTPUT CONTRACT:
1. Five essays written and stored in data/seed/essays.json:
   a. "How to Read an Alchemical Emblem" — introductory, worked example
   b. "De Jong's Source-Critical Method" — methodological, with examples
   c. "The Great Work in Fifty Steps" — alchemical processes across emblems
   d. "The Musical Dimension" — fugues as alchemical allegory
   e. "Maier and the Rosicrucian Moment" — historical context
2. Each essay: body_html with cross-links to emblem pages, dictionary terms,
   source authorities. Sources cited listed. is_ai_generated=1.
3. scripts/seed_essays.py populates the essays table from essays.json
4. build_site.py generates /essays/{slug}.html for each essay
5. Essay index page (/essays/index.html) shows cards with abstracts
6. "How to Read" guided pathway: a 3-page sequence
   (Frontispiece -> Emblem I -> "Now you know the method") with
   next/previous navigation
7. All essays carry the AI disclosure banner from AFSTYLING.md

DECISION RULES:
- Present tense for analysis, past tense for history (per AFSTYLING.md).
- De Jong is the canonical anchor. Tilton supplements.
- Cross-links use the conventions in AFSTYLING.md section 5.
- Each essay has an abstract (2-3 sentences) for the index page.
- The "Musical Dimension" essay may be thinner than others since the site
  has no audio component. Acknowledge this limitation honestly.
- All essays are DRAFT status. They require human review before VERIFIED.
- Do NOT reproduce copyrighted material. Paraphrase and cite.
```

---

### PROMPT L7: Image Pipeline

```
OBJECTIVE: Source remaining emblem images and build the vision analysis pipeline.

SCOPE:
- Identify and download 41 emblem plate images (X-L) from public domain sources
- Write scripts/analyze_emblem_images.py
- Populate emblems.visual_elements with structured descriptions

INPUTS:
- site/images/emblems/ (10 existing images: emblem-00.jpg through emblem-09.jpg)
- data/seed/identity.json (51 emblem identity records)
- HIRO321TUNEUP.md (image sourcing status + SHI viewer failure)
- DOWEREALLYNEEDARAG.md section 6 (image analysis pipeline design)
- docs/ONTOLOGY.md (visual_elements column spec)

OUTPUT CONTRACT:
1. 51 emblem images in site/images/emblems/ (emblem-00.jpg through emblem-50.jpg)
2. All images from public domain sources (BSB, Wikimedia Commons, or
   equivalent). NOT from Furnace & Fugue (CC BY-NC-ND).
3. identity.json updated with image_source and image_url for all 51 entries
4. analyze_emblem_images.py:
   - Reads each image file
   - Sends to Claude Vision with structured extraction prompt
   - Extracts: figures, objects, architecture, landscape, symbols, composition
   - Stores as JSON in emblems.visual_elements
   - Validates against image_description field where available
5. All vision-extracted data: source_method=VISION_ANALYSIS, confidence=MEDIUM

DECISION RULES:
- Wikimedia Commons is the preferred source (labeled by emblem number).
- BSB digital collections as fallback.
- If an emblem image cannot be reliably identified, mark
  alignment_confidence=LOW rather than guessing.
- Image format: JPEG, max 1200px wide, reasonable compression.
- The vision prompt should ask for structured JSON output, not prose.
- Compare vision output against De Jong's image_description where available.
  Log discrepancies but do not auto-resolve them.
```

---

## 5. Execution Notes

### 5a. Deterministic vs LLM Layers

| Layer | Type | Human Review Needed? |
|-------|------|---------------------|
| 0: Documentation Reset | DETERMINISTIC | No (can verify by diffing docs against reality) |
| 1: Schema Alignment | DETERMINISTIC | No (SQL migration, testable) |
| 2: Seed Data Refactor | DETERMINISTIC | Regression test: row counts must match |
| 3: Content Enrichment (deterministic) | DETERMINISTIC | Spot-check new timeline events |
| 4A: De Jong Gap-Fill | MIXED (regex + LLM) | Review 3 LLM-extracted discourses, spot-check Latin mottos |
| 4B: Dictionary Enrichment | LLM | Review all definition_long entries and registers JSON |
| 4C: Tilton Extraction | LLM | Review all scholarly_refs, dictionary candidates, timeline events |
| 4D: Alchemical Classification | LLM | Review all 50 stage assignments |
| 5A: Interface Quick Wins | DETERMINISTIC | Visual review of generated pages |
| 5B: Interface New Features | DETERMINISTIC + JS | Functional testing of search, matrix, navigation |
| 6: Pedagogical Scaffolding | LLM | All 5 essays need human review before VERIFIED |
| 7: Image Pipeline | MIXED (sourcing + Vision) | Verify image-emblem alignment for all 41 new images |

### 5b. Swarm Patterns for Parallel Execution

**Layer 0** can run as a single agent or a human session — it's fast enough that parallelism doesn't help.

**Layer 2** must be sequential (refactoring scripts that read from the same file).

**Layer 4** benefits most from parallelism:
```
Workstream 4A (De Jong gap-fill)  ──┐
Workstream 4B (Dictionary)        ──┼── All run in parallel
Workstream 4C (Tilton extraction) ──┤
Workstream 4D (Classification)    ──┘
```

**Layer 5** can split:
```
Phase 5A (build_site.py changes)  ──── Sequential (one file)
Phase 5B (new JS + templates)     ──── Parallel by feature (search agent, matrix agent, source pages agent)
```

**Layer 6** essays are naturally parallel (one agent per essay), following the swarm pattern in SWARMWRITING.md:
```
Essay Agent 1 (How to Read)    ──┐
Essay Agent 2 (Source Method)  ──┤
Essay Agent 3 (Great Work)     ──┼── All produce staging/essays/*.json
Essay Agent 4 (Musical)        ──┤
Essay Agent 5 (Rosicrucian)    ──┘
                                   ↓
                              Merge into data/seed/essays.json
```

### 5c. The Bash Permission Issue

**Problem discovered this session**: Background agents launched via the Agent tool in Claude Code run in a sandboxed environment that does NOT have Bash tool permissions. This means any agent that needs to query the database (`sqlite3 db/atalanta.db`) will fail silently.

**Affected operations**:
- Audit agents that query row counts, NULL counts, or provenance distributions
- Any agent that needs to verify database state before or after insertion
- Validation scripts that read from the DB

**Workarounds**:
1. **Pre-query pattern**: Before launching a background agent, run the DB queries in the foreground session and pass results as text input to the agent prompt.
2. **Foreground-only for DB work**: Run DB-dependent agents as foreground agents (blocking the main session but retaining Bash access).
3. **File-based handoff**: Export DB state to JSON files (`data/db_snapshot/`) that background agents can read via the Read tool without needing Bash.

**Recommended approach for this project**: Use the pre-query pattern. Before each Layer 4 workstream, run a foreground query that dumps relevant DB state to a snapshot file. Background agents read the snapshot instead of querying the DB directly.

### 5d. Execution Order Summary

```
Layer 0: DOCUMENTATION RESET        [~2.5 hrs] [deterministic] [no dependencies]
    ↓
Layer 1: SCHEMA ALIGNMENT           [~0.5 hrs] [deterministic] [depends on L0]
    ↓
Layer 2: SEED DATA REFACTOR         [~2.5 hrs] [deterministic] [depends on L1]
    ↓
Layer 3: CONTENT ENRICHMENT (det.)  [~1 hr]    [deterministic] [depends on L2]
    ↓
Layer 4: CONTENT ENRICHMENT (LLM)   [~12-16 hrs] [LLM, parallel] [depends on L2]
    ↓
Layer 5: INTERFACE IMPROVEMENTS     [~14 hrs]  [deterministic + JS] [depends on L4]
    ↓
Layer 6: PEDAGOGICAL SCAFFOLDING    [~7 hrs]   [LLM, parallel] [depends on L4+L5]
    ↓
Layer 7: IMAGE PIPELINE             [~5-7 hrs] [mixed] [blocked on manual sourcing]
```

**Critical path**: L0 -> L1 -> L2 -> L4 -> L5 -> L6
**Total estimated effort**: ~45-55 hours across all layers
**Layers 0-3 are prerequisite cleanup**: ~6.5 hours before any new content work begins

### 5e. What to Do First

If starting a new session:

1. Run Layer 0 (documentation reset) — it's the highest-leverage work because it prevents every subsequent decision from being based on stale information.
2. Run Layer 1 (schema alignment) — 30 minutes, unblocks dictionary enrichment.
3. Run Layer 2 (seed data refactor) — unblocks parallel agent work on domain-specific seed files.
4. Then choose based on priority:
   - **Highest pedagogical impact**: Layer 5A (home page intro, motto display, epigram)
   - **Highest data impact**: Layer 4C (Tilton extraction — richest secondary source)
   - **Highest completeness impact**: Layer 4A (3 remaining discourses, Latin mottos)
   - **Highest visual impact**: Layer 7 (images — but blocked on manual sourcing)
