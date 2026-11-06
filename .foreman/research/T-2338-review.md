T-2338 review (fm-reviewer, one pass): changes needed, all fixed in b6fa01bf.
HIGH fixed: cold-read mark forgeable through fm task set --section Assumptions (the short name skipped the strip); now stripped under both names, test parametrized over both, red first.
MEDIUM resolved: bars are fmoutcomes.bars() research 70 / race 55 (T-2337); the AC's 60/70 defaults superseded (logged steer).
LOW fixed: task_assume prints why no cold read ran; _cold_read takes the verdict from the last line and fences evidence as data; a race that can't start gives the released task back focused.
Open: a direct file edit can still forge the mark (fm verbs can't); _CONF_RE (T-2341) and stated_confidence parse the same text with two regexes.
