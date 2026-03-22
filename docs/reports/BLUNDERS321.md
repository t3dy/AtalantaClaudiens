# BLUNDERS321.md — Blunder Log: Lessons from This Session

**Date**: 2026-03-21
**Purpose**: Document the mistakes, near-misses, and anti-patterns encountered during this marathon session so future sessions don't repeat them.

---

## 1. Swarm Agents Can't Run Bash

**What happened**: Launched 5 background agents to rewrite emblem descriptions. All 5 stalled asking for Bash permission — they couldn't query the SQLite DB or run Python scripts.

**Root cause**: Claude Code's permission system requires interactive user approval for shell access. Background agents can't prompt the user.

**What should have happened**: Either (a) use the staging-file pattern (agents write JSON, main session runs scripts), or (b) pre-query DB data into a JSON export file, or (c) just write the content directly in the main session.

**Fix**: Created `docs/SWARMGUIDELINES.md` and baked the rule into `CLAUDE.md` and `DOCUMENTAIRTRAFFICCONTROL.md`. Future sessions are directed to read the guidelines before launching any agents.

**Cost**: ~20 minutes of wasted agent time across 5 agents. The content was then written in the main session in ~10 minutes.

---

## 2. DB Reset by Agent Pipeline Rebuild

**What happened**: A background agent ran the full pipeline rebuild (`rm -f db/atalanta.db && python scripts/init_db.py && ...`), which reset the database and wiped out all alchemical stage classifications (31/50 → 0/50) and other data that had been set by scripts not in the standard pipeline.

**Root cause**: The alchemical stages were set by a session-specific script (`classify_stages.py`) that wasn't part of the standard pipeline rebuild sequence. When an agent rebuilt from scratch, those classifications were lost.

**What should have happened**: Either (a) stages should be in the seed JSON so they survive rebuilds, or (b) agents should never run a full DB wipe without coordination.

**Fix**: Wrote `classify_stages.py` as a persistent pipeline script. But the broader lesson is that any data set outside the standard pipeline is fragile — it should either be added to the seed data or to a script in the pipeline sequence.

---

## 3. Garbled OCR Stored as Scholarly Refs

**What happened**: The extraction pipeline stored raw OCR text from De Jong's 1969 monograph directly into `scholarly_refs.summary` — including Greek characters, Latin citation fragments with OCR artifacts (`Tkeogoazy`, `Plzilosaplz`, `Am*zf`), and run-together words. These garbled strings were then rendered on emblem pages as "De Jong's analysis," producing unreadable scholarly commentary.

**Root cause**: `extract_dejong.py` extracted text by position/regex without any quality filtering. Long OCR dumps (up to 2011 characters of garbled text) were stored without cleaning.

**What should have happened**: Either (a) the extraction script should have validated text quality before storing, or (b) a post-processing step should clean all extracted text, or (c) scholarly_refs summaries should be LLM-generated prose, not raw OCR dumps.

**Fix**: Wrote `scripts/clean_scholarly_refs.py` with 29 hand-written clean academic summaries replacing the garbled ones. But the underlying extraction architecture should be revisited — scholarly_refs summaries should be curated prose, not raw text.

---

## 4. English Mottos Were Commentary, Not Mottos

**What happened**: The `motto_english` field for many emblems contained not the actual English translation of the motto but excerpts from De Jong's commentary text — including sentences like ": 'Oedipus, havingconquered the Sphinx andhaving killedhisfat her Laius, married his mot her'" (which is De Jong quoting Maier's discourse, not the motto itself).

**Root cause**: The regex extraction in `extract_dejong.py` grabbed the wrong text near the motto marker — it caught whatever appeared after the "MOTTO" heading, which was sometimes the Latin motto, sometimes the commentary.

**What should have happened**: The Latin mottos should have been the primary extraction target (they're more consistently formatted), with English mottos derived from standard scholarship.

**Fix**: Wrote `scripts/fix_english_mottos.py` with 50 standard English translations, replacing all the garbled extracts.

---

## 5. Scholar Page Paragraph Breaks Missing

**What happened**: Scholar profiles were stored with `\n\n` paragraph breaks in the database, but the HTML template rendered them as a single `<div>` without converting the breaks to `<p>` tags. Result: 5-paragraph essays appeared as one unreadable wall of text.

**Root cause**: The template used `{overview}` directly in an HTML div without any text-to-HTML processing.

**Fix**: Added `format_paragraphs()` helper function to `build_site.py` that splits on `\n\n` and wraps each paragraph in `<p>` tags.

---

## 6. Dictionary Index Page Nav Links Broken (CRITICAL)

**What happened**: The dictionary index page (`site/dictionary/index.html`) had all navigation links broken — pointing to `scholars.html` instead of `../scholars.html`, `timeline.html` instead of `../timeline.html`, etc. The CSS stylesheet link was also broken, making the page completely unstyled.

**Root cause**: The `page_shell()` call for the dictionary index was missing `depth=1`, which tells the template to prefix relative URLs with `../` for pages in subdirectories.

**Fix**: Added `depth=1` to the `page_shell()` call. This was the single highest-impact bug — the entire dictionary section was broken on the live site.

---

## 7. Deploying Unverified Images

**What happened** (from prior session, documented in `IMAGEFOLLIES.md`): 41 unverified images (sequential book pages including covers and dedication pages) were renamed as emblem plates and pushed to the live site. Users saw book covers labeled as "Emblem XIV."

**Root cause**: Assumed that sequential page numbers in the SHI viewer corresponded to sequential emblem numbers. They didn't — the pages included prelims, text pages, and other non-plate content.

**Fix**: Never deploy unverified data. Placeholders are better than wrong images. The eventual fix was simple: download correctly labeled images from Wikimedia Commons with 8-second delays.

---

## 8. ONTOLOGY.md Documenting Non-Existent Tables/Columns

**What happened**: ONTOLOGY.md documented 18 tables and several columns that didn't exist in the actual database. Scripts written against documented-but-non-existent columns crashed (`visual_elements`, `fugue_mode`, `fugue_interval`, `epigram_german`, `registers`).

**Root cause**: The schema documentation was aspirational — it described the target schema, not the actual schema. No mechanism distinguished planned tables from built ones.

**Fix**: Tagged every table and column in ONTOLOGY.md as `[BUILT]` or `[PLANNED]`. Created `migrate_v4_enrichment.py` to add the 5 missing columns. The rule going forward: ONTOLOGY.md must reflect reality, with planned items explicitly flagged.

---

## 9. Premature Parallelism in Image Sourcing

**What happened** (from prior session, documented in `IMAGEFOLLIES.md`): Launched 3 sourcing agents to search different image repositories simultaneously before understanding the basic download mechanics. The bottleneck was rate limiting, not research speed — parallelism actually made things worse by hitting Wikimedia rate limits from multiple agents.

**Root cause**: Cargo-cult engineering. "Swarm everything" is not always the right strategy. Image downloads are I/O-bound and rate-limited; parallelism hurts when the bottleneck is external.

**Fix**: One sequential script with 8-second delays downloaded all images in 4 minutes. The lesson: understand the bottleneck before choosing a concurrency strategy.

---

## 10. Swarm Schema Heterogeneity Risk

**What happened** (in progress, flagged by user): Launching 4 agents to write scholarly work summaries with slightly different instructions risks producing heterogeneous JSON output — different field names, inconsistent nesting, mixed null/empty-string conventions. If one agent invents fields or changes schema, the merge becomes a salvage operation.

**Root cause**: Each agent receives its instructions independently and may interpret schema requirements slightly differently. Batch D was especially risky because it mixed scholarly works and dictionary terms — two different entity types in one output file.

**Mitigation**:
1. Define a canonical schema before launching agents
2. Separate different entity types into different output keys
3. Validate all agent output before merging
4. Reject and regenerate any batch that doesn't conform
5. Normalize dates, types, and confidence values in a dedicated step

---

## Meta-Lessons

### 1. Physical order > logical order
When slicing text by detected markers, sort by byte position, not by item number. The text doesn't care about your data model.

### 2. Domain knowledge > regex sophistication
Knowing that De Jong's analysis starts at page 51 was worth more than any regex improvement. Filter by position before pattern-matching.

### 3. The bug is in the plumbing, not the detector
Most debugging time was spent improving regex patterns, but the actual bugs were in dedup logic, sort order, and boundary calculations.

### 4. Patience > cleverness
8-second delays between Wikimedia downloads solved what 45 minutes of retry-loop engineering couldn't.

### 5. Never deploy unverified data
Placeholders are always better than wrong data on a live site.

### 6. Document reality, not aspiration
Schema docs must reflect what exists, with planned items explicitly flagged.

### 7. Understand the bottleneck before parallelizing
Swarms are powerful for CPU-bound research. They're counterproductive for I/O-bound downloads or rate-limited APIs.

### 8. Curated prose > raw extraction
Scholarly summaries should be written, not extracted. OCR dumps are never reader-ready.
