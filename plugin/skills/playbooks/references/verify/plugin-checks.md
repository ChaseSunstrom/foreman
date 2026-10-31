<!-- Foreman's own playbook (written for Foreman, not ported). -->
# Verify a Claude Code plugin in three layers: manifest, behavior, install

Use when you changed a plugin manifest, skills, commands or agents and must show it still loads and behaves.

Built on the cards `fm lib show cc-plugin-testing`, `fm lib show cc-plugin-manifest`, `fm lib show cc-mod-testing` and `fm lib show cc-plugin-evals`.

1. **Structure layer:** the manifest and catalog are valid.
   ```bash
   claude plugin validate --strict .
   python3 -m json.tool .claude-plugin/plugin.json
   ```
2. **Fixture layer:** hook and helper scripts against recorded payloads, no model in the loop.
   ```bash
   python3 -m unittest discover -s tests -t tests
   ```
3. **Session layer:** a real session loads it, and `plugin_errors` in the init event is empty:
   ```bash
   claude --plugin-dir ./plugin -p "ping" --output-format stream-json --verbose | jq -e 'select(.type=="system" and .subtype=="init") | (.plugin_errors // []) | length == 0'
   ```
4. **Behaviour layer, only when a skill's wording changed:** `claude plugin eval ./plugin --trust-plugin --scaffold --runs 1 --max-cost-usd 5 --no-publish --json "$(mktemp)"`, then compare per-case scores with the run before.
5. **Record which layers ran.** A green structure layer proves the files parse, not that a hook behaves; say so for any layer you skipped.

Pass: layers 1 to 3 exit 0 on the tree you are committing, and a changed skill has an eval number before and after.

Never claim "plugin works" from layer 1 alone.
