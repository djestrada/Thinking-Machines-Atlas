"""Build AI_arguments_table.xlsx from _out/table.json (assembled from content/)."""
import json, sys, os
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter

DATA = json.load(open("_out/table.json"))
OUT = sys.argv[1] if len(sys.argv) > 1 else "site/AI_arguments_table.xlsx"
FONT = "Arial"
NAVY, GREY = "1F3864", "7F7F7F"
FILLS = {"For": "E2EFDA", "Against": "FBE5D6", "Deflationary": "EDEDED"}
thin = Side(style="thin", color="BFBFBF")
BORDER = Border(left=thin, right=thin, top=thin, bottom=thin)
B = "• "

wb = Workbook()
wb.remove(wb.active)

def header(ws, cols, widths, color=NAVY, height=32):
    for j, (h, w) in enumerate(zip(cols, widths), start=1):
        c = ws.cell(row=1, column=j, value=h)
        c.font = Font(name=FONT, bold=True, color="FFFFFF", size=10)
        c.fill = PatternFill("solid", fgColor=color)
        c.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center")
        ws.column_dimensions[get_column_letter(j)].width = w
    ws.row_dimensions[1].height = height

def body(ws, i, vals, widths, bold_cols=(), fill=None, fill_cols=()):
    est = 1
    for j, v in enumerate(vals, start=1):
        c = ws.cell(row=i, column=j, value=v)
        c.font = Font(name=FONT, size=9, bold=(j in bold_cols))
        c.alignment = Alignment(wrap_text=True, vertical="top")
        c.border = BORDER
        if fill and j in fill_cols:
            c.fill = PatternFill("solid", fgColor=fill)
        cpl = max(8, int(widths[j - 1] * 1.15))
        est = max(est, sum(max(1, -(-len(p) // cpl)) for p in str(v or "").split("\n")))
    ws.row_dimensions[i].height = min(409, est * 12 + 6)

def bl(items):
    return "\n".join(B + x for x in items if x)

# ------------------------------------------------------------------ README
ws = wb.create_sheet("README")
ws.column_dimensions["A"].width = 130
r = 1
_RD = DATA["readme_new"] if "readme_new" in DATA else DATA["readme"]
if os.environ.get("BLIND") == "1":   # review copy: no model's AI on AI entries, no link to the live Atlas
    _RD = [l for l in _RD if not (isinstance(l, list) and isinstance(l[1], str) and l[1].startswith("Notes on current AI"))]
    for l in _RD:
        if isinstance(l, list) and isinstance(l[1], str):
            if l[1].startswith("AI on AI:"):
                l[1] = "AI on AI: in this review copy the tab holds only the empty template that each AI model fills in. No model’s entries are included."
            l[1] = l[1].replace("Thinking Machines Atlas, the interactive companion: https://djestrada.github.io/Thinking-Machines-Atlas/. Source files, corrections and suggestions: https://github.com/djestrada/Thinking-Machines-Atlas.", "Thinking Machines Atlas, the interactive companion, supplied with this workbook.")
for line in _RD:
    kind, txt = (line if isinstance(line, list) else ["text", line])
    c = ws.cell(row=r, column=1, value=txt)
    if kind == "title":
        c.font = Font(name=FONT, size=15, bold=True)
    elif kind == "head":
        c.font = Font(name=FONT, size=11, bold=True, color=NAVY)
    else:
        c.font = Font(name=FONT, size=10)
    c.alignment = Alignment(wrap_text=True, vertical="top")
    r += 1

# ------------------------------------------------------------------ cluster tabs
NOTES_TAB = DATA.get("notes_tab", False)
COLS = ["Group", "ID", "Stance", "Argument", "Target", "Scope", "Summary", "Summary checked?", "Original source", "Primary link",
        "Further reading", "Responses and objections"] + ([] if NOTES_TAB else ["Editorial note (Claude, unsourced)"]) + ["Related rows", "Family"]
WID = [18, 7, 12, 26, 16, 18, 58, 14, 46, 28, 46, 64] + ([] if NOTES_TAB else [36]) + [12, 24]
LINK_COL = COLS.index("Primary link") + 1
GROUP_TOP = Side(style="medium", color="1F3864")
FAMN = {f["key"]: f["key"] + " " + f["name"] for f in DATA.get("family_defs", [])}
clusters = DATA["clusters"]  # list of {key, tab, name, bracketed}
for cl in clusters:
    rows = sorted([x for x in DATA["rows"] if x["cluster"] == cl["key"]], key=lambda x: x.get("order", 999))
    ws = wb.create_sheet(cl["tab"])
    header(ws, COLS, WID, color=GREY if cl.get("bracketed") else NAVY)
    if cl.get("bracketed"):
        ws.sheet_properties.tabColor = "808080"
    for i, d in enumerate(rows, start=2):
        vals = ["", d["id"], d["stance"], d["arg"], d["target"], d["scope"], d["summary"], "Not yet checked against the source" if d["ver_status"][1].startswith("Paraphrase") else "Checked", d["orig"],
                d["link"], bl(d["further"]), bl(d["resp"])] + ([] if NOTES_TAB else [d.get("note", "")]) + [d.get("rel", ""), FAMN.get(d.get("family", ""), "")]
        body(ws, i, vals, WID, bold_cols=(3, 4), fill=FILLS.get(d["stance"]), fill_cols=(2, 3))
        if d["link"]:
            cell = ws.cell(row=i, column=LINK_COL)
            cell.hyperlink = d["link"]
            cell.font = Font(name=FONT, size=9, color="0563C1", underline="single")
    # Group column: one merged cell per run of rows sharing a thread
    start = 2
    for i in range(2, len(rows) + 3):
        cur = rows[i - 2].get("thread", "") if i - 2 < len(rows) else None
        prev = rows[start - 2].get("thread", "")
        if cur != prev:
            end = i - 1
            c = ws.cell(row=start, column=1, value=prev)
            c.font = Font(name=FONT, size=10, bold=True, color=NAVY)
            c.alignment = Alignment(wrap_text=True, vertical="top", horizontal="left")
            for k in range(start, end + 1):
                cell = ws.cell(row=k, column=1)
                cell.fill = PatternFill("solid", fgColor="DDEBF7")
                cell.border = Border(left=thin, right=thin,
                                     top=thin if k == start else Side(style=None),
                                     bottom=thin if k == end else Side(style=None))
            if end > start:
                ws.merge_cells(start_row=start, start_column=1, end_row=end, end_column=1)
                # openpyxl's merge re-formats the edges; reset them so no line falls inside the block
                ws.cell(row=start, column=1).border = Border(left=thin, right=thin, top=thin, bottom=Side(style=None))
                ws.cell(row=end, column=1).border = Border(left=thin, right=thin, top=Side(style=None), bottom=thin)
                for k in range(start + 1, end):
                    ws.cell(row=k, column=1).border = Border(left=thin, right=thin, top=Side(style=None), bottom=Side(style=None))
            start = i
    ws.freeze_panes = "E2"
    ws.auto_filter.ref = f"A1:{get_column_letter(len(COLS))}{len(rows) + 1}"
    ws.sheet_view.zoomScale = 90

# ------------------------------------------------------------------ generic table tabs
def table_tab(name, rows, widths, link_col=None):
    if not rows:
        return
    ws = wb.create_sheet(name)
    header(ws, rows[0], widths)
    for i, vals in enumerate(rows[1:], start=2):
        body(ws, i, vals, widths, bold_cols=(1,))
        if link_col is not None and vals[link_col]:
            c = ws.cell(row=i, column=link_col + 1)
            c.hyperlink = vals[link_col]
            c.font = Font(name=FONT, size=9, color="0563C1", underline="single")
    ws.freeze_panes = "B2"
    return ws

table_tab("Relations", DATA["relations"], [9, 36, 22, 9, 36, 60])
table_tab("Existing surveys", DATA["surveys"], [48, 18, 55, 55, 40, 36], link_col=4)
if DATA.get("show_drafts", True):
    table_tab("Kernel", DATA["kernel"], [10, 30, 70, 44, 64])
    table_tab("Families", DATA["families"], [30, 50, 62, 22, 56])


# ------------------------------------------------------------------ exchanges (from the Atlas data)
import os
AJ = os.environ.get("ATLAS_JSON", "site/data.json")
BLIND = os.environ.get("BLIND") == "1"
if os.path.exists(AJ):
    A = json.load(open(AJ)); RR = {r["id"]: r for r in A["rows"]}
    ws = wb.create_sheet("Exchanges")
    EC = ["Cluster", "Exchange", "#", "Side", "Move type", "ID", "Argument or move", "What the move says (paraphrase)", "Answers"]
    EW = [9, 30, 5, 11, 20, 8, 34, 70, 22]
    header(ws, EC, EW)
    SIDE = {"A": "Affirms", "D": "Denies", "M": "Reframes"}
    i = 2
    for cl in clusters:
        for xi, x in enumerate(A["ex"].get(cl["key"], []), start=1):
            num = {m["key"]: n for n, m in enumerate(x["moves"], start=1)}
            body(ws, i, [cl["key"], f"{xi}. {x['title']}", "", "", "", "", "Contested claim", x["claim"], ""], EW, bold_cols=(2, 7, 8), fill="DDEBF7", fill_cols=tuple(range(1, 10)))
            i += 1
            for n, m in enumerate(x["moves"], start=1):
                to = m.get("to", "claim"); tk = to.split(":")[0]
                ans = "the claim" if to == "claim" else (f"move {num[tk]}" + (f" ({to.split(':')[1]})" if ":" in to else ""))
                if m.get("groups"):
                    gist = "\n".join(f"{g['label']}: " + "; ".join(f"{it['id']} {RR[it['id']]['a']} (reply: {it['reply']})" for it in g["items"]) for g in m["groups"])
                    name = m.get("title", "")
                else:
                    gist = m.get("gist", ""); name = RR[m["id"]]["a"] if m.get("id") else m.get("label", "")
                fill = {"A": "E2EFDA", "D": "FBE5D6", "M": "EDEDED"}[m["side"]]
                body(ws, i, ["", "", n, SIDE[m["side"]], m["type"], m.get("id", ""), name, gist, ans], EW, bold_cols=(7,), fill=fill, fill_cols=(4,))
                i += 1
            body(ws, i, ["", "", "", "", "", "", "Where it stands", x["stands"], ""], EW, bold_cols=(7,))
            i += 1
            body(ws, i, ["", "", "", "", "", "", "Where it goes next", "\n".join(f"{p['id']} {RR[p['id']]['a']} ({p['why']})" for p in x["passes"]), ""], EW, bold_cols=(7,))
            i += 2
    ws.freeze_panes = "C2"


# ------------------------------------------------------------------ AI on AI: every model in one tab, same columns, alphabetical
if os.path.exists(AJ) and A.get("models"):
    ws = wb.create_sheet("AI on AI")
    OC = ["Model", "Cluster", "The question, for systems like me", "Strongest", "Least convincing", "Where it lands", "What follows if the strongest go through", "Why the strongest", "Why the least convincing"]
    OW = [12, 10, 34, 34, 30, 60, 48, 52, 52]
    header(ws, OC, OW)
    i = 2
    for m in A["models"]:
        about = (f"{m['name']} ({m['maker']}), collected {m['collected']}. {m['method']}" if m["key"] != "template" else m["method"])
        body(ws, i, [m["name"], "About", "", "", "", about, m["intro"], "", ""], OW, bold_cols=(1,), fill="E9EDF2", fill_cols=tuple(range(1, 10)))
        i += 1
        for a in m["rows"]:
            nm = lambda ids: "\n".join(f"{x} {RR[x]['a']}" for x in ids)
            pk = lambda ids, note: "\n".join(x for x in [nm(ids), note or ""] if x)
            cl = "Overall" if a["k"] == "all" else a["k"]
            if m["key"] == "template":
                body(ws, i, ["", cl, "", "", "", "", "", "", ""], OW, bold_cols=(2,))
            else:
                body(ws, i, [m["name"], cl, a["q"], pk(a["strong"], a.get("strong_note")), pk(a["weak"], a.get("weak_note")), a["land"], a["follow"], a["strong_txt"], a["weak_txt"]], OW, bold_cols=(1,))
            i += 1
        i += 1
    ws.freeze_panes = "C2"

# ------------------------------------------------------------------ teaching notes (Claude's unsourced remarks)
if NOTES_TAB and not BLIND:
    ws = wb.create_sheet("Notes on current AI")
    i = 0
    # row remarks
    i += 1
    c = ws.cell(row=i, column=1, value="Remarks on how individual rows bear on current AI (written by Claude, unsourced)")
    c.font = Font(name=FONT, size=12, bold=True, color="1F3864")
    i += 1
    for j, h in enumerate(["ID", "Argument", "Remark on current AI (Claude, unsourced)"], start=1):
        c = ws.cell(row=i, column=j, value=h)
        c.font = Font(name=FONT, bold=True, color="FFFFFF", size=10)
        c.fill = PatternFill("solid", fgColor="1F3864")
    ws.merge_cells(start_row=i, start_column=3, end_row=i, end_column=6)
    i += 1
    for cl in clusters:
        for d in sorted([x for x in DATA["rows"] if x["cluster"] == cl["key"]], key=lambda x: x.get("order", 999)):
            if d.get("note"):
                body(ws, i, [d["id"], d["arg"], d["note"]], [20, 30, 200], bold_cols=(1,))
                ws.merge_cells(start_row=i, start_column=3, end_row=i, end_column=6)
                i += 1
    ws.freeze_panes = "A3"

# ------------------------------------------------------------------ verification status and changelog
ws = wb.create_sheet("Verification")
VC = ["ID", "Argument", "Sources", "Summary", "Primary link", "Outstanding"]
VW = [8, 34, 40, 46, 40, 30]
header(ws, VC, VW)
i = 2
for cl in clusters:
    for d in sorted([x for x in DATA["rows"] if x["cluster"] == cl["key"]], key=lambda x: x.get("order", 999)):
        st = d.get("ver_status") or ["", "", "", ""]
        body(ws, i, [d["id"], d["arg"], st[0], st[1], st[2], st[3]], VW, bold_cols=(1,))
        i += 1
ws.freeze_panes = "C2"
if DATA.get("changelog"):
    table_tab("Changelog", DATA["changelog"], [16, 120])

wb.save(OUT)
print("built", OUT, [s.title for s in wb.worksheets])
