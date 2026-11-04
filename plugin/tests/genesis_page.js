// T-2154: runs site/genesis/genesis.js against a stub DOM; prints what the scorecard table did with a hostile why.
const fs = require("fs"), vm = require("vm"), dir = process.argv[2], texts = [], html = [];
const data = JSON.parse(fs.readFileSync(dir + "/genesis.json", "utf8"));
function el() {
  const e = {children: [], classList: {add() {}, remove() {}, toggle() {}}, style: {}, dataset: {}, addEventListener() {},
    setAttribute() {}, getAttribute() { return null; }, closest() { return null; }, querySelector() { return null; },
    querySelectorAll() { return []; }, appendChild(c) { this.children.push(c); return c; }, append(...c) { this.children.push(...c); }};
  for (const k of ["textContent", "innerHTML"]) {
    let v = "";
    Object.defineProperty(e, k, {get() { return v; }, set(x) { v = String(x); (k === "innerHTML" ? html : texts).push(v); }});
  }
  return e;
}
async function page(extra) {
  texts.length = html.length = 0;
  const D = Object.assign({}, data, extra), els = {};
  const ctx = {document: {documentElement: el(), getElementById: id => els[id] = els[id] || el(), querySelector: () => null,
    addEventListener() {}, createElement: el, createTextNode: t => ({textContent: t})}, location: {hash: ""}, localStorage: {},
    matchMedia: () => ({matches: false}), fetch: async () => ({ok: true, json: async () => D}), setTimeout, console};
  vm.runInNewContext(fs.readFileSync(dir + "/genesis.js", "utf8"), ctx);
  await new Promise(r => setTimeout(r, 50));
  return {texts: texts.slice(), html: html.join("\n"), docs: !!(els["docs-body"] && els["docs-body"].innerHTML)};
}
// T-2852: `genesis_page.js DIR scale` prints what the Moons part did with moons_scale: a hostile family, then none
async function scale() {
  const bad = "<img src=x onerror=alert(1)>", says = (x, re) => x.texts.some(t => re.test(t));
  const s = await page({moons_scale: {funnel: {generated: 10000, write: {schema: 3}, dups: {exact: 40, embed: 1200, shingle: 7},
    rejected: {kill: 5000, tier: 2600, novelty: 900}, merged: 150, kept: 103, pending: 0},
    families: [{id: "F-007", size: 12, lead: "Lead " + bad, today: "today it can't", with_this: "with this it can, on Jarvis-big",
      tier: "massive", cold: "extreme", wild: 5, block: "M-61", stage: "kill", evidence: "ev " + bad, kinds: ["kill"]}],
    families_total: 340}});
  const n = await page({moons_scale: undefined});
  console.log(JSON.stringify({text: s.texts.some(t => t.includes("Lead " + bad)), markup: s.html.includes("onerror"),
    funnel: says(s, /10,000 generated/) && says(s, /40 exact/) && says(s, /1,200 by embedding/) && says(s, /5,000 at the kill test/)
      && says(s, /150 merged/) && says(s, /103 kept/),
    lead: says(s, /today it can't/) && says(s, /with this it can/), tiers: says(s, /massive.*extreme/), stage: says(s, /kill test/),
    evidence: s.texts.some(t => t.includes("ev " + bad)), more: says(s, /1 of 340 families/), none: says(n, /no funnel run yet/i),
    // the endpoint's name never shows: the data's "jarvis" reads as its role
    jarvis: !s.texts.concat(s.html).some(t => /jarvis/i.test(t)) && says(s, /on a large local model(?![\w-])/)}));
}
(async () => {
  if (process.argv[3] === "scale") return scale();
  const bad = "<img src=x onerror=alert(1)>";
  const a = await page({scorecard: [null, 7, {n: 1, name: "Initiative", state: "partial", closed: 2, graded: 4, why: bad}]});
  const b = await page({scorecard: undefined});
  // T-2263: the deciding long-horizon row; a key with a verdict, a key with only a reason, and no key at all
  const side = c => ({true_done_same: 2, false_done: 1, regressions: 0, resumes_needed: null, unfinished: 0, cost: c});
  const l = await page({long: {state: "ahead", goals: 3, foreman: side(1.5), plain: Object.assign(side(null), {true_done_same: 1})}});
  const r = await page({long: {state: "no common goals", goals: 0, foreman: null, plain: null}});
  const n = await page({long: undefined});
  const says = (x, re) => x.texts.some(t => re.test(t));
  console.log(JSON.stringify({text: a.texts.includes(bad), markup: a.html.includes("onerror"),
    none: b.texts.concat(b.html.split("\n")).some(t => /not graded yet/i.test(t)),
    docs: a.docs,
    long: says(l, /ahead/) && says(l, /Sampo/) && says(l, /\$1\.50/) && says(l, /cost \?/) && says(l, /2 of 3/),
    longReason: says(r, /no common goals/) && !says(r, /ahead|behind/), longNone: says(n, /no long-horizon run yet/i)}));
})();
