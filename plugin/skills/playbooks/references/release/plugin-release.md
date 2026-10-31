<!-- Foreman's own playbook (written for Foreman, not ported). -->
# Tag a Claude Code plugin or marketplace entry

Use when you tag a plugin version or change its marketplace catalog entry.

Built on the cards `fm lib show cc-plugin-release`, `fm lib show cc-marketplaces`, `fm lib show cc-plugin-manifest` and `fm lib show cc-plugin-testing`.

1. **One version everywhere.** List every version string you ship and make them equal:
   ```bash
   grep -rn '"version"' .claude-plugin/ plugin/.claude-plugin/
   ```
2. **Validate manifest and catalog with warnings as failures:** `claude plugin validate --strict .` at the marketplace root, and `python3 -m json.tool .claude-plugin/marketplace.json`.
3. **Run the suite on the tree you tag:** `python3 -m unittest discover -s tests -t tests`.
4. **Load it for real:** `claude --plugin-dir ./plugin -p "ping" --output-format stream-json --verbose | jq -e 'select(.type=="system" and .subtype=="init") | (.plugin_errors // []) | length == 0'` must exit 0.
5. **Changelog for users:** what changed in their terms, plus any setting or hook they must migrate.
6. **Tag after the gates, never before;** publishing is outward and needs the owner's grant.

Pass: validate and suite exit 0, one version string appears everywhere, and the changelog has the version's entry.

Never move a published tag; ship a patch version.
