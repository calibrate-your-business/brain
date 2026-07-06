#!/usr/bin/env python3
"""Build the brain's derived indexes from the canonical markdown (rebuildable
from git; disposable cache). Two indexes today:
  - FTS5 keyword index over wiki pages + raw items (BM25), context-scopable.
  - the entity/link graph (pages + [[wikilinks]]) for traversal + lint.
Semantic/vector index is deferred (the heavy one).

  python3 db/build_index.py    # rebuilds db/brain.db from scratch
"""
import os, re, sqlite3, sys
from pathlib import Path

# DATA lives in the private brain-db repo; this script is the brain SYSTEM.
# Override the data dir with BRAIN_DB (default ~/Claude/brain-db).
B = Path(os.environ.get("BRAIN_DB") or (Path.home() / "Claude" / "brain-db"))
DB = B / "db" / "brain.db"

FM = re.compile(r"^---\n(.*?)\n---\n(.*)$", re.S)
LINK = re.compile(r"\[\[([^\]]+)\]\]")


def parse(path):
    text = path.read_text(encoding="utf-8")
    m = FM.match(text)
    meta, body = ({}, text)
    if m:
        body = m.group(2)
        for line in m.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip().strip("[]")
    slug = meta.get("slug") or path.stem
    return {
        "slug": slug, "path": str(path.relative_to(B)),
        "type": meta.get("type", ""), "title": meta.get("title", path.stem),
        "contexts": meta.get("contexts", ""), "sensitivity": meta.get("sensitivity", "none"),
        "tags": meta.get("aliases", ""), "body": body,
        "links": [l.split("|")[0].strip() for l in LINK.findall(body)],
    }


def main():
    DB.parent.mkdir(exist_ok=True)
    if DB.exists():
        DB.unlink()
    c = sqlite3.connect(DB)
    c.executescript("""
      CREATE TABLE pages(slug TEXT PRIMARY KEY, path, type, title, contexts, sensitivity, aliases);
      CREATE VIRTUAL TABLE pages_fts USING fts5(slug UNINDEXED, title, body, tags);
      CREATE TABLE links(src TEXT, dst TEXT);
      CREATE VIRTUAL TABLE raw_fts USING fts5(id UNINDEXED, source UNINDEXED, body);
    """)

    npages = nlinks = 0
    for d in ("wiki/projects", "wiki/concepts", "wiki/entities", "wiki/synthesis"):
        for p in sorted((B / d).glob("*.md")):
            r = parse(p)
            c.execute("INSERT OR REPLACE INTO pages VALUES(?,?,?,?,?,?,?)",
                      (r["slug"], r["path"], r["type"], r["title"], r["contexts"], r["sensitivity"], r["tags"]))
            c.execute("INSERT INTO pages_fts VALUES(?,?,?,?)",
                      (r["slug"], r["title"], r["body"], r["tags"]))
            for dst in set(r["links"]):
                c.execute("INSERT INTO links VALUES(?,?)", (r["slug"], dst))
                nlinks += 1
            npages += 1

    nraw = 0
    for p in (B / "raw").rglob("*.md"):
        r = parse(p)
        c.execute("INSERT INTO raw_fts VALUES(?,?,?)", (r["slug"], r["path"].split("/")[1], r["body"]))
        nraw += 1

    c.commit()
    c.close()
    print(f"built {DB.relative_to(B)}: {npages} pages, {nlinks} links, {nraw} raw items indexed")


if __name__ == "__main__":
    main()
