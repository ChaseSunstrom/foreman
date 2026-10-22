---
name: directions
description: Use when a new UI needs a look: six style directions, the pick saved as DESIGN.md.
---

# Foreman: style directions

One sentence about a product in; six distinct style directions out, each a card that fits on one screen; one is
picked and saved as `DESIGN.md` with an audacity level. Start it with `/foreman:directions <sentence>` (in Claude
Code or an `fm code` session), or start it yourself when the user asks for looks or styles to choose from before a
UI exists. It is for web and app screens; a terminal UI or a Claude Code mod takes the playbooks' `terminal-ui.md`
instead.

It widens the UI playbook `../playbooks/references/ui/design-direction.md` from one direction to six to choose from:
that file holds the taste words, the direction bank, the audacity dial, "Defaults to avoid" and the DESIGN.md
template. Read it, then `references/cards.md` (the card format, the rules for the set, the generic defaults, the
preview page recipe and a worked example) before drafting.

Directions come from three shelves: the playbook's twelve-row bank; the twelve looks (`fm lib list --area looks`,
then `fm lib show look-NAME`: measured palettes, type, layout, motion and a contrast test); and the shader looks
(`fm lib show shader-NAME`) as an optional texture on one surface, never as the direction itself.

## Procedure

1. **A brief, and an existing direction.** Saving DESIGN.md is an edit, so work inside a focused task; with none,
   `fm task new "Style direction for <product>" --type FEATURE --tier S --ac "DESIGN.md names a direction, a
   runner-up and an audacity :: grep -qE 'audacity (safe|bold|wild)' DESIGN.md" --focus`. If the repo already has a
   `DESIGN.md`, a token file or a brand guide, it wins (the playbook's step 1): name it and stop, unless the user
   asked for a new look. A token file with no `DESIGN.md` table yet: `fm design extract <ui root>` writes one (its
   Tokens section, with each pair's contrast). Then draft against it (its direction is not offered again) and replace the file; git keeps
   the old one, and the new Direction section says which direction it replaced.
2. **Read the sentence.** Take the product, the audience and any taste words (the playbook's table; its empty words
   set no knob). Answer interview questions 1 (who, and what they were doing a minute before) and 3 (what it must
   never be mistaken for) from the sentence, else from the repo (README, existing copy), marked *assumed*. Don't ask
   question 2: the six cards are its answers, one physical thing each. If the sentence names no product at all
   ("make it pretty"), ask one question, what it is and for whom; under full autonomy read that from the README.
3. **Draft six cards** in the format of `references/cards.md`, then hold the whole set to its rules:
   - at least four from the bank or the looks, at most two `own`;
   - spread: a dark ground and a mid or tinted one, three type classes, a sparse and a dense card, a still and a
     lively one, and each audacity setting (safe, bold, wild) at least once;
   - any two differ on at least three of the five knobs and never share a physical thing or a signature move;
   - each card's body text pair measured at 4.5:1 or more (a look's palette is measured already; otherwise use the
     script in `fm lib show look-lido --section "Test first"`), its accent 30° or more from the status hues;
   - none is a generic default from cards.md, none breaks "Defaults to avoid", and no look whose `Not for:` names
     this kind of product.
   Redraft a card that fails, at most twice per slot, then fill the slot with another bank row or look; keep one
   line on each card you dropped and why.
4. **Show them.** All six cards in one message, then the comparison table (one row each: ground, type, density,
   motion, radius, audacity) so the spread shows, the dropped ones, and your recommendation and runner-up, each with
   its reason. Recommend at the playbook's default dial for the surface (safe for settings, admin and forms; bold for
   a product's home; wild for games, portfolios and events) unless the user's words move it. Preview pages only when
   asked ("show me", "mock them up") or when the user is torn between two: cards.md's recipe, outside the repo, then
   `fm design lint` over them.
5. **The pick.**
   - Standard autonomy: one AskUserQuestion with two questions. "Which direction?": four options, your
     recommendation first, then the next three; its free-text answer takes any number from 1 to 6, or a blend of two
     (one owns type, the other colour; never three). "How bold?": the picked card's audacity first, then the other
     two settings.
   - Full autonomy (`fm autonomy` says full): no question. Take your recommendation at its audacity and record it:
     `fm decide "Style direction: <name>, audacity <setting>" --task <ID> --why "<why it fits the sentence>"
     --rejected "<the other five, a reason each>"`. Name the pick and the runner-up in the final report, so the user
     can switch with one word.
6. **Save DESIGN.md** at the repo root (or beside an existing design-system package), filling the playbook's DESIGN.md
   template with every heading in its order: Point of view, Interview, Direction, Knobs, Signature moves, Banned,
   Allowed exceptions (Tokens waits for the token file; `fm design extract` writes it).
   - Point of view and Interview from step 2; "Feels like" is the picked card's physical thing, marked *user* when
     the user picked it and *assumed* under full autonomy.
   - Direction: `<bank row, look-NAME or "own: NAME">, audacity <safe | bold | wild>.`, then the runner-up and why it
     lost, then the taste-word split. A blend names both and what each owns: `Gallery (type) + Negative file
     (colour), audacity bold.`
   - Knobs: the card widened to the template's detail; every colour with its role, and the measured contrast of each
     text and background pair.
   - Signature moves: as many as the audacity row allows (safe 1, bold 2, wild 3), the card's first.
   - Banned: the anti-reference, the generic default the set came closest to, and each "Defaults to avoid" line that
     applies.
   Check it, and record the check as the step's evidence (`fm task evidence <ID> --step N --run "<cmd>"`):
   `grep -cE '^## (Point of view|Interview|Direction|Knobs|Signature moves|Banned|Allowed exceptions)$' DESIGN.md`
   prints 7, and `grep -E 'audacity (safe|bold|wild)' DESIGN.md` finds the Direction line.
7. **Hand on.** Building follows the playbook's step 7: build, then its Checks (the cover test included). Preview
   pages stay out of the repo. Close the task through the Foreman loop, or carry on when the look is one step of a
   larger task.

A second run finds the DESIGN.md the first one saved and stops at step 1, unless the user asks for a new look.
