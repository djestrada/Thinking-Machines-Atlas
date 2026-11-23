"""Assemble _out/table.json from the files in content/ (the single source)."""
import json, yaml, glob, os
os.makedirs("_out", exist_ok=True)
def load(p): return yaml.safe_load(open(p, encoding="utf-8"))
key = lambda s: tuple(int(p) for p in s.split("."))
rows = [load(p) for p in glob.glob("content/rows/*/*.yaml")]
rows.sort(key=lambda r: (int(r["cluster"]), r.get("order", 999), key(r["id"])))
R = {r["id"]: r for r in rows}
errors = []
ids = [r["id"] for r in rows]
if len(ids) != len(set(ids)): errors.append("duplicate row IDs")
for p in glob.glob("content/rows/*/*.yaml"):
    r = load(p); folder = p.split(os.sep)[-2]; stem = os.path.basename(p)[:-5]
    if r["id"] != stem or r["cluster"] != folder: errors.append(f"{p}: id/cluster do not match the file name and folder")
    if r["stance"] not in ("For", "Against", "Deflationary"): errors.append(f"{p}: stance must be For, Against or Deflationary")
rels = load("content/relations.yaml")
for x in rels:
    for k in ("source", "target"):
        if x[k] not in R: errors.append(f"relations.yaml: unknown row {x[k]}")
P = load("content/project.yaml")
fams = {f["key"] for f in P["family_defs"]}
for r in rows:
    if r.get("family") and r["family"] not in fams: errors.append(f"{r['id']}: unknown family {r['family']}")
    for s in r.get("see_also") or []:
        if s not in R: errors.append(f"{r['id']}: see_also names unknown row {s}")
if errors:
    raise SystemExit("Content errors:\n  " + "\n  ".join(errors))
nb = {k: set() for k in R}
for x in rels: nb[x["source"]].add(x["target"]); nb[x["target"]].add(x["source"])
out_rows = []
for r in rows:
    r = dict(r); extra = r.pop("see_also") or []
    r["rel"] = ", ".join(sorted(nb[r["id"]] | set(extra), key=key))
    out_rows.append(r)
D = dict(rows=out_rows)
D["families"] = load("content/families.yaml"); D["kernel"] = load("content/kernel.yaml")
D["relations"] = [["From ID", "From argument", "Relation", "To ID", "To argument", "Note"]] + \
    [[x["source"], R[x["source"]]["arg"], x["relation"], x["target"], R[x["target"]]["arg"], x["note"]] for x in rels]
D["surveys"] = load("content/surveys.yaml"); D["readme"] = load("content/readme.yaml")
D.update({k: P[k] for k in ("fam_map", "clusters", "notes_tab", "show_drafts")})
D["readme_new"] = load("content/readme_new.yaml")
L = load("content/ai_on_ai_legacy.yaml"); D["ai_on_ai_intro"] = L["intro"]; D["ai_on_ai"] = L["rows"]
D.update({k: P[k] for k in ("family_defs", "kernel_defs", "relation_chronology_fixes")})
D["changelog"] = load("content/changelog.yaml")
json.dump(D, open("_out/table.json", "w"), ensure_ascii=False, indent=1)
print(f"assembled {len(out_rows)} rows, {len(rels)} relations")
