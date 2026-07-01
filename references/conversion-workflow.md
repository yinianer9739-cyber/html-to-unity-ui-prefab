# Conversion Workflow

## Project Rule Gate

Before any Unity edit:

1. Read the workspace `AGENTS.md`.
2. Follow triggered detail docs, especially UI module, resource, C# performance, logging, and verification rules.
3. Check whether `SubDoc/` exists beside `Docs/`; if it exists, read every `.md` directly under it.
4. If child-branch rules conflict with main rules, stop and ask the user which rule to follow.

## Element Evidence Plan

Write this plan after reading source inputs and before mapping HTML into Unity objects, generating resources, or editing existing prefabs. It is the first priority judgment step for conversion quality.

For every UI element that will be created, moved, removed, rebound, restyled, toggled, or handled by runtime code, answer:

- Why does this element exist?
- Why use this image, color, font, material, or atlas entry?
- Why use this position, size, anchor, sibling order, mask, and hierarchy?
- Which states exist, and which serialized nodes or properties change for each state?
- Which interactions exist, and which View, model, or event binding owns them?
- Which parts must be static prefab/resource data, and which parts may be handled at runtime?
- Is any evidence missing or inferred?

For each affected element, record the concrete evidence fields that apply: screenshot region, HTML node, existing prefab node, source art file, atlas entry, config row, or explicit user instruction; visual basis for sprite, texture, color, font, `.meta` GUID, atlas entry, and material; layout basis for bounds, anchors, size, sibling order, mask, and view layer; state coverage for default active, selected, disabled, locked, hover, pressed, empty, and which prebuilt nodes toggle; interaction ownership for button, toggle, drag, scroll, modal, navigation, model fields, events, and runtime binding.

Use this plan to decide whether generation may proceed. Missing evidence is a blocker for material prefab/resource changes until it is proven from prototype source first, then browser measurements, source assets, atlas entries, approved prefabs, View bindings, config, tests, or explicit user messages.

Do not accept weak evidence. "Looks similar", "the current prefab already does this", "another screen uses this", or "close enough" is not a source. Mark measured, source-authored, inherited, generated, and inferred values separately. A current prefab is evidence only when the user approved it as the source or it matches prototype/source evidence.

Do not choose images, colors, node structures, or state semantics because a similar prefab currently uses them. Same-project samples can prove serialization shape, component layout, fileID/GUID syntax, nested prefab mechanics, or Unity-side structure; they do not prove visual asset identity. Do not use visually similar project sprites, common atlas entries, button backgrounds, panel backgrounds, frame sprites, or other reusable UI pieces as substitute source art. If source evidence shows a border, badge, pill, chip, panel, card surface, or similar visual container but no approved sprite or texture exists, bind a source-proven asset, bind a generated asset documented by the plan, leave the reference empty or transparent when the visual is already baked into another approved asset, or ask the user to confirm the exact substitute before editing.

If the project has no approved documentation path for the element evidence plan, keep the plan in the conversation or a task-local scratch file instead of adding project Markdown.

## Source-First Intake

Before opening a rendered page, controlling a browser, collecting screenshots, or using screenshot evidence, read the relevant source inputs:

- HTML files and templates.
- CSS files, inline styles, theme variables, and generated style inputs.
- JavaScript or TypeScript that creates UI, mutates DOM, switches state, loads assets, or binds events.
- Config/data files that drive labels, states, resource keys, item lists, or feature variants.
- Resource manifests, atlas inputs, generator inputs, and source asset references.

Record which source files define each target UI state. Browser rendering and screenshots may verify source interpretation or expose mismatches only after this source pass.

## Unity Output Preparation

Before converting web evidence into Unity files, establish how the result belongs in the Unity project. HTML/CSS/JavaScript can prove layout, text, state, and visual intent; same-project Unity samples, resource ownership, `.meta` files, prefab structure, runtime/static boundaries, and validation decide how that intent is serialized.

Before editing Unity files:

1. Find the Unity project root by locating `ProjectSettings/ProjectVersion.txt`, `Assets/`, and `Packages/manifest.json`.
2. Read `ProjectSettings/ProjectVersion.txt`. If the Unity version is missing, state the higher risk and ask whether to continue.
3. Classify each target prefab as source-authored, generated, nested instance output, imported asset output, or unknown.
4. If a prefab is generated from HTML, a source spec, a converter, atlas input, an editor tool, or another generator, fix that source/input first and regenerate. Do not hand-patch generated YAML as the primary fix. Direct prefab-file editing is fragile across Unity versions, packages, GUIDs, and serialized component layouts, and is allowed only when the user explicitly approves the prefab file itself as the editing surface for the current task. Treat same-project samples and Unity validation as the source of truth for serialized output.
5. Treat any project path containing `MiniGameKit` as framework-owned and read-only by default. Do not add, delete, modify, move, format, generate, or overwrite files there unless the user explicitly approves the exact file-changing work. If the solution appears to require changing framework files, stop and ask; prefer business-side files, configuration, prefabs, or approved extension points.
6. Respect existing framework loader boundaries. Prefabs, views, and atlases normally go through `MiniFrameWork.AssetManager`; UI atlas sprites for documented dynamic business states may go through `MiniFrameWork.UIManager.GetSprite/TryGetSprite`; generated `ConfigXXXEntry` JSON data is loaded as `TextAsset` from `Resources/config/ConfigXXXEntry`. Do not add new framework APIs or business-side `Resources.Load` wrappers unless explicitly approved.
7. Serialize default UI visuals into prefab/resources first; runtime View code may bind data, toggle prepared states, call approved atlas sprite APIs for documented dynamic business states, or instantiate complete item prefabs, but must not repair missing default visuals or construct raw product UI controls.
8. Search same-project samples before generating serialized fields: similar prefabs, scene objects, script `.meta`, asset `.meta`, nested prefab examples, prefab instance overrides, class IDs, fileIDs, object order, component field names, and external references.
9. Write the element evidence plan and structured prefab spec before prefab/resource edits. Present the spec for confirmation before writing production `.prefab` files unless the user has already explicitly approved automated generation or regeneration for this task.
10. Evaluate common prefab or item prefab extraction before generation.
11. Validate generated prefabs with `scripts/validate_unity_prefab.py`, run `scripts/check_static_ui_compliance.py` for UI prefab work when a project root is available, and try Unity batchmode import validation when practical.

The HTML parser may determine rendered layout and prototype state evidence. It must not decide asset identity, prefab ownership, serialized fields, GUID/fileID references, default visual serialization, or runtime/static boundaries by itself. If a parser, mapper, inferred component type, screenshot-derived layout, or generated resource rule touches those Unity concerns, adapt the HTML conversion result to the Unity output preparation above.

## HTML/CSS Intake

Use the runnable prototype as an evidence input when it is available, but read the target source files before opening or inspecting the rendered page. Extract state-specific rendering logic from source first, such as card types, disabled states, selected states, cooldown labels, refresh timers, modal pause behavior, empty-state copy, and event handlers, then reconcile that evidence with explicit user instructions, target project rules, same-project Unity samples, and the Unity output preparation above.

Use screenshots only after source review as visual evidence, mismatch evidence, or gap evidence. Do not treat screenshots as a higher-priority source than source code, explicit user instructions, target project rules, same-project Unity samples, or Unity output rules.

After source review, render HTML with a browser engine and collect:

- viewport width and height
- DOM tree order
- `getBoundingClientRect()` for each visible node
- computed styles for position, display, width, height, color, font, background, overflow, transform, opacity, z-index
- image source URLs and natural image sizes
- text content after rendering

Do not hand-calculate flex, margin collapse, text metrics, or transforms from source CSS when browser-computed values are available.

When a screenshot and source-backed runnable prototype disagree, report the mismatch before editing generated Unity assets. Resolve it by priority: explicit user instruction first, then source files and project rules, then Unity output rules, then approved same-project Unity samples, then browser measurements, then screenshot evidence.

Do not label directories or files as authoritative source art from path names alone. Folders named like `art`, `source`, `raw`, `Z-main`, `Z-stage`, or similar are only candidates until a generator, atlas input, export manifest, import log, config, documentation, or explicit user instruction proves the source chain. In evidence plans, label unproven art folders as candidate art/resource with source status unproven, and continue tracing the generation chain before relying on them.

## DOM To UGUI Mapping

| HTML / style | Unity output |
| --- | --- |
| `div` | `gr_xxx` group by default |
| `button` | `bt_xxx` Button |
| `img` with either side <= 300 | Image sprite from atlas |
| `img` with either side > 300 | RawImage large texture |
| `input` | WebglInput |
| visible text node | Text |
| `overflow: scroll` / `auto` | ScrollView |
| `background-image` | Image or RawImage according to source size |
| `background-color` | solid-color Image |

Prefer `data-ui-type` over tag inference when present.

Map prototype state logic into serialized prefab states or runtime bindings deliberately. Static visuals, card subnodes, labels, and empty-state containers should exist in prefabs or item prefabs; runtime code should toggle/bind prebuilt nodes instead of inventing product UI controls from screenshot-derived guesses.

When DOM/CSS inference and Unity output rules disagree, preserve the DOM/CSS as evidence but follow the Unity rules for structure, serialized field generation, resource identity, root policy, item extraction, runtime/static boundary, and validation.

## Naming

Node names must be lowercase English and must not contain Chinese characters.

Name priority:

1. `data-ui-name`
2. `id`
3. meaningful `class`
4. tag and semantic role
5. generated name

Prefixes:

| Purpose | Prefix |
| --- | --- |
| Button | `bt_` |
| Text | `lb_` |
| Image sprite | `sp_` |
| RawImage texture | `tex_` |
| Group | `gr_` |
| Input | `ip_` |

If an inferred name is unstable, generate a legal name and include it in the report.

## Scale And Coordinates

Use the project default reference width:

```text
scale = 720 / htmlViewportWidth
```

Apply the same scale to node width, node height, centered x/y positions, and font size unless the user requests exact pixel text. Do not use a separate height scale for y positions.

Coordinate conversion:

1. Use the rendered viewport center as `(0, 0)`.
2. Convert each node center from browser top-left coordinates into centered coordinates.
3. Multiply centered coordinates by `scale`.
4. Use centered anchors by default.
5. Use edge or stretch anchors only when HTML semantics or `data-ui-anchor` clearly requires it.

## Stacking And Hierarchy

Use computed `z-index` first. For equal `z-index`, preserve DOM order. Later Unity siblings render above earlier siblings.

Preserve logical groups when they help readability or later binding. Do not flatten everything into one layer unless the HTML is already flat and no grouping is useful.

`position: fixed` maps relative to the prefab root. `position: absolute` maps relative to the nearest positioned ancestor. Normal flow nodes use browser-computed bounds.

## Assets

Split images by source size:

- Any side greater than `300` goes to `Assets/Resources/tex/`.
- Small sprites are grouped by interface/module source folder.
- Small sprite names use module prefix and function suffix, such as `main@confirm_button`.

Before building an atlas from an external folder, derive the expected sprite prefix from the output atlas short name. For example, `Z-common@...` generates `ui_atlas_common`, so every source sprite in that folder must be named `common@...`. Bare filenames such as `btn_primary.png`, mixed bare/prefixed duplicates such as `btn_primary.png` plus `common@btn_primary.png`, and duplicate normalized names are blockers. Fix the source input and regenerate; do not rely on TexturePacker, Unity import, or Inspector display to repair names.

After atlas generation, inspect the generated `.tpsheet` and `.png.meta`. Every sprite name under `ui_atlas_<shortName>` must start with `<shortName>@`, including `nameFileIdTable` entries. If the project has `UiAtlasNamingTests`, run that test or an equivalent static check before binding atlas entries in prefabs.

For CSS-drawn visuals that are necessary for the UI, rasterize to PNG first, then apply the same split rules.

Before binding an image to a prefab, record evidence for why that image is used: prototype asset reference, source art file, atlas entry, generated asset prompt, config row, or explicit user instruction. If the image is generated because the prototype lacks an asset, mark it as generated and record the gap, prompt/source inputs, expected output size, atlas name, sprite name, placement, and visual verification criteria.

Do not call generated images prototype sources. If an image cannot be justified from prototype evidence, an approved source chain, generated asset record, or explicit user instruction, ask before generating or binding it. Never bind an unrelated atlas sprite and tint it to approximate the source.

## Nine-Slice

Only write nine-slice data when one of these is true:

- The HTML has `data-ui-slice="left,top,right,bottom"`.
- The user explicitly asks for it.
- The asset is confidently a button, background, or frame and the border value is safe.

Prefer values greater than `8` when inferred. If uncertain, do not guess; add the asset to the manual-check report.

Nine-slice data may be written by editing the matching `.tpsheet` file when that is the project-supported path.

## Prefab Generation

Generate `UIXXXView.prefab` under:

```text
Assets/Resources/ui/
```

Before generating or regenerating a View prefab, inspect:

```text
Assets/Resources/ui/UIStartView.prefab
Assets/Scripts/Runtime/Start/UIStartView.cs
```

Use `UIStartView` as the project-standard generated View structure:

- Root GameObject name matches the prefab/class name, such as `UIXXXView`.
- Root has a full-stretch `RectTransform`.
- Root attaches the matching `UIXXXView.cs` MonoBehaviour when it exists.
- First child is `mask`, a full-stretch background/mask layer. Preserve its transparent Image and the FULL script from the sample; that script handles notch-screen adaptation through reverse fill, not ordinary visual content layout.
- Second child is `view`, a full-stretch content container. Place regular generated visible UI controls under `view`.
- Do not put generated visual controls directly under the root when the `view` container is present.
- Do not move background coverage, modal mask behavior, or notch-screen reverse-fill behavior out of `mask` unless the user explicitly requests a different structure.
- Keep generated item prefabs separate; do not fold reusable list rows or cells into the View root structure.

Keep the root as a thin layout and scripting boundary. Do not put Image, Text, TMP text, Button, Toggle, Slider, ScrollRect, CanvasRenderer, layout groups, or content widgets on the root unless the user explicitly asks for it or same-project samples require it.

Do not generate root-only or placeholder UI prefabs for visible screens. A converted production View prefab must contain the static child hierarchy for labels, buttons, panels, lists, HUD markers, and other visible controls.

Serialize default UI visual references into the prefab/resources before runtime View code is written. If View binding reveals a missing static visual reference, return to prefab/resource generation instead of adding runtime visual repair code.

When creating a matching `UIXXXView.cs`, follow the `UIStartView.cs` registration pattern: subclass `UIView`, provide static `RegisterView()`, create `UIViewInfo`, set `viewName`, `canvasType`, `viewType`, and call `UIManager.Instance.RegisterView(info)`.

If the prefab already exists, delete and recreate it only when the user asked to regenerate the view. Attach `UIXXXView.cs` if a matching MonoBehaviour exists.

Use native UGUI components by default:

- WebglInput for input fields
- ScrollView for scrolling regions
- project font at `Assets/Resources/font/normal` for Text
- Image for atlas sprites and pure color blocks
- RawImage for large textures

For Text, set text content, font size, color, alignment, and RectTransform size so text is not clipped.

Do not collapse styled text controls into bare `Text` objects when the source gives them visual container semantics. If HTML/CSS, design notes, or screenshots show a label with background, border, radius, padding, pill/badge/chip behavior, disabled surface, hover surface, or state-specific decoration, create a serialized visual container such as `sp_xxx_bg` or `gr_xxx` with `Image` or `RawImage`, then place `lb_xxx` text under it. Runtime code may change text or toggle prepared state groups, but must not create the missing visual container.

This container rule does not imply that the container needs a `Source Image`. If the source visual is CSS-drawn and no source-proven or plan-documented generated sprite exists, keep the container's sprite or texture empty and its visual color transparent, or bake the CSS visual into a generated texture recorded by the evidence plan. Do not auto-fill styled containers from common atlases, button sprites, panel sprites, frame sprites, or any stretchable project sprite just because an `Image` component exists.

## Item Prefabs

Create `UIXXXItem.prefab` under `Assets/Resources/ui/` for repeated or complex groups:

- repeated 3 or more times
- 2 complex or reusable instances unless the structured spec records why they intentionally diverge
- list rows
- backpack cells
- reward cells
- repeated composite UI blocks
- stat cells, shop goods cards, skill cards, inventory slots, HUD markers, option rows, and fixed-grid repeated cards

If the item belongs to a ScrollView, do not place it as a static View reference. For other cases, ask whether the item should be statically placed in the View.

For data-driven repeated UI, the parent View prefab may contain only a static container with `GridLayoutGroup`, `HorizontalLayoutGroup`, `VerticalLayoutGroup`, `ScrollRect`, viewport, and content objects configured from project samples. Runtime code may instantiate or reuse complete `UIXXXItem.prefab` instances, but must not build the raw item controls with `new GameObject` or `AddComponent<Image/Text/Button/...>`.

## Structured Prefab Spec

Before generating prefab files or UI resources, prepare a concise structured spec containing:

- Prefab name and output path.
- Source/generated classification and owning source file, converter input, tool, or generator.
- GameObject hierarchy and `UIStartView` root/mask/view usage.
- Root object policy: keep the outermost prefab object as a thin root whenever practical.
- RectTransform values, anchors, sibling order, masks, and layer decisions.
- Component list and important serialized fields.
- Asset references and `.meta` GUID sources.
- Script components and MonoScript GUID sources.
- Tags, layers, active state, and static flags when relevant.
- Common prefab and item extraction decisions.
- Validation plan.

Ask only for missing details that materially affect generation. If a component cannot be generated from stable Unity conventions or local samples, ask for a sample or reduce scope.

## Sample-Driven Serialization

Prefer same-project serialized examples over invented fields. Use hardcoded Unity knowledge only for low-risk basics such as `GameObject`, `Transform`, `RectTransform`, `m_GameObject`, `m_Component`, `m_Father`, and `{fileID, guid, type}` reference shapes. Do not fabricate complex MonoBehaviour, UI, renderer, animation, physics, or package-specific serialized fields without a project sample.

Sample-driven copying is limited to serialization mechanics. Do not copy a sample object's sprite, texture, color palette, material, Image type, or visual state into the target prefab unless that exact visual reference is separately proven by the element evidence plan or explicitly approved by the user.

When creating new local fileIDs, keep them unique within the prefab and update every local reference consistently. When referencing assets or scripts, read the target `.meta` file for the GUID instead of inventing one.

## Static Validation Details

Run `scripts/validate_unity_prefab.py` on every generated or modified prefab. The validator checks Unity object blocks, duplicate fileIDs, missing GameObject or Transform-like objects, dangling local fileID references, basic component back-references, parent/child references, GUID format, and matching `.meta` files when possible.

Run `scripts/check_static_ui_compliance.py` for UI prefab work when a project root is available. The scanner catches root-only View prefabs, non-ASCII GameObject names, visible or interactive components attached to a View root, built-in font fallback, runtime raw UI construction, and suspicious runtime visual repair.

Treat validator errors as blockers. Treat warnings as risks to resolve or report. The validator is not a replacement for Unity import validation.

After static validation, try Unity batchmode import validation when a Unity Editor executable is available and practical. Inspect logs for YAML parse errors, missing scripts, asset import errors, prefab load failures, and missing GUIDs. If Unity cannot be found or batchmode cannot run, state that Unity import validation was not completed.

## Common Prefab Extraction

If multiple requested prefabs share structure, components, resource groups, naming semantics, or maintenance purpose, evaluate extraction before writing files.

Signals include repeated GameObject hierarchy, repeated component combinations, repeated material/sprite/model/script/audio/effect references, names like `Common`, `Shared`, `Base`, `Template`, `ItemCell`, `ButtonBase`, `TongYong`, `JiChu`, or `MoBan`, and reuse that reduces maintenance cost without hiding meaningful variation.

Before extraction, present the common prefab name and path, reason for extraction, prefabs that will reference it, fields that remain as instance overrides, and risks. After confirmation, generate the common prefab first, then generate dependent prefabs as prefab instances or nested references using local samples for the exact serialized shape.
