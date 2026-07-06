# Methodology -- the knowledge model

- **raw -> wiki (Karpathy LLM-Wiki).** Immutable sources in `raw/`; Claude
  compiles a self-rewriting `wiki/` of entity / concept / project / source
  pages. Rewrite on new material, don't just append.
- **Entity-concept-source triad.** Always factor knowledge into three page
  types: sources (what came in), entities (people/orgs/tools/products), concepts
  (ideas/frameworks/techniques). Dense cross-links between them are the value.
- **MOC/LYT-leaning** (matches Karim's working style): links over deep folders;
  Maps of Content as navigation. Folders are light; the graph carries meaning.
- **AI-first notes:** written for Claude's retrieval, not pretty reading. See
  `frontmatter-schema.md`. Provenance + recency + bi-temporal facts on claims.
- **Context is a dimension** (`contexts.md`): `context/<name>` tags + scoped
  views/indexes over the ONE graph. Never separate vaults.
- **Mechanics vs strategy.** Determinism belongs in scheduling / IO / store;
  understanding is always Claude. A regex classifier is the wrong layer doing
  strategy's job -- never ship one.
- **git is the only truth.** Keyword (FTS), semantic (vector), and
  entity/temporal databases are disposable indexes rebuilt from these files,
  each scopable per context.
