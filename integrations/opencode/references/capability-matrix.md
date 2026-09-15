# Host and portable-standard capability matrix

Use this matrix as a routing index, not as permission to invent a format. Read
the reference for every selected host or portable standard and verify current
local CLI behavior for host targets before writing.

Last reviewed: 2026-09-15 (OpenCode v2 column; other targets retain their references).

| Component | Codex | Claude Code | Grok Build | Copilot CLI | OpenCode v2 | Cursor | Agent Plugins 1.0.0 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Skills | Native | Native | Native | Native | Native | Native | Native |
| Commands | No plugin field | Native/legacy | Claude-compatible | Native | Native | Native | Unsupported in portable core |
| Agents/subagents | Not a Codex plugin component | Native | Native | Native | Native | Native | Unsupported in portable core |
| Hooks | Native (trust-gated) | Native | Native | Native | Native V2 plugin hooks/events | Native | Unsupported in portable core |
| MCP servers | Native | Native | Native | Native | Native config | Native | Native |
| LSP servers | Not a Codex plugin component | Native | Native | Native | Unsupported (no LSP runtime) | Verify per plugin contract | Unsupported in portable core |
| Rules/instructions | Skill or project instructions | Plugin skills/components | Claude-compatible | Skill or agent | AGENTS.md/skills; instructions config inactive | Native rules | Unsupported in portable core |
| Apps | Native Codex app manifest | Unsupported as Codex apps | Unsupported as Codex apps | Unsupported as Codex apps | Unsupported as Codex apps | MCP Apps are a different contract | Unsupported in portable core |
| Monitors/themes/output styles | Unsupported | Host-specific | Verify Claude compatibility | Unsupported | Host-specific themes; other types unsupported | Unsupported | Unsupported in portable core |
| Executables | Use skill instructions or app/MCP | Native `bin/` | Verify compatibility | Plugin extensions or declared components | V2 npm/local JS/TS plugin | Verify plugin contract | Unsupported in portable core |

OpenCode targets 2.x. Its executable plugin API is incompatible with V1;
file-based skills and commands keep their paths. LSP configuration acceptance
does not provide an LSP runtime. Themes use the terminal-specific V2 contract.
See [OpenCode v2](opencode.md) for sources, limitations, and migration rules.

## Mapping policy

1. Model the user's requested behavior before choosing files.
2. Mark a component `native` only when the selected host has the same component type.
3. Mark intentional provider-only functionality `host-specific`.
4. Mark missing or unverified component contracts `unsupported`.
5. Never convert an agent to a skill, a hook to instructions, or an app to MCP without explicit user approval after explaining the semantic difference.
6. Permit different native files to implement the same approved behavior, but keep their user-visible outcome and safety gates aligned.
7. Treat Agent Plugins as a portable standard rather than a host. Its client
   extensions are non-portable and require an explicit design decision; never
   use them as an automatic mapping for an unsupported component.

## Naming policy

- Use lowercase hyphen-case identifiers with a maximum of 64 characters unless the host is stricter.
- Use the plugin namespace where the host supplies one, such as `$plugin:skill` or `/plugin:skill`.
- Prefix component names with `<plugin>-` where discovery is flat or where the host does not guarantee namespacing.
- Do not rename existing public components during an update without explicit migration approval.
