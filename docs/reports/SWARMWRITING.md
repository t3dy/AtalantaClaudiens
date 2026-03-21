# SWARMWRITING.md — Agent Swarm for AtalantaClaudiens Content Generation

## Purpose

This document specifies an agent swarm architecture for batch-generating scholarly content across five parallel workstreams. The swarm populates the AtalantaClaudiens website with scholar profiles, bibliography annotations, timeline events, dictionary terms, and a Maier biography — all derived from the source corpus at `atalanta fugiens/`.

---

## 1. The Swarm Architecture

Five agents run in parallel, each producing a self-contained JSON staging file:

| Agent | Output File | Content | Estimated Items |
|-------|-------------|---------|-----------------|
| SCHOLAR | `staging/scholars.json` | 11 scholar profiles (bio, contribution summary, emblem coverage) | 11 profiles |
| BIBLIOGRAPHY | `staging/bibliography.json` | Annotated bibliography entries (relevance, scope, key arguments) | 10 annotations |
| TIMELINE | `staging/timeline.json` | Historical events from Maier's life through modern reception | 10+ new events |
| DICTIONARY | `staging/dictionary.json` | Alchemical/emblematic terms with definitions and emblem cross-refs | 15+ new terms |
| BIOGRAPHY | `staging/biography.json` | Michael Maier's life: chronology, positions, publications, legacy | 1 structured document |

After all five agents complete, a MERGE phase integrates their output into `atalanta_fugiens_seed.json` and triggers the pipeline rebuild (`init_db` through `build_site`).

### Why Parallel Works

Each agent writes to a different staging file. All agents read from the same corpus directory (`atalanta fugiens/`), which is read-only. There are no shared mutable resources. No file conflicts are possible because:

- Agent outputs are separate files in `staging/`.
- The source `.md` files are never modified.
- The database is not touched until the merge phase.
- Each agent's JSON artifact is self-contained — no cross-agent dependencies.

The merge phase is the only sequential step. It reads all five staging files, validates them, and feeds them into the seed JSON.

---

## 2. How Agents Consult the PDFs

The source PDFs have been converted to markdown (`.md` files) via OCR. The corpus lives at `atalanta fugiens/` and includes:

| Source | Lines | Role |
|--------|-------|------|
| De Jong (1969) | 11,729 | Primary scholarly source — fully extracted |
| Tilton (2003) | 13,881 | Major secondary — not yet extracted |
| Craven (1910) | 6,483 | Biographical primary — not yet extracted |
| 10 articles/reviews | ~3,000 total | Supplementary scholarship |

### The Reading Pipeline

Agents access corpus content through a three-step process:

1. **Grep search.** The agent uses targeted keyword searches to locate relevant passages. For example, searching for `Emblem XXVIII` in Tilton, or `Rosicrucian` in Craven, or `coniunctio` across all files. This narrows thousands of lines to the specific sections that matter.

2. **Targeted file reading.** Once Grep identifies the location (file and line range), the agent reads that section into context using the Read tool. This loads the actual OCR markdown — complete with its artifacts, Latin passages, and scholarly apparatus.

3. **LLM synthesis.** The LLM reads the loaded passage and produces structured output: a scholar biography, a term definition, a timeline event. The LLM is the reading comprehension engine. It handles OCR noise, interprets scholarly arguments, and synthesizes multi-paragraph source material into concise structured entries.

This is **scripted search + targeted LLM reading**:

```
Grep finds WHERE → Read loads WHAT → LLM synthesizes HOW → Output is structured JSON
```

There are no API calls to external services. No embeddings. No vector databases. No retrieval-augmented generation. The LLM reads the source files directly, the same way a human researcher would open a book to a specific page.

### Context Window Capacity

Each source file fits comfortably in a single context window:

- Tilton (~13,881 lines) is roughly 180K tokens — well within a 1M-token context.
- De Jong (~11,729 lines) is roughly 150K tokens.
- All remaining sources combined are under 50K tokens.
- The entire corpus is approximately 547K tokens total.

No chunking is needed. An agent can load an entire source file if a passage spans multiple sections.

---

## 3. Why Not RAG

The entire corpus is 547K tokens. The model context window is 1M tokens. The corpus fits in context with room to spare.

RAG (Retrieval-Augmented Generation) would introduce:

- **An embedding pipeline** to vectorize the corpus and store it in a vector database.
- **A retrieval step** to query the vector store and return ranked passages.
- **Infrastructure dependencies** — a vector DB (Chroma, FAISS, Pinecone), an embedding model, a query pipeline.
- **Retrieval errors** — vector similarity search can miss passages that keyword search finds trivially (e.g., a specific emblem number, a Latin term, a scholar's name).

None of this is necessary. Grep + Read + LLM comprehension handles the entire workflow with zero infrastructure overhead. The corpus is small, highly structured (emblem numbers, section headers, scholar names), and keyword-searchable. RAG would add complexity for no gain.

This aligns with the project's architecture constraint: no runtime dependencies, no build tools, no external services.

---

## 4. Quality Control

### Structured Output

Every agent produces JSON with named fields. No free-form text blobs. Each entry follows the schema defined in `docs/ONTOLOGY.md`:

- Scholar profiles: `name`, `affiliation`, `era`, `contribution_summary`, `emblem_coverage`
- Bibliography annotations: `relevance_badge`, `scope`, `key_argument`, `emblem_coverage`
- Timeline events: `year`, `event`, `category`, `source_citation`
- Dictionary terms: `term`, `definition`, `category`, `emblem_refs`, `related_terms`
- Biography sections: `period`, `events`, `sources`

### Provenance Tracking

All agent-generated content carries mandatory provenance fields:

```json
{
  "source_method": "LLM_ASSISTED",
  "confidence": "MEDIUM",
  "review_status": "DRAFT"
}
```

- `source_method='LLM_ASSISTED'` — the content was synthesized by the LLM from corpus sources.
- `confidence='MEDIUM'` — default for all LLM-generated content. Only human review can promote to `HIGH`.
- `review_status='DRAFT'` — all swarm output starts as DRAFT. The promotion path is DRAFT -> REVIEWED -> VERIFIED.

Content that was deterministically extracted (regex-parsed mottos, emblem numbers) retains `source_method='DETERMINISTIC'` and `confidence='HIGH'`. The swarm never overwrites these.

### Merge-Phase Validation

The merge step validates before integrating:

1. **JSON syntax** — every staging file must parse without errors.
2. **Field completeness** — required fields must be present and non-empty.
3. **No duplicates** — no duplicate scholar names, term names, or timeline events.
4. **Schema conformance** — entries must match the expected structure from `docs/ONTOLOGY.md`.
5. **Cross-reference integrity** — emblem numbers referenced by terms or events must exist (0-50).

### AI Disclosure

The website's AI disclosure banner (defined in `build_site.py`) appears on all pages containing generated content. Each generated section shows a review badge indicating its status: DRAFT (amber), REVIEWED (blue), or VERIFIED (green). This is a project-wide architectural constraint, not a swarm-specific feature.

### Human Review Gate

No swarm output reaches VERIFIED status automatically. The promotion path:

1. Swarm generates DRAFT content in `staging/`.
2. Merge integrates into seed JSON and rebuilds the site.
3. A human reviews the generated pages.
4. Accepted entries are promoted to REVIEWED, then VERIFIED.
5. Rejected entries are flagged for revision or removal.

---

## 5. What the Swarm Does NOT Do

- **Does NOT modify existing extracted data.** De Jong's mottos, discourse summaries, scholarly refs, and emblem-source links (currently 50/50 mottos, 34/50 discourses, 60 scholarly refs, 119 emblem-source links) are untouched. The swarm only adds new content alongside existing data.

- **Does NOT download images or scrape websites.** All source material is local `.md` files already in the repository. Image acquisition is a separate task (Phase 4A in the roadmap).

- **Does NOT create new database tables.** The schema already defines all needed tables (`scholars`, `bibliography`, `dictionary_terms`, `timeline_events`, etc.) in `docs/ONTOLOGY.md`. The swarm populates existing tables, it does not alter the schema.

- **Does NOT run at deployment time.** This is a one-time batch operation. The results are committed to the repository as structured JSON. The static site generator reads from the database, which is built from that JSON. There is no runtime agent execution.

- **Does NOT overwrite VERIFIED data.** Any entry with `review_status='VERIFIED'` is protected. If the swarm encounters a conflict with verified data, it logs a discrepancy rather than overwriting. This is an existing project-wide data integrity rule.

---

## 6. Future Swarms

After the content-generation swarm completes, three additional swarms follow the same architecture pattern (parallel agents, staging files, merge, pipeline rebuild):

### TILTON Extraction Swarm

Parse Tilton's 13,881-line markdown into `scholarly_refs` entries. Tilton covers Maier's Rosicrucian context, spiritual alchemy, and biographical details that supplement De Jong's emblem-focused analysis.

- Agent per section: Rosicrucian context, alchemical philosophy, biographical details, emblem references
- Output: `staging/tilton_refs.json`
- Estimated yield: 50+ new scholarly refs, 30+ new emblem-source links

### IMAGE Analysis Swarm

Process 50 emblem plate images through Claude Vision to populate `visual_elements` entries.

- One agent per emblem (or batched by groups of 10)
- Output: `staging/visual_elements.json`
- Each entry describes: figures, objects, architecture, landscape, symbols, positions, alchemical meanings
- Requires image acquisition first (Phase 4A)

### ESSAY Writing Swarm

Generate 5 thematic essays (~2,000 words each) synthesized from corpus material.

- One agent per essay topic (identified in `docs/INTERFACE.md`)
- Output: `staging/essays.json`
- Each essay carries `source_method='LLM_ASSISTED'`, `review_status='DRAFT'`
- All essays display the AI-generated content banner

Each future swarm follows the identical pattern:

```
Parallel agents → staging/*.json → merge validation → seed JSON update → pipeline rebuild
```

The architecture scales because the pattern is fixed. Only the agent instructions and output schemas change between swarms.
