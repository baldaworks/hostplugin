# Codex plugin contract

Last reviewed: 2026-07-19.

Official references:

- https://learn.chatgpt.com/docs/build-plugins
- https://learn.chatgpt.com/docs/hooks

## Marketplace

Use `.agents/plugins/marketplace.json` at the marketplace root. Include:

- top-level `name`, optional `interface.displayName`, and ordered `plugins`;
- plugin `name` matching its folder and manifest name;
- local source object `{ "source": "local", "path": "./plugins/<name>" }`;
- explicit `policy.installation`, `policy.authentication`, and `category`.

Do not add `policy.products` unless the user explicitly requests product gating.

## Plugin

Place the manifest at `plugins/<name>/.codex-plugin/plugin.json`. Use relative paths beginning with `./`. A skill-only plugin declares `skills: "./skills/"`.

The current contract supports skills, lifecycle hooks, MCP server configuration, Codex apps, and UI metadata. Do not add commands, agents, LSP servers, or other unrecognized fields merely because another host supports them.

Keep `apps` out unless `.app.json` exists. Keep `mcpServers` out unless a real companion config or inline server map exists.

## Hooks

Use `hooks/hooks.json` for default discovery without a manifest field. When custom routing is needed, `hooks` may be a relative path, an array of paths, an inline hooks object, or an array of inline objects.

Treat hooks as executable, trust-gated components. Installing or enabling a plugin does not automatically trust its hooks; require the user to review the current definition. Use `${PLUGIN_ROOT}` and `${PLUGIN_DATA}` for plugin-relative and writable data paths.

## Skills and invocation

Store canonical skills under `skills/<skill>/SKILL.md`. Match the directory and frontmatter names. Codex invokes an installed skill as `$<plugin>:<skill>`.

Generate `agents/openai.yaml` for Codex UI metadata. Quote strings and make `interface.default_prompt` explicitly mention `$<plugin>:<skill>`.

## Installation and validation

For a GitHub marketplace:

```text
codex plugin marketplace add <owner>/<repo>
codex plugin add <plugin>@<marketplace>
```

Validate the manifest with the current plugin-creator validator and installed Codex help. Treat successful JSON parsing alone as insufficient.

If an installed validator rejects a hooks field that the current official contract documents, report a validator-version conflict and partial native validation. Verify the hook JSON, paths, events, commands, and trust effects against the official hook contract; do not misclassify the component as unsupported.
