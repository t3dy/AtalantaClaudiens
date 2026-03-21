# Hard OCR Cases: Deckard Boundary Analysis

Three emblems (XI, XXXVIII, XLVIII) remain without extracted discourse summaries despite achieving 50/50 mottos and 47/50 discourses. This document analyzes why deterministic regex extraction fails on these cases and recommends a boundary-crossing strategy.

---

## 1. OCR Pipeline Overview

**Source:** H.M.E. De Jong, *Michael Maier's Atalanta Fugiens: Sources of an Alchemical Book of Emblems* (1969), reprinted 2002 by Nicolas-Hays.

**Digitization chain:** Physical book -> PDF scan -> OCR -> Markdown conversion. The OCR markdown is 11,729 lines and 823,134 characters.

**Quality profile:**
- Pages 50-200 (Emblems I-XXXV): Generally good OCR. Section headers like `SUMMARY OF THEDISCOURSE` are consistently recognizable, even if "THE" runs into "DISCOURSE" without a space. Common garbling is limited to run-together words and missing spaces.
- Pages 200-310 (Emblems XXXVI-L): Noticeably worse. EMBLEM headers start showing character substitution (`EMBLEMXXXT/'III` for XXXVIII, `Efl/IBLEMXLVIII` for XLVIII), figure references get garbled (`fl . 8MOTTO( g3)` for `(fig. 38) MOTTO`), and SUMMARY headers occasionally mutate (`SUMIVIARY` for SUMMARY at Emblem XLIII).
- Running page headers (e.g., `290EMBLEMXLVIII`, `252EMBLEMXXKVIII`) are frequent throughout and must be distinguished from actual section starts.

**Common artifacts:**
- Run-together words: `thetree` for `the tree`, `THEDISCOURSE` for `THE DISCOURSE`
- Character substitution: `/'` for `X`, `fl/` for `EMB`, `K` for `X`
- Digit-for-Roman: `E11!` for `EMBLEM XI` (Arabic `11` instead of Roman `XI`)
- Line-break hyphenation: `some- thing` split across lines
- Footnote intrusion: page numbers and footnote references mixed into running text

---

## 2. Extraction Architecture (Deckard Boundary Map)

### DETERMINISTIC (regex-based, working well)

| Component | Pattern | Status |
|-----------|---------|--------|
| Emblem section detection | `EMBLEM\s*([IVXLCDM]+)` with MOTTO lookahead (500-800 chars) | Finds 48/50 |
| Recovery pass | `(fi[eg]\.?\s*(\d+))\s*M\s*O\s*T\s*T\s*O` for garbled EMBLEM headers | Catches 2 more (XLVIII, plus others) |
| Section markers | `E\s*P\s*I\s*G\s*R\s*A\s*M`, `SUMMARY\|SU.{0,8}ARY`, `SOURCE\s+OF`, `COM\s*M?\s*ENTARY` | Tolerant of most OCR noise |
| OCR cleanup | `clean_ocr()` fixes lowercase-uppercase joins, missing spaces, hyphenated breaks | Effective for body text |
| Page-range derivation | `derive_page_ranges()` maps emblem text positions to `## Page N` markers | Dynamic, not hardcoded |
| Position-aware dedup | Filters intro references (pos < 20000) vs. analysis section (pos > 20000) | Eliminates false matches from De Jong's introduction |
| Pass 2 interpolation | For emblems not found by regex, computes approximate page range from neighbors | Fills gaps with MEDIUM confidence |

### PROBABILISTIC (would require LLM)

| Task | Why regex cannot solve it |
|------|--------------------------|
| Identify emblem content when ALL structural markers are garbled | No anchor text to match against |
| Understand discourse meaning despite word-level OCR errors | Requires semantic comprehension, not pattern matching |
| Detect thematic boundaries when section headers are missing | Requires understanding that a new topic has begun |
| Disambiguate overlapping emblem content in very long sections | Requires understanding which emblem is being discussed |

---

## 3. The Three Hard Cases

### Emblem XI (Whitening of Latona)

**What the OCR looks like (lines 3475-3477):**
```
EMBLEMXII I3
E11! BLEMXI
(fig. II) MOTTOMakeLatonawhite andtearupthe books.
```

**What works:** The MOTTO content is successfully extracted. The `SUMMARY OF THEDISCOURSE` header appears cleanly at line 3485. The discourse text itself is well-preserved and runs for several paragraphs.

**Why it fails:** The EMBLEM header is garbled as `E11! BLEMXI` -- OCR produced Arabic digits `11` and an exclamation mark instead of the word `EMBLEM`. The main regex `EMBLEM\s*([IVXLCDM]+)` cannot match because the word `EMBLEM` itself is broken. The recovery pattern `(fi[eg]\.?\s*(\d+))` cannot match either, because the figure reference is `(fig. II)` with Roman numeral `II` rather than Arabic `11`. The recovery regex expects Arabic digits in the parenthetical.

**Root cause:** Two independent OCR errors conspire: the EMBLEM header uses digits where it should have letters, and the fig reference uses Roman where the recovery pattern expects Arabic. If either one were correct, extraction would succeed. Pass 2 does find this emblem by page-range interpolation, but the page range it computes is apparently too narrow or misaligned, so the SUMMARY marker falls outside the extracted chunk.

**Specific fix available:** Broaden the fig-reference recovery to accept Roman numerals: `(fi[eg]\.?\s*([IVXLCDM\d]+))`. This would match `(fig. II)` and recover the section. Alternatively, the pass 2 page range for Emblem XI could be widened.

---

### Emblem XXXVIII (Rebis / Two-natured Hermaphrodite)

**What the OCR looks like (lines 7516-7517):**
```
EMBLEMXXXT/'III
fl . 8MOTTO( g3)
```

**The correct reading would be:**
```
EMBLEM XXXVIII
(fig. 38) MOTTO
```

**What works:** The EPIGRAM at line 7528, SUMMARY OF THEDISCOURSE at line 7535, and the discourse body text are all cleanly preserved. The scholarly content is extensive and well-formed.

**Why it fails:** The main regex matches `EMBLEMXXXT` and reads the Roman numeral as `XXX` (30), because `T`, `'`, `/` are not valid Roman numeral characters. This means the match is assigned to Emblem XXX, not XXXVIII. The figure reference `fl . 8MOTTO( g3)` is so severely garbled that the recovery pattern `(fi[eg]\.?\s*(\d+))` cannot match -- the `fi` prefix has become `fl`, the `g.` has become `g3)`, and the number `38` has been split and scrambled into `8` and `3`. There is no `(fig. 38)` or `(fie. 38)` anywhere in the file.

**Root cause:** Both the EMBLEM header and the fig reference are damaged beyond the tolerance of any reasonable regex. The Roman numeral `XXXVIII` has become `XXXT/'III` (the `V` became `T/`), and the figure reference is completely unrecognizable. Pass 2 can locate the approximate page range but the section boundaries computed by interpolation may not capture the full SUMMARY section.

**No simple regex fix exists.** The garbling is character-level and unique to this section.

---

### Emblem XLVIII (King Drinking from the Fountain)

**What the OCR looks like (lines 8579-8580):**
```
Efl/IBLEMXLVIII1
(fig. 48) MOTTO
```

**What works:** The `(fig. 48) MOTTO` recovery pattern successfully matches at line 8580, so the emblem IS found. The SUMMARY OF THEDISCOURSE header appears cleanly at line 8588. The motto and epigram are extracted.

**Why it fails (only 2/5 fields in pass 1):** Emblem XLVIII is De Jong's longest analysis section, spanning approximately pages 289-310 (roughly 20 pages, compared to the typical 4-8). The script uses a section text window of `motto_start + 8000` chars or `next_start + 2000` chars, whichever is larger. For most emblems this is generous, but XLVIII's discourse summary, source of motto, and commentary are spread across thousands of characters of dense scholarly apparatus including extensive Latin quotations, footnotes, and cross-references. The extraction window likely captures the early part of the section (motto + epigram) but the section boundary truncates before the SUMMARY marker can be reached, OR the SUMMARY is found but the SOURCE and COMMENTARY markers fall outside the window.

Additionally, XLVIII is the second-to-last emblem, so the `next_start` value (for Emblem XLIX) defines the boundary. If Emblem XLIX's position is correctly identified, the boundary should be adequate -- but the running headers (`290EMBLEMXLVIII`, `292EMBLEMXLVIII`, `293EMBLEMXLVIII`, etc.) that appear on nearly every page of this long section may be interfering with section-boundary detection, since they contain valid `EMBLEM + XLVIII` patterns that could confuse the deduplication logic.

**Root cause:** The combination of exceptional section length (~20 pages) and dense running headers creates ambiguity. The dedup logic picks one candidate position for XLVIII, but the full scholarly content extends far beyond the extraction window. The running headers at lines 8596, 8624, 8657, 8692, 8729, 8762, 8833, 8930, 8962, 8996, 9025 (11 separate running headers) all match `EMBLEM\s*XLVIII` and could interfere with section boundary logic.

**Potential fix:** Special-case the extraction window for XLVIII to be much larger (e.g., 25000 chars instead of 8000), or use the known page range (289-310) to define the chunk boundary directly. However, this risks false matches from the many running headers within the section.

---

## 4. Methods Attempted

| Method | What it caught | Session |
|--------|----------------|---------|
| Main regex: `EMBLEM\s*([IVXLCDM]+)` with MOTTO lookahead | 44 emblems initially, 48 after dedup fix | Session 1 |
| Recovery: `(fi[eg]\.?\s*(\d+))\s*MOTTO` for garbled EMBLEM headers | Caught XXXVI, XLV, XLVIII, XLIX | Session 2 |
| OCR-tolerant SUMMARY: `SU.{0,8}ARY` | Caught XXXIX, XLI (garbled as `SUl\'IMA.RYOF` and `SUMIVIARY`) | Session 2 |
| Position-aware dedup | Filtered false matches from intro section (positions < 20000) | Session 2 |
| Page-range interpolation (pass 2) | Filled 6 more emblems via `derive_page_ranges()` | Session 2 |
| Period-tolerant fig pattern: `fi[eg]\.?\s*` | Caught Emblem II header variant | Session 2 |
| Emblem XVII manual entry in seed data | Motto garbled as `M GT1[] 0`, unrecoverable | Session 2 |

**Current state:** 50/50 mottos, 47/50 discourse summaries. The three remaining cases are XI, XXXVIII, and XLVIII.

---

## 5. Boundary Recommendation

The deterministic approach has reached its practical limit for these three cases. Each one fails for a different reason:

- **XI:** Both header and fig reference are garbled in complementary ways (a fix for either would solve it, but a general regex cannot anticipate both failure modes simultaneously)
- **XXXVIII:** Both anchors are damaged beyond regex tolerance; no reasonable pattern can match `fl . 8MOTTO( g3)` as `(fig. 38) MOTTO`
- **XLVIII:** Found but too long for the fixed extraction window; running headers create boundary confusion

**Recommended approach:** A one-time LLM-assisted pass:

1. For each of the 3 missing emblems, read the known page range from the markdown (~3000-5000 chars per emblem, ~8000 for XLVIII)
2. Prompt Claude to extract the discourse summary from the garbled text, providing the surrounding motto and epigram as context anchors
3. Validate output: must be 50-500 words, must not duplicate an existing discourse summary, must relate to the emblem's known motto
4. Store with `source_method='LLM_ASSISTED'`, `confidence='MEDIUM'`, `review_status='DRAFT'`

**This is NOT RAG.** It is a batch operation on 3 known, bounded text chunks where the source location is already identified. The LLM is being used as a robust text parser, not as a knowledge source.

**Cost estimate:** ~15K tokens input (3 chunks plus prompts) + ~3K tokens output = approximately $0.05-0.10 total. Trivial.

**Implementation:** A new script `scripts/extract_dejong_llm.py` that:
- Queries the database for emblems with `motto_english IS NOT NULL AND discourse_summary IS NULL`
- Reads the page range from `derive_page_ranges()`
- Sends each chunk to Claude with extraction instructions
- Validates and stores results with LLM provenance markers

---

## 6. Why Not Just Fix the Regex?

Each remaining case has **unique, non-repeating garbling** that would require case-specific patterns:

| Emblem | Would require | Risk |
|--------|--------------|------|
| XI | Roman-numeral fig recovery: `(fig\.\s*[IVXLCDM]+)` | Could false-match fig references to unrelated Roman numerals throughout the text |
| XXXVIII | Character-level reconstruction of `fl . 8MOTTO( g3)` | Pattern so specific it would only ever match this one instance -- a hardcoded fix disguised as regex |
| XLVIII | 25000-char extraction window + running-header suppression | Increases memory usage and processing time for all 50 emblems to handle one edge case |

Adding 3 more case-specific regex patterns increases maintenance burden, adds false-positive risk, and makes the extraction logic harder to reason about -- all to handle less than 1% of the data. The LLM approach is the correct tool for the tail of the distribution.

---

## 7. Provenance Implications

Per the project's provenance model (see `docs/SYSTEM.md`):

| Field | Regex-extracted | LLM-assisted |
|-------|----------------|--------------|
| `source_method` | `CORPUS_EXTRACTION` | `LLM_ASSISTED` |
| `confidence` | `HIGH` | `MEDIUM` |
| `review_status` | `VERIFIED` (after manual check) | `DRAFT` (until reviewed) |

LLM-extracted discourse summaries will be clearly marked in the database and on the website with appropriate badges, consistent with the project's AI disclosure policy. The 47 regex-extracted discourses retain `HIGH` confidence; the 3 LLM-assisted ones carry `MEDIUM` until manual review promotes them.
