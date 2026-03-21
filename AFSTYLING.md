# AFSTYLING.md — Template & Style Guide for AtalantaClaudiens

## 1. Design System

### Color Palette
```css
--bg: #f5f0e8           /* Warm parchment background */
--bg-card: #fff          /* Card surfaces */
--text: #2c2418          /* Dark brown body text */
--text-muted: #6b5d4d    /* Secondary text */
--accent: #8b4513        /* Burnt sienna — headings, links, interactive elements */
--accent-light: #d4a574  /* Tan — highlights, hover states */
--border: #d4c5a9        /* Muted gold borders */
--header-bg: #2c2418     /* Dark brown header bar */
--header-text: #f5f0e8   /* Light parchment text on header */
```

### Type Colors (for badges and borders)
| Type | Color | Usage |
|------|-------|-------|
| HERMETIC | `#16a085` | Source authority type |
| ALCHEMICAL | `#c0392b` | Source authority type |
| CLASSICAL | `#8e44ad` | Source authority type |
| BIBLICAL | `#2980b9` | Source authority type |
| PATRISTIC | `#e67e22` | Source authority type |
| MOVEMENT | `#795548` | Source authority type |
| PUBLICATION | `#27ae60` | Timeline event type |
| EDITION | `#2980b9` | Timeline event type |
| SCHOLARSHIP | `#8e44ad` | Timeline event type |
| BIOGRAPHY | `#e67e22` | Timeline event type |
| DIGITAL | `#16a085` | Timeline event type |

### Typography
- **Serif** (body): Georgia, Times New Roman — for scholarly reading
- **Sans** (UI): Segoe UI, system-ui — for navigation, badges, labels
- **Line height**: 1.7 (body), 1.5-1.65 (cards)

---

## 2. Voice & Style Rules (Dekany Audit)

### Tense
- **Present tense** for describing emblems, scholarly claims, and alchemical processes: "Maier draws from the Turba...", "De Jong identifies..."
- **Past tense** for historical events: "Maier published in 1617...", "De Jong completed her dissertation in 1969..."

### Voice
- **Active voice** preferred: "De Jong traces the source to..." not "The source is traced by De Jong to..."
- **Third person** throughout: never "I" or "you" in scholarly content
- **First person plural** ("we") only in About page and methodology sections

### Terminology
- De Jong's terminology is **canonical**; variants noted when scholars disagree
- Latin forms preferred for alchemical terms on first mention: "the *coniunctio* (union of opposites)"
- Subsequent references may use English equivalent
- AF-specific meanings take priority over general alchemical definitions

### Formality
- Scholarly but accessible — no jargon without explanation
- Avoid hedging in HIGH confidence content; use hedging (likely, appears to) for MEDIUM/LOW

### Citations
- Inline: "De Jong (1969)" or "as Tilton (2003) argues"
- Section/page when available: "De Jong, Emblem XIV section"

### AI-Generated Content
All AI-drafted content shows this banner:
> Assembled from De Jong (1969) corpus extraction. Not reviewed by a human scholar. Citations should be verified against original sources.

CSS class: `.ai-banner`

---

## 3. Card Templates

### Emblem Gallery Card (Homepage + `/emblems/`)
```html
<div class="card">
  <!-- Image if available, placeholder if not -->
  <img src="images/emblems/emblem-{NN}.jpg" alt="Emblem {ROMAN}">
  <!-- OR: <div class="card-placeholder">{ROMAN}</div> -->
  <div class="card-body">
    <div class="card-sig">Emblem {ROMAN}</div>
    <div class="card-label">{canonical_label}</div>
    <div class="card-desc">{motto preview, 80 chars}</div>
  </div>
</div>
```

### Emblem Analysis Block (on emblem detail pages)
```html
<div class="emblem-analysis">
  <div class="ai-banner">...</div>
  <section>
    <h3>Overview</h3>
    <p>Motto meaning + what the emblem depicts</p>
  </section>
  <section>
    <h3>Maier's Source Texts</h3>
    <p>Cross-linked to /sources.html#{authority_id}</p>
  </section>
  <section>
    <h3>Alchemical Significance</h3>
    <p>Scholarly commentary summaries</p>
  </section>
  <section>
    <h3>Related Terms</h3>
    <p>Cross-linked to /dictionary/{slug}.html</p>
  </section>
</div>
```

### Dictionary Term Card (index page)
```html
<a href="{slug}.html" class="dict-card">
  <div class="dict-label">{label} <span class="badge badge-stage">{CATEGORY}</span></div>
  <div class="dict-latin">{label_latin}</div>  <!-- Suppressed if identical to label -->
  <div class="dict-def">{definition_short}</div>
</a>
```

### Dictionary Term Page
```
h1: {label} [CATEGORY badge]
.term-latin: {label_latin}  (italic, muted — suppressed if identical)
.motto-block: {definition_short}
body: {definition_long}
h2: In Atalanta Fugiens → {significance_to_af}
h2: Appears in Emblems → emblem-link-badges
h2: Related Terms → source-link buttons
footer: Source: {source_basis}
```

### Source Authority Card
```html
<div class="source-card" id="{authority_id}" style="border-left:4px solid {TYPE_COLOR}">
  <h4>{name} <span class="badge">{N} emblems</span></h4>
  <div class="source-desc">{description_long OR relationship_to_maier}</div>
  <div class="emblem-links">
    <a href="emblems/emblem-{NN}.html" class="emblem-link-badge">{ROMAN}</a>
    ...
  </div>
</div>
```

### Timeline Event Card
```html
<div class="timeline-year">{year}</div>  <!-- Sticky header, only on year change -->
<div class="timeline-card" style="border-left:4px solid {TYPE_COLOR}">
  <h4><span class="badge">{EVENT_TYPE}</span> {title}</h4>
  <div class="event-desc">{description_long OR description}</div>
</div>
```

### Scholar Reference Card (emblem detail pages)
```html
<div class="ref-card">
  <h4>{author} <span class="badge badge-stage">{interpretation_type}</span>
      <span class="review-badge confidence-{level}">{confidence}</span></h4>
  <p>{summary, truncated to 800 chars}</p>
  <p class="citation">{section_page}</p>
</div>
```

---

## 4. Page Templates

### Emblem Detail Page (Comparative View)
- **Layout**: CSS grid, 3fr / 2fr split
- **Left panel** (source-panel): Image, motto, epigram (collapsible), discourse summary, **analysis block**, stage badge
- **Right panel** (scholarship-panel): Scholarly refs, Maier's source links
- **Navigation**: Prev/Next links + Gallery link

### Dictionary Index
- **Title**: "Dictionary of *Atalanta Fugiens*"
- **Layout**: Grouped by category, each category has a heading + dict-cards
- **Card style**: Clickable full-width cards with Latin subtitle

### Sources Index
- **Title**: "Maier's Sources & Influences"
- **Layout**: Grouped by type (HERMETIC, ALCHEMICAL, CLASSICAL, etc.)
- **Card style**: Left-colored border, rich description, emblem link badges

### Timeline
- **Title**: "Timeline of Atalanta Fugiens"
- **Layout**: Vertical chronological, sticky year headers
- **Card style**: Left-colored border, type badge, rich description

---

## 5. Cross-Linking Conventions

| From | To | Link Pattern |
|------|----|-------------|
| Emblem analysis | Source authority | `<a href="../sources.html#{authority_id}" class="cross-link">` |
| Emblem analysis | Dictionary term | `<a href="../dictionary/{slug}.html" class="cross-link">` |
| Source card | Emblem page | `<a href="emblems/emblem-{NN}.html" class="emblem-link-badge">` |
| Dictionary term | Emblem page | `<a href="../emblems/emblem-{NN}.html" class="source-link">` |
| Dictionary term | Related term | `<a href="{slug}.html" class="source-link">` |

---

## 6. Provenance Badges

| Badge | CSS Class | When to Show |
|-------|-----------|-------------|
| HIGH confidence | `.confidence-high` | Deterministic extraction or verified data |
| MEDIUM confidence | `.confidence-medium` | LLM-assisted or unverified extraction |
| LOW confidence | `.confidence-low` | Uncertain or sparse source data |
| DRAFT review | `.review-badge` | Content not yet human-reviewed |
| AI-generated | `.ai-banner` | Any AI-assembled content block |
| Stage badge | `.badge-stage` | Alchemical stage or category label |

---

## 7. File Reference

| Component | File | Lines |
|-----------|------|-------|
| CSS variables | `site/style.css` | 4-17 |
| Card styles | `site/style.css` | 42-95 |
| Analysis block styles | `site/style.css` | 97-115 |
| Source/Timeline/Dict card styles | `site/style.css` | 117-155 |
| Emblem page template | `scripts/build_site.py` | 166-270 |
| Dictionary templates | `scripts/build_site.py` | 501-590 |
| Timeline template | `scripts/build_site.py` | 615-650 |
| Sources template | `scripts/build_site.py` | 654-720 |
| Analysis generator | `scripts/seed_emblem_analyses.py` | full file |
| Seed data | `atalanta_fugiens_seed.json` | dictionary, source_authorities, timeline arrays |
