# SwarmSchemaAudit.md

**Tables in DB**: 13: bibliography, dictionary_term_links, dictionary_terms, emblem_identity, emblem_sources, emblems, schema_version, scholar_works, scholarly_refs, scholars, source_authorities, term_emblem_refs, timeline_events

### bibliography (10 rows)
- Documented: Yes
- Columns: id, source_id, author, title, year, journal, publisher, pub_type, af_relevance, in_collection, annotation

### dictionary_term_links (66 rows)
- Documented: Yes
- Columns: term_id, linked_term_id, link_type

### dictionary_terms (38 rows)
- Documented: Yes
- Columns: id, slug, label, category, definition_short, definition_long, significance_to_af, source_basis, review_status, label_latin

### emblem_identity (51 rows)
- Documented: MISSING from ONTOLOGY.md
- Columns: id, emblem_number, roman_label, canonical_order, image_filename, image_source, image_url, alignment_confidence, source_method, notes

### emblem_sources (134 rows)
- Documented: Yes
- Columns: id, emblem_id, authority_id, relationship_type, de_jong_page, notes, confidence

### emblems (51 rows)
- Documented: Yes
- Columns: id, number, roman_numeral, canonical_label, motto_latin, motto_english, motto_german, epigram_latin, epigram_english, discourse_summary, image_description, image_path, alchemical_stage, source_method, review_status, confidence, analysis_html

### schema_version (4 rows)
- Documented: MISSING from ONTOLOGY.md
- Columns: version, applied_at, description

### scholar_works (9 rows)
- Documented: Yes
- Columns: scholar_id, bib_id

### scholarly_refs (64 rows)
- Documented: Yes
- Columns: id, emblem_id, bib_id, interpretation_type, summary, source_texts_referenced, section_page, confidence

### scholars (11 rows)
- Documented: Yes
- Columns: id, name, birth_year, death_year, specialization, af_focus, overview, review_status

### source_authorities (15 rows)
- Documented: Yes
- Columns: id, authority_id, name, type, author, era, relationship_to_maier, description_long

### term_emblem_refs (73 rows)
- Documented: Yes
- Columns: term_id, emblem_id, context

### timeline_events (29 rows)
- Documented: Yes
- Columns: id, year, year_end, event_type, title, description, scholar_id, bib_id, confidence, description_long

## Schema Versions
- v1: Phase 1 minimal schema: emblems, bibliography, source_authorities, scholarly_refs, emblem_sources
- v2: Phase 2-3 tables: scholars, scholar_works, dictionary_terms, dictionary_term_links, term_emblem_refs, timeline_events
- v3: Content enrichment: emblems.analysis_html, dictionary_terms.label_latin, source_authorities.description_long, timeline_events.description_long
- v4: Emblem identity layer: emblem_identity table for deterministic image grounding

## Drift Found
- emblem_identity: not documented in ONTOLOGY.md
- bibliography.annotation: not documented
- registers JSON field: documented but never populated
- definition_long: documented but never populated
