---
name: author
description: Create, review, update, or publish coding-agent plugins across supported hosts and Agent Plugins. Use for component mapping, packaging, validation, installation guidance, and authorized publication.
---

# HostPlugin Author

Create, review, update, or publish coding-agent plugins without inventing host
capabilities, portable behavior, or CLI commands.

## Core rules

- Inspect before proposing and propose before writing.
- During discovery, run only documented `--help` and `--version` commands. Do not
  install, authenticate, publish, release, or run state-changing commands.
- Never silently translate an unsupported component into another component type.
- Preserve unrelated changes, licenses, attribution, and existing components.
- Before writing, show the exact file manifest and concise diff, then require
  explicit confirmation. Tool approval is not product confirmation.
- Do not publish, tag, push, create a release, or mutate a registry without user
  authorization for that destination and scope.

## References

Read only what the request needs:

- Read `../../references/capability-matrix.md` when selecting or comparing
  targets or mapping components.
- Read `../../references/safety-and-preview.md` before changing files or
  publishing.

Read the reference for every selected target:

- `../../references/codex.md`
- `../../references/claude.md`
- `../../references/grok.md`
- `../../references/copilot.md`
- `../../references/opencode.md`
- `../../references/cursor.md`
- `../../references/agent-plugins.md`

Treat references as pinned guidance, not timeless truth. Prefer installed host
help and native validators when available. If observed behavior conflicts with a
reference, stop and report the conflict.

## Workflow

### 1. Establish scope

Determine whether the request creates, updates, audits, or publishes a plugin.
Inspect applicable agent instructions, repository status, documentation,
licenses, manifests, release metadata, marketplaces, and component directories.
Resolve the output root, repository layout, targets, identity, version, component
inventory, invocation names, and host-specific behavior from existing evidence.
Ask only for product decisions that inspection cannot answer. Propose `0.1.0` for
a new plugin; preserve an existing version until a SemVer change is confirmed.

An explicit Agent Plugins 1.0.0 request selects that portable standard. `All
supported hosts` means the six host targets. A generic portable-plugin request
also selects Agent Plugins only when every requested component fits its portable
core. Otherwise report that slice as unsupported and ask whether to omit it, omit
the component, keep the component host-native, or design a named client extension.

### 2. Verify capabilities

For CLI integrations, verify the executable, documented installation methods,
help, relevant commands and flags, I/O, exit behavior, authentication, environment
variables, network use, and side effects. Do not infer commands from names. Mark
runtime details unverified when neither an installed CLI nor checked-in evidence
establishes them.

Build a capability report mapping every component to every selected host or portable
standard as `native`, `host-specific`, or `unsupported`. For unsupported behavior,
stop for an explicit product decision; never substitute another component type or
an Agent Plugins client extension automatically.

### 3. Design the layout

Follow each selected target reference. Use canonical skill names where the host
provides namespaces and plugin-prefixed names where discovery is flat. Keep their
behavior equivalent while allowing native frontmatter, paths, and invocation
syntax to differ. Share files only when formats and path semantics are identical.
Update only selected marketplaces and preserve unrelated entries.

For Agent Plugins, use its portable package contract and create no installation,
marketplace, invocation, or runtime behavior. For OpenCode, use its native package
contract; a skill-only entrypoint must register only its bundled instruction
assets.

### 4. Present the preview

Before writing, present assumptions, unresolved verification, the capability
report, metadata, invocation names, prerequisites, security effects, exact
create/modify/preserve/omit files, a concise diff or content preview, version
changes, and validation commands. Request explicit confirmation. Re-preview only
when the scope, mapping, permissions, or affected files change materially.

### 5. Implement and validate

Create only confirmed files. Preserve unknown supported fields and merge
marketplace entries by plugin name. Keep secrets out of generated files and use
documented environment placeholders.

Parse structured files and frontmatter; verify paths, names, variant parity, and
placeholders. Run repository checks, selected native host validators, and Agent
Plugins schema plus semantic validation when applicable. Report unavailable
validators as limitations. Reinspect the diff and report changed files, omitted
components, validation evidence, installation and invocation instructions, and
remaining manual checks.

### 6. Publish when requested

A clear publication request authorizes routine preparation and publication to the
specified destination; do not ask again at each step. Verify the destination,
visibility, artifact, and version, then use the existing release workflow. Never
overwrite a published version. Stop dependent steps after a failure and report
what actually changed. Return the verified revision or registry version and the
real consumer installation command.
