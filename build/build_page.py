"""Assemble the Atlas page from index_src.html and the cluster-map code in oldmap.js.
Writes _out/index_fragment.html (the page body, used for the single-file copy) and
site/index.html (a complete document, with doctype and viewport, for GitHub Pages)."""
s = open("build/index_src.html").read()
old = open("build/oldmap.js").read().replace('  drawLocator(svg, k, CM.right + 6, 16, 270, others);\n', '').replace('const CM = { W: 1290,', 'const CM = { W: 1020,') \
    .replace('if (state.view === "overview" || !CM.nodeEls) return;', 'if (state.view === "overview" || !CM.nodeEls || D.ex[state.view.slice(1)]) return;')
frag = s.replace('/*OLDMAP*/', old)
open("_out/index_fragment.html", "w").write(frag)

def document(html):
    """Wrap the fragment in a full document: head tags before the first <style> block's end go in <head>."""
    head, rest = html.split("<style>", 1)
    style, body = rest.split("</style>", 1)
    meta = ('<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
            '<meta name="description" content="A teaching map of the debate over whether machines can think, understand, feel, act or matter morally.">\n'
            '<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 32 32%22%3E%3Crect width=%2232%22 height=%2232%22 rx=%226%22 fill=%22%231f3864%22/%3E%3Cpath d=%22M9 23V9h4l3 7 3-7h4v14%22 stroke=%22white%22 stroke-width=%222.5%22 fill=%22none%22/%3E%3C/svg%3E">\n')
    return ('<!doctype html>\n<html lang="en">\n<head>\n' + meta + head.replace('<meta name="claude:viewport-fit-sides" content="cover">\n', '')
            + "<style>" + style + "</style>\n</head>\n<body>\n" + body + "\n</body>\n</html>\n")
open("site/index.html", "w").write(document(frag))
