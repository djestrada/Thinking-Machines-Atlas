"""Assemble atlas/index.html from index_src.html and the cluster-map code in oldmap.js."""
s = open("build/index_src.html").read()
old = open("build/oldmap.js").read().replace('  drawLocator(svg, k, CM.right + 6, 16, 270, others);\n', '').replace('const CM = { W: 1290,', 'const CM = { W: 1020,') \
    .replace('if (state.view === "overview" || !CM.nodeEls) return;', 'if (state.view === "overview" || !CM.nodeEls || D.ex[state.view.slice(1)]) return;')
open("site/index.html", "w").write(s.replace('/*OLDMAP*/', old))
