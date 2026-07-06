#!/usr/bin/env python3
"""Query the brain's derived indexes (db/brain.db). This is how Claude (and
Karim) retrieve from the brain -- use this instead of scanning files.

  query.py search "<terms>" [--context X] [--raw] [--limit N]
  query.py links <slug>          # forward links + backlinks (graph)
  query.py orphans               # lint: pages nothing links to
  query.py broken                # lint: [[links]] that resolve to no page
  query.py page <slug>           # the file path for a page
"""
import os, re, sqlite3, sys
from pathlib import Path

# DATA lives in the private brain-db repo; this script is the brain SYSTEM.
# Override the data dir with BRAIN_DB (default ~/Claude/brain-db).
B = Path(os.environ.get("BRAIN_DB") or (Path.home() / "Claude" / "brain-db"))
DB = B / "db" / "brain.db"


def conn():
    if not DB.exists():
        sys.exit("no index; run db/build_index.py first")
    return sqlite3.connect(DB)


def norm(s):
    return s.lower().strip().replace(" ", "-")


def search(terms, context=None, raw=False, limit=10):
    c = conn()
    if raw:
        rows = c.execute(
            "SELECT id, source, snippet(raw_fts,2,'[',']','...',12) FROM raw_fts "
            "WHERE raw_fts MATCH ? ORDER BY rank LIMIT ?", (terms, limit)).fetchall()
        for rid, src, snip in rows:
            print(f"  raw/{src} {rid}: {snip.strip()[:140]}")
        return
    q = ("SELECT f.slug, p.title, p.type, p.contexts, snippet(pages_fts,2,'[',']','...',12) "
         "FROM pages_fts f JOIN pages p ON p.slug=f.slug WHERE pages_fts MATCH ?")
    args = [terms]
    if context:
        q += " AND p.contexts LIKE ?"
        args.append(f"%{context}%")
    q += " ORDER BY rank LIMIT ?"
    args.append(limit)
    for slug, title, typ, ctx, snip in c.execute(q, args).fetchall():
        print(f"  [{typ}] {title} ({slug}) [{ctx}]\n      {snip.strip()[:160]}")


def links(slug):
    c = conn()
    fwd = [r[0] for r in c.execute("SELECT dst FROM links WHERE src=?", (slug,))]
    # backlinks: any page whose link target resolves to this slug/title
    title = c.execute("SELECT title FROM pages WHERE slug=?", (slug,)).fetchone()
    keys = {norm(slug)} | ({norm(title[0])} if title else set())
    back = sorted({s for (s, d) in c.execute("SELECT src,dst FROM links") if norm(d) in keys})
    print(f"forward ({len(fwd)}): " + ", ".join(sorted(set(fwd))[:40]))
    print(f"backlinks ({len(back)}): " + ", ".join(back[:40]))


def _resolvable():
    c = conn()
    s = set()
    for slug, title, aliases in c.execute("SELECT slug,title,aliases FROM pages"):
        s.add(norm(slug)); s.add(norm(title))
        for a in (aliases or "").split(","):
            if a.strip():
                s.add(norm(a))
    return c, s


def orphans():
    c, _ = _resolvable()
    targets = {norm(d) for (d,) in c.execute("SELECT DISTINCT dst FROM links")}
    rows = c.execute("SELECT slug,title,type FROM pages").fetchall()
    orphan = [(s, t, ty) for (s, t, ty) in rows if norm(s) not in targets and norm(t) not in targets]
    print(f"orphans ({len(orphan)} pages nothing links to):")
    for s, t, ty in orphan:
        print(f"  [{ty}] {t} ({s})")


def broken():
    c, slugs = _resolvable()
    cnt = {}
    for (d,) in c.execute("SELECT dst FROM links"):
        if d.lower().startswith("raw/") or d.upper() == "PROFILE":
            continue
        if norm(d) not in slugs:
            cnt[d] = cnt.get(d, 0) + 1
    print(f"broken/forward-only link targets ({len(cnt)}):")
    for d, n in sorted(cnt.items(), key=lambda x: -x[1]):
        print(f"  [[{d}]] x{n}")


def page(slug):
    c = conn()
    r = c.execute("SELECT path FROM pages WHERE slug=?", (slug,)).fetchone()
    print(str(B / r[0]) if r else "not found")


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a:
        sys.exit(__doc__)
    cmd = a[0]
    if cmd == "search":
        ctx = a[a.index("--context") + 1] if "--context" in a else None
        lim = int(a[a.index("--limit") + 1]) if "--limit" in a else 10
        terms = a[1]
        search(terms, ctx, "--raw" in a, lim)
    elif cmd == "links":
        links(a[1])
    elif cmd == "orphans":
        orphans()
    elif cmd == "broken":
        broken()
    elif cmd == "page":
        page(a[1])
    else:
        sys.exit(__doc__)
