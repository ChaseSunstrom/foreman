/* T-3101: the cards page. Reads cards/index.json, a small manifest (the counts per grid and cell, the pages, each file's
   version; written by build.py --cards), then the index a page of ~2,000 cards at a time, newest first: the first page
   draws at once, later ones load as the list needs them, and a search or a filter reads them all, saying how far it has
   got. A card's steps, example, check and traps come from its shard when it opens. A card is model output: its text is
   set with textContent, never parsed. */
(function () {
  "use strict";
  var PAGE = 50, WAIT = 15000, READ = 60000;
  var root = document.getElementById("cards");
  if (!root) return;
  var $ = function (id) { return document.getElementById(id); };
  var q = $("cards-q"), gridsEl = $("cards-grids"), facetsEl = $("cards-facets"), status = $("cards-status"),
      empty = $("cards-empty"), list = $("cards-list"), more = $("cards-more");
  var src = root.getAttribute("data-index"), at = src.indexOf("?");
  var ver = at < 0 ? "" : src.slice(at), base = (at < 0 ? src : src.slice(0, at)).replace(/[^/]*$/, "");
  // every map keyed by card data has no prototype: a cell or grid named "constructor" is just a name
  var bare = function (o) { return Object.assign(Object.create(null), o); };
  var obj = function (o) { return o && typeof o === "object" && !Array.isArray(o) ? o : {}; };
  var LABELS = bare({ all: "All", general: "General", ui: "UI", variants: "Variants", other: "Other" });
  var man = null, total = 0, files = bare(), pages = [], byId = bare(), grid = "all", picks = bare(), limit = PAGE,
      hits = [], shards = bare(), timer = 0, busy = null, opening = null;

  function el(tag, cls, text) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text != null) e.textContent = text;
    return e;
  }
  function n(x) { return x.toLocaleString("en"); }
  function label(g) { return LABELS[g] || g.charAt(0).toUpperCase() + g.slice(1); }
  function num(id) { return +String(id || "").replace(/^K-/i, "") || 0; }
  function url(name) {  // a file's own version, so a browser keeps every page and shard that didn't change
    var v = files[name];
    return base + name + ".json" + (typeof v === "string" && /^[0-9a-f]{1,16}$/.test(v) ? "?v=" + v : ver);
  }

  // a stalled request ends in a message: WAIT for the answer to start, READ for the rest of it
  function get(u) {
    var ctl = new AbortController(), t = setTimeout(function () { ctl.abort(); }, WAIT);
    return fetch(u, { signal: ctl.signal }).then(function (r) {
      clearTimeout(t);
      if (!r.ok) throw new Error("HTTP " + r.status);
      t = setTimeout(function () { ctl.abort(); }, READ);
      return r.json();
    }).then(function (v) { clearTimeout(t); return v; }, function (e) {
      clearTimeout(t);
      throw new Error(e && e.name === "AbortError" ? "it took too long" : (e && e.message) || "it failed");
    });
  }

  function words() { return q.value.toLowerCase().split(/\s+/).filter(Boolean); }
  function idOf(w) { return w.length === 1 && /^k-\d+$/.test(w[0]) ? num(w[0]) : 0; }
  function matches(c, w) {
    if (idOf(w)) return c.id.toLowerCase() === w[0];  // an id is that card, not a prefix
    for (var i = 0; i < w.length; i++) if (c.hay.indexOf(w[i]) < 0) return false;
    return true;
  }
  function picked(c, skip) {
    for (var f in picks) if (f !== skip && c.cell[f] !== picks[f]) return false;
    return true;
  }
  function picking() { return Object.keys(picks).length > 0; }
  // the pages a view reads: a search reads every page (the tab counts are its counts), a grid only its own
  function inScope(p, w) { return w.length > 0 || grid === "all" || !!p.grids[grid]; }

  // the loaded cards, newest first. Browsing (no search, no filter) stops at the first page in scope not yet here, so
  // the list never skips a page that a permalink's out-of-order fetch left behind.
  function pool(deep, w) {
    var out = [];
    for (var i = pages.length - 1; i >= 0; i--) {
      var p = pages[i];
      if (p.cards) for (var j = 0; j < p.cards.length; j++) out.push(p.cards[j]);
      else if (!deep && !p.failed && inScope(p, w)) break;
    }
    return out;
  }

  // the next page this view needs, or null: an id's own page; every page in scope for a search or a filter; else the
  // next in scope once the list is within a click of what it holds
  function want(w) {
    var id = idOf(w), deep = w.length > 0 || picking();
    for (var i = pages.length - 1; i >= 0; i--) {
      var p = pages[i];
      if (p.cards || p.failed) continue;
      if (id) { if (id >= p.first && id <= p.last) return p; continue; }
      if (!inScope(p, w)) continue;
      return deep || hits.length < limit + PAGE ? p : null;
    }
    return null;
  }

  function pump() {  // one page in flight at a time, newest first
    if (busy || !man) return;
    var p = want(words());
    if (!p) return;
    busy = p;
    get(url(p.name)).then(function (d) {
      if (!d || !Array.isArray(d.cards)) throw new Error("it isn't a page of the index");
      p.cards = d.cards.filter(function (c) { return c && typeof c.id === "string" && typeof c.title === "string"; })
        .map(function (c) {
          c.cell = bare(obj(c.cell));
          c.when = String(c.when || "");
          c.hay = [c.id, c.title, c.when, String(c.cmds || "")].join("\n").toLowerCase();
          byId[c.id] = c;
          return c;
        }).reverse();
    }).catch(function (e) {
      p.failed = e.message;
    }).then(function () {
      busy = null;
      render(true);
    });
  }

  function drawGrids(counts) {
    gridsEl.querySelectorAll("button").forEach(function (b) {
      var g = b.getAttribute("data-grid");
      b.setAttribute("aria-pressed", g === grid ? "true" : "false");
      b.querySelector(".n").textContent = n(counts[g] || 0);
    });
  }

  function drawFacets(pool, exact) {  // exact: no search, so the manifest's counts are this view's
    var spec = obj(man.grids[grid]), fields = grid === "all" ? [] : Array.isArray(spec.fields) ? spec.fields : [];
    if (facetsEl.getAttribute("data-grid") !== grid) {
      facetsEl.replaceChildren();
      facetsEl.setAttribute("data-grid", grid);
      fields.forEach(function (f) {
        var lab = el("label", "cards-facet"), sel = el("select");
        sel.setAttribute("data-field", f);
        lab.append(el("span", null, f), sel);
        facetsEl.append(lab);
      });
    }
    facetsEl.querySelectorAll("select").forEach(function (sel) {
      var f = sel.getAttribute("data-field"), tally = bare();
      if (exact && !Object.keys(picks).some(function (k) { return k !== f; })) {
        var cells = obj(obj(spec.cells)[f]);
        Object.keys(cells).forEach(function (v) { if (cells[v] > 0) tally[v] = +cells[v]; });
      } else {
        pool.forEach(function (c) { var v = c.cell[f]; if (v && picked(c, f)) tally[v] = (tally[v] || 0) + 1; });
      }
      if (picks[f] && !tally[picks[f]]) tally[picks[f]] = 0;  // the one picked stays, at 0, so it can be undone
      var opts = [new Option("Any " + f, "")];
      Object.keys(tally).sort(function (a, b) { return tally[b] - tally[a] || (a < b ? -1 : 1); }).forEach(function (v) {
        opts.push(new Option(v + " (" + n(tally[v]) + ")", v));
      });
      sel.replaceChildren.apply(sel, opts);
      sel.value = picks[f] || "";
    });
  }

  function summary(c) {
    var s = el("summary"), head = el("span", "khead"), chips = el("span", "kcell");
    head.append(el("span", "kid", c.id), el("span", "ktitle", c.title));
    s.append(head);
    if (c.when) s.append(el("span", "kwhen", c.when));
    chips.append(el("span", "kchip kgrid", label(c.grid)));
    var fields = obj(man.grids[c.grid]).fields;
    (Array.isArray(fields) ? fields : []).forEach(function (f) {
      if (!c.cell[f]) return;
      var chip = el("span", "kchip", String(c.cell[f]));
      chip.title = f;
      chips.append(chip);
    });
    s.append(chips);
    return s;
  }

  // from: the cards already drawn, kept as they are (open ones stay open); left: the cards this view has, loaded or not
  function drawList(from, w, left) {
    var frag = document.createDocumentFragment(), upto = Math.min(limit, hits.length), deep = w.length > 0 || picking();
    for (var i = from || 0; i < upto; i++) {
      var c = hits[i], d = el("details", "kcard");
      d.id = c.id;
      d.append(summary(c), el("div", "kbody"));
      frag.append(d);
    }
    if (from) list.append(frag); else list.replaceChildren(frag);
    var next = want(w), reading = next && (deep || upto < Math.min(limit, left)), failed = pages.filter(function (p) {
      return p.failed;
    });
    var all = deep ? hits.length : left;
    more.hidden = upto >= all;
    more.textContent = "Show " + n(Math.min(PAGE, all - upto)) + " more · " + n(all - upto) + " left";
    if (!total) status.textContent = "0 cards";
    else if (reading && deep) {
      var read = 0, of = 0;
      pages.forEach(function (p) {
        if (!inScope(p, w)) return;
        of += p.count;
        if (p.cards || p.failed) read += p.count;
      });
      status.textContent = idOf(w) ? "Finding " + q.value.trim().toUpperCase() + "…" : "Searching " + n(read) + " of " +
        n(of) + " cards… " + n(hits.length) + (hits.length === 1 ? " match" : " matches") + " so far";
    } else if (!deep) status.textContent = reading && !upto ? "Loading the newest of " + n(left) + " cards…" :
      "Showing " + n(upto) + " of " + n(left) + " cards" + (reading ? "…" : "");
    else status.textContent = "Showing " + n(upto) + " of " + n(hits.length) + (hits.length === 1 ? " match" : " matches") +
      " · " + n(total) + " cards in all";
    if (failed.length) status.textContent += " · " + n(failed.length) + (failed.length === 1 ? " page" : " pages") +
      " of cards couldn't load (" + failed[0].failed + "): reload the page to try again";
    empty.hidden = hits.length > 0 || !!reading;
    if (!hits.length) empty.textContent = total ? "No card matches this search and these filters. Clear the search or pick All." :
      "No cards yet: the card store was empty when this site was built. Each Rune generation writes cards; python3 site/build.py --cards exports them here.";
  }

  function render(keep) {  // keep: leave the drawn cards in place when the new list starts with them
    var w = words(), deep = w.length > 0 || picking(), all = pool(deep, w);
    var text = w.length ? all.filter(function (c) { return matches(c, w); }) : all, counts = bare({ all: total });
    if (w.length) {
      counts.all = text.length;
      text.forEach(function (c) { counts[c.grid] = (counts[c.grid] || 0) + 1; });
    } else {
      Object.keys(man.grids).forEach(function (g) { counts[g] = +obj(man.grids[g]).count || 0; });
    }
    drawGrids(counts);
    var view = grid === "all" ? text : text.filter(function (c) { return c.grid === grid; });
    drawFacets(view, !w.length);
    hits = view.filter(function (c) { return picked(c); });
    var from = keep ? Math.min(list.children.length, hits.length) : 0;
    for (var i = 0; i < from; i++) if (list.children[i].id !== hits[i].id) { from = 0; break; }
    if (keep && from < list.children.length) from = 0;
    drawList(from, w, grid === "all" ? total : counts[grid] || 0);
    if (opening) {
      var d = $(opening);
      if (d && d.classList.contains("kcard")) {
        opening = null;
        d.open = true;
        d.scrollIntoView({ block: "start" });
      } else if (!want(w)) opening = null;
    }
    pump();
  }

  function shard(name) {
    if (!/^[a-z0-9-]+$/.test(name || "")) return Promise.reject(new Error("no shard"));
    return shards[name] || (shards[name] = get(url(name)));
  }

  function section(title, cls) {
    var s = el("section", "ksec " + (cls || ""));
    s.append(el("h3", null, title));
    return s;
  }

  function copyButton(what, text, label) {
    if (!navigator.clipboard) return null;
    label = label || "Copy";
    var b = el("button", "kcopy", label);
    b.type = "button";
    b.setAttribute("aria-label", "Copy " + what);
    b.addEventListener("click", function () {
      navigator.clipboard.writeText(text).then(function () {
        b.textContent = "Copied";
        setTimeout(function () { b.textContent = label; }, 1600);
      }, function () {});
    });
    return b;
  }

  function body(c, k) {
    var out = [], steps = section("Steps", "ksteps"), ol = el("ol");
    (k.steps || []).forEach(function (st) {
      var li = el("li");
      li.append(el("p", null, st.do));
      if (st.cmd) {
        var cmd = el("div", "kcmd"), code = el("code", null, st.cmd), b = copyButton("the command", st.cmd);
        cmd.append(code);
        if (b) cmd.append(b);
        li.append(cmd);
      }
      ol.append(li);
    });
    steps.append(ol);
    out.push(steps);
    if (k.example) { var ex = section("Worked example", "kex"); ex.append(el("p", "kpre", k.example)); out.push(ex); }
    if (k.check) { var ch = section("Check"); ch.append(el("p", "kpre", k.check)); out.push(ch); }
    if ((k.traps || []).length) {
      var tr = section("Traps"), ul = el("ul");
      k.traps.forEach(function (t) { ul.append(el("li", null, t)); });
      tr.append(ul);
      out.push(tr);
    }
    var foot = el("p", "kfoot"), a = el("a", "kperma", "Permalink · " + c.id), link = copyButton("the link to " + c.id,
      location.href.split("#")[0] + "#" + c.id, "Copy link");
    a.href = "#" + c.id;
    foot.append(a);
    if (link) foot.append(link);
    out.push(foot);
    return out;
  }

  function fill(d) {
    var c = byId[d.id], box = d.querySelector(".kbody");
    if (!c || box.getAttribute("data-state")) return;
    box.setAttribute("data-state", "loading");
    box.replaceChildren(el("p", "kwait", "Loading the card…"));
    shard(c.shard).then(function (all) {
      var k = all && all[c.id];
      if (!k) throw new Error("its shard doesn't hold it");
      box.replaceChildren.apply(box, body(c, k));
      box.setAttribute("data-state", "ok");
    }).catch(function (e) {
      delete shards[c.shard];  // the next open asks again
      box.removeAttribute("data-state");
      box.replaceChildren(el("p", "kerr", "Couldn't load this card's steps (" + e.message + "). Close it and open it again to retry."));
    });
  }

  function fromHash() {  // the id's own page is fetched; the card opens when it arrives
    var id = location.hash.slice(1);  // an id is plain ASCII: no decoding, so a malformed %-escape can't throw
    if (!/^K-\d+$/.test(id)) return false;
    q.value = id;
    grid = "all";
    picks = bare();
    limit = PAGE;
    opening = id;
    render();
    return true;
  }

  function start(data) {
    if (!data || !Array.isArray(data.pages) || !data.grids || typeof data.grids !== "object") throw new Error("the index isn't one");
    man = data;
    man.grids = bare(obj(data.grids));
    files = bare(obj(data.files));
    total = +data.count || 0;
    pages = data.pages.filter(function (p) { return p && /^index\.\d+$/.test(p.name); }).map(function (p) {
      return { name: p.name, count: +p.count || 0, first: num(p.first), last: num(p.last), grids: bare(obj(p.grids)) };
    });
    ["all"].concat(Object.keys(man.grids)).forEach(function (g) {
      var b = el("button", "cards-grid");
      b.type = "button";
      b.setAttribute("data-grid", g);
      b.append(el("span", null, label(g)), el("span", "n"));
      gridsEl.append(b);
    });
    root.classList.toggle("bare", total === 0);
    q.disabled = total === 0;
    if (!fromHash()) render();
  }

  gridsEl.addEventListener("click", function (e) {
    var b = e.target.closest("button[data-grid]");
    if (!b || !man) return;
    grid = b.getAttribute("data-grid");
    picks = bare();
    limit = PAGE;
    render();
  });
  facetsEl.addEventListener("change", function (e) {
    var f = e.target.getAttribute("data-field");
    if (!f) return;
    if (e.target.value) picks[f] = e.target.value; else delete picks[f];
    limit = PAGE;
    render();
  });
  q.addEventListener("input", function () {
    clearTimeout(timer);
    timer = setTimeout(function () { if (man) { limit = PAGE; render(); } }, 120);
  });
  more.addEventListener("click", function () { limit += PAGE; render(true); });
  list.addEventListener("toggle", function (e) {  // toggle doesn't bubble: heard on the way down
    var d = e.target;
    if (!d.classList || !d.classList.contains("kcard")) return;
    if (d.open) {
      fill(d);
      if (location.hash !== "#" + d.id) history.replaceState(null, "", "#" + d.id);
    } else if (location.hash === "#" + d.id) {
      history.replaceState(null, "", location.pathname + location.search);
    }
  }, true);
  window.addEventListener("hashchange", function () { if (man) fromHash(); });
  document.addEventListener("keydown", function (e) {
    if (e.key === "/" && !/^(INPUT|SELECT|TEXTAREA)$/.test(document.activeElement.tagName)) { e.preventDefault(); q.focus(); }
  });

  get(src).then(start).catch(function (e) {
    status.textContent = "Couldn't load the cards: " + e.message + ". Reload the page to try again.";
    root.classList.add("failed");
  });
})();
