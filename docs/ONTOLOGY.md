# ONTOLOGY.md — AtalantaClaudiens Database Schema

## Overview

**13 tables built** in `db/atalanta.db` + **7 tables planned** (documented here but not yet created via migration).

Tables tagged `[BUILT]` exist in the database. Tables tagged `[PLANNED]` are designed but have no migration script yet — do NOT write code that depends on them without creating the migration first.

Schema designed from SCHOLARSHIPREPORT.md ontology recommendations and GPTAF.txt/GPTPIPE.txt pipeline design.

## Entity-Relationship Summary

```
Emblem (0-50)
  ├── has many → EmblemProcesses → AlchemicalProcess
  ├── has many → VisualElements
  ├── has many → EmblemFigures → MythologicalFigure
  ├── has many → EmblemSources → SourceAuthority
  ├── has many → ScholarlyRefs → Bibliography → Scholar
  ├── has many → TermEmblemRefs → DictionaryTerm
  └── referenced by → TimelineEvents, Essays

Scholar ←→ Bibliography (via ScholarWorks)
DictionaryTerm ←→ DictionaryTerm (via DictionaryTermLinks)
```

## Core Tables

### emblems `[BUILT]`
The primary organizing unit. 51 rows (frontispiece = 0, emblems I-L = 1-50).

| Column | Type | Notes |
|--------|------|-------|
| id | INTEGER PK | |
| number | INTEGER UNIQUE | 0=frontispiece, 1-50=emblems |
| roman_numeral | TEXT | NULL for frontispiece, I-L |
| canonical_label | TEXT NOT NULL | Short English label |
| motto_latin | TEXT | |
| motto_english | TEXT | |
| motto_german | TEXT | |
| epigram_latin | TEXT | |
| epigram_english | TEXT | |
| epigram_german | TEXT | |
| discourse_summary | TEXT | |
| image_description | TEXT | Visual elements described |
| image_path | TEXT | Relative path to emblem image |
| alchemical_stage | TEXT | CHECK: NIGREDO/ALBEDO/CITRINITAS/RUBEDO/NULL |
| fugue_mode | TEXT | Musical mode if known |
| fugue_interval | TEXT | Canon interval type |
| analysis_html | TEXT | Structured emblem analysis (AI-assembled from DB fields) |
| visual_elements | TEXT | JSON: allegorical figures, symbols, composition |
| source_method | TEXT | DETERMINISTIC/SEED_DATA/LLM_ASSISTED |
| review_status | TEXT | DRAFT/REVIEWED/VERIFIED |
| confidence | TEXT | HIGH/MEDIUM/LOW |

### alchemical_processes `[PLANNED]`
Multi-register process model. NOT lab steps — symbolic clusters. **Not yet created — no migration exists.**

| Column | Type | Notes |
|--------|------|-------|
| id | INTEGER PK | |
| name | TEXT UNIQUE | e.g., "Coniunctio" |
| material_register | TEXT | Transmutation description |
| medical_register | TEXT | Humoral/healing description |
| spiritual_register | TEXT | Soul/spirit description |
| cosmological_register | TEXT | Planetary/macrocosm description |
| stage | TEXT | CHECK: NIGREDO/ALBEDO/CITRINITAS/RUBEDO/NULL |

### emblem_processes `[PLANNED]`
Join table: emblem ←→ process (many-to-many). **Not yet created.**

### visual_elements `[PLANNED]`
For image-text concordance. Describes what's depicted in each emblem. **Not yet created.** (Note: `emblems.visual_elements` JSON column exists on the `emblems` table as a simpler alternative.)

| Column | Type | Notes |
|--------|------|-------|
| id | INTEGER PK | |
| emblem_id | INTEGER FK | |
| element_type | TEXT | CHECK: FIGURE/OBJECT/ARCHITECTURE/LANDSCAPE/SYMBOL |
| description | TEXT | |
| position | TEXT | CHECK: FOREGROUND/BACKGROUND/CENTER/BORDER/NULL |
| alchemical_meaning | TEXT | |
| scholarly_source_id | INTEGER FK → bibliography | Who described this |

### mythological_figures `[PLANNED]`
Named figures appearing in emblems. **Not yet created.**

| Column | Type | Notes |
|--------|------|-------|
| id | INTEGER PK | |
| name | TEXT UNIQUE | e.g., "Atalanta", "Osiris" |
| description | TEXT | |
| tradition | TEXT | GREEK/EGYPTIAN/BIBLICAL/HERMETIC |

### emblem_figures `[PLANNED]`
Join table: emblem ←→ figure. **Not yet created.**

### source_authorities `[BUILT]`
De Jong's central contribution: Maier's textual sources as navigable entities.

| Column | Type | Notes |
|--------|------|-------|
| id | INTEGER PK | |
| authority_id | TEXT UNIQUE | e.g., AUTH_TURBA |
| name | TEXT | Full name |
| type | TEXT | CHECK: CLASSICAL/ALCHEMICAL/BIBLICAL/MEDICAL/PATRISTIC/HERMETIC/MOVEMENT |
| author | TEXT | |
| era | TEXT | |
| relationship_to_maier | TEXT | |
| description_long | TEXT | Rich scholarly description of this source's expression in AF |

### emblem_sources `[BUILT]`
Links emblems to their textual sources (De Jong's source identifications).

| Column | Type | Notes |
|--------|------|-------|
| id | INTEGER PK | |
| emblem_id | INTEGER FK | |
| authority_id | INTEGER FK | |
| relationship_type | TEXT | CHECK: MOTTO_SOURCE/DISCOURSE_CITATION/THEMATIC_PARALLEL/NARRATIVE_SOURCE |
| de_jong_page | TEXT | Page reference in De Jong |
| notes | TEXT | |
| confidence | TEXT | HIGH/MEDIUM/LOW |

### scholars `[BUILT]`
11 scholar profiles.

| Column | Type | Notes |
|--------|------|-------|
| id | INTEGER PK | |
| name | TEXT UNIQUE | |
| birth_year | INTEGER | |
| death_year | INTEGER | |
| specialization | TEXT | |
| af_focus | TEXT | What they study about AF |
| overview | TEXT | Biography/description |
| review_status | TEXT | DRAFT/REVIEWED/VERIFIED |

### bibliography `[BUILT]`
10 source works with relevance classification.

| Column | Type | Notes |
|--------|------|-------|
| id | INTEGER PK | |
| source_id | TEXT UNIQUE | e.g., de_jong_1969 |
| author | TEXT | |
| title | TEXT | |
| year | INTEGER | |
| journal | TEXT | |
| publisher | TEXT | |
| pub_type | TEXT | monograph/article/review/primary_source |
| af_relevance | TEXT | CHECK: PRIMARY/DIRECT/CONTEXTUAL |
| in_collection | INTEGER | 1 if we have the PDF |

### scholar_works `[BUILT]`
Join table: scholar ←→ bibliography.

### scholarly_refs `[BUILT]`
The core concordance table: links scholars' interpretations to specific emblems.

| Column | Type | Notes |
|--------|------|-------|
| id | INTEGER PK | |
| emblem_id | INTEGER FK | Nullable for general claims |
| bib_id | INTEGER FK | |
| interpretation_type | TEXT | CHECK: ICONOGRAPHIC/ALCHEMICAL/MYTHOLOGICAL/HISTORICAL/MUSICAL |
| summary | TEXT | |
| source_texts_referenced | TEXT | JSON array of authority_ids |
| section_page | TEXT | |
| confidence | TEXT | HIGH/MEDIUM/LOW |

### dictionary_terms `[BUILT]`
38 alchemical/emblematic terms. **Note**: `registers` column is documented below but does NOT exist in the DB yet — needs a migration to add it.

| Column | Type | Notes |
|--------|------|-------|
| id | INTEGER PK | |
| slug | TEXT UNIQUE | URL-safe identifier |
| label | TEXT | Display name |
| category | TEXT | CHECK: PROCESS/SUBSTANCE/FIGURE/CONCEPT/MUSICAL/SOURCE_TEXT |
| label_latin | TEXT | Latin form as used in AF (e.g., Lapis Philosophorum) |
| definition_short | TEXT | One-line definition |
| definition_long | TEXT | Extended definition |
| registers | TEXT | JSON: {alchemical, medical, spiritual, cosmological} |
| significance_to_af | TEXT | AF-specific usage paragraph |
| source_basis | TEXT | |
| review_status | TEXT | DRAFT/REVIEWED/VERIFIED |

### dictionary_term_links `[BUILT]`
Cross-references between dictionary terms.

### term_emblem_refs `[BUILT]`
Links dictionary terms to emblems where they appear.

### timeline_events `[BUILT]`
29 reception history events from 1568-2020.

| Column | Type | Notes |
|--------|------|-------|
| id | INTEGER PK | |
| year | INTEGER | |
| year_end | INTEGER | |
| event_type | TEXT | CHECK: PUBLICATION/EDITION/SCHOLARSHIP/BIOGRAPHY/DIGITAL/FACSIMILE |
| title | TEXT | |
| description | TEXT | Short description |
| description_long | TEXT | Rich historical context paragraph |
| scholar_id | INTEGER FK | |
| bib_id | INTEGER FK | |
| confidence | TEXT | HIGH/MEDIUM/LOW |

### editions `[PLANNED]`
Publication history of AF itself. **Not yet created.**

| Column | Type | Notes |
|--------|------|-------|
| id | INTEGER PK | |
| year | INTEGER | |
| place | TEXT | |
| publisher | TEXT | |
| state | TEXT | 1617/1618/1687/1708/etc. |
| components_present | TEXT | JSON: {music, images, german_text} |
| notes | TEXT | |

### essays `[PLANNED]`
5 AI-drafted essays. **Not yet created — needs migration + seed script.**

| Column | Type | Notes |
|--------|------|-------|
| id | INTEGER PK | |
| slug | TEXT UNIQUE | |
| title | TEXT | |
| topic | TEXT | |
| body_html | TEXT | |
| sources_cited | TEXT | JSON array of bib_ids |
| is_ai_generated | INTEGER | Default 1 |
| review_status | TEXT | DRAFT/REVIEWED/VERIFIED |

---

## Infrastructure Tables

### emblem_identity `[BUILT]`
Canonical identity layer for emblem-to-image grounding. 51 rows. Seeded by `seed_identity.py` from `data/emblem_manifest.json`.

| Column | Type | Notes |
|--------|------|-------|
| id | INTEGER PK | |
| emblem_number | INTEGER NOT NULL | 0=frontispiece, 1-50=emblems |
| roman_label | TEXT NOT NULL | Roman numeral (or "F" for frontispiece) |
| canonical_order | INTEGER NOT NULL | Display order |
| image_filename | TEXT | e.g., `emblem-05.jpg` |
| image_source | TEXT | e.g., `wikimedia_commons`, `science_history_institute` |
| image_url | TEXT | Source URL |
| alignment_confidence | TEXT | HIGH/MEDIUM/LOW |
| source_method | TEXT | DETERMINISTIC/SEED_DATA/MANUAL |
| notes | TEXT | |

### schema_version `[BUILT]`
Tracks which migrations have been applied. 4 rows (v1 through v4).

| Column | Type | Notes |
|--------|------|-------|
| version | INTEGER PK | 1, 2, 3, 4 |
| applied_at | TEXT | ISO timestamp |
| description | TEXT | What this migration added |
