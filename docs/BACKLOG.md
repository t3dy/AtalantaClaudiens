# BACKLOG.md — Queued Feature Requests (from 2026-03-21 session)

**Priority key**: P1 = next session, P2 = soon, P3 = when time allows

---

## P1: Dictionary Enrichment (in progress)

**Status**: 4 swarm agents writing 5-10 paragraph encyclopedia entries. Awaiting completion.

- 94 terms need enriched `definition_long` following the canonical template in `WRITING_TEMPLATES.md`
- Template emphasizes: De Jong's source-critical findings, Maier's lusus serius pedagogy, specific AF emblem references
- Autolink infrastructure ready: `autolink_emblems()` converts "Emblem XXIV" to clickable links
- When swarm completes: validate JSON, merge, update DB, rebuild

---

## P2: "Emblems According to Maier" Tab

**Request**: A new tab displaying each emblem with:
- Large emblem image pane/card
- 5-10 sentence summary of the **poem** (epigram) connected to the emblem
- 5-10 sentence summary of the **discourse** connected to the emblem
- Verbatim quoting of key passages with academic explanation
- Alchemical theories and contexts for the nonspecialist reader

**Design notes**:
- Large cards or frames with substantial visible text (not requiring click-through)
- Consider CSS Grid or flexbox cards with emblem image LEFT, text RIGHT
- 51 entries (frontispiece + 50 emblems)
- Content sourced from `emblems.epigram_english` + `emblems.discourse_summary` + new curated prose
- Should use best front-end practices for economical display of 51 rich entries (lazy loading, scroll-based rendering)

**Implementation**:
- New nav tab: `('Maier', 'maier.html')`
- New function: `build_maier_page(conn)` in `build_site.py`
- Content: curated academic prose summarizing each emblem's epigram and discourse
- Data source: existing DB fields + new `maier_commentary` field or inline content

---

## P2: "Maier According to Jung" Essay

**Request**: An essay for the essays section covering:
- Jung's psychological readings of AF plates (from Psychology and Alchemy, extracted to E:/pdf/alchemy/)
- The Newman-Principe critique of Jungian readings of alchemy
- Hereward Tilton's response in The Quest for the Phoenix (already in our corpus)
- How Tilton mediates between the reductive laboratory readings and purely Jungian symbolic approaches

**Sources available**:
- Jung, Psychology and Alchemy: 44 Maier-relevant pages extracted
- Tilton corpus: 13,881 lines, full chapters on this debate
- Newman/Principe arguments referenced in Tilton

**Implementation**:
- Write essay content (5-15 paragraphs)
- Add to `essays` table in DB (needs migration — table is `[PLANNED]`)
- Or: build as a standalone page like the Szulakowska feature page

---

## P2: "Maier's Social World" Essay

**Request**: An essay collecting information from our sources about:
- All Maier's known associates (Rudolf II, Moritz von Hessen, Sir William Paddy, Francis Anthony, etc.)
- The courts he was involved with (Prague, London, Hessen-Kassel, Magdeburg)
- Alchemical movements he engaged with (Paracelsianism, Rosicrucianism) and his idiosyncratic positions
- Forshaw's characterization of Maier as "not Paracelsian" and his preference for "chemical" over "alchemical"
- Godwin's account of the unlanded nobleman problem and diplomatic mission

**Sources**:
- Godwin essay (fully read)
- Tilton corpus (partially read)
- Forshaw transcript (fully read)
- Craven (partially read)
- Szulakowska (all three books)

---

## P2: External Corpus Integration

**Request**: Produce substantial summaries of everything about Maier in the 56 extracted PDF sources from E:/pdf/alchemy/. Record all works mentioning Maier in the bibliography.

**Status**: Text extracted to .maier_extract.txt files alongside each PDF. Report at docs/reports/EXTERNALCORPUSSEARCH.md lists all 91 PDFs with page counts.

**Top targets for reading**:
1. Lyndy Abraham, Dictionary of Alchemical Imagery (47 pages of Maier content)
2. Jung, Psychology and Alchemy (44 pages)
3. Margaret Healy, Shakespeare and Alchemy (41 pages)
4. Tara Nummedal, Alchemy and Authority (37 pages)
5. Peter Forshaw, The Mage's Images (35 pages)
6. Glasgow Emblem Studies, Emblems and Alchemy (32 pages)
7. William Newman, Newton the Alchemist (32 pages)
8. Lawrence Principe, The Secrets of Alchemy (30 pages)

---

## P2: Timeline Update — Maier-Focused Studies

**Request**: Add all Maier-focused scholarly works to the timeline, plus all recordings and performances of AF music. Do NOT include works where Maier is merely mentioned (e.g., Jung, Abraham, Newman) — only works primarily about Maier.

**Works to add** (year, type, title):
- 1910 SCHOLARSHIP: Craven, Count Michael Maier (already in timeline?)
- 1965 SCHOLARSHIP: De Jong, Netherlands Yearbook article on AF
- 1969 SCHOLARSHIP: De Jong, Atalanta Fugiens: Sources monograph
- 1973 SCHOLARSHIP: Pagel, Review of De Jong
- 1985 PUBLICATION: Godwin, "Background for Maier's AF" (Hermetic Journal)
- 1987 PUBLICATION: Godwin edition of AF (Magnum Opus) — already added
- 1989 PUBLICATION: Godwin, Phanes Press edition
- 1991 SCHOLARSHIP: Leedy, Review of Godwin edition
- 1999 SCHOLARSHIP: Godwin, "Deepest of the Rosicrucians" essay
- 2003 SCHOLARSHIP: Tilton, Quest for the Phoenix
- 2007 PUBLICATION: Godwin, Spanish edition (La Fuga de Atalanta)
- 2008 PUBLICATION: Hofmeier, Chymisches Cabinet (German edition)
- 2009 SCHOLARSHIP: Smith, Review of Hofmeier edition
- 2011 SCHOLARSHIP: Hasler, Performative and Multimedia Aspects
- 2012 SCHOLARSHIP: Long, Music and Meditative Practices
- 2012 SCHOLARSHIP: Miner, Blake and AF
- 2012 SCHOLARSHIP: Forshaw, Infinite Fire webinar
- 2017 SCHOLARSHIP: Bilak, Playful Humanism (Columbia WIP)
- 2020 DIGITAL: Furnace and Fugue — already added
- 2020 SCHOLARSHIP: Forshaw, "Michael Maier and Mythoalchemy"
- 2024 SCHOLARSHIP: Rozenrichter, Hidden Dryads (SHAC)

**Recordings/performances to add** (some already in timeline):
- 1987 recording: Godwin edition first recording
- 2006 performance: Arcanum at Philadelphia — already added
- 2011 recording: Ensemble Plus Ultra/Claudio — already added
- 2014 performance: Les Canards Chantants begin — already added
- 2020 performance: MITO Festival
- 2021 recording: RIM c-Orchestra/Kanaga (Bandcamp)

---

## P3: Related Emblems Sidebar

From FUTURESESSIONS.md — horizontal row of 3-4 related emblem thumbnails on each emblem page, linked by shared alchemical stage, source authorities, or dictionary terms. ~30 min implementation, pure SQL + template.

## P3: Source x Emblem Matrix Visualization

From FUTURESESSIONS.md — interactive grid showing which source authorities appear in which emblems. 15x51 grid with colored cells by relationship type. ~30-60 min.

## P3: Thematic Pathways

Named reading sequences that cut across numerical order: King sequence, Washing motif, Hermaphrodite series, Fire mastery, Death/resurrection, Mythological. Each as a guided pathway on the home page.

## P3: Vision Pipeline

Claude Vision analysis of all 51 emblem plates → structured JSON in `emblems.visual_elements`. ~$1 API cost, 60 min implementation.

---

## Infrastructure Notes

- **Swarm pattern**: Use staging-file pattern (agents write JSON, main session merges). See `docs/SWARMGUIDELINES.md`.
- **Dictionary template**: See `docs/WRITING_TEMPLATES.md` — canonical 5-section structure with autolinks.
- **Emblem template**: See `docs/WRITING_TEMPLATES.md` — 4-section museum-level structure.
- **Scholar template**: See `docs/WRITING_TEMPLATES.md` — 5-section academic profile.
- **External corpus**: Text extracts in E:/pdf/alchemy/*.maier_extract.txt (56 files).
