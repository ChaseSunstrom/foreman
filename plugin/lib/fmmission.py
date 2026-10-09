"""fm mission (T-0375): the mission and brainstorm seeds for an open-ended or exhaustive request, composed from the project
itself, so nobody has to hand-write the "finish everything, map every capability, make it beautiful everywhere,
verify on the real path, clean up, recurse until dry" prompt again. It writes two files under research/: the mission
(pillars, surfaces, lenses, the exact fm ideas line) and the pack fm ideas reads (the user's words, the project, the
open work)."""
import os
import re
import shlex
import time

import fmcore as c
import fmideas

# surface → what in `git ls-files` says the project has it
SURFACES = {
    "web UI": re.compile(r"^(?!(.*/)?(docs?|tests?|examples?)/).*\.(svelte|vue|tsx|jsx|html|css|scss)$"),
    "mobile app": re.compile(r"(^|/)(android|ios)/|AndroidManifest\.xml$|(^|/)pubspec\.yaml$|\.xcodeproj/"),
    "desktop app": re.compile(r"(^|/)src-tauri/|(^|/)electron[^/]*\.(js|ts)$|\.desktop$"),
    "server": re.compile(r"(^|/)(Dockerfile|docker-compose[^/]*\.ya?ml|compose[^/]*\.ya?ml)$|\.service$"),
    "car or embedded": re.compile(r"(^|/)(car|hud|firmware|embedded)/|\.ino$"),
}
_AI = re.compile(r"\b(anthropic|openai|ollama|llama|langchain|claude|whisper|transformers|litellm)\b", re.I)
_DEPS = re.compile(r"(^|/)(requirements[^/]*\.txt|pyproject\.toml|package\.json|Cargo\.toml|go\.mod|build\.gradle(\.kts)?)$")
CLIENTS = ("web UI", "mobile app", "desktop app", "car or embedded")


def surfaces(root):
    """The kinds of thing the project ships, from its tracked files and dependency lists."""
    files = c._git(root, "ls-files", timeout=10).splitlines()
    found = [name for name, rx in SURFACES.items() if any(rx.search(f) for f in files)]
    for f in (f for f in files if _DEPS.search(f)):
        try:
            with open(os.path.join(root, f), encoding="utf-8", errors="replace") as fh:
                if _AI.search(fh.read(200_000)):
                    found.append("AI and agents")
                    break
        except OSError:
            continue
    return found


def lenses(found):
    """fm ideas' defaults plus the lenses this project's surfaces call for."""
    extra = []
    if any(s in found for s in CLIENTS):
        extra.append("beautiful UI and motion")
    if sum(s in found for s in CLIENTS + ("server",)) >= 2:
        extra.append("every device and surface")
    if "AI and agents" in found:
        extra += ["agents of agents", "privacy and local-first"]
    elif "mobile app" in found:
        extra.append("privacy and local-first")
    return list(dict.fromkeys(fmideas.DEFAULT_LENSES + extra))


def pillars(found):
    ui = any(s in found for s in CLIENTS)
    out = ["Finish the open queue and inbox first, independent tasks in parallel builder lanes on the cheapest model "
           "that can; never idle while a gate, build, pipeline or review runs.",
           "Capability map: name the best products in this space, list everything they do, mark what this project "
           "has, half-has or lacks; every sensible gap becomes a task.",
           "Super recursive brainstorm with the lenses below (--rounds 4 --deepen 3); show the user every idea on a "
           "checklist page with build/skip marks before skipping any; build almost all in rounds; brainstorm again "
           "past them (--seen) until it comes back dry."]
    if ui:
        out.append("UI and motion on every surface (" + ", ".join(s for s in found if s in CLIENTS) + "): one design "
                   "language, empty/loading/error states, transitions and states that move; screenshot every screen "
                   "before and after and fix what looks off.")
    out.append("Verify on the real path for each surface, not only in tests" + (" (the device, the browser, the car)"
                                                                                if ui else "") + ".")
    if "AI and agents" in found or "mobile app" in found:
        out.append("Privacy and local-first: nothing leaves the owner's network without an explicit setting or "
                   "approval; prefer local engines; list what still needs the cloud and why.")
    out.append("Clean up as you go; end with a repo sweep (code, docs, briefs, settings, environment, dead or replaced "
               "functionality: playbooks/clean/repo-sweep.md).")
    out.append("In full autonomy ask nothing mid-run; what only the user can do goes in the final report.")
    return out


def _readme(root, words=250):
    for name in ("README.md", "README.rst", "README.txt", "README"):
        try:
            with open(os.path.join(root, name), encoding="utf-8", errors="replace") as f:
                return " ".join(f.read(20_000).split()[:words])
        except OSError:
            continue
    return ""


def compose(p, request=""):
    """{path, pack, surfaces, lenses, ideas, mission} — the files written under the project's research/."""
    import fmmap
    found = surfaces(p.root)
    chosen = lenses(found)
    briefs = c.load_briefs(p)
    open_work = [b for b in briefs if b.status not in c.CLOSED]
    log = c._git(p.root, "log", "-10", "--format=%s")
    try:
        mapped = fmmap.compact(p, 600) or ""
    except Exception:
        mapped = ""
    pack = "\n".join(
        [f"# Context pack — {os.path.basename(p.root)}", "", "## The request", request or "(none given: improve the "
         "project in every way that matters to its user)", "", "## The project", _readme(p.root) or "(no README)", "",
         f"Surfaces: {', '.join(found) or 'library or CLI'}", mapped, "", "## Recent commits", log.strip(), "",
         "## Open work", *[f"- {b.id} {b.type} {b.tier} {b.status}: {c.fit(b.title, 110)}" for b in open_work[:40]]]
    ) + fmideas.user_voice(p)
    stamp = time.strftime("%Y%m%d-%H%M%S")
    folder = os.path.join(p.dir, "research")
    os.makedirs(folder, exist_ok=True)
    pack_path, path = (os.path.join(folder, f"mission-{stamp}{x}.md") for x in (".pack", ""))
    ideas = (f"fm ideas --pack {shlex.quote(pack_path)} --rounds 4 --deepen 3 "
             + " ".join(f"--lens '{lens}'" for lens in chosen))
    mission = "\n".join(
        [f"# Mission — {os.path.basename(p.root)}", "", f"Request: {request or '(open-ended)'}", "",
         f"Surfaces found: {', '.join(found) or 'library or CLI'}", "", "## Pillars",
         *[f"{i}. {x}" for i, x in enumerate(pillars(found), 1)], "", "## Brainstorm seeds",
         *[f"- {lens}" for lens in chosen], "", "## Run", ideas, "", f"Pack: {pack_path}", "", pack])
    pack, mission = c.redact(pack), c.redact(mission)  # what's saved and what's printed alike
    with c.lock(p.dir):
        c.write_atomic(pack_path, pack + "\n")
        c.write_atomic(path, mission + "\n")
    return {"path": path, "pack": pack_path, "surfaces": found, "lenses": chosen, "ideas": ideas, "mission": mission}


def cmd_mission(args):
    import fmcli
    p = fmcli.resolve(args)
    res = compose(p, args.request or "")
    return fmcli.out(args, res, res["mission"] + f"\n\nSaved: {res['path']}")
