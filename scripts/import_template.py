"""Import a model's AI on AI answers written in the template (a markdown table with 6 columns).
Usage: import_template.py SRC OUT key name maker method [drop=k:id,...]
Picks are the argument IDs named in the strongest / least-convincing columns; 'drop' removes IDs that are
mentioned in a column without being picks (e.g. cited as support)."""
import json, re, sys
src, out, key, name, maker, method = sys.argv[1:7]
drop, add = {}, {}
for a in sys.argv[7:]:
    for tag, store in (("drop=", drop), ("addweak=", add), ("addstrong=", add)):
        if a.startswith(tag):
            for kv in a[len(tag):].split(","):
                k, i = kv.split(":"); store.setdefault((tag[:-1] if tag != "drop=" else "drop", k), []).append(i)
t = open(src, encoding="utf-8").read()
intro = re.search(r"^\*(As .+?|Written .+?|I am .+?|[A-Z][^*]{40,})\*\s*$", t, re.M).group(1).strip()
ids = lambda s: list(dict.fromkeys(re.findall(r"\b(\d{1,2}\.\d{2})\b", s)))
rows = []
for line in t.splitlines():
    if not line.startswith("| **") or "| | | |" in line: continue
    c = [x.strip() for x in line.strip().strip("|").split("|")]
    lab = c[0].strip("*")
    k = "all" if lab.startswith("Overall") else lab.split(".")[0]
    d = set(drop.get(("drop", k), []))
    st = [i for i in ids(c[2]) if i not in d] + add.get(("addstrong", k), [])
    wk = [i for i in ids(c[3]) if i not in d] + add.get(("addweak", k), [])
    notes = dict(strong_note="" if st else c[2], weak_note="" if wk else c[3])   # a column naming no entries keeps its words in place of chips
    rows.append(dict(k=k, q=c[1], strong=st, weak=wk, **notes,
                     strong_txt=c[2], weak_txt=c[3], land=c[4], follow=c[5]))
m = dict(key=key, name=name, maker=maker, collected=__import__("os").environ.get("COLLECTED", __import__("datetime").date.today().strftime("%-d %B %Y")), collected_by="Daniel Estrada", method=method, intro=intro, rows=rows)
json.dump(m, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for r in rows: print(r["k"], r["strong"], "|", r["weak"])
