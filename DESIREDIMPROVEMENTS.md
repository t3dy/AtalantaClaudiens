# DESIREDIMPROVEMENTS.md — Comprehensive Improvement Plan

All aspects of AtalantaClaudiens: interface, writing, pedagogy, data ontology, by website section.

---

## 1. EMBLEM PAGES (51 pages)

### Data Gaps
| Field | Filled | Gap | Fix Method |
|-------|--------|-----|------------|
| motto_english | 50/50 | 0 | Done |
| motto_latin | 1/50 | 49 | Extract from OCR or seed manually (Maier's original Latin) |
| epigram_english | 50/50 | 0 | Done |
| discourse_summary | 47/50 | 3 (XI, XXXVIII, XLVIII) | LLM-assisted pass on known page ranges |
| analysis_html | 50/50 | 0 | Done (template assembly) |
| image_description | 22/50 | 28 | Seed from De Jong's plate descriptions |
| alchemical_stage | 0/50 | 50 | Classify each emblem as NIGREDO/ALBEDO/CITRINITAS/RUBEDO |
| visual_elements | 0/50 | 50 | Claude Vision batch on plate images |
| Images (HIGH confidence) | 10/51 | 41 | Source from labeled Wikimedia/SHI |
| Term links | 22/50 have links | 28 with 0 links | Expand term-emblem mapping |
| Source links | 47/50 have links | 3 with 0 (XIII, XXXV, XLIII) | Extract from De Jong |

### Writing Improvements
- **Latin motto alongside English**: Every emblem should show the original Latin motto. Maier chose his words precisely — the bilingual display teaches the reader how alchemical Latin works.
- **Clean OCR text**: Discourse summaries still have run-together words ("thephilosophers", "theStone"). A text-cleaning pass would dramatically improve readability.
- **Visual element descriptions**: "What you see in this plate" section — allegorical figures, setting, objects, composition. Currently 28 emblems have `image_description` from seed data; expand to all 50.
- **Alchemical stage classification**: Tag each emblem as Nigredo/Albedo/Citrinitas/Rubedo. Enables thematic browsing by stage.
- **Thematic connections**: "See also" links between emblems that share motifs (e.g., the king sequence: XXVIII → XLVIII, the washing motif: III → XI → XIII).
- **Epigram display**: Currently hidden behind `<details>` — consider showing by default since epigrams are short and central to each emblem's meaning.

### Interface Improvements
- **Motto block**: Show Latin above, English below, with a thin divider.
- **"What You See" section**: Visual description before the scholarly analysis — let the reader look before reading.
- **Related Emblems sidebar**: Horizontal scroll of 3-4 related emblem thumbnails.
- **Stage badge on every page**: Color-coded NIGREDO/ALBEDO/CITRINITAS/RUBEDO indicator.
- **Full-width plate image**: Currently max-width 600px — consider a lightbox zoom for the 10 confirmed images.

---

## 2. HOME PAGE

### Current State
Stats dashboard + emblem card grid. No introductory text, no guidance.

### Desired Improvements
- **Hero section**: 2-3 sentences explaining what AF is and what this site offers. "In 1617, Michael Maier published fifty alchemical emblems combining art, text, and music. In 1969, H.M.E. De Jong showed how to read them."
- **"Start Here" button**: Points to frontispiece or a guided introduction.
- **Thematic browse modes**: Beyond sequential numbering — browse by alchemical stage, source tradition, mythological figure, process type.
- **Featured emblem**: Rotate or highlight one well-populated emblem (e.g., Emblem V with its confirmed image + full analysis).
- **Reader-facing stats**: Replace insider metrics (64 refs, 134 links) with "50 emblems explored, 15 source traditions traced, 38 alchemical terms defined."

---

## 3. DICTIONARY (38 terms)

### Data Gaps
| Field | Filled | Gap |
|-------|--------|-----|
| definition_short | 38/38 | 0 |
| definition_long | 0/38 | 38 — every term needs an expanded paragraph |
| label_latin | 38/38 | 0 |
| significance_to_af | 38/38 | 0 |
| registers (multi-register JSON) | Column doesn't exist yet | 38 — schema needs migration |
| Term-emblem links | 22 terms linked | 16 terms with 0 emblem links |

### Writing Improvements
- **definition_long**: Every term needs a 3-5 sentence expanded definition covering historical usage, alchemical meaning, and how it functions in scholarly literature. Currently all NULL.
- **Multi-register definitions**: The schema was designed for a `registers` JSON field (alchemical, medical, spiritual, cosmological). This column was never created. Add it and populate — this is De Jong's key insight about how alchemical terms operate across registers.
- **More terms**: 38 is good but AF's vocabulary is richer. Candidates: Aqua Regia, Elixir, Tinctura, Projectio, Corpus/Spiritus/Anima triad, Cauda Pavonis, Vitriol, Pelican, Phoenix, Rebis, Draco.
- **Term relationships**: The `dictionary_term_links` table supports RELATED/SEE_ALSO/OPPOSITE/PARENT/CHILD — populate with more cross-references.

### Interface Improvements
- **Introductory paragraph**: "Alchemical language is deliberately polysemous — a single term carries meaning across material, medical, spiritual, and cosmological registers simultaneously..."
- **Visual term network**: Even a simple list showing which terms cluster together.
- **Filter by category**: Tabs or buttons for PROCESS / SUBSTANCE / FIGURE / CONCEPT / MUSICAL / SOURCE_TEXT.
- **Multi-register display**: Show the 4 registers as a definition list when populated.

---

## 4. SOURCES (15 authorities)

### Current State
Rich cards with descriptions and emblem badges. This is the site's strongest section.

### Writing Improvements
- **Distinguish MOTTO_SOURCE from DISCOURSE_CITATION**: The data supports this distinction (via `relationship_type`) but the display doesn't differentiate. Show which emblems use the source for their motto vs which cite it in the discourse.
- **Key passage excerpts**: Where De Jong quotes the source text, show the quotation (within fair use limits) alongside Maier's adaptation.
- **Source text overviews**: Expand the 15 `description_long` entries to cover the historical transmission of each text (e.g., how the Turba reached Maier through the Artis Auriferae compilation).

### Interface Improvements
- **Source x Emblem matrix**: A 50×15 grid showing which sources appear in which emblems. This single visualization IS De Jong's argument.
- **Individual source pages**: Currently all sources are on one page. Each deserves its own page with full description, all linked emblems with previews, and related dictionary terms.
- **Anchor stability**: Source cards have `id="{authority_id}"` for cross-linking. Verify all cross-links from emblem analysis blocks resolve correctly.

---

## 5. SCHOLARS (11 profiles)

### Current State
All 11 have overviews now. Individual pages show specialization + works.

### Writing Improvements
- **De Jong's page**: Should be the richest on the site. Add: biographical context (her dissertation at Utrecht), her method explained with a worked example, her key arguments, how she differs from prior scholarship.
- **Scholarly conversation**: How do these 11 scholars relate? Who responds to whom? Add a "Responses" or "Conversation" section showing intellectual lineage.
- **Emblem coverage map**: For each scholar, show which emblems they discuss. De Jong covers all 50; Tilton focuses on ~5; Pagel on ~5.

### Interface Improvements
- **Scholar cards on index**: Add the overview text as a preview on the card (currently only shows specialization).
- **Link to emblem pages**: Where a scholar has a scholarly_ref for an emblem, the scholar page should link to that emblem.

---

## 6. TIMELINE (29 events)

### Current State
29 events with rich descriptions, sticky year headers, type badges.

### Writing Improvements
- **More events**: Fill gaps in Maier's publication history (Arcana Arcanissima, Lusus Serius, Silentium Post Clamores, etc.) and the Rosicrucian debate context.
- **Era narrative text**: Between era groups, add a brief paragraph explaining the significance of that period. E.g., "1614-1617: The Rosicrucian Moment" paragraph.
- **Links to scholars/bibliography**: Timeline events about scholarship (1969, 2003, 2020) should link to the relevant scholar page and bibliography entry.

### Interface Improvements
- **Era groupings with headers**: "Maier's Lifetime (1568-1622)", "Early Editions (1687-1708)", "Modern Scholarship (1910-present)", "Digital Era (2003-present)".
- **Filter by event type**: Let readers show/hide BIOGRAPHY, PUBLICATION, SCHOLARSHIP, etc.
- **Visual timeline**: Consider a horizontal timeline visualization with periods marked.

---

## 7. BIBLIOGRAPHY (10 entries)

### Current State
All 10 annotated with scholarly descriptions.

### Writing Improvements
- **More entries**: The corpus has 13+ .md source files; only 10 are in the bibliography. Add Kuntz (Golden Rosicrucians), Basilius Valentinus (Golden Tripod), the De Jong 1965 review.
- **Availability notes**: Mark which sources are freely available (Craven is public domain on archive.org, De Jong reprinted by Nicolas-Hays) vs paywalled.
- **Key argument summaries**: Beyond the annotation, what is each scholar's central claim about AF?

### Interface Improvements
- **Link to scholar pages**: Each bibliography entry should link to its author's scholar profile.
- **Sort options**: By year (current), by relevance, by author.
- **Citation format**: Add a "copy citation" button with formatted citation (Chicago, MLA).

---

## 8. BIOGRAPHY (new page, 6 sections)

### Current State
Newly created with 6 sections covering Maier's life.

### Writing Improvements
- **More biographical detail**: Expand Early Life with Maier's education at multiple universities, his interest in medicine and alchemy. Add detail about his extensive publication record (~20 works).
- **Images**: If public domain portraits of Maier exist, add them.
- **Connection to AF**: The Atalanta Fugiens section should cross-reference specific emblems as examples.
- **Navigation link**: Add to the nav bar (currently under "About" which is not discoverable).

### Interface Improvements
- **Table of contents**: Sticky sidebar with section links for the biography page.
- **Timeline integration**: Link biography sections to relevant timeline events.

---

## 9. ESSAYS (0/5 written)

### Current State
Placeholder index with 5 planned titles, no content.

### Planned Essays
1. **"Playful Reading in Atalanta Fugiens"** — How the multimedia format (image + text + music) creates a participatory reading experience.
2. **"De Jong's Source-Critical Method"** — Explained with worked examples. The methodological essay.
3. **"Alchemical Processes in the Emblems"** — How Nigredo → Albedo → Rubedo maps across the 50 emblems.
4. **"The Musical Dimension"** — The three-voice fugues as alchemical allegory (Atalanta = volatile, Hippomenes = fixed, Apple = catalyst).
5. **"The Rosicrucian Context"** — AF in the context of the Rosicrucian manifestos and Maier's intellectual milieu.

### Writing Requirements
- 1500-3000 words each
- AI-drafted with prominent disclosure banner
- Cross-linked to emblem pages, dictionary terms, source authorities
- Present tense for analysis, past tense for history
- De Jong as canonical anchor, supplemented by Tilton/Bilak/Nummedal

---

## 10. ABOUT PAGE

### Writing Improvements
- **"How to Use This Site" guide**: A brief orientation for newcomers.
- **Project purpose statement**: Why this project exists, what it contributes to DH and AF scholarship.
- **Methodology section**: How data flows from OCR → regex → SQLite → static HTML. The pipeline IS a pedagogical statement.
- **Acknowledgments**: De Jong, Tilton, SHI for images, the broader DH community.
- **Link to GitHub**: Already present, but add a "How to contribute" note.

---

## 11. CROSS-CUTTING IMPROVEMENTS

### Data Ontology
- **registers JSON column**: Add to dictionary_terms for multi-register definitions.
- **visual_elements column**: Add to emblems for structured image descriptions (JSON: figures, objects, setting, composition).
- **motto_latin population**: 49/50 emblems lack Latin mottos — these are available in the OCR.
- **alchemical_stage classification**: 50/50 empty — classify all emblems.
- **Expand term-emblem links**: 28 emblems have no dictionary term connections.
- **Frontispiece enrichment**: Emblem 0 has no motto, no discourse, no analysis. It's the interpretive key to the entire work per De Jong.

### Pedagogical Method
- **Progressive disclosure**: Newcomers get "What You See" → experts get De Jong's source analysis.
- **Multiple entry points**: Gallery, dictionary, sources, timeline, biography all lead inward.
- **Guided pathways**: "Start Here" → Frontispiece → Emblem I → "How to Read" essay.
- **Comparison tools**: Side-by-side emblem comparison for tracing thematic threads.
- **Source x Emblem matrix**: The single most powerful pedagogical visualization possible.

### Interface Design
- **Mobile responsiveness**: Test and fix dictionary cards, source badges, timeline on mobile.
- **Search**: Add a simple client-side search (JavaScript, searching data.json + term names).
- **Breadcrumb navigation**: "Home > Emblems > Emblem V > Sources > Turba Philosophorum"
- **Print stylesheet**: Scholars may want to print emblem pages for reference.

---

## 12. PRIORITY RANKING

| Priority | Task | Impact | Effort | Dependencies |
|----------|------|--------|--------|-------------|
| P1 | Home page intro + "Start Here" | First impression | Low | None |
| P2 | Clean OCR discourse text | Readability of 47 pages | Medium | None |
| P3 | Latin mottos for all 50 | Bilingual display | Medium | OCR extraction |
| P4 | 3 remaining discourses (XI, XXXVIII, XLVIII) | Completeness | Low | LLM pass |
| P5 | Alchemical stage classification | Thematic browsing | Low | Manual/LLM |
| P6 | Dictionary definition_long | Content depth | Medium | Writing swarm |
| P7 | Essay: "How to Read an Alchemical Emblem" | Core pedagogy | High | Writing |
| P8 | Frontispiece enrichment | Gateway emblem | Medium | Writing |
| P9 | Source x Emblem matrix | Visualization | Medium | JS + data |
| P10 | Tilton extraction | Secondary voice | High | LLM pass |
| P11 | Visual element descriptions | Image literacy | High | Vision API |
| P12 | Remaining 41 emblem images | Visual completeness | High | Sourcing |
| P13 | Individual source pages | Deep exploration | Medium | build_site.py |
| P14 | Expand dictionary to 60+ terms | Vocabulary coverage | Medium | Writing swarm |
| P15 | 5 essays | Pedagogical backbone | Very High | Writing |
| P16 | Biography in nav bar | Discoverability | Low | build_site.py |
| P17 | Search functionality | Navigation | Medium | JavaScript |
| P18 | Term-emblem link expansion | Cross-referencing | Medium | Data work |
| P19 | Era groupings on timeline | Navigation | Low | build_site.py |
| P20 | Scholarly conversation mapping | Intellectual context | High | Writing |
