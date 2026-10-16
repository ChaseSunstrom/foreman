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
import http.client
import ipaddress
import itertools
import json
import os
import time
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
STOPS = {"stop": "end", "end_turn": "end", "stop_sequence": "end", "tool_calls": "tool_calls",
         "function_call": "tool_calls", "tool_use": "tool_calls", "length": "length", "max_tokens": "length"}

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
        with _LOCAL_OPENER.open(base_url + "/models", timeout=PROBE_TIMEOUT) as r:
            data = json.loads(r.read(1 << 20))
        ids = [x.get("id") for x in data.get("data") or [] if isinstance(x, dict)]
    except (*_TRANSPORT, ValueError, AttributeError, TypeError, RecursionError):
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


def complete(profile, messages, tools=None, max_tokens=2048, timeout=120):
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
