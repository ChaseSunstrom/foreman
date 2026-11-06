# Brainstorm — lens: configuration inside the TUI

- **Backtest a cap or timeout against your own run history** — FEATURE — value 4 — effort M — risk low — category: runners/limits
  Why: assumption: the pack shows spend caps, stall watchdogs and retry budgets as settings, but no way to know a good value. The settings screen can replay the run ledger against a candidate value.
  Done when: editing a dollar cap or stall timeout shows "would have stopped N of your last M runs" computed from the run journal, and a test fixture with a known history asserts the count.

- **Dry-render the candidate config in a headless child before applying** — FEATURE — value 4 — effort M — risk low — category: safety nets
  Why: the pack has confirm-or-revert and last-good fallback, but those act after the damage. Rendering one frame in a throwaway child pty catches bad themes, broken keymaps and layout overflow first.
  Done when: a config with an unreadable theme or a layout wider than the terminal is rejected before apply, with the child's frame and error shown in the settings view.

- **Show guard-related rows locked, with the explicit step to change them** — SECURITY — value 4 — effort S — risk low — category: safety
  Why: the constraint is that the guard's safety is never weakened, and the tighten-only lattice idea exists. No idea shows how the settings screen presents a setting it refuses to change.
  Done when: rows covering guard strictness, containment and protected paths render read-only with a lock glyph and the exact CLI command, and a test asserts no key sequence in the screen can write them.

- **Notify when a release changes a default you never set** — FEATURE — value 3 — effort S — risk low — category: upgrades
  Why: assumption: users who never touched a setting still get silent behaviour changes on release (1.2.49, 1.2.50). The config layer can store defaults per version and diff them.
  Done when: after upgrade, the first launch lists settings whose effective value moved, with a one-key "pin the old value" that writes it to tui.toml.

- **Auto-apply profiles keyed to the terminal (ssh, tmux, TERM, width, docked pane)** — FEATURE — value 4 — effort M — risk med — category: profiles
  Why: the pack mentions docked-pane mode, slow links, NO_COLOR and capability detection as separate ideas. A `[when]` match in tui.toml would unify them (for example `ssh = true` gives reduced motion).
  Done when: a config with a `[profile.ssh]` table takes effect under a faked SSH_CONNECTION, the settings screen shows which profile is active, and a golden-frame test covers both.

- **Probe which key chords the terminal actually delivers during keybinding capture** — FEATURE — value 3 — effort M — risk low — category: keys
  Why: the recorder with conflict detection exists. It does not cover Ctrl-I vs Tab, Ctrl-M vs Enter, or keys tmux and the Linux console swallow, which silently yield dead bindings.
  Done when: binding a chord the terminal can't distinguish shows a warning naming the collision, and a pty test feeds ambiguous bytes and checks the warning.

- **Pick colours with an OKLCH picker on truecolor gradient tracks and a live contrast readout** — FEATURE — value 3 — effort M — risk low — category: themes
  Why: T-1217 shows the docked pane background is #262626, and themes need contrast fixes. A picker that shows contrast against the probed background stops bad themes at the source.
  Done when: sliders for L, C and H redraw a gradient track per channel, show a contrast ratio against the real background, and block saving a text role below the configured minimum.

- **Let extensions declare a settings schema that merges into the settings screen** — FEATURE — value 3 — effort M — risk med — category: extensibility
  Why: extensions add panels and widgets today, but the screen is planned as generated from one schema. Extension settings would otherwise stay hand-edited TOML.
  Done when: an example extension's declared fields appear under its own namespaced section, validated by its schema, and its values never write outside its table.

- **Switch layouts by rule, such as showing the test panel while verify runs** — FEATURE — value 3 — effort M — risk med — category: layout
  Why: assumption: the layout builder gives static layouts, while the run moves through stations whose useful panels differ. A small `when station = verify` rule table covers that.
  Done when: tui.toml rules switch the layout on a station change with an eased transition, a manual override pins it, and the settings screen lists active rules.

- **Wild: Rotary-dial rows with detents for numeric settings** — FEATURE — value 2 — effort S — risk low — category: delight
  Why: wild; the mixing-console idea covers motion, but ordinary numeric rows (frame rate, density, cache sizes) could look like dials with snapping and a quiet tick, where reduced motion gives a plain stepper.
  Done when: arrow keys turn a drawn dial through named detents, the value matches the toml, and a golden frame shows the dial at three positions.

- **Wild: Record a tweak session and distil the minimal config patch** — FEATURE — value 3 — effort M — risk med — category: config by demonstration
  Why: wild; the user adjusts live (resize a pane, toggle panels, nudge the theme) in a record mode. Foreman diffs the resolved state and proposes only the keys that matter, as a diff and never auto-applied.
  Done when: after a recorded session of five changes the app shows a patch of exactly those five keys, and applying it reproduces the layout in a headless render.

- **Wild: Render two candidate configs side by side on the same live event stream** — FEATURE — value 3 — effort L — risk med — category: preview
  Why: wild; the A/B flicker key swaps one frame at a time, but a split compositor over one event log lets the user judge both looks under real load and keep the half they prefer.
  Done when: the split view draws both configs from one event feed with no divergence in content, and choosing a side writes only the differing keys.

- **Wild: Run a 20-second scripted stress replay under the candidate config** — PERFORMANCE — value 3 — effort M — risk low — category: validation
  Why: wild; the frame-time budget and flood-handling ideas exist, but a user turning on gradients, shimmer and particles has no way to know what that costs on their machine.
  Done when: a stress key plays a floods-plus-resize-plus-wide-glyph replay and reports dropped frames and CPU, flags settings over budget, and offers a one-key downgrade.
