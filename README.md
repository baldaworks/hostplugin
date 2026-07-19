# HostPlugin

**Author portable plugins for coding-agent hosts.**

HostPlugin inspects a project or CLI, maps the requested behavior onto each host's native plugin components, previews every affected file, and writes only after explicit confirmation. It creates new standalone or embedded plugins and safely updates existing ones.

## Install

HostPlugin supports Codex, Claude Code, Grok Build, GitHub Copilot CLI, OpenCode, and Cursor.

### Codex

```sh
codex plugin marketplace add baldaworks/hostplugin
codex plugin add hostplugin@hostplugin
```

Invoke with `$hostplugin:author`.

### Claude Code

```sh
claude plugin marketplace add baldaworks/hostplugin
claude plugin install hostplugin@hostplugin --scope user
```

Invoke with `/hostplugin:author`.

### Grok Build

```sh
grok plugin install 'baldaworks/hostplugin#plugins/hostplugin' --trust
```

Invoke with `/hostplugin-author`.

### GitHub Copilot CLI

```sh
copilot plugin marketplace add baldaworks/hostplugin
copilot plugin install hostplugin@hostplugin
```

Invoke with `/hostplugin-author`.

### Cursor

```sh
agent plugin marketplace add https://github.com/baldaworks/hostplugin.git
```

Then install HostPlugin from the marketplace UI and invoke the `hostplugin-author` skill.

### OpenCode

From the project where you want to install HostPlugin, run:

```sh
hostplugin_source="$(mktemp -d)"
git clone --depth 1 https://github.com/baldaworks/hostplugin.git "$hostplugin_source"
mkdir -p .opencode
cp -R "$hostplugin_source"/integrations/opencode/{skills,references,commands} .opencode/
rm -rf "$hostplugin_source"
```

Invoke with `/hostplugin-author`. For a global installation, copy the same directories below `~/.config/opencode/` instead; keep the `skills/` and `references/` relative layout together.

## Use

Describe the plugin outcome in natural language:

```text
$hostplugin:author Inspect this repository and write a plugin for using its CLI on all supported hosts.
```

HostPlugin performs read-only repository and CLI discovery, asks only for missing product decisions, and presents:

1. a host-by-component capability report;
2. metadata, invocation names, prerequisites, and security effects;
3. the exact file manifest and concise diff;
4. validation commands and known limitations.

No files are written until you confirm that preview. Unsupported components are reported and block generation until you choose to remove the target, remove the component, or explicitly redesign it.

## Components

HostPlugin understands the current native component families of each target, including skills, commands, agents, hooks, MCP and LSP integrations, rules, Codex apps, Cursor subagents, and OpenCode JS/TS plugins. It does not pretend those component models are interchangeable.

Provider contracts are pinned under `plugins/hostplugin/references/` and include their review date and official sources. Installed host help and native validators take precedence when they reveal a newer contract.

## Development

Run the dependency-free contract suite:

```bash
python3 -m unittest discover -s tests -v
```

Then validate the canonical and prefixed skills, the Codex plugin, and available native host manifests. See `AGENTS.md` for the required completion checks.

## License

HostPlugin is available under the [MIT License](LICENSE).
