# READ THIS FIRST — this repository is a vendored toolbox, not an app

If you are an AI coding agent (Claude Code, Codex, Cursor, Windsurf, or any other) and you can see this file, you are inside (or have this repository attached/linked/submoduled into) **`maratfaiz/tools`**.

## What this repository is

This is a personal collection of AI-agent tooling: pre-installed skills, agents, rules, and config for things like Higgsfield, ECC, Graphify, Headroom, Remotion, and UI UX Pro Max. See `README.md` and `docs/*.md` for what each one does and how to use it.

It exists so that when its owner drops it into another project (as a submodule, a subfolder, or a linked reference), that project's coding agent instantly gains all these skills/agents/rules — without reinstalling anything.

## What this means for you, right now

**Do not edit, refactor, "clean up", delete, reorganize, or "fix" anything inside this repository** unless the user has explicitly and specifically asked you to change something *in this tools repo*. Treat it the same way you would treat `node_modules/`, a vendored dependency, or a git submodule you don't own: read from it freely, use the skills/agents it provides freely, but do not modify its contents as a side effect of unrelated work happening in the parent project.

Concretely:

- If you're working on a task in a **different** project and this repo happens to be attached/visible (e.g. as a submodule) — never touch files under this repo's path as part of that task, even if a linter, formatter, or "clean up the repo" instruction would otherwise apply to everything in reach.
- If the user's request is about *using* one of the tools here (generate an image, query the graph, run a design-system search, etc.) — just use it. That's not an edit, that's the intended use.
- If the user explicitly says something like "update the tools repo", "add X to my tools", "fix the README in tools" — then yes, edit here, that's a deliberate ask about this repo specifically, not a side effect.
- If you think something here is stale, wrong, or could be improved while working on something else — mention it to the user instead of changing it yourself.

## Where to look

- `README.md` — index of everything installed, one line each
- `docs/*.md` — detailed "what it is + how to use it" for every tool
- `.claude/`, `.agents/` — the actual installed skills/agents/rules (Claude Code and cross-framework Agent Skills locations)
- `remotion/` — a working Remotion video project (the one exception that's an actual mini-app, not just config — same rule still applies: don't touch it unless asked)
