**Answer**
- **o1-mini:** confirmed retired. OpenAI's page gives shutdown 2025-10-27, replacement `o4-mini`. It is already in `_RETIRED_ROWS` at `fmmodels.py:104`.
- **gpt-4:** refuted as "now retired". The page shows `gpt-4-0613` (aliases `gpt-4`, `gpt-4-completions`) shutting down 2026-10-23, which is tomorrow, with replacement `gpt-5.6-sol`. It becomes retired on 2026-10-23.
- **Contradictions:** I found none in the existing rows.
- **Fetch method:** WebFetch summarises the page with a small model. The quotes below are reproduced from that summary, not byte-checked against the page.

**Findings**

Rows to paste once past the date. On 2026-10-22 these are still future, so they feed the warning list, not `RETIRED`. All come from https://developers.openai.com/api/docs/deprecations (primary), announced 2026-04-22, confidence medium-high.
```
("openai","2026-10-23","gpt-5.6-terra","gpt-3.5-turbo-0125 gpt-3.5-turbo gpt-3.5-turbo-completions o4-mini o4-mini-2025-04-16"),
("openai","2026-10-23","gpt-5.6-sol","gpt-4-0613 gpt-4 gpt-4-completions gpt-4-0613-completions gpt-4-1106-preview gpt-4-turbo gpt-4-turbo-2024-04-09 gpt-4-turbo-completions gpt-4o-2024-05-13 o1 o1-2024-12-17 o3-mini o3-mini-2025-01-31 o1-pro o1-pro-2025-03-19"),
("openai","2026-10-23","gpt-5.6-luna","gpt-4.1-nano"),
```
- The page says "gpt-4-0613 | gpt-4, gpt-4-0613-completions, gpt-4-completions" and "gpt-3.5-turbo-0125 | gpt-3.5-turbo, gpt-3.5-turbo-completions".
- `o1-pro` replacement is `gpt-5.6-sol` with `reasoning.mode: pro`.

Future retirements, as (provider, date, replacement, ids):
- Anthropic, 2026-11-30, `claude-sonnet-5-5`: `claude-sonnet-4-5-20250929`. Source https://platform.claude.com/docs/en/about-claude/model-deprecations, deprecated 2026-09-30. Confidence high.
- OpenAI, 2026-12-11: `gpt-5-2025-08-07`, `o3-2025-04-16` and `o3-pro-2025-06-10` → `gpt-5.6-sol`. `gpt-5-mini-2025-08-07` → `gpt-5.6-terra`. `gpt-5-nano-2025-08-07` → `gpt-5.6-luna`. `gpt-5-pro-2025-10-06` → `gpt-5.6-sol`. Confidence medium.
- OpenAI, 2027-01-14, `gpt-6-luna`: `gpt-4o-2024-08-06`, `gpt-4o-2024-11-20`, `gpt-4o-mini-2024-07-18`, `gpt-4.1-2025-04-14`, `gpt-4.1-mini-2025-04-14`. Confidence medium.
- OpenAI, 2027-04-01: `gpt-5.3-codex` and `gpt-5.1` → `gpt-6-sol`. `gpt-5.4-nano` → `gpt-6-luna`. Confidence medium.
- Gemini, 2027-05-07, `gemini-3.5-flash-lite`: `gemini-3.1-flash-lite`. Source https://ai.google.dev/gemini-api/docs/deprecations. Confidence medium.

Gaps in `_RETIRED_ROWS`, not contradictions:
- OpenAI, 2026-07-23, `gpt-5.6-terra`: `gpt-4o-mini-search-preview-2025-03-11` and `gpt-4o-search-preview-2025-03-11`.
- OpenAI, 2026-07-23, `gpt-5.6-sol`: `o3-deep-research` and `o4-mini-deep-research`.
- OpenAI, 2024-12-06, `gpt-4o`: `gpt-4-vision-preview` and `gpt-4-1106-vision-preview`.
- OpenAI, 2024-09-13, `gpt-3.5-turbo`: `gpt-3.5-turbo-0301`.

**Risks / surprises**
- The default model at `fmmodels.py:63` is `gpt-4.1-mini`. Only the dated `gpt-4.1-mini-2025-04-14` is listed for 2027-01-14. The page doesn't say what happens to the bare alias.
- Anthropic's status table lists `claude-haiku-4-5-20251001` as "Not sooner than October 15, 2026". That date has passed and no retirement is announced. It is the replacement in several rows, so recheck it.
- Gemini `gemini-3.7-flash` and `gemini-3.5-flash` are aliases that auto-route to `gemini-3.8-flash` and `gemini-3.6-flash`. Neither is retired. Google says shutdown dates are "earliest possible".
- Some Gemini 3 and 2.5 GA models show "No shutdown date announced", so they are not warning candidates.

**Not checked**
- Non-text models (audio, image, embedding, realtime).
- Fine-tuned `ft-*` ids, which the OpenAI page lists as removed on 2026-10-23.
- Bedrock and Vertex schedules.
- Groq and OpenRouter ids.

**Noticed:** `fmmodels.py:103-104` has the OpenAI rows out of date order (2025-07-28 before 2025-10-27). This is harmless but inconsistent.
