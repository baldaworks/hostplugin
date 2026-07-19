# Host capability matrix

Use this matrix as a routing index, not as permission to invent a format. Read the selected host references and verify current local CLI behavior before writing.

Last reviewed: 2026-07-19.

| Component | Codex | Claude Code | Grok Build | Copilot CLI | OpenCode | Cursor |
| --- | --- | --- | --- | --- | --- | --- |
| Skills | Native | Native | Native | Native | Native | Native |
| Commands | No plugin field | Native/legacy | Claude-compatible | Native | Native | Native |
| Agents/subagents | Not a Codex plugin component | Native | Native | Native | Native | Native |
| Hooks | Not accepted by the current Codex plugin validator | Native | Native | Native | Native JS/TS plugin events | Native |
| MCP servers | Native | Native | Native | Native | Native config | Native |
| LSP servers | Not a Codex plugin component | Native | Native | Native | Host configuration only | Verify per plugin contract |
| Rules/instructions | Skill or project instructions | Plugin skills/components | Claude-compatible | Skill or agent | AGENTS.md/skills | Native rules |
| Apps | Native Codex app manifest | Unsupported as Codex apps | Unsupported as Codex apps | Unsupported as Codex apps | Unsupported as Codex apps | MCP Apps are a different contract |
| Monitors/themes/output styles | Unsupported | Host-specific | Verify Claude compatibility | Unsupported | Unsupported | Unsupported |
| Executables | Use skill instructions or app/MCP | Native `bin/` | Verify compatibility | Plugin extensions or declared components | npm/local JS/TS plugin | Verify plugin contract |

## Mapping policy

1. Model the user's requested behavior before choosing files.
2. Mark a component `native` only when the selected host has the same component type.
3. Mark intentional provider-only functionality `host-specific`.
4. Mark missing or unverified component contracts `unsupported`.
5. Never convert an agent to a skill, a hook to instructions, or an app to MCP without explicit user approval after explaining the semantic difference.
6. Permit different native files to implement the same approved behavior, but keep their user-visible outcome and safety gates aligned.

## Naming policy

- Use lowercase hyphen-case identifiers with a maximum of 64 characters unless the host is stricter.
- Use the plugin namespace where the host supplies one, such as `$plugin:skill` or `/plugin:skill`.
- Prefix component names with `<plugin>-` where discovery is flat or where the host does not guarantee namespacing.
- Do not rename existing public components during an update without explicit migration approval.
