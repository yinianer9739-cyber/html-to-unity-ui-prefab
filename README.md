# html-to-unity-ui-prefab

`html-to-unity-ui-prefab` is a Codex skill for converting HTML/CSS UI sources into Unity UGUI prefab workflows for a lightweight mini-game client framework.

It is intended for UI reconstruction, first-time UI generation, large UI rebuilds, and prefab validation work where web-authored prototypes, source assets, Unity project rules, and same-project serialized samples must be reconciled before production Unity files are written.

## Current Focus

The skill now treats conversion as a source-first, evidence-driven workflow:

- Read HTML, CSS, JavaScript, config, resource manifests, generator inputs, and project rules before using screenshots or browser output.
- Write an element evidence plan before mapping, generating, editing, or validating Unity files.
- Write a structured prefab spec before prefab or resource edits.
- Classify target prefabs as source-authored, generated, nested instance output, imported asset output, or unknown.
- Fix source specs, converter inputs, art inputs, atlas inputs, or tool workflows before regenerating generated outputs.
- Preserve framework-owned boundaries such as `MiniGameKit` and existing `MiniFrameWork` loading patterns.
- Serialize default UI visuals into prefabs/resources before runtime View code binds data or toggles states.
- Use same-project samples for serialization mechanics, not as proof for copying unrelated visual assets.
- Validate generated or modified prefabs with the bundled static validation scripts before claiming completion.

## What It Covers

- Project rule and child-rule intake before Unity edits.
- Source-first prototype interpretation.
- Browser-computed layout collection after source review.
- Per-element evidence for visuals, layout, hierarchy, state, interaction, static data, runtime behavior, and remaining gaps.
- Unity output contracts for prefab ownership, source/generated status, framework boundaries, resource loading, and validation.
- `UIStartView.prefab`-based View generation under `Assets/Resources/ui/`.
- Thin View roots with visible and interactive controls placed under stable child nodes.
- Repeated item and common prefab extraction decisions.
- Atlas source naming gates before TexturePacker or generated atlas outputs are accepted.
- Static prefab and UI compliance validation.
- Completion reports that include generated files, skipped checks, validation results, mismatches, and remaining manual Unity checks.

## Repository Layout

```text
html-to-unity-ui-prefab/
  SKILL.md
  SKILL.zh-CN.md
  LICENSE
  README.md
  agents/
    openai.yaml
  references/
    conversion-workflow.md
    output-checklist.md
  scripts/
    validate_unity_prefab.py
    check_static_ui_compliance.py
    tests/
      test_validate_unity_prefab.py
      test_check_static_ui_compliance.py
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

The skill expects the target Unity project to provide its own `AGENTS.md` and project-specific rule documents. It also expects Codex to read `references/conversion-workflow.md` during execution and `references/output-checklist.md` before reporting completion.

## Important Defaults

- UI prefabs and item prefabs: `Assets/Resources/ui/`
- Large textures: `Assets/Resources/tex/`
- Standard generated View baseline: `Assets/Resources/ui/UIStartView.prefab`
- Default scale: `scale = 720 / htmlViewportWidth`
- TexturePacker is required before asset or atlas work.
- Atlas source sprites must already use the target atlas short-name prefix, such as `<atlasShortName>@<functional_name>.png`.
- Runtime View code may bind data, toggle prepared states, call approved atlas sprite APIs for documented dynamic business states, or instantiate complete item prefabs; it must not repair missing default visuals or build raw product UI controls.

## Validation Scripts

The repository includes static validation helpers used by the skill:

```text
python scripts/validate_unity_prefab.py <prefab-file>
python scripts/check_static_ui_compliance.py <unity-project-root>
```

`validate_unity_prefab.py` checks prefab YAML structure, duplicate fileIDs, dangling local references, basic GameObject/component relationships, GUID formats, and nearby `.meta` references when possible.

`check_static_ui_compliance.py` checks UI-specific risks such as root-only View prefabs, non-ASCII GameObject names, visible or interactive components on View roots, built-in font fallback, runtime raw UI construction, and suspicious runtime visual repair.

These scripts are static checks. They do not replace Unity import validation, so the skill still asks Codex to try Unity batchmode import validation when practical.

## Maintenance Notes

- Keep `SKILL.zh-CN.md` synchronized whenever `SKILL.md` or `references/*.md` changes behavior, workflow steps, project structure rules, validation requirements, or completion reporting.
- Keep English Markdown in the skill files free of CJK rule text; put Chinese explanations in `SKILL.zh-CN.md` unless preserving source/prototype display text as data.
- Update this README when the public workflow, repository layout, validation commands, or maintenance contract changes.
- The MIT license in `LICENSE` covers the skill documentation and bundled scripts.

## License

MIT License. See [LICENSE](LICENSE).
