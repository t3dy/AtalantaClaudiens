# Do We Really Need a RAG?

**Project**: AtalantaClaudiens — Digital humanities site for De Jong's scholarship on Maier's *Atalanta Fugiens*
**Date**: 2026-03-21
**Verdict**: No. Not now, and probably not ever for this project.

---

## 1. The Corpus Fits in Context

| Source | Lines | Est. Tokens |
|--------|------:|------------:|
| De Jong (1969) monograph | 11,729 | ~152K |
| Tilton (2003) monograph | 13,881 | ~180K |
| Craven (1910) biography | 6,483 | ~84K |
| Kuntz, Golden Rosicrucians | 6,766 | ~88K |
| De Jong (1964) article | 1,024 | ~13K |
| Wescott article | 608 | ~8K |
| 7 shorter articles/reviews | ~900 | ~12K |
| **Total corpus** | **42,086** | **~547K** |

Claude's 1M-token context window can hold the **entire corpus** with ~450K tokens to spare for instructions, schema, and output. Even the 200K context window holds the two primary sources (De Jong + Tilton = ~332K) comfortably.

**RAG solves the problem of corpora too large for a single context window.** Our corpus is small enough to read whole.

---

## 2. What Our Pipeline Already Does

The current architecture is **deterministic extraction → SQLite → static HTML**:

```
OCR markdown → regex parsing → SQLite → Python templates → static site
```

This pipeline has already achieved:
- **50/50** emblem mottos extracted
- **45/50** discourse summaries
- **50/50** analysis blocks assembled
- **64** scholarly references
- **134** source-authority links
- **15/15** source descriptions
- **23/23** dictionary terms with Latin

The extraction scripts (`extract_dejong.py`, `extract_dejong_pass2.py`) use regex patterns tuned to OCR garbling. This is the right tool for structured, repetitive extraction from a known text. RAG would not improve this — it would make it worse by introducing non-determinism.

---

## 3. Where LLM Assistance Is Actually Needed

There are exactly **three** places where an LLM adds value to this project. None require RAG:

### 3a. Semantic Enrichment (one-time batch)

Filling gaps that regex can't extract: multi-register readings, thematic connections between emblems, identifying alchemical processes from discourse text. This is a **one-time batch operation** where you feed each emblem's extracted data to an LLM and ask for structured output.

**What this looks like**: A script that iterates over 50 emblems, constructs a prompt from DB fields, calls Claude, validates output, writes to staging table. No retrieval needed — the per-emblem context is small (~2K tokens of motto + discourse + sources).

### 3b. Secondary Source Extraction (one-time batch)

Parsing Tilton (13,881 lines), Craven (6,483 lines), and smaller sources for emblem-specific commentary. These are **sequential reads** of known files, not retrieval from an unknown corpus.

**What this looks like**: Feed Tilton's full text (180K tokens) into context with instructions like "For each of the 50 emblems, extract any commentary Tilton makes." This is a single-pass extraction, not retrieval.

### 3c. Image Analysis (one-time batch)

Using Claude's vision to describe emblem plates, then comparing LLM descriptions to De Jong's scholarly descriptions. Again, a **batch operation** — 50 images, each analyzed independently.

**What this looks like**: For each emblem image, send to Claude Vision with "Describe the visual elements of this alchemical emblem." Compare output to `image_description` field in DB.

---

## 4. Why RAG Would Hurt

### 4a. Chunking Destroys Scholarly Context

RAG requires chunking documents into ~500-token fragments. De Jong's emblem analyses span 4-10 pages each, with cross-references to other emblems, footnotes, and multi-paragraph arguments. Chunking would sever:
- The connection between a source identification and its evidence
- Cross-emblem thematic threads (e.g., the washing motif across VI, XI, XIII)
- Footnote citations that anchor claims to specific texts

### 4b. Retrieval Introduces Noise

With 15 source authorities and 50 emblems, a vector search for "Turba Philosophorum" would return chunks from dozens of emblems where De Jong mentions it. The correct approach is a **SQL JOIN** — `emblem_sources WHERE authority_id = 'AUTH_TURBA'` — which is exact, fast, and already implemented.

### 4c. We Already Have Structured Retrieval

The SQLite database IS our retrieval layer. It's better than vector search because:
- **Exact**: `SELECT * FROM scholarly_refs WHERE emblem_id = 5` returns precisely the right data
- **Relational**: joins across emblems, sources, scholars, dictionary terms
- **Provenance-tracked**: every datum has `source_method`, `confidence`, `review_status`
- **Deterministic**: same query, same results, every time

### 4d. Embedding Quality on OCR Text

Our corpus is OCR-converted with garbled spacing, run-together words, and artifacts. Vector embeddings of "thephilosophers" and "the philosophers" would produce different vectors. The regex pipeline handles this with explicit cleanup patterns. RAG would need a separate text-cleaning pass before embedding — additional complexity for no gain.

---

## 5. What About Furnace & Fugue?

The Furnace and Fugue digital edition (UVA Press, 2020) is published under **CC BY-NC-ND**. This means:
- We **cannot** ingest their essays into our database (no derivatives)
- We **cannot** reproduce their content on our site
- We **can** reference it as a scholarly source and link to it
- We **can** read it ourselves to inform our own original writing

Even if we could ingest F&F, it would add ~50 essays (one per emblem) of ~2K tokens each = ~100K tokens. Still fits in context. Still no RAG needed.

**What to do**: Add F&F as a bibliography entry and reference source. Read their essays to inform our own emblem descriptions, but write original content.

---

## 6. The Image Analysis Pipeline

This is the most interesting LLM use case and does NOT need RAG:

```
emblem plate image → Claude Vision → structured description JSON
    ↓
compare with → De Jong's image_description field
    ↓
merge/validate → store in emblems.visual_elements (new column)
```

This is a **batch vision pipeline**, not a retrieval problem. Each image is analyzed independently. The reference layer (De Jong's descriptions) is already in SQLite.

---

## 7. What We Actually Need Instead of RAG

| Need | Solution | Status |
|------|----------|--------|
| Extract from De Jong | Regex + OCR cleanup | DONE (50/50) |
| Extract from Tilton | Single-pass LLM read (180K tokens in context) | TODO |
| Extract from smaller sources | Single-pass LLM read per file | TODO |
| Enrich emblem descriptions | Batch LLM pass over DB fields | TODO |
| Image analysis | Batch vision pass over 50 plates | TODO |
| Cross-reference lookup | SQL JOINs in SQLite | DONE |
| Full-text search | `grep` on 547K-token corpus | SUFFICIENT |
| User-facing Q&A | Not in scope (static site) | N/A |

---

## 8. When Would RAG Make Sense?

RAG would become relevant if:

1. **The corpus grows beyond 1M tokens** — e.g., ingesting the full Artis Auriferae compilation (hundreds of alchemical texts Maier drew from). We're at 547K. Not close.

2. **The site becomes interactive** — a chatbot that answers questions about AF in real-time, retrieving from a knowledge base. Our site is static HTML. No runtime queries.

3. **Multiple users contribute content** — a wiki-style platform where retrieval helps surface relevant prior contributions. We have one author (the pipeline).

None of these apply now or are planned.

---

## 9. Verdict

**No RAG.** The corpus is small, the extraction is deterministic, the retrieval is relational, and the LLM tasks are batch operations on known files. Adding RAG would introduce:
- Vector database dependency (Chroma, Pinecone, etc.)
- Chunking logic that destroys scholarly context
- Embedding pipeline for OCR-garbled text
- Non-deterministic retrieval replacing exact SQL queries
- Runtime infrastructure for a static site

The right architecture is exactly what we have: **SQLite + Python scripts + batch LLM passes when needed**. The only additions needed are:
1. A Tilton extraction script (single-pass, ~180K tokens)
2. An image analysis script (batch vision, 50 images)
3. Richer emblem descriptions via LLM enrichment (batch, 50 prompts)

All three are scripts in `scripts/`, writing to SQLite, generating static HTML. No retrieval infrastructure required.

---

## 10. Pedagogical Dimensions Audit

| Dimension | Current Coverage | RAG Needed? |
|-----------|-----------------|-------------|
| Emblem mottos (Latin/English) | 50/50 | No — deterministic extraction |
| Discourse summaries | 45/50 | No — regex + OCR cleanup |
| Source text identification | 134 links | No — SQL JOINs |
| Scholarly commentary | 64 refs | No — per-emblem extraction |
| Alchemical process mapping | 50/50 analysis blocks | No — template assembly |
| Dictionary terms + Latin | 23/23 | No — seed data |
| Timeline context | 20/20 events | No — seed data |
| Visual element descriptions | 0/50 (TODO) | No — batch vision |
| Multi-register readings | Partial (in analysis) | No — batch LLM enrichment |
| Cross-emblem thematic links | Partial (in sources) | No — SQL graph queries |
| Secondary source integration | 1/10 sources extracted | No — single-pass LLM reads |
| Interactive Q&A | N/A (static site) | Would need RAG, but not in scope |
