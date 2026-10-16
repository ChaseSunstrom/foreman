"""fm code's model layer (T-1211): one stdlib client for OpenAI-compatible and Anthropic endpoints.

Interface (the loop, T-1212, codes against exactly this):

  profiles() -> [profile]      every profile usable now: models.json's, then reachable local servers, then keyed clouds
  resolve(name=None) -> profile
      name given: the models.json profile so named, else the built-in cloud or local one; unknown -> ModelError.
      no name: models.json's "default", else the first reachable local server, else the first cloud whose key is set.
  profile = {name, kind: 'openai'|'anthropic', base_url, model, key_env (env var name or None), context, tools: bool}
  complete(profile, messages, tools=None, max_tokens=2048, timeout=120)
      -> {text, tool_calls: [{id, name, args}], usage: {in, out}, stop}
  extract_json(text) -> the first balanced JSON object in text (fenced or bare), or None (for models without tools)
  ModelError(msg, status=None)  every failure: HTTP status and a short body, never the key

Messages are OpenAI-shaped: [{role: system|user|assistant|tool, content, tool_calls?, tool_call_id?}]. An assistant
message's tool_calls may be OpenAI wire shape ({id, type, function: {name, arguments}}) or complete()'s own
({id, name, args}), so a reply can go straight back in. Tools are JSON-schema function specs, OpenAI shape
({type: function, function: {name, description, parameters}}) or the bare inner object. For kind 'anthropic' the
system messages become the top-level system field, tool results become tool_result blocks in a user turn, tool
calls become tool_use blocks, and same-role neighbours merge. A tool call whose arguments aren't JSON comes back as
args {"_raw": "<the text>"}.

$FOREMAN_HOME/models.json (user-edited, optional):
  {"default": "mine", "profiles": {"mine": {"kind": "openai", "base_url": "http://host/v1", "model": "x",
                                            "key_env": "MY_KEY", "context": 32768, "tools": true}}}

429 and 5xx are retried (3 tries in all), waiting Retry-After (capped at 20 s) or 1 s, 2 s. Redirects are never
followed (urllib would carry the key to the new host). The key is read only from the env var the profile names and
is scrubbed from every error; nothing here logs or writes it.
"""
import json
import os
import time
import urllib.error
import urllib.request

TRIES, RETRY_CAP, MAX_BODY, PROBE_TIMEOUT = 3, 20.0, 32 << 20, 0.3
ANTHROPIC_VERSION = "2023-06-01"

# name, kind, base_url, default model, key env, context; first keyed one wins when nothing else is chosen
CLOUD = [
    ("anthropic", "anthropic", "https://api.anthropic.com/v1", "claude-sonnet-4-5", "ANTHROPIC_API_KEY", 200000),
    ("openai", "openai", "https://api.openai.com/v1", "gpt-4.1-mini", "OPENAI_API_KEY", 128000),
    ("openrouter", "openai", "https://openrouter.ai/api/v1", "openai/gpt-4.1-mini", "OPENROUTER_API_KEY", 128000),
    ("groq", "openai", "https://api.groq.com/openai/v1", "llama-3.3-70b-versatile", "GROQ_API_KEY", 128000),
    ("gemini", "openai", "https://generativelanguage.googleapis.com/v1beta/openai", "gemini-2.5-flash",
     "GEMINI_API_KEY", 1000000),
]
LOCAL = [("ollama", "http://127.0.0.1:11434/v1"), ("lmstudio", "http://127.0.0.1:1234/v1"),
         ("llamacpp", "http://127.0.0.1:8080/v1"), ("vllm", "http://127.0.0.1:8000/v1")]
LOCAL_CONTEXT = 8192

_sleep = time.sleep  # tests swap it out


class ModelError(Exception):
    def __init__(self, msg, status=None):
        super().__init__(msg)
        self.status = status


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **kw):
        return None  # urllib then raises the 3xx as an HTTPError


_OPENER = urllib.request.build_opener(_NoRedirect)
_LOCAL_OPENER = urllib.request.build_opener(_NoRedirect, urllib.request.ProxyHandler({}))  # localhost, never a proxy


# ---------------------------------------------------------------- profiles

def _home():
    h = os.environ.get("FOREMAN_HOME")
    return os.path.abspath(os.path.expanduser(h)) if h else os.path.join(os.path.expanduser("~"), ".claude", "foreman")


def _profile(name, d):
    return {"name": name, "kind": d.get("kind", "openai"), "base_url": str(d.get("base_url", "")).rstrip("/"),
            "model": d.get("model", ""), "key_env": d.get("key_env"), "context": int(d.get("context", LOCAL_CONTEXT)),
            "tools": bool(d.get("tools", True))}


def _config():
    path = os.path.join(_home(), "models.json")
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        profs = data.get("profiles") or {}
        return data.get("default"), {n: _profile(n, d) for n, d in profs.items()}
    except FileNotFoundError:
        return None, {}
    except (OSError, ValueError, AttributeError, TypeError) as e:
        raise ModelError(f"{path}: unreadable models.json ({e})")


def _cloud(name=None, keyed=True):
    return [{"name": n, "kind": k, "base_url": u, "model": mo, "key_env": env, "context": ctx, "tools": True}
            for n, k, u, mo, env, ctx in CLOUD if (name is None or n == name) and (not keyed or os.environ.get(env))]


def _probe(name, base_url):
    """The local server's profile when it answers /models with at least one model, else None."""
    try:
        with _LOCAL_OPENER.open(base_url + "/models", timeout=PROBE_TIMEOUT) as r:
            ids = [x.get("id") for x in json.loads(r.read(1 << 20)).get("data") or [] if isinstance(x, dict)]
    except (OSError, ValueError, AttributeError, TypeError):
        return None
    ids = [i for i in ids if isinstance(i, str) and i]
    return ids and {"name": name, "kind": "openai", "base_url": base_url, "model": ids[0], "key_env": None,
                    "context": LOCAL_CONTEXT, "tools": False}  # small local models: extract_json, not native tools


def _local(name=None):
    # ponytail: probes run one after another, up to 0.3 s each on a filtered port; threads if that ever bites
    return [p for p in (_probe(n, u) for n, u in LOCAL if name is None or n == name) if p]


def profiles():
    _, conf = _config()
    return list(conf.values()) + _local() + _cloud()


def resolve(name=None):
    default, conf = _config()
    name = name or default
    if name:
        if name in conf:
            return conf[name]
        found = _cloud(name, keyed=False) or _local(name)
        if not found:
            raise ModelError(f"no model profile named {name!r} (models.json, {', '.join(n for n, *_ in CLOUD)}, "
                             f"{', '.join(n for n, _ in LOCAL)})")
        return found[0]
    found = _local() or _cloud()
    if not found:
        raise ModelError("no model: no local server answered and no API key is set "
                         f"({', '.join(c[4] for c in CLOUD)}); or add $FOREMAN_HOME/models.json")
    return found[0]


# ---------------------------------------------------------------- wire shapes

def _tool_spec(t):
    return t.get("function", t) if isinstance(t, dict) else {}


def _call_parts(c):
    """(id, name, args dict) of a tool call in either OpenAI wire shape or complete()'s shape."""
    if "function" in c:
        f = c["function"]
        return c.get("id"), f.get("name"), _args(f.get("arguments"))
    return c.get("id"), c.get("name"), c.get("args") or {}


def _args(raw):
    if isinstance(raw, dict):
        return raw
    try:
        v = json.loads(raw or "{}")
        return v if isinstance(v, dict) else {"_raw": raw}
    except (ValueError, TypeError):
        return {"_raw": raw}


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
        return content
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

def _post(url, body, headers, timeout, secret):
    def scrub(s):
        return s.replace(secret, "***") if secret else s

    data = json.dumps(body).encode()
    for attempt in range(TRIES):
        req = urllib.request.Request(url, data=data, method="POST",
                                     headers=dict(headers, **{"Content-Type": "application/json"}))
        try:
            with _OPENER.open(req, timeout=timeout) as r:
                raw = r.read(MAX_BODY + 1)
            if len(raw) > MAX_BODY:
                raise ModelError(f"{url}: reply over {MAX_BODY >> 20} MB")
            try:
                return json.loads(raw)
            except ValueError:
                raise ModelError(scrub(f"{url}: not JSON: {raw[:200].decode('utf-8', 'replace')}"))
        except urllib.error.HTTPError as e:
            status, wait = e.code, e.headers.get("Retry-After") if e.headers else None
            try:
                text = e.read(2000).decode("utf-8", "replace")
            except OSError:
                text = ""
            finally:
                e.close()
            if (status == 429 or status >= 500) and attempt < TRIES - 1:
                try:
                    delay = float(wait)
                except (TypeError, ValueError):
                    delay = float(2 ** attempt)
                _sleep(min(max(delay, 0.0), RETRY_CAP) if delay == delay else 1.0)  # NaN != NaN
                continue
            raise ModelError(scrub(f"{url}: HTTP {status}: {' '.join(text.split())[:300]}"), status)
        except (urllib.error.URLError, OSError) as e:  # refused, DNS, timeout: no retry, the caller decides
            raise ModelError(scrub(f"{url}: {getattr(e, 'reason', e)}"))


def complete(profile, messages, tools=None, max_tokens=2048, timeout=120):
    base = (profile.get("base_url") or "").rstrip("/")
    if not base.startswith(("http://", "https://")):
        raise ModelError(f"profile {profile.get('name')!r}: base_url must be http(s), got {base!r}")
    env, key = profile.get("key_env"), None
    if env:
        key = os.environ.get(env)
        if not key:
            raise ModelError(f"profile {profile.get('name')!r}: {env} is not set")
    if profile.get("kind") == "anthropic":
        system, msgs = to_anthropic(messages)
        body = {"model": profile["model"], "max_tokens": max_tokens, "messages": msgs}
        if system:
            body["system"] = system
        if tools:
            body["tools"] = to_anthropic_tools(tools)
        headers = {"anthropic-version": ANTHROPIC_VERSION}
        if key:
            headers["x-api-key"] = key
        r = _post(base + "/messages", body, headers, timeout, key)
        content = [b for b in r.get("content") or [] if isinstance(b, dict)]
        usage = r.get("usage") or {}
        return {"text": "".join(b.get("text", "") for b in content if b.get("type") == "text"),
                "tool_calls": [{"id": b.get("id"), "name": b.get("name"), "args": _args(b.get("input"))}
                               for b in content if b.get("type") == "tool_use"],
                "usage": {"in": usage.get("input_tokens", 0), "out": usage.get("output_tokens", 0)},
                "stop": r.get("stop_reason")}
    body = {"model": profile["model"], "max_tokens": max_tokens, "messages": to_openai(messages)}
    if tools:
        body["tools"] = [t if "function" in t else {"type": "function", "function": t} for t in tools]
    headers = {"Authorization": f"Bearer {key}"} if key else {}
    r = _post(base + "/chat/completions", body, headers, timeout, key)
    try:
        choice = r["choices"][0]
        msg = choice.get("message") or {}
    except (KeyError, IndexError, TypeError, AttributeError):
        raise ModelError(f"{base}: reply has no choices: {json.dumps(r)[:200]}")
    usage = r.get("usage") or {}
    return {"text": msg.get("content") or "",
            "tool_calls": [{"id": i, "name": n, "args": a}
                           for i, n, a in map(_call_parts, msg.get("tool_calls") or [])],
            "usage": {"in": usage.get("prompt_tokens", 0), "out": usage.get("completion_tokens", 0)},
            "stop": choice.get("finish_reason")}


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
