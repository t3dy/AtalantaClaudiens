# Pipeline Audit Report

**Date**: 2026-03-21
**Auditor**: Pipeline Audit Agent

---

## 1. Scripts: Documented vs Actual

### PIPELINE.md Documents These Scripts (12 total)

| Script | Exists on Disk? | Stage |
|--------|:---------------:|-------|
| `init_db.py` | YES | 1: Scaffold |
| `migrate_v2.py` | YES | 1: Scaffold |
| `migrate_v3.py` | YES | 1: Scaffold |
| `migrate_v3_identity.py` | YES | 1: Scaffold |
| `seed_from_json.py` | YES | 1: Scaffold |
| `seed_phase2.py` | YES | 1: Scaffold |
| `seed_identity.py` | YES | 1: Scaffold |
| `extract_dejong.py` | YES | 2: Extract |
| `extract_dejong_pass2.py` | YES | 2: Extract |
| `link_dictionary.py` | YES | 3: Enrich |
| `seed_emblem_analyses.py` | YES | 3: Enrich |
| `build_site.py` | YES | 4: Build |
| `validate_identity.py` | YES | 5: Validate |

### Actual Scripts on Disk (13 total)

All 13 `.py` files in `scripts/` are documented in PIPELINE.md.

---

## 2. Phantom Scripts (documented but do not exist)

### In PIPELINE.md "Future Stages" Section

These are listed as planned/future and do NOT exist on disk. This is expected and correctly documented as future work:

- `extract_tilton.py` (Stage 2b)
- `extract_secondary.py` (Stage 2b)
- `analyze_emblem_images.py` (Stage 3b)

### In CLAUDE.md File Structure

The CLAUDE.md file structure lists three scripts that do NOT exist:

| Script | Listed In | Exists? | Notes |
|--------|-----------|:-------:|-------|
| `extract_secondary.py` | CLAUDE.md file tree | NO | Listed as Stage 2; never created |
| `seed_dictionary.py` | CLAUDE.md file tree | NO | Listed as Stage 3; functionality absorbed into `seed_phase2.py` |
| `seed_timeline.py` | CLAUDE.md file tree | NO | Listed as Stage 3; functionality absorbed into `seed_phase2.py` |
| `validate.py` | CLAUDE.md file tree | NO | Listed as Stage 5; replaced by `validate_identity.py` |

**Finding**: CLAUDE.md file structure is stale. It reflects an earlier design where dictionary/timeline seeding and general validation were separate scripts. The actual pipeline consolidated these differently.

---

## 3. Undocumented Scripts (exist but not in PIPELINE.md)

**None.** All 13 scripts on disk are accounted for in PIPELINE.md.

---

## 4. Execution Order Analysis

### Documented Full Rebuild Command

```
rm -f db/atalanta.db
python scripts/init_db.py
python scripts/migrate_v2.py
python scripts/migrate_v3.py
python scripts/migrate_v3_identity.py
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

### Dependency Verification

| Script | Requires | Order Correct? |
|--------|----------|:--------------:|
| `init_db.py` | Nothing (creates DB from scratch) | YES |
| `migrate_v2.py` | Existing DB with base tables | YES (after init_db) |
| `migrate_v3.py` | Existing DB with v2 tables | YES (after migrate_v2) |
| `migrate_v3_identity.py` | Existing DB | YES (after migrate_v3) |
| `seed_from_json.py` | Base tables + `atalanta_fugiens_seed.json` | YES |
| `seed_phase2.py` | v2 tables + `atalanta_fugiens_seed.json` | YES (after migrate_v2) |
| `seed_identity.py` | `emblem_identity` table + `data/emblem_identity_seed.json` | YES (after migrate_v3_identity) |
| `extract_dejong.py` | Seeded emblems + De Jong markdown | YES (after seed) |
| `extract_dejong_pass2.py` | First pass results | YES (after extract_dejong) |
| `link_dictionary.py` | dictionary_terms + emblems | YES (after seed_phase2) |
| `seed_emblem_analyses.py` | All content tables populated | YES (after extract + link) |
| `build_site.py` | Fully populated DB | YES (last data step) |
| `validate_identity.py` | emblem_identity populated | YES (final step) |

### Verdict: Execution order is correct. The rebuild command should work from a clean state.

### Minor Note on `seed_identity.py`

This script reads from `data/emblem_identity_seed.json`, which does exist on disk. No issue.

---

## 5. ROADMAP.md Staleness Assessment

**Verdict: SEVERELY STALE**

ROADMAP.md reflects an early planning state and has not been updated since the initial session. Key discrepancies:

| Item | ROADMAP.md Says | Actual State |
|------|----------------|--------------|
| Phase 1, Slice 1A (schema) | IN PROGRESS | DONE -- init_db.py, migrate_v2, v3, v3_identity all exist and work |
| Phase 1, Slice 1B (seed) | READY | DONE -- seed_from_json.py, seed_phase2.py, seed_identity.py all work |
| Phase 1, Slice 1C (extraction) | READY | DONE -- 50/50 mottos, 34/50 discourses |
| Phase 1, Slice 1D (verification) | READY | DONE -- validate_identity.py exists |
| Phase 2, Slice 2A (CSS/JS) | DEFERRED | DONE -- style.css, components.css, script.js exist |
| Phase 2, Slice 2B (build_site.py) | DEFERRED | DONE -- generates gallery, emblem pages, dictionary, timeline, scholars, sources, about |
| Phase 2, Slice 2C (scholars/bib) | DEFERRED | DONE -- scholars table populated, scholar pages generated |
| Phase 3A (dictionary) | DEFERRED | DONE -- 23 terms with Latin labels, term pages generated |
| Phase 3B (timeline) | DEFERRED | DONE -- 20 events with descriptions |
| Phase 3C (sources page) | DEFERRED | DONE -- sources page with rich cards |
| Phase 3D (secondary extraction) | DEFERRED | Still deferred (correct) |
| Phase 4A (images) | BLOCKED | Partially done -- emblem_identity table exists, some images present |
| Phase 4B (essays) | DEFERRED | Partially done -- essays index exists |
| Deferred schema tables | All listed as deferred | Most are now created: scholars, scholar_works, dictionary_terms, dictionary_term_links, term_emblem_refs, timeline_events, emblem_identity |

**Summary**: ROADMAP.md shows Phase 1 as "IN PROGRESS" and everything else as "DEFERRED" or "BLOCKED". In reality, Phases 1-3 are substantially complete. The document has not been updated since the very first session.

---

## 6. PHASESTATUS.md Staleness Assessment

**Verdict: MODERATELY STALE**

PHASESTATUS.md has two session entries, both dated 2026-03-21. The most recent (session "b") is more current but still outdated:

### Accurate in PHASESTATUS.md
- Current Phase marked as 2 (reasonable, though Phase 2 is substantially complete)
- Schema Version listed as 2 (actually now at v3 with identity -- should be updated)
- Database totals from session "b" (51 emblems, 50/50 mottos, 34/50 discourses, 23 dictionary terms, 20 timeline events, 11 scholars)
- Pipeline command in session "b" is close but missing: `migrate_v3.py`, `migrate_v3_identity.py`, `seed_identity.py`, `seed_emblem_analyses.py`

### Missing from PHASESTATUS.md
- No session entry for the work that added: `migrate_v3.py`, `migrate_v3_identity.py`, `seed_identity.py`, `seed_emblem_analyses.py`, `validate_identity.py`
- Schema version should be 3 (or "3+identity")
- The "Current Slice" header says "2A complete, 2B in progress" but 2B appears substantially complete
- No mention of the enrichment layer (Stage 3: `link_dictionary.py`, `seed_emblem_analyses.py`)
- No mention of the identity/image grounding work

### Pipeline Command Drift

The pipeline command in PHASESTATUS.md session "b":
```
rm -f db/atalanta.db && python scripts/init_db.py && python scripts/migrate_v2.py && python scripts/seed_from_json.py && python scripts/seed_phase2.py && python scripts/extract_dejong.py && python scripts/extract_dejong_pass2.py && python scripts/link_dictionary.py && python scripts/build_site.py
```

Missing from this command (but present in PIPELINE.md's rebuild command):
- `migrate_v3.py`
- `migrate_v3_identity.py`
- `seed_identity.py`
- `seed_emblem_analyses.py`
- `validate_identity.py`

PIPELINE.md has the correct and complete rebuild command.

---

## 7. Recommendations

### High Priority

1. **Update ROADMAP.md** -- Mark Phases 1-3 slices as BUILT/DONE. This document is severely misleading in its current state. Anyone reading it would think the project is in early Phase 1.

2. **Update PHASESTATUS.md** -- Add a new session entry documenting the v3 migration, identity system, emblem analyses enrichment, and validate_identity work. Update the header to reflect Schema Version 3 and current phase/slice status.

3. **Update CLAUDE.md file structure** -- Remove phantom scripts (`extract_secondary.py`, `seed_dictionary.py`, `seed_timeline.py`, `validate.py`) or clearly mark them as planned/future. The current file tree implies these exist.

### Medium Priority

4. **PIPELINE.md Stage Overview line is missing `validate_identity.py`** -- The Stage Overview block at the top does not list `validate_identity.py` in the STAGE 5 line, though it is documented below and in the rebuild command. The overview line says just `validate_identity.py` -- actually this is present. No issue here on closer inspection.

5. **PIPELINE.md Stage 1 section is missing `migrate_v3_identity.py` and `seed_identity.py` documentation** -- The Stage Overview lists them but there are no detailed subsections (### headers) for `migrate_v3_identity.py` or `seed_identity.py` like there are for the other Stage 1 scripts. Add matching documentation blocks.

### Low Priority

6. **Consider adding `extract_secondary.py`** to the pipeline as a concrete next step, since it is the primary remaining extraction gap (secondary scholars: Tilton, Pagel, Wescott, Craven).

7. **The 16 missing discourse summaries** noted in PHASESTATUS.md remain an open gap. Consider whether `extract_dejong_pass2.py` improvements or manual curation can close this.

---

## Summary

| Aspect | Status |
|--------|--------|
| PIPELINE.md vs actual scripts | ALIGNED -- no phantom scripts, no undocumented scripts |
| Execution order | CORRECT -- dependencies respected |
| Full rebuild command | CORRECT -- would work from clean state |
| ROADMAP.md | SEVERELY STALE -- shows Phase 1 in progress, reality is Phase 3 substantially complete |
| PHASESTATUS.md | MODERATELY STALE -- missing at least one session of work (v3 + identity) |
| CLAUDE.md file tree | STALE -- lists 4 scripts that do not exist |
