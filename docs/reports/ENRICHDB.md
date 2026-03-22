# ENRICHDB.md — Database Enrichment Needs

## Current State (post-analysis rewrite)

The emblem analysis template now assembles 5 sections from DB data:
1. Overview (motto + stage)
2. Maier's Discourse (excerpt from OCR)
3. Source Texts (De Jong's identifications, grouped by type)
4. Scholarly Commentary (ref summaries)
5. Key Alchemical Concepts (dictionary terms, grouped by category)

Average analysis: **2236 chars** (up from 1240). But the quality is limited by what's in the database.

## What Makes a Thin Description

Emblem descriptions are thin when:
- The discourse excerpt is garbled OCR ("thephilosophers", "theStone")
- Only 1 scholarly ref exists (De Jong) with no second voice
- Source links are generic (DISCOURSE_CITATION) without detail
- Dictionary terms are few or missing
- No alchemical stage classification
- No Latin motto
- No image description (what you SEE in the plate)

## Data Gaps by Category

### 1. OCR Text Quality (affects ALL 50 emblems)
The discourse summaries are raw OCR with:
- Run-together words: "thephilosophers" → "the philosophers"
- Missing spaces after punctuation: "that.This" → "that. This"
- Garbled characters: "P/z" for "Phil", "rnatter" for "matter"

**Fix**: A text-cleaning pass that applies more aggressive OCR cleanup patterns. Can be done deterministically (regex) for ~80% of issues, LLM-assisted for the rest.

### 2. Latin Mottos (49/50 missing)
Only Emblem XVII has a Latin motto (from seed data). The original Latin mottos are available in the OCR but were never extracted (the extraction focused on English translations).

**Fix**: Extract Latin mottos from the OCR. Each emblem section has "MOTTO" followed by the Latin text, then the English translation. A targeted regex pass can pull these.

### 3. Dictionary Term Links (4 emblems still unlinked)
After auto-linking via text matching: 46/50 have term connections. 4 remain unlinked — their discourse text doesn't contain recognizable term labels.

**Fix**: Manual review or LLM-assisted term identification for the 4 gaps.

### 4. Source Links (3 emblems with 0 sources)
Emblems XIII, XXXV, XLIII have no source authority connections. De Jong discusses sources for all 50 emblems, so these are extraction gaps.

**Fix**: Re-read De Jong's sections for these 3 emblems and identify which source authorities she references.

### 5. Alchemical Stage (19 unclassified)
31/50 are classified (NIGREDO/ALBEDO/CITRINITAS/RUBEDO). The remaining 19 don't map cleanly to a single stage, or need closer reading of De Jong's analysis.

**Fix**: LLM-assisted classification reading each emblem's discourse + De Jong's commentary. Some may legitimately be NULL (spanning stages or not stage-specific).

### 6. Scholarly Commentary Depth (50 refs, mostly De Jong)
64 total refs, but 50 are De Jong. Only 14 from other scholars. The analysis blocks quote De Jong but lack comparative perspectives.

**Fix**: Tilton extraction (13,881 lines) would add ~20 scholarly refs for key emblems. This is the single highest-impact enrichment.

### 7. Definition_long (38/38 empty)
Every dictionary term has a one-sentence `definition_short` but no extended definition. The analysis blocks link to thin term pages.

**Fix**: Writing swarm for 38 extended definitions (3-5 sentences each, drawing from De Jong's usage in the corpus).

### 8. Image Descriptions (28/50 from seed, rest NULL)
22 emblems have `image_description` from the original seed data. 28 are NULL. Without these, the "What You See" section can't be generated.

**Fix**: Claude Vision batch on the 51 plate images, or manual description from De Jong's plate discussions.

## Priority Ranking

| Priority | Enrichment | Impact | Effort | Method |
|----------|-----------|--------|--------|--------|
| P1 | OCR text cleanup | Readability of every page | Medium | Regex pass |
| P2 | Tilton extraction | +20 scholarly refs, second voice | High | LLM single-pass |
| P3 | Latin mottos | Bilingual display, scholarly rigor | Medium | Regex extraction |
| P4 | Definition_long | Richer dictionary pages | Medium | Writing swarm |
| P5 | Image descriptions | Visual literacy section | High | Vision or manual |
| P6 | Alchemical stages (19) | Complete stage classification | Low | LLM classification |
| P7 | Source links (3 gaps) | Complete source coverage | Low | Manual/LLM |
| P8 | Term links (4 gaps) | Complete cross-referencing | Low | Manual |

## What We DON'T Need

- **No new tables** — all data fits in existing schema
- **No RAG** — corpus fits in context
- **No re-extraction** — De Jong's data is already in the DB. We need enrichment, not re-parsing.
- **No schema migration** — except `registers` column if we want multi-register definitions
