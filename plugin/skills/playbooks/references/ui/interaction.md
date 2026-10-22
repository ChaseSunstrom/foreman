<!-- Foreman's own playbook (written for Foreman, not ported). -->
# Interaction: feedback, keyboard, forms, words and the phone

Use when a web or app screen gets something to do: a form, a button that saves or sends, a menu, a list you act on, a sign-up, a checkout, a settings page. The sibling playbooks decide how a screen looks; this one decides how it behaves in the hand. Most UI that looks finished fails here first: the button that gives no sign it was pressed, the error that says "Invalid", the field hidden behind the phone's keyboard, the menu a keyboard can't leave.

Every rule below is pass or fail. Where a script can mark it, the script is in this file; where only a person (or a session that can see frames) can, the hand test says exactly what to do and what counts as a pass.

How it fits with the others: the stance and the density knob come from `design-direction.md` (`DESIGN.md`); focus-ring contrast and the 16 px body floor from `type-and-colour.md`; durations, easings, loading thresholds and the reduced path from `motion.md`; page structure and where things sit from `composition.md`; the frames at 360, 768 and 1440 from `visual-qa.md`. **Precedence:** where a number here and a sibling's overlap, the stricter one wins, and `DESIGN.md` may raise a floor in this file but never lower it (the Civic direction's 44 px targets everywhere beats the 24 px floor here). Time to *respond* is set here; the animation that fills that time is `motion.md`'s. Terminals: `terminal-ui.md`.

The code side (native controls, ARIA widgets, focus moves, autofill tokens) lives in the library cards listed at the end; this file says what has to be true, they say how to write it.

## The procedure

1. **List the verbs.** Write the actions the screen exists for, at most five, as verbs with an object: "create invoice", "send invoice", "mark paid". Everything below is checked per verb. More than five means the screen is doing two jobs: split it before you polish it.
2. **Fill the verb ledger** (Microcopy) before the first button is labelled.
3. **Build** with native controls first: `<button>`, `<a href>`, `<input>`, `<select>`, `<dialog>`, `<details>`. A `div` with a click handler is a defect the probe names.
4. **Run the probes** (`qa/interaction.mjs` on every view the task changed, `qa/double-press.mjs` on each verb that writes) and the grep in Microcopy.
5. **Do the four hand tests:** the unplugged walk (Keyboard and focus), the slow double press (Feedback, scripted), the wrong-input pass (Forms), the thumb pass (Mobile).
6. **Mark the Checks** at the end and put the result in the receipt line (Running it).

## Feedback

A person who acts and sees nothing assumes it didn't work, and acts again. Three deadlines, measured from the press:

| Within | What the person sees | Where | A fail looks like |
|---|---|---|---|
| the same frame (≤ 100 ms) | the control itself changes: pressed, checked, toggled, the typed letter | on the control | a button that looks the same until the server answers |
| 1 s | the result, or a sign that work has started (`motion.md`'s thresholds decide spinner versus nothing) | where the result will appear | a spinner in a far corner while the pressed button sits idle |
| 10 s | progress with a quantity or a stage ("Importing 1,240 of 3,000"), and a way to cancel or leave | on the thing being worked on | an indeterminate spinner on a 40 s export |
| longer | the work moves to the background; the person can leave the screen and is told when it's done | a lasting place (a list row, a notification), not only a toast | a modal that holds the screen hostage for a minute |

1. **Every verb has an end state the person can see:** done, failed with a way forward, or queued. Write them in the verb ledger. A save that succeeds silently fails this rule; a quiet "Saved" beside the button passes.
2. **Feedback lands where the eye is.** The change shows at the control or at the thing it changed. A toast alone is for results that happen off screen (an email sent, a file exported), and a toast for an action whose result is already visible is noise.
3. **One press, one action.** While a write is in flight, a second press does nothing: the button stays in place, shows its busy label from the verb ledger, and ignores presses (`aria-disabled="true"` plus a guard, or `disabled` for the duration). Pass: `qa/double-press.mjs` (below) prints `ok`. Money and messages to other people also carry an idempotency key, so a retry after a dropped connection can't charge or send twice (`fm lib show idempotency`).
4. **Undo beats confirm.** A reversible action happens at once and offers Undo for at least 5 s (the delete storyboard in `motion.md` is this rule animated). Confirm only what can't be undone, and then the confirm button repeats the verb and the object ("Delete 3 invoices"), never "OK".
5. **Optimistic only when it's safe.** Show the result before the server agrees only when all three hold: the server rarely refuses it, the change can be rolled back, and a refusal is shown in the same place as the change with the person's input kept. Never optimistic: payments, anything sent to another person, deletes without undo (`fm lib show optimistic-ui`).
6. **Failures say which kind.** Offline, refused (bad input, no permission) and broken (server error) read differently and offer different next steps: wait or retry, fix, or try later and quote a reference. One generic error for all three fails.
7. **Measured, not guessed.** With 4× CPU slowdown in Chrome DevTools, the Performance panel's live Interaction to Next Paint stays at or under 200 ms for every interaction on the main path (the "good" band of Core Web Vitals). A long handler is split or moved off the main thread (`fm lib show web-workers`), not hidden behind a spinner.

### Double-press probe

Copy into the project as `qa/double-press.mjs`. It opens the page, slows every request by 1.5 s (a phone on a poor connection, which is when people press twice), presses the named button twice on the same element, and counts the write requests that reach the app's own host. Run it once per verb that writes. It really presses the button, so the first write goes through: run it on the seeded fixture, never against data that matters.

```js
// qa/double-press.mjs: one press, one action (ui/interaction.md, Feedback rule 3).
// node qa/double-press.mjs http://localhost:5173/signup "Create account"
import { chromium } from "playwright";

const [url, label] = process.argv.slice(2);
if (!/^https?:\/\//.test(url || "") || !label) {
  console.error('usage: node qa/double-press.mjs <http(s) url> "<button name>"');
  process.exit(2);
}
const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto(url, { waitUntil: "load", timeout: 30000 });
const sent = [];
// from here on every request waits 1.5 s: a slow phone network, where people press twice
await page.route("**/*", async (route) => {
  const r = route.request();
  // writes to the app's own host; an analytics beacon elsewhere isn't the action
  if (r.method() !== "GET" && new URL(r.url()).origin === new URL(url).origin) sent.push(`${r.method()} ${new URL(r.url()).pathname}`);
  await new Promise((done) => setTimeout(done, 1500));
  await route.continue().catch(() => {}); // the page may have moved on
});
// the same element both times: a busy label ("Creating…") must not dodge the second press
const button = await page.getByRole("button", { name: label, exact: true }).elementHandle({ timeout: 5000 }).catch(() => null);
if (!button) {
  console.error(`no single button named "${label}" on ${url}`);
  await browser.close();
  process.exit(2);
}
await button.click();
await button.click({ timeout: 1000, force: true }).catch(() => {}); // gone, disabled or covered: guarded
await page.waitForTimeout(2500);
await browser.close();
console.log(sent.map((s) => `  ${s}`).join("\n") || "  (no request)");
const ok = sent.length === 1;
console.log(`${ok ? "ok" : "✗"} "${label}" pressed twice sent ${sent.length} write request(s); want 1`);
process.exit(ok ? 0 : 1);
```

A form the button can't submit until its fields are filled needs them filled first: seed the fixture's draft (`visual-qa.md`, Seeded fixture) or add `page.fill` lines before the first click. `(no request)` is a fail too: the press did nothing the network saw.

## Keyboard and focus

**The unplugged walk.** Put the mouse away and do every verb in the ledger with Tab, Shift+Tab, Enter, Space, Esc and the arrow keys. `qa/interaction.mjs` walks Tab for you and prints the path; the rest (arrows, Esc, Enter) is by hand or a few `page.keyboard.press` lines in the project's tests.

1. **Every stop can be seen.** A focus indicator at least 2 px thick with 3:1 contrast against the surface beside it (`type-and-colour.md`, Contrast), on `:focus-visible`. `outline: none` without a replacement fails. Probe: `NO FOCUS STYLE`.
2. **Only what's on screen takes focus.** A closed drawer, a collapsed menu, an off-canvas panel or a hidden tab panel is `inert`, `hidden` or `display: none`, not just moved out of view. Probe: `OFF SCREEN`, `NOT VISIBLE`.
3. **Nothing covers the focused thing.** A sticky header, cookie bar or chat bubble that hides the focused control fails (WCAG 2.4.11). Fix with `scroll-padding-top` (and `-bottom`) equal to the bars' heights. Probe: `COVERED`.
4. **Order follows reading order.** The Tab path matches the order a person reads the 1440 frame: left to right, top to bottom within each region, regions in the order they appear. No `tabindex` above 0. Probe: prints the path and fails any positive `tabindex`; you compare the path to the frame.
5. **A widget is one stop.** Tabs, menus, listboxes, radio groups, toolbars and grids take one Tab; arrows move inside (a roving `tabindex`, `fm lib show aria-patterns`). Pass: a 12-item menu costs one Tab, not twelve.
6. **Esc closes the top layer only, and focus goes home.** After Esc, focus is back on the control that opened the layer, and the next Tab goes to the control after it. Esc never closes two layers or throws away a half-filled form without asking.
7. **Focus moves only because the person did something.** It moves into an opened dialog (as it starts entering, `motion.md` rule 5), to the next row after a delete, to the new page's `h1` after a route change. A background refresh, a toast or a live result never steals it; those speak through a `role="status"` region (`fm lib show focus-management`).
8. **No traps.** Tab leaves every widget except a modal dialog, which keeps focus inside until it closes. Probe: `Tab cycles back to stop N`.
9. **A skip link** is the first stop on any view with navigation before the main content, and it becomes visible when focused.
10. **Enter submits** from any single-line field of a form (a real `<form>` with a submit button), and Space and Enter both press a button.
11. **Single-key shortcuts** (a letter with no modifier) can be switched off or remapped, or work only while their widget has focus (WCAG 2.1.4). Every shortcut is listed where people can find it (a `?` sheet, the menu item's hint).

## Forms

**Ask less.** Before styling a field, write what breaks if it's removed. "Might be useful later" is a fail: drop the field. Don't ask for what you already know (WCAG 3.3.7): a shipping address copies to billing with one tick.

**Layout**

1. One column. Two fields share a row only when they are one answer (expiry month and year), and never at 360.
2. A visible label above each field, always: a placeholder is an example, not a label, and it vanishes the moment someone types. Probe: `has no name (a placeholder is not a label)`.
3. Hint text sits between the label and the field, so it is read before typing, and is tied to the field with `aria-describedby`.
4. Mark the minority: if most fields are required, label the others "(optional)"; if most are optional, mark the required ones. Never a bare red asterisk without a legend.
5. Field width hints at the answer: a postcode field is short, a street field long.
6. The right keyboard and autofill: `type`, `inputmode` and `autocomplete` on every field that asks for a person's details (WCAG 1.3.5; tokens in `fm lib show forms`). Paste always works, including into password and code fields (WCAG 3.3.8).

**When to check: late to accuse, quick to forgive**

| Moment | What is checked | What shows |
|---|---|---|
| while typing a field for the first time | nothing, except help the person asked for (a password rule list ticking off, a counter near the limit) | no red |
| leaving a field that has content | its format: email shape, a date that exists, a number in range | an error under that field |
| leaving an empty required field | nothing: people Tab through forms to see them | no red |
| submit | every field, then the server | a summary above the form listing each error as a link to its field; focus moves to the summary |
| typing in a field that shows an error | that field, on every keystroke | the error clears the moment the value is good |

**Error messages**

1. Each one says what to do, in the field's own words, and gives an example when the format is the problem: "Enter an email address like name@example.com". Pass: every error string contains an instruction verb or an example value. "Invalid", "Required" or "Error" alone fails.
2. No blame and no jokes. "You entered an invalid date" becomes "Enter a date in the past".
3. The person's input stays exactly as typed, including after a server refusal and a page reload.
4. The error sits under its field, is tied to it with `aria-describedby`, and the field gets `aria-invalid="true"`. Colour is never the only sign: an icon or the word "Error" goes with it.

**Accept what people type**

Trim spaces, accept any case in emails and codes, accept spaces and dashes in card and phone numbers, accept a pasted one-time code (one field with `autocomplete="one-time-code"` beats six boxes). Pass: `" 4111 1111-1111 1111 "` goes into the card field and is accepted.

**The submit button**

Never disabled to signal "not ready yet": the person can't learn why. It stays pressable and the press shows the errors. It is disabled (or `aria-disabled`) only while the request is in flight, showing its busy label.

**Nothing typed is lost**

A form of more than five fields survives Back, a reload and a session timeout: it saves a draft, or the browser warns before leaving. Pass: fill five fields, reload, the values are still there or a warning appeared first.

**The wrong-input pass (hand test).** For each field: submit it empty, submit it wrong (a letter in a number, a date that doesn't exist, 300 characters in a name), paste a value with spaces around it. Each error says what to do; nothing typed vanished; fixing it clears the error without another submit.

## Microcopy

Words are interface. The same action called by three names across a flow reads as three different actions, and a button that says "OK" makes the person read the whole dialog again to know what OK does.

1. **Buttons are verbs.** A verb, plus the object when the screen has more than one thing it could act on: "Save draft", "Send invoice", "Create account". Never "OK", "Submit", "Yes", "No" or "Confirm" alone.
2. **One name per action, one name per thing.** The verb in the button is the verb in the busy label, the success message, the error and the history line. The noun is the same everywhere too: not "project" on one screen and "workspace" on the next. The verb ledger enforces it.
3. **A dialog's title asks, its buttons answer.** "Delete 'Q3 report'?" is answered by "Delete report" and "Keep it", and the body says what happens next ("It moves to Trash for 30 days").
4. **Errors: what happened, what to do, then a reference.** "Couldn't send the invoice. Try again in a minute; if it keeps failing, give support the code 7F3A." The code comes after the human sentence, never instead of it.
5. **Empty states say what goes here and how to start:** "No invoices yet" plus the one action that makes the first one. "No data" fails.
6. **The person's words, not the system's:** no "entity", "null", "payload", "sync conflict (409)" in anything a person reads.
7. **Sentence case, digits for numbers, real plurals.** "3 files deleted" and "1 file deleted", never "file(s)". A relative time ("2 hours ago") within the week, a date after that.
8. **Links name where they go:** "Read how roles work", not "Click here" or a bare "Learn more".
9. **No "simply", "just" or "easily"** in instructions: they tell a stuck person the problem is them.
10. **It fits at 360 in the longest language you ship.** German runs about a third longer than English. Pass: with the longest locale (or a pseudo-locale that pads every string by 40%) at 360, no button truncates or wraps to a third line (`fm lib show i18n`).

### The verb ledger

One row per verb from the procedure, written before the buttons are labelled and kept in the task's brief or PR. Each row uses one verb stem in every column.

| Verb | Button | Busy | Done | Failed | History |
|---|---|---|---|---|---|
| create invoice | Create invoice | Creating… | Invoice INV-104 created | Couldn't create the invoice: the customer has no billing address. Add one, then try again. | Created by Ana Ruiz |
| send invoice | Send invoice | Sending… | Sent to billing@acme.test | Couldn't send: you're offline. It will send when you reconnect. | Sent by Ana Ruiz to billing@acme.test |
| mark paid | Mark as paid | Marking… | Marked as paid · Undo | Couldn't mark as paid. Try again; your other changes are saved. | Marked as paid by Ana Ruiz |

Pass: no row mixes stems (Send / Deliver / Dispatch), and a grep for each Button string finds the same words in the code's busy, success and error strings.

### Before and after

| Where | Before | After | What changed |
|---|---|---|---|
| form button | Submit | Create account | names the result |
| delete dialog | Are you sure? [Yes] [No] | Delete "Q3 report"? It moves to Trash for 30 days. [Delete report] [Keep it] | the buttons answer the question; says what happens |
| email error | Invalid email | Enter an email address like name@example.com | an instruction and an example |
| date error | Invalid date | Enter a date of birth in the past | says what a good value is |
| password rule | Password does not meet requirements | Use at least 12 characters (a list ticks off as you type) | the rule before the failure |
| offline | Oops! Something went wrong. | Couldn't save: you're offline. Your changes are kept and will save when you reconnect. | what happened, what's safe, what next |
| server error | Error 500 | Couldn't send the invoice. Try again in a minute; if it keeps failing, give support the code 7F3A. | the code after the sentence |
| no permission | Access denied | Only workspace owners can change billing. Ask Maria Chen, the owner. | who can, and who to ask |
| empty list | No data | No invoices yet. [Create invoice] | what goes here and how to start |
| after archive | Success! | Project archived. [Undo] | names what happened; offers the way back |
| long wait | Loading… | Importing 1,240 of 3,000 contacts | a quantity, so the wait has an end |
| plural | 1 file(s) deleted | 1 file deleted | a real plural |
| link | Click here to learn more about roles | Read how roles work | the link names its destination |
| one flow, three names | [Post] → "Published!" → history "Went live" | [Publish] → "Published" → "Published by Ana Ruiz" | one verb across the flow |

### Copy grep

Run from the project root; it reads the UI source and locale files. Each hit is a string to rewrite, or one you justify in the receipt (a "No" in a yes/no survey question is fine). A hit inside a code comment doesn't count.

```bash
grep -rnoiE ">\s*(ok|submit|yes|no|click here|here|learn more|read more)\s*<|\b(oops|whoops|uh-oh)\b|something went wrong|invalid (input|value|entry|data)|an error (has )?occurred|[a-z]\(s\)( [a-z]|[\"'\`<])|\b(simply|easily)\b" \
  --include=*.{html,js,jsx,ts,tsx,vue,svelte,astro,json,yml,yaml,ftl,po,strings,xml} src
```

It finds the patterns of bad copy, not bad copy: a button labelled `{t("submit")}` hides from it, so the locale files it reads are in the list too (`json`, `yml`, `po` and the rest). Swap `src` for the folders the UI lives in. The `{…}` list needs bash or zsh; plain `sh` takes it literally and finds nothing.

## Mobile

The phone is the first layout, not a squeezed desktop. 360 px wide is the width that must work (`visual-qa.md` takes its frames there).

1. **Targets.** Every control is at least 24×24 CSS px (WCAG 2.5.8; the probe fails anything smaller). The main path's controls and anything pressed often are at least 44×44 (the probe lists every target between 24 and 44 for you to judge). A link inside a sentence is exempt. The hit area may be larger than what's drawn (padding, or a `::after` that extends it); adjacent targets keep at least 8 px between their hit areas.
2. **The thumb pass (hand test).** At 360×800, the primary action of each view sits in the lower half of the screen or directly after the last field in the flow; nothing on the main path needs a reach to a top corner. Destructive actions are not next to the primary one and not in the bottom corner where the thumb rests. Pass: mark each view's primary action's position on its 360 frame.
3. **Nothing needs hover.** Anything shown on hover (row actions, tooltips that carry information, menus) is also reachable by a tap and by focus. Under `@media (hover: none)` row actions are visible or behind an overflow button.
4. **Every gesture has a button.** Swipe to delete also has a menu item; drag to reorder also has Move up and Move down (WCAG 2.5.7, `fm lib show drag-and-drop`); a pinch-zoomed map also has + and − (WCAG 2.5.1).
5. **The on-screen keyboard hides nothing you need.** Focusing the last field leaves that field and the submit button visible above the keyboard. Full-height layouts use `dvh` or `svh`, not `vh`; a bottom bar that must ride above the keyboard needs `interactive-widget=resizes-content` in the viewport meta on Chromium and a `visualViewport` resize handler on Safari. Pass: on a real phone or a device emulator, focus the last field of every form.
6. **Zoom stays on, inputs don't trigger it.** The viewport never sets `user-scalable=no` or a `maximum-scale` below 2, and form text is at least 16 px so iOS doesn't zoom on focus. Probe: both.
7. **Safe areas.** Fixed bars at the bottom pad by `env(safe-area-inset-bottom)` when the viewport uses `viewport-fit=cover`; nothing pressable sits under the home indicator or a notch.
8. **Width.** No horizontal scroll at 360 (the frame script checks it), and text pages reflow at 320 px and at 200% zoom without losing content (WCAG 1.4.10; `type-and-colour.md` checks a hero headline). Wide tables scroll inside their own box, never the page.
9. **Landscape works.** The orientation isn't locked, and at 800×360 sticky bars take no more than a fifth of the height together, so a form still shows a field and its label.
10. **Pressed looks pressed.** Every control has an `:active` state; removing the tap highlight (`-webkit-tap-highlight-color: transparent`) is allowed only when that `:active` state exists.

## Interaction probe

Copy into the project as `qa/interaction.mjs`, next to the frame script, with the project's own Playwright (`visual-qa.md` says how to get it). For each path it does two passes and prints text, so a model that can't see images can use it as well as a person:

- **@360 touch** (360×800, touch, phone): the viewport meta, every control's accessible name, positive `tabindex`, role-only controls the keyboard can't reach, `onclick` on things that aren't controls, form text under 16 px, and target sizes: under 24 fails, 24 to 44 is listed.
- **keyboard** (1440×900): presses Tab until the path ends, wraps, loops or reaches 150 stops, and for each stop prints what took focus and whether it is visible, on screen, uncovered and styled differently from its unfocused self.

```js
// qa/interaction.mjs: the scripted half of Foreman's interaction playbook (ui/interaction.md).
// node qa/interaction.mjs http://localhost:5173 / /signup /settings
import { chromium } from "playwright";

const [base, ...paths] = process.argv.slice(2);
if (!/^https?:\/\//.test(base || "") || !paths.length) {
  console.error("usage: node qa/interaction.mjs <http(s) base url> <path>...");
  process.exit(2);
}
const MAX_STOPS = 150; // more tab stops than this on one view needs a skip link, not a longer walk

// Installed in every page before its own scripts: the names and looks both passes share.
function helpers() {
  const text = (el) => (el ? el.innerText || el.textContent || "" : "").replace(/\s+/g, " ").trim();
  const name = (el) => {
    const by = el.getAttribute("aria-labelledby");
    if (by) return by.split(/\s+/).map((id) => text(document.getElementById(id))).join(" ").trim();
    return (el.getAttribute("aria-label") || "").trim() || [...(el.labels || [])].map(text).join(" ").trim()
      || (/^(submit|button|reset)$/.test(el.type) ? el.value : "")
      || (el.matches("input,select,textarea") ? "" : text(el))
      || el.querySelector("img[alt]")?.alt.trim() || text(el.querySelector("svg title")) || (el.title || "").trim();
  };
  const tag = (el) => {
    const n = name(el) || (el.placeholder ? `placeholder: ${el.placeholder}` : "");
    return `${el.tagName.toLowerCase()}${el.id ? "#" + el.id : ""}${el.tagName === "INPUT" ? `[${el.type}]` : ""} "${n.slice(0, 40)}"`;
  };
  // what focus can change: the element, its wrapper, the sibling a hidden native input styles, its labels
  const near = (el) => [el, el.parentElement, el.nextElementSibling, ...(el.labels || [])];
  const look = (el) => near(el).map((e) => {
    if (!e) return "";
    const s = getComputedStyle(e);
    return [s.outlineStyle, s.outlineWidth, s.outlineColor, s.boxShadow, s.borderColor, s.backgroundColor, s.color, s.textDecorationLine].join("|");
  }).join("/");
  const settle = (el) => near(el).forEach((e) => e?.getAnimations?.().forEach((a) => { try { a.finish(); } catch {} }));
  window.__qa = { text, name, tag, look, settle, stops: [], looks: [] };
}

// Phone width, touch: what a script can name without a person.
function phoneProbe() {
  const { text, name, tag } = window.__qa;
  const bad = [], small = [];
  const shown = (el) => {
    const r = el.getBoundingClientRect();
    return r.width * r.height > 0 && r.right > 0 && getComputedStyle(el).visibility !== "hidden" && !el.closest("[inert],[aria-hidden=true]");
  };
  const vp = document.querySelector('meta[name="viewport"]')?.content || "";
  if (!vp) bad.push("no <meta name=viewport>: phones draw it as a shrunken desktop page");
  const max = vp.match(/maximum-scale\s*=\s*([\d.]+)/i);
  if (/user-scalable\s*=\s*(no|0)\b/i.test(vp) || (max && +max[1] < 2)) bad.push(`viewport "${vp}" stops pinch zoom`);

  const CONTROLS = "a[href],button,input:not([type=hidden]),select,textarea,summary,"
    + "[role=button],[role=link],[role=checkbox],[role=radio],[role=switch],[role=tab],[role=menuitem],[role=option]";
  for (const el of document.querySelectorAll(CONTROLS)) {
    const labels = [...(el.labels || [])].filter(shown);
    if (!shown(el) && !labels.length) continue;
    const field = el.matches("input:not([type=submit],[type=button],[type=reset],[type=image]),select,textarea");
    if (!name(el)) bad.push(`${tag(el)} has no name${field && el.placeholder ? " (a placeholder is not a label)" : ""}`);
    if (el.tabIndex > 0) bad.push(`${tag(el)} has tabindex=${el.tabIndex}: tab order no longer follows the page`);
    if (field && !/^(checkbox|radio|range|color|file)$/.test(el.type) && parseFloat(getComputedStyle(el).fontSize) < 16)
      bad.push(`${tag(el)} text is ${getComputedStyle(el).fontSize}: iOS zooms the page on focus below 16px`);
    if (el.matches("[role]:not(a,button,input,select,textarea,summary)") && el.tabIndex < 0)
      bad.push(`${tag(el)} has role=${el.getAttribute("role")} but the keyboard can't reach it`);
    // a link inside a sentence is exempt from target size; a link standing on its own is not
    const p = el.parentElement;
    if (el.tagName === "A" && getComputedStyle(el).display === "inline" && p?.matches("p,li,td,dd,blockquote,figcaption,span,em,strong,small")
      && text(p) !== text(el)) continue;
    const rs = [el, ...labels].map((e) => e.getBoundingClientRect()).filter((r) => r.width * r.height > 0);
    const w = Math.round(Math.max(...rs.map((r) => r.right)) - Math.min(...rs.map((r) => r.left)));
    const h = Math.round(Math.max(...rs.map((r) => r.bottom)) - Math.min(...rs.map((r) => r.top)));
    if (w < 24 || h < 24) bad.push(`${tag(el)} is ${w}×${h} px, under the 24×24 floor`);
    else if (w < 44 || h < 44) small.push(`${tag(el)} ${w}×${h}`);
  }
  for (const el of document.querySelectorAll("[onclick]:not(a,button,input,select,textarea,summary,[role])"))
    bad.push(`${tag(el)} takes clicks but isn't a control: no keyboard, no role`);
  return { bad, small };
}

// After each Tab: what has focus, and can a sighted keyboard user see it.
function stop() {
  const qa = window.__qa;
  let el = document.activeElement;
  while (el?.shadowRoot?.activeElement) el = el.shadowRoot.activeElement;
  if (!el || el === document.body || el === document.documentElement) return null;
  const first = qa.stops.indexOf(el);
  qa.stops.push(el);
  qa.settle(el);
  qa.looks.push(qa.look(el));
  const box = [el, ...(el.labels || [])].map((e) => e.getBoundingClientRect()).find((r) => r.width * r.height > 0);
  const flags = [];
  if (!box || getComputedStyle(el).visibility === "hidden") flags.push("NOT VISIBLE");
  else {
    const x = box.left + box.width / 2, y = box.top + box.height / 2;
    if (x < 0 || y < 0 || x >= innerWidth || y >= innerHeight) flags.push("OFF SCREEN");
    else {
      const hit = document.elementFromPoint(x, y);
      if (!hit || !(el.contains(hit) || [...(el.labels || [])].some((l) => l.contains(hit)))) flags.push("COVERED");
    }
  }
  return { first, desc: qa.tag(el), flags };
}

// After the walk, nothing focused: which stops look the same as when they had focus.
function unchanged() {
  const qa = window.__qa;
  document.activeElement?.blur();
  return qa.stops.map((el, i) => { qa.settle(el); return qa.look(el) === qa.looks[i]; });
}

const browser = await chromium.launch();
const bad = [];
for (const path of paths) {
  const url = new URL(path, base).href;
  const open = async (opts) => {
    const ctx = await browser.newContext(opts);
    await ctx.addInitScript(helpers);
    const page = await ctx.newPage();
    await page.goto(url, { waitUntil: "load", timeout: 30000 });
    await page.evaluate(() => document.fonts.ready);
    return { ctx, page };
  };

  let { ctx, page } = await open({ viewport: { width: 360, height: 800 }, hasTouch: true, isMobile: true, deviceScaleFactor: 2 });
  const p = await page.evaluate(phoneProbe);
  console.log(`${path} @360 touch: ${p.bad.length} finding(s), ${p.small.length} target(s) between 24 and 44 px`);
  for (const s of p.small) console.log(`  · ${s}`);
  bad.push(...p.bad.map((b) => `${path} @360: ${b}`));
  await ctx.close();

  ({ ctx, page } = await open({ viewport: { width: 1440, height: 900 } }));
  const stops = [];
  let end = `stopped after ${MAX_STOPS} stops`;
  for (let n = 0; n < MAX_STOPS; n++) {
    await page.keyboard.press("Tab");
    const s = await page.evaluate(stop);
    if (!s) { if (stops.length) { end = "end of page"; break; } continue; }
    if (s.first >= 0) {
      end = s.first === 0 ? "wrapped to the first stop" : "loop";
      if (s.first > 0) bad.push(`${path} keyboard: Tab cycles back to stop ${s.first + 1} ${s.desc}; the rest of the page is out of reach`);
      break;
    }
    stops.push(s);
  }
  const same = stops.length ? await page.evaluate(unchanged) : [];
  console.log(`${path} keyboard: ${stops.length} stop(s), ${end}`);
  stops.forEach((s, i) => {
    if (same[i]) s.flags.push("NO FOCUS STYLE");
    console.log(`  ${String(i + 1).padStart(3)} ${s.desc}${s.flags.length ? "  ✗ " + s.flags.join(", ") : ""}`);
    if (s.flags.length) bad.push(`${path} keyboard: stop ${i + 1} ${s.desc}: ${s.flags.join(", ").toLowerCase()}`);
  });
  if (!stops.length) bad.push(`${path} keyboard: Tab reaches nothing`);
  await ctx.close();
}
await browser.close();
for (const b of bad) console.log(`✗ ${b}`);
console.log(`${bad.length ? "✗" : "ok"} ${paths.length} view(s), ${bad.length} finding(s)`);
process.exit(bad.length ? 1 : 0);
```

A clean run on a sign-up page reads:

```
/signup @360 touch: 0 finding(s), 0 target(s) between 24 and 44 px
/signup keyboard: 7 stop(s), end of page
    1 a "Skip to content"
    2 a "Home"
    3 a "terms"
    4 input#email[email] "Email"
    5 input[checkbox] "Send me the monthly letter"
    6 button "Create account"
    7 a "Back to top"
ok 1 view(s), 0 finding(s)
```

**What it can't see,** so the hand tests stay: whether the Tab order matches the reading order (it prints the path; you compare), arrow keys inside widgets, Esc and where focus returns, focus-ring contrast (it sees that the style changes, not that the change is visible enough: `type-and-colour.md` measures it), error wording and timing, the on-screen keyboard, the thumb pass, anything that happens after a click, and controls inside an iframe or a shadow root (the walk follows focus into an open shadow root but stops at an iframe; the phone pass skips both). A view behind a login needs the session first: add a `storageState` to both `newContext` calls. It reads the page as it loads, so a menu or dialog is probed only if the path opens it (a `?open=…` route, or a project test that opens it and calls the same checks).

## Running it

- **In a Claude Code session** (Foreman's plugin): start the app on the seeded fixture, run `node qa/interaction.mjs <base> <paths…>`, each `node qa/double-press.mjs <url> "<button>"`, and the copy grep with Bash. Then compare the printed Tab path with each view's 1440 frame from `visual-qa.md` (open the PNG with the Read tool), and use the 360 frames for the thumb pass. Arrows, Esc and the wrong-input pass are a few lines of Playwright run the same way (`page.keyboard.press("Escape")`, then read `document.activeElement`); write them as project tests when the screen stops changing.
- **In `fm code`:** its model reads text, which is what the probes print. Put each probe in the request as a criterion's verify ("done when the sign-up form passes the interaction probe :: node qa/interaction.mjs http://localhost:5173 /signup"); `--verify` fits a fix the probe already fails on (a missing label, a trap), since `--verify` must fail before the change. Put the verb ledger in the request as text, so the plan writes those exact strings. The hand tests stay `pending` in the receipt for a Claude Code session or a person.
- **By hand:** the same commands in a terminal, the unplugged walk in a real browser, the thumb pass and the keyboard check on a real phone.

The receipt is one line in the task's evidence, next to the visual-QA one:

```
interaction <commit>: probe ok (<views>), double-press ok (<verbs>), copy grep <n> justified, hand: walk ✓ wrong-input ✓ thumb ✓ keyboard-cover ✓
```

From `fm code`, the `hand:` part reads `hand: pending` until someone does them; a hand test that finds something becomes a fix task (`fm capture`).

## Checks

- [ ] The verb ledger exists in the brief or PR, one stem per row, and the built strings match it.
- [ ] `qa/interaction.mjs` exits 0 for every view the task changed.
- [ ] `qa/double-press.mjs` prints `ok` for every verb that writes.
- [ ] The copy grep's hits are fixed, or each is justified in the receipt.
- [ ] Every target the probe listed between 24 and 44 px is either off the main path or made bigger.
- [ ] The printed Tab path matches the reading order of the 1440 frame, and the unplugged walk completes every verb with Tab, Shift+Tab, Enter, Space, Esc and the arrows.
- [ ] Esc closes one layer and returns focus to its opener; no background update moves focus.
- [ ] The wrong-input pass: every error says what to do, nothing typed is lost, and fixing a field clears its error without another submit.
- [ ] The submit button is never disabled to signal invalid input.
- [ ] At 360×800 each view's primary action is in the lower half or right after the last field, and focusing the last field of each form leaves it and its submit button above the on-screen keyboard.
- [ ] Every gesture and every hover-only reveal has a tap and keyboard equivalent.
- [ ] With 4× CPU slowdown, every interaction on the main path shows Interaction to Next Paint at or under 200 ms.

## Library cards

The code side lives in the stack library: `fm lib show forms` (native controls, autofill tokens, server-side errors), `fm lib show input-validation` (the server half of every check above), `fm lib show react-hook-form`, `fm lib show focus-management` (where focus goes after open, close, delete and navigation), `fm lib show keyboard-navigation`, `fm lib show aria-patterns` (roving `tabindex`, menus, tabs, comboboxes), `fm lib show dialogs`, `fm lib show toasts`, `fm lib show optimistic-ui`, `fm lib show idempotency`, `fm lib show skeleton-loading`, `fm lib show drag-and-drop`, `fm lib show responsive-design` (viewport, breakpoints, pointer and hover queries), `fm lib show i18n` (string length, plurals), `fm lib show accessibility`, `fm lib show accessibility-testing` (axe in CI, which covers what this probe doesn't), `fm lib show playwright`, `fm lib show web-workers`. Add `--section verify` for each card's checks.
