# brain

Karim's second brain: one well-designed, plain-markdown + git knowledge graph
that Claude reads, compiles, links, and synthesizes -- and that loads Karim's
context every session. Many SOURCES feed it; Claude is the intelligence on top.

This is a NEW, deliberately-built project. It is **not** the old
`~/Documents/Claude/Projects/Obsidian Vault` (that one is set aside; content is
mined into here selectively, never bulk-imported).

## The shape

```
PROFILE.md          who Karim is -- loaded every session (built via interview)
CRITICAL_FACTS.md   ~120-token always-loaded essentials
CLAUDE.md           operating manual: how Claude works this brain
index.md            catalog of wiki pages
log.md              append-only activity log

raw/<source>/       immutable source material, one subdir per source (Claude reads, never edits)
wiki/               the COMPILED layer Claude writes/rewrites:
  entities/         people, orgs, tools, products
  concepts/         ideas, frameworks, techniques
  projects/         per-project / per-context notes
  sources/          one overview page per source

sources/            the ingest contract + one <name>.source per registered source
meta/               the knowledge model: methodology, frontmatter schema, contexts, sensitivity
```

## Principles (the architecture, decided)

- **One brain, context is a DIMENSION** -- not a vault per context. "Research"
  vs "Schedule Wrangler" are scoped views + per-context indexes over this one
  graph, never separate brains. The value is the connections across contexts.
- **git is the only truth.** Every derived index (keyword / semantic / entity)
  is a disposable cache rebuilt from these files.
- **Sources feed the brain** (up to ~100). A source drops raw material into
  `raw/<source>/` and declares itself in `sources/`. **x-bookmarks is source
  #1.** Claude's intelligence compiles `raw/` -> `wiki/`.
- **Mechanics vs strategy.** Deterministic plumbing (launchd scheduling, ingest
  transport, git store) is separate from intelligence (Claude understanding).
  Never use a mechanic (regex) to do strategy's job (understanding).
- **Selective, never bulk.** Old/business/research content comes in deliberately,
  current and relevant only.

Plan of record: `~/Claude/x-bookmarks/plans/second-brain-spec.md`.
