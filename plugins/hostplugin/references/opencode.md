# OpenCode v2 extension contract

Last reviewed: 2026-09-15. Target: OpenCode 2.x; installed CLI checked: v2.0.3.
V1 is no longer the HostPlugin authoring target.

## Official references

- [Installation](https://opencode.ai/v2/docs)
- [V1 migration](https://opencode.ai/v2/docs/migrate-v1)
- [Configuration](https://opencode.ai/v2/docs/config)
- [Skills](https://opencode.ai/v2/docs/skills)
- [Commands](https://opencode.ai/v2/docs/commands)
- [Agents](https://opencode.ai/v2/docs/agents)
- [Permissions](https://opencode.ai/v2/docs/permissions/)
- [MCP servers](https://opencode.ai/v2/docs/mcp-servers/)
- [Plugin distribution](https://opencode.ai/v2/docs/plugins)
- [Plugin API](https://opencode.ai/v2/docs/build/plugins/)
- [Plugin migration](https://opencode.ai/v2/docs/build/plugins/migrate-v1)
- [CLI plugins](https://opencode.ai/v2/docs/build/plugins/cli/)
- [Instructions](https://opencode.ai/v2/docs/instructions)
- [Themes](https://opencode.ai/v2/docs/themes)

## Distribution and discovery

The released executable is `opencode`; verify `opencode --version` and
`opencode --help`. The V2 npm CLI package is `@opencode/cli`. HostPlugin ships
skills, references, and a Markdown command wrapper through the manual copy in
the README. Keep that distribution skill-only; `opencode plugin add` installs
executable package plugins and is not an installer for this bundle.

Use `.opencode/skills/<id>/SKILL.md`, `.opencode/commands/<name>.md`, and
`.opencode/agents/<name>.md`; global equivalents live under
`~/.config/opencode/`. Keep supporting references at their declared relative
paths. Existing HostPlugin files and `/hostplugin-author` remain compatible.

## Native configuration

Use `opencode.json(c)` and the documented schema
`https://opencode.ai/config.json`. Author native V2 fields:

| Component | V2 shape |
| --- | --- |
| Skills | `skills: ["./skills", "https://example.com/skills/"]` |
| Commands | `commands.<id>` with `template`; Markdown body supplies the template |
| Agents | `agents.<id>` with `system`; Markdown body supplies the system prompt |
| Permissions | Ordered `permissions` array of `action`, `resource`, `effect` |
| MCP | `mcp.servers.<id>` with `type`, command or URL, and optional `disabled` |
| Executable plugins | `plugins` array of strings or `{ "package": "...", "options": {} }` |

Agents use `disabled`, `request.body`, and `provider/model#variant` when needed.
Commands use `subagent` for background delegation; preserve `$ARGUMENTS` in
prompt templates. Skill source paths are relative to the active working
directory; plugin paths are relative to the declaring config file.

Permission rules use the last match. Use `shell`, `subagent`, and `edit` for V2
actions; do not emit V1 `bash`, `task`, or `permission` shapes for new work.
MCP `disabled: true` prevents connection; preserve environment placeholders
such as `{env:NAME}` and review connection/process effects before enabling.

Supported V1 config is normalized in memory. Preserve unrelated settings and
do not mechanically mix V1 and V2 fields within one agent, command, provider,
or model entry. Do not rewrite users' installations as part of authoring.

## Skill identity and invocation

V2 derives skill IDs from paths; frontmatter `name` is a display label.
HostPlugin keeps lowercase hyphen-case IDs, matching names, and descriptions
of 1–1024 characters for portability, not because V2 enforces those limits.
Within OpenCode, the `skill` tool loads a skill by its path-derived ID:
`{ "id": "<skill-id>" }`. Use the authored skill's ID in OpenCode-specific examples.
V2 also exposes skills in interactive command catalogs; retain the existing
Markdown wrapper and its invocation. `metadata.opencode/slash` can override
`slash`; `metadata.opencode/autoinvoke: false` hides model advertising without
preventing explicit loading. Avoid changing these flags during a routine port.

## Executable plugin API

For explicitly requested executable components, use the V2 `@opencode/plugin`
API: default-export `Plugin.define({ id, setup(ctx) { ... } })`. Register hooks,
transforms, tools, and subscriptions through the context; V1 returned hook
objects and `@opencode-ai/plugin` implementations do not run in V2. Port each
hook and tool against its documented domain API; renaming config is insufficient.

Use `.opencode/plugins/` for local modules or immediate package directories.
Pin compatible package dependencies and validate the packaged entrypoint.
CLI plugins use `@opencode/plugin/tui` and a `./tui` package export; CLI-only
packages belong in global `cli.json`. Keep server and terminal contracts distinct.
An executable plugin requires an explicit component request, dependency review,
and execution-risk preview. HostPlugin itself gains no JS/TS runtime package.

## Unsupported and host-specific capabilities

- **LSP: unsupported.** V2 preserves `lsp` config but does not run language
  servers, expose LSP tools, or produce their diagnostics. Report this loss;
  require an explicit decision before replacing LSP with lint/compiler commands.
- **Instructions:** use `AGENTS.md`. V2 has no `CLAUDE.md` fallback and accepts
  the `instructions` array without loading its entries. Schema acceptance is
  not evidence of working instruction discovery.
- **Themes: host-specific.** V2 theme JSON uses `version: 2` with `light` and/or
  `dark` under `.opencode/themes/` or `~/.config/opencode/themes/`. Select themes
  in global `~/.config/opencode/cli.json`, not server config. Do not imply support
  for unrelated monitor or output-style components.

## Validation

Parse frontmatter/config, check reference paths and skill-copy parity, and run
repository contract tests. Installed v2.0.3 help exposes no dedicated static
plugin or skill validator: `opencode plugin check` checks package updates.
`opencode debug config` lists configuration sources; it is not skill validation.
Do not invent `opencode plugin validate` or reuse V1 `debug skill` commands.

Runtime discovery remains a separate disposable-project smoke test. Inspect
current help and isolate configuration before starting a server: it may load
plugins, install packages, or connect MCP servers. Do not run a model merely to
validate static discovery without approval. Report static checks separately
from actual loading and invocation.
