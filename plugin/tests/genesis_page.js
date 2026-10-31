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
(async () => {
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
    long: says(l, /ahead/) && says(l, /foreman/) && says(l, /\$1\.50/) && says(l, /cost \?/) && says(l, /2 of 3/),
    longReason: says(r, /no common goals/) && !says(r, /ahead|behind/), longNone: says(n, /no long-horizon run yet/i)}));
})();
