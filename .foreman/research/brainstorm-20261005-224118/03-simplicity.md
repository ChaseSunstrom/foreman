# Brainstorm — lens: simplicity

- **Fold Remote control and Agents into Sessions and Devices** — CLEAN — value 4 — effort M — risk low — category: navigation
  Why: the user wants it "better organized" and "less AI made", and the nav has five items for what is really sessions and devices. Remote-control units are sessions, and agent wiring is a per-device property.
  Done when: the sidebar nav shows at most 3 entries, and starting or stopping a remote-control unit and Wire in / Remove still work from their new locations.

- **Merge Queue, Inbox and Blocked into one Work tab** — CLEAN — value 4 — effort M — risk low — category: project page
  Why: three searchable tables share the same type chips and the same brief drawer. The user wants to "scroll/view all inbox/queue items, everything", and one list with a state filter does that with less UI.
  Done when: the project page has a single Work tab where state chips switch between queue, inbox and blocked, and Start, Drop and Approve work from the drawer.

- **Merge Decisions, Activity and Gates into one History timeline** — CLEAN — value 3 — effort M — risk low — category: project page
  Why: these are three read-only views of what already happened. Project tabs drop from six to three: Overview, Work and History.
  Done when: one timeline interleaves decisions, ledger lines and gate runs, filterable by kind, with costly or outward decisions still flagged.

- **Make "Needs you" the landing page with j/k/Enter** — FEATURE — value 4 — effort S — risk low — category: keyboard
  Why: the user's core loop is giving yeses. Home already has Waiting on you; promoting it to the top and making it keyboard-driven shortens that loop. Enter opens the agent session where the reply happens, so the app never grants permissions itself.
  Done when: opening the app focuses the first waiting item, and j/k/Enter move through items and open the right session without the mouse.

- **Collapse tool calls to one-line summaries in conversations** — FEATURE — value 3 — effort S — risk low — category: sessions
  Why: the conversation view shows markdown, tool calls and images, and long sessions are noisy. Show messages by default and expand tool calls on click.
  Done when: a 200-tool-call session renders as messages plus grouped "ran 12 tools" rows, and each row expands to the full call.

- **Replace per-page polling with one `fm ui --follow` stream per device** — PERFORMANCE — value 3 — effort M — risk med — category: data layer
  Why: `fm ui --follow` and `fm projects --json` already exist as a device-wide read surface. One stream is simpler than many fetches and uses fewer ssh round trips for a user watching limits.
  Done when: with 3 devices connected, the app holds at most 1 long-lived command per device and pages update without their own timers.

- **Generate the allow-list, palette entries and buttons from one command table** — CLEAN — value 3 — effort M — risk med — category: architecture
  Why: the fm allow-list is a security boundary and Ctrl+K is the main action surface, so they must not drift apart. Assumption: they are currently defined separately.
  Done when: adding a command in one table makes it appear in the allow-list and the palette, and a test fails if a UI call uses a command outside the table.

- **Wild: Add a Home sentence instead of cards** — FEATURE — value 3 — effort S — risk low — category: delight
  Why: wild. A plain-language line such as "Quiet. 2 things need you. Laptop is at 61% of its 5-hour pace." at the top replaces several dashboard widgets. That answers "look less AI made".
  Done when: Home leads with a generated one-line summary that updates live and links each clause to its target.

- **Wild: Add a tray popover with the wait count and nothing else** — FEATURE — value 3 — effort M — risk low — category: ambient
  Why: wild. The simplest UI is none. A tray icon shows how many things need the user and the usage pace, and clicking lists them. Notifications already exist, so this extends them.
  Done when: the tray icon badge matches the waiting count, and the popover opens the matching item in the main window.

- **Wild: Add an "Ask in plain words" box that shows the exact fm command for a yes/no** — FEATURE — value 4 — effort L — risk med — category: command
  Why: wild. The user wants Claude to run everything with only yes/no consent. Match local phrases to allow-listed commands first, so no tokens are spent, and show the literal command with Run / Cancel. Assumption: a small local phrase matcher covers most requests.
  Done when: typing "start session on laptop in foreman" shows `fm session start …` for confirmation, and unmatched input falls back to the palette without calling a model.

- **Wild: Add a "Why is this here?" hide switch for every section** — FEATURE — value 2 — effort S — risk low — category: personalization
  Why: wild. Let the user hide any Home section or tab with one click and restore it from the palette, so the app converges on what they actually use.
  Done when: hidden sections stay hidden after restart, and "Show hidden sections" in the palette restores them.
