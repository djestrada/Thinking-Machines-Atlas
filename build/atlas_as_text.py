"""Plain-text version of the Atlas diagram (overview and exchanges), for reviewers whose file readers cannot take the full HTML."""
import json, sys
D = json.load(open(sys.argv[1])); out = sys.argv[2]
R = {r["id"]: r for r in D["rows"]}
nm = lambda i: f"{i} {R[i]['a']} [{R[i]['s']}]"
L = ["# Thinking Machines Atlas: the diagram as text", "",
     "Created and edited by Daniel Estrada (NJIT). Drafted and built with Claude (Anthropic). This file reproduces the structure of the interactive Atlas: "
     "the overview (five questions, Q0 to Q4, with each argument placed under the answer it gives) and the exchanges for each cluster. "
     "Argument IDs match the workbook, which has the summaries and sources. Stance in brackets is relative to the cluster's question: For, Against or Deflationary.", "",
     "## Part A. The overview", ""]
for s in D["spine"]:
    L += [f"### {s['key']}. {s['q']}", "", s["lede"], ""]
    if "gate" in s:
        g = s["gate"]; L += [f"**{g['label']}**", f"- No, in principle: " + "; ".join(nm(i) for i in g["no"]), f"- Possible, but feasible? (practical limits): " + "; ".join(nm(i) for i in g.get("practice", [])), f"- Yes: " + "; ".join(nm(i) for i in g["yes"])]
        if g.get("note"): L.append(f"- Note: {g['note']}")
        if g.get("reply"): L.append(f"- {g['reply']}")
        L += ["", f"**The ladder** (rungs from thin to thick). For each rung: arguments that propose it ({s.get('pro_label','proposes')}); "
                  f"that say machines can meet it ({s.get('yes_label','yes')}); that say they cannot ({s.get('no_label','no')}).", ""]
        for n, r in enumerate(s["rungs"], 1):
            if r.get("step"): L.append(f"   *Step from rung {n-1}:* {r['step']}")
            L.append(f"{n}. **{r['label']}.** {r['why']}")
            for jp in r.get("jumps", []): L.append(f"   - {'Jump ahead' if jp['to'] > n else 'Back'} to rung {jp['to']}: {jp['text']}")
            for lab, key in (("Proposes it", "pro"), ("Machines can meet it", "yes"), ("Machines cannot", "no")):
                if r[key]: L.append(f"   - {lab}: " + "; ".join(nm(i) for i in r[key]))
        L.append("")
    for ln in s.get("lanes", []):
        L.append(f"- **{ln['label']}**" + (f" ({ln['note']})" if ln.get("note") else ""))
        for i in ln["ids"]: L.append(f"  - {nm(i)}")
    if s.get("next"): L += ["", f"*Connector to the next question:* {s['next']}"]
    L.append("")
SIDE = {"A": "Affirms", "M": "Reframes", "D": "Denies"}
L += ["## Part B. The exchanges, cluster by cluster", "",
      "Each exchange has a contested claim and numbered moves. Side: Affirms the claim, Reframes it, or Denies it. 'Answers' names what the move responds to. "
      "The stance in brackets is the argument's stance on its cluster's question in the workbook; the side is its role in this exchange, so the two can differ "
      "(for example, connectionism is For machine minds but Denies that thinking is symbol manipulation).", ""]
for c in D["clusters"]:
    for x, e in enumerate(D["ex"].get(c["k"], []), 1):
        L += [f"### Cluster {c['name']}: exchange {x}. {e['title']}", "", f"**Contested claim:** {e['claim']}", ""]
        keyid = {m["key"]: (m["id"] if m.get("id") in R and not m.get("label") else f"move {n}") for n, m in enumerate(e["moves"], 1)}
        for n, m in enumerate(e["moves"], 1):
            to = "the claim" if m["to"] == "claim" else (m["to"][4:] if m["to"].startswith("obj:") else keyid.get(m["to"], m["to"]))
            who = nm(m["id"]) if m.get("id") in R else (m.get("label") or m.get("title") or "")
            line = f"{n}. {SIDE.get(m['side'], m['side'])}, {m.get('type','')}: {who}."
            if m.get("gist"): line += f" {m['gist']}"
            L.append(line + f" (Answers: {to})")
            for g in m.get("groups", []):
                L.append(f"   - {g['label']}:")
                for it in g["items"]:
                    L.append(f"     - {nm(it['id'])}: Turing's reply: {it['reply']}" + (f" (carried on in {', '.join(it['pass_'])})" if it.get("pass_") else ""))
        L += ["", f"**Where it stands:** {e['stands']}", ""]
        if e.get("passes"): L += ["**Where the argument goes next:** " + "; ".join(f"{p['id']} ({p['why']})" for p in e["passes"]), ""]
open(out, "w").write("\n".join(L)); print(len("\n".join(L)), "chars")
