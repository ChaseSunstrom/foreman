// Foreman for opencode, written by `fm agents install opencode` (`fm agents uninstall opencode` removes it).
// Every tool call goes past Foreman's guard first, and Foreman's state goes into the system prompt, through the hook
// Claude Code runs: `hook --agent opencode EVENT` with the event as JSON on stdin.
const HOOK: string = __HOOK__;

type Answer = { code: number; err: string; deny?: string; context?: string };

async function hook(event: string, payload: Record<string, unknown>): Promise<Answer> {
  const p = Bun.spawn([HOOK, "--agent", "opencode", event], {
    stdin: new Blob([JSON.stringify(payload)]),
    stdout: "pipe",
    stderr: "pipe",
  });
  const [out, err, code] = await Promise.all([new Response(p.stdout).text(), new Response(p.stderr).text(), p.exited]);
  let answer = {};
  try {
    answer = JSON.parse(out || "{}");
  } catch {}
  return { code, err, ...answer };
}

export const Foreman = async ({ directory }: { directory: string }) => {
  const notes = new Map<string, { start?: string; prompt?: string }>(); // per session: Foreman's context to add
  return {
    // a refusal, or a hook that can't run at all, stops the tool call (the guard fails closed)
    "tool.execute.before": async (input: { tool: string; sessionID: string }, output: { args: unknown }) => {
      const r = await hook("PreToolUse", { session_id: input.sessionID, cwd: directory, tool: input.tool, args: output.args });
      if (r.code !== 0) throw new Error(r.deny || r.err.trim() || "Foreman's guard refused this tool call");
    },
    // a criterion's verify command run by hand is recorded as its evidence
    "tool.execute.after": async (input: { tool: string; sessionID: string; args?: unknown }, output: { output?: string }) => {
      try {
        await hook("PostToolUse", { session_id: input.sessionID, cwd: directory, tool: input.tool, args: input.args, output: output.output ?? "" });
      } catch {}
    },
    "chat.message": async (input: { sessionID: string }, output: { parts: { type: string; text?: string }[] }) => {
      try {
        const n = notes.get(input.sessionID) ?? { start: (await hook("SessionStart", { session_id: input.sessionID, cwd: directory })).context };
        const prompt = output.parts.filter((p) => p.type === "text").map((p) => p.text ?? "").join("\n");
        n.prompt = (await hook("UserPromptSubmit", { session_id: input.sessionID, cwd: directory, prompt })).context;
        notes.set(input.sessionID, n);
      } catch {}
    },
    "experimental.chat.system.transform": async (input: { sessionID?: string }, output: { system: string[] }) => {
      const n = notes.get(input.sessionID ?? "");
      for (const t of [n?.start, n?.prompt]) if (t) output.system.push(t);
    },
  };
};
