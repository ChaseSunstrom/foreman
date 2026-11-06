# Brainstorm — lens: delight

- **Animate the usage meter as a pace gauge** — FEATURE — value 4 — effort S — risk low — category: motion
  Why: the user watches plan limits closely; the sidebar meter already has an even-pace mark. Easing the fill, tinting amber when ahead of pace and holding calm when under it turns a number into a glanceable feeling.
  Done when: changing the usage value in a fixture animates the bar over ~300ms, and the bar shows the amber state only when usage is ahead of the pace mark. `prefers-reduced-motion` disables the animation.

- **Add a "Waiting on you" zero state that celebrates** — FEATURE — value 3 — effort S — risk low — category: polish
  Why: the Home page is built around yeses to give. Clearing the list should feel like a reward: a quiet check mark drawing itself and a line such as "Nothing needs you. 3 tasks moving."
  Done when: with zero waits and blocked items, Home renders the empty state with the SVG stroke animation and a live in-progress count.

- **Give every session a live pulse row** — FEATURE — value 4 — effort M — risk low — category: liveness
  Why: Live and Recent sessions exist and `fm ui --follow` provides a stream. A small breathing dot, a "typing…" shimmer on the last tool call and a streaming conversation tail make sessions feel alive instead of polled.
  Done when: a running session shows a pulsing dot and its new conversation lines slide in without a full re-render. A finished session's dot goes still.

- **Add a one-key "Yes" flow with a consent card** — FEATURE — value 5 — effort M — risk med — category: consent
  Why: the user wants to give only yes/no consent. A focused card (Y/N, a diff or brief summary, a cost flag) for each Waiting item, stepping through them like a card stack, would make clearing the queue fast. Constraint: the app never grants guard permissions itself, so Y here approves plans, Start or Drop, and for guard asks it deep-links to the agent session.
  Done when: pressing J/K moves through the waiting items, Y runs the allow-listed approve command, and a guard ask only opens its session. A test confirms no guard-grant command exists in the allow-list.

- **Make Ctrl+K a real command palette with previews** — FEATURE — value 4 — effort M — risk low — category: keyboard
  Why: the palette exists. Adding fuzzy search across tasks, sessions, decisions and inbox items, with a side preview of the highlighted item (brief or last message), makes "scroll/view everything" instant.
  Done when: typing a task id or phrase lists matches from at least 4 entity types with a preview pane. Enter navigates.

- **Draw the step bar as a living task timeline** — FEATURE — value 3 — effort M — risk low — category: visualization
  Why: the active task shows stages and a step bar. A horizontal timeline of steps, criteria ticking green as gates pass, and audits as small markers makes progress something people show others.
  Done when: Overview renders each step as a node, criteria changes animate to done, and a failed gate shows as an amber node.

- **Wild: Put a mini "Foreman at a glance" tray widget** — FEATURE — value 4 — effort M — risk low — category: ambient (wild)
  Why: assumption: Tauri can run a tray icon. The icon's dot shows waits (amber) or calm (graphite), and a click opens a popover of the top 3 asks with Y/N. The user could answer without opening the app.
  Done when: the tray icon changes state when waits appear, and the popover lists the waiting items.

- **Wild: Replay a session as a scrubbable time-lapse** — FEATURE — value 3 — effort L — risk med — category: replay (wild)
  Why: the conversation, tool calls, files and images are already readable. A timeline scrubber that replays the scratchpad files and pictures as they appeared makes reviewing a remote-control session feel like watching it happen.
  Done when: dragging the scrubber on a finished session updates the conversation and Files panes to that moment.

- **Wild: Show a device constellation on Home** — FEATURE — value 3 — effort M — risk low — category: visual identity (wild)
  Why: several devices over ssh and Tailscale are central. A restrained node graph, with each device a node, projects as small satellites and active sessions as moving pulses, could be the screenshot people share. It needs to stay graphite with one amber accent to avoid the AI-made look.
  Done when: Home has a devices view toggle, each node shows online or offline state, and session activity animates along it.

- **Wild: Add a weekly "Foreman wrapped" digest card** — FEATURE — value 3 — effort M — risk low — category: delight (wild)
  Why: `fm digest` and `fm cost` already exist and are unused by the app. A shareable card (tasks shipped, plan usage vs pace, friction fixed, longest-running session) rendered from them would make the self-improvement loop visible.
  Done when: a Digest page renders from `fm digest --json` and `fm cost` and exports as a PNG.

- **Add motion tokens and a reduced-motion pass** — CLEAN — value 3 — effort S — risk low — category: design system
  Why: the user wants it "animated" but "less AI made". One set of durations and easings, used everywhere, keeps motion restrained and consistent, and it keeps the app usable on low-power devices.
  Done when: all transitions use shared CSS variables, a grep finds no inline durations, and `prefers-reduced-motion` turns off every animation.
