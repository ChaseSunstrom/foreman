/* Genesis run (T-2080): draws the live tower from genesis.json (written by `fm genesis export site/genesis`).
   Every box opens its doc in the drawer. No libraries, nothing from another host. */
(function () {
  "use strict";
  var root = document.documentElement, D = null, G = null;
  function $(id) { return document.getElementById(id); }
  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }
  function plural(n, w) { return n + " " + w + (n === 1 ? "" : "s"); }

  var theme = document.querySelector(".theme");
  if (theme) theme.addEventListener("click", function () {
    var t = root.getAttribute("data-theme");
    var dark = t ? t === "dark" : matchMedia("(prefers-color-scheme: dark)").matches;
    root.setAttribute("data-theme", dark ? "light" : "dark");
    try { localStorage.setItem("fm-theme", dark ? "light" : "dark"); } catch (e) {}
  });

  /* A small markdown renderer: headings, lists, tables, code, bold, italics, links. Escapes first. */
  function inline(s) {
    return String(s).split(/(`[^`]+`)/).map(function (part, i) {
      if (i % 2) return "<code>" + esc(part.slice(1, -1)) + "</code>";
      return esc(part)
        .replace(/\*\*(.+?)\*\*/g, "<b>$1</b>")
        .replace(/(^|[\s(])\*([^*\s][^*]*?)\*(?=[\s).,;:]|$)/g, "$1<i>$2</i>")
        .replace(/\[([^\]]+)\]\(([^)\s]+)\)/g, function (m, t, h) {
          return /^(https:\/\/|#|[\w./-]+$)/.test(h) ? '<a href="' + h + '">' + t + "</a>" : t;
        });
    }).join("");
  }
  function table(rows) {
    function cells(r) { return r.trim().replace(/^\||\|$/g, "").split("|").map(function (c) { return c.trim(); }); }
    var body = rows.slice(1).filter(function (r) { return !/^\|[\s:|-]+\|$/.test(r.trim()); });
    return '<div class="tbl"><table><thead><tr>' + cells(rows[0]).map(function (c) { return "<th>" + inline(c) + "</th>"; }).join("") +
      "</tr></thead><tbody>" + body.map(function (r) {
        return "<tr>" + cells(r).map(function (c) { return "<td>" + inline(c) + "</td>"; }).join("") + "</tr>";
      }).join("") + "</tbody></table></div>";
  }
  function md(text) {
    var lines = String(text || "").replace(/\r/g, "").split("\n"), out = [], para = [], list = null, i = 0, m;
    function flush() {
      if (para.length) { out.push("<p>" + inline(para.join(" ")) + "</p>"); para = []; }
      if (list) { out.push("</" + list + ">"); list = null; }
    }
    while (i < lines.length) {
      var l = lines[i];
      if (/^```/.test(l)) {
        flush(); var code = [];
        for (i++; i < lines.length && !/^```/.test(lines[i]); i++) code.push(lines[i]);
        out.push("<pre><code>" + esc(code.join("\n")) + "</code></pre>"); i++; continue;
      }
      if ((m = /^(#{1,4})\s+(.*)$/.exec(l))) {
        flush(); var h = m[1].length + 2; out.push("<h" + h + ">" + inline(m[2]) + "</h" + h + ">"); i++; continue;
      }
      if (/^\|.*\|\s*$/.test(l)) {
        flush(); var rows = [];
        while (i < lines.length && /^\|.*\|\s*$/.test(lines[i])) rows.push(lines[i++]);
        out.push(table(rows)); continue;
      }
      if ((m = /^\s*([-*]|\d+\.)\s+(.*)$/.exec(l))) {
        var kind = /\d/.test(m[1]) ? "ol" : "ul", item = [m[2]];
        if (list !== kind) { flush(); list = kind; out.push("<" + kind + ">"); }
        for (i++; i < lines.length && /^\s+\S/.test(lines[i]) && !/^\s*([-*]|\d+\.)\s/.test(lines[i]); i++) item.push(lines[i].trim());
        out.push("<li>" + inline(item.join(" ")) + "</li>"); continue;
      }
      if (!l.trim()) { flush(); i++; continue; }
      if (list) flush();
      para.push(l.trim()); i++;
    }
    flush();
    return out.join("\n");
  }

  /* data helpers */
  function capName(n) { var c = D.capabilities.filter(function (x) { return x.n === n; })[0]; return c ? c.name : "#" + n; }
  function firstSentence(s) { var m = /^(.*?[.!?])(\s|$)/.exec(s || ""); return m ? m[1] : s || ""; }
  function state(m) {
    if (m.critiqued) return "critiqued";
    if (m.tasks.length && m.tasks.every(function (t) { return t.status === "done"; })) return "done";
    if (m.tasks.length) return "active";
    return m.written ? "written" : "planned";
  }
  var STATE = { planned: "planned", written: "written", active: "building", done: "built", critiqued: "critiqued" };
  function allTasks(g) {
    var seen = {}, out = [];
    g.missions.forEach(function (m) {
      m.tasks.forEach(function (t) { if (!seen[t.id]) { seen[t.id] = 1; out.push({ t: t, m: m }); } });
    });
    g.tasks.forEach(function (t) { if (!seen[t.id]) { seen[t.id] = 1; out.push({ t: t, m: null }); } });
    return out;
  }
  function tierChips(gaps) {
    return gaps.map(function (x) {
      return '<span class="chip' + (x.tier >= 3 ? " t" + x.tier : "") + '">' + (x.tier ? "T" + x.tier + " " : "") + esc(x.text) + "</span>";
    }).join("");
  }
  function counts(gaps) {
    var c = { 1: 0, 2: 0, 3: 0, 4: 0, none: 0 };
    gaps.forEach(function (x) { c[x.tier] !== undefined ? c[x.tier]++ : c.none++; });
    return c;
  }
  function ago(iso) {
    var t = Date.parse(iso);
    if (isNaN(t)) return iso || "";
    var m = Math.round((Date.now() - t) / 60000);
    return m < 1 ? "just now" : m < 60 ? m + " min ago" : m < 2880 ? Math.round(m / 60) + " h ago" : Math.round(m / 1440) + " days ago";
  }
  function bar(t) {
    var pct = t.steps ? Math.round(100 * t.done / t.steps) : (t.status === "done" ? 100 : 0);
    return '<span class="bar" aria-hidden="true"><i style="width:' + pct + '%"></i></span>';
  }

  /* header */
  function stats() {
    var g = G, written = g.missions.filter(function (m) { return m.written; }).length, steps = 0, done = 0;
    allTasks(g).forEach(function (x) { steps += x.t.steps; done += x.t.done; });
    var mg = [].concat.apply([], g.missions.map(function (m) { return m.gaps; })), c = counts(mg), tiered = c[1] + c[2] + c[3] + c[4];
    var rows = [
      [D.capabilities.length, "abilities to pass"],
      ["gen " + g.n, "of " + plural(D.generations.length, "generation")],
      [written + "/" + g.missions.length, "missions written"],
      [done + "/" + steps, "task steps done"],
      [tiered ? Math.round(100 * (c[3] + c[4]) / tiered) + "%" : "–", "of planned gaps tier 3–4"],
      [D.exam.length, "exam results"],
      [D.coverage.filled + "/" + D.coverage.cells, "coverage cells filled"],
      [D.not_yet, "not-yet ideas waiting"],
      [1, "message from you"]];
    $("stats").innerHTML = rows.map(function (r) { return "<dt>" + esc(r[1]) + "</dt><dd>" + esc(r[0]) + "</dd>"; }).join("") +
      '<dd class="rev">rev ' + esc(D.rev) + " · updated " + esc(ago(D.updated)) + "</dd>";
    $("gen-label").textContent = "generation " + g.n + " · live";
    $("foot").textContent = "Exported by fm genesis export · " + D.rev;
  }

  /* A: the tower */
  var CRANE = '<svg class="crane" viewBox="0 0 64 800" preserveAspectRatio="none" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.5">' +
    '<path vector-effect="non-scaling-stroke" d="M18 40V800M40 40V800M4 40H64M18 40L29 12L40 40M29 12L64 40"/>' +
    '<path vector-effect="non-scaling-stroke" d="M18 70L40 100L18 130L40 160L18 190L40 220L18 250L40 280L18 310L40 340L18 370L40 400L18 430L40 460L18 490L40 520L18 550L40 580L18 610L40 640L18 670L40 700L18 730L40 760L18 790"/>' +
    '<path vector-effect="non-scaling-stroke" d="M58 40V260" stroke-dasharray="4 4" stroke="var(--signal)"/>' +
    '<rect x="6" y="46" width="10" height="18" fill="currentColor" opacity=".5"/></svg>';
  function tower() {
    var g = G, ts = allTasks(g), live = ts.filter(function (x) { return x.t.status !== "done"; }).length;
    var tiles = g.missions.map(function (m) {
      var s = state(m);
      return '<button type="button" class="tile ' + s + '" data-mission="' + esc(m.name) + '" data-n="' + (m.n || "") +
        '" data-deps="' + m.depends.join(" ") + '"><i>' + (m.n ? m.n + " · " : "") + STATE[s] + "</i><b>" + esc(m.name) + "</b></button>";
    }).join("");
    var trows = ts.length ? '<ul class="trows">' + ts.map(function (x) {
      var t = x.t;
      return '<li><button type="button" class="trow' + (t.status === "done" ? " done" : "") + '" data-task="' + esc(t.id) + '"><code>' + esc(t.id) +
        '</code><span class="t">' + esc(t.title) + '</span><span class="n">' + t.done + "/" + t.steps + " · " + esc(t.status) + "</span>" + bar(t) + "</button></li>";
    }).join("") + "</ul>" : '<p class="empty">No task filed yet for this generation.</p>';
    var seed = "gen-" + g.n + "/seed.md";
    $("tower-body").className = "";
    $("tower-body").innerHTML = '<div class="tower">' + CRANE + '<div class="levels"><div class="loop" aria-hidden="true"><span>↻ rewrites the Seed every round</span></div>' +
      '<button type="button" class="lvl l4" data-l4="1"><span class="flag">only better rewrites survive</span><span class="k">Level 4</span><h3>Exam &amp; critique</h3>' +
      "<p>" + plural(D.exam.length, "exam result") + " · " + plural(g.critiques.length, "critique") + " · lineage " + (D.docs["lineage.md"] ? "kept" : "starts after gen 1") + "</p></button>" +
      '<div class="lvl l3"><span class="k">Level 3</span><h3>Tasks, built &amp; proved</h3><p>' + plural(ts.length, "task") + ", " + live + " open · red tests first, spikes and races in lanes</p>" + trows + "</div>" +
      '<div class="lvl l2"><span class="k">Level 2</span><h3>Missions, up to 8</h3><p>One prompt per gap cluster, each its own session. Hover one to see what it waits on.</p>' +
      '<div class="tiles" id="tiles">' + tiles + "</div>" +
      '<div class="legend"><span class="p">planned</span><span class="w">written</span><span class="a">building</span><span class="d">built</span><span class="c">critiqued</span></div></div>' +
      '<button type="button" class="lvl l1" data-doc="' + seed + '"' + (D.docs[seed] ? "" : " disabled") + '><span class="k">Level 1</span><h3>Seed · generation ' + g.n + "</h3>" +
      "<p>Biggest gaps, lenses, order · " + plural(g.missions.length, "mission") + ", " + plural(g.rules.length, "standing rule") + "</p></button>" +
      '<button type="button" class="lvl l0" data-doc="gen-0.md"><span class="k">Level 0 · foundation</span><h3>Your message</h3><p>Goals, MUSTs, NEVERs. Sent once, never edited.</p></button>' +
      "</div></div>" +
      '<div class="genesis-box"><code>fm genesis</code><p>' + (g.n < 2 ? "Gen 1's Seed was written by hand from your message. From gen 2 on, fm genesis writes every Seed (#13)."
        : "Gen " + g.n + "'s Seed is written by fm genesis itself (#13).") + "</p></div>";
  }
  function highlight(on) {
    var box = $("tiles");
    if (!box) return;
    box.classList.toggle("hl", !!on);
    [].forEach.call(box.children, function (t) {
      var deps = on ? on.getAttribute("data-deps").split(" ") : [], n = t.getAttribute("data-n");
      t.classList.toggle("me", t === on);
      t.classList.toggle("dep", !!on && n !== "" && deps.indexOf(n) >= 0);
      t.classList.toggle("needs", !!on && on.getAttribute("data-n") !== "" &&
        t.getAttribute("data-deps").split(" ").indexOf(on.getAttribute("data-n")) >= 0);
    });
  }

  /* B: capabilities */
  var GROUPS = [["finds", "Finds", "work nobody asked for", [1, 3, 11]], ["thinks", "Thinks", "every possibility, then chooses by evidence", [2, 4, 8]],
    ["does", "Does", "whatever it takes, with whatever it needs", [9, 5, 10]], ["proves", "Proves", "and gets better at all of it", [6, 7, 12, 13]]];
  function missionsFor(n, g) { return g.missions.filter(function (m) { return m.caps.indexOf(n) >= 0; }); }
  function caps() {
    var known = {};
    D.capabilities.forEach(function (c) { known[c.n] = c; });
    $("caps-body").innerHTML = GROUPS.map(function (gr) {
      return '<div class="group ' + gr[0] + '"><h3>' + gr[1] + "<small>" + gr[2] + "</small></h3>" + gr[3].filter(function (n) { return known[n]; }).map(function (n) {
        var c = known[n], gaps = D.gaps[String(n)] || [], k = counts(gaps), ms = missionsFor(n, G);
        var chips = (k[4] ? '<span class="chip t4">' + k[4] + "× tier 4</span>" : "") + (k[3] ? '<span class="chip t3">' + k[3] + "× tier 3</span>" : "") +
          (ms.length ? ms.map(function (m) { return '<span class="chip">→ ' + esc(m.name) + "</span>"; }).join("") : '<span class="chip">no mission in gen ' + G.n + "</span>");
        return '<button type="button" class="cap" data-cap="' + n + '"><span class="num">' + n + "</span><span><b>" + esc(c.name) + "</b>" +
          (n === 13 ? '<span class="big">THE BIG ONE</span>' : "") + "<p>" + esc(firstSentence(c.text)) + '</p><span class="chips">' + chips + "</span></span></button>";
      }).join("") + "</div>";
    }).join("");
  }

  /* C: ambition */
  function ambition() {
    var all = [].concat.apply([], Object.keys(D.gaps).map(function (k) { return D.gaps[k]; })), c = counts(all);
    var mg = [].concat.apply([], G.missions.map(function (m) { return m.gaps; })), p = counts(mg), tiered = p[1] + p[2] + p[3] + p[4];
    var share = tiered ? Math.round(100 * (p[3] + p[4]) / tiered) : 0;
    var T = [[1, "Tweak", "wording, ms, a flag"], [2, "Feature", "a new verb or view"], [3, "Capability", "a new class of things it can do"], [4, "Paradigm", "changes what Foreman is"]];
    $("ambition").innerHTML = '<div class="scale">' + T.map(function (t) {
      return '<div class="tier' + (t[0] >= 3 ? " hi" : "") + '"><b>' + t[0] + " · " + t[1] + "</b><span>" + t[2] + "</span><strong>" + c[t[0]] +
        "</strong><small>open in the gap map · " + p[t[0]] + " planned in gen " + G.n + "</small></div>";
    }).join("") + "</div>" +
      '<div class="share" role="img" aria-label="' + share + '% of gen ' + G.n + ' planned gaps are tier 3 or 4; the floor is 70%"><i style="width:' + share + '%"></i><u></u><span>' +
      share + "% of gen " + G.n + "'s planned gaps are tier 3–4 · floor 70%</span></div>" +
      '<p class="note">↳ tweaks go to the inbox, not the build. At least 70% of everything built is tier 3–4.</p>';
  }

  /* D: exam */
  function frac(a, b) { return b ? esc(a + "/" + b) : "–"; }
  function exam() {
    var rows = D.exam.slice(-12).reverse();
    $("exam").innerHTML = rows.length ? '<div class="tbl"><table><thead><tr><th>agent</th><th>run</th><th>found</th><th>false alarms</th><th>fixed</th><th>tests first</th><th>readings</th><th>missing tool</th><th>cost</th><th>split</th></tr></thead><tbody>' +
      rows.map(function (e) {
        return "<tr><td><b>" + esc(e.agent) + "</b></td><td><code>" + esc(e.run || "") + "</code></td><td>" + frac(e.found, e.keyed) + "</td><td>" + esc(e.false_alarms == null ? "–" : e.false_alarms) +
          "</td><td>" + frac(e.fixed, e.fixable) + "</td><td>" + frac(e.tf_first, e.tf_keyed) + "</td><td>" + frac(e.readings_hit, e.readings_keyed) + "</td><td>" + frac(e.missing_hit, e.missing_keyed) +
          "</td><td>" + (typeof e.cost === "number" && e.cost > 0 ? "$" + e.cost.toFixed(2) : "–") +
          "</td><td>" + esc(e.split || "all") + (e.author && e.author !== "self" ? " · by " + esc(e.author) : "") + (e.holdout && e.holdout.scenarios ? " · held out " + frac(e.holdout.found, e.holdout.keyed) + " found" : "") + (typeof e.errors === "number" && e.errors > 0 ? " · " + e.errors + " errored" : "") + "</td></tr>";
      }).join("") + "</tbody></table></div>"
      : '<div class="rule"><b>No exam run yet.</b>Mission 1 (fm exam) is building it: throwaway repos in six languages with planted defects, vague, ambiguous and missing-tool requests, a held-out third, and plain Claude Code run beside Foreman on the same repos. Every result lands here.</div>';
  }

  /* E: rules */
  var RUN = [["Held-out exam", "A third of the practice repos are never trained on. They decide \"done\"."], ["Subtract as you add", "Each round cuts as much as it adds. Hooks can't get slower."],
    ["Spikes, not vetoes", "\"Too ambitious\" is never a reason. A failed prototype is."], ["Two new tries, then move on", "Stuck tasks get two fresh angles, then a recorded diagnosis."],
    ["Everything finished", "Tests, docs, site, every surface. Nothing left half-built."], ["No outside sweeps", "Tokens go into building and proving, not reading other repos."]];
  function rules() {
    var steer = G.rules.map(function (r, i) {
      var m = /^\*\*(.+?)\*\*\s*(.*)$/.exec(r), title = m ? m[1].replace(/\.$/, "") : "Standing rule " + (i + 1), rest = m ? m[2] : r;
      return '<button type="button" class="rule steer" data-rule="' + i + '"><b>' + inline(title) + "</b>" + inline(firstSentence(rest)) + "</button>";
    });
    $("rules").innerHTML = RUN.map(function (r) { return '<div class="rule"><b>' + esc(r[0]) + "</b>" + esc(r[1]) + "</div>"; }).join("") + steer.join("");
  }

  /* G: docs */
  function docs() {
    var names = Object.keys(D.docs).sort(), groups = { "Foundation": [], "Tower-wide": [] };
    names.forEach(function (n) {
      var key = n === "gen-0.md" ? "Foundation" : n.indexOf("/") < 0 ? "Tower-wide" : n.split("/")[0].replace("gen-", "Generation ");
      (groups[key] = groups[key] || []).push(n);
    });
    $("docs-body").innerHTML = Object.keys(groups).filter(function (k) { return groups[k].length; }).map(function (k) {
      return "<div><h4>" + esc(k) + "</h4>" + groups[k].map(function (n) {
        return '<button type="button" class="doc" data-doc="' + esc(n) + '">' + esc(n) + "<small>" + D.docs[n].split("\n").length + " lines</small></button>";
      }).join("") + "</div>";
    }).join("");
  }

  /* the drawer */
  var dlg = $("drawer");
  function box(title, html) { return html ? '<div class="box"><b>' + esc(title) + "</b>" + html + "</div>" : ""; }
  function show(kicker, title, meta, body, hash) {
    $("dr-kicker").textContent = kicker;
    $("dr-title").textContent = title;
    $("dr-meta").innerHTML = meta || "";
    $("dr-body").innerHTML = body || "";
    dlg.scrollTop = 0;
    if (!dlg.open) { if (dlg.showModal) dlg.showModal(); else dlg.setAttribute("open", ""); }
    try { history.replaceState(null, "", hash ? "#" + hash : location.pathname); } catch (e) {}
  }
  function close() { if (dlg.close) dlg.close(); else dlg.removeAttribute("open"); }
  dlg.addEventListener("close", function () { try { history.replaceState(null, "", location.pathname); } catch (e) {} });
  $("dr-close").addEventListener("click", close);
  dlg.addEventListener("click", function (e) { if (e.target === dlg) close(); });
  function title(text, fallback) { var m = /^#\s+(.+)$/m.exec(text || ""); return m ? m[1] : fallback; }
  function openDoc(name) {
    var text = D.docs[name];
    if (text == null) return;
    show(name, title(text, name), "", md(text), "doc=" + name);
  }
  function taskList(ts) {
    return ts.length ? "<ul>" + ts.map(function (t) {
      return "<li><code>" + esc(t.id) + "</code> " + esc(t.title) + " — " + t.done + "/" + t.steps + " steps, " + esc(t.status) + "</li>";
    }).join("") + "</ul>" : "";
  }
  function openMission(name) {
    var m = G.missions.filter(function (x) { return x.name === name; })[0];
    if (!m) return;
    var doc = D.docs["gen-" + G.n + "/mission-" + name + ".md"];
    var deps = m.depends.map(function (n) { var d = G.missions.filter(function (x) { return x.n === n; })[0]; return d ? n + " · " + d.name : "#" + n; });
    var meta = box("State", esc(STATE[state(m)])) +
      box("Capabilities", m.caps.map(function (n) { return '<span class="chip">#' + n + " " + esc(capName(n)) + "</span>"; }).join(" ") || esc(m.caps_text)) +
      box("Gaps it closes", '<span class="chips">' + tierChips(m.gaps) + "</span>") +
      box("Waits on", esc(deps.join(", ") || "nothing: it can start now")) +
      box("Tasks", taskList(m.tasks)) +
      (m.critiqued ? box("Critique", '<button type="button" class="doc" data-doc="gen-' + G.n + "/critique-" + esc(name) + '.md">critique-' + esc(name) + ".md</button>") : "");
    show("gen " + G.n + " · mission " + (m.n || ""), "Mission: " + name, meta,
      doc ? md(doc) : '<p class="empty">Not written yet. The Seed queues it' + (deps.length ? " after " + esc(deps.join(", ")) : "") + "; it shows here the moment it's filed.</p>",
      "mission=" + name);
  }
  function capSection(text, n) {
    var lines = (text || "").split("\n"), out = [], on = false, start = new RegExp("^" + n + "\\. \\*\\*");
    for (var i = 0; i < lines.length; i++) {
      if (start.test(lines[i])) on = true;
      else if (on && (/^\d+\. \*\*/.test(lines[i]) || /^## /.test(lines[i]))) break;
      if (on) out.push(lines[i].replace(start, "**"));
    }
    return out.join("\n");
  }
  function openCap(n) {
    var c = D.capabilities.filter(function (x) { return x.n === n; })[0];
    if (!c) return;
    var gap = (D.docs["gap-map.md"] || "").split(/^(?=## )/m).filter(function (s) { return new RegExp("^## " + n + "\\.").test(s); })[0] || "";
    var per = D.generations.map(function (g) {
      var ms = missionsFor(n, g);
      return ms.length ? "<li>gen " + g.n + ": " + ms.map(function (m) { return '<button type="button" class="chip" data-mission="' + esc(m.name) + '" data-gen="' + g.n + '">' + esc(m.name) + " · " + STATE[state(m)] + "</button>"; }).join(" ") + "</li>" : "";
    }).join("");
    var k = counts(D.gaps[String(n)] || []);
    var meta = box("Open gaps", k[4] + " tier 4 · " + k[3] + " tier 3" + (k[2] + k[1] ? " · " + (k[2] + k[1]) + " smaller" : "")) +
      box("Missions", per ? "<ul>" + per + "</ul>" : "none yet") +
      box("Exam", D.exam.length ? plural(D.exam.length, "result") + " in the exam log (section D)" : "no run yet: mission 1 builds the exam");
    show("capability #" + n, c.name, meta, "<h4>Your message, §2</h4>" + md(capSection(D.docs["gen-0.md"], n)) +
      (gap ? "<h4>Gap map</h4>" + md(gap.replace(/^## .*\n/, "")) : ""), "cap=" + n);
  }
  function openTask(id) {
    var x = allTasks(G).filter(function (y) { return y.t.id === id; })[0];
    if (!x) return;
    var t = x.t;
    show(t.id + " · " + [t.type, t.tier].filter(Boolean).join(" "), t.title,
      box("Progress", t.done + " of " + t.steps + " steps · " + esc(t.status) + bar(t)) +
      box("Now on", esc(t.current || (t.status === "done" ? "closed" : "–"))) +
      box("Mission", x.m ? '<button type="button" class="chip" data-mission="' + esc(x.m.name) + '">' + esc(x.m.name) + "</button>" : "the Seed itself"),
      '<p class="empty">The brief lives in the project\'s Foreman state; every commit it makes names ' + esc(t.id) + ".</p>", "task=" + t.id);
  }
  function openL4() {
    var g = G, crit = g.critiques.map(function (n) { return '<button type="button" class="doc" data-doc="gen-' + g.n + "/critique-" + esc(n) + '.md">critique-' + esc(n) + ".md</button>"; }).join("");
    show("level 4", "Exam & critique · generation " + g.n,
      box("Exam", plural(D.exam.length, "result") + " logged. A rewrite survives only if it closes more held-out scenarios than its parent.") +
      box("Critiques", crit || "Each mission is critiqued when it closes: scenarios closed vs planned, outside signals, coverage cells filled.") +
      box("Lineage", D.docs["lineage.md"] ? '<button type="button" class="doc" data-doc="lineage.md">lineage.md</button>' : "Starts when generation 1 closes."),
      "", "l4");
  }

  document.addEventListener("click", function (e) {
    var t = e.target.closest("[data-doc],[data-mission],[data-cap],[data-task],[data-rule],[data-l4]");
    if (!t || !D) return;
    if (t.hasAttribute("data-gen")) selectGen(+t.getAttribute("data-gen"));
    if (t.hasAttribute("data-doc")) openDoc(t.getAttribute("data-doc"));
    else if (t.hasAttribute("data-mission")) openMission(t.getAttribute("data-mission"));
    else if (t.hasAttribute("data-cap")) openCap(+t.getAttribute("data-cap"));
    else if (t.hasAttribute("data-task")) openTask(t.getAttribute("data-task"));
    else if (t.hasAttribute("data-rule")) show("gen " + G.n + " · standing rule " + (+t.getAttribute("data-rule") + 1), "Standing rule", "", md(G.rules[+t.getAttribute("data-rule")]));
    else openL4();
  });
  ["mouseover", "focusin"].forEach(function (ev) {
    document.addEventListener(ev, function (e) { var t = e.target.closest && e.target.closest(".tile"); if (t) highlight(t); });
  });
  ["mouseout", "focusout"].forEach(function (ev) {
    document.addEventListener(ev, function (e) { if (e.target.closest && e.target.closest(".tile")) highlight(null); });
  });

  function selectGen(n) {
    G = D.generations.filter(function (g) { return g.n === n; })[0] || D.generations[D.generations.length - 1];
    $("gens").innerHTML = D.generations.map(function (g) {
      return '<button type="button" aria-pressed="' + (g === G) + '" data-pick="' + g.n + '">gen ' + g.n + "</button>";
    }).join("");
    stats(); tower(); caps(); ambition(); rules();
  }
  $("gens").addEventListener("click", function (e) { var b = e.target.closest("[data-pick]"); if (b) selectGen(+b.getAttribute("data-pick")); });

  fetch("genesis.json", { cache: "no-cache" }).then(function (r) {
    if (!r.ok) throw new Error(r.status);
    return r.json();
  }).then(function (data) {
    D = data;
    if (!D.generations.length) D.generations = [{ n: 1, seed: false, missions: [], critiques: [], tasks: [], rules: [] }];
    selectGen(D.generations[D.generations.length - 1].n);
    exam(); docs();
    var h = location.hash.slice(1);
    try { h = decodeURIComponent(h); } catch (e) { h = ""; }  // a malformed hash (#doc=%) opens nothing, breaks nothing
    var m = /^(doc|cap|mission|task)=(.+)$/.exec(h);
    if (m) ({ doc: openDoc, cap: function (v) { openCap(+v); }, mission: openMission, task: openTask })[m[1]](m[2]);
    else if (h === "l4") openL4();
  }).catch(function () {
    $("tower-body").innerHTML = '<p class="empty">The tower\'s data (genesis.json) didn\'t load. Opened from disk? Serve the folder, e.g. from the site build.</p>';
  });
})();
