# HostPlugin agent guidance

- Keep HostPlugin skill-only. Do not add a generator CLI, npm runtime package, or hidden code-generation scripts without an explicit product decision.
- Treat official host documentation, installed host help, and native validators as sources of truth. Record the review date when changing a provider reference.
- Never claim cross-host support by silently translating unsupported component types. Update the capability report and require an explicit decision.
- Preserve canonical and prefixed skill behavior. Run the contract tests after changing either variant or any OpenCode integration copy.
- Keep plugin and marketplace versions synchronized. Do not tag, release, publish, or submit to a public marketplace without separate authorization.
- Preserve licenses, attribution, unrelated worktree changes, and existing marketplace entries.
- Before completion, run the repository contract tests, skill validation, Codex plugin validation, and every installed native host validator that can operate without authentication or external mutation.
