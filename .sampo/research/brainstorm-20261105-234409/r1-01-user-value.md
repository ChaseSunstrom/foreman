# Brainstorm — lens: user value

- **Print "what you no longer have to do" in the morning card** — FEATURE — value 5 — effort M — risk low — category: user value
  Why: The user's words are full of "don't interrupt me," "keep working the rest of the queue without waiting," "never block on the user." They value autonomy above polish. The existing "minutes-saved estimate" idea is a static number; what's missing is the *behavioral* delta: list the 2–3 manual actions the user performed last week that Sampo now handles unprompted (e.g., "you re-typed the ship command 4×; the drive did it"), so the value is visible as their own saved behavior, not a metric Sampo invented.
  Done when: `sampo status` prints a "Saved you" section listing at least one user action from the last 7 days that no longer required a manual keystroke, with a link to the ledger line proving it.

- **Turn every pushback into a "you told me once" receipt** — FEATURE — value 5 — effort S — risk low — category: user value
  Why: The user repeatedly corrects Sampo ("not a breakage," "absorbed by T-2893," "dropped: …"). The standing rule says "every user steer becomes a standing rule plus an automatic check." But there is no *user-facing* confirmation that the correction stuck. The user's deep need is trust that Sampo actually internalized their pushback and won't repeat the mistake.
  Done when: After any user "dropped" or "steered" message, the next `sampo status` prints "Remembered: <one-line steer> — check: <command> — passes."

- **Predict the user's next "I didn't ask for that"** — FEATURE — value 5 — effort M — risk med — category: user value
  Why: The user's drops section shows repeated frustration with Sampo over-reaching (wrong tool installs, misreading a rename, assuming a tool is missing). The standing rule says "never interrupt the user mid-run." The unspoken need: before Sampo does something the user didn't ask for, it should *name the boundary* and show what it will NOT do. The "scope dial with a price preview" idea covers width; this covers the *negative* scope explicitly.
  Done when: Every unattended task that touches a file or verb not named in the brief prints a "Not doing: <list of adjacent actions I will not take>" line at start.

- **One-line "is Sampo still earning its tokens?" in `sampo doctor`** — FEATURE — value 4 — effort S — risk low — category: user value
  Why: The user explicitly steered: "I don't want to just cap the cost… I want it to still get done without burning a fuck ton of money, and quick." The lean-substance rule and "needed-share" ideas exist, but the user never *sees* whether the injected context is still pulling its weight per session. They need a running, visible answer: "This session's Sampo injection earned 3 correct tool calls and 1 prevented Ward violation."
  Done when: `sampo doctor` prints "Sampo earned: N correct calls, M violations prevented, K tokens injected" for the current session, computed from the hook ledger.

- **Make the "left out" list actionable from the phone** — FEATURE — value 4 — effort M — risk med — category: user value
  Why: The user works across machines and sessions ("manage all of that across sessions too, like a consensus thing"). The "Left out" slip and "pocket left-out digest" ideas exist but are read-only. The user's unspoken need: when they see a gap on their phone during a meeting or commute, they want to *promote it to a task in one tap*, not wait for the next session. The "promote a left-out cell to a task in one key" idea is the CLI version; this is the remote version.
  Done when: A phone push notification for the morning card includes a tappable "Build this" button on each left-out item, which files the task via the loopback webhook with HMAC.

- **Show "what would break if I said no to this steer?"** — FEATURE — value 4 — effort M — risk low — category: user value
  Why: The user writes 80+ standing steers. The "give each steer a review-by date and an evidence query" idea covers staleness, but the user's deeper need is understanding the *consequence* of a steer before they remove or relax it. They want to know: "If I stop enforcing 'no idea is killed for ambition,' what actually happens?" The answer should come from the ledger, not from Sampo's opinion.
  Done when: `sampo steer show <id>` prints "Last 30 days without this rule: N tasks filed, M dropped without retry" computed from the ledger.

- **Draft the "I'll be annoyed if…" line at intake** — WILD — value 5 — effort S — risk low — category: user value
  Why: The user's words reveal a pattern: they specify what they want, but the *negative* specification ("I don't want X," "never Y," "don't do Z") is what actually defines satisfaction. The "ask for an 'I'll be annoyed if…' line at intake and compile it into a clause" idea exists in the goal space but not in the brief space. Making this a *default prompt* at every `sampo task add` would turn the user's most important value signal (annoyance threshold) into a first-class, checkable clause.
  Done when: `sampo task add` prompts "What would make you delete this task in 10 seconds? (one line)" and files that line as a negative Done-when clause.

- **Weekly "what I got wrong about you" confession** — WILD — value 5 — effort M — risk med — category: user value
  Why: The user's drops section is essentially a log of Sampo's misreads of their intent. The "keep a 'what I assumed about you' file the user can strike through" idea is static. The wild version: once a week, a cold child reads the last week's ledger (the user's actual messages, drops, steers) and writes a plain-language confession: "I assumed you wanted X, but you actually wanted Y. Here are the 3 moments." This builds trust by making Sampo's model of the user *visible and challengeable*.
  Done when: `sampo week review` generates a "Misreads" section listing at least one assumption Sampo made that the user's words contradicted, with the ledger line for each.

- **Let the user type "I meant X, not Y" and watch it propagate** — FEATURE — value 4 — effort M — risk low — category: user value
  Why: The user's "already built" drops and "dropped: not a breakage" corrections are all instances of "I meant X, not Y." The "compile 'I meant X, not Y' into a reading pair" idea exists but is passive. The user wants *active* propagation: when they correct a term or a path, Sampo should immediately scan open tasks, steers, and injected text for the old reading and show what it will change, then apply with one key.
  Done when: Typing `sampo correct "foreman" → "sampo" --open` lists the 5 open tasks and 2 steers that still use the old term, and `--apply` rewrites them.

- **Show the user's "cost of being interrupted" as a live gauge** — FEATURE — value 4 — effort S — risk low — category: user value
  Why: The user's standing rule: "Never interrupt the user mid-run." But Sampo has no *measure* of how costly interruptions are to this user. The "interrupt ledger with a zero target" idea exists but is a count. The user value version: track the *time lost* (session paused, context rebuilt) per interruption and print it as "You lost 14 minutes this week to interruptions." This makes the "never interrupt" rule *felt* rather than abstract.
  Done when: The morning card prints "Interruptions cost: N minutes (M times, avg K sec context loss)."

- **A "would I have asked?" shelf for overnight work the user never wanted** — WILD — value 4 — effort M — risk low — category: user value
  Why: The user's drops section shows Sampo repeatedly doing work the user didn't want (bulk card writing on Haiku when local was fine, running a review that was "stale"). The "let the user veto a past Foreman decision and replay the run without it" idea covers the past. The wild version: maintain a *living* shelf of unattended actions that the user neither thanked for nor complained about—silent acceptance—and periodically ask: "You've let these 7 actions slide. Do you want them to stop?" This turns silence into a signal without breaking the "never interrupt" rule.
  Done when: `sampo silence review` lists unattended actions with zero user response in 7+ days, grouped by verb, with a "stop doing this" checkbox per group.

- **Price each capability in "minutes saved per week" from the user's own ledger** — FEATURE — value 4 — effort M — risk low — category: user value
  Why: The existing idea "price each capability in 'minutes saved per week' from the user's own ledgers" is listed but thin. The user value version focuses on the *ranking*: which 3 capabilities earn their token budget, and which 3 don't. The user's steer: "I want it to still get done without burning a fuck ton of money." They need to *see* the Pareto: "The Ward stops 2 dangerous commands/week (worth 30 min). The brainstorm lens produces 1 adopted idea/month (worth 10 min). The site publish runs every generation (worth 0 min—automated)."
  Done when: `sampo value` prints a ranked table of every capability with "minutes saved/week" computed from ledger timestamps, and flags the bottom 3 as "consider retiring."

- **Let the user's silence be a label: "no response in 48h = not wanted"** — FEATURE — value 3 — effort S — risk low — category: user value
  Why: The user's drops are the only explicit "not wanted" signal, but they are rare. The standing rule says "treat the user's silence as a label" (already in ideas). The user-value sharpening: apply this *proactively*. If Sampo files a task, drafts a steer, or files a follow-up and the user doesn't act on it in 48 hours, Sampo should *downgrade* it (move to not-yet, mark as "likely not wanted") and *tell the user once*: "I filed X; you didn't touch it; I'm parking it. Say 'keep' and I'll un-park." This respects the "never interrupt" rule while making the user's inaction *mean* something.
  Done when: Any task, steer-draft, or follow-up with zero user interaction in 48h is moved to a "parked" state and the next morning card notes it with a one-word "keep?" prompt.

- **Print "the one thing I'd ask you if I could" at session close** — WILD — value 4 — effort S — risk low — category: user value
  Why: The user's standing rule: "Never interrupt the user mid-run" and "options go on an artifact, picks are made with fm decide." But at session *close*, the user is already leaving. The wild idea: at close, print one line: "If I could ask you one thing before you go: <question derived from the open gaps, the left-out list, and the next predicted ask>." It's a *soft* interrupt at the *only* moment the user is transitioning away, so the cost is near zero. The user can ignore it (it's a line, not a prompt) or answer with one word, which files the task.
  Done when: The session-close output includes exactly one line beginning "If I could ask you one thing:" followed by a specific question tied to an open gap or left-out cell.

Next question: Does the user actually *read* the morning card, or do they skim it? If they skim, which 2 lines do they read first—and should the "user value" signal be in those 2 lines?
Next question: What does the user's "quick" in "get done without burning a fuck ton of money, and quick" actually mean in seconds or minutes—and is there a measurable "slowness" in Sampo's own loop that the user feels but hasn't named?
