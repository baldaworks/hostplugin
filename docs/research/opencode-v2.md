# OpenCode v2 support migration

## Summary

HostPlugin can move its OpenCode target to 2.x while preserving the shipped
skill, Markdown command, reference layout, and `/hostplugin-author` invocation.
The material work is updating the authoring contract: executable plugins have
a new API, native configuration uses revised fields, and capability reporting
must reflect features that V2 does not implement. OpenCode's migration guide
explicitly preserves supported file-based definitions while identifying plugin,
server API, and terminal configuration changes.[^1]

The official V2 installation documentation identifies `@opencode/cli` as the
npm package and `opencode` as the executable. Local evidence on 2026-09-15
identifies the installed host as `opencode v2.0.3`. This provides a concrete
review baseline without asserting that this patch version will remain the
latest release.[^2]

HostPlugin 0.2.0 adopts the reviewed OpenCode v2 contract. Plugin and
marketplace versions are synchronized; the license and skill bodies remain
intact. The repository review baseline was HostPlugin 0.1.1.

## Support boundaries

| Component | V2 capability | HostPlugin consequence |
| --- | --- | --- |
| Skills | Native, identified by file path | Keep `hostplugin-author` and supporting references |
| Prompt commands | Native Markdown or `commands` config | Keep the wrapper and `$ARGUMENTS` |
| Agents | Native Markdown or `agents` config | Describe V2 fields for future authoring |
| Hooks and executable tools | Native V2 plugin API | Require explicit executable-component scope |
| MCP | Native `mcp.servers` config | Document connection and process effects |
| LSP | No runtime, despite accepted config | Report unsupported; require a decision on alternatives |
| Project instructions | `AGENTS.md` discovery | Do not promise `instructions` array loading |
| Themes | Terminal-specific V2 format | Mark host-specific; do not generalize to output styles |

This is a semantic capability report. A parseable file does not establish that
the host implements its behavior. In particular, accepting an LSP definition
cannot justify a claim that an agent receives language-server diagnostics.[^1]

## Skill and command distribution

V2 finds skills under project `.opencode/skills/` and global
`~/.config/opencode/skills/`, including compatibility sources under `.claude`
and `.agents`. IDs come from paths; `name` is a display label. The native loader
does not enforce the old reference's name-match and description-length rules.
HostPlugin should retain those restrictions as its own portability policy.[^3]

The existing directory layout keeps the skill's `../../references/` links
resolvable after installation. Moving only `SKILL.md` would break that local
contract. Both canonical and copied reference sets therefore change together,
while the canonical and prefixed skill bodies remain equivalent.

V2 supports Markdown command bodies as prompt templates, with `$ARGUMENTS`
carrying the supplied argument string. Global and project `commands/`
directories remain valid. The wrapper can continue loading `hostplugin-author`
without introducing new permissions, model selection, or delegated execution.
New command configuration should use `commands` and `subagent`; the latter
requests a background child session.[^4]

V2 also lists skills in interactive command catalogs. Retaining the wrapper
minimizes this migration's scope. Actual catalog selection and full invocation
are runtime verification items; static parity checks alone cannot prove them.

## Authoring configuration

New agent JSON belongs under `agents`; its instruction string is `system`.
Markdown agent bodies supply that content directly. Use `disabled`, a model
reference with any `#variant`, and `request.body` for applicable request settings.
Agent mode must be intentional: V2 distinguishes primary, subagent, and combined
profiles, and child agents use their own configured permissions.[^5]

V2 permission rules form an ordered array. Every rule identifies an action,
resource, and effect; the last matching rule determines the result. Use `shell`,
`subagent`, and `edit` rather than treating V1 tool names as current permission
actions. Preserve ordering during edits because rearranging rules can change
which operations are allowed.[^6]

MCP server entries belong under `mcp.servers`. A local server specifies its
command array; a remote server specifies its URL. `disabled: true` prevents a
connection. Environment substitution uses `{env:NAME}`. Enabling a server is
operational work: local servers start processes and remote servers establish
connections, potentially requiring authentication.[^7]

The source of a relative path also matters. Plugin paths are resolved against
the declaring config file, whereas extra skill paths use the active working
directory. A common path-rewriting helper would therefore be inappropriate for
both settings.[^3][^8]

Existing supported V1 configuration can remain in place. A targeted migration
should preserve unrelated fields and avoid mixing incompatible formats within
one nested definition. Updating this repository's reference is not a reason to
rewrite a developer's global OpenCode configuration.[^1]

## Executable plugins

V2 executable packages have their own installation and discovery model.
`opencode plugin add` manages package plugins; local modules and package
directories can be discovered beneath `.opencode/plugins/`. Config entries use
`plugins`, optionally with `package` and `options`. The command is unsuitable
for installing HostPlugin's current collection of instruction files.[^8]

Executable authoring requires a real port. Replace the V1 plugin function and
returned hook object with a default-exported definition containing an ID and
`setup(ctx)`, normally through `Plugin.define` from `@opencode/plugin`.
Register behavior through the relevant context domains. Plugin IDs also scope
storage, so an arbitrary ID rename is a state migration, not a cosmetic edit.[^9]

Hooks, transforms, subscriptions, and custom tools need separate API review.
Use the current plugin reference to check each domain and package entrypoint.
Dependencies must match the targeted OpenCode release, and testing should cover
the packaged artifact rather than only a linked development copy. A dual V1/V2
entrypoint is possible, but retaining a V1 implementation would introduce an
additional compatibility obligation outside this migration.[^10]

Terminal extensions are a distinct contract. They import
`@opencode/plugin/tui`; packages can expose `./tui`, and CLI-only packages are
configured through global `cli.json`. Terminal UI capabilities should not be
implemented by guessing server-plugin hooks.[^11]

HostPlugin itself remains skill-only. This migration adds neither a runtime
package nor code-generation scripts. Guidance about executable plugins exists
for explicitly requested future authoring tasks.

## Removed and qualified claims

LSP is unsupported in the V2 runtime. A workflow that requires language-server
functionality needs an explicit product decision: omit OpenCode for that
component, omit the component, or approve an alternative implementation.
HostPlugin must not silently substitute lint or compiler commands.[^1]

The instruction guide and configuration guide agree that `instructions` is
accepted but its file, glob, and URL entries are not loaded. Use `AGENTS.md` for
active guidance. V2 does not provide a `CLAUDE.md` fallback. These detailed
limitations qualify the migration guide's broader compatibility language and
should be reflected in the capability report.[^12][^13]

Themes are supported as a terminal-specific component. Theme files use
`version: 2` and at least a light or dark definition; selection belongs in
`cli.json`. This does not establish equivalent support for monitors or output
styles grouped into the same matrix row.[^14]

## Validation and confidence

The contract suite checks all existing repository contracts plus V2
source pinning, the revised capability column, and preservation of the command
wrapper. Existing tests compare the copied skill and every reference with its
source. Skill validation covers the canonical skill, the prefixed skill, and
the OpenCode integration copy. Codex plugin validation and the installed
Claude Code and Grok native validators cover their respective manifests.

Installed OpenCode v2.0.3 help exposes `debug agents`, `debug config`, and
`debug paths`. Its plugin commands are list, add, check, update, and remove.
There is no dedicated static skill/plugin validator in that inspected command
surface. The documentation describes `plugin check` as an update check; it is
not a substitute for validation.[^8]

The installed Codex, Copilot, and Cursor plugin help likewise provides no
dedicated native validation command. Codex is covered by the installed
plugin-creator validator. Copilot and Cursor receive repository static checks;
no installation or authenticated session is necessary for this patch.

Runtime skill loading, slash catalog behavior, and model invocation remain
unverified. A future smoke test should use a disposable project with isolated
configuration and inspect the registered `hostplugin-author` skill and command
before exercising the workflow. Ordinary server startup can load executable
plugins, resolve packages, or connect configured MCP servers, so starting a
user's configured host is not an inert validation operation.[^7][^8]

## Change inventory

Modify `README.md`, `tests/test_contract.py`, and the `opencode.md` and
`capability-matrix.md` references in both `plugins/hostplugin/references/` and
`integrations/opencode/references/`. Add this report at
`docs/research/opencode-v2.md`. Synchronize the six plugin manifests, four
versioned marketplaces, and test version constant at 0.2.0. Preserve all other
tracked content.

Release validation covers the repository contracts, three skill validations,
Codex plugin validation, and available native manifest validators. The remaining
runtime limitation must be reported alongside those results rather than
represented as a successful OpenCode load.

## Sources

All web sources below are published by OpenCode, have no publication date
shown on the reviewed page, and were reviewed on 2026-09-15. Local CLI evidence
is the installed `opencode --version`, top-level/debug/plugin help, and other
installed hosts' plugin help inspected on that date. Repository observations
refer to the pre-migration HostPlugin 0.1.1 manifests, integration, and tests.

[^1]: OpenCode. [Migrate from V1](https://opencode.ai/v2/docs/migrate-v1).
[^2]: OpenCode. [Intro and installation](https://opencode.ai/v2/docs).
[^3]: OpenCode. [Skills](https://opencode.ai/v2/docs/skills).
[^4]: OpenCode. [Commands](https://opencode.ai/v2/docs/commands).
[^5]: OpenCode. [Agents](https://opencode.ai/v2/docs/agents).
[^6]: OpenCode. [Permissions](https://opencode.ai/v2/docs/permissions/).
[^7]: OpenCode. [MCP servers](https://opencode.ai/v2/docs/mcp-servers/).
[^8]: OpenCode. [Plugins](https://opencode.ai/v2/docs/plugins).
[^9]: OpenCode. [Migrate plugins from V1](https://opencode.ai/v2/docs/build/plugins/migrate-v1).
[^10]: OpenCode. [Plugin API overview](https://opencode.ai/v2/docs/build/plugins/).
[^11]: OpenCode. [CLI plugins](https://opencode.ai/v2/docs/build/plugins/cli/).
[^12]: OpenCode. [Instructions](https://opencode.ai/v2/docs/instructions).
[^13]: OpenCode. [Config](https://opencode.ai/v2/docs/config).
[^14]: OpenCode. [Themes](https://opencode.ai/v2/docs/themes).
