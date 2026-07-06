# Ingest -- the intelligence pass (raw -> wiki, with judgment)

Replaces the regex enricher. Claude (not rules) reads `raw/<source>/` and
compiles/rewrites `wiki/` pages. This file is the contract every compile follows
so pages are uniform.

## What to produce

For a cluster of raw items, write/REWRITE pages of the entity-concept-source
triad:
- `wiki/entities/<slug>.md` -- a person, org, tool, product, or platform that
  recurs (e.g. Claude Code, MCP, Anthropic, Obsidian, Andrej Karpathy).
- `wiki/concepts/<slug>.md` -- an idea, framework, technique, or pattern (e.g.
  multi-agent orchestration, the second brain, context engineering, the
  solo-operator-with-AI model).
- (`wiki/sources/` and `wiki/projects/` come later -- not this pass.)

Only make a page when >= ~3 raw items support it, OR a single item is clearly
important (high-signal). Quality over coverage. Synthesize -- do NOT just list
bookmarks. The value is connecting what he read into a coherent take.

## Page format

```
---
type: entity            # entity | concept
title: Claude Code
slug: claude-code
contexts: [research]
aliases: [...]
status: active
created: 2026-06-28
updated: 2026-06-28
sources: 18             # how many raw items informed this page
---

> For future Claude: <one line on what this page is and why it matters to Karim>.

<2-5 paragraphs SYNTHESIZING what the raw material says about this entity/concept:
what it is, why it matters, the notable takes/techniques/threads Karim saved,
how it connects to his work (Schedule Wrangler, agent infra, the second brain).
Be substantive and specific; cite provenance inline.>

## Related
[[other-entity]] [[some-concept]] ...

## Provenance
- [[raw/x-bookmarks/bookmarks/<id>]] -- <1-line what that item contributed>
- ... (the strongest few, not all)
```

## Rules

- **Synthesis, not storage.** Connect, compare, draw out the throughline. Karim
  remembers he read these; the page gives him the details + the new idea.
- **Cross-link** with `[[wikilinks]]` (by page title/slug) generously -- the graph
  is the value. Linking a page that doesn't exist yet is fine.
- **Provenance** on claims: link the raw items (`[[raw/x-bookmarks/...]]`).
- **Recency / bi-temporal** where a fact ages: "(as of YYYY-MM, source)".
- **Rewrite, don't append** if the page exists.
- Tag `contexts: [research]` (this source's default). Sensitivity: none here.

## Daily incremental

The scheduled ingest reads only NEW raw since the last run (by `log.md` /
mtime), and updates the affected entity/concept pages + `index.md` + `log.md`.
Same format, same judgment, smaller batch.
