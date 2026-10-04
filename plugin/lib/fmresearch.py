"""fm research ask (T-0206): web research as an engine, not one agent's word. What the project already knows comes
first (fm recall); the question is split into sub-questions (by a tool-less planner child, or --sub); each is researched
by its own `claude -p` child that can only search and fetch the web; every claim must cite a page and quote it; then
each cited page is fetched here and the quoted words are looked for, so a claim is marked verified, not found or
unchecked before anyone relies on it. One note goes to the project's research/ (recall finds it next time).

Only public https pages are fetched (every redirect re-checked), at most 3 MB each."""
import html
import http.client
import ipaddress
import json
import os
import re
import socket
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor

import fmbudget
import fmcore as c

NO_MCP = ["--strict-mcp-config", "--mcp-config", json.dumps({"mcpServers": {}})]
WEB_TOOLS = "WebSearch,WebFetch"
PLANNER = ("Split the question below into 2-{n} sub-questions that together answer it and can each be researched on "
           "the web on their own. Reply with only the sub-questions, one per line, each starting with '- '.")
RESEARCHER = """You research one sub-question on the web for a software engineer. Use WebSearch, then WebFetch the most
authoritative pages (official docs, source repositories, specs, papers, maintainers' posts before blogs and forums).
Reply with claim lines only, in exactly this format, one per line:
- CLAIM: <one specific, checkable statement> | SOURCE: <the https URL you fetched> | QUOTE: "<5-25 words copied exactly from that page>" | TIER: primary|secondary|community | DATE: <the page's publication or update date, or unknown>
Then the strongest evidence against your own answer, same format but starting "- AGAINST:" (search for it on purpose).
Then what you could not find out: "- OPEN: <question>".
Rules: every CLAIM and AGAINST quotes words that really are on the cited page (they are checked by fetching it);
prefer recent sources and say when a source is older than a year; no claim without a source; 3-10 claims."""
_FIELD = re.compile(r"\|\s*(SOURCE|QUOTE|TIER|DATE):\s*", re.I)
MAX_PAGE = 3_000_000
FETCH_S = 30  # a whole page, not each read: a server dripping bytes can't hold a worker
MIN_QUOTE = 4  # words: "the" is on every page


class Claim:
    def __init__(self, text, url, quote, tier, date, kind="claim"):
        self.text, self.url, self.quote, self.tier, self.date, self.kind = text, url, quote, tier, date, kind
        self.status, self.why = "unchecked", "not checked"


def parse_claims(text):
    """{"claims": [Claim], "open": [str]} from a researcher's claim lines; other lines are ignored."""
    claims, open_ = [], []
    for line in text.splitlines():
        m = re.match(r"\s*[-*]\s*(CLAIM|AGAINST|OPEN):\s*(.+)$", line, re.I)
        if not m:
            continue
        kind, rest = m.group(1).lower(), m.group(2)
        if kind == "open":
            open_.append(rest.strip())
            continue
        parts = _FIELD.split(rest)
        fields = {k.upper(): v.strip() for k, v in zip(parts[1::2], parts[2::2])}
        claims.append(Claim(parts[0].strip(), fields.get("SOURCE", ""), fields.get("QUOTE", "").strip('"“” '),
                            fields.get("TIER", "").lower() or "unknown", fields.get("DATE", "unknown"), kind))
    return {"claims": claims, "open": open_}


def public_https(url):
    """True for an https URL whose host resolves only to public addresses (no localhost, LAN or cloud metadata)."""
    try:
        u = urllib.parse.urlsplit(url)
        if u.scheme != "https" or not u.hostname:
            return False
        infos = socket.getaddrinfo(u.hostname, u.port or 443, proto=socket.IPPROTO_TCP)
    except (ValueError, OSError):
        return False
    # ponytail: resolved here and again by urllib (DNS rebinding could differ); pin the address if that ever matters
    return bool(infos) and all(ipaddress.ip_address(i[4][0].split("%")[0]).is_global for i in infos)


class _Redirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if not public_https(newurl):
            raise urllib.error.URLError(f"redirect to a non-public or non-https URL ({c.fit(newurl, 80)})")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def fetch(url):
    """(page text, None) or (None, why)."""
    if not public_https(url):
        return None, "not a public https URL"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Foreman research check)",
                                               "Accept": "text/html,text/plain,*/*"})
    deadline, raw = time.monotonic() + FETCH_S, b""
    try:
        with urllib.request.build_opener(_Redirect).open(req, timeout=15) as resp:
            while len(raw) < MAX_PAGE and time.monotonic() < deadline:
                chunk = resp.read1(65536)
                if not chunk:
                    break
                raw += chunk
            charset = resp.headers.get_content_charset() or "utf-8"
    except urllib.error.HTTPError as e:
        return None, f"HTTP {e.code}"
    except (urllib.error.URLError, http.client.HTTPException, OSError, ValueError) as e:
        return None, c.fit(str(getattr(e, "reason", e)) or type(e).__name__, 80)
    return _decode(raw, charset), None


def _decode(raw, charset):
    try:
        return raw.decode(charset, "replace")
    except LookupError:  # a charset the server made up
        return raw.decode("utf-8", "replace")


def _norm(text):
    text = re.sub(r"(?is)<(script|style)\b.*?</\1>", " ", text)
    text = html.unescape(re.sub(r"<[^>]+>", " ", text))
    text = text.translate(str.maketrans("‘’“”–— ", "''\"\"-- "))
    return re.sub(r"\s+", " ", text).strip().lower()


def verify(claims, fetch=fetch):
    """Mark each claim verified (its quote is on its page), not found, or unchecked (no source, or the page can't be
    read: a 403, a JavaScript-only page)."""
    def safe(url):  # one bad page costs its claims, never the run (and the paid research with it)
        try:
            return fetch(url)
        except Exception as e:
            return None, f"{type(e).__name__}: {c.fit(str(e), 60)}"
    urls = sorted({x.url for x in claims if x.url and x.quote})
    with ThreadPoolExecutor(8) as pool:
        pages = dict(zip(urls, pool.map(safe, urls)))
    for x in claims:
        if not x.url or not x.quote:
            x.status, x.why = "unchecked", "no source or quote"
            continue
        page, why = pages[x.url]
        if page is None:
            x.status, x.why = "unchecked", why
        elif len(_norm(x.quote).split()) < MIN_QUOTE:
            x.status, x.why = "unchecked", f"quote too short to check (under {MIN_QUOTE} words)"
        elif _norm(x.quote) in _norm(page):
            x.status, x.why = "verified", ""
        else:
            x.status, x.why = "not found", "the quoted words aren't on the page"


def _child(model, tools, system):
    return ["claude", "-p", "--model", model, "--no-session-persistence", "--output-format", "json",
            "--setting-sources", "project,local",
            "--tools", tools, *(["--allowed-tools", tools] if tools else []), *NO_MCP, "--append-system-prompt", system]


def _run(jobs, timeout):
    """[(stdout or None, error)] for [(argv, stdin)], run in parallel in a scratch folder."""
    with tempfile.TemporaryDirectory(prefix="fm-research-", dir=os.environ.get("XDG_RUNTIME_DIR") or None) as cwd:
        procs = []
        try:
            for argv, stdin in jobs:
                pr = subprocess.Popen(argv, cwd=cwd, text=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE)
                procs.append(pr)
                pr.stdin.write(stdin)
                pr.stdin.close()
        except OSError as e:
            for pr in procs:
                pr.kill()
                pr.communicate()
            raise OSError(f"can't start claude: {e} (is it on PATH and logged in?)")
        deadline, out = time.time() + timeout, []
        for pr in procs:
            try:
                so, se = pr.communicate(timeout=max(1, deadline - time.time()))
                so, usd = fmbudget.result(so)  # T-0227
                fmbudget.record("research", usd)
                out.append((so, None) if pr.returncode == 0 and so.strip() else
                           (None, f"exit {pr.returncode}: {c.fit((se or so).strip(), 160)}"))
            except subprocess.TimeoutExpired:
                pr.kill()
                pr.communicate()
                fmbudget.record("research", None, detail="timed out: cost unknown")
                out.append((None, f"timed out after {timeout}s"))
        return out


MARK = {"verified": "✓", "not found": "✗", "unchecked": "?"}


def _line(x):
    return (f"- {MARK[x.status]} {x.text} — {x.url or 'no source'}" + (f' "{x.quote}"' if x.quote else "")
            + f" ({x.tier}, {x.date}" + (f"; {x.status}: {x.why}" if x.status != "verified" else "; quote found") + ")")


def cmd_ask(args):
    import fmcli
    import fmrecall
    p = fmcli.resolve(args)
    q = args.question.strip()
    if not q:
        raise fmcli.UsageError("ask what?")
    # most of the question's words, or it isn't known yet
    known = [h for h in fmrecall.recall(p, q, n=5, cover=0.67) if h[1] in ("research", "brief", "decision")]
    subs = [s.strip() for s in args.sub or [] if s.strip()]
    try:
        fmbudget.check("research", fmbudget.estimate("research", (0 if subs else 1) + min(len(subs) or args.fanout,
                                                                                          args.fanout), 0.2),
                       "a smaller --fanout")
    except fmbudget.BudgetError as e:
        raise fmcli.UsageError(str(e))
    try:
        if not subs:
            [(plan, err)] = _run([(_child(args.model, "", PLANNER.format(n=args.fanout)), f"Question: {q}\n")],
                                 args.timeout)
            subs = [ln.strip()[2:].strip() for ln in (plan or "").splitlines() if ln.strip().startswith("- ")]
            if not subs:
                raise fmcli.UsageError(f"the planner gave no sub-questions ({err or c.fit(plan or '', 120)}); "
                                       f"pass them with --sub")
        subs = subs[:args.fanout]
        answers = _run([(_child(args.model, WEB_TOOLS, RESEARCHER), f"Question: {q}\nSub-question: {s}\n")
                        for s in subs], args.timeout)
    except OSError as e:
        raise fmcli.UsageError(str(e))
    parsed = [parse_claims(a or "") for a, _ in answers]
    claims = [x for got in parsed for x in got["claims"]]
    if not claims:
        why = "; ".join(err or c.fit(c.plain(a or ""), 100) for a, err in answers)
        raise fmcli.UsageError(f"no claims came back ({why})")
    if not args.no_verify:
        verify(claims)
    count = {k: sum(x.status == k for x in claims) for k in MARK}
    body = [f"# Research: {q}", "",
            f"Asked {c.now()[:10]} · {len(subs)} sub-question(s) · {len(claims)} claims: {count['verified']} quote "
            f"found, {count['not found']} quote not found, {count['unchecked']} unchecked. ✓ means the quoted words "
            f"are on the cited page, not that the claim is true.", ""]
    if known:
        body += ["## Already known (fm recall)"] + [f"- {h[2]}" for h in known] + [""]
    for s, got, (_, err) in zip(subs, parsed, answers):
        body += [f"## {s}"] + [_line(x) for x in got["claims"] if x.kind == "claim"]
        against = [_line(x) for x in got["claims"] if x.kind == "against"]
        body += (["", "Against:"] + against if against else []) + (["", "Open:"] + [f"- {o}" for o in got["open"]]
                                                                     if got["open"] else [])
        body += [f"- (failed: {err})"] if err else []
        body.append("")
    name = args.name or "ask-" + (re.sub(r"[^a-z0-9]+", "-", q.lower()).strip("-")[:40] or "q") + "-" \
        + time.strftime("%Y%m%d-%H%M")
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,80}", name):
        raise fmcli.UsageError(f"research name must be a plain file name, got {name!r}")
    path = os.path.join(p.dir, "research", name + ".md")
    with c.lock(p.dir):
        c.write_atomic(path, c.defang(c.redact("\n".join(body))))
        c.log_event(p, "research", task=args.task, data={"name": name, "claims": len(claims), **count},
                    session=fmcli.session())
        c.regen_views(p)
    res = {"path": path, "subs": subs, "claims": len(claims), "known": [h[2] for h in known], **count,
           "failed": [err for _, err in answers if err]}
    fmcli.out(args, {k.replace(" ", "_"): v for k, v in res.items()},
              f"Research note: {path}\n  {len(claims)} claims over {len(subs)} sub-question(s): "
              f"{count['verified']} ✓ quote found, {count['not found']} ✗ not on the page, {count['unchecked']} ? "
              f"unchecked" + (f"\n  already known: {'; '.join(c.fit(h[2], 80) for h in known[:3])}" if known else "")
              + "".join(f"\n  failed: {e}" for e in res["failed"]))
    if count["not found"]:
        print(f"fm: {count['not found']} claim(s) quote words that aren't on the cited page: treat them as unverified",
              file=sys.stderr)
