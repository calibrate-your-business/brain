# Contexts -- a dimension, not separate vaults

A context (research, schedule-wrangler, personal, ...) is a SCOPED VIEW over the
one graph, not a separate brain. Implemented as:
- a `context/<name>` tag (in `contexts:` frontmatter) on pages that belong to it,
- a per-context derived index/view (scoped FTS/semantic) for "search just this
  context,"
- never a separate vault or repo.

Why: the same node often spans contexts (a customer appears in research,
product, and delivery at once). Separate vaults would cut those links -- which
are the entire point of a second brain.

## Registered contexts (grow deliberately)

- `research` -- default for x-bookmarks and exploratory material.
- (add product/business contexts as Karim brings current context in -- e.g.
  `schedule-wrangler`. Do NOT pre-create from stale Jan docs.)

## Sensitivity layer

Orthogonal to context. Tag `sensitive/pii` (customer transcripts, rosters) or
`sensitive/secret` (credentials) and keep scoped (restricted subtree / scoped
keys). Access is controlled by keys, never by prompt instructions.
