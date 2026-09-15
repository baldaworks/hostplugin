import { readFile } from "node:fs/promises"
import { fileURLToPath } from "node:url"

const skillURL = new URL("./skills/hostplugin-author/SKILL.md", import.meta.url)

function body(markdown) {
  return markdown.replace(/^---\r?\n[\s\S]*?\r?\n---\r?\n/, "")
}

export default {
  id: "hostplugin",
  async setup(ctx) {
    const markdown = await readFile(skillURL, "utf8")

    await ctx.skill.transform((editor) => {
      editor.add({
        id: "hostplugin-author",
        name: "HostPlugin Author",
        description:
          "Create, review, update, and publish coding-agent plugins for supported hosts.",
        location: fileURLToPath(skillURL),
        content: body(markdown),
      })
    })
  },
}
