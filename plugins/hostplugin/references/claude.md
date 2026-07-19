# Claude Code plugin contract

Last reviewed: 2026-07-19.

Official references:

- https://code.claude.com/docs/en/plugins
- https://code.claude.com/docs/en/plugins-reference
- https://code.claude.com/docs/en/plugin-marketplaces

## Marketplace and manifest

Use `.claude-plugin/marketplace.json` at the marketplace root and `.claude-plugin/plugin.json` inside the plugin directory. Keep components at the plugin root, not inside `.claude-plugin/`.

Use explicit SemVer only when updates will bump it; Claude caches versioned plugins. For this authoring workflow, propose the version and require confirmation before changing it.

## Native components

Claude plugins may provide skills, legacy commands, agents, hooks, MCP servers, LSP servers, monitors, output styles, themes, executables in `bin/`, and supported default settings. Use only fields and paths documented by the current plugin reference.

Prefer `skills/<name>/SKILL.md` over new legacy command-only implementations. Plugin skills are invoked as `/<plugin>:<skill>`.

Use `${CLAUDE_PLUGIN_ROOT}` for paths from hooks, MCP, or scripts. Never reference files outside the plugin directory because installation copies the plugin into a cache.

## Validation

Run:

```text
claude plugin validate <marketplace-or-plugin-path>
```

Then test installation from a local marketplace in an isolated configuration when practical. Validation does not prove external tools, credentials, or hooks work.
