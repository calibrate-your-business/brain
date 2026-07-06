#!/usr/bin/env python3
"""Routing mechanic (NOT understanding): cluster raw bookmarks into theme
digests so each compile agent reads one high-signal file, not 600 files.
Uses the existing (regex) enrichment tags purely to ROUTE; the agents do the
synthesis. Caps each theme to top-N by engagement to keep digests readable.
"""
import json
from pathlib import Path

import os
XB = Path(os.environ.get("XBM_DATA", os.path.expanduser("~/Claude/brain-db/data/x-bookmarks")))
DIG = Path(__file__).resolve().parent / "digests"
DIG.mkdir(parents=True, exist_ok=True)

enr = json.load(open(XB / "xbm_enriched.json"))
enrich = json.load(open(XB / "xbm_enrichment.json"))

THEMES = {
 "anthropic-claude-mcp": ["claude","anthropic","mcp","prompt-cach","context-window","artifact"],
 "agent-engineering": ["agent","orchestrat","subagent","multi-agent","sandbox","model-rout","tool-use","agent-loop","autonomous","fine-tun","eval"],
 "second-brain-pkm": ["obsidian","notion","karpathy","knowledge","second-brain","vault","rag","memory","note","zettel"],
 "ai-models-platforms": ["openai","chatgpt"," gpt","gemini","cursor","kimi","deepseek","grok"," llm","copilot","windsurf"],
 "dev-coding": ["github","docker","postgres","supabase","react","next.js","nextjs","typescript","python"," go ","coding","kubernetes","terraform","api"],
 "business-solo-operator": ["business-startup","agency","founder","cold-email","productivity","startup","saas","one-person","revenue","marketing"],
}

def tagtext(bid):
    e = enrich.get(bid, {}); parts = []
    for k in ("topics","techniques","tools","entities"):
        v = e.get(k)
        parts += v if isinstance(v, list) else ([v] if v else [])
    return " ".join(str(p).lower() for p in parts)

theme_items = {t: [] for t in THEMES}; theme_items["long-tail"] = []
people = {}
for bid, b in enr.items():
    f = b.get("focal", {}); author = f.get("author"); text = f.get("text") or ""
    likes = int((f.get("metrics") or {}).get("likes") or 0)
    people[author] = people.get(author, 0) + 1
    blob = (tagtext(bid) + " " + text.lower())
    hit = False
    for t, kws in THEMES.items():
        if any(kw in blob for kw in kws):
            theme_items[t].append((bid, author, text, likes)); hit = True
    if not hit:
        theme_items["long-tail"].append((bid, author, text, likes))

manifest = {}
for t, items in theme_items.items():
    items.sort(key=lambda x: -x[3])
    cap = items[:90]
    out = [f"# digest: {t} -- {len(items)} items, top {len(cap)} by likes shown\n"]
    for bid, author, text, likes in cap:
        out.append(f"### {bid} @{author} ({likes} likes)\n{text}\n")
    (DIG / f"{t}.md").write_text("\n".join(out), encoding="utf-8")
    manifest[t] = len(items)

# people: top accounts + sample saves (for influencer entity pages)
top = sorted(people.items(), key=lambda x: -x[1])[:25]
out = ["# digest: people -- top accounts Karim follows (for entity pages)\n"]
for author, cnt in top:
    out.append(f"## @{author} ({cnt} bookmarks)")
    n = 0
    for bid, b in enr.items():
        f = b.get("focal", {})
        if f.get("author") == author and n < 6:
            out.append(f"- {bid}: {(f.get('text') or '')[:150]}"); n += 1
    out.append("")
(DIG / "people.md").write_text("\n".join(out), encoding="utf-8")
manifest["people(top authors)"] = [a for a, _ in top]

json.dump(manifest, open(DIG.parent / "manifest.json", "w"), indent=2)
print(json.dumps(manifest, indent=2))
print("\ndigest sizes:")
for p in sorted(DIG.glob("*.md")):
    print(f"  {p.name}: {p.stat().st_size//1024}K")
