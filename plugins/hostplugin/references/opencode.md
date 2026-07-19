# OpenCode extension contract

Last reviewed: 2026-07-19.

Official references:

- https://opencode.ai/docs/skills
- https://opencode.ai/docs/commands
- https://opencode.ai/docs/agents
- https://opencode.ai/docs/plugins

## Distribution model

OpenCode does not consume the same marketplace bundle as the other targets. Emit project-local files or document a manual/global copy. Do not describe copied skills as an installed OpenCode npm plugin.

## Native components

- Skills: `.opencode/skills/<name>/SKILL.md`, with Claude- and agent-compatible discovery locations also supported.
- Commands: `.opencode/commands/<name>.md` or the documented config form.
- Agents: `.opencode/agents/<name>.md` or the documented config form.
- MCP: `opencode.json` configuration using the current schema.
- Plugins/hooks/custom tools: JavaScript or TypeScript modules below `.opencode/plugins/`, or published npm modules declared in config.

An OpenCode JS/TS plugin is executable code and is not equivalent to an Agent Skill. Require an explicit component request, dependency review, and execution-risk preview before generating one.

## Skill constraints

Use lowercase hyphen-case names matching their directory. Keep descriptions between 1 and 1024 characters. OpenCode loads skills on demand through its skill tool; a command wrapper may provide an explicit slash invocation.

## Validation

Parse frontmatter and config, verify discovery paths, and test in a disposable project. Do not run OpenCode with a model merely to validate static discovery unless the user approves the model call.
