# Codex plugin contract

Last reviewed: 2026-07-19. Validate generated plugins with the current Codex plugin validator before handoff.

Official overview: https://help.openai.com/en/articles/20001256/

## Marketplace

Use `.agents/plugins/marketplace.json` at the marketplace root. Include:

- top-level `name`, optional `interface.displayName`, and ordered `plugins`;
- plugin `name` matching its folder and manifest name;
- local source object `{ "source": "local", "path": "./plugins/<name>" }`;
- explicit `policy.installation`, `policy.authentication`, and `category`.

Do not add `policy.products` unless the user explicitly requests product gating.

## Plugin

Place the manifest at `plugins/<name>/.codex-plugin/plugin.json`. Use relative paths beginning with `./`. A skill-only plugin declares `skills: "./skills/"`.

The current contract supports skills, MCP server configuration, Codex apps, and UI metadata. Do not add hooks, agents, LSP servers, or other unrecognized fields merely because another host supports them.

Keep `apps` out unless `.app.json` exists. Keep `mcpServers` out unless a real companion config or inline server map exists.

## Skills and invocation

Store canonical skills under `skills/<skill>/SKILL.md`. Match the directory and frontmatter names. Codex invokes an installed skill as `$<plugin>:<skill>`.

Generate `agents/openai.yaml` for Codex UI metadata. Quote strings and make `interface.default_prompt` explicitly mention `$<plugin>:<skill>`.

## Installation and validation

For a GitHub marketplace:

```text
codex plugin marketplace add <owner>/<repo>
codex plugin add <plugin>@<marketplace>
```

Validate the manifest with the current plugin-creator validator. Treat successful JSON parsing alone as insufficient.
