---
name: hostplugin-author
description: Author, audit, or update portable plugins for Codex, Claude Code, Grok Build, GitHub Copilot CLI, OpenCode, and Cursor. Use when an agent must inspect a project or CLI, design host-native skills, commands, agents, hooks, MCP/LSP integrations, rules, or apps, scaffold either a standalone marketplace or an embedded plugin, and preview every file before writing.
---

# HostPlugin Author

Create or update coding-agent plugins without inventing host capabilities or CLI commands. Treat CLI integrations as the primary workflow while supporting instruction-only, MCP-backed, and host-specific plugins.

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

Treat those files as pinned guidance, not timeless truth. Prefer an installed host's read-only help and validator when available. If observed behavior conflicts with a reference, stop and report the conflict instead of guessing.

## Authoring workflow

### 1. Establish the operation

Determine whether the request creates a new plugin, updates an existing plugin, or audits one before an update. Resolve:

- standalone marketplace repository or embedded `plugins/<name>` layout;
- target hosts, defaulting to all six only when the user asks for a portable plugin;
- plugin identity, version, description, publisher, repository, license, and intended invocation names;
- requested component inventory and whether any component is host-specific;
- output root and whether it already contains related files.

Ask only for product decisions that repository inspection cannot answer. For a new plugin, propose version `0.1.0`. For an existing plugin, preserve its version until the user confirms a SemVer change.

### 2. Ground in the repository

Read the applicable agent instructions, repository status, README, license, package manifests, release metadata, existing marketplaces, plugin manifests, and component directories. Identify dirty or untracked files before preparing edits.

For a CLI integration, derive and verify:

- executable name and supported installation methods;
- version and top-level help commands;
- relevant subcommands, flags, input/output streams, exit behavior, authentication, environment variables, and network requirements;
- which operations are read-only, mutating, destructive, or externally visible.

Do not infer commands from naming conventions. If the executable is unavailable, use checked-in documentation and mark unverified runtime details explicitly.

### 3. Build a capability report

Map every requested semantic component to every selected host. Report one of:

- `native`: the host has the same component type and the contract is verified;
- `host-specific`: the component is intentionally emitted only for named hosts;
- `unsupported`: the host lacks the component or its contract cannot be verified.

For `unsupported`, stop and ask the user to drop the host, drop the component, or explicitly redesign it as a different component. Do not choose an adaptation automatically.

### 4. Design the portable layout

Use canonical skill names in namespaced hosts and plugin-prefixed names in flat-name hosts. Keep behavior bodies equivalent while allowing frontmatter and invocation syntax to differ.

For shared semantics with incompatible wire formats, create host-specific directories and point each manifest at its own directory. Share files only when the selected hosts consume the exact same format and path semantics.

For an embedded plugin, update only the selected repository marketplaces. For a standalone plugin, make the repository root the marketplace root and place the plugin below `plugins/<name>`.

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

Run available native validators for selected hosts. Treat an unavailable validator as a reported limitation, not a success. Reinspect the final diff and report:

- created and updated files;
- native validation results and skipped checks;
- unsupported or intentionally omitted components;
- installation and invocation instructions;
- remaining manual verification.

Do not publish, tag, push, create a release, or mutate a registry unless the user separately authorizes that action.
