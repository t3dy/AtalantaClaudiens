# WRITING_TEMPLATES.md — Voice Rules and Page Content Templates

## Voice Rules

- **Person**: Third person for scholarly content. First person plural ("we") only in About page and methodology sections.
- **Tense**: Present tense for describing what emblems depict and what scholars argue. Past tense for historical events.
- **Terminology**: Use De Jong's terminology as canonical. When scholars disagree on terms, note the variant.
- **Citations**: Always include page/section references when available. Format: `(De Jong, p. 45)` or `(Tilton, ch. 3)`.
- **Confidence language**: When confidence is MEDIUM or LOW, use hedging: "likely," "appears to," "De Jong suggests." When HIGH, use declarative: "derives from," "identifies," "is."

## AI-Generated Content Disclosure

All AI-drafted content must include this banner at the top of the page:

> This content was drafted by an AI language model based on the scholarly sources in our corpus. It has not been reviewed by a human scholar. Citations are provided but should be verified against the original sources.

## Page Templates

### Emblem Detail Page

```
[Emblem Number] — [Canonical Label]

LEFT PANEL:
  [Image or placeholder]

  MOTTO
  Latin: [motto_latin]
  English: [motto_english]

  EPIGRAM (collapsible)
  [epigram text]

  DISCOURSE SUMMARY
  [discourse_summary]

  Stage: [NIGREDO/ALBEDO/CITRINITAS/RUBEDO badge]

RIGHT PANEL:
  DE JONG'S ANALYSIS
  [De Jong scholarly_ref summary]
  Sources identified: [authority links]
  Citation: [section_page]
  [confidence badge]

  OTHER SCHOLARS
  [For each non-De-Jong scholarly_ref:]
    [scholar name] — [interpretation_type badge]
    [summary]
    [confidence badge]

  MAIER'S SOURCES
  [For each emblem_source:]
    [authority name] → [relationship_type badge]
    [notes]

  VISUAL ELEMENTS
  [For each visual_element:]
    [description] ([position]) — [alchemical_meaning]

  RELATED TERMS
  [term labels as link buttons]
```

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

PROVENANCE
Source: [source_method] | Review: [review_status]
```

### Dictionary Term Page

```
← Dictionary

[Term Label] [category badge] [review badge]

[definition_short — italicized, boxed]

DEFINITION
[definition_long]

REGISTERS (if multi-register)
  Alchemical: [registers.alchemical]
  Medical: [registers.medical]
  Spiritual: [registers.spiritual]
  Cosmological: [registers.cosmological]

SIGNIFICANCE TO ATALANTA FUGIENS
[significance_to_af]

APPEARS IN EMBLEMS
[linked emblem numbers with canonical labels]

RELATED TERMS
[link buttons to related terms]

PROVENANCE
Source: [source_basis] | Review: [review_status]
```

### Timeline Event

```
[year] [event_type badge]
[title]
[description]
[scholar link if applicable] | [bibliography link if applicable]
```

### Bibliography Entry

```
[author] ([year]). [title]. [journal/publisher].
[af_relevance badge] [in_collection badge]
```

### Essay Page

```
[AI-GENERATED BANNER]

[Title]

[body_html — sectioned with h2/h3 headers]

SOURCES CITED
[numbered list of bibliography entries]
```
