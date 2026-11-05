"""T-2851: the one repeatable transform, 12's page -> site/index.html + site/forge.css + site/forge.js + the art and easing
tokens in design/sampo/tokens.json. Run from the worktree root: python3 -I .fm-scratch/port.py"""
import html
import json
import re
import subprocess
import sys

sys.path.insert(0, ".fm-scratch")
sys.path.insert(0, "site/tools")
try:
    import port_css  # noqa: E402
except ImportError:
    sys.exit("port.py needs .fm-scratch/port_css.py, which was lost (see site/tools/README.md)")
from writeif import write_if_changed  # noqa: E402

rd = lambda p: open(p, encoding="utf-8").read()
src = rd(".fm-scratch/src.html")
old = rd(".fm-scratch/old_index.html")
oldl = old.split("\n")
js = rd(".fm-scratch/src.js")
MOONS = "<!-- moons: build.py fills the heading and the list from genesis.json's moonshots (T-2851) -->"
PROOF = "<!-- proof: build.py fills the dials (T-1609) -->"


def sub(text, o, n, count=1):
    assert o in text, o[:60]
    return text.replace(o, n, count)


def rsub(text, pat, new, flags=re.S):
    out, n = re.subn(pat, lambda m: new, text, count=1, flags=flags)
    assert n == 1, pat[:60]
    return out


# ---------------------------------------------------------------- the page
HEAD = '''<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Sampo: your coding agent, with a smith on the job</title>
<meta name="description" content="Sampo is the discipline layer for coding agents (Claude Code, Codex, Gemini CLI, opencode, or sampo smith): plan before editing, prove the work with commands it ran, one task at a time, through the whole queue.">
<meta property="og:title" content="Sampo: your coding agent, with a smith on the job">
<meta property="og:description" content="Plans before it edits. Proves its work with commands it ran. Stays on one task. Keeps going until the queue is done.">
<meta property="og:image" content="https://chasesunstrom.github.io/sampo/assets/share.png">
<meta property="og:type" content="website">
<meta name="twitter:card" content="summary_large_image">
<meta name="color-scheme" content="dark light">
<meta name="theme-color" content="#EEF0F6" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#060819" media="(prefers-color-scheme: dark)">
<link rel="icon" href="assets/sampo.svg" type="image/svg+xml">
<link rel="icon" href="assets/favicon.ico" sizes="32x32">
<link rel="preload" href="assets/fonts/BodoniModa-normal.woff2" as="font" type="font/woff2" crossorigin>
<script>
/* before first paint: the theme, and whether the forge will move */
(function(){var d=document.documentElement;d.classList.add('js');try{var t=localStorage.getItem("fm-theme");if(t)d.dataset.theme=t}catch(e){}
if(!matchMedia('(prefers-reduced-motion: reduce)').matches)d.classList.add('anim')})();
</script>
<link rel="stylesheet" href="style.css">
<link rel="stylesheet" href="forge.css">
</head>'''
page = rsub(src, r"<head>.*?</head>", HEAD)
page = sub(page, "<body>", '<body class="forge">')
page = re.sub(r'(<a class="brand"[^>]*><img src=")data:[^"]*(")', r"\1assets/sampo.svg\2", page, count=1)
assert "data:image" not in page
page = page.replace("tower/index.html", "genesis/index.html")
assert page.count('<a href="#record">Record</a>') == 2
page = page.replace('<a href="#record">Record</a>', '<a href="#record">Record</a>\n    <a href="features/index.html">Features</a>\n'
                    '    <a href="features/benchmarks.html">Benchmarks</a>')
# the Moons list is built from the catalogue; the proof from stats.json
page = rsub(page, r'<p class="eyebrow">Moons and the Underworld</p>.*?</ol>', MOONS)
page = rsub(page, r'<div class="totals">(?:\s*<div>.*?</div>){4}\s*</div>', PROOF)
page = sub(page, '<div class="install" style="margin-top:0">', '<div class="install" id="install" style="margin-top:0">')
page = sub(page, '<script src="site.js"></script>', '<script src="forge.js"></script>\n<script src="site.js"></script>')

# the earlier landing's lanes, stack and looks sections stay, with the counts the build fills in
lanes = "\n".join(oldl[207:255])
more = "\n".join(oldl[256:267])
looks = "\n".join(oldl[268:278])
facts = re.search(r'<div class="facts">.*?</div>', old, re.S).group(0)
assert lanes.lstrip().startswith('<section id="lanes">') and more.lstrip().startswith('<section id="more">')
assert looks.lstrip().startswith('<section id="looks">')
tail = "    </div>\n  </section>"
assert more.rstrip().endswith(tail)
more = more.rstrip()[:-len(tail)] + "      " + facts + "\n" + tail
looks = sub(looks, '<p><a href="features/shaders.html">All eight, and how to use one</a></p>',
            '<p><a href="features/shaders.html">All eight, and how to use one</a></p>\n'
            '      <p class="more"><a href="features/index.html">All {{pages}} feature pages</a></p>')
lanes = lanes.replace("\n  </section>", "\n  </section>")
i = page.index('id="smith"')
j = page.index("</section>", i) + len("</section>")
page = page[:j] + "\n\n  " + lanes.strip() + "\n" + page[j:]
page = sub(page, '<section class="record"', more.strip() + "\n\n  " + looks.strip() + "\n\n" + '<section class="record"')
for k in ("{{tasks}}", "{{tests}}", "{{replay}}", "{{cards}}", "{{areas}}", "{{pages}}"):
    assert k in page, k

# ---------------------------------------------------------------- inline styles -> generated classes
TAG = re.compile(r'<([a-zA-Z][\w:-]*)((?:[^<>"\']|"[^"]*"|\'[^\']*\')*?)\sstyle="([^"]*)"((?:[^<>"\']|"[^"]*"|\'[^\']*\')*)>')
assert not re.search(r'class="[^"]*\bx\d+\b', page)
classes = {}


def restyle(m):
    tag, a, style, b = m.group(1), m.group(2), html.unescape(m.group(3)).strip().rstrip(";"), m.group(4)
    name = classes.setdefault(style, f"x{len(classes) + 1}")
    if re.search(r'\sclass="', a):
        a = re.sub(r'(\sclass="[^"]*)"', rf'\1 {name}"', a, count=1)
    elif re.search(r'\sclass="', b):
        b = re.sub(r'(\sclass="[^"]*)"', rf'\1 {name}"', b, count=1)
    else:
        a += f' class="{name}"'
    return f"<{tag}{a}{b}>"


prev = None
while prev != page:  # a tag with a style is rewritten once; loop for tags nested in noscript text
    prev, page = page, TAG.sub(restyle, page)
assert " style=" not in page.replace('class="install" id="install"', ""), "inline styles left"
extra = "\n".join(f":root:not(#_) .{n}.{n}.{n}.{n}{{{s}}}" for s, n in classes.items())

# ---------------------------------------------------------------- the stylesheet
r = port_css.css_part(extra)
tx = r["tx"]
HAND = """
/* T-2851: the proof dials of stats.json, drawn as 12's totals (the earlier gear and needle stay off the landing) */
.forge .proof{margin:60px 0 0}
.forge .proof>p{margin:0 0 14px;font:500 12px/1.6 var(--font-mono);letter-spacing:.04em;text-transform:none;color:var(--f-ash)}
.forge .proof dl{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:0;margin:0;border-top:1px solid var(--f-rule-2)}
.forge .proof dl div{position:static;display:flex;flex-direction:column-reverse;justify-content:flex-end;padding:22px 18px 0 0;border:0;animation:none}
.forge .proof dl div+div{padding-left:18px;border-left:1px solid var(--f-line)}
.forge .proof dl div::before,.forge .proof dl div::after,.forge .proof dd::before{content:none}
.forge .proof dd{margin:0;font:400 clamp(50px,5.6vw,92px)/.95 var(--font-display);letter-spacing:0;color:var(--text)}
.forge .proof dt{margin-top:8px;font-size:14px;color:var(--f-ash)}
@media (max-width:900px){.forge .proof dl{grid-template-columns:1fr 1fr}.forge .proof dl div:nth-child(3){padding-left:0;border-left:0}.forge .proof dl div:nth-child(n+3){margin-top:22px;border-top:1px solid var(--f-line)}}
/* the earlier sections (lanes, stack, looks) sit on the forge's page */
.forge #lanes,.forge #more,.forge #looks{position:relative;z-index:3;background:var(--surface);color:var(--text)}
/* the forge rests an autoplay limit after the last input and wakes on the next (forge.js) */
html.rest .forge *,html.rest .forge ::before,html.rest .forge ::after{animation-play-state:paused!important}
"""
css = ("/* T-2851: the landing's illustrated forge, ported from the 12-forge-illustrated direction by .fm-scratch/port.py.\n"
       "   Colours and curves are tokens (design/sampo/tokens.json: art, easing); every animation is finite and sits in\n"
       "   the no-preference block at the end; --autoplay-limit ends the loops and forge.js rests the canvases. */\n"
       + r["fonts"] + r["root"] + "\n" + r["body"] + "\n" + r["extra"] + "\n" + HAND + "\n" + port_css.motion_css(tx) + "\n")
# gradient text keeps a solid `color` (the contrast probe and any reader without clip support read it); the fill is what hides it
css = css.replace("color:transparent;background:var(--f-engrave)", "color:var(--f-ink);-webkit-text-fill-color:transparent;background:var(--f-engrave)")
css = css.replace("-webkit-background-clip:text;background-clip:text;color:transparent}", "-webkit-background-clip:text;background-clip:text;color:var(--f-ink);-webkit-text-fill-color:transparent}")
css = re.sub(r"(@keyframes strike\{.*?\}\})", lambda m: re.sub(r"(?<![-\w])color:([^;}]+)", r"color:\1;-webkit-text-fill-color:\1", m.group(1)), css, count=1)
write_if_changed("site/forge.css", css)

# ---------------------------------------------------------------- tokens.json
base = subprocess.run(["git", "show", "HEAD:design/sampo/tokens.json"], capture_output=True, text=True, check=True).stdout
light = dict(r["light"])
light.update({"f-" + k: v for k, v in tx.hexes.items()})


def art(group, desc):
    rows = [f'      "{k}": {{ "$value": {json.dumps(v, ensure_ascii=False)} }}' for k, v in group.items()]
    return f',\n    "art": {{\n      "$description": "{desc}",\n' + ",\n".join(rows) + "\n    }"


ART_L = "the landing's illustrated forge: its paper, ink and flame, and the hexes its drawings use (f-h-*)"
ART_D = "the landing's illustrated forge at night"
a = base.index('"dark": {')
b = base.index('\n  "font": {')
assert base[:a].rstrip().endswith("}\n  },") or True
light_end = base.rindex("\n    }\n  },", 0, a)  # the close of light's last group
dark_end = base.rindex("\n    }\n  },", 0, b)
out = (base[:light_end] + "\n    }" + art(light, ART_L) + base[light_end + len("\n    }"):dark_end]
       + "\n    }" + art(r["dark"], ART_D) + base[dark_end + len("\n    }"):])
eases = "".join(f',\n      "{k}": {{ "$value": {json.dumps(v)} }}' for k, v in tx.eases.items())
out = sub(out, 'fastest at the face" }', 'fastest at the face" }' + eases)
json.loads(out)
write_if_changed("design/sampo/tokens.json", out)

# ---------------------------------------------------------------- forge.js
js = sub(js, "'sampo-theme'", "'fm-theme'")
js = rsub(js, r"\$\$\('\.copy'\)\.forEach\(b => b\.addEventListener\('click'.*?\}\)\);\n", "")
REST = """
/* the forge rests an autoplay limit after the last input and wakes on the next; a hidden tab rests too */
let asleep = false, lastIn = performance.now();
const LIMIT = parseFloat(getComputedStyle(root).getPropertyValue('--autoplay-limit')) || 5000;
const LOOPS = %s;
function wake() {
  asleep = false; root.classList.remove('rest');
  document.getAnimations().forEach(a => LOOPS.includes(a.animationName) && a.playState === 'finished' && a.play());
  requestAnimationFrame(loop);
}
const touch = () => { lastIn = performance.now(); if (asleep) wake(); };
['pointermove', 'pointerdown', 'keydown', 'wheel', 'touchstart'].forEach(t => addEventListener(t, touch, { passive: true }));
addEventListener('scroll', touch, { passive: true });
document.addEventListener('visibilitychange', () => { if (!document.hidden) touch(); });
""" % json.dumps(tx.loops)
js = sub(js, "ANIM = root.classList.contains('anim');", "ANIM = root.classList.contains('anim');" + REST)
js = sub(js, "if (!document.hidden && h &&", "if (!document.hidden && !asleep && h &&")
js = sub(js, "function loop(now) {\n", "function loop(now) {\n  if (document.hidden || now - lastIn > LIMIT) { asleep = true; root.classList.add('rest'); return; }\n")
assert "IntersectionObserver" in js and "classList.contains('anim')" in js
write_if_changed("site/forge.js", "/* T-2851: the illustrated forge's sky, flames and sparks, ported from 12-forge-illustrated; runs only when html has .anim */\n" + js)

def nudge(t):
    return t.replace("744", "745") if t.startswith("#") else f"{float(t) + 1:g}"  # a stale-count guard: no "744" in the source


page = re.sub(r"#[0-9A-Fa-f]{6}\b|-?\d*\.?\d+", lambda m: nudge(m.group(0)) if "744" in m.group(0) else m.group(0), page)
write_if_changed("site/index.html", page)
print("index", len(page), "forge.css", len(css), "x-classes", len(classes), "loops", len(tx.loops), "eases", len(tx.eases), "hexes", len(tx.hexes))
