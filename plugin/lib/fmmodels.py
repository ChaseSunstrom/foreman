"""fm code's model layer (T-1211): one stdlib client for OpenAI-compatible and Anthropic endpoints.

Interface (the loop, T-1212, codes against exactly this):

  profiles() -> [profile]      every profile usable now: models.json's, then reachable local servers, then keyed clouds
  resolve(name=None) -> profile
      name given: the models.json profile so named, else the built-in cloud or local one; unknown -> ModelError.
      no name: models.json's "default", else the first local server to answer (probed in LOCAL's order, stopping at
      the first), else the first cloud whose key is set.
  profile = {name, kind: 'openai'|'anthropic', base_url, model, key_env (env var name or None), context, tools: bool}
  complete(profile, messages, tools=None, max_tokens=2048, timeout=120)
      -> {text, tool_calls: [{id, name, args}], usage: {in, out}, stop}
      stop is one vocabulary for both wire shapes: 'end' (finished), 'tool_calls' (wants tools run), 'length' (hit
      max_tokens; any tool call may be cut off); a reason outside those (content_filter, refusal, ...) passes through
      as the server sent it. A tool call the server gave no id gets a process-unique 'call_N'.
      timeout is per socket operation (connect, each read), not a wall-clock deadline: a server trickling bytes can
      hold a call longer, and the retries add up to 3 x timeout plus up to 2 x 20 s of waiting.
  extract_json(text) -> the first balanced JSON object in text (fenced or bare), or None (for models without tools)
  ModelError(msg, status=None)  every failure: HTTP status and a short body, never the key

Messages are OpenAI-shaped: [{role: system|user|assistant|tool, content, tool_calls?, tool_call_id?}]. An assistant
message's tool_calls may be OpenAI wire shape ({id, type, function: {name, arguments}}) or complete()'s own
({id, name, args}), so a reply can go straight back in. Tools are JSON-schema function specs, OpenAI shape
({type: function, function: {name, description, parameters}}) or the bare inner object. For kind 'anthropic' the
system messages become the top-level system field, tool results become tool_result blocks in a user turn, tool
calls become tool_use blocks, and same-role neighbours merge; the caller's messages are never changed. A tool call
whose arguments aren't JSON comes back as args {"_raw": "<the text>"}.

$FOREMAN_HOME/models.json (user-edited, optional; a bad field is a ModelError naming the file):
  {"default": "mine", "profiles": {"mine": {"kind": "openai", "base_url": "http://host/v1", "model": "x",
                                            "key_env": "MY_KEY", "context": 32768, "tools": true}}}
The built-in clouds' default model ids (CLOUD below) are only defaults: a models.json profile of the same name
overrides one.

429 and 5xx are retried (3 tries in all), waiting Retry-After (capped at 20 s) or 1 s, 2 s. Redirects are never
followed (urllib would carry the key to the new host). The key is read only from the env var the profile names,
stripped, refused if it holds control characters, never sent over plain http to a host that isn't loopback, and
scrubbed from every error; nothing here logs or writes it. A base_url with a user or password in it is refused.
"""
import datetime
import http.client
import ipaddress
import itertools
import json
import os
import shlex
import socket
import subprocess
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request

from fmcore import foreman_home

TRIES, RETRY_CAP, MAX_BODY, PROBE_TIMEOUT = 3, 20.0, 32 << 20, 0.3
ANTHROPIC_VERSION = "2023-06-01"
KINDS = ("openai", "anthropic")

# name, kind, base_url, default model, key env, context; first keyed one wins when nothing else is chosen
CLOUD = [
    ("anthropic", "anthropic", "https://api.anthropic.com/v1", "claude-sonnet-5-5", "ANTHROPIC_API_KEY", 200000),
    ("openai", "openai", "https://api.openai.com/v1", "gpt-4.1-mini", "OPENAI_API_KEY", 128000),
    ("openrouter", "openai", "https://openrouter.ai/api/v1", "openai/gpt-4.1-mini", "OPENROUTER_API_KEY", 128000),
    ("groq", "openai", "https://api.groq.com/openai/v1", "llama-3.3-70b-versatile", "GROQ_API_KEY", 128000),
    ("gemini", "openai", "https://generativelanguage.googleapis.com/v1beta/openai", "gemini-2.5-flash",
     "GEMINI_API_KEY", 1000000),
]
LOCAL = [("ollama", "http://127.0.0.1:11434/v1"), ("lmstudio", "http://127.0.0.1:1234/v1"),
         ("llamacpp", "http://127.0.0.1:8080/v1"), ("vllm", "http://127.0.0.1:8000/v1")]
LOCAL_CONTEXT = 8192

# T-1409/T-1433: model ids the provider no longer serves, read off each provider's deprecation page (research
# T-1409-retired-models, T-1433-deprecations). _RETIRED_ROWS: dates already past on RETIRED_AS_OF; _RETIRING_ROWS:
# announced later dates (they feed the "retiring soon" note, and count as retired once their day comes). Text/chat
# models only; Google's are its "earliest possible" dates. Dates came through a page summary, not byte-checked
# (medium confidence). Rows run newest first within each provider. ponytail: static and dated, so a stale table
# reads as stale; re-read the pages to refresh.
RETIRED_AS_OF = "2026-10-22"
RETIRING_DAYS = 60
_PAGES = {"anthropic": "https://platform.claude.com/docs/en/about-claude/model-deprecations",
          "openai": "https://developers.openai.com/api/docs/deprecations",
          "gemini": "https://ai.google.dev/gemini-api/docs/deprecations"}
_RETIRED_ROWS = [  # provider, retired on, replacement, ids
    ("anthropic", "2026-08-05", "claude-opus-4-8", "claude-opus-4-1-20250805"),
    ("anthropic", "2026-06-15", "claude-opus-4-8", "claude-opus-4-20250514"),
    ("anthropic", "2026-06-15", "claude-sonnet-5-5", "claude-sonnet-4-20250514"),
    ("anthropic", "2026-04-20", "claude-haiku-4-5-20251001", "claude-3-haiku-20240307"),
    ("anthropic", "2026-02-19", "claude-haiku-4-5-20251001", "claude-3-5-haiku-20241022"),
    ("anthropic", "2026-02-19", "claude-sonnet-5-5", "claude-3-7-sonnet-20250219"),
    ("anthropic", "2026-01-05", "claude-opus-4-8", "claude-3-opus-20240229"),
    ("anthropic", "2025-10-28", "claude-sonnet-5-5", "claude-3-5-sonnet-20240620 claude-3-5-sonnet-20241022"),
    ("anthropic", "2025-07-21", "claude-opus-4-8", "claude-2.0 claude-2.1"),
    ("anthropic", "2025-07-21", "claude-sonnet-5-5", "claude-3-sonnet-20240229"),
    ("anthropic", "2024-11-06", "claude-haiku-4-5-20251001",
     "claude-1.0 claude-1.1 claude-1.2 claude-1.3 claude-instant-1.0 claude-instant-1.1 claude-instant-1.2"),
    ("openai", "2026-10-01", "the most capable cyber model available to you", "gpt-5.4-cyber"),
    ("openai", "2026-09-28", "gpt-5.6-terra", "gpt-3.5-turbo-instruct babbage-002 davinci-002 gpt-3.5-turbo-1106"),
    ("openai", "2026-08-10", "gpt-5.6-sol", "gpt-5.2-chat-latest gpt-5.3-chat-latest"),
    ("openai", "2026-07-23", "gpt-5.6-sol",
     "gpt-5-chat-latest gpt-5-codex gpt-5.1-chat-latest gpt-5.1-codex gpt-5.1-codex-max gpt-5.2-codex "
     "o3-deep-research o4-mini-deep-research"),
    ("openai", "2026-07-23", "gpt-5.6-terra",
     "gpt-5.1-codex-mini gpt-4o-mini-search-preview-2025-03-11 gpt-4o-search-preview-2025-03-11"),
    ("openai", "2026-03-26", "gpt-5 or gpt-4.1", "gpt-4-0314 gpt-4-0125-preview gpt-4-turbo-preview"),
    ("openai", "2026-02-17", "gpt-5.1-chat-latest", "chatgpt-4o-latest"),
    ("openai", "2026-02-12", "gpt-5-codex-mini", "codex-mini-latest"),
    ("openai", "2025-10-27", "o4-mini", "o1-mini"),
    ("openai", "2025-07-28", "o3", "o1-preview"),
    ("openai", "2025-07-14", "gpt-4.1", "gpt-4.5-preview"),
    ("openai", "2025-06-06", "gpt-4o", "gpt-4-32k gpt-4-32k-0613 gpt-4-32k-0314"),
    ("openai", "2024-12-06", "gpt-4o", "gpt-4-vision-preview gpt-4-1106-vision-preview"),
    ("openai", "2024-09-13", "gpt-3.5-turbo", "gpt-3.5-turbo-0613 gpt-3.5-turbo-16k-0613 gpt-3.5-turbo-0301"),
    ("gemini", "2026-07-28", "gemini-3.8-flash", "gemini-2.5-computer-use-preview-10-2025"),
    ("gemini", "2026-06-01", "gemini-3.6-flash", "gemini-2.0-flash gemini-2.0-flash-001"),
    ("gemini", "2026-06-01", "gemini-3.1-flash-lite", "gemini-2.0-flash-lite gemini-2.0-flash-lite-001"),
    ("gemini", "2026-05-25", "gemini-3.1-flash-lite", "gemini-3.1-flash-lite-preview"),
    ("gemini", "2026-03-31", "gemini-3.1-flash-lite", "gemini-2.5-flash-lite-preview-09-2025"),
    ("gemini", "2026-03-09", "gemini-3.1-pro-preview", "gemini-3-pro-preview"),
    ("gemini", "2026-02-17", "gemini-3.6-flash", "gemini-2.5-flash-preview-09-25"),
    ("gemini", "2025-12-09", "gemini-3.1-flash-lite",
     "gemini-2.0-flash-lite-preview gemini-2.0-flash-lite-preview-02-05"),
    ("gemini", "2025-12-02", "gemini-3.1-pro-preview",
     "gemini-2.5-pro-preview-03-25 gemini-2.5-pro-preview-05-06 gemini-2.5-pro-preview-06-05"),
    ("gemini", "2025-11-18", "gemini-3.6-flash", "gemini-2.5-flash-preview-05-20"),
]
_RETIRING_ROWS = [  # provider, retires on, replacement, ids: dates after RETIRED_AS_OF
    ("anthropic", "2026-11-30", "claude-sonnet-5-5", "claude-sonnet-4-5-20250929"),
    ("openai", "2027-04-01", "gpt-6-sol", "gpt-5.3-codex gpt-5.1"),
    ("openai", "2027-04-01", "gpt-6-luna", "gpt-5.4-nano"),
    ("openai", "2027-01-14", "gpt-6-luna",
     "gpt-4o-2024-08-06 gpt-4o-2024-11-20 gpt-4o-mini-2024-07-18 gpt-4.1-2025-04-14 gpt-4.1-mini-2025-04-14"),
    ("openai", "2026-12-11", "gpt-5.6-sol", "gpt-5-2025-08-07 o3-2025-04-16 o3-pro-2025-06-10 gpt-5-pro-2025-10-06"),
    ("openai", "2026-12-11", "gpt-5.6-terra", "gpt-5-mini-2025-08-07"),
    ("openai", "2026-12-11", "gpt-5.6-luna", "gpt-5-nano-2025-08-07"),
    ("openai", "2026-10-23", "gpt-5.6-terra",
     "gpt-3.5-turbo-0125 gpt-3.5-turbo gpt-3.5-turbo-completions o4-mini o4-mini-2025-04-16"),
    ("openai", "2026-10-23", "gpt-5.6-sol",
     "gpt-4-0613 gpt-4 gpt-4-completions gpt-4-0613-completions gpt-4-1106-preview gpt-4-turbo "
     "gpt-4-turbo-2024-04-09 gpt-4-turbo-completions gpt-4o-2024-05-13 o1 o1-2024-12-17 o3-mini "
     "o3-mini-2025-01-31 o1-pro o1-pro-2025-03-19"),
    ("openai", "2026-10-23", "gpt-5.6-luna", "gpt-4.1-nano"),
    ("gemini", "2027-05-07", "gemini-3.5-flash-lite", "gemini-3.1-flash-lite"),
]


def _table(rows):
    return {i: (day, repl, _PAGES[prov]) for prov, day, repl, ids in rows for i in ids.split()}


RETIRED = _table(_RETIRED_ROWS)
RETIRING = _table(_RETIRING_ROWS)


def _today(today):
    """today if given, else $FOREMAN_TODAY when it parses as YYYY-MM-DD (a test pins the clock with it), else the
    clock."""
    for d in (today, os.environ.get("FOREMAN_TODAY")):
        try:
            return datetime.date.fromisoformat(d)
        except (TypeError, ValueError):
            pass
    return datetime.date.today()


def _lookup(table, model_id):
    if not isinstance(model_id, str):
        return None
    hit = table.get(model_id.strip().lower().rsplit("/", 1)[-1])
    return hit and {"date": hit[0], "replacement": hit[1], "source": hit[2]}


def retired(model_id, today=None):
    """{"date", "replacement", "source"} when model_id (a provider prefix like openai/ or models/ is ignored) is on
    RETIRED, or on RETIRING with its date reached by today (YYYY-MM-DD; default $FOREMAN_TODAY, then the clock)."""
    hit = _lookup(RETIRED, model_id) or _lookup(RETIRING, model_id)
    return hit if hit and hit["date"] <= _today(today).isoformat() else None


def retiring(model_id, today=None):
    """Same shape, for an id on RETIRING whose date is after today but at most RETIRING_DAYS away, else None."""
    hit = _lookup(RETIRING, model_id)
    t = _today(today)
    soon = (t + datetime.timedelta(days=RETIRING_DAYS)).isoformat()
    return hit if hit and t.isoformat() < hit["date"] <= soon else None


STOPS = {"stop": "end", "end_turn": "end", "stop_sequence": "end", "tool_calls": "tool_calls",
         "function_call": "tool_calls", "tool_use": "tool_calls", "length": "length", "max_tokens": "length"}

STOP = object()  # T-1388: an on_line answer that ends the call now (fmcode.STOP is this one)
RESOLVE_TIMEOUT = 2  # T-1421: seconds a base_url's host may take to resolve before it's let through unchecked
_RESOLVED = {}  # T-1436: host -> (when, addresses) of a lookup that answered, kept RESOLVED_FOR s
RESOLVED_FOR = 60
_sleep = time.sleep  # tests swap it out
_ids = itertools.count(1)
_TRANSPORT = (urllib.error.URLError, OSError, http.client.HTTPException)


class ModelError(Exception):
    def __init__(self, msg, status=None):
        super().__init__(msg)
        self.status = status


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **kw):
        return None  # urllib then raises the 3xx as an HTTPError


_OPENER = urllib.request.build_opener(_NoRedirect)
_LOCAL_OPENER = urllib.request.build_opener(_NoRedirect, urllib.request.ProxyHandler({}))  # localhost, never a proxy


def _scrub(s, key):
    return s.replace(key, "***") if key else s


def _of(v, typ):
    """v when it's a typ, else an empty one: a reply field of the wrong JSON type reads as missing."""
    return v if isinstance(v, typ) else typ()


# ---------------------------------------------------------------- profiles

def _profile(name, d, where):
    def bad(why):
        raise ModelError(f"{where}: profile {name!r}: {why}")

    if not isinstance(d, dict):
        bad("must be an object")
    p = {"name": name, "kind": d.get("kind", "openai"), "base_url": d.get("base_url", ""), "model": d.get("model", ""),
         "key_env": d.get("key_env"), "context": d.get("context", LOCAL_CONTEXT), "tools": d.get("tools", True)}
    if p["kind"] not in KINDS:
        bad(f"kind must be one of {', '.join(KINDS)}, not {p['kind']!r}")
    if not isinstance(p["base_url"], str) or not isinstance(p["model"], str):
        bad("base_url and model must be strings")
    if p["key_env"] is not None and not (isinstance(p["key_env"], str) and p["key_env"]):
        bad("key_env must be an environment variable name or null")
    if isinstance(p["context"], bool) or not isinstance(p["context"], int) or p["context"] <= 0:
        bad("context must be a positive whole number")
    if not isinstance(p["tools"], bool):
        bad("tools must be true or false")
    p["base_url"] = p["base_url"].rstrip("/")
    return p


def _config():
    path = os.path.join(foreman_home(), "models.json")
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        profs = data.get("profiles") or {}
        return data.get("default"), {n: _profile(n, d, path) for n, d in profs.items()}
    except FileNotFoundError:
        return None, {}
    except (OSError, ValueError, AttributeError, TypeError, RecursionError) as e:
        raise ModelError(f"{path}: unreadable models.json ({e})") from None


def configured():
    """(models.json's default name or None, {name: profile}); ModelError when the file is unreadable."""
    return _config()


def _cloud(name=None, keyed=True):
    return [{"name": n, "kind": k, "base_url": u, "model": mo, "key_env": env, "context": ctx, "tools": True}
            for n, k, u, mo, env, ctx in CLOUD if (name is None or n == name) and (not keyed or os.environ.get(env))]


def _probe(name, base_url):
    """The local server's profile when it answers /models with at least one model, else None."""
    try:
        _check_url({"name": name}, base_url, None)  # T-1438: a metadata or link-local address isn't probed either
        with _LOCAL_OPENER.open(base_url + "/models", timeout=PROBE_TIMEOUT) as r:
            data = json.loads(r.read(1 << 20))
        ids = [x.get("id") for x in data.get("data") or [] if isinstance(x, dict)]
    except (ModelError, *_TRANSPORT, ValueError, AttributeError, TypeError, RecursionError):
        return None
    ids = [i for i in ids if isinstance(i, str) and i]
    return ids and {"name": name, "kind": "openai", "base_url": base_url, "model": ids[0], "key_env": None,
                    "context": LOCAL_CONTEXT, "tools": False}  # small local models: extract_json, not native tools


def _local(name=None):
    """Reachable local servers, probed lazily in LOCAL's order (up to 0.3 s each on a filtered port)."""
    for n, u in LOCAL:
        if name is None or n == name:
            p = _probe(n, u)
            if p:
                yield p


def profiles():
    _, conf = _config()
    return list(conf.values()) + list(_local()) + _cloud()


def resolve(name=None):
    default, conf = _config()
    name = name or default
    if name:
        if name in conf:
            return conf[name]
        found = next(iter(_cloud(name, keyed=False)), None) or next(_local(name), None)
        if not found:
            raise ModelError(f"no model profile named {name!r} (models.json, {', '.join(n for n, *_ in CLOUD)}, "
                             f"{', '.join(n for n, _ in LOCAL)})")
        return found
    found = next(_local(), None) or next(iter(_cloud()), None)
    if not found:
        raise ModelError("no model: no local server answered and no API key is set "
                         f"({', '.join(c[4] for c in CLOUD)}); or add $FOREMAN_HOME/models.json")
    return found


# ---------------------------------------------------------------- wire shapes

def _tool_spec(t):
    return t.get("function", t) if isinstance(t, dict) else {}


def _call_parts(c):
    """(id, name, args dict) of a tool call in either OpenAI wire shape or complete()'s shape."""
    if "function" in c:
        f = c["function"] or {}
        return c.get("id"), f.get("name"), _args(f.get("arguments"))
    return c.get("id"), c.get("name"), c.get("args") or {}


def _args(raw):
    if isinstance(raw, dict):
        return raw
    try:
        v = json.loads(raw or "{}")
        return v if isinstance(v, dict) else {"_raw": raw}
    except (ValueError, TypeError, RecursionError):
        return {"_raw": raw}


def _stop(raw, calls):
    if STOPS.get(raw) == "length":
        return "length"
    return "tool_calls" if calls else STOPS.get(raw, raw or "end")


def to_openai(messages):
    out = []
    for msg in messages:
        if msg.get("tool_calls"):
            msg = dict(msg, tool_calls=[
                {"id": i, "type": "function", "function": {"name": n, "arguments": json.dumps(a)}}
                for i, n, a in map(_call_parts, msg["tool_calls"])])
        out.append(msg)
    return out


def _blocks(content):
    if isinstance(content, list):
        return list(content)  # a copy: merging appends to it, and the caller resends its messages
    return [{"type": "text", "text": content}] if content else []


def to_anthropic(messages):
    """(system text or None, Anthropic messages) from OpenAI-shaped ones."""
    system, out = [], []
    for msg in messages:
        role = msg.get("role")
        if role == "system":
            system.append(msg.get("content") or "")
            continue
        if role == "tool":
            role, blocks = "user", [{"type": "tool_result", "tool_use_id": msg.get("tool_call_id"),
                                     "content": msg.get("content") or ""}]
        else:
            blocks = _blocks(msg.get("content"))
            if role == "assistant":
                blocks += [{"type": "tool_use", "id": i, "name": n, "input": a}
                           for i, n, a in map(_call_parts, msg.get("tool_calls") or [])]
        if not blocks:
            continue
        if out and out[-1]["role"] == role:
            out[-1]["content"] += blocks
        else:
            out.append({"role": role, "content": blocks})
    return ("\n\n".join(system) or None), out


def to_anthropic_tools(tools):
    return [{"name": s.get("name"), "description": s.get("description", ""),
             "input_schema": s.get("parameters") or {"type": "object", "properties": {}}}
            for s in map(_tool_spec, tools)]


# ---------------------------------------------------------------- transport

def _loopback(host):
    if host == "localhost":
        return True
    try:
        return ipaddress.ip_address(host).is_loopback
    except ValueError:
        return False


def is_loopback(host):
    """True for localhost and loopback addresses: where a key may go over plain http."""
    return _loopback(host)


def _link_local(host):
    """T-1395: 169.254.0.0/16 or fe80::/10, in any spelling the resolver takes (2852039166, 0xa9.0xfe.0xa9.0xfe,
    ::ffff:169.254.169.254, fullwidth digits or ideographic dots, which IDNA folds to ASCII), and AWS's IPv6 metadata
    fd00:ec2::254; T-1421: Alibaba's 100.100.100.200 and Azure's wireserver 168.63.129.16 too, and a hostname any of
    whose addresses is one of these (looked up for at most RESOLVE_TIMEOUT s). ponytail: the request resolves the name
    again, so a name that answers differently the second time (DNS rebinding) or that times out here isn't caught; pin
    the checked address on the connection if that matters."""
    import threading
    host = unicodedata.normalize("NFKC", host).replace("。", ".")  # what the IDNA encoder sends
    try:
        ips = [ipaddress.ip_address(host)]
    except ValueError:
        try:  # the legacy IPv4 forms urllib's resolver also accepts, read without any lookup
            ips = [ipaddress.IPv4Address(socket.inet_aton(host))]
        except (OSError, ValueError):
            when, kept = _RESOLVED.get(host, (0, None))
            found = list(kept) if kept and time.monotonic() - when < RESOLVED_FOR else []

            def look():
                try:
                    found.extend(ipaddress.ip_address(a[4][0].split("%")[0]) for a in socket.getaddrinfo(host, None))
                except (OSError, ValueError, UnicodeError):
                    pass
            if not found:
                t = threading.Thread(target=look, daemon=True)  # getaddrinfo has no timeout of its own
                t.start()
                t.join(RESOLVE_TIMEOUT)
                if found:  # only an answer is kept: a failed or slow lookup is tried again next call
                    _RESOLVED[host] = (time.monotonic(), list(found))
            ips = list(found)  # a copy: a lookup still running past the timeout changes nothing here
    bad = {ipaddress.ip_address(a) for a in ("fd00:ec2::254", "100.100.100.200", "168.63.129.16")}
    return any(ip.is_link_local or ip in bad for ip in (getattr(x, "ipv4_mapped", None) or x for x in ips))


def _check_url(profile, base, key):
    """Refuse a base_url the key mustn't go to; the messages never echo base_url (it may hold a password)."""
    who = f"profile {profile.get('name')!r}"
    try:
        u = urllib.parse.urlsplit(base)
        host = u.hostname
    except ValueError:
        raise ModelError(f"{who}: base_url is not a URL") from None
    if u.scheme not in ("http", "https") or not host:
        raise ModelError(f"{who}: base_url must be an http(s) URL")
    if "@" in u.netloc:
        raise ModelError(f"{who}: base_url must not carry a user or password (put the key in key_env)")
    if _link_local(host):
        raise ModelError(f"{who}: base_url is, or resolves to, a link-local or cloud metadata address "
                         "(169.254.0.0/16, fe80::/10, fd00:ec2::254, 100.100.100.200, 168.63.129.16); refused")
    if key and u.scheme == "http" and not _loopback(host):
        raise ModelError(f"{who}: refusing to send {profile.get('key_env')} over plain http to {host}; use https")


def _post(url, body, headers, timeout, key):
    data = json.dumps(body).encode()
    for attempt in range(TRIES):
        req = urllib.request.Request(url, data=data, method="POST",
                                     headers=dict(headers, **{"Content-Type": "application/json"}))
        try:
            with _OPENER.open(req, timeout=timeout) as r:
                raw = r.read(MAX_BODY + 1)
        except urllib.error.HTTPError as e:
            status, hdrs = e.code, e.headers or {}
            try:
                text = e.read(2000).decode("utf-8", "replace")
            except (OSError, http.client.HTTPException):
                text = ""
            finally:
                e.close()
            if (status == 429 or status >= 500) and attempt < TRIES - 1:
                try:
                    delay = float(hdrs.get("Retry-After"))
                except (TypeError, ValueError):
                    delay = float(2 ** attempt)
                _sleep(min(max(delay, 0.0), RETRY_CAP) if delay == delay else 1.0)  # NaN != NaN
                continue
            where = f" -> {hdrs.get('Location')}" if 300 <= status < 400 else ""
            raise ModelError(_scrub(f"{url}: HTTP {status}{where}: {' '.join(text.split())[:300]}", key), status)
        except _TRANSPORT as e:  # refused, DNS, timeout, cut off: no retry, the caller decides
            raise ModelError(_scrub(f"{url}: {getattr(e, 'reason', None) or e!r}", key)) from None
        except ValueError as e:  # http.client refusing a header value: its message may hold the key
            raise ModelError(_scrub(f"{url}: request refused: {e}", key)) from None
        if len(raw) > MAX_BODY:
            raise ModelError(f"{url}: reply over {MAX_BODY >> 20} MB")
        try:
            v = json.loads(raw)
        except (ValueError, RecursionError):
            raise ModelError(_scrub(f"{url}: not JSON: {raw[:200].decode('utf-8', 'replace')}", key)) from None
        if not isinstance(v, dict):
            raise ModelError(f"{url}: reply is not a JSON object")
        return v


# T-1329: what a CLI's stream shows: claude's stream-json tool_use blocks, as (action, the input key it acts on)
TOOL_SHOW = {"Read": ("read", "file_path"), "Edit": ("edit", "file_path"), "MultiEdit": ("edit", "file_path"),
             "Write": ("edit", "file_path"), "NotebookEdit": ("edit", "notebook_path"), "Bash": ("run", "command"),
             "Grep": ("search", "pattern"), "Glob": ("search", "pattern")}
CLI_KEEP = 8 << 20  # a CLI's stdout kept for its reply


def heartbeat():
    """Seconds between working events while a CLI turn shows nothing (FM_HEARTBEAT, for tests; default 10)."""
    try:
        return max(0.1, float(os.environ.get("FM_HEARTBEAT") or 10))
    except ValueError:
        return 10.0


def stall():
    """T-1336: seconds with no byte at all before a CLI turn gets a stalled event (FM_STALL, for tests; default 120)."""
    try:
        return max(0.1, float(os.environ.get("FM_STALL") or 120))
    except ValueError:
        return 120.0


def stream_tools(line, root=""):
    """T-1329: the tool uses in one line of claude's stream-json as [(action, target)], each target one line of at
    most 200 characters, relative when it's in root; [] for any other line, a malformed one included."""
    if '"tool_use"' not in line:
        return []
    try:
        e = json.loads(line)
        content = e["message"]["content"] if e.get("type") == "assistant" else []
    except (ValueError, TypeError, KeyError, AttributeError):
        return []
    out = []
    for b in content if isinstance(content, list) else []:
        if isinstance(b, dict) and b.get("type") == "tool_use":
            action, key = TOOL_SHOW.get(b.get("name"), (_shown(str(b.get("name") or "tool").lower())[:40], None))
            target = str((b.get("input") if isinstance(b.get("input"), dict) else {}).get(key) or "") if key else ""
            if root and target.startswith(root.rstrip(os.sep) + os.sep):
                target = os.path.relpath(target, root)
            target = _shown(target)
            out.append((action, target if len(target) <= 200 else target[:199] + "…"))
    return out


def _shown(s):
    """One line a terminal only prints: whitespace runs as one space, no control character (ESC, BEL, C1)."""
    return "".join(c for c in " ".join(s.split()) if c.isprintable())


def stream_result(line):
    """A claude stream-json line that is the run's final result, as a dict; None for any other."""
    if '"result"' not in line:
        return None
    try:
        e = json.loads(line)
    except ValueError:
        return None
    return e if isinstance(e, dict) and e.get("type") == "result" else None


def _cli(profile, messages, timeout):
    """T-1320: a slot filled by a coding CLI run once in its read-only mode (claude -p … --permission-mode plan): the
    conversation as one prompt, its reply as the text. Claude's stream-json shows each tool use live (T-1329) and its
    final result line gives the reply and the token counts; a quiet call sends heartbeats."""
    import tempfile
    import threading
    import fmcore
    prompt = "\n\n".join(f"{msg['role'].upper()}:\n{msg['content']}" for msg in messages
                          if isinstance(msg.get("content"), str))
    argv = [w.replace("{prompt}", prompt) for w in shlex.split(profile["argv"])]
    limit = max(timeout, profile.get("timeout") or 0)
    stream, shown, found, out, stopped = profile.get("stream") == "claude", profile.get("on_line"), [], bytearray(), []
    done = threading.Event()  # set once the call returns: a line a leftover grandchild prints shows nothing

    def sink(chunk):
        out.extend(chunk)
        del out[:-CLI_KEEP]

    def on_line(line):
        if not stream or done.is_set() or stopped:  # T-1438: after a STOP, the chunk's other lines kill nothing again
            return False
        res = stream_result(line)
        if res:
            found.append(res)
        got = shown and shown(line)
        if got is STOP:  # T-1426: the caller's check stopped the call (a lean planner's init loaded too much)
            stopped.append(line)
            fmcore.kill_group(proc)
        return bool(got)
    live = profile.get("heartbeat") and profile["heartbeat"]()
    beat = live and (lambda *a: done.is_set() or live(*a))
    with tempfile.TemporaryFile() as err:
        try:
            proc = subprocess.Popen(argv, cwd=profile.get("cwd"), env=profile.get("env"), stdin=subprocess.DEVNULL,
                                    stdout=subprocess.PIPE, stderr=err, start_new_session=True)
        except OSError as e:
            raise ModelError(f"{profile['name']}: {e}") from None
        reader = threading.Thread(target=fmcore.pump, args=(proc.stdout, sink, on_line, beat and heartbeat(), beat),
                                  daemon=True)
        reader.start()
        try:
            proc.wait(limit)
        except subprocess.TimeoutExpired:  # it and everything it started: nothing keeps working after we give up
            fmcore.kill_group(proc)
            proc.wait()
            raise ModelError(f"{profile['name']}: no reply in {limit} s") from None
        finally:
            if proc.poll() is None:  # T-1326: fm code stopped mid-call (SystemExit from a signal): the CLI goes too
                fmcore.kill_group(proc)
            reader.join(5)
            done.set()
        err.seek(0)
        stderr = err.read().decode("utf-8", "replace")
    stdout = out.decode("utf-8", "replace")
    if stopped:
        raise ModelError(f"{profile['name']}: stopped at a line its caller refused")
    if proc.returncode:
        raise ModelError(f"{profile['name']}: exit {proc.returncode}: {(stderr or stdout).strip()[-300:]}")
    if stream and not found:
        raise ModelError(f"{profile['name']}: its stream ended with no result line: {(stderr or stdout).strip()[-300:]}")
    if stream and not isinstance(found[-1].get("result"), str):  # error_max_turns and the like carry no reply
        raise ModelError(f"{profile['name']}: {found[-1].get('subtype') or 'its result had no reply text'}")
    try:
        got = found[-1] if found else json.loads(stdout)
    except ValueError:
        got = None
    if not (isinstance(got, dict) and isinstance(got.get("result"), str)):
        return {"text": stdout.strip(), "tool_calls": [], "usage": {"in": 0, "out": 0}, "stop": "end"}
    if got.get("is_error"):
        raise ModelError(f"{profile['name']}: {got['result'][:300]}")
    u = _of(got.get("usage"), dict)
    seen = sum(v for k in ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens")
               if type(v := u.get(k)) is int)  # T-1423: a "10" or null isn't added (Run.usage zeroes the rest)
    return {"text": got["result"], "tool_calls": [], "usage": {"in": seen, "out": u.get("output_tokens") or 0},
            "stop": "end"}


def complete(profile, messages, tools=None, max_tokens=2048, timeout=120):
    if profile.get("kind") == "cli":
        return _cli(profile, messages, timeout)
    base = (profile.get("base_url") or "").rstrip("/")
    env, key = profile.get("key_env"), None
    if env:
        key = (os.environ.get(env) or "").strip()
        if not key:
            raise ModelError(f"profile {profile.get('name')!r}: {env} is not set")
        if any(ord(ch) < 32 or ord(ch) == 127 for ch in key):
            raise ModelError(f"profile {profile.get('name')!r}: {env} holds control characters")
    _check_url(profile, base, key)
    if profile.get("kind") == "anthropic":
        system, msgs = to_anthropic(messages)
        body = {"model": profile.get("model"), "max_tokens": max_tokens, "messages": msgs}
        if system:
            body["system"] = system
        if tools:
            body["tools"] = to_anthropic_tools(tools)
        headers = {"anthropic-version": ANTHROPIC_VERSION}
        if key:
            headers["x-api-key"] = key
        r = _post(base + "/messages", body, headers, timeout, key)
        content = [b for b in _of(r.get("content"), list) if isinstance(b, dict)]
        usage = _of(r.get("usage"), dict)
        calls = [{"id": b.get("id") or f"call_{next(_ids)}", "name": b.get("name"), "args": _args(b.get("input"))}
                 for b in content if b.get("type") == "tool_use"]
        return {"text": "".join(b.get("text", "") for b in content if b.get("type") == "text"), "tool_calls": calls,
                "usage": {"in": usage.get("input_tokens", 0), "out": usage.get("output_tokens", 0)},
                "stop": _stop(r.get("stop_reason"), calls)}
    body = {"model": profile.get("model"), "max_tokens": max_tokens, "messages": to_openai(messages)}
    if tools:
        body["tools"] = [t if "function" in t else {"type": "function", "function": t} for t in tools]
    headers = {"Authorization": f"Bearer {key}"} if key else {}
    r = _post(base + "/chat/completions", body, headers, timeout, key)
    try:
        choice = r["choices"][0]
        msg = choice.get("message") or {}
        calls = [{"id": i or f"call_{next(_ids)}", "name": n, "args": a}
                 for i, n, a in map(_call_parts, msg.get("tool_calls") or [])]
    except (KeyError, IndexError, TypeError, AttributeError):
        raise ModelError(_scrub(f"{base}: reply has no usable choices: {json.dumps(r)[:200]}", key)) from None
    usage = _of(r.get("usage"), dict)
    return {"text": msg.get("content") or "", "tool_calls": calls,
            "usage": {"in": usage.get("prompt_tokens", 0), "out": usage.get("completion_tokens", 0)},
            "stop": _stop(choice.get("finish_reason"), calls)}


# ---------------------------------------------------------------- JSON from free text

def extract_json(text, tries=64):
    """The first balanced JSON object in text, or None. Tries the first `tries` '{' positions; each try is one linear
    scan, so hostile input costs at most tries x len(text)."""
    if not text:
        return None
    dec, i = json.JSONDecoder(), text.find("{")
    while i != -1 and tries > 0:
        tries -= 1
        try:
            v, _ = dec.raw_decode(text, i)
            if isinstance(v, dict):
                return v
        except (ValueError, RecursionError):
            pass
        i = text.find("{", i + 1)
    return None
