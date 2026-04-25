# PHASESTATUS.md — Session Discipline Log

## Current Phase: 3A/3B complete, 4 essentially complete (4D/4C ongoing), 5A complete (images)
## Schema Version: 5 (v1 core + v2 phase2-3 + v3 enrichment + v4 identity + v4 enrichment cols)
## Document Routing: See `DOCUMENTAIRTRAFFICCONTROL.md` for which file to consult for any task

---

## Session: 2026-04-25 — Dictionary Multi-Register Expansion (Phase 4C)

### What Shipped (4 PRs, all merged + deployed)

- **PR #1** — Phase 4C batch 1: 7 CONCEPT terms (alembic, athanor, four-elements, mercury-sulphur-theory, garden-of-hesperides, golden-apple, golden-fleece) gain four-register treatment (alchemical / medical / spiritual / cosmological).
- **PR #2** — Phase 4C batch 2: 13 more terms (5 substances, 5 figures, 3 concepts).
- **PR #3** — Phase 4C batch 3: 15 mythological figures and alchemical creatures tied directly to specific emblems (boreas, hippomenes, jason, medea, kronos-saturn, ulysses-odysseus, oedipus, ceres, naaman, alchemical-eagle/-lion/-wolf, salamander, raven-crow, philosophical-bird).
- **PR #4** — Phase 4C batch 4: 11 more figures and concepts (alchemical-dog, alchemical-toad, apocalyptic-woman, cybele, dryad, geryon, screech-owl, lusus-serius, prisca-sapientia, mytho-alchemy, rosicrucian-brotherhood).
- **Visual-elements pass** — added 12 NEW dictionary terms for recurring visual elements depicted across the emblem plates (hesperides, earth-mother, arbor-philosophica, philosophical-child, balneum, celestial-dew, alchemical-rose, hierogamy, wild-boar, pallas-athena, triptolemus, flaming-sword), each with full definition_short / definition_long / significance_to_af / registers, plus 29 term-emblem links. Also populated registers for the two MUSICAL terms (cantus-firmus, fugue).

### Current Database Totals
- Dictionary terms: **140** (was 128) — 32 CONCEPT, 41 FIGURE, 2 MUSICAL, 18 PROCESS, 25 SOURCE_TEXT, 22 SUBSTANCE
- Terms with multi-register treatment: **113 / 140** (~81%; remaining 27 are mostly source-text titles where four-register reading would be forced)
- Term-emblem refs: 141 (was 112)

### Operating Note for Future Sessions
- `scripts/build_site.py` is currently destructive for `site/essays/*.html` and `site/bibliography.html`: live site holds hand-curated content not in the DB, and a full rebuild silently regresses essays into stub text. After running `build_site.py`, always `git checkout -- site/essays/ site/bibliography.html` before staging, and only stage targeted files. This is a known divergence from the SQLite-as-source-of-truth rule; reconciling essay/bibliography content into the DB is out of current shipping scope.

### Live URL
- https://t3dy.github.io/AtalantaClaudiens/

---

## Session: 2026-03-21 — Foundation to Deployment

### What Was Built (cumulative)

**Pipeline (13 scripts)**:
- init_db.py → migrate_v2.py → migrate_v3.py → migrate_v3_identity.py
- seed_from_json.py → seed_phase2.py → seed_identity.py
- extract_dejong.py → extract_dejong_pass2.py
- link_dictionary.py → seed_emblem_analyses.py
- build_site.py → validate_identity.py

**Extraction**:
- De Jong (1969): 49 sections found by regex, 50/50 mottos, 50/50 discourses
- OCR fixes: position-aware dedup, `(fig. N)` recovery, `SU.{0,8}ARY` tolerance
- 3 hard cases (XI, XXXVIII, XLVIII) resolved by widened end boundary
- OCR run-together cleanup: `clean_ocr_text.py` — deterministic regex-based splitting of 47/47 discourse summaries (camelCase splits, function-word prefix/suffix detection, recursive word-boundary resolution, OCR mid-word rejoin patterns)

**Content Overhaul (writing swarm)**:
- 50/50 emblem analysis blocks with cross-links to sources and dictionary
- 38 dictionary terms with Latin forms and AF significance
- 29 timeline events (including Rosicrucian manifestos, Rudolf II context)
- 11 scholar profiles with rich overviews
- 10 annotated bibliography entries
- Maier biography page (6 sections)
- 31/50 alchemical stage classifications

**Infrastructure**:
- Emblem identity layer (deterministic image grounding, 10 HIGH confidence)
- CSS design system (emblem-analysis, source-card, timeline-card, dict-card, ai-banner)
- Home page intro + "Start with the Frontispiece" button
- Biography added to nav bar
- GitHub Pages deployment at t3dy/AtalantaClaudiens

### Database Totals
- Emblems: 51 (50/50 mottos EN+LA, 47/50 discourses, 50/50 analyses)
- Latin mottos: 50/50
- Alchemical stages: 50/50 classified (NIGREDO 17, ALBEDO 11, CITRINITAS 11, RUBEDO 11)
- Scholarly refs: 64
- Emblem-source links: 134
- Source authorities: 15 (all with description_long)
- Dictionary terms: 73 (all with definition_long, label_latin, significance_to_af)
- Term-emblem links: 112
- Timeline events: 29 (all with description_long)
- Scholars: 11 (all with overviews)
- Bibliography: 10 (all with annotations)
- Emblem images: 51 on disk (Wikimedia Commons)
- Schema version: 5 (v4 + enrichment columns)
- DB tables: 14 built, 7 planned (see ONTOLOGY.md for `[BUILT]`/`[PLANNED]` tags)
- Pipeline scripts: 20

### Pipeline Command
```bash
rm -f db/atalanta.db
python scripts/init_db.py
python scripts/migrate_v2.py
python scripts/migrate_v3.py
python scripts/migrate_v3_identity.py
python scripts/migrate_v4_enrichment.py
python scripts/seed_from_json.py
python scripts/seed_phase2.py
python scripts/seed_identity.py
python scripts/extract_dejong.py
python scripts/extract_dejong_pass2.py
python scripts/link_dictionary.py
python scripts/seed_emblem_analyses.py
python scripts/build_site.py
python scripts/validate_identity.py
```

### Reports Produced (23 .md files)
AFSTYLING.md, DECKARDAF1.md, DECKARDTILT.md, DESIREDIMPROVEMENTS.md,
DOWEREALLYNEEDARAG.md, HANDOVER.md, HARDOCRCASES.md, HIRO321TUNEUP.md,
HIROREBUILD.md, PRISPEDAGOGYREPORT.md, REFLAYERAF1.md, SWARMWRITING.md,
SwarmContentAudit.md, SwarmPipelineAudit.md, SwarmProvenanceAudit.md,
SwarmSchemaAudit.md, TRIALANDERROR.md, MISSINGEMBLEMS.md

### Git Commits: 15

### What Changed This Session (2026-03-21 evening)
- **DOCUMENTAIRTRAFFICCONTROL.md** created — LLM routing guide for all project docs
- **Schema v5**: migrate_v4_enrichment.py added visual_elements, fugue_mode, fugue_interval, epigram_german, registers columns
- **Latin mottos**: 50/50 populated (seed_latin_mottos.py)
- **Alchemical stages**: 50/50 classified (classify_stages.py)
- **OCR cleanup**: discourse summaries + mottos + epigrams cleaned (clean_ocr_text.py extended)
- **Dictionary**: expanded from 38 to 73 terms, all with definition_long (seed_definition_long.py)
- **Term-emblem links**: expanded from 66 to 112
- **UI enhancements**: bilingual motto block (Latin italic above English), epigram visible by default, stage badges on headings + gallery cards, "What You See" visual description section
- **Documentation fixes**: ROADMAP.md, ONTOLOGY.md (BUILT/PLANNED tags, 2 missing tables documented, 5 planned columns flagged then created), INTERFACE.md (biography page, dictionary rename, sources/timeline updates), PIPELINE.md (migrate_v4, TEMPLATE_ASSEMBLY fix), CLAUDE.md (file tree, table counts, DATC reference), parent CLAUDE.md (phase status update)

### Next Steps (priority order, essays are LOW priority)
1. Tilton extraction (13,881 lines → scholarly_refs) — highest-value new data
2. Secondary scholar extraction (Craven, Wescott, Pagel, Miner)
3. Image-emblem verification (~27 need visual confidence check)
4. Image descriptions for 28 missing emblems
5. 3 remaining discourse summaries (XI, XXXVIII, XLVIII)
6. Vision pipeline (Claude Vision on plates → visual_elements)
7. Multi-register dictionary definitions (populate `registers` JSON)
8. 5 essays (LOW priority, after Tilton)

### Blockers
- Tilton not yet extracted (13,881 lines available)
- 5 essays empty (planned topics exist, content not written — LOW priority)
- 7 ONTOLOGY tables never created (need migrations if/when needed)
