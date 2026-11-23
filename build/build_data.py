"""Build site/data.json from _out/table.json (assembled from content/) plus the editorial spine (overview), Guide and exchanges (cluster views)."""
import json, re, os, glob, yaml
def load(p): return yaml.safe_load(open(p, encoding="utf-8"))
D = json.load(open("_out/table.json"))
R = {r["id"]: r for r in D["rows"]}

SHORT = load("content/atlas/short_names.yaml")
def short(a, rid=None):
    if rid in SHORT: return SHORT[rid]
    a = re.sub(r"\s*\([^)]*\)", "", a).strip()
    return a if len(a) <= 34 else a[:33].rsplit(" ", 1)[0] + "…"

# ---------------- overview, exchanges and Guide: edited in content/atlas/ ----------------
SPINE = load("content/atlas/overview.yaml")
X = {}
for p in sorted(glob.glob("content/atlas/exchanges/*.yaml")):
    X[str(int(os.path.basename(p)[:-5]))] = load(p)

# ---------------- AI on AI (Claude's assessment), from the workbook tab ----------------
LEGACY = load("content/ai_on_ai_legacy.yaml")
PICKS = {k: (v["strong"], v["weak"]) for k, v in LEGACY["picks"].items()}
AION = []
for row in D["ai_on_ai"][1:]:
    k = "all" if row[0].startswith("Overall") else row[0].split(".")[0]
    s, w = PICKS[k]
    assert all(i in R for i in s + w)
    AION.append(dict(k=k, q=row[1], strong_txt=row[2], weak_txt=row[3], land=row[4], follow=row[5], strong=s, weak=w))
AION_INTRO = D["ai_on_ai_intro"][1]
MODELS = [] if os.path.exists("content/ai_models/claude.json") else [dict(key="claude", name="Claude", maker="Anthropic", collected="19 November 2026", collected_by="Daniel Estrada",
               method="Written by Claude while building the Atlas, with the whole table in view. Claude made the map, so its picks also shaped how the arguments are presented.",
               intro=AION_INTRO, rows=AION)]
for p in sorted(glob.glob("content/ai_models/*.json")):
    m = json.load(open(p))
    for row in m["rows"]:
        assert row["k"] in PICKS, (p, row["k"])
        for i in row["strong"] + row["weak"]:
            assert i in R, (p, i)
    MODELS.append(m)
MODELS.sort(key=lambda m: m["name"].lower())   # alphabetical: no model is listed first by default
BLIND = os.environ.get("BLIND") == "1"
if BLIND:   # review copy: no model's entries, an empty template in their place
    CL = {c["key"]: c["name"] for c in D["clusters"]}
    MODELS = [dict(key="template", name="[Model name]", maker="—", collected="—", collected_by="",
                   method="This copy of the Atlas has no AI model’s entries. The rows below are the empty template each model fills in.",
                   intro="[A short note, in the first person: who you are, and how far your judgments may reflect your training and your maker.]",
                   rows=[dict(k=k, q="[The question this cluster asks, for systems like you]", strong=[], weak=[],
                              strong_note="[The arguments you find strongest, by ID]", weak_note="[The arguments you find least convincing, by ID]",
                              land="[Where you land]", follow="[What follows if the strongest arguments go through]",
                              strong_txt="[Why these are strongest]", weak_txt="[Why these are least convincing]") for k in list(CL) + ["all"]])]
    AION = []
    AION_INTRO = ""   # nothing from any model's entry in the review copy


GUIDE = load("content/atlas/guide.yaml")
# checks
def ids_in(x):
    out = []
    for m in x["moves"]:
        if m.get("id"): out.append(m["id"])
        for g in m.get("groups", []):
            out += [i["id"] for i in g["items"]]
    return out
for k, exs in X.items():
    cov = [i for x in exs for i in ids_in(x)]
    allc = sorted(r["id"] for r in D["rows"] if r["cluster"] == k)
    missing = set(allc) - set(cov)
    if missing: raise SystemExit(f"content/atlas/exchanges/{int(k):02d}.yaml: rows not in any exchange: {sorted(missing)}")
    for x in exs:
        keys = {m["key"] for m in x["moves"]} | {"claim"} | {f"obj:{i['id']}" for m in x["moves"] for g in m.get("groups", []) for i in g["items"]}
        for m in x["moves"]:
            if m.get("id") and m["id"] not in R: raise SystemExit(f"exchange '{x['title']}': unknown row {m['id']}")
            if m["to"] not in keys: raise SystemExit(f"exchange '{x['title']}', move {m['key']}: 'to' names no move ({m['to']})")
        for p in x["passes"]:
            if p["id"] not in R: raise SystemExit(f"exchange '{x['title']}': hand-off to unknown row {p['id']}")
for s in SPINE:
    for l in s.get("lanes", []) or []:
        bad = [i for i in l["ids"] if i not in R]
        if bad: raise SystemExit(f"content/atlas/overview.yaml, {s['key']} lane '{l['label']}': unknown rows {bad}")
    for r in s.get("rungs", []) or []:
        bad = [i for i in (r.get("pro") or []) + r["yes"] + r["no"] if i not in R]
        if bad: raise SystemExit(f"content/atlas/overview.yaml, rung '{r['label']}': unknown rows {bad}")

out = dict(
 clusters=[dict(k=c["key"], tab=c["tab"], name=c["name"], q=c.get("question", "")) for c in D["clusters"]],
 rows=[dict(id=r["id"], c=r["cluster"], g=r["thread"], o=r.get("order", 99), s=r["stance"], a=r["arg"], sh=short(r["arg"], r["id"]), t=r["target"], sc=r["scope"],
            sum=r["summary"], orig=r["orig"], link=r["link"], f=r["family"], chk=0 if r["ver_status"][1].startswith("Paraphrase") else 1) for r in D["rows"]],
 rel=[dict(a=r[0], r=r[2], b=r[3], n=r[5]) for r in D["relations"][1:]],
 fam=D["family_defs"], kernel=D["kernel_defs"], spine=SPINE, ex=X, aion=AION, aion_intro=AION_INTRO, models=MODELS, guide=GUIDE)
s = json.dumps(out, ensure_ascii=False, separators=(",", ":"))
open("_out/data_blind.json" if BLIND else "site/data.json", "w").write(s)
print("data.json", len(s), "bytes")
