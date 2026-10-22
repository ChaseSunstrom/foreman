<!-- Foreman's own playbook (written for Foreman, not ported). -->
# Docs: task-first pages, examples that run

Use when writing or reworking documentation a person reads to get something done: a README, a guide, a how-to, a
reference page, CLI help. For keeping a whole repo's doc set owned and fresh over time, use `living-docs.md`.

## The procedure

1. **Name the reader and the outcome.** Each page opens by saying who it is for and what they will have when they
   finish. The title is the task ("Deploy to a VPS"), not the feature ("Deployment"). Pass: the first three lines of
   the page state the outcome.
2. **One kind of page per page.** A *tutorial* teaches by walking one path end to end; a *how-to* gets one task done
   for someone who knows the basics; a *reference* is complete and built for lookup; an *explanation* says why.
   Pass: you can name the page's kind, and nothing of another kind is longer than a paragraph (link to it instead).
3. **The common path first.** The first example is the thing most readers came for, in ten lines or fewer. Options,
   edge cases and troubleshooting come after it.
4. **Numbered steps, one action each, each with what you should see.** Start every step with a verb; end it with
   the observable result ("The server prints `listening on :8080`"). Pass: no step holds two actions, and none ends
   without a result.
5. **Examples run, in CI.** Every code block is copy-pasteable: no `$` prompts in copyable commands (show output in
   its own block), no `...` without saying what goes there, real values or clearly fake ones (`example.com`).
   Python examples run through the script below (or `doctest`); shell examples through a test that executes them.
   Pass: a CI job runs the examples and fails the build when one breaks.
6. **Reference comes from the source.** CLI flags from `--help`, endpoints from the OpenAPI file, functions from
   docstrings. Where generation is impossible, a test asserts the page names every flag or field.
7. **Plain words.** Second person, present tense, short sentences. Define a term at first use and keep one name per
   thing. Pass: `grep -niwE "simply|just|easy|obviously" PAGE.md` returns nothing.
8. **Links are checked.** Relative links are verified in CI; link text says where it goes (never "click here").
9. **Docs change with the code.** A change to behaviour updates its page in the same commit (Foreman records it
   with `fm task finish --docs`).

## Running the Python examples

Save as `run_examples.py` and point it at your Markdown. Each fenced Python block runs in a fresh, isolated
interpreter inside a temporary folder; a block whose fence line reads `python no-run` is skipped. It exits 1 and
names the file and line of each block that fails or runs longer than 60 seconds.

```python
#!/usr/bin/env python3
import re, subprocess, sys, tempfile

FENCE = re.compile(r"^```python([^\n]*)\n(.*?)^```", re.M | re.S)


def run(path):
    text = open(path, encoding="utf-8").read()
    failed = 0
    for m in FENCE.finditer(text):
        if "no-run" in m.group(1):
            continue
        line = text.count("\n", 0, m.start()) + 1
        with tempfile.TemporaryDirectory() as tmp:
            try:
                r = subprocess.run([sys.executable, "-I", "-c", m.group(2)], cwd=tmp, capture_output=True,
                                   text=True, timeout=60)
                err = r.stderr.strip() if r.returncode else ""
            except subprocess.TimeoutExpired:
                err = "timed out after 60 s"
        if err:
            failed += 1
            print(f"{path}:{line}: example failed\n{err}")
    return failed


if __name__ == "__main__":
    sys.exit(1 if sum(run(p) for p in sys.argv[1:]) else 0)
```

Only blocks fenced at the start of a line are found; examples indented inside a list item are not, so keep runnable
examples at the top level.

## Checks

- [ ] Each page's title is a task and its first three lines state the outcome.
- [ ] Each page is one kind: tutorial, how-to, reference or explanation.
- [ ] Every step is one action with an observable result.
- [ ] A CI job runs the examples and fails on a broken one.
- [ ] Reference pages are generated, or a test checks they list every flag or field.
- [ ] Relative links are checked in CI; no "click here".

## Library cards

`fm lib show technical-writing`, `fm lib show readme-writing`, `fm lib show docs-as-code`, `fm lib show api-docs`,
`fm lib show markdownlint`, `fm lib show mkdocs`, `fm lib show sphinx`, `fm lib show docusaurus`,
`fm lib show diagrams-as-code`, `fm lib show changelogs`.
