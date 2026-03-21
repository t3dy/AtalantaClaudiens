# INTERFACE.md — AtalantaClaudiens Website Specification

## Navigation

9 tabs, consistent across all pages. Active tab highlighted with `--accent` color.

```
Home | Emblems | Scholars | Dictionary | Timeline | Sources | Essays | Bibliography | About
```

## Page Types

### 1. Home / Emblem Gallery (`/index.html`)

- **Stats bar**: Total emblems, scholars, sources, dictionary terms
- **Filter buttons**: By alchemical stage (Nigredo/Albedo/Citrinitas/Rubedo), by source tradition, "All"
- **Gallery grid**: CSS Grid `repeat(auto-fill, minmax(320px, 1fr))`
- **Cards**: Emblem thumbnail, Roman numeral, canonical label, stage badge
- **Lightbox**: Click card → modal with larger image, motto, stage, key scholarly note. Prev/Next navigation. Keyboard: Escape, ArrowLeft, ArrowRight.
- **Data source**: `data.json` loaded by `script.js`

### 2. Emblem Detail Pages (`/emblems/emblem-01.html` through `emblem-50.html` + `frontispiece.html`)

**Layout: Comparative View** (CSS Grid, two columns)

**Left Panel (60%)**:
- Emblem image (placeholder or public domain scan)
- Motto (Latin + English)
- Epigram (Latin + English, collapsible)
- Discourse summary
- Alchemical stage badge

**Right Panel (40%)**:
- **De Jong's Commentary** (primary, always shown first)
  - Source identifications with authority links
  - Interpretation summary
  - Page/section citation
  - Confidence badge
- **Other Scholars** (sorted by relevance)
  - Scholar name → link to scholar page
  - Interpretation type badge (ICONOGRAPHIC/ALCHEMICAL/MYTHOLOGICAL/HISTORICAL/MUSICAL)
  - Summary
  - Confidence badge
- **Maier's Sources** (from `emblem_sources`)
  - Authority name → link to sources page
  - Relationship type badge (MOTTO_SOURCE/DISCOURSE_CITATION/THEMATIC_PARALLEL)
- **Visual Elements** (from `visual_elements`)
  - Element descriptions with positions and meanings
- **Related Dictionary Terms**
  - Term labels as link buttons → dictionary pages

**Navigation**: Prev/Next buttons. Back to gallery link.

### 3. Scholars (`/scholars.html` + `/scholar/*.html`)

**Index**: Grid of scholar cards with name, specialization, af_focus, work count.

**Detail page**:
- Scholar name + review badge
- Overview biography
- "Works in Archive" — paper cards with title, year, topic badges, summary
- "Emblem Coverage" — which emblems this scholar analyzes, with links
- Provenance section

### 4. Dictionary (`/dictionary/index.html` + `/dictionary/*.html`)

**Index**: Grouped by category (PROCESS, SUBSTANCE, FIGURE, CONCEPT, MUSICAL, SOURCE_TEXT). Category headers with count badges.

**Term page**:
- Back link to dictionary index
- Term name + category badge + review badge
- Short definition (italicized, boxed)
- Long definition
- "Registers" section: alchemical, medical, spiritual, cosmological meanings (if applicable)
- "Significance to Atalanta Fugiens"
- "Appears in Emblems" — linked emblem numbers
- "Related Terms" — inline link buttons
- Provenance section

### 5. Timeline (`/timeline.html`)

- Vertical timeline with year markers
- Color-coded event type badges:
  - PUBLICATION (green)
  - EDITION (blue)
  - SCHOLARSHIP (purple)
  - BIOGRAPHY (orange)
  - DIGITAL (teal)
  - FACSIMILE (brown)
- Filter checkboxes by event type
- Each event: year, type badge, title, description
- Events span 1568-2020

### 6. Sources (`/sources.html`)

- Grouped by source type: CLASSICAL, ALCHEMICAL, BIBLICAL, MEDICAL, PATRISTIC, HERMETIC
- Each source authority: name, author, era, relationship to Maier
- "Used in Emblems" — linked emblem numbers
- "Identified by" — scholar attribution

### 7. Essays (`/essays/index.html` + `/essays/*.html`)

**Index**: Cards with essay title, topic, AI-generated badge.

**Essay page**:
- AI-generated banner (prominent, honest)
- Title + topic
- Sectioned long-form content
- Inline citations linking to bibliography
- Sources cited list at bottom

**Planned essays**:
1. "Playful Reading in Atalanta Fugiens"
2. "Alchemical Symbolism and the Emblem Tradition"
3. "Maier's Musical Fugues"
4. "The Rosicrucian Context"
5. "Reception History: From 1618 to Digital Humanities"

### 8. Bibliography (`/bibliography.html`)

- Stats bar: total works, in-collection count, by relevance
- Relevance badges: PRIMARY (red), DIRECT (blue), CONTEXTUAL (gray)
- Full citation for each work
- Link to scholar page if author is in scholars table

### 9. About (`/about.html`)

- Project statistics (counts from all tables)
- Methodology description
- Data provenance notes (what's deterministic, what's LLM-assisted)
- AI disclosure statement
- Link to GitHub repository
- Credits and acknowledgments

## CSS Component Classes

| Class | Used On | Pattern |
|-------|---------|---------|
| `.gallery` | Home | Grid of cards |
| `.card` | Home, scholars, essays | Hover-lift box |
| `.lightbox` | Home | Fixed overlay modal |
| `.comparative-view` | Emblem detail | Two-column CSS Grid |
| `.emblem-nav` | Emblem detail | Prev/Next bar |
| `.scholar-card` | Scholars | Bordered profile box |
| `.dict-detail` | Dictionary | Max-width readability |
| `.timeline` | Timeline | Vertical line with events |
| `.bib-entry` | Bibliography | Citation with badges |
| `.source-type-badge` | Sources | Color-coded by type |
| `.confidence-badge` | Throughout | HIGH/MEDIUM/LOW color |
| `.review-badge` | Throughout | DRAFT/REVIEWED/VERIFIED |
| `.ai-generated-banner` | Essays | Prominent AI disclosure |
| `.register-tabs` | Dictionary | Tabs for multi-register display |
| `.stat-card` | Home, About | Flexbox stat boxes |
| `.filter-btn` | Home, Timeline | Toggle filter buttons |

## Badge Color Scheme

| Badge | Background | Text |
|-------|-----------|------|
| PRIMARY | `#c0392b` | white |
| DIRECT | `#2980b9` | white |
| CONTEXTUAL | `#7f8c8d` | white |
| HIGH confidence | `#27ae60` | white |
| MEDIUM confidence | `#f39c12` | white |
| LOW confidence | `#e74c3c` | white |
| DRAFT review | `#f0e6d3` | `--text-muted` |
| VERIFIED review | `#d4edda` | `#155724` |
| AI-GENERATED | `#fff3cd` | `#856404` |
