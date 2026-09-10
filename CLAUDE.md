## READ FIRST — this repo is a vendored toolbox, not an app

This is `maratfaiz/tools` — a personal collection of AI-agent skills/config (Higgsfield, ECC, Graphify, Headroom, Remotion, UI UX Pro Max). See `README.md` and `docs/*.md` for details, and `AGENTS.md` for the full rule.

**Short version: do not edit, refactor, or "clean up" anything in this repository** unless the user explicitly asked to change something in this tools repo specifically — including when this repo is only attached/visible as a submodule or subfolder while you work on a different project. Using the installed skills/agents normally is fine and expected; that's what they're for.

## graphify

This project has a knowledge graph at graphify-out/ with god nodes, community structure, and cross-file relationships.

Rules:
- For codebase questions, first run `graphify query "<question>"` when graphify-out/graph.json exists. Use `graphify path "<A>" "<B>"` for relationships and `graphify explain "<concept>"` for focused concepts. These return a scoped subgraph, usually much smaller than GRAPH_REPORT.md or raw grep output.
- If graphify-out/wiki/index.md exists, use it for broad navigation instead of raw source browsing.
- Read graphify-out/GRAPH_REPORT.md only for broad architecture review or when query/path/explain do not surface enough context.
- After modifying code, run `graphify update .` to keep the graph current (AST-only, no API cost).
