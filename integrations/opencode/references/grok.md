# Grok Build plugin contract

Last reviewed: 2026-07-19.

Official references:

- https://docs.x.ai/build/features/skills-plugins-marketplaces
- https://docs.x.ai/build/cli/reference

## Marketplace and plugin

Use `.grok-plugin/marketplace.json` at the marketplace root and `.grok-plugin/plugin.json` inside the plugin. Grok also reads Claude-compatible plugin content, but do not assume every new Claude-specific primitive has identical Grok behavior.

Grok natively discovers plugin skills, agents, hooks, MCP servers, and LSP servers. Put user-invocable skill variants under a prefixed directory such as `prefixed-skills/<plugin>-<skill>` so flat slash-command names remain unambiguous.

## Invocation and inspection

User-invocable skills appear as slash commands. Use `/<plugin>-<skill>` for the prefixed variant unless installed help reports a qualified namespace.

Use `grok inspect` only when the user authorizes host discovery beyond the basic plugin validator; it inspects the current project configuration and may reveal environment-specific state.

## Validation

Run:

```text
grok plugin validate <plugin-path>
```

Use `grok plugin details` or installation tests only in isolated state and with approval. Report Claude-compatibility assumptions explicitly.
