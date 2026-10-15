---
name: cobol
title: COBOL
area: lang
tags: [cobol, mainframe, batch, records, decimal, legacy]
detect: [ext:.cob, ext:.cbl, ext:.cpy]
related: [sql]
---
COBOL programs: structured paragraphs, exact fixed-point decimal fields, file status checks and golden-file batch tests.

## Verify
- `cobc -x -Wall -o prog main.cob`: compiles with GnuCOBOL and warnings on (use your site's compiler on a mainframe).
- `cobc -fsyntax-only -Wall main.cob`: syntax check only, without producing a binary.
- `./prog < tests/in.txt | diff - tests/expected.txt`: the output matches the golden file.

## Test first
Batch programs test best as golden files: fixed input records and expected output.
```sh
printf 'ALICE   00100\nBOB     00250\n' > tests/in.txt
printf 'TOTAL 00350\n' > tests/expected.txt
cobc -x -o sum sum.cob && ./sum < tests/in.txt | diff - tests/expected.txt
```
Write `sum.cob` to make the diff empty, and add one record layout edge case (blank amount, maximum value) per test.

## Do
- Put the four divisions in order, and keep the logic in small named paragraphs or sections invoked with `PERFORM`.
- Use `PIC S9(7)V99 COMP-3` or `DISPLAY` decimal fields for money, with explicit signs and implied decimals.
- Share record layouts through copybooks (`COPY`), not copied text.
- Check `FILE STATUS` after every `OPEN`, `READ`, `WRITE` and `CLOSE`, and branch on it.
- Use `ON SIZE ERROR` on arithmetic and `ROUNDED` where rounding is intended.
- Use `EVALUATE` for multi-way branches and `END-IF`, `END-READ` and similar scope terminators instead of periods.
- Initialize working storage explicitly with `INITIALIZE` or `VALUE` clauses.
- Keep one `STOP RUN` or `GOBACK` exit and a clear return code.

## Avoid
- Floating-point (`COMP-1`, `COMP-2`) for money: rounding errors. Use packed or display decimals.
- Periods inside nested `IF` blocks: a stray period ends every open scope early. Use explicit terminators.
- Ignoring `FILE STATUS`: failed reads look like empty files. Test it.
- Overlapping `REDEFINES` without a discriminator: data is reinterpreted wrongly. Pair it with a type field.
- `ALTER` and uncontrolled `GO TO`: untraceable flow. Use `PERFORM` of paragraphs.
- Moving numeric fields into alphanumeric ones without thought: truncation and sign loss. Match picture clauses.
- `MOVE` of a longer field into a shorter one without a size check: silent truncation. Validate lengths.

## Review
- [ ] Money fields are decimal with explicit scale and rounding.
- [ ] Every file operation checks its status.
- [ ] Arithmetic has `SIZE ERROR` handling where overflow is possible.
- [ ] Scope terminators are used and no stray periods remain.
- [ ] A golden-file test covers normal and boundary records.
