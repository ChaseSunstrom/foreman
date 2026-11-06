**1. Answer.** The three pages were fetched on 2026-10-21 and give the retired text/chat ids and replacements below. WebFetch passes page text through a small model, so a main-thread spot-check of the Anthropic and OpenAI ids is worthwhile. Image, audio, video and embedding models are omitted. Google's page says its dates are "earliest possible dates".

**2. Findings**

**Anthropic** (primary): https://platform.claude.com/docs/en/about-claude/model-deprecations. `docs.claude.com` redirects there. No page date is shown, but the newest entry is 2026-09-30. Quote: "Retired: The model is no longer available for use. Requests to retired models fail." Confidence: high.

| Model id | Retired | Replacement |
|---|---|---|
| claude-opus-4-1-20250805 | 2026-08-05 | claude-opus-4-8 |
| claude-opus-4-20250514 | 2026-06-15 | claude-opus-4-8 |
| claude-sonnet-4-20250514 | 2026-06-15 | claude-sonnet-5-5 |
| claude-3-haiku-20240307 | 2026-04-20 | claude-haiku-4-5-20251001 |
| claude-3-5-haiku-20241022 | 2026-02-19 | claude-haiku-4-5-20251001 |
| claude-3-7-sonnet-20250219 | 2026-02-19 | claude-sonnet-5-5 |
| claude-3-opus-20240229 | 2026-01-05 | claude-opus-4-8 |
| claude-3-5-sonnet-20240620 | 2025-10-28 | claude-sonnet-5-5 |
| claude-3-5-sonnet-20241022 | 2025-10-28 | claude-sonnet-5-5 |
| claude-2.0 | 2025-07-21 | claude-opus-4-8 |
| claude-2.1 | 2025-07-21 | claude-opus-4-8 |
| claude-3-sonnet-20240229 | 2025-07-21 | claude-sonnet-5-5 |
| claude-1.0, 1.1, 1.2, 1.3, claude-instant-1.0, 1.1, 1.2 | 2024-11-06 | claude-haiku-4-5-20251001 |

Deprecated with a future retirement date:
- claude-sonnet-4-5-20250929 retires 2026-11-30. Replacement is claude-sonnet-5-5.
- claude-mythos-preview is deprecated (2026-06-09), with the retirement date "To be announced" and no replacement stated.

**OpenAI** (primary): https://developers.openai.com/api/docs/deprecations. `platform.openai.com` returns a 301 to it. No page date is shown, but the newest entry is 2026-10-14. Quote: "Fine-tuned versions of these models follow the same shutdown schedule as their underlying base models." Confidence: medium-high.

| Model id | Shutdown | Replacement |
|---|---|---|
| gpt-5.4-cyber | 2026-10-01 | "most capable cyber model available to you" |
| gpt-3.5-turbo-instruct, babbage-002, davinci-002, gpt-3.5-turbo-1106 | 2026-09-28 | gpt-5.6-terra |
| gpt-5.2-chat-latest, gpt-5.3-chat-latest | 2026-08-10 | gpt-5.6-sol |
| gpt-5-chat-latest, gpt-5-codex, gpt-5.1-chat-latest, gpt-5.1-codex, gpt-5.1-codex-max, gpt-5.2-codex | 2026-07-23 | gpt-5.6-sol |
| gpt-5.1-codex-mini | 2026-07-23 | gpt-5.6-terra |
| gpt-4-0314, gpt-4-0125-preview (including gpt-4-turbo-preview) | 2026-03-26 | gpt-5 or gpt-4.1* |
| chatgpt-4o-latest | 2026-02-17 | gpt-5.1-chat-latest |
| codex-mini-latest | 2026-02-12 | gpt-5-codex-mini |
| o1-preview | 2025-07-28 | o3 |
| o1-mini | 2025-10-27 | o4-mini |
| gpt-4.5-preview | 2025-07-14 | gpt-4.1 |
| gpt-4-32k, gpt-4-32k-0613, gpt-4-32k-0314 | 2025-06-06 | gpt-4o |
| gpt-3.5-turbo-0613, gpt-3.5-turbo-16k-0613 | 2024-09-13 | gpt-3.5-turbo |

Dated 2026-10-23, so not yet past as of 2026-10-21: gpt-3.5-turbo-0125, gpt-4-0613, gpt-4-1106-preview, gpt-4-turbo, gpt-4.1-nano, gpt-4o-2024-05-13, o1, o1-pro, o3-mini, o4-mini.

Other future dates:
- 2026-12-11: gpt-5-2025-08-07, gpt-5-mini-2025-08-07, gpt-5-nano-2025-08-07, gpt-5-pro-2025-10-06, o3-2025-04-16, o3-pro-2025-06-10.
- 2027-01-14: gpt-4o-2024-08-06, gpt-4o-2024-11-20, gpt-4o-mini-2024-07-18, gpt-4.1-2025-04-14, gpt-4.1-mini-2025-04-14.
- 2027-04-01: gpt-5.3-codex, gpt-5.1, gpt-5.4-nano.

**Gemini** (primary): https://ai.google.dev/gemini-api/docs/deprecations. Page date: "Last updated 2026-10-20 UTC." Confidence: medium-high.

| Model id | Shutdown | Replacement |
|---|---|---|
| gemini-2.0-flash, gemini-2.0-flash-001 | 2026-06-01 | gemini-3.6-flash |
| gemini-2.0-flash-lite, gemini-2.0-flash-lite-001 | 2026-06-01 | gemini-3.1-flash-lite |
| gemini-2.5-computer-use-preview-10-2025 | 2026-07-28 | gemini-3.8-flash |
| gemini-3.1-flash-lite-preview | 2026-05-25 | gemini-3.1-flash-lite |
| gemini-2.5-flash-lite-preview-09-2025 | 2026-03-31 | gemini-3.1-flash-lite |
| gemini-3-pro-preview | 2026-03-09 | gemini-3.1-pro-preview |
| gemini-2.5-flash-preview-09-25 | 2026-02-17 | gemini-3.6-flash |
| gemini-2.5-flash-preview-05-20 | 2025-11-18 | gemini-3.6-flash |
| gemini-2.5-pro-preview-03-25, -05-06, -06-05 | 2025-12-02 | gemini-3.1-pro-preview |
| gemini-2.0-flash-lite-preview, gemini-2.0-flash-lite-preview-02-05 | 2025-12-09 | gemini-3.1-flash-lite |

Future dates: gemini-3.1-flash-tts-preview and gemini-2.5-flash-preview-tts retire 2026-11-17. gemini-3.1-flash-lite retires 2027-05-07 (replacement gemini-3.5-flash-lite). gemini-3.7-flash and gemini-3.5-flash show "N/A" with replacements gemini-3.8-flash and gemini-3.6-flash.

**3. Risks / surprises**
- Google dates are "earliest possible" dates, so a model may be retired later than listed.
- OpenAI aliases (gpt-4, o1, o3-mini, o4-mini and others) share their base model's date. Match on aliases as well as dated ids.
- Gemini rows come from a model-summarised table, and the "Gemini 3" section's placement of gemini-3-flash-preview was ambiguous. I left that row out.
- Anthropic's retired list is the most reliable, because the page explicitly marks each model "Retired".

**4. Not checked**
- Third-party providers.
- Bedrock and Vertex schedules, which the Anthropic page says differ.
- Google's models page, and whether Gemini models served through Vertex follow the same dates.
- Raw page HTML, since only the summarised text was available.

**Noticed:** none
