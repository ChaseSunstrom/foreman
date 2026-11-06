# Blind spots — gen 4

Hunted from inputs Sampo didn't author: the user's steers of 2026-11-04 (seven, each one a miss nothing predicted), the
failures this session found only by looking (an exam arm scored on a missing key, a drift read that flagged a different
line on each run), and the gen-4 review on fable. Each class names its source, the rule it gives (recorded with
sampo decide --check) and the check that holds the rule.

## A filter that bans the subject the user wants
- Source: the user asked "how come ideas like that were never come up with during the moons?" after proposing Kalevala, an orchestrator of genesis towers. The moon generator's prompt said payoffs never land "on the harness's own parts", the write rule rejected payoffs naming towers, generations or Sampo, and the one-day kill judge rejected 70 of the 127 orchestration-like moons as "needs a tool nobody has built" (T-3045, T-3051).
- Rule: Every feature the user asks for that a generator never proposed is traced to the prompt line or rule that excluded it, and that line changes in the same generation.
- Check: python3 plugin/tests/run.py test_moons_scale

## A goal counted at the wrong stage
- Source: "I want it to literally output 10000 moons that will be used, not just in total". TARGET counted the candidate store, so the night's grow gate shut at 10,007 rows while 292 were kept (T-3042, T-3046).
- Rule: A target counts the outcome the user named (kept, closed, passing, used), never an upstream count that feeds it.
- Check: python3 plugin/tests/run.py test_moons_scale test_night

## A setting the user gave once, seen from one context only
- Source: the user's model key, stored for a login shell, was missing from hooks, the night job and the live service (T-3036), then from every exam sandbox, whose HOME is a throwaway: the 27B arm ran 0 of 3 on "LLM_API_KEY is not set" before anyone read its notes (T-3080). The user: "I shouldn't even need to tell you this".
- Rule: A setting the user gives once is checked from every context Sampo runs in (a login shell, a hook, a night job, a service, an exam sandbox) before it is called done.
- Check: python3 plugin/tests/run.py test_models

## A measurement that failed reads as a score
- Source: the same 27B arm reported "0/3 found, ends: other 3" in the arms log; the setup error lived only in each answer's notes, so the run read as a weak model, not a broken run.
- Rule: A run whose answers all carry a setup error (a missing key, an unreachable model) is reported as not run, never as a score.
- Check: python3 plugin/tests/run.py test_exam

## A rule built for circumstances that changed
- Source: "remove the weekly usage 80% lean on this project specifically, I have a few subscriptions to claude". The lean dates from one subscription and a usage scare (T-0198, 2026-09-26); the user switched subscriptions on 2026-11-03 and nothing re-asked (T-3049).
- Rule: A rule derived from the user's circumstances names them, and is revisited when Sampo sees them change (a new account, a new limit, a steer that contradicts it).
- Check: python3 plugin/tests/run.py test_budget

## A brand look on a working tool
- Source: "update the live view website to be more modern and have less forge specific things, unless turned on as a setting". The forge theme was carried "everywhere" (T-2788), including the operational page people read to run work (T-3054).
- Rule: A brand theme dresses brand surfaces (the site, the logo); a working tool defaults to a plain, modern look and carries the brand only as a setting.
- Check: python3 plugin/tests/run.py test_live_page

## Gains that stay where they landed
- Source: "keep building on built things going forward, for example if new things change how you behave, like coming up with ideas/more thoughts and such better, add that to the genesis of genesis, an infinite loop". Improvements to how Sampo thinks (prompts, ideas, moons yield) reached the next generation only when someone remembered them (T-3050, T-3081).
- Rule: A change that improves how Sampo thinks is registered when it closes and reaches every tower's next seed without anyone carrying it.
- Check: python3 plugin/tests/run.py test_genesis

## Far domain, medical screening: a positive screen is confirmed before it counts
- Source: gen 4's drift cold read flagged a different line on each rerun: first a fair one (the train split said to decide what held-out projects decide), then "Frontier digest … read, never cloned", which agrees with gen-0's NEVER (T-3056). Screening programmes confirm a positive with a second, different test before acting, because a single screen's false positives cost more than the delay.
- Rule: A single model verdict that blocks work is confirmed by a second, independent read before it blocks.
- Check: python3 plugin/tests/run.py test_genesis
