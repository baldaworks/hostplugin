import json
import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "hostplugin"
VERSION = "0.1.0"


def read(path):
    return (ROOT / path).read_text(encoding="utf-8")


def load_json(path):
    return json.loads(read(path))


def skill_body(text):
    parts = text.split("---", 2)
    if len(parts) != 3:
        raise AssertionError("skill is missing YAML frontmatter")
    return parts[2].lstrip()


class ContractTests(unittest.TestCase):
    def test_json_files_parse_without_placeholders(self):
        placeholder_marker = "[" + "TODO:"
        for path in ROOT.rglob("*.json"):
            with self.subTest(path=path.relative_to(ROOT)):
                json.loads(path.read_text(encoding="utf-8"))
        for path in ROOT.rglob("*"):
            if (
                path.is_file()
                and ".git" not in path.parts
                and "__pycache__" not in path.parts
                and path.suffix != ".pyc"
            ):
                text = path.read_text(encoding="utf-8")
                self.assertNotIn(placeholder_marker, text, path)

    def test_marketplaces_point_to_one_hostplugin(self):
        paths = [
            ".agents/plugins/marketplace.json",
            ".claude-plugin/marketplace.json",
            ".grok-plugin/marketplace.json",
            ".github/plugin/marketplace.json",
            ".cursor-plugin/marketplace.json",
        ]
        for path in paths:
            with self.subTest(path=path):
                manifest = load_json(path)
                self.assertEqual("hostplugin", manifest["name"])
                self.assertEqual(1, len(manifest["plugins"]))
                entry = manifest["plugins"][0]
                self.assertEqual("hostplugin", entry["name"])
                source = entry["source"]
                if isinstance(source, dict):
                    source = source["path"]
                self.assertEqual("./plugins/hostplugin", source)

    def test_plugin_manifests_are_versioned_and_routed(self):
        expected = {
            ".codex-plugin/plugin.json": "./skills/",
            ".claude-plugin/plugin.json": "./skills/",
            ".grok-plugin/plugin.json": "./prefixed-skills/",
            ".plugin/plugin.json": "./prefixed-skills/",
            ".cursor-plugin/plugin.json": "./prefixed-skills/",
        }
        for relative, skills in expected.items():
            with self.subTest(path=relative):
                manifest = json.loads((PLUGIN / relative).read_text(encoding="utf-8"))
                self.assertEqual("hostplugin", manifest["name"])
                self.assertEqual(VERSION, manifest["version"])
                self.assertEqual(skills, manifest["skills"])

    def test_marketplace_versions_match_plugin_version(self):
        for path in [
            ".claude-plugin/marketplace.json",
            ".grok-plugin/marketplace.json",
            ".github/plugin/marketplace.json",
            ".cursor-plugin/marketplace.json",
        ]:
            with self.subTest(path=path):
                manifest = load_json(path)
                if "metadata" in manifest and "version" in manifest["metadata"]:
                    self.assertEqual(VERSION, manifest["metadata"]["version"])
                self.assertEqual(VERSION, manifest["plugins"][0]["version"])

    def test_skill_variants_have_matching_bodies(self):
        canonical = (PLUGIN / "skills/author/SKILL.md").read_text(encoding="utf-8")
        prefixed = (PLUGIN / "prefixed-skills/hostplugin-author/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("name: author", canonical)
        self.assertIn("name: hostplugin-author", prefixed)
        self.assertEqual(skill_body(canonical), skill_body(prefixed))

    def test_skill_enforces_preview_and_safe_discovery(self):
        text = (PLUGIN / "skills/author/SKILL.md").read_text(encoding="utf-8")
        for fragment in [
            "--help",
            "--version",
            "Build a capability report",
            "Present the preview",
            "explicit confirmation",
            "Do not publish",
            "unsupported",
        ]:
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, text)

    def test_skill_reference_paths_exist_for_plugin_and_opencode(self):
        paths = [
            PLUGIN / "skills/author/SKILL.md",
            PLUGIN / "prefixed-skills/hostplugin-author/SKILL.md",
            ROOT / "integrations/opencode/skills/hostplugin-author/SKILL.md",
        ]
        reference_names = [
            "capability-matrix.md",
            "safety-and-preview.md",
            "codex.md",
            "claude.md",
            "grok.md",
            "copilot.md",
            "opencode.md",
            "cursor.md",
        ]
        for skill in paths:
            text = skill.read_text(encoding="utf-8")
            for name in reference_names:
                with self.subTest(skill=skill.relative_to(ROOT), reference=name):
                    target = (skill.parent / "../../references" / name).resolve()
                    self.assertIn(f"../../references/{name}", text)
                    self.assertTrue(target.is_file(), target)

    def test_references_cover_every_host_and_are_officially_sourced(self):
        references = PLUGIN / "references"
        expected_sources = {
            "codex": [
                "https://learn.chatgpt.com/docs/build-plugins",
                "https://learn.chatgpt.com/docs/hooks",
            ],
            "claude": ["https://code.claude.com/docs/en/plugins-reference"],
            "grok": [
                "https://docs.x.ai/build/features/skills-plugins-marketplaces"
            ],
            "copilot": [
                "https://docs.github.com/en/copilot/reference/"
                "copilot-cli-reference/cli-plugin-reference"
            ],
            "opencode": ["https://opencode.ai/docs/plugins"],
            "cursor": [
                "https://cursor.com/docs/plugins",
                "https://cursor.com/docs/reference/plugins",
                "https://github.com/cursor/plugin-template",
            ],
        }
        for host, sources in expected_sources.items():
            with self.subTest(host=host):
                text = (references / f"{host}.md").read_text(encoding="utf-8")
                self.assertIn("2026-07-19", text)
                for source in sources:
                    self.assertIn(source, text)
        matrix = (references / "capability-matrix.md").read_text(encoding="utf-8")
        for host in ["Codex", "Claude Code", "Grok Build", "Copilot CLI", "OpenCode", "Cursor"]:
            self.assertIn(host, matrix)

    def test_codex_hooks_are_native_and_documented(self):
        matrix = read("plugins/hostplugin/references/capability-matrix.md")
        self.assertIn("| Hooks | Native (trust-gated) |", matrix)

        reference = read("plugins/hostplugin/references/codex.md")
        for fragment in [
            "hooks/hooks.json",
            "trust-gated components",
            "`${PLUGIN_ROOT}`",
            "`${PLUGIN_DATA}`",
            "validator-version conflict",
            "partial native validation",
            "do not misclassify the component as unsupported",
        ]:
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, reference)

    def test_cursor_metadata_uses_documented_locations(self):
        plugin = json.loads(
            (PLUGIN / ".cursor-plugin/plugin.json").read_text(encoding="utf-8")
        )
        self.assertEqual("HostPlugin", plugin["displayName"])
        for field in ["publisher", "category", "tags"]:
            with self.subTest(field=field):
                self.assertNotIn(field, plugin)

        marketplace = load_json(".cursor-plugin/marketplace.json")
        self.assertEqual(VERSION, marketplace["metadata"]["version"])
        entry = marketplace["plugins"][0]
        self.assertEqual(VERSION, entry["version"])
        self.assertEqual("developer-tools", entry["category"])
        self.assertEqual(["plugins", "skills", "authoring"], entry["tags"])

    def test_codex_ui_metadata_names_the_installed_skill(self):
        metadata = (PLUGIN / "skills/author/agents/openai.yaml").read_text(encoding="utf-8")
        self.assertIn('display_name: "HostPlugin Author"', metadata)
        self.assertIn("$hostplugin:author", metadata)

    def test_opencode_distribution_matches_prefixed_skill_and_references(self):
        source_skill = PLUGIN / "prefixed-skills/hostplugin-author/SKILL.md"
        installed_skill = ROOT / "integrations/opencode/skills/hostplugin-author/SKILL.md"
        self.assertEqual(source_skill.read_bytes(), installed_skill.read_bytes())

        source_refs = PLUGIN / "references"
        installed_refs = ROOT / "integrations/opencode/references"
        self.assertEqual(
            sorted(path.name for path in source_refs.glob("*.md")),
            sorted(path.name for path in installed_refs.glob("*.md")),
        )
        for path in source_refs.glob("*.md"):
            self.assertEqual(path.read_bytes(), (installed_refs / path.name).read_bytes())

    def test_readme_documents_all_hosts(self):
        text = read("README.md")
        self.assertIn(
            """### Codex

```sh
codex plugin marketplace add baldaworks/hostplugin
codex plugin add hostplugin@hostplugin
```""",
            text,
        )
        for fragment in [
            "$hostplugin:author",
            "/hostplugin:author",
            "/hostplugin-author",
            "claude plugin marketplace add baldaworks/hostplugin",
            "grok plugin install 'baldaworks/hostplugin#plugins/hostplugin' --trust",
            "copilot plugin marketplace add baldaworks/hostplugin",
            "agent plugin marketplace add",
            "integrations/opencode",
        ]:
            self.assertIn(fragment, text)


if __name__ == "__main__":
    unittest.main()
