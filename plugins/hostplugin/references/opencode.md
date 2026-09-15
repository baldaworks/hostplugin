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
- [npm pack](https://docs.npmjs.com/cli/v11/commands/npm-pack)
- [npm publish](https://docs.npmjs.com/cli/v11/commands/npm-publish)

## Distribution and discovery

The released executable is `opencode`; verify `opencode --version` and
`opencode --help`. The V2 npm CLI package is `@opencode/cli`.

For a requested native OpenCode plugin, author a package installable through
`opencode plugin add`. It accepts npm and Git package specifications, including
repository subdirectories. Use the packaging and publication workflow below.
HostPlugin itself is distributed as a native Git package. Its package entrypoint
registers the bundled instruction skill through the V2 skill API; the same
package contract applies to plugins authored with it.

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
and execution-risk preview. A package entrypoint that only registers bundled
instruction assets remains skill-only and must not add hooks, tools, servers, or
other behavior implicitly.

## Package an authored OpenCode plugin

Choose the package root from the requested repository layout. A standalone
repository can place `package.json` at its root; an embedded plugin can use a
subdirectory such as `packages/opencode-plugin/`. Keep all files needed by the
installed entrypoint inside that package root.

A native package needs:

- `package.json`: real package `name`, SemVer `version`, `type: "module"`,
  `exports` pointing to the shipped entrypoint, a `files` allowlist, license,
  repository metadata (including `directory` for an embedded package), and
  compatible dependencies such as `@opencode/plugin` when imported;
- a default-exported V2 plugin definition with a stable `id` and `setup(ctx)`;
- the requested components and all supporting files referenced at runtime.

A manifest alone does not implement components. When the requested plugin
bundles skills or commands, its entrypoint registers them through the matching
V2 API; read packaged content relative to the module location, not the consumer's
working directory. Preserve the intended skill instructions and command
arguments. Add `./tui` only for a requested terminal extension. Do not introduce
hooks, tools, or dependencies unrelated to the requested behavior.

Use the project's existing build/check commands when the package needs a build.
Inside the package root, inspect `npm pack --dry-run --ignore-scripts --json`:
verify the entrypoint, license and supporting files are included and credentials,
local configuration and unrelated files are excluded. For compiled output,
ensure the built files exist before inspecting the package; ignoring lifecycle
scripts does not build them. Use `npm pack --ignore-scripts` when an actual archive
is needed for inspection. Neither command publishes to a registry.

## Publish and provide installation instructions

Select Git distribution or npm registry publication from the user's request and
repository conventions. Git distribution does not require npm registry
publication. An explicit request to publish covers routine release preparation;
it does not grant access to a different repository or change package visibility.

### Git repository

1. Verify the configured remote, package subdirectory and intended release
   version. Review the diff and package contents before committing.
2. Use the repository's release workflow to commit and push the verified files
   and, when requested, create a new release tag. Do not replace existing tags.
3. Verify the remote revision contains the package and its entrypoint, then
   produce an install command using that actual repository and revision.

Documented forms (replace example owners, names, revisions and paths):

```sh
opencode plugin add github:acme/opencode-plugin
opencode plugin add git+ssh://git@github.com/acme/opencode-plugin.git#main
opencode plugin add 'github:acme/plugins#main::path:packages/opencode-plugin'
```

Use a release tag or full commit hash instead of `main` for a reproducible
release command. Quote specifications containing `#` and `::path:`. A private
Git target requires the consumer's existing Git credentials; never embed them
in the command. For a local development path, use the `plugins` configuration
array rather than passing the path to `plugin add`.

### npm registry

When npm publication is explicitly selected, verify the package name, registry,
access setting, version availability, and existing release automation. Use the
project's publish workflow; if none exists, run `npm publish` from the validated
package root with the intended registry/access options. Scoped public packages
need the appropriate public-access setting. Authentication or OTP must be
provided through the supported npm workflow, never written into package files.

Verify the published version in the selected registry, then give consumers:

```sh
opencode plugin add @acme/opencode-plugin@1.2.0
```

`@latest` is also supported for users who want the registry's moving dist-tag.
`opencode plugin add` installs the package and updates global OpenCode config;
it is a consumer installation command, not a publication command.

### Completion evidence

Report the package root, entrypoint, published Git revision or registry version,
checks performed, and exact install/invocation instructions. Distinguish package
validation from host execution. Do not start an OpenCode server or call a model
merely to write or validate package metadata and publication documentation.

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
plugin or skill validator: `opencode plugin check` checks package updates. For
HostPlugin itself, the repository contract imports the package entrypoint with
an isolated skill editor and verifies the packaged registration without
starting OpenCode.
`opencode debug config` lists configuration sources; it is not skill validation.
Do not invent `opencode plugin validate` or reuse V1 `debug skill` commands.

Runtime discovery remains a separate disposable-project smoke test. Inspect
current help and isolate configuration before starting a server: it may load
plugins, install packages, or connect MCP servers. Do not run a model merely to
validate static discovery without approval. Report static checks separately
from actual loading and invocation.
