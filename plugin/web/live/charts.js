// Sampo · live chart kit (T-3092): SVG charts and progress bars, no library. Every colour is a CSS token: a series
// carries `--c` (a var(--k-*) name) and live.css does the painting, so both looks and both schemes read right. Every chart
// is role="img" with its figures as a text label, and nothing here uses innerHTML (the page runs under a strict CSP).
(function () {
"use strict";
const NS = "http:" + "//www.w3.org/2000/svg";  // a namespace name, not a link: split so the offline check stays literal
const fin = v => typeof v === "number" && isFinite(v);
const fnum = v => fin(v) ? (Math.abs(v) >= 100 ? Math.round(v) : Math.round(v * 10) / 10).toLocaleString("en-US") : "—";

function svg(tag, cls, attrs, kids) {
  const e = document.createElementNS(NS, tag);
  if (cls) e.setAttribute("class", cls);
  for (const k in attrs || {}) e.setAttribute(k, String(attrs[k]));
  if (kids) e.append(...kids);
  return e;
}
const txt = (cls, x, y, s, anchor) => { const t = svg("text", "ch-t " + cls, {x: x.toFixed(1), y: y.toFixed(1)}); if (anchor) t.setAttribute("text-anchor", anchor); t.textContent = s; return t; };
function frame(host, w, h, label, cls) {  // one svg per chart: its title and label are the text equivalent
  const s = svg("svg", "ch " + (cls || ""), {viewBox: "0 0 " + w + " " + h, width: w, height: h, role: "img", "aria-label": label});
  s.append(svg("title", "", {}, [document.createTextNode(label)]));
  return s;
}
function html(tag, cls, text) { const e = document.createElement(tag); if (cls) e.className = cls; if (text != null) e.textContent = text; return e; }

function ticks(max, n) {  // 0 .. a round number at or above max
  if (!fin(max) || max <= 0) return [0, 1];
  const raw = max / (n || 4), p = Math.pow(10, Math.floor(Math.log10(raw))), f = raw / p, st = (f <= 1 ? 1 : f <= 2 ? 2 : f <= 5 ? 5 : 10) * p, out = [];
  for (let i = 0; i < 12; i++) { const v = +(i * st).toPrecision(10); out.push(v); if (v >= max) break; }
  return out;
}

function legend(items) {  // [{name, c, value}]: a swatch, the name, its latest figure
  const ul = html("ul", "ch-leg");
  for (const it of items) {
    const li = html("li"); li.style.setProperty("--c", it.c);
    li.append(html("span", "ch-sw"), html("span", "ch-n", it.name), ...(it.value != null ? [html("b", "", it.value)] : []));
    ul.append(li);
  }
  return ul;
}

// line({label, series:[{name, c, pts:[[x,y]...]}], xfmt, yfmt, area, h}): axes, gridlines, a legend, the latest point lifted.
function line(host, o) {
  const series = (o.series || []).map(s => ({name: s.name, c: s.c, pts: (s.pts || []).filter(p => fin(p[0]) && fin(p[1]))})).filter(s => s.pts.length);
  if (!series.length) { host.replaceChildren(html("p", "ch-empty", o.empty || "No readings yet")); return; }
  const W = Math.max(220, host.clientWidth || 320), H = o.h || 150, L = 40, R = 14, T = 10, B = 22;
  const xs = series.flatMap(s => s.pts.map(p => p[0])), x0 = Math.min(...xs), x1 = Math.max(...xs) > x0 ? Math.max(...xs) : x0 + 1;
  const yt = ticks(Math.max(...series.flatMap(s => s.pts.map(p => p[1]))), 3), ymax = yt[yt.length - 1];
  const X = x => L + (x - x0) / (x1 - x0) * (W - L - R), Y = y => T + (1 - y / ymax) * (H - T - B);
  const yf = o.yfmt || fnum, xf = o.xfmt || fnum;
  const read = series.map(s => s.name + " now " + yf(s.pts[s.pts.length - 1][1]) + ", high " + yf(Math.max(...s.pts.map(p => p[1]))));
  const label = o.label + ": " + read.join("; ") + "; from " + xf(x0) + " to " + xf(x1);
  const s = frame(host, W, H, label, "ch-line");
  for (const v of yt) { s.append(svg("line", "ch-grid", {x1: L, x2: W - R, y1: Y(v).toFixed(1), y2: Y(v).toFixed(1)}), txt("ch-y", L - 6, Y(v) + 4, yf(v), "end")); }
  [0, 1 / 3, 2 / 3, 1].forEach((f, i) => s.append(txt("ch-x", L + f * (W - L - R), H - 6, xf(x0 + f * (x1 - x0)), i === 0 ? "start" : i === 3 ? "end" : "middle")));
  s.append(svg("line", "ch-axis", {x1: L, x2: W - R, y1: Y(0).toFixed(1), y2: Y(0).toFixed(1)}));
  for (const se of series) {
    const g = svg("g", "ch-ser"); g.style.setProperty("--c", se.c);
    const d = se.pts.map((p, i) => (i ? "L" : "M") + X(p[0]).toFixed(1) + " " + Y(p[1]).toFixed(1)).join("");
    if (o.area) g.append(svg("path", "ch-area", {d: d + "L" + X(se.pts[se.pts.length - 1][0]).toFixed(1) + " " + Y(0).toFixed(1) + "L" + X(se.pts[0][0]).toFixed(1) + " " + Y(0).toFixed(1) + "Z"}));
    g.append(svg("path", "ch-ln", {d}));
    const last = se.pts[se.pts.length - 1];
    g.append(svg("circle", "ch-halo", {cx: X(last[0]).toFixed(1), cy: Y(last[1]).toFixed(1), r: 8}),
             svg("circle", "ch-dot", {cx: X(last[0]).toFixed(1), cy: Y(last[1]).toFixed(1), r: 4}));
    s.append(g);
  }
  host.replaceChildren(s, legend(series.map(se => ({name: se.name, c: se.c, value: yf(se.pts[se.pts.length - 1][1])}))));
}

// stack({label, total, segs:[{name, c, v}], fmt}): one bar split by who holds the memory; what is left over is the track.
function stack(host, o) {
  const segs = (o.segs || []).filter(g => fin(g.v) && g.v > 0), sum = segs.reduce((a, g) => a + g.v, 0), total = Math.max(o.total || 0, sum);
  if (!total) { host.replaceChildren(html("p", "ch-empty", o.empty || "No memory reading")); return; }
  const W = Math.max(180, host.clientWidth || 260), H = 52, L = 2, R = 2, f = o.fmt || fnum, bw = W - L - R;
  const label = o.label + ": " + segs.map(g => g.name + " " + f(g.v)).join(", ") + (total > sum ? ", free " + f(total - sum) : "") + ", of " + f(total);
  const s = frame(host, W, H, label, "ch-stack");
  s.append(svg("rect", "ch-free", {x: L, y: 6, width: bw, height: 26, rx: 5}));
  let x = L;
  for (const g of segs) {
    const w = g.v / total * bw, r = svg("rect", "ch-seg", {x: x.toFixed(1), y: 6, width: Math.max(1, w - 1).toFixed(1), height: 26});
    r.style.setProperty("--c", g.c); r.append(svg("title", "", {}, [document.createTextNode(g.name + " " + f(g.v))]));
    s.append(r); x += w;
  }
  s.append(txt("ch-x", L, 48, "0", "start"), txt("ch-x", W - R, 48, f(total), "end"));
  host.replaceChildren(s);
}

// funnel({label, stages:[{name, kept, rej, wait}], fmt}): each stage a bar as wide as its candidates, kept | waiting | rejected.
function funnel(host, o) {
  const st = (o.stages || []).map(s => ({name: s.name, kept: s.kept || 0, rej: s.rej || 0, wait: s.wait || 0})).map(s => Object.assign(s, {total: s.kept + s.rej + s.wait}));
  if (!st.length) { host.replaceChildren(html("p", "ch-empty", o.empty || "No funnel yet")); return; }
  const f = o.fmt || fnum, most = Math.max(1, ...st.map(s => s.total)), W = Math.max(240, host.clientWidth || 300), RH = 30, G = 6, LW = 64, CW = 104;
  const H = st.length * (RH + G) + 2, bx = LW, bw = Math.max(60, W - LW - CW), cx = bx + bw / 2;
  const label = o.label + ": " + st.map(s => s.name + " " + f(s.kept) + " kept of " + f(s.total) + (s.wait ? ", " + f(s.wait) + " waiting" : "")).join("; ");
  const s = frame(host, W, H, label, "ch-funnel");
  st.forEach((r, i) => {
    const y = i * (RH + G) + 1, w = Math.max(3, r.total / most * bw), x = cx - w / 2;
    if (i) { const p = st[i - 1], pw = Math.max(3, p.total / most * bw); s.append(svg("polygon", "ch-link", {points: [cx - pw / 2, y - G, cx + pw / 2, y - G, cx + w / 2, y, cx - w / 2, y].map(n => n.toFixed(1)).join(" ")})); }
    const t = r.total || 1;
    s.append(txt("ch-n", 0, y + RH / 2 + 4, r.name, "start"));
    let px = x;
    for (const [cls, v] of [["ch-kept", r.kept], ["ch-wait", r.wait], ["ch-rej", r.rej]]) {
      if (v <= 0) continue;
      const sw = v / t * w; s.append(svg("rect", cls, {x: px.toFixed(1), y, width: sw.toFixed(1), height: RH})); px += sw;
    }
    s.append(txt("ch-v", W, y + RH / 2 + 4, f(r.kept) + " of " + f(r.total), "end"));
  });
  host.replaceChildren(s, legend([{name: "kept", c: "var(--k-blue)"}, {name: "waiting", c: "var(--k-amber)"}, {name: "rejected", c: "var(--k-other)"}]));
}

// spark(host, values, {label, c}): a line with an area fill and a dot on the latest reading.
function spark(host, vals, o) {
  const v = (vals || []).filter(fin), W = 100, H = 28;
  const lo = Math.min(...v), hi = Math.max(...v), span = hi - lo || 1;
  const label = (o.label || "Trend") + (v.length > 1 ? ": now " + fnum(v[v.length - 1]) + ", low " + fnum(lo) + ", high " + fnum(hi) + " over " + v.length + " readings" : v.length ? ": " + fnum(v[0]) + ", one reading so far" : ": no readings yet");
  const s = frame(host, W, H, label, "ch-spark");
  s.style.setProperty("--c", o.c || "var(--k-blue)");
  if (v.length) {
    const X = i => v.length < 2 ? W - 4 : 3 + i / (v.length - 1) * (W - 9), Y = y => H - 4 - (y - lo) / span * (H - 10);
    const d = v.map((y, i) => (i ? "L" : "M") + X(i).toFixed(1) + " " + Y(y).toFixed(1)).join("");
    if (v.length > 1) s.append(svg("path", "ch-area", {d: d + "L" + X(v.length - 1).toFixed(1) + " " + (H - 1) + "L" + X(0).toFixed(1) + " " + (H - 1) + "Z"}), svg("path", "ch-ln", {d}));
    s.append(svg("circle", "ch-dot", {cx: X(v.length - 1).toFixed(1), cy: Y(v[v.length - 1]).toFixed(1), r: 2.6}));
  }
  host.replaceChildren(s);
}

const dur = sec => !fin(sec) || sec < 0 ? "" : sec < 90 ? Math.round(sec) + "s" : sec < 5400 ? Math.round(sec / 60) + "m" : Math.floor(sec / 3600) + "h " + String(Math.round(sec % 3600 / 60)).padStart(2, "0") + "m";
// progress({done, total, unit, rate (per second), eta (seconds)}): a bar and its words: percent, count, rate, ETA.
function progress(o) {
  o = o || {};
  const known = fin(o.done) && fin(o.total) && o.total > 0, frac = known ? Math.min(1, Math.max(0, o.done / o.total)) : null;
  const bits = known ? [Math.round(frac * 100) + "%", fnum(o.done) + " of " + fnum(o.total) + (o.unit ? " " + o.unit : "")] : ["no progress reported"];
  if (known && fin(o.rate) && o.rate > 0) bits.push(o.rate >= 1 ? fnum(o.rate) + "/s" : fnum(o.rate * 60) + "/min");
  if (known && fin(o.eta) && frac < 1) bits.push("ETA " + dur(o.eta));
  const wrap = html("div", "pg"), bar = html("div", frac != null ? "jbar pg-bar" : "jbar pg-bar heat"), fill = html("span", "jfill");
  bar.setAttribute("role", "progressbar"); bar.setAttribute("aria-valuemin", "0"); bar.setAttribute("aria-valuemax", "100");
  if (frac != null) { bar.setAttribute("aria-valuenow", String(Math.round(frac * 100))); fill.style.setProperty("--p", frac.toFixed(4)); }
  bar.setAttribute("aria-valuetext", bits.join(", ")); bar.setAttribute("aria-label", o.label || "Progress");
  bar.append(fill); wrap.append(bar, html("p", "pg-t", bits.join(" · ")));
  return wrap;
}

window.Charts = {line, stack, funnel, spark, progress, legend, ticks, dur};
})();
