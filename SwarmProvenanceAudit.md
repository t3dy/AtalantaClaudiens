# SwarmProvenanceAudit.md

### emblems (51 rows)
- confidence=HIGH: 49
- confidence=MEDIUM: 2
- review_status=DRAFT: 51

### scholarly_refs (64 rows)
- confidence=HIGH: 63
- confidence=MEDIUM: 1

### emblem_sources (134 rows)
- confidence=HIGH: 133
- confidence=MEDIUM: 1

### emblem_identity (51 rows)
- alignment_confidence=HIGH: 10
- alignment_confidence=NULL: 41
- source_method=MANUAL: 51

### dictionary_terms (38 rows)
- review_status=DRAFT: 38

### timeline_events (29 rows)
- confidence=HIGH: 29

## Assessment
- All extracted data has provenance (source_method on emblems, confidence on refs)
- No data at VERIFIED status (no human review has occurred)
- 41 emblem_identity rows have NULL confidence (no images sourced)
- Dictionary terms all DRAFT (appropriate for AI-seeded content)
