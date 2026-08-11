# Agent Plugins 1.0.0 reference

Last reviewed: 2026-08-11.

Agent Plugins is a vendor-neutral portable package standard, not an agent host,
CLI, marketplace, or runtime. Version 1.0.0 is currently a Working Draft. Pin
generated packages to its canonical schema identifiers and re-check the official
specification before changing this reference.

Official sources:

- https://agent-plugins.org/specification
- https://agent-plugins.org/plugin-authors/manifest
- https://agent-plugins.org/plugin-authors/skills
- https://agent-plugins.org/plugin-authors/mcp-servers
- https://agent-plugins.org/plugin-authors/client-extensions
- https://agent-plugins.org/schemas/1.0.0/plugin.schema.json
- https://agent-plugins.org/schemas/1.0.0/mcp.schema.json

## Portable package boundary

An Agent Plugin is a directory with one required `plugin.json` at its root.
Portable components use fixed locations:

```text
my-plugin/
├── plugin.json
├── skills/
│   └── summarize/
│       └── SKILL.md
└── mcp.json
```

All package-supplied paths must resolve within the plugin root. Do not use
symlinks or equivalent mechanisms to escape it. Distribution, installation,
enablement, updates, invocation UX, and marketplaces are client-managed and are
not portable Agent Plugins behavior. Do not invent commands for them.

## Manifest

`plugin.json` uses this required schema identifier:

```json
{
  "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
  "name": "example-plugin"
}
```

The schema is closed. The only portable top-level fields are `$schema`, `name`,
`version`, `description`, `author`, `homepage`, `repository`, `license`,
`keywords`, and `extensions`. `$schema` and `name` are required. Plugin names
are 1–64 characters, use lowercase ASCII letters, digits, hyphens, and periods,
start and end with an alphanumeric character, and contain neither `--` nor `..`.
An unknown top-level field is reported and ignored by conformant clients, but it
is still a schema violation and HostPlugin must reject it before writing.

## Skills

Skills follow the Agent Skills specification. A client discovers only immediate
children of root `skills/` whose exact `SKILL.md` path is a regular file. It does
not recursively discover deeper skills. Missing `skills/` is valid. One invalid
skill is skipped and reported without invalidating other skills or component
types.

## MCP servers

Root `mcp.json` is optional. When present, its schema version must match
`plugin.json`:

```json
{
  "$schema": "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json",
  "mcpServers": {}
}
```

The document is closed and supports these explicit transports:

- `stdio`: requires `type` and one executable-token `command`; optional `args`,
  `env`, and `cwd`;
- `streamable-http`: requires `type` and `url`; optional literal `headers`;
- `sse`: deprecated HTTP+SSE; client support is optional.

A `stdio` command is either a bare executable resolved by the platform or a
plugin-relative path beginning with `./`; it is never a shell command and is not
placeholder-expanded. The default working directory is the plugin root. An
explicit `cwd` must begin with `./`, `${PLUGIN_ROOT}`, or `${PLUGIN_DATA}` and
remain inside that root after resolution.

Clients provide reserved `PLUGIN_ROOT` and `PLUGIN_DATA` variables. Expand only
those exact placeholders, once and non-recursively, in `args`, `env` values, and
`cwd`. Do not expand them in `command`, environment keys, URLs, or headers. A
server must not override either reserved variable.

Remote URLs must be absolute HTTP or HTTPS URLs without user information or
fragments. Non-loopback endpoints must use HTTPS. Headers and environment values
are visible package data: never embed credentials or secrets. Agent Plugins
1.0.0 defines no portable OAuth or credential-reference field; authentication is
client-managed.

An invalid top-level `mcp.json` disables MCP for the plugin. An invalid,
unsupported, or unavailable server disables only that entry. Do not let an MCP
failure invalidate independent skills or client extensions.

## Client extensions

Client extensions are explicitly non-portable. They use a reverse-domain
namespace, such as `com.example.client`, under the manifest's `extensions`
object and/or as a matching top-level directory. The namespace owner defines its
format and behavior.

Never translate an unsupported command, agent, hook, LSP server, rule, app,
executable, or other host-native component into a client extension silently.
Stop and ask the user to drop the Agent Plugins target, drop the component, keep
it in a selected host-native package, or explicitly approve a named extension
design. Report an approved extension as host-specific and non-portable.

## Validation

Validate `plugin.json` and optional `mcp.json` against their canonical schemas,
then perform the semantic checks that JSON Schema cannot express: package path
containment, matching schema versions, URL rules, secret safety, placeholder
behavior, and skill validity. A schema download used by an authoring tool does
not imply that a client fetches schemas while loading a plugin. Static validation
does not prove that any client loaded or invoked the package.
