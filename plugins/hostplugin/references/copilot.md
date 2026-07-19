# GitHub Copilot CLI plugin contract

Last reviewed: 2026-07-19.

Official reference: https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference

## Marketplace and manifest

Use `.github/plugin/marketplace.json` at the marketplace root. Copilot also probes other compatible marketplace locations, but emit the native GitHub path for a portable repository.

Place the portable manifest at `.plugin/plugin.json` in the plugin directory. Current Copilot CLI also recognizes root and GitHub/Claude-compatible manifest locations; do not depend on fallback order when an explicit `.plugin` manifest is available.

## Native components

Copilot plugins may provide agents, skills, commands, hooks, MCP servers, LSP servers, and extensions. Follow the official field types: several path fields accept a string or string array, while hooks and server fields may accept inline objects.

Use prefixed skill names such as `<plugin>-<skill>` because skills use flat name-based precedence. Project and personal components can shadow plugin components.

## Installation and validation

Install from a registered marketplace as `<plugin>@<marketplace>`, or directly from `owner/repo:path` while developing. Copilot CLI does not currently expose a dedicated `plugin validate` command; perform contract tests and a disposable local installation instead.

Do not claim successful Copilot loading until `copilot plugin list` and an invocation confirm the installed component.
