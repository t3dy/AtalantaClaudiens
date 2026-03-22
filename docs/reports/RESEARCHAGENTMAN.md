# RESEARCHAGENTMAN.md — How Research Agents Work and How They Worked for Us

**Date**: 2026-03-21

---

## What Is a Research Agent?

A research agent is a background subprocess launched from the main Claude Code session using the `Agent` tool. It runs autonomously with its own context window, reading files, searching text, and producing output — but it cannot interact with the user, run shell commands, or modify the database.

### How It's Launched

```
Agent(
    description="Research music essay enrichment",
    prompt="You are researching for AtalantaClaudiens...",
    subagent_type="general-purpose",
    run_in_background=True
)
```

The main session specifies:
- **What to read**: specific corpus files, staging exports, reports
- **What to produce**: a JSON file written to `staging/`
- **What NOT to do**: no Bash, no DB queries, no code edits
- **The exact output schema**: field names, structure, format

The agent then works autonomously, typically for 3-15 minutes, reading the assigned files and writing structured output. The main session is notified when it completes and can read the output.

### What Agents CAN Do
- Read any file on disk (corpus .md files, staging JSON, reports)
- Search files with Grep (regex patterns across large corpora)
- Write new files (staging JSON, never code or DB)
- Launch sub-agents (though we didn't use this)

### What Agents CANNOT Do
- Run Bash/Python/shell commands (the hard constraint)
- Query SQLite databases
- Modify application code
- Interact with the user for approval
- Access the internet (no web searches)

---

## How We Used Research Agents

### Pattern 1: Corpus Reading Swarm (Dictionary Enrichment)

**Task**: Write 5-10 paragraph encyclopedia entries for 94 dictionary terms.

**Setup**: Main session exported all term data to `staging/dict_terms_export.json`. Four agents launched, each assigned a category (PROCESS, FIGURE, SUBSTANCE, CONCEPT+SOURCE_TEXT).

**What agents did**: Each read De Jong's 11,729-line monograph, searching for mentions of their assigned terms. They also read Forshaw's transcript, the scholar profiles, and the Szulakowska report.

**Result**: 94 entries produced in ~10 minutes wall time. Quality was high — agents found specific emblem references, attributed claims to scholars, and followed the voice rules from WRITING_TEMPLATES.md.

**What worked**: Splitting by category meant each agent read the same corpus but searched for different terms — no duplication of effort. The corpus reading was the bottleneck, and it parallelized perfectly.

### Pattern 2: Essay Enrichment Swarm

**Task**: Research and rewrite 4 essays with specific corpus-grounded detail.

**Setup**: Main session exported emblem data and scholar info to staging. Four agents launched, each assigned one essay (Music, Social World, Jung, Paracelsianism).

**What agents did**: Each read 2-6 specific corpus files relevant to their essay topic, searching for named scholars, specific arguments, page references, and quotable material.

**Key findings agents surfaced that the main session had missed**:
- Wescott's full planetary-modal correspondence table (Saturn/Mixolydian/G through Moon/Hypodorian/A)
- Ludwig's discovery that 40/50 fugues derive from John Farmer's 1591 collection
- The Padua violence (Maier attacked Heino Lambechius, fled, warrant issued — from Tilton/Figala-Neumann)
- Sleeper's 1938 identification of the Christe eleison cantus firmus
- Maier's critique of English Latin pronunciation ("Tziertz" for "Church")
- The dove augury from De Medicina Regia
- Tilton's argument that "Jung is alchemy's latest practitioner, not its interpreter"

**Result**: 73.9K chars of enriched essay content, substantially more detailed than the main session's initial drafts.

### Pattern 3: Scholarly Work Summaries Swarm

**Task**: Write 5-15 paragraph summaries of 18 scholarly works on AF.

**Setup**: Four agents assigned chronological batches (1910-1969, 1985-2003, 2009-2020, misc).

**Schema heterogeneity problem**: Each batch used slightly different field names (`summary_html` vs `summary`, string vs list). The main session had to normalize in a dedicated merge step.

**Result**: 18 work summaries produced with good scholarly quality. The merge step was ~5 minutes of Python normalization.

### Pattern 4: Chemistry Essay Swarm

**Task**: Write 2-5 paragraph chemistry/medicine entries for each of the 51 emblems.

**Setup**: Two agents split the emblems (0-25 and 26-50). Each read De Jong's corpus, the source-emblem mappings, and the dictionary data.

**Result**: 103K chars, 157 paragraphs. The largest single content production of the session.

---

## Performance Assessment

### What Research Agents Are Best At

1. **Focused corpus reading**: An agent assigned to read Wescott's 608-line article for modal analysis will find details that a main session skimming thousands of lines would miss. The focused attention is the key advantage.

2. **Parallel research**: Four agents reading four different corpus files simultaneously cuts research time by ~4x. The corpus reading (not the writing) is the bottleneck.

3. **Structured output**: Agents produce clean JSON when given an exact schema. The structured format makes validation and merge straightforward.

4. **Volume content generation**: 94 dictionary entries in ~10 minutes, 51 chemistry entries in ~15 minutes. The main session couldn't have written this volume at the same quality.

### What Research Agents Are NOT Good At

1. **Editorial voice**: The main session knows the user's stylistic preferences (e.g., "don't be credulous about Szulakowska's theurgy theory"). Agents follow the WRITING_TEMPLATES voice rules but can't calibrate to conversational feedback.

2. **Cross-batch coordination**: Agents can't see each other's output. If Agent A discovers something relevant to Agent B's topic, there's no communication channel.

3. **DB interaction**: This remains the hard constraint. Any task requiring SQL queries must be handled by the main session.

4. **Schema consistency**: Each agent interprets instructions slightly differently. Normalization is always needed.

---

## Metrics

| Metric | Value |
|--------|-------|
| Total research agents launched | 15 |
| Successful | 14 (93%) |
| Failed (Bash blocked) | 0 (since learning staging pattern) |
| Pending (creatures) | 1 |
| Total content produced | ~350K chars |
| Average agent duration | ~8 minutes |
| Corpus files read per agent | 2-6 |
| Main session time saved (estimated) | 3-4 hours |

---

## Lessons

1. **Pre-export DB data** — eliminates the Bash constraint entirely
2. **Split by corpus file, not by output type** — each agent reads different material, maximizing parallel value
3. **Give exact JSON schema** — reduces merge friction
4. **Plan for normalization** — agents will always drift on schema
5. **Agents find things humans miss** — their focused, systematic reading surfaces details that skimming overlooks
6. **The sweet spot is 4-6 agents** — fewer underutilizes parallelism, more creates coordination overhead
7. **Research agents + main session editorial control** = the best workflow. Agents research; the main session curates, normalizes, and publishes.
