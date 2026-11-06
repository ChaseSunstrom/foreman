---
id: T-2494
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-01T18:46:02Z
updated: 2026-11-01T19:55:58Z
base: fbd3e4992ce4b9bea3279d27db65ba7bb3088362
base_tree: 44e93240554db5ee441e1d5584d02c9051e02a6d
predict_minutes: 10
predict_attempts: 1
plan0_at: 2026-11-01T19:44:06Z
plan0_scope: []
verified: strong
---
# The model registry reads TYPESAFE_BASE_URL (selfjev-4b/jeff behind the Jev-compatible…
## Raw request
> FEATURE: the model registry reads TYPESAFE_BASE_URL (selfjev-4b/jeff behind the Jev-compatible API, as the user's T-2437 steer names): a profile from it, local when its host is loopback, no key sent it didn't name
## Interpretation
Readings: (a) likeliest: the user's servers become model-layer backends without secrets on disk: a models.json profile for the llama-swap route (https://<host>/llm/v1, qwen3.8-27b, key_env LLM_API_KEY) marked own (a server the user owns: the night shadow pass may use it for a non-sensitive project; a sensitive project still uses loopback only), and TYPESAFE_BASE_URL read from the environment as the T-2437 steer named. (b) Treat the user's server as local: rejected, it is reached over a public hostname, so a sensitive repo's text would leave the machine. Fails if: LLM_API_KEY isn't in Foreman's environment (then the backend errors fast and decide() moves on).
## Assumptions (confidence)
## Acceptance criteria
- [x] an own profile is parsed and validated; registry orders loopback, own, cloud; shadow_pass answers through an own backend for a plain project and never for a sensitive one; TYPESAFE_BASE_URL makes a typesafe profile, unset makes none; the doctor line names own backends — verify with `python3 plugin/tests/run.py test_models test_doctor`
## Non-goals
## Approach (options → choice → why)
1) an own flag on models.json profiles: registry orders loopback, own, cloud; shadow_pass takes local or own; decide() still skips any non-loopback backend for a sensitive project; _env_profiles adds TYPESAFE_BASE_URL; fm doctor's backends line names the own bucket. Fails if: own is set on a stranger's server (it is the user's file to write). 2) use what exists: a plain models.json profile with no flag. Fails if: the night shadow pass (local only) never asks it, so no use is ever scored. 3) do less: mark the profile local. Fails if: it breaks the sensitive-repo rule. Choice 1 (85%): one flag, read in two places, keeps the sensitive rule intact and lets the shadow pass score the user's server.
## Risks and rollback
A 46 s reply makes the night tick slow: the shadow pass is capped at 5 rows a tick. The key never lands on disk; models.json names only its variable. Rollback: revert and remove the profile.
## Execution prompt
## Steps
1. [x] red tests: own flag, ordering, shadow pass, TYPESAFE env profile, doctor bucket
2. [x] fmmodels own flag + _env_profiles + shadow_pass; fmdoctor bucket; models.json profile in FOREMAN_HOME
## Resume here
## Docs impact
README.md, MASTER.md, CHANGELOG.md, .gitignore
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_models.OwnServer test_doctor.ModelBackends` → ✗ exit 1 · Ran 4 tests in 0.6s (2 classes, 16 at a time; slowest: ModelBackends 0s, OwnServer 0s) / FAILED (2 classes: test_models.OwnServer, test_doctor.ModelBackends) [ran] [tree e115f2f6773a] (2026-11-01T19:44:50Z)
- (step 2) `python3 plugin/tests/run.py test_models test_doctor test_mcp` → exit 0 · Ran 199 tests in 9.6s (60 classes, 16 at a time; slowest: ViewsRepair 6s, LockProbe 6s, Bench 5s) / OK [ran] [tree 38656c327dc1] (2026-11-01T19:46:34Z)
- `python3 plugin/tests/run.py test_models.OwnServer test_doctor.ModelBackends` → ✗ exit 1 · Ran 4 tests in 2.2s (2 classes, 16 at a time; slowest: ModelBackends 0s, OwnServer 0s) / FAILED (2 classes: test_models.OwnServer, test_doctor.ModelBackends) (start tree + this task's tests) [ran] [tree 38656c327dc1] (2026-11-01T19:46:38Z)
- `python3 plugin/tests/run.py test_models.OwnServer test_doctor.ModelBackends` → exit 0 · Ran 4 tests in 0.7s (2 classes, 16 at a time; slowest: ModelBackends 0s, OwnServer 0s) / OK [ran] [tree 38656c327dc1] (2026-11-01T19:46:38Z)
- (ac 1) `python3 plugin/tests/run.py test_models test_doctor` → exit 0 · Ran 170 tests in 4.6s (45 classes, 16 at a time; slowest: ViewsRepair 4s, LockProbe 3s, Bench 2s) / OK [ran] [tree 38656c327dc1] (2026-11-01T19:55:20Z)
- (audit intent) `self-review: own is absent from a profile unless true (keeps every other profile's shape), validated as a bool; registry orders loopback, own, cloud; shadow_pass takes own only for a non-sensitive project and decide() still skips every non-loopback backend for a sensitive one; TYPESAFE_BASE_URL names its key only when TYPESAFE_API_KEY is set; models.json is gitignored and holds no secret` → the user's llama-swap route is a backend (a live decide() through it answered FIX 0.95 in 1.05 s), the T-2437 TYPESAFE_BASE_URL steer is read, and a sensitive project's text never leaves the machine [tree 38656c327dc1] (2026-11-01T19:55:20Z)
- (audit adversary) `self-review: own is absent from a profile unless true (keeps every other profile's shape), validated as a bool; registry orders loopback, own, cloud; shadow_pass takes own only for a non-sensitive project and decide() still skips every non-loopback backend for a sensitive one; TYPESAFE_BASE_URL names its key only when TYPESAFE_API_KEY is set; models.json is gitignored and holds no secret` → the key stays in the environment (key_env names it); the profile file can't be committed; complete()'s URL checks (no key over plain http to a non-loopback host, no metadata hosts) still apply to the new profiles [tree 38656c327dc1] (2026-11-01T19:55:20Z)
- (audit edge) `self-review: own is absent from a profile unless true (keeps every other profile's shape), validated as a bool; registry orders loopback, own, cloud; shadow_pass takes own only for a non-sensitive project and decide() still skips every non-loopback backend for a sensitive one; TYPESAFE_BASE_URL names its key only when TYPESAFE_API_KEY is set; models.json is gitignored and holds no secret` → own: 'yes' is refused; with LLM_API_KEY unset the backend fails fast and decide() moves on; a sensitive project with only an own backend spends nothing [tree 38656c327dc1] (2026-11-01T19:55:20Z)
## Log
- 2026-11-01T18:46:02Z created
- 2026-11-01T18:46:12Z set tier=S
- 2026-11-01T19:21:28Z steer (user 2026-11-01): the OpenAI-compatible endpoint at https://<host>/ is usable for model-layer work. Probed: /v1/models is the Jarvis app's 404 page; /api/v1/models, /api/openai/v1/models and /api/models all answer 401 {"ok":false,"error":"sign in to the console first"}, so the base is under /api and needs a key. Scope widens: the registry also reads JARVIS_BASE_URL (default https://<host>/api/v1 when JARVIS_API_KEY is set) with key_env JARVIS_API_KEY, https only, cloud (not loopback) so a sensitive project never uses it; the probe sends the key only to that configured host
- 2026-11-01T19:23:59Z probe with the two keys the user gave (MODELS_API_KEY, LLM_API_KEY; not stored): every /api route (v1/models, openai/v1/models, v1/chat/completions POST, openai/v1/chat/completions POST) answers 401 'sign in to the console first' with either key as Bearer or X-API-Key; /v1, /models/v1, /llm/v1 are the app's 404 page. The console's session check fronts all of /api, so the OpenAI route is elsewhere or needs the console cookie: waiting on the user for the exact route
- 2026-11-01T19:26:40Z probe 2 (JARVIS_TOKEN, console password; neither stored): console sign-in POST /api/console {password} → 200 ok; with that session /api/v1/models, /api/openai/v1/models, /api/models, /api/llm/v1/models are the app's 404 page; POST /v1/{chat/completions,responses,messages,completions} → 405 SvelteKit 'Method Not Allowed' (page routes). The app's settings name LLM_URL (an internal OpenAI-compatible base: llama-swap in jarvis-models, bearer LLM_API_KEY), the model manager on port 8001 (MODELS_API_KEY) and the adapter's front door (JARVIS_API_KEY): none is served on <host>'s public routes. Waiting on the user for the base URL that reaches llama-swap or the adapter
- 2026-11-01T19:30:00Z found (user's JARVIS_PUBLIC_URL): https://<host>/hermes/v1 is OpenAI-compatible behind the console session (POST /api/console {password} sets the cookie; bearer tokens alone get 401). /models lists one model, 'jarvis' (owned_by hermes); one chat call answered 'ok' in 18.1 s. It is the Hermes agent, not the raw LLM: it has the user's memory context and tools, so untrusted text sent to it could steer a tool and Foreman's prompts may land in Jarvis's memory. The raw model (LLM_URL http://jarvis-models:8000/v1, qwen3.8-27b, 256k context) is compose-internal: not reachable here (DNS), nor <host>:8000 or 192.168.9.59:8000 (no route), and ssh to the box timed out. Plan: profile auth kind 'login' (password from JARVIS_CONSOLE_PASSWORD, https, cookie kept in memory per process, sent only to the configured host); cloud-class (never a sensitive project, never the night shadow pass); a raw llama-swap route would be the better backend
- 2026-11-01T19:40:07Z the user's llama-swap route is up: https://<host>/llm/v1 (bearer LLM_API_KEY; 401 without). Models: qwen3.8-27b (loaded, 256k), qwen3.6-35b, qwen3.8-27b-uncensored. A decide-shaped call returned valid JSON {choice, probability} in 46.3 s (52 completion tokens, 35 reasoning). Plan: a models.json profile (kind openai, that base_url, model qwen3.8-27b, key_env LLM_API_KEY) plus an 'own' flag for a server the user owns: the night shadow pass may use it for non-sensitive projects; a sensitive project still never does (not loopback). Needs the user: LLM_API_KEY in the environment Foreman runs in (shell and the systemd user units)
- 2026-11-01T19:44:04Z set tier=M
- 2026-11-01T19:44:05Z criterion 1 verify: `python3 plugin/tests/run.py test_models` → `python3 plugin/tests/run.py test_models test_doctor`
- 2026-11-01T19:44:05Z criterion 1 text: TYPESAFE_BASE_URL set → registry() lists a typesafe profile, local only when its host is loopback; unset → none; no key sent unless TYPESAFE_API_KEY is set → an own profile is parsed and validated; registry orders loopback, own, cloud; shadow_pass answers through an own backend for a plain project and never for a sensitive one; TYPESAFE_BASE_URL makes a typesafe profile, unset makes none; the doctor line names own backends
- 2026-11-01T19:44:05Z planned: it has criteria and steps
- 2026-11-01T19:44:05Z set approved=True
- 2026-11-01T19:44:06Z focused
- 2026-11-01T19:44:06Z predicted from its closes: 10 min, 1 attempt(s)
- 2026-11-01T19:46:38Z scope: fmmodels own flag/_env_profiles/registry/shadow_pass, fmdoctor own bucket, .gitignore models.json, tests, README/MASTER/CHANGELOG; models.json (gitignored) holds the jarvis profile; a live decide() through it answered FIX 0.95 in 1.05 s
- 2026-11-01T19:55:56Z done
- 2026-11-01T19:55:58Z committed 47fdcaa5 (8 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2437 [FEATURE L, done, 5 steps] Gen 2: a model layer (user steer 2026-10-31, start after round 1). (1) A… — lesson: A user's next-generation request has to reach the n…
- T-2489 [FEATURE M, done, 3 steps] Model layer surfaces: MCP decide tool, fm doctor backend health, the site's Model layer… — lesson: README has a 2000-word visible budge…
- decision 2026-10-31: Standing rule (user steer 2026-10-31): gen 2 builds a model layer, small specialist models wherever a decision, ranking or lookup is the job, backen…
- T-2486 [FEATURE M, done, 3 steps] The user's four model rules as tests: no model import in fmguard or the evidence gates,… — lesson: A rule is only standing when a test …
## Lessons
- a user's own server is neither local nor cloud: give it its own class so the private-data rule (loopback only) and the cost rule (cheapest first) can each be applied honestly
## Plan gaps
- failed first: step 1 red tests: own flag, ordering, shadow pass, TYPESAFE env profile, doctor bucket
## Files touched
- plugin/tests/test_doctor.py
- plugin/tests/test_models.py
- plugin/lib/fmdoctor.py
- plugin/lib/fmmodels.py
- .gitignore
- models.json
- CHANGELOG.md
- MASTER.md
- README.md
