# Deckard Boundary Analysis: Tilton Ingestion

**Subject:** Ingesting Hereward Tilton's *The Quest for the Phoenix* (2003) into AtalantaClaudiens
**Source file:** `atalanta fugiens/Hereward Tilton The Quest for the Phoenix...md` (13,881 lines)
**Current state:** De Jong (1969) extracted as primary source (50/50 mottos, 47/50 discourses, 64 scholarly refs, 134 source links). Tilton has NOT been extracted.

---

## 1. What Tilton Adds

Tilton's monograph is the most comprehensive English-language study of Michael Maier's life and intellectual world. Where De Jong provides close emblem-by-emblem analysis of alchemical sources, Tilton situates *Atalanta Fugiens* within:

- **Paracelsian vs Aristotelian framing:** Tilton argues Maier navigated between Paracelsian chemical philosophy and Aristotelian natural philosophy, rejecting a simple reduction of AF to Tria Prima (sulphur, mercury, salt). This directly challenges interpretive shortcuts.
- **Rosicrucian connections:** Maier's relationship to the Rosicrucian manifestos (*Fama Fraternitatis*, *Confessio*) and his role as intermediary rather than member.
- **Biographical context:** Chapters 1-3 provide the most detailed treatment of Maier's life available: his time at Rudolf II's court in Prague, his English sojourn, his medical practice, and his publishing career.
- **Specific emblem analyses:** Tilton discusses emblems XXIII, XXVIII, XXXIX, XLIV, and XLVIII (per De Jong's seed data cross-references), often from a philosophical rather than source-critical angle.
- **Counter-argument to reductive readings:** Tilton argues AGAINST reducing AF to a Tria Prima framework, positioning it instead within a broader philosophical and spiritual tradition.

Tilton supplements De Jong; he does not replace him. De Jong's source identifications remain canonical. Tilton adds interpretive depth, historical context, and biographical material.

---

## 2. Boundary Map

### DETERMINISTIC TASKS (use code, not LLM)

| Task | Method | Rationale |
|------|--------|-----------|
| File reading and line counting | Python `open()` / `len()` | Mechanical I/O |
| Page/chapter boundary detection | Regex (`^#+\s`, `^Chapter`, `^PART`) | Structural markers are syntactic |
| Emblem number identification | Regex (`EMBLEM\s+[IVXLCDM]+`, `Emblem\s+\d+`) | Pattern matching on known format |
| Database INSERT/UPDATE operations | Python sqlite3 | Schema-driven, no interpretation |
| Schema migration (if needed) | SQL DDL statements | Structural change, not semantic |
| HTML generation from DB fields | Jinja2 / string templates in `build_site.py` | Deterministic rendering |
| Bibliography entry creation | Hardcoded `bib_id=tilton_2003` metadata | Known publication data |

### PROBABILISTIC TASKS (LLM appropriate)

| Task | Why LLM is needed |
|------|--------------------|
| Identifying which paragraphs discuss specific emblems | Tilton does not use De Jong's `EMBLEM XX` section headers; references are embedded in running prose |
| Extracting Tilton's interpretive claims vs historical narrative | Requires semantic understanding of argument structure |
| Classifying interpretation type (PHILOSOPHICAL, ROSICRUCIAN, ALCHEMICAL) | Tilton blends registers; classification requires judgment |
| Summarizing multi-page arguments into `scholarly_refs` entries | Compression of extended scholarly argument |
| Identifying disagreements between Tilton and De Jong | Cross-source semantic comparison |
| Extracting Rosicrucian vocabulary for dictionary candidates | Domain-specific term identification in context |
| Identifying timeline events with dates | Dates appear in narrative context, not structured lists |

### VALIDATION LAYERS

1. **Emblem reference validation:** LLM-extracted emblem numbers checked against known set (0-50). Any reference outside this range is flagged and discarded.
2. **Summary length check:** `scholarly_refs.summary` text length-checked before INSERT. Reject entries exceeding 500 characters (force re-summarization).
3. **Confidence floor:** All LLM-extracted data inserted with `confidence='MEDIUM'`. No exceptions.
4. **Review status:** All LLM-extracted data inserted with `review_status='DRAFT'` until human verification.
5. **Provenance marking:** Every record carries `source_method='LLM_ASSISTED'`, `bib_id='tilton_2003'`.
6. **De Jong preservation:** Before any INSERT touching an emblem already covered by De Jong, verify no `review_status='VERIFIED'` row is overwritten. Tilton data is additive only.

### BOUNDARY VIOLATIONS TO AVOID

- **Do NOT use LLM to parse file structure.** Chapter and section boundaries are syntactic; use regex.
- **Do NOT store raw LLM output without provenance marking.** Every datum must carry `source_method`, `confidence`, and `review_status`.
- **Do NOT overwrite De Jong's data.** Tilton supplements, never replaces. De Jong rows with `review_status='VERIFIED'` are immutable.
- **Do NOT let LLM generate SQL.** LLM produces structured JSON; Python code handles all database operations.
- **Do NOT skip validation.** Every LLM-extracted emblem reference must pass the known-emblem-number check before insertion.

---

## 3. Ontology Impact

### Existing tables affected

| Table | Impact |
|-------|--------|
| `scholarly_refs` | New entries with `bib_id='tilton_2003'`. Estimated 20-40 new rows covering emblem-specific interpretations and thematic arguments. |
| `dictionary_terms` | Potential new terms from Rosicrucian vocabulary: *Fama Fraternitatis*, *Confessio*, *chymical wedding*, *Paracelsian Tria Prima* (as a concept to define and problematize). Estimated 5-15 new terms. |
| `timeline_events` | Tilton's historical framing adds events: Rudolf II's court at Prague, Rosicrucian manifesto publications (1614-1616), Maier's English sojourn (1611-1616), Maier's death (1622). Estimated 10-20 new events. |
| `scholars` | Tilton row already exists from seed data. Enrich with biography, methodology description, and contribution summary. |
| `bibliography` | `tilton_2003` entry already seeded. Verify completeness. |
| `source_authorities` | If Tilton identifies alchemical sources De Jong missed, add new rows. Likely few additions since De Jong's source coverage is thorough. |

### Potential new features

- **Biography tab for Maier on emblem pages or About page:** Tilton Chapters 1-3 provide the most detailed biographical treatment of Maier available. This is new content not derivable from De Jong. Could become a standalone page (`site/biography.html`) or a section on the About page.
- **Interpretive disagreements view:** Where Tilton explicitly disagrees with De Jong (e.g., Tria Prima framing), this could be surfaced as a "Scholarly Debate" note on affected emblem pages.

### Schema changes

No schema migration expected. The existing `scholarly_refs` table with `bib_id`, `emblem_id`, `summary`, `source_method`, `confidence`, and `review_status` fields accommodates Tilton data without modification. If a biography feature is added, that would be a separate Phase 3+ decision.

---

## 4. Implementation Plan

### Script

`scripts/extract_tilton.py`

### Method

Single-pass LLM-assisted read. At 13,881 lines (~180K tokens), the full text fits within a single context window. No chunking, no RAG pipeline, no vector store.

**Workflow:**
1. Deterministic pre-pass: regex-based chapter/section boundary detection, emblem number identification, page number extraction.
2. LLM pass: with structural boundaries established, prompt LLM to extract per-emblem interpretive claims, classify interpretation types, identify dictionary candidates and timeline events.
3. Validation: check all LLM outputs against known emblem numbers, enforce length limits, apply confidence/review_status defaults.
4. Database insertion: Python script handles all INSERT operations with full provenance.

### Pipeline position

**Stage 2b** — after De Jong extraction (`extract_dejong.py`), parallel to or after `extract_secondary.py`. Does not block Stage 3 (dictionary, timeline) but enriches it.

```
Stage 1: init_db.py + seed_from_json.py
Stage 2a: extract_dejong.py
Stage 2b: extract_tilton.py        <-- NEW
Stage 2c: extract_secondary.py
Stage 3: seed_dictionary.py + seed_timeline.py
Stage 4: build_site.py
Stage 5: validate.py
```

### Output targets

| Output | Target table | Estimated rows |
|--------|-------------|----------------|
| Emblem interpretations | `scholarly_refs` | 20-40 |
| Dictionary candidates | `dictionary_terms` | 5-15 |
| Timeline events | `timeline_events` | 10-20 |
| Source authority links | `source_authorities` | 0-5 |
| Scholar profile enrichment | `scholars` | 1 (update) |

### Provenance for all outputs

```python
source_method = 'LLM_ASSISTED'
confidence = 'MEDIUM'
review_status = 'DRAFT'
bib_id = 'tilton_2003'
```

---

## 5. Website Impact

### Enriched pages

- **Scholar page for Tilton** (`site/scholar/tilton.html`): Currently minimal. Gains full methodology description, contribution summary, and list of emblem coverage with interpretation types.
- **Emblem pages** (especially XXIII, XXVIII, XXXIX, XLIV, XLVIII): Gain a second scholarly voice in the comparative view. Tilton's philosophical/Rosicrucian framing complements De Jong's source-critical analysis.
- **Dictionary** (`site/dictionary/`): May gain Rosicrucian and Paracelsian terms that De Jong does not define.
- **Timeline** (`site/timeline.html`): Gains Rudolf II court context, Rosicrucian manifesto dates, and Maier biographical events that De Jong's source-focused work does not cover.

### Potential new pages

- **Maier biography page** (`site/biography.html`): Tilton Chapters 1-3 are the richest source for Maier's life. This could be a Phase 3+ addition, not required for Tilton extraction itself.
- **No other new pages required.** Tilton data fits into existing page templates.

### Display considerations

- Emblem pages should clearly attribute Tilton vs De Jong in the scholarly apparatus panel (RIGHT side of comparative view).
- If Tilton disagrees with De Jong on interpretation, both views are shown with attribution, not merged.
- Tilton-sourced data carries a visible `DRAFT` badge until verified.

---

## 6. What NOT to Do

1. **Do NOT attempt to extract ALL of Tilton.** Focus on AF-relevant chapters. Tilton's extended treatment of Maier's other works (*Symbola Aureae Mensae*, *Arcana Arcanissima*, etc.) is out of scope unless it directly illuminates AF emblems.
2. **Do NOT create a RAG pipeline.** The corpus fits in a single context window. A vector store adds complexity without benefit.
3. **Do NOT merge Tilton's claims with De Jong's.** Every `scholarly_refs` entry must carry its own `bib_id`. The comparative view depends on clear attribution.
4. **Do NOT add Tilton data at HIGH confidence.** Tilton is supplementary. Only De Jong's deterministically-extracted data (mottos, discourse text, source identifications) earns HIGH confidence.
5. **Do NOT let Tilton extraction block other work.** Stage 2b runs in parallel with or after existing Stage 2 scripts. It does not gate Stage 3.
6. **Do NOT auto-promote DRAFT to VERIFIED.** Human review is required for all LLM-extracted scholarly interpretations.
7. **Do NOT use Tilton to "correct" De Jong.** Where they disagree, both positions are preserved. De Jong remains the canonical anchor for emblem analysis.
