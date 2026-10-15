---
name: diagrams-as-code
title: Diagrams as code
area: docs
tags: [diagrams, plantuml, d2, graphviz, mermaid, architecture]
detect: [dep:diagrams, dep:@mermaid-js/mermaid-cli, dep:graphviz, ext:.puml, ext:.d2, ext:.dot]
related: [mermaid, adrs, docs-as-code, technical-writing]
---
Diagram sources kept in the repo as text, rendered in CI, small and focused, and reviewed like code.

## Verify
- `mmdc -i diagram.mmd -o diagram.svg`: the Mermaid source renders (mermaid-cli).
- `dot -Tsvg diagram.dot -o diagram.svg`: the Graphviz source parses and renders.
- `plantuml -checkonly diagram.puml`: PlantUML syntax is valid (when plantuml is installed).
- `d2 diagram.d2 diagram.svg`: the D2 source compiles (when d2 is installed).

## Test first
The failing check is a render that must succeed, plus a guard that the committed image is current.
```sh
for f in docs/diagrams/*.mmd; do
  mmdc -i "$f" -o "${f%.mmd}.svg" || exit 1
done
git diff --exit-code -- docs/diagrams
```
Add a diagram for a change before editing the prose it supports. Name the question it answers in one line above it.

## Do
- Keep sources next to the docs that use them (`docs/diagrams/`), with one diagram per question: context, container, sequence, state.
- Pick the tool by shape: sequence and flow in Mermaid or PlantUML, architecture in D2 or C4 tooling, graphs in Graphviz, cloud topology in `diagrams` (Python).
- Label every edge with a verb or protocol, and name nodes by role (`Order service`), not by class name.
- Limit one diagram to about 10 to 15 nodes. Split into levels and link between them.
- Render in CI to SVG and publish or embed that output, or check the render in as a build artifact.
- Write alt text or a caption stating the point, so the diagram reads when the image fails.
- Use consistent shapes and colour for the same kinds of thing, and a short legend if colour carries meaning.
- Update the diagram in the same commit as the code change it describes.

## Avoid
- Binary exports from a GUI tool as the only source: they cannot be diffed or edited. Keep the text source and render from it.
- One giant diagram of everything: unreadable. Split by audience and level.
- Auto-generated dependency graphs pasted without curation: noise. Filter to the boundaries that matter.
- Unlabelled arrows: the reader guesses direction and meaning. Label with the action.
- Rendering only on a developer machine: output drifts. Render in CI with pinned tool versions.
- Diagrams that contradict the code: stale pictures mislead. Review them when the code they depict changes.

## Review
- [ ] Source and rendered output are both in sync and reproducible by one command.
- [ ] Each diagram answers one stated question, with at most about 15 nodes.
- [ ] Every edge is labelled and the direction is clear.
- [ ] Alt text or caption is present.
- [ ] CI fails when a diagram does not render.
