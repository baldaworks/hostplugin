---
name: hostplugin-author
description: Create, review, update, and publish coding-agent plugins for Codex, Claude Code, Grok Build, Copilot CLI, OpenCode v2, Cursor, and Agent Plugins 1.0.0. Use for plugin component design, packaging, host installation instructions, and authorized publication.
---

# HostPlugin Author

Create, update, or publish coding-agent plugins without inventing host capabilities,
portable-standard behavior, or CLI commands. Treat CLI integrations as the
primary workflow while supporting Agent Plugins packages, instruction-only,
MCP-backed, and host-specific plugins.

## Core rules

- Inspect before proposing and propose before writing.
- Keep discovery read-only. Run only documented `--help` and `--version` commands without additional approval.
- Never install dependencies, authenticate, publish, tag, release, or execute state-changing CLI commands as part of discovery.
- Never silently translate an unsupported component into a different component type.
- Preserve unrelated worktree changes, licenses, attribution, and existing component content.
- Require explicit confirmation after showing the exact file manifest and concise diff. Tool approval alone is not product confirmation.

## Load the references

Always read `../../references/capability-matrix.md` and `../../references/safety-and-preview.md`.
Then read the reference for every selected target:

- `../../references/codex.md`
- `../../references/claude.md`
- `../../references/grok.md`
- `../../references/copilot.md`
- `../../references/opencode.md`
- `../../references/cursor.md`
- `../../references/agent-plugins.md`

Treat those files as pinned guidance, not timeless truth. Prefer an installed host's read-only help and validator when available. If observed behavior conflicts with a reference, stop and report the conflict instead of guessing.

## Authoring workflow

### 1. Establish the operation

Determine whether the request creates, updates, audits, or publishes a plugin.
Carry existing user authorization forward; a request to publish includes the
necessary packaging and release preparation. Resolve:

- standalone marketplace repository or embedded `plugins/<name>` layout;
- targets, distinguishing the six host targets from Agent Plugins as a portable
  standard;
- plugin identity, version, description, publisher, repository, license, and intended invocation names;
- requested component inventory and whether any component is host-specific;
- output root and whether it already contains related files.

Ask only for product decisions that repository inspection cannot answer. For a new plugin, propose version `0.1.0`. For an existing plugin, preserve its version until the user confirms a SemVer change.

An explicit Agent Plugins request selects that standard. `All supported hosts`
continues to mean the six host targets. A generic portable-plugin request
selects all six hosts and also selects Agent Plugins when its component inventory
fits the portable core. If any requested component is unsupported by that core,
report only the Agent Plugins slice as unsupported and ask whether to omit the
standard, omit the component, keep it host-native, or explicitly design a
client extension. Agent Plugins defines no invocation namespace or CLI.

### 2. Ground in the repository

Read the applicable agent instructions, repository status, README, license, package manifests, release metadata, existing marketplaces, plugin manifests, and component directories. Identify dirty or untracked files before preparing edits.

For a CLI integration, derive and verify:

- executable name and supported installation methods;
- version and top-level help commands;
- relevant subcommands, flags, input/output streams, exit behavior, authentication, environment variables, and network requirements;
- which operations are read-only, mutating, destructive, or externally visible.

Do not infer commands from naming conventions. If the executable is unavailable, use checked-in documentation and mark unverified runtime details explicitly.

### 3. Build a capability report

Map every requested semantic component to every selected host or portable
standard. Report one of:

- `native`: the selected target has the same component type and the contract is verified;
- `host-specific`: the component is intentionally emitted only for named hosts
  or an explicitly approved client extension;
- `unsupported`: the selected target lacks the component or its contract cannot be verified.

For `unsupported`, stop and ask the user to drop the target, drop the component,
keep it in a selected host-native package, or explicitly redesign it. Never
translate unsupported behavior into an Agent Plugins client extension
automatically. An approved extension remains host-specific and non-portable.

### 4. Design the portable layout

Use canonical skill names in namespaced hosts and plugin-prefixed names in flat-name hosts. Keep behavior bodies equivalent while allowing frontmatter and invocation syntax to differ.

For shared semantics with incompatible wire formats, create host-specific directories and point each manifest at its own directory. Share files only when the selected hosts consume the exact same format and path semantics.

For targets that consume marketplaces, update only the selected repository
marketplaces. A standalone marketplace uses the repository root as marketplace
root and places plugins below `plugins/<name>`. For OpenCode-only work, use the
native package layout in its reference; do not add a marketplace.

For Agent Plugins 1.0.0, make the package directory the plugin root. Create the
required closed-schema `plugin.json`, place Agent Skills only at immediate
children of `skills/`, and create root `mcp.json` only when MCP servers are
requested. Keep both schema versions equal. Reject invalid names, unknown
manifest fields, package escapes, invalid transports or URLs, reserved
`PLUGIN_ROOT`/`PLUGIN_DATA` overrides, unsafe placeholders, and literal secrets
before writing. Do not create an installer, marketplace, registry, invocation,
or runtime contract because the standard defines none.

For OpenCode v2 package distribution, follow the packaging and publication
sections in `../../references/opencode.md`. Include the native `package.json`,
entrypoint, bundled resources, and consumer install command in the authored
plugin. Keep a skill-only package entrypoint limited to registering its bundled
instruction assets; do not add servers, hooks, tools, or unrelated behavior.

### 5. Present the preview

Before any write, present:

1. assumptions and unresolved verification markers;
2. the host-by-component capability report;
3. plugin metadata, invocation names, prerequisites, and permission/security effects;
4. the exact files to create, modify, preserve, or intentionally omit;
5. a concise content preview or diff, including version changes;
6. validation commands that will run after writing.

Request explicit confirmation for that preview. If the request changes materially after confirmation, show a revised preview and confirm again.

### 6. Write safely

Create only confirmed files. Refuse to overwrite unrelated files. When updating, preserve unknown supported manifest fields and merge marketplace entries by plugin name without reordering unrelated entries.

Keep secrets out of generated files. Use documented environment-variable placeholders for authentication. Avoid generated install hooks or arbitrary code execution unless the user requested them and the target host supports them natively.

### 7. Validate and report

Parse every JSON, YAML, TOML, and frontmatter file. Verify declared paths exist, names match directory conventions, component variants remain semantically aligned, and no placeholders remain.

Run available native validators for selected hosts and canonical schema plus
semantic validation for Agent Plugins. Treat an unavailable validator as a
reported limitation, not a success. Reinspect the final diff and report:

- created and updated files;
- native validation results and skipped checks;
- unsupported or intentionally omitted components;
- installation and invocation instructions;
- remaining manual verification.

### 8. Publish when requested

Do not publish, tag, push, create a release, or mutate a registry unless the user
has authorized that action. A clear publication request is that authorization;
do not ask for it again at each routine step.

Use the selected host reference to prepare the package and installation command.
Confirm the intended repository or registry from the request and existing
metadata; ask only if the destination or visibility is genuinely missing.
Review the exact artifact and version, run applicable checks, then perform the
authorized commit/push/tag or registry publication using the existing project
release workflow. Preserve existing releases and never overwrite a published
version to retry a failure.

Verify the published revision or registry version and return the real consumer
install command. If a check or publication fails, diagnose that failure and stop
before dependent publication steps; report what was actually published. Starting
a host server or making model calls is not required for package metadata or
publication documentation work; perform runtime testing only when requested.
