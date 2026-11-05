"""T-2851: after port.py, silence the design-lint findings that are 12's own art timing, one inline allow per line."""
import sys

sys.path.insert(0, "plugin/lib")
sys.path.insert(0, "site/tools")
from writeif import write_if_changed  # noqa: E402
from sampo import design  # noqa: E402

P = "site/forge.css"
WHY = {"untokened-duration": "12's art timing, kept as drawn",
       "afterglow": "12's hover state, kept as drawn",
       "layout-animation": "12's art motion, finite and in the no-preference block"}
text = open(P, encoding="utf-8").read().split("\n")
by = {}
for f in design.lint([P]):
    if f["file"].endswith("forge.css"):
        by.setdefault(f["line"], set()).add(f["rule"])
for n, rules in by.items():
    text[n - 1] += "".join(f" /* design-lint: allow {r} {WHY.get(r, 'ported art')} */" for r in sorted(rules))
write_if_changed(P, "\n".join(text))
print(len(by), "lines annotated")
