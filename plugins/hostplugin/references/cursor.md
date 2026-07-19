# Cursor plugin contract

Last reviewed: 2026-07-19.

Official references:

- https://cursor.com/docs/plugins
- https://cursor.com/docs/reference/plugins
- https://github.com/cursor/plugin-template

## Marketplace and manifest

Use `.cursor-plugin/marketplace.json` at the marketplace root and `.cursor-plugin/plugin.json` inside the plugin. Keep `displayName` and publisher identity in the plugin manifest through `displayName` and `author`. Put marketplace-only presentation fields such as `category` and `tags` on the marketplace entry, and keep manifest and marketplace versions synchronized.

Cursor plugins can bundle skills, agents, rules, hooks, MCP servers, and commands. Treat MCP Apps as an MCP-specific UI capability, not as a Codex `.app.json` equivalent.

Use prefixed skill names such as `<plugin>-<skill>` unless current Cursor documentation guarantees plugin namespacing for the installation path.

## Installation and validation

Current Cursor Agent CLI registers a Git marketplace with:

```text
agent plugin marketplace add <git-url>
```

Plugin selection may continue in Cursor's marketplace UI. The CLI accepts `--plugin-dir <path>` for isolated local loading; prefer that for smoke testing without modifying marketplace state.

Do not claim marketplace publication merely because a local manifest loads. Public Cursor Marketplace submission is a separate external action.
