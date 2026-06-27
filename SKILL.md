---
name: html-to-unity-ui-prefab
description: Use when converting HTML/CSS UI sources into Unity UGUI prefabs for the mini-game client framework, especially first-time UI reconstruction, large UI rebuilds, prefab generation from web-authored layouts, or validating HTML input intended for prefab automation.
---

# HTML To Unity UI Prefab

## Maintenance Rule

When maintaining this skill, keep `SKILL.zh-CN.md` synchronized in the same change whenever `SKILL.md` or `references/*.md` changes behavior, workflow steps, project structure rules, validation requirements, or completion reporting.

## Core Rule

Convert HTML/CSS into Unity UGUI prefabs through rendered browser layout data, not by guessing from source text alone. Always obey the target project's `AGENTS.md` and any applicable child-branch rules before generating or editing Unity files.

## Required Reading

- For the execution workflow, read `references/conversion-workflow.md`.
- Before claiming completion, read `references/output-checklist.md`.

## Default Pipeline

1. Read project rules, including `AGENTS.md`, detail docs, and `SubDoc/*.md` when present.
2. Confirm TexturePacker is installed before asset or atlas work. Stop if missing.
3. Render the HTML in a browser and collect `getBoundingClientRect()` plus computed styles.
4. Convert the rendered layout into a structured UI description.
5. Split images into large textures and small sprites, then build atlases for small sprites.
6. Inspect `Assets/Resources/ui/UIStartView.prefab` and use it as the standard View prefab structure before generating `UIXXXView`.
7. Generate or recreate `UIXXXView` and needed `UIXXXItem` prefabs under `Assets/Resources/ui/`.
8. Attach matching `UIXXXView.cs` when it exists, use UGUI components, and preserve project naming rules.
9. Emit a generation report listing created files, unsupported CSS, inferred nodes, missing assets, and manual checks.

## Non-Negotiable Defaults

- Use `Assets/Resources/ui/` for UI prefabs and items; do not create per-module UI prefab folders unless the user explicitly changes the rule.
- Use `UIStartView.prefab` as the canonical generated View baseline: root object named `UIXXXView`, matching `UIView` script on the root, a full-stretch `mask` background/mask layer, and a full-stretch `view` content container.
- Use uniform width-based scale: `scale = 720 / htmlViewportWidth`. Apply this scale to node sizes and centered positions.
- Treat height as adaptive viewport space, not a second independent scale factor.
- Use browser-computed layout for flex, text, margins, padding, transforms, and positioned nodes.
- Sort visual stacking by computed `z-index`; preserve DOM order for equal `z-index`.
- Do not silently invent business behavior. Ask or report when button callbacks, static item references, or script exposure are unclear.
- The HTML authoring rules for other AI tools are a separate handoff document, not part of this skill's required workflow.
