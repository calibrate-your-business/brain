# Frontmatter schema

Raw notes (`raw/<source>/`) -- minimal, set by the source:
```yaml
source: x-bookmarks      # which source produced it
type: bookmark           # bookmark | article | transcript | clip | ...
id: "2070..."            # stable source id
author: handle
url: https://...
created: <source timestamp>
```

Wiki notes (`wiki/`) -- richer, written by Claude:
```yaml
type: entity             # entity | concept | project | source | moc
title: ...
contexts: [research, schedule-wrangler]   # the context dimension (tags)
aliases: [...]
status: active
sensitivity: none        # none | pii | secret
created: YYYY-MM-DD
updated: YYYY-MM-DD
believed_on: YYYY-MM-DD   # bi-temporal: when the current claim was believed
revised_on: YYYY-MM-DD    # ...and when it last changed (omit if never)
```

Body conventions: open with a one-line "for future Claude" preamble; use
`[[wikilinks]]`; put provenance on claims (`[[raw/x-bookmarks/bookmarks/<id>]]`
or a source URL); add recency markers "(as of YYYY-MM, source)" on facts that
age.
