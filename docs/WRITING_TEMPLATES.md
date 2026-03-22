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

### Scholar Page

```
[Scholar Name] [review badge]

OVERVIEW
[overview text — 2-3 paragraphs]

WORKS IN ARCHIVE
[For each bibliography entry via scholar_works:]
  [title] ([year])
  [pub_type] | [af_relevance badge]
  [summary if available]

EMBLEM COVERAGE
[List of emblem numbers this scholar analyzes, as links]
Covers [N] of 50 emblems.
```

### Dictionary Term Page

```
[Term Label] [category badge]
[label_latin in italic]

[definition_short — italicized, boxed]

DEFINITION
[definition_long — 3-5 sentences, scholarly but accessible]

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
