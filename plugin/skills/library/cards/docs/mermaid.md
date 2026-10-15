---
name: mermaid
title: Mermaid diagrams
area: docs
tags: [mermaid, diagrams, markdown, flowchart, sequence, docs]
detect: [dep:mermaid, dep:@mermaid-js/mermaid-cli, ext:.mmd, ext:.mermaid]
related: [technical-writing, latex]
---
Mermaid diagrams as text: flowcharts, sequence, class, state and ER diagrams, rendered by mermaid-cli or the host.

## Verify
- `mmdc -i diagram.mmd -o diagram.svg`: the diagram parses and renders (mermaid-cli); a syntax error exits non-zero.
- `mmdc -i README.md -o README.out.md`: every mermaid block in a Markdown file renders.
- `grep -rn '```mermaid' docs | wc -l`: count of embedded diagrams to render-check.
- `git diff --stat -- '*.mmd'`: diagram source changed, not only its generated output.

## Test first
The renderer is the test. Write the diagram that should exist and let parsing fail first.
```bash
# fails on any syntax error; run over every diagram
for f in docs/diagrams/*.mmd; do
  mmdc -i "$f" -o "/tmp/$(basename "$f" .mmd).svg" || exit 1
done
```
Start with a deliberately incomplete diagram (for example an arrow to an undefined participant in a sequence diagram) and fix until `mmdc` passes. Put sources in `docs/diagrams/` and render in CI.

## Do
- Start each diagram with its type line: `flowchart TD`, `sequenceDiagram`, `classDiagram`, `stateDiagram-v2`, `erDiagram`.
- Give nodes short IDs and quoted labels: `A["Load config"] --> B{Valid?}`.
- Keep one idea per diagram, under about 15 nodes; split larger flows into several diagrams.
- Use `subgraph` to group and `direction` to control layout; label edges with `-->|yes|`.
- In sequence diagrams, declare `participant A as Auth service` once and use short aliases after.
- Use `%%` for comments and a `classDef` plus `class` for styling instead of per-node styles.
- Commit the source `.mmd` or fenced block; commit rendered SVG or PNG only if the host cannot render.
- Pin the mermaid or mermaid-cli version in `package.json` so output is stable.

## Avoid
- Using `graph` with reserved words as node IDs (`end`, `graph`, `subgraph`) in lowercase: it breaks the parser. Capitalize or rename.
- Unquoted labels containing parentheses, brackets, colons or quotes: syntax errors. Wrap in double quotes and escape with `#quot;`.
- Pasting diagrams copied from other tools with Unicode quotes: parse errors. Use plain ASCII quotes.
- Assuming every feature works on the viewer: GitHub, GitLab and docs sites bundle different mermaid versions. Stick to stable diagram types and test where it will be shown.
- Huge diagrams with crossing edges: unreadable. Split or simplify.
- Hand-editing the generated SVG: lost on next render. Edit the source.
- Running `mmdc` as root in a container without a Puppeteer config: Chromium sandbox error. Pass `-p puppeteer-config.json` with the needed args.

## Review
- [ ] Every diagram renders with `mmdc` without errors.
- [ ] Labels with special characters are quoted.
- [ ] Each diagram is small enough to read and has a clear direction.
- [ ] The diagram type is supported by the viewer where it is published.
- [ ] Source diagrams are committed; version of the renderer is pinned.
