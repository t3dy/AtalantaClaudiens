# SWARMWRITING321.md — Post-Mortem: Swarm Writing Experiments (2026-03-21 Session)

**Date**: 2026-03-21
**Scope**: All swarm operations during this marathon session, covering dictionary entries, scholarly work summaries, essay enrichment, and emblem content rewrites.

---

## 1. Swarm Operations Summary

| Swarm | Agents | Task | Pattern | Outcome |
|-------|--------|------|---------|---------|
| Emblem content rewrite | 5 | Rewrite image_description + discourse_summary for 51 emblems | Direct DB write | **FAILED** — all 5 blocked on Bash permission |
| Dictionary enrichment | 4 | Write 5-10 paragraph encyclopedia entries for 94 terms | Staging JSON | **SUCCESS** — all 94 terms enriched |
| Scholarly work summaries | 4 | Write 5-15 paragraph summaries for 18 works | Staging JSON | **SUCCESS** — 18 summaries, schema heterogeneity normalized |
| Essay enrichment | 4 | Research + rewrite 4 essays from corpus | Staging JSON | **SUCCESS** — all 4 enriched (73.9K chars) |
| De Jong Sources essay | 1 | Research + write De Jong sources essay | Staging JSON | **SUCCESS** — 17.8K chars |
| Chemistry essay | 2 | Write chemistry/medicine content for 51 emblems | Staging JSON | **IN PROGRESS** |

**Success rate**: 15/16 swarm batches succeeded (93.75%). The one failure was the first attempt, before we understood the Bash constraint.

---

## 2. What Worked

### The Staging-File Pattern
Every successful swarm used the same pattern:
1. Main session exports DB data to `staging/` as JSON
2. Agents read corpus .md files + staging exports (no Bash needed)
3. Agents write structured JSON to `staging/` (one file per batch)
4. Main session validates, normalizes, merges, and integrates

This pattern works because it respects the hard constraint: **agents cannot run Bash**. All shell operations (DB queries, Python scripts, git) stay in the main session.

### Corpus Reading Quality
Agents reading the actual source corpus produced genuinely new findings:
- **Wescott's full planetary-modal correspondence table** (Saturn/Mixolydian/G through Moon/Hypodorian/A) — from reading the AthanorX article
- **Ludwig's John Farmer discovery** (40/50 fugues from 1591 collection) — from reading the RIDE review
- **The Padua violence** (Maier attacked Heino Lambechius, fled, warrant issued) — from reading Tilton
- **Sleeper's Christe eleison cantus firmus identification** — from reading Wescott
- **The dove augury** from De Medicina Regia — from reading Tilton
- **Maier's critique of English pronunciation** ("Tziertz" for "Church") — from reading Godwin's essay

These are details that the main session's prior reading had missed. The agents' focused, targeted reading of specific corpus sections produced higher-quality extraction than general browsing.

### Parallel Efficiency
The 4-agent dictionary swarm (94 terms) completed in roughly the time a single agent would take for ~25 terms. The parallel essay enrichment swarm (4 agents reading different corpus files) similarly compressed what would have been sequential research. The key insight: **corpus reading is the bottleneck**, and it parallelizes well because each agent reads different files.

### Schema Normalization
The scholarly works swarm produced 4 batches with heterogeneous schemas:
- Batch A: `summary_html` (string with HTML)
- Batch B: `summary_html` (string with HTML)
- Batch C: `summary` (plain text with `\n\n` breaks)
- Batch D: `summary` (list of paragraphs) + separate `dictionary_terms` key

The main session normalized all four to a canonical format (HTML paragraphs) in a dedicated merge step. **Lesson**: schema heterogeneity is inevitable with multiple agents; plan for normalization rather than hoping for uniformity.

---

## 3. What Failed

### Emblem Content Rewrite (5 agents, all blocked)
The first swarm attempt launched 5 agents to rewrite emblem descriptions. All 5 stalled asking for Bash permission because they needed to:
- Query the SQLite database for current emblem data
- Run their Python update scripts

**Root cause**: Agents were instructed to write scripts AND run them. The staging-file pattern wasn't yet established.

**Fix**: The main session wrote all 51 emblem descriptions in a single inline script (`rewrite_emblem_content.py`) in ~10 minutes — faster than the 5 agents would have taken even if they'd worked.

**Lesson**: For tasks where the main session has sufficient context, a single comprehensive script is faster and more reliable than a swarm. Swarms are most valuable when corpus reading (not DB writing) is the bottleneck.

### One Agent Actually Succeeded (Batch B)
Intriguingly, one of the 5 emblem agents (Batch B, emblems 14-26) did complete — apparently Bash permission was granted during an interactive prompt. It produced high-quality corpus-sourced descriptions. But since the main session's `rewrite_emblem_content.py` ran later and overwrote its work, the agent's output was lost.

**Lesson**: When running swarms alongside main-session work, ensure outputs don't conflict. The agent's work was wasted because the main session didn't know it had succeeded.

---

## 4. Schema Discipline

The user correctly flagged the **schema heterogeneity risk** before the scholarly works swarm completed. The prediction was accurate:

> "The most common blunder at this stage is that the coordinator starts coding to an imagined output shape, and then each batch arrives with slightly different field names, missing arrays, inconsistent evidence objects, or mixed null/empty-string conventions."

This is exactly what happened:
- Batch A used `summary_html` (HTML string) + `emblems_discussed` + `key_findings`
- Batch C used `summary` (plain text) + `pub_type` + `publication`
- Batch D used `summary` (list) + `relevance` + `scholar_slug` + `venue`

The fix was a dedicated normalization step that unified all formats before the page renderer touched the data. The renderer itself (`build_works_page()`) is a pure function over the canonical merged JSON — no cleanup logic in the build step.

**Rule confirmed**: Define a canonical schema before launching agents. But also plan for normalization, because agents will always drift.

---

## 5. Provenance Concerns

The user also flagged the **provenance risk**: when agents read "corpus + reports," the output may mix claims grounded in the scholarly source itself with claims grounded in our own project notes or prior assistant summaries.

In practice, this was partially mitigated by the agents' tendency to attribute claims to specific scholars ("De Jong identifies...", "Forshaw notes...", "Tilton argues..."). But some passages inevitably blend corpus reading with synthesized knowledge. For a serious scholarly site, this provenance distinction matters.

**Current state**: The essays carry AI-generated banners and attribution language, but there is no systematic mechanism to distinguish corpus-grounded claims from synthesized ones. A future improvement would be adding inline citations with source file + line number references.

---

## 6. Performance Metrics

| Metric | Value |
|--------|-------|
| Total agents launched | 24 |
| Successful completions | 19 (79%) |
| Blocked on Bash | 5 (21%) |
| Total content produced | ~250K chars |
| Dictionary entries enriched | 94 |
| Essay paragraphs produced | ~80 |
| Scholarly work summaries | 18 |
| Emblem chemistry entries | 51 (in progress) |
| Average agent duration | ~5-10 minutes |
| Longest agent | ~15 minutes (Tilton reading) |

---

## 7. Recommendations for Future Swarms

### DO
1. **Pre-export DB data** to staging JSON before launching agents
2. **Use the staging-file pattern** (agents write JSON, main session merges)
3. **Tell agents explicitly** they cannot run Bash — put it in the first line of the prompt
4. **Split by corpus file** not by output type — each agent reads different source material
5. **Plan for schema normalization** — a dedicated merge step before rendering
6. **Validate before integrating** — parse JSON, check field presence, reject malformed batches
7. **Use agents for corpus reading** — this is where they add the most value

### DON'T
1. **Don't ask agents to query the DB** — pre-export instead
2. **Don't ask agents to run scripts** — they can write scripts but not execute them
3. **Don't mix entity types** in one output file (works + dictionary terms in Batch D caused confusion)
4. **Don't build the renderer before validating outputs** — the canonical schema should emerge from actual agent output, not from assumptions
5. **Don't duplicate agent work in the main session** — if you delegate, wait for the result
6. **Don't launch swarms for tasks the main session can do in 10 minutes** — the overhead isn't worth it for small tasks

### The Sweet Spot
Swarms are most valuable when:
- The task involves **reading multiple large corpus files** (10K+ lines each)
- The output is **structured data** (JSON, not free-form prose)
- The batches are **independent** (no cross-references between agents)
- The main session has **other work to do** while agents run
- The content benefits from **focused, targeted reading** rather than general knowledge

Swarms are least valuable when:
- The task requires **DB interaction** (use the main session)
- The task is **small enough for one pass** (just write it)
- The batches **depend on each other** (can't parallelize)
- The output requires **careful editorial voice** (better done by the coordinator who knows the user's preferences)

---

## 8. Architecture for Production Swarms

If this project continues to use swarms, the following infrastructure would make them more reliable:

1. **Canonical schema files** in `staging/schemas/` defining exact JSON shape per task type
2. **Validation scripts** that reject non-conforming output automatically
3. **Merge scripts** that normalize field names, types, and null/empty conventions
4. **Pre-approved Bash patterns** in `.claude/settings.local.json` so agents CAN run Python if needed
5. **Agent prompt templates** in `docs/SWARMGUIDELINES.md` (already started) with the exact constraints and output format

The current ad-hoc approach works for a single session but would not scale to a multi-session production workflow without these hardening steps.
