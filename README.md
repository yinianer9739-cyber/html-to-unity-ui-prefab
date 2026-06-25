# html-to-unity-ui-prefab

`html-to-unity-ui-prefab` is a Codex skill for converting HTML/CSS UI sources into Unity UGUI prefab workflows for a lightweight mini-game client framework.

The skill is designed for UI reconstruction, first-time UI generation, and large UI rebuilds where web-authored HTML/CSS is used as the input source.

## What It Does

- Reads project rules before Unity edits.
- Renders HTML/CSS through browser-computed layout data.
- Converts DOM nodes and computed styles into Unity UGUI prefab intent.
- Uses `Assets/Resources/ui/` as the default UI prefab path.
- Applies uniform width-based scale: `scale = 720 / htmlViewportWidth`.
- Maps common HTML nodes to UGUI concepts such as groups, buttons, text, images, RawImages, inputs, and ScrollViews.
- Splits image resources into large textures and small sprites.
- Requires TexturePacker before atlas work.
- Emits a generation report with unsupported CSS, inferred nodes, missing assets, and manual checks.

## Repository Layout

```text
html-to-unity-ui-prefab/
  SKILL.md
  agents/
    openai.yaml
  references/
    conversion-workflow.md
    output-checklist.md
```

## Installation

Copy this folder into your Codex skills directory:

```text
%USERPROFILE%\.codex\skills\html-to-unity-ui-prefab
```

Restart Codex or start a new conversation so the skill can be discovered.

## Usage

Ask Codex to use this skill when converting an HTML/CSS UI source into a Unity UGUI prefab workflow.

Example:

```text
Use html-to-unity-ui-prefab to convert this HTML/CSS UI into a Unity UGUI prefab following the project rules.
```

The skill expects the target Unity project to provide its own `AGENTS.md` and project-specific rule documents.

## Important Defaults

- UI prefabs: `Assets/Resources/ui/`
- Large textures: `Assets/Resources/tex/`
- Non-UI runtime prefabs: `Assets/Resources/prefab/`
- Atlas-generated assets: project atlas workflow
- Missing TexturePacker: stop and ask the project owner to install or configure it

## Notes

This skill is a workflow and rules package. It does not include a standalone Unity editor importer or a browser parser script. The actual conversion depends on the target project's Unity tooling and Codex's available browser or file tools.

## License

MIT License. See [LICENSE](LICENSE).

