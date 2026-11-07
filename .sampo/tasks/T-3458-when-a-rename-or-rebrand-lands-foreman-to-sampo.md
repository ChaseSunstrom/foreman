---
id: T-3458
type: FEATURE
tier: S
status: captured
priority: normal
scope: []
depends_on: []
source: steer
created: 2026-11-06T16:09:51Z
updated: 2026-11-06T16:24:13Z
steer_method_rate: 0.218
---
# When a rename or rebrand lands (Foreman to Sampo, Rune to Kalevala), treat it as…
## Raw request
> why is there a .foreman and .sampo folder? also why was the rune page on the website not updated to be kalevala?and the demo video in the readme not rerecorded
> (fm exam steer: the user's words expanded into a standing rule by an expander whose held-out coverage is 22%; record it with fm decide --cites 'user steer' --check CMD and build that check)
## Interpretation
- When a rename or rebrand lands (Foreman to Sampo, Rune to Kalevala), treat it as complete only when no old-name surface is left. Sweep the whole repo and its generated outputs for the old name in any case or spelling: code, identifiers, config, package metadata, CLI help and output, env vars, comme…
- Don't leave two parallel state or config directories such as `.foreman` and `.sampo`. Use the new name as the single canonical directory. On first run, migrate or read the legacy directory once, then stop writing to it. Add a test that proves the migration and that nothing writes to the old path.
- When asked why a leftover exists, find the actual cause (a missed reference, a deliberate compatibility shim, or a stale artifact) and report it plainly. Then fix it in the same turn unless it is intentional. If it is intentional, document why next to the code.
- Before deleting or overwriting a legacy folder, inspect its contents. Move anything the user may need into the new location, and ask before removing data that has no copy elsewhere.
- Update the website's rune page to the Kalevala name, content, links, titles, metadata, nav entries, and any URL. Keep a redirect from the old URL so existing links don't break. Build the site locally and verify that no old-name text remains on any page.
- Re-record the README demo video or GIF whenever the visible UI, CLI output, branding, or command names change. Regenerate it from the current build with a scripted, reproducible recording step, then check that the frames show the new names and update the README embed and alt text.
- Add a repeatable check, such as a grep-based test or CI step, that fails when old-name strings appear outside an explicit allowlist of intentional compatibility references. Run it before reporting a rename as done.
- Report the outcome faithfully. List the surfaces updated, the ones deliberately left, and anything that couldn't be verified, such as a recording that couldn't run.
- Keep outward or irreversible steps behind the user's explicit grant: deploying or publishing the website, pushing or uploading the video, publishing packages, and deleting user data. Do all the local edits, builds, and re-recordings without asking.
## Assumptions (confidence)
## Acceptance criteria
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-06T16:09:51Z created
- 2026-11-06T16:24:13Z steer: the stale .foreman/ was folded into .sampo/ by sync.move's no-loss rules and committed gone (f6777351f, between queue rows)
## Follow-ups captured
