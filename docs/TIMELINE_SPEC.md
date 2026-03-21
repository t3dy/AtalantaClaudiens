# TIMELINE_SPEC.md — Timeline Event Model

## Scope

Reception and publication history of Atalanta Fugiens from 1568 (Maier's birth) through 2020 (Furnace & Fugue). 20+ events.

## Event Types

| Type | Color | Description |
|------|-------|-------------|
| PUBLICATION | Green | First publications of AF or related works |
| EDITION | Blue | Reprints, new editions, facsimiles |
| SCHOLARSHIP | Purple | Monographs, articles, reviews about AF |
| BIOGRAPHY | Orange | Life events of Maier and key scholars |
| DIGITAL | Teal | Digital editions, databases, websites |
| FACSIMILE | Brown | Photographic or facsimile reproductions |

## Initial Event Set (from seed JSON)

| Year | Type | Title |
|------|------|-------|
| 1568 | BIOGRAPHY | Michael Maier born in Rendsburg |
| 1597 | BIOGRAPHY | Maier receives MD from Rostock |
| 1608 | BIOGRAPHY | Maier joins Rudolf II's court |
| 1617 | PUBLICATION | Atalanta Fugiens first published |
| 1618 | PUBLICATION | Second typographic state |
| 1622 | BIOGRAPHY | Michael Maier dies in Magdeburg |
| 1687 | EDITION | Frankfurt German edition |
| 1708 | EDITION | Chymisches Cabinet edition |
| 1910 | SCHOLARSHIP | Craven biography published |
| 1964 | SCHOLARSHIP | De Jong article on Emblem XLVIII |
| 1965 | SCHOLARSHIP | De Jong reviews Wuethrich facsimile |
| 1969 | SCHOLARSHIP | De Jong monograph published (E.J. Brill) |
| 1973 | SCHOLARSHIP | Pagel review in Medical History |
| 1989 | EDITION | Godwin musical edition |
| 1991 | SCHOLARSHIP | Leedy reviews Godwin edition |
| 2002 | EDITION | De Jong monograph reprinted (Nicolas-Hays) |
| 2003 | SCHOLARSHIP | Tilton Quest for the Phoenix |
| 2009 | SCHOLARSHIP | Smith reviews Hofmeier edition |
| 2012 | SCHOLARSHIP | Miner Blake article |
| 2020 | DIGITAL | Furnace and Fugue published (UVA Press) |

## Display Rules

- Events sorted chronologically (ascending)
- Year shown as sticky header when multiple events share a year
- Filter checkboxes at top for each event type
- If `scholar_id` is set, scholar name links to scholar page
- If `bib_id` is set, "View in Bibliography" link
- Confidence badge shown if not HIGH

## Data Source

All events from `atalanta_fugiens_seed.json` → `timeline_events` array. Source method: `SEED_DATA`. Additional events may be added during Phase 2 extraction from corpus.
