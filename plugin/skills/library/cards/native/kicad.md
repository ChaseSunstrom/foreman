---
name: kicad
title: KiCad
area: native
tags: [kicad, pcb, schematic, electronics, erc, drc, hardware]
detect: [file:*.kicad_pro, file:*.kicad_sch, file:*.kicad_pcb, ext:.kicad_sym, ext:.kicad_mod]
related: [embedded-c, stm32-hal, verilog-fpga]
---
KiCad projects: ERC and DRC from kicad-cli, library hygiene, manufacturing outputs, and review of text-diffable design files.

## Verify
- `kicad-cli sch erc --exit-code-violations -o erc.rpt project.kicad_sch`: schematic electrical rules check; non-zero exit on violations.
- `kicad-cli pcb drc --exit-code-violations -o drc.rpt project.kicad_pcb`: board design rules check.
- `kicad-cli sch export pdf -o schematic.pdf project.kicad_sch`: the schematic renders for review.
- `kicad-cli pcb export gerbers -o gerbers/ project.kicad_pcb && kicad-cli pcb export drill -o gerbers/ project.kicad_pcb`: fabrication outputs.
- `kicad-cli sch export bom -o bom.csv project.kicad_sch`: BOM generates with all needed fields.

## Test first
The check that fails first is ERC or DRC on the change: run it before editing and keep zero violations.
```sh
kicad-cli sch erc --exit-code-violations -o erc.rpt board.kicad_sch   # baseline: 0
# add the new part/net, then rerun; fix every violation or add a justified exclusion
kicad-cli pcb drc --exit-code-violations -o drc.rpt board.kicad_pcb
```
Put both commands in CI so a violation breaks the build.

## Do
- Commit `*.kicad_pro`, `*.kicad_sch`, `*.kicad_pcb`, `sym-lib-table`, `fp-lib-table` and project libraries; ignore backups (`*-backups/`, `*.bak`, `fp-info-cache`).
- Keep project-local symbol and footprint libraries and reference them with `${KIPRJMOD}`, so clones build without global setup.
- Set the design rules from the fab's capabilities (min track, clearance, via drill, annular ring) in board setup before routing.
- Fill every symbol's `Value`, `Footprint` and an MPN or supplier field so the BOM is complete.
- Add power flags and mark intentional no-connects so ERC is meaningful; fix violations rather than disabling checks.
- Run `Update PCB from Schematic` after each schematic change and run DRC again, including the unconnected-items check.
- Verify footprints against the datasheet land pattern and pin 1 orientation; review the 3D view for fit.
- Version with tags per fabrication release, and store generated gerbers alongside the tag, not in each commit.

## Avoid
- Silencing ERC/DRC violations by severity change instead of fixing: ships bugs. Allow exclusions only with a comment.
- Using global library paths without `${KIPRJMOD}`: the project breaks on another machine.
- Copying a footprint from an unvetted library without checking pad size and pin mapping: wrong parts land. Compare to the datasheet.
- Routing before setting net classes and rules: rework. Define rules first.
- Reusing reference designators after annotating partially: duplicate refs. Re-annotate and rerun ERC.
- Committing generated gerbers on every change: noisy diffs. Generate in CI or at release.
- Relying on the GUI version differences: file format changes across major versions. Pin the KiCad major.

## Review
- [ ] ERC and DRC both report zero unexplained violations.
- [ ] BOM has complete value, footprint and part-number fields.
- [ ] Libraries are project-local or version-pinned, and paths are relative.
- [ ] Fab rules in board setup match the chosen manufacturer.
- [ ] Release outputs (gerbers, drill, BOM, PDF) are tagged and reproducible.
