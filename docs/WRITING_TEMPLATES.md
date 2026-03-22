# WRITING_TEMPLATES.md — Voice Rules, Style Guide, and Content Templates

## Voice & Register

**Target reader**: An educated non-specialist visiting a museum exhibition on alchemical emblems. They have general humanities literacy but no prior knowledge of alchemy, Maier, or De Jong. Write as a curator would for a gallery wall text: authoritative, specific, grounded in visual and textual evidence.

**Voice rules**:
- **Person**: Third person for scholarly content. First person plural ("we") only in About and methodology.
- **Tense**: Present tense for what emblems depict and what scholars argue. Past tense for historical events.
- **Specificity**: Name concrete details — figures, objects, gestures, textual sources, page numbers. Avoid vague generalities like "this emblem is significant" or "the symbolism is complex."
- **Attribution**: Always attribute interpretations to their scholar. "De Jong identifies..." not "The emblem represents..." Write about what scholars argue, not what the emblem "means" in the abstract.
- **No verbatim copying**: Describe Maier's discourse in academic prose. Do not quote Maier's text as if it were description. Wrong: "The philosophers agree that their work is nothing but men's and women's work." Right: "Maier frames the alchemical operation as gendered labor, arguing that the masculine role is to generate and govern while the feminine role is to conceive, bear, and nourish."
- **Confidence language**: HIGH confidence = declarative ("derives from," "identifies"). MEDIUM = hedging ("likely," "appears to," "De Jong suggests"). LOW = explicit uncertainty ("may represent," "the connection is speculative").
- **Citations**: `(De Jong, p. 45)` or `(Tilton, ch. 3)`. Always include when available.
- **Terminology**: Use De Jong's terminology as canonical. When scholars disagree, note the variant.

## AI-Generated Content Disclosure

All AI-drafted content must include this banner:

> This content was drafted by an AI language model based on the scholarly sources in our corpus. It has not been reviewed by a human scholar. Citations are provided but should be verified against the original sources.

---

## Emblem Analysis Template (CANONICAL)

**This is the master template for the `analysis_html` field on each emblem.** Every emblem's analysis block must follow this 4-section structure. The script `seed_emblem_analyses.py` assembles this from DB fields and LLM-written prose stored in `image_description`, `discourse_summary`, and `analysis_html` sub-fields.

### Section 1: The Plate — What You See (3-5 sentences)

**Source field**: `emblems.image_description`

**Purpose**: Describe the engraved plate as a museum curator would describe a painting to a visitor standing in front of it. Ground the reader in the visual before any interpretation.

**Requirements**:
- Name every significant figure, animal, object, and architectural element
- Describe their positions, gestures, and spatial relationships
- Note the setting (landscape, interior, mythological space)
- Mention any inscriptions, banners, or text visible in the plate
- Use present tense ("A woman sits...", "The king extends...")
- Do NOT interpret symbolism here — just describe what is visible

**Example** (Emblem V):
> A woman sits outdoors on a stone bench, her bodice loosened, nursing a large toad at her breast. The toad clings to her chest with its forelimbs, drawing milk while the woman's expression registers neither pain nor alarm but a calm resignation. Behind her, a walled town rises against a hilly landscape with scattered trees. In the foreground, a second smaller toad waits on the ground. The scene is framed by Maier's characteristic architectural border with the emblem number and "De Secretis Naturae" header.

### Section 2: Maier's Discourse — What the Author Argues (3-5 sentences)

**Source field**: `emblems.discourse_summary`

**Purpose**: Summarize what Maier says in the prose discourse that accompanies this emblem. Write in academic prose — describe Maier's argument, do not reproduce his text. Frame it as "Maier argues..." or "The discourse develops..."

**Requirements**:
- Summarize the central argument or analogy Maier develops
- Note any classical, biblical, or alchemical authorities Maier cites
- Describe how Maier connects the emblem's visual allegory to the alchemical process
- Mention any specific alchemical operations or substances named
- Attribute clearly: this is Maier's argument, not objective fact

**Example** (Emblem V):
> Maier frames the alchemical operation as gendered labor, arguing that the masculine principle begets and governs while the feminine conceives, bears, and nourishes. He develops the toad as a figure for the volatile, poisonous agent that must be fed by the maternal body of the prima materia — a feeding that kills the nurse but matures the product. Maier draws the analogy to Cleopatra's death by asp-venom, suggesting that the transfer of vital essence from woman to toad mirrors the transfer of tincture from base matter to the philosophical mercury. The discourse explicitly cites the Pseudo-Aristotelian *Tractatulus de Practica Lapidis* as the source of this imagery.

### Section 3: De Jong's Source Analysis — Alchemical Traditions and Hidden Chemistry (3-5 sentences)

**Source field**: assembled from `scholarly_refs` (De Jong entries) + `emblem_sources` + `source_authorities`

**Purpose**: Present De Jong's central scholarly contribution — tracing each emblem back to its sources in earlier alchemical, Hermetic, and classical texts, and explaining what chemical knowledge is coded in the allegorical language.

**Requirements**:
- Identify which textual traditions De Jong traces this emblem to (Turba Philosophorum, Rosarium, Tabula Smaragdina, Ovid, etc.)
- Explain the specific chemical process or substance hidden behind the allegory
- Connect the emblem to broader Hermetic or Greek mythological traditions when applicable
- Note any cross-references De Jong makes to other emblems in the sequence
- This section is the scholarly heart of the page — De Jong's contribution is what makes this site unique

**Example** (Emblem V):
> De Jong traces the toad-and-woman motif to the Pseudo-Aristotelian *Tractatulus de Practica Lapidis Philosophici*, where the toad represents the volatile sulphurous component that must absorb the nurturing moisture of the mercurial body. She identifies the underlying chemistry as the fixation of volatile sulphur through prolonged contact with a liquid menstruum — the "feeding" is a slow absorption process in which the solvent (the woman/mercury) is consumed while the solute (the toad/sulphur) grows and stabilizes. De Jong connects this to the broader Hermetic tradition of the *coniunctio* as a sacrificial exchange, noting that Maier's image deliberately inverts the nurturing maternal archetype into an image of productive destruction. The emblem participates in a nigredo sequence (Emblems IV-VI) where dissolution, corruption, and death are presented as necessary preconditions for the alchemical work.

### Section 4: Scholarly Perspectives (1-3 sentences, optional)

**Source field**: assembled from `scholarly_refs` (non-De-Jong entries)

**Purpose**: Note any significant contributions from other scholars in our corpus (Tilton, Craven, Wescott, Pagel, Miner) that add to or complicate De Jong's reading.

**Requirements**:
- Keep this brief — De Jong is the primary focus, others supplement
- Note where scholars agree, disagree, or extend De Jong's analysis
- Mention Tilton's Rosicrucian context, Wescott's musical analysis, Craven's biographical detail, Pagel's medical-historical framing, or Miner's Blake connections where relevant
- If no other scholars discuss this emblem, omit this section entirely

**Example** (Emblem V):
> Tilton places this emblem within Maier's broader engagement with Paracelsian iatrochemistry, noting that the toad-venom imagery connects to early modern debates about the pharmaceutical use of animal poisons (Tilton, ch. 4, pp. 143-144). Craven reads the woman's death as Maier's commentary on the cost of alchemical knowledge to the practitioner.

---

## Writing Anti-Patterns (DO NOT)

| Anti-Pattern | Example | Why It's Wrong |
|-------------|---------|----------------|
| Vague significance | "This emblem is one of the most important in the series" | Says nothing specific |
| Copying Maier's voice | "The philosophers agree that their work is nothing but men's and women's work" | Unattributed quotation presented as description |
| Interpreting without attribution | "The toad represents evil" | Whose interpretation? |
| OCR artifacts in prose | "thephilosophers agree" | Raw extraction, not curated prose |
| Passive generality | "Symbolism is used throughout" | No agent, no specifics |
| Listing without synthesis | "Sources: Turba, Rosarium, Ovid" | Name them, but explain the connection |

---

## DB Field Contracts

Each field that feeds into the emblem page has specific content requirements:

| Field | Length | Content Type | Template Section |
|-------|--------|-------------|-----------------|
| `image_description` | 3-5 sentences | Visual description of plate (curatorial, descriptive, no interpretation) | Section 1: The Plate |
| `discourse_summary` | 3-5 sentences | Academic summary of Maier's discourse (attributed, analytical) | Section 2: Maier's Discourse |
| `analysis_html` | Full HTML block | Assembled by `seed_emblem_analyses.py` from all 4 sections | Complete analysis block |
| `motto_latin` | 1 sentence | Maier's original Latin motto | Motto display |
| `motto_english` | 1 sentence | Standard English translation | Motto display |

**Data flow**: Agents write `image_description` and `discourse_summary` as clean prose. The `seed_emblem_analyses.py` script reads these plus `scholarly_refs`, `emblem_sources`, and `source_authorities` to assemble the full `analysis_html` block following the 4-section template above.

---

## Other Page Templates

### Scholar Profile Template (CANONICAL)

**Source field**: `scholars.overview`

**Purpose**: Present each scholar as a museum exhibition would introduce a contributing expert — their background, intellectual formation, specific contributions to Maier/AF studies, key arguments, and place in the scholarly conversation.

**Structure**: 5-10 paragraphs covering these areas in order:

1. **Identity and credentials** (1 paragraph): Full name, dates, institutional affiliation, discipline, degrees. Frame the scholar within their field — art historian, musicologist, historian of science, etc.

2. **Intellectual formation and approach** (1-2 paragraphs): What tradition does this scholar work within? What methods do they bring — source criticism, iconographic analysis, musicological analysis, biographical reconstruction, reception history? What questions drive their work?

3. **Contributions to Maier studies** (2-3 paragraphs): What specifically has this scholar discovered, argued, or demonstrated about Maier and/or Atalanta Fugiens? Name specific findings: source identifications, biographical facts, interpretive frameworks, corrected misconceptions. Cite their key publications.

4. **Key arguments** (1-2 paragraphs): What are this scholar's most distinctive claims? Where do they agree with or challenge other scholars in our corpus? What would be lost from our understanding of Maier if this scholar's work didn't exist?

5. **Relevance to this site** (1 paragraph): How does this scholar's work inform the content presented here? Which emblem pages, dictionary entries, or source identifications draw on their research?

**Voice**: Academic but accessible. Write as a museum catalog essay introducing a contributor to an exhibition. Authoritative, specific, generous to the scholar's achievements.

**Anti-patterns**:
- Do NOT write "X is an important scholar" — explain WHY through specific contributions
- Do NOT list publications without explaining what they argue
- Do NOT reduce a scholar to a single finding — show the breadth of their contribution
- Do NOT write a Wikipedia-style biography — focus on their Maier/AF work

**Example opening** (De Jong):
> Helena Maria Elisabeth De Jong (1933-2016) was a Dutch art historian trained at the University of Utrecht, where she completed her doctoral dissertation on Michael Maier's Atalanta Fugiens in 1965. De Jong's monograph, published in expanded form by E.J. Brill in 1969, remains the foundational work of Atalanta Fugiens scholarship — the first systematic attempt to trace every emblem, motto, and discourse in Maier's book back to its sources in earlier alchemical, classical, and Hermetic literature.

**DB field contract**: The `scholars.overview` field stores the full profile text. It is rendered as the main content on individual scholar pages (`site/scholar/{slug}.html`). Minimum 5 paragraphs, maximum 10.

### Scholar Page (Layout)

```
[Scholar Name] [review badge]

PROFILE
[overview — 5-10 paragraphs following the template above]

WORKS IN ARCHIVE
[For each bibliography entry via scholar_works:]
  [title] ([year])
  [pub_type] | [af_relevance badge]
  [summary if available]

EMBLEM COVERAGE
[List of emblem numbers this scholar analyzes, as links]
Covers [N] of 50 emblems.
```

### Dictionary Entry Template (CANONICAL)

**Source field**: `dictionary_terms.definition_long`

**Purpose**: Each dictionary entry is a self-contained encyclopedia article that teaches a lay reader what this term means, how it functions in alchemical tradition, and — most importantly — how it is expressed in Michael Maier's Atalanta Fugiens as identified by De Jong and other scholars. The entry should make the reader feel they've learned something specific and fascinating, not that they've read a generic definition.

**Structure**: 5-10 paragraphs covering these areas:

1. **What is this?** (1-2 paragraphs): Define the term for a reader encountering it for the first time. If it's a mythological figure, tell their story. If it's a chemical process, explain what physically happens. If it's a source text, say who wrote it, when, and what it contains. Ground the reader before any alchemical interpretation.

2. **What does it mean in alchemy?** (1-2 paragraphs): Explain the term's alchemical significance — what does it represent in the symbolic language of the art? How do alchemists use this term differently from its ordinary meaning? If De Jong's multi-register model applies, show how the term operates simultaneously as material process, medical analogy, spiritual state, and cosmological principle.

3. **How does Maier express it in Atalanta Fugiens?** (2-3 paragraphs): This is the heart of the entry. Name specific emblems by number and describe exactly how Maier deploys this term — in the visual composition of the engraved plate, in the Latin motto, in the discourse argument, or in the fugue's musical structure. Quote Maier's motto text where relevant. Describe what the reader sees in the plate. Connect the visual allegory to the alchemical meaning. This section should feel like standing in front of the emblem with a knowledgeable guide.

4. **What does De Jong's scholarship reveal?** (1-2 paragraphs): Present De Jong's specific findings about this term — which source texts does she trace it to? What earlier traditions is Maier drawing upon? What does the source identification reveal about the hidden meaning? This is where the site's scholarly distinctiveness lives: De Jong's source-critical method is what makes the Atalanta Fugiens legible.

5. **The playful dimension** (1 paragraph): Where applicable, connect the term to Maier's lusus serius — his pedagogy of play and multi-sensory learning. How does the emblem's visual puzzle, musical accompaniment, or riddling epigram make this concept not merely an intellectual proposition but an experiential encounter? Maier designed the AF as a serious game: the reader chases meaning through the golden apples of image, verse, and music. Each dictionary entry should honor this ludic dimension.

**Voice**: Write as a museum guide speaking to an intelligent, curious visitor who has never heard of alchemy before. Be authoritative without being pompous. Use specific, concrete details — name emblems, describe images, identify sources. Avoid vague generalities like "this is an important concept" or "alchemists used this widely."

**Anti-patterns**:
- Do NOT write a generic Wikipedia-style definition with no AF content
- Do NOT list emblems without describing what happens in them
- Do NOT describe alchemical processes as if the reader already knows what they mean
- Do NOT omit De Jong — her source identifications are the scholarly foundation
- Do NOT ignore the visual and ludic dimensions — AF is an emblem book, not a textbook

**Example** (Nigredo — opening paragraphs):
> The nigredo, or blackening, is the first and most fearsome stage of the alchemical Great Work. In the sealed vessel of the alchemist's laboratory, the raw material — whatever combination of substances the practitioner has chosen — undergoes complete decomposition. The matter darkens, putrefies, and gives off a terrible stench. To the alchemist, this death of form is not failure but the necessary beginning: nothing new can be born until the old has been utterly destroyed. The nigredo is Saturn's dominion — cold, heavy, leaden, melancholy — and the alchemist must endure it as the farmer endures winter, knowing that spring depends upon the death of the previous year's growth.
>
> In Michael Maier's Atalanta Fugiens, the nigredo manifests across a sequence of emblems depicting death, dissolution, devouring, and entombment. In Emblem XXIV, a wolf devours a crowned king — the base, voracious antimony consuming the noble but impure gold. In Emblem XXVIII, King Duenech sits in a steam bath while black bile drains from his body, attended by physicians who purge the saturnine corruption through gentle moist heat. In Emblem XXXIII, the Hermaphrodite lies in total darkness, motionless as if dead, awaiting the fire that will begin its resurrection. And in Emblem XLIV, Typhon murders Osiris and scatters his limbs — the most violent image of dissolution in the entire series — before Isis painstakingly gathers and reassembles the divine body. Each of these emblems presents a different face of the nigredo: predation, purgation, death-sleep, and dismemberment.

**DB field contracts**:

| Field | Length | Content Type |
|-------|--------|-------------|
| `definition_short` | 1 sentence | Quick identification for card display |
| `definition_long` | 5-10 paragraphs | Full encyclopedia entry following this template |
| `significance_to_af` | 2-3 sentences | Quick AF-specific relevance (for structured display) |
| `registers` | JSON | 4-register definitions (if applicable) |

### Dictionary Term Page (Layout)

```
[Term Label] [category badge]
[label_latin in italic]

[definition_short — italicized, boxed]

DEFINITION
[definition_long — 5-10 paragraphs following the template above]

MEANINGS ACROSS REGISTERS (if applicable)
  Alchemical: [1-2 sentences]
  Medical: [1-2 sentences]
  Spiritual: [1-2 sentences]
  Cosmological: [1-2 sentences]

IN ATALANTA FUGIENS
[significance_to_af]

APPEARS IN EMBLEMS
[linked emblem numbers]

RELATED TERMS
[link buttons]
```

### Timeline Event

```
[year] [event_type badge]
[title]
[description_long — 2-3 sentences with historical context]
```

### Bibliography Entry

```
[author] ([year]). [title]. [journal/publisher].
[af_relevance badge] [annotation]
```

### Essay Page

```
[AI-GENERATED BANNER]
[Title]
[body_html — sectioned with h2/h3 headers]
SOURCES CITED
[numbered list]
```
