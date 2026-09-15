# HostPlugin

**Author and publish plugins for coding-agent hosts.**

HostPlugin inspects a project or CLI, maps the requested behavior onto each host's native plugin components, and previews the affected files. It creates standalone or embedded plugins, updates existing ones, and publishes them when requested.

## Install

HostPlugin supports Codex, Claude Code, Grok Build, GitHub Copilot CLI,
OpenCode v2 (2.x), and Cursor. It also supports the vendor-neutral Agent Plugins 1.0.0
portable package standard.

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

### OpenCode v2

Requires OpenCode 2.x (`opencode --version`). Install the host with
`@opencode/cli` following the [official installation guide](https://opencode.ai/v2/docs).

From the project where you want to install HostPlugin, run:

```sh
hostplugin_source="$(mktemp -d)"
git clone --depth 1 https://github.com/baldaworks/hostplugin.git "$hostplugin_source"
mkdir -p .opencode
cp -R "$hostplugin_source/integrations/opencode/." .opencode/
rm -rf "$hostplugin_source"
```

Invoke with `/hostplugin-author`. For a global installation, copy the same directories below `~/.config/opencode/` instead; keep the `skills/` and `references/` relative layout together.

HostPlugin provides skills, references, and a command wrapper for OpenCode.
Install these files using the copy commands above.

### Agent Plugins 1.0.0

The directory `plugins/hostplugin` is an Agent Plugins 1.0.0 package. A
compatible client can load that directory through its documented local-plugin or
installation workflow. The Agent Plugins standard itself does not define a
universal installation command, marketplace, registry, or invocation syntax.

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

Confirm the file preview before HostPlugin writes the proposed plugin. An explicit publication request authorizes the routine publication steps for the agreed destination and scope. Unsupported components are reported and require a decision to remove the target, remove the component, or explicitly redesign it.

### Create and publish an OpenCode v2 plugin

For example, invoke HostPlugin in OpenCode with:

```text
/hostplugin-author Create an OpenCode v2 plugin for this repository's CLI and publish it to our GitHub repository acme/opencode-plugin.
```

Replace `acme/opencode-plugin` with your destination. HostPlugin prepares the
native `package.json`, plugin entrypoint, and bundled resources; checks the
package contents; and follows the repository's release workflow. You can also
request publication to an npm registry. Git distribution does not require an npm
publication.

Users install the resulting plugins with OpenCode's native commands. These are
example package names and repositories to replace with your published destination:

```sh
opencode plugin add @acme/opencode-plugin@latest
opencode plugin add github:acme/opencode-plugin
opencode plugin add git+ssh://git@github.com/acme/opencode-plugin.git#main
opencode plugin add 'github:acme/plugins#main::path:packages/opencode-plugin'
```

Use a specific npm version or Git tag/commit for a fixed release. The last
example selects a package inside a repository. These commands install the native
plugins you create; to install the HostPlugin authoring skill itself, use the
[OpenCode instructions above](#opencode-v2).

See the [OpenCode packaging and publication reference](plugins/hostplugin/references/opencode.md)
for package checks and release steps, and the
[official OpenCode plugin guide](https://opencode.ai/v2/docs/plugins) for installation options.

## Components

HostPlugin understands the current native component families of each host,
including skills, commands, agents, hooks, MCP and LSP integrations, rules,
Codex apps, Cursor subagents, and OpenCode JS/TS plugins. It also understands the
Agent Plugins 1.0.0 portable core: Agent Skills and MCP servers in fixed package
locations. Other component families are not portable Agent Plugins components
and are never translated silently.

Provider and portable-standard contracts are pinned under
`plugins/hostplugin/references/` and include their review date and official
sources. Installed host help and native validators take precedence when they
reveal a newer contract.

## Development

Run the dependency-free contract suite:

```bash
python3 -m unittest discover -s tests -v
```

Then validate the canonical and prefixed skills, the Codex plugin, and available native host manifests. See `AGENTS.md` for the required completion checks.

## License

HostPlugin is available under the [MIT License](LICENSE).
