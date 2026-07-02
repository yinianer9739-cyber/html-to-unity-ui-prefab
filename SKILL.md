---
name: html-to-unity-ui-prefab
description: Use when converting HTML/CSS UI sources into Unity UGUI prefabs for the mini-game client framework, especially first-time UI reconstruction, large UI rebuilds, prefab generation from web-authored layouts, or validating HTML input intended for prefab automation.
---

# HTML To Unity UI Prefab

## Maintenance Rule

When maintaining this skill, keep `SKILL.zh-CN.md` synchronized in the same change whenever `SKILL.md` or `references/*.md` changes behavior, workflow steps, project structure rules, validation requirements, or completion reporting.

Keep English Markdown in this skill free of CJK rule text. Put Chinese explanations in `SKILL.zh-CN.md`, except for source/prototype display text that must be preserved as data examples.

## Core Rule

Convert HTML/CSS into Unity UGUI prefabs by reading source first, then using rendered browser layout data to verify and measure what the source produces. Treat runnable prototypes, DOM, CSS, JavaScript state/rendering logic, browser-measured layout, screenshots, and Unity render or RectTransform exports as evidence inputs. The final Unity output must still follow explicit user instructions, target project rules, same-project Unity samples, resource ownership, serialization boundaries, and validation requirements. Always obey the target project's `AGENTS.md` and applicable child-branch rules before generating or editing Unity files.

The conversion is not complete merely because prefab files were written. Completion requires a quality gate that proves the generated Unity layout and visual evidence are close enough to the source-backed prototype, or reports the remaining mismatch as unfinished work.

All prototype interpretation is source-first. Read the relevant HTML, CSS, JavaScript, config, resource manifests, and generation inputs before opening the rendered page, running browser measurements, or looking at screenshots. Browser output and screenshots are verification or gap evidence after source review; they are not allowed to seed the first interpretation of structure, state, copy, assets, or behavior.

## First Priority: Element Evidence Plan

After source review and before mapping, generating, editing, or validating Unity files, write a conversion plan with per-element evidence. This is the first priority decision gate for the skill, not a completion-report extra. For every planned UI element, answer:

- Why does this element exist?
- Why use this image, color, font, material, or atlas entry?
- Why use this position, size, anchor, sibling order, mask, and hierarchy?
- Which states exist, and which serialized nodes or properties change for each state?
- Which interactions exist, and which View, model, or event binding owns them?
- Which parts must be static prefab/resource data, and which parts may be handled at runtime?
- Is any evidence missing or inferred?

Do not generate or edit prefabs/resources until the plan identifies stable GameObject names, parent paths, source evidence, Unity representation, runtime/static boundary, and remaining gaps for the affected elements. Use the user's requested documentation language for this plan. If the project has no approved documentation path for the plan, keep it in the conversation or a task-local scratch file instead of adding project Markdown. Present the element evidence plan and structured prefab spec before writing production `.prefab` files. Generating a new View requested by the current task does not need separate write confirmation; editing, overwriting, or regenerating an existing `.prefab` does. If evidence is missing, fill it from prototype source first, then browser measurements, source assets, atlas entries, approved prefabs, View bindings, config, tests, or explicit user messages; if it still cannot be proven, ask before continuing.

Evidence must be explicit. "Looks similar", "the current prefab already does this", "another screen uses this", or "the agent thinks it is close enough" is not enough. Mark measured values, source-authored values, inherited values, generated values, and inferred values differently. A current prefab is evidence only when the user approved it as the source or it matches prototype/source evidence.

Do not choose different images, colors, node structures, or state semantics just because a similar prefab currently does so. Do not use visually similar project sprites, common atlas entries, button backgrounds, panel backgrounds, frame sprites, or other reusable UI pieces as substitute source art. Same-project samples can justify serialized field shape, component layout, fileID/GUID syntax, nested prefab mechanics, or Unity-side structure; they do not justify choosing that sample's visual asset. If source evidence shows a border, badge, pill, chip, panel, card surface, or similar visual container but no approved sprite or texture exists, use one of these paths before editing: bind a source-proven asset, bind a generated asset documented by the plan, leave the reference empty or transparent when the visual is already baked into another approved asset, or ask the user to confirm the exact substitute. Never bind an unrelated atlas sprite and tint it to approximate the source.

For image/resource evidence, search prototype source files, DOM, CSS, JavaScript, referenced prototype assets, and source screenshots before Unity-side candidate art folders or current prefab choices. Do not label a file or directory as source art or authoritative source from its path, folder name, or naming convention alone; `art`, `source`, `raw`, `Z-main`, `Z-stage`, and similar names are only candidate locations until a generator, atlas input, export manifest, import log, config, documentation, or explicit user instruction proves the chain. In evidence plans, label unproven art folders as candidate art/resource with source status unproven, and continue tracing the generation chain before relying on them. If the prototype lacks a required image, generated raster assets are allowed only when the plan marks them as generated and records the prototype gap, visual/layout/state/interaction constraints, prompt or source inputs, expected output size, atlas name, sprite name, placement, and verification criteria. Do not call generated assets prototype sources.

## Unity Output Contract

Use HTML/CSS/JavaScript to discover what the UI should show and how states behave. Use Unity project evidence to decide how that UI is represented as prefabs, resources, scripts, GUID/fileID references, reusable items, runtime bindings, and validation. If web evidence and Unity production rules disagree, keep the web evidence in the report and adapt the generated Unity structure to the Unity rules.

Before generating or editing Unity UI assets:

- Find the Unity project root and read `ProjectSettings/ProjectVersion.txt` before writing assets. If the Unity version is missing, state the higher risk and ask whether to continue.
- Apply the Prefab Write Authorization Gate before editing existing prefabs. Generating a new `UIXXXView` requested by the current task does not require separate prefab write authorization. Editing, overwriting, regenerating, reverting, or hand-patching an existing `.prefab` requires explicit authorization for the current task and target prefab.
- Classify each target prefab as source-authored, generated, nested instance output, imported asset output, or unknown. For generated prefabs, fix the source spec, converter input, art input, or tool workflow first and regenerate; do not hand-patch generated YAML as the primary fix. Direct prefab-file editing is fragile across Unity versions, packages, GUIDs, and serialized component layouts, and is allowed only when the user explicitly approves the prefab file itself as the editing surface for the current task. Treat same-project samples and Unity validation as the source of truth for serialized output.
- Treat any project path containing `MiniGameKit` as framework-owned and read-only by default, especially `Assets/MiniGameKit/**`. Do not add, delete, modify, move, format, generate, or overwrite files there unless the user explicitly approves the exact file-changing work for the current task. If a solution appears to require changing framework files, stop and ask; prefer business-side files, configuration, prefabs, or approved extension points.
- Respect existing framework loader boundaries: prefabs, views, atlases, textures, fonts, sprites, and other non-Config runtime resources go through `MiniFrameWork.AssetManager` or another approved framework loader; UI atlas sprites for documented dynamic business states may go through `MiniFrameWork.UIManager.GetSprite/TryGetSprite`. Config assets under `Resources/config/` are not constrained by this AssetManager-only rule. Do not generate or add direct non-Config `Resources.Load(...)` calls anywhere in runtime or business code, including prefab, UI, texture, font, and sprite loading. If the existing `AssetManager` or approved framework loader does not support the needed non-Config resource type, path, or loading mode, stop and ask the user whether to add or extend that loader instead of using `Resources.Load`.
- Serialize default UI sprites, colors, Image types, masks, fonts, nine-slice choices, and item internals into prefabs/resources first. Runtime View code may bind data, toggle prepared states, call approved atlas sprite APIs for documented dynamic business states, or instantiate complete item prefabs; it must not repair missing default visuals or build raw product UI controls.
- Write the element evidence plan and structured prefab spec before generating or editing prefabs/resources. The spec must include prefab name/path, source/generated classification and owning input, hierarchy, Transform or RectTransform values, root object policy, anchors, masks, sibling order, components, serialized fields, asset and script GUID sources, tags, layers, active state, static flags, extraction decisions, and validation plan.
- Decide popup/sidebar View ownership before prefab generation. Ordinary click-open interfaces, popups, sidebars, help/profile/confirmation flows, and platform-gated entry flows default to separate `UIView` flows opened through `UIManager.ShowView` without asking. Recommend embedding only for same-View switching patterns such as local tabs/pages, bottom navigation buttons switching prepared page groups, or same-screen mode panels; if embedding is strongly recommended and not explicitly requested, explain why and ask first.
- Search same-project samples, referenced `.meta` files, script `.meta` files, and nested prefab examples before generating serialized fields.
- Evaluate reusable item/common prefab extraction before generation.
- Run the layout quality gate after generation: compare browser-measured HTML rects against generated Unity rects, record visual asset/style evidence for every meaningful element, and fail the task when required elements exceed the agreed thresholds or lack visual evidence. Use `scripts/compare_layout_quality.py` when a JSON comparison file is available.
- Validate generated or modified prefabs with `scripts/validate_unity_prefab.py`; run `scripts/check_static_ui_compliance.py` for UI prefab work when a project root is available; then try Unity batchmode import validation when practical. The prefab validator checks Unity object blocks, duplicate fileIDs, missing GameObject or Transform-like objects, dangling local fileID references, basic component back-references, parent/child references, GUID format, and matching `.meta` files when possible. The UI scanner catches root-only View prefabs, generated View masks missing the `UIStartView` Full script, non-ASCII GameObject names, visible or interactive components attached to a View root, direct non-Config `Resources.Load(...)` calls, built-in font fallback, runtime raw UI construction, and suspicious runtime visual repair. Treat validator, scanner, or layout quality errors as blockers, and treat warnings as risks to resolve or report. Static validation is not a replacement for Unity import validation.
- Before atlas generation, derive the atlas short name from the external atlas folder using the project atlas rule, then scan every source sprite file. Every small sprite filename must already use `<atlasShortName>@<functional_name>.png`, and the normalized sprite names must be unique. Treat bare names such as `btn_primary.png`, mixed bare/prefixed duplicates, or names that would generate unprefixed atlas entries as blockers. Do not run TexturePacker or keep generated atlas outputs until the source inputs are fixed and regenerated.

## Unity Serialization And Reuse Rules

Prefer copying the serialized shape of same-project objects over inventing fields. Inspect similar prefabs, scene objects, asset `.meta`, script `.meta`, nested prefab examples, prefab instance overrides, object ordering, component field names, class IDs, fileIDs, and external references before generating serialized data. Sample-driven copying is limited to serialization mechanics: do not copy a sample object's sprite, texture, color palette, material, Image type, or visual state into the target prefab unless that exact visual reference is separately proven by the element evidence plan or explicitly approved by the user.

Use hardcoded Unity knowledge only for low-risk basics such as `GameObject`, `Transform`, `RectTransform`, `m_GameObject`, `m_Component`, `m_Father`, and `{fileID, guid, type}` reference shapes. Do not fabricate complex MonoBehaviour, UI, renderer, animation, physics, or package-specific serialized fields without a project sample. New local fileIDs must be unique within the prefab, and every local reference must be updated consistently. Asset and script references must come from target `.meta` files, not invented GUIDs.

Text font references must be serialized into prefabs, generated specs, or explicit project font asset fields. Do not add runtime fallback code such as `Resources.GetBuiltinResource<Font>("LegacyRuntime.ttf")`, `Resources.GetBuiltinResource<Font>("Arial.ttf")`, or other Unity built-in font lookup for product UI.

Do not collapse styled text controls into bare `Text` objects when the source gives them visual container semantics. If source HTML/CSS, design notes, or screenshots show a label with background, border, radius, padding, pill/badge/chip behavior, disabled surface, hover surface, or state-specific decoration, create a serialized visual container such as `sp_xxx_bg` or `gr_xxx` with `Image` or `RawImage` as appropriate, then put `lb_xxx` text under it. Runtime code may change text or toggle prebuilt state groups; it must not create missing badge, pill, or container visuals.

This container rule does not imply that the container needs a `Source Image`. If the source visual is CSS-drawn and no source-proven or plan-documented generated sprite exists, keep the container's sprite/texture empty and its visual color transparent, or bake the CSS visual into a generated texture recorded by the evidence plan. Do not auto-fill styled containers from common atlases, button sprites, panel sprites, frame sprites, or any "stretchable" project sprite just because an `Image` component exists.

If multiple requested prefabs share structure, components, resource groups, naming semantics, or maintenance purpose, evaluate common prefab extraction before writing files. Signals include repeated hierarchy/components, repeated resource references, names such as `Common`, `Shared`, `Base`, `Template`, `ItemCell`, `ButtonBase`, `TongYong`, `JiChu`, or `MoBan`, and reuse that lowers future maintenance cost without hiding meaningful variation. Before extraction, present the candidate name/path, reason, dependent prefabs, fields that remain instance overrides, and risks; after confirmation, generate the common prefab first and then generate dependent prefabs as nested instances using same-project samples.

## Required Reading

- For the execution workflow, read `references/conversion-workflow.md`.
- Before claiming completion, read `references/output-checklist.md`.

## Default Pipeline

1. Read project rules, including `AGENTS.md`, detail docs, and `SubDoc/*.md` when present.
2. Identify and read source inputs: HTML, CSS, JavaScript, config/data files, resource manifests, generator inputs, and state/render code for the target UI states. Do this before opening a rendered page or screenshot.
3. Apply the Prefab Write Authorization Gate before editing existing prefabs. New requested View generation does not need separate write authorization.
4. Establish the Unity output contract: project root, Unity version, source/generated prefab classification, framework-owned path boundaries, resource/static-runtime boundaries, and validation plan.
5. Apply the popup/sidebar View ownership rule before prefab/resource edits or runtime View binding.
6. Confirm TexturePacker is installed before asset or atlas work. Stop if missing.
7. Only after source review and planning, render the HTML in a browser and collect `getBoundingClientRect()` plus computed styles for those states.
8. Use screenshots only after source review as visual verification, mismatch evidence, or gap evidence.
9. Convert the source-backed and browser-verified layout/state logic into a structured UI description.
10. Split images into large textures and small sprites, then build atlases for small sprites.
11. Inspect `Assets/Resources/ui/UIStartView.prefab` and use it as the standard View prefab structure before generating `UIXXXView`.
12. Generate new requested `UIXXXView` and needed `UIXXXItem` prefabs under `Assets/Resources/ui/`; recreate or overwrite existing prefabs only after explicit edit authorization.
13. Run the layout quality gate by comparing browser rects, generated Unity rects, and visual/style evidence; resolve or report every blocker before claiming completion.
14. Validate the prefab/resource result before editing matching `UIXXXView.cs`; runtime View code may only consume completed prefab nodes and item prefabs.
15. Attach or update matching `UIXXXView.cs` when it exists, use UGUI components, and preserve project naming rules.
16. Emit a generation report listing created files, unsupported CSS, inferred nodes, missing assets, layout quality results, validation results, skipped checks, and manual Unity checks.

## Non-Negotiable Defaults

- Use `Assets/Resources/ui/` for UI prefabs and items; do not create per-module UI prefab folders unless the user explicitly changes the rule.
- New requested View generation may create new `.prefab` files without separate write authorization; editing, overwriting, or regenerating existing `.prefab` files requires explicit authorization for the current task and target prefab.
- Use `UIStartView.prefab` as the canonical generated View baseline: root object named `UIXXXView`, matching `UIView` script on the root, a full-stretch `mask` background/mask layer that preserves the sample Full script, and a full-stretch `view` content container.
- Keep the prefab root thin: root normally contains only `RectTransform` plus the required View/controller script. Put Image, Text, Button, ScrollRect, layout groups, and other visible or interactive controls on named child objects.
- Decide popup/sidebar View ownership before prefab generation: ordinary click-open interfaces, popups, sidebars, help/profile/confirmation flows, and platform-gated entries default to separate `UIView` flows opened through `UIManager.ShowView` without asking. Recommend embedding only for same-View switching patterns such as local tabs/pages, bottom navigation buttons switching prepared page groups, or same-screen mode panels.
- Serialize default UI visuals into prefab/resources before runtime binding: sprites, colors, Image types, masks, raycast settings, fonts, nine-slice choices, and item internals. Do not repair missing default visuals in View code with runtime `SetSprite`, direct `image.sprite =`, direct `image.color =`, built-in font fallback, or ad-hoc resource loading.
- Extract repeated UI cells/cards/rows into `UIXXXItem.prefab`, nested/static prefab instances, or item-prefab pools under static layout containers. Three or more repeated instances are a hard extraction signal; two complex or reusable instances should also be extracted unless the spec documents why not.
- Use uniform width-based scale: `scale = 720 / htmlViewportWidth`. Apply this scale to node sizes and centered positions.
- Treat height as adaptive viewport space, not a second independent scale factor.
- Use browser-computed layout for flex, text, margins, padding, transforms, and positioned nodes.
- Export or otherwise record the generated Unity rect for each meaningful UI element and compare it to the browser-measured rect. Default completion thresholds are position delta <= 4 scaled pixels and size delta <= 2 percent unless the user or project sets stricter values. Exceeding the threshold is unfinished conversion work, not a cosmetic note.
- For required visual elements, record `asset_status` and `style_status` as source, generated, supported, missing, unsupported, inferred, substitute, or unknown. Required visuals with missing, unknown, inferred, placeholder, or substitute evidence block completion unless the user explicitly accepts the compromise.
- Preserve prototype-driven UI states and type-specific rendering rules from JavaScript, such as card variants, disabled states, cooldown labels, refresh/ad countdown states, modal pause behavior, and empty-state copy.
- Sort visual stacking by computed `z-index`; preserve DOM order for equal `z-index`.
- Do not silently invent business behavior. Ask or report when button callbacks, static item references, or script exposure are unclear.
- The HTML authoring rules for other AI tools are a separate handoff document, not part of this skill's required workflow.

## Atlas Input And Output Gate

For project atlases generated from external folders, derive the expected sprite prefix from the output atlas name. For example, `Z-common@...` produces `ui_atlas_common`, so every source sprite in that folder must be named `common@...`.

Do not treat TexturePacker, Unity import, or Inspector display as a naming fixer. The atlas tool preserves source sprite names into `.tpsheet` and `.png.meta`; therefore bare source filenames create bare atlas entries. Before building, fail the plan if any source sprite lacks the expected prefix, if both `name.png` and `<prefix>name.png` exist, or if normalized sprite names are duplicated.

After building or inspecting an atlas, check the generated `.tpsheet` and `.png.meta`. Every sprite name under `ui_atlas_<shortName>` must start with `<shortName>@`; `nameFileIdTable` entries must follow the same rule; duplicate sprite names outside Unity's id table are blockers. If the project has `UiAtlasNamingTests`, run that test or an equivalent static check before using atlas entries in prefabs.
