function defsArrows(svg) {
  const defs = el("defs", {}, svg);
  ["oppose", "respond", "build", "parallel"].forEach(c => {
    const m = el("marker", { id: "ar-" + c, viewBox: "0 0 10 10", refX: 9, refY: 5, markerWidth: 7, markerHeight: 7, orient: "auto-start-reverse" }, defs);
    el("path", { d: "M0,0 L10,5 L0,10 z", fill: `var(--e-${c})` }, m);
  });
}
function legendEl(withEdges = true) {
  const lg = h("div", { className: "legend" });
  lg.innerHTML = Object.entries(ST).map(([k, v]) => `<span><i class="dot" style="background:${v}"></i>${k}</span>`).join("") +
    (withEdges ? Object.entries(CATN).map(([k, v]) => `<span><i class="ln" style="border-color:var(--e-${k});${k === "parallel" ? "border-top-style:dashed" : ""}"></i>${v}</span>`).join("") : "") +
    `<span style="margin-left:auto">${withEdges ? "Chips inside a box are links to other clusters, in that cluster’s colour." : "Line width: number of links between two clusters."}</span>`;
  return lg;
}

/* ---------------- cluster map ---------------- */
const CM = { W: 1290, label: [16, 170], cols: { For: 196, Deflationary: 466, Against: 736 }, colW: 240, right: 1010 };
function drawCluster(main, k) {
  const c = D.clusters.find(x => x.k === k);
  main.innerHTML = "";
  const others = D.rel.filter(e => (R[e.a].c === k) !== (R[e.b].c === k));
  main.appendChild(h("div", { className: "plate-head" },
    `<h2><span style="color:${hue(k)};font-family:var(--mono);font-weight:500">${k}</span>&nbsp; ${esc(c.name.replace(/^\d+\.\s*/, ""))}</h2>
     <span class="sub">${byC[k].length} arguments in ${groupsOf(k).length} groups; ${D.rel.filter(e => R[e.a].c === k && R[e.b].c === k).length} links within the cluster and ${others.length} to other clusters. Click a box for its summary and links.</span>`));
  const sc = h("div", { className: "scroll" }); main.appendChild(sc);

  // measure nodes
  const LINE = 32;
  const nodes = {};
  byC[k].forEach(r => {
    const lines = wrap(r.a, LINE);
    const outs = D.rel.filter(e => (e.a === r.id && R[e.b].c !== k) || (e.b === r.id && R[e.a].c !== k)).map(e => e.a === r.id ? e.b : e.a);
    const uniq = [...new Set(outs)];
    const chipRows = Math.ceil(uniq.length / 4);
    nodes[r.id] = { r, lines, outs: uniq, hgt: 24 + lines.length * 15 + (chipRows ? chipRows * 21 + 2 : 0) + 6 };
  });
  // bands
  let y = 44; const bands = [];
  groupsOf(k).forEach(([g, rs]) => {
    const colY = { For: 0, Deflationary: 0, Against: 0 }; const items = [];
    rs.forEach(r => { const n = nodes[r.id]; n.x = CM.cols[r.s]; n.y = y + 14 + colY[r.s]; colY[r.s] += n.hgt + 12; items.push(n); });
    const labLines = wrap(g, 22);
    const bh = Math.max(...Object.values(colY), labLines.length * 16 + 10) + 16;
    bands.push({ g, y, h: bh, labLines }); y += bh + 8;
  });
  const H = Math.max(y + 10, 470);
  const svg = el("svg", { viewBox: `0 0 ${CM.W} ${H}`, width: "100%", role: "img", "aria-label": `Map of cluster ${k}` });
  svg.style.minWidth = "980px"; sc.appendChild(svg); defsArrows(svg);
  // column heads
  Object.entries(CM.cols).forEach(([s, x]) => {
    el("rect", { x, y: 16, width: CM.colW, height: 4, rx: 2, fill: ST[s] }, svg);
    const t = el("text", { x, y: 36, "font-size": 13.5, "font-weight": 600, fill: ST[s] }, svg); t.textContent = s;
  });
  bands.forEach((b, i) => {
    el("rect", { x: 8, y: b.y, width: CM.right - 22, height: b.h, rx: 5, fill: i % 2 ? "transparent" : "var(--band)" }, svg);
    b.labLines.forEach((s, j) => { const t = el("text", { x: CM.label[0], y: b.y + 24 + j * 16, "font-size": 13, "font-weight": 600, fill: "var(--accent)" }, svg); t.textContent = s; });
  });
  const gE = el("g", {}, svg), gN = el("g", {}, svg);
  // intra edges
  const intra = D.rel.filter(e => R[e.a].c === k && R[e.b].c === k);
  const edgeEls = [];
  intra.forEach(e => {
    const A = nodes[e.a], B = nodes[e.b], cat = CAT(e.r);
    let d;
    const ay = A.y + Math.min(A.hgt / 2, 26), by = B.y + Math.min(B.hgt / 2, 26);
    if (A.x === B.x) { const xr = A.x + CM.colW; const bulge = 26 + Math.min(40, Math.abs(by - ay) * 0.12);
      d = `M${xr},${ay} C${xr + bulge},${ay} ${xr + bulge},${by} ${xr + 2},${by}`; }
    else if (A.x < B.x) { const x1 = A.x + CM.colW, x2 = B.x; d = `M${x1},${ay} C${(x1 + x2) / 2},${ay} ${(x1 + x2) / 2},${by} ${x2 - 2},${by}`; }
    else { const x1 = A.x, x2 = B.x + CM.colW; d = `M${x1},${ay} C${(x1 + x2) / 2},${ay} ${(x1 + x2) / 2},${by} ${x2 + 2},${by}`; }
    const p = el("path", { d, fill: "none", stroke: `var(--e-${cat})`, "stroke-width": 1.6, "stroke-dasharray": cat === "parallel" ? "5 4" : null,
      "marker-end": `url(#ar-${cat})`, class: "fade" }, gE);
    const hit = el("path", { d, fill: "none", stroke: "transparent", "stroke-width": 10 }, gE);
    hoverable(hit, `${e.a} ${e.r} ${e.b}: ${e.n}`);
    edgeEls.push({ e, p });
  });
  // nodes
  const nodeEls = {};
  Object.values(nodes).forEach(n => {
    const r = n.r;
    const g = el("g", { class: "clickable fade", tabindex: 0, role: "button", "aria-label": `${r.id} ${r.a}` }, gN);
    const box = el("rect", { x: n.x, y: n.y, width: CM.colW, height: n.hgt, rx: 4, fill: "var(--surface)", stroke: "var(--line)" }, g);
    el("rect", { x: n.x, y: n.y, width: 4, height: n.hgt, rx: 2, fill: ST[r.s] }, g);
    const idt = el("text", { x: n.x + 12, y: n.y + 17, "font-size": 12, "font-family": "IBM Plex Mono, monospace", fill: "var(--muted)" }, g); idt.textContent = r.id;
    n.lines.forEach((s, j) => { const t = el("text", { x: n.x + 12, y: n.y + 34 + j * 15, "font-size": 13.5, "font-weight": 500 }, g); t.textContent = s; });
    n.outs.forEach((oid, j) => {
      const ck = R[oid].c, cx = n.x + 12 + (j % 4) * 56, cy = n.y + 24 + n.lines.length * 15 + 6 + Math.floor(j / 4) * 21;
      const cg = el("g", { class: "clickable" }, g);
      el("rect", { x: cx, y: cy, width: 52, height: 17, rx: 8.5, fill: "none", stroke: hue(ck), "stroke-width": 1.4 }, cg);
      const ct = el("text", { x: cx + 26, y: cy + 12.5, "font-size": 11.5, "text-anchor": "middle", "font-family": "IBM Plex Mono, monospace", fill: hue(ck) }, cg); ct.textContent = oid;
      const e = D.rel.find(x => (x.a === r.id && x.b === oid) || (x.b === r.id && x.a === oid));
      hoverable(cg, `${e.a} ${e.r} ${e.b} (${R[oid].a}, cluster ${ck}). Click to go there.`);
      cg.addEventListener("click", ev => { ev.stopPropagation(); hideTip(); go("c" + ck, oid); });
    });
    g.addEventListener("click", () => select(r.id));
    g.addEventListener("keydown", ev => { if (ev.key === "Enter" || ev.key === " ") { ev.preventDefault(); select(r.id); } });
    nodeEls[r.id] = { g, box };
  });
  // right column: where this cluster connects (locator + counts)
  drawLocator(svg, k, CM.right + 6, 16, 270, others);
  svg.addEventListener("click", ev => { if (ev.target === svg) { state.sel = null; renderPanel(); paintCluster(); } });
  CM.edgeEls = edgeEls; CM.nodeEls = nodeEls; CM.k = k;
  main.appendChild(legendEl(true));
  paintCluster();
}
function paintCluster() {
  if (state.view === "overview" || !CM.nodeEls) return;
  const sel = state.sel && R[state.sel] && R[state.sel].c === CM.k ? state.sel : null;
  const linked = new Set(sel ? D.rel.filter(e => e.a === sel || e.b === sel).flatMap(e => [e.a, e.b]) : []);
  Object.entries(CM.nodeEls).forEach(([id, n]) => {
    n.g.setAttribute("opacity", !sel || linked.has(id) || id === sel ? 1 : .35);
    n.box.setAttribute("stroke", id === sel ? "var(--ink)" : "var(--line)"); n.box.setAttribute("stroke-width", id === sel ? 2 : 1);
  });
  CM.edgeEls.forEach(({ e, p }) => p.setAttribute("opacity", !sel || e.a === sel || e.b === sel ? 1 : .12));
}

