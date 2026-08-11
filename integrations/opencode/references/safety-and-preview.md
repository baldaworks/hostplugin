# Safety and preview contract

## Discovery boundary

Treat file reads, repository status, manifest parsing, and documented `--help`/`--version` calls as discovery. Do not run setup, install, login, update, publish, release, migration, destructive, or domain-specific commands without separate approval.

If `--help` or `--version` is not demonstrably supported, do not execute the binary. Read documentation instead.

## CLI safety inventory

For each command exposed through the authored plugin, record:

- executable and exact argument form;
- prerequisites and installation source;
- stdin, stdout, stderr, and exit-status behavior;
- filesystem, network, registry, cloud, or human communication effects;
- authentication and environment variables without secret values;
- whether confirmation is required before the skill invokes it.

Classify operations as read-only, local write, destructive, or externally visible. Require explicit confirmation for destructive or externally visible operations even if the host tool would otherwise auto-approve them.

## Required preview

Show all of the following before writing:

- target root and create/update mode;
- metadata and proposed version;
- selected host and portable-standard targets with their capability report;
- complete create/modify/preserve/omit file list;
- concise diff or representative full contents for new files;
- required permissions, credentials, network access, and external side effects;
- exact validation commands and known unavailable validators.

For Agent Plugins, separate portable-core capabilities from client extensions.
Label every approved extension host-specific and non-portable, and never imply
that the standard defines installation, distribution, invocation, or a runtime.

Ask the user to confirm the preview. A generic request to author a plugin is not confirmation of an unseen implementation.

## Update discipline

- Inspect `git status` and the current file bytes before editing.
- Preserve unrelated changes and unknown supported manifest keys.
- Merge marketplace entries by name; never replace the entire catalog to update one plugin.
- Do not overwrite files with a different owner or purpose.
- Do not bump a version, tag, publish, push, or open a pull request without explicit authorization for that action.
- Re-preview when scope, component mapping, permissions, or affected files change.

## Final report

Report verified facts separately from assumptions and skipped validation. Never claim that a host loaded or invoked the plugin when only static files were checked.
