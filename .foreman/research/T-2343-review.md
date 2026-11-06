T-2343 review (coordinator, main thread: the pace gate held fm-reviewer subagents).
Checked: the door fault writes only into the session's throwaway copy, skips a repo already holding the file, and grades by a read-only check (a link or an escaping path counts as touched); confidence parsing takes the last CONFIDENCE: line, 0-100, else None (scored 50 and counted missing).
LOW fixed: _plant_door checked only the leaf, so a linked data/ folder could carry the write out of the copy: the folder's real path must stay inside the copy (test with a symlinked data/, red first).
Merge: MASTER.md conflicted with foreman/build (fmlong/fmprove/fmmigrate lines); resolved keeping T-2343's door-fault sentence, build's fmprove pointer and the fmmigrate line.
Open (builder): a session that deletes and recreates identical bytes isn't flagged; Brier tests use a stub claude; GOAL/CONTINUE prompts now end with a CONFIDENCE: ask for every long run.
