# Output Checklist

Before reporting completion, verify and summarize:

## Required Files

- Element evidence plan was written before conversion/generation decisions.
- Structured prefab spec was written before prefab/resource edits.
- Structured prefab spec was presented before writing production `.prefab` files. New requested View generation did not need separate write confirmation; editing, overwriting, or regenerating existing prefabs did.
- Relevant HTML/CSS/JavaScript/config/resource source inputs were read before opening the rendered page, running browser measurements, or using screenshots.
- `UIXXXView.prefab` created or regenerated under `Assets/Resources/ui/`.
- `UIXXXItem.prefab` files created for repeated or complex items when applicable.
- New Unity files have `.meta` files.
- Matching `UIXXXView.cs` was attached if it exists.
- Target prefabs were classified as source-authored, generated, nested instance output, imported asset output, or unknown.
- Explicit edit authorization was obtained for the current task and target prefab before modifying, regenerating, overwriting, reverting, or hand-patching any existing `.prefab`. New requested View generation was allowed to create new prefab files without separate write authorization.
- Generated prefab sources, converter inputs, atlas inputs, or tool workflows were fixed before regeneration; generated prefab files were not hand-patched as the primary fix unless explicitly approved.
- Direct prefab-file edits were performed only when that file was explicitly approved as the editing surface.
- Runtime code fixes, validation passes, reports, screenshot inspections, and rule checks did not include incidental edits to existing prefabs without explicit edit authorization.
- Popup/sidebar View ownership was decided before prefab generation. Ordinary click-open interfaces, user/profile popups, button panels, confirmation popups, sidebar/help overlays, and platform-gated entry flows became separate `UIView` flows opened through `UIManager.ShowView` without asking unless they were same-View switching patterns or the user explicitly asked for one View to own the whole flow.
- No new interface flow was embedded inside an existing View merely because it appears as an overlay, popup, or sidebar.

## Resource Checks

- TexturePacker was found before atlas work.
- Large images were placed under `Assets/Resources/tex/`.
- Small sprites were grouped and packed through the atlas workflow.
- Atlas source sprite filenames use the target atlas short-name prefix, such as `<atlasShortName>@<functional_name>.png`; no bare names, mixed bare/prefixed duplicates, or duplicate normalized sprite names remain.
- Generated `.tpsheet` and `.png.meta` sprite entries for every `ui_atlas_<shortName>` all start with `<shortName>@`, including `nameFileIdTable`; `UiAtlasNamingTests` or an equivalent static check was run when available.
- Image and RawImage references resolve.
- Text font uses `Assets/Resources/font/normal`.
- Every UI Text font reference points to an assigned project font asset; runtime scripts contain no built-in font fallback such as `Resources.GetBuiltinResource<Font>`, `LegacyRuntime.ttf`, or `Arial.ttf`.
- Asset and script GUIDs came from `.meta` files or same-project samples.
- Asset identity was justified by prototype/source evidence, generated asset records, config, atlas entries, or explicit user instruction; path names alone were not treated as proof.
- Visually similar project sprites, common atlas entries, button backgrounds, panel backgrounds, frame sprites, or other reusable UI pieces were not used as substitute source art.
- Same-project samples were used only for serialization mechanics or approved Unity structure, not as proof for copying their visual assets, colors, materials, Image types, or visual states.
- Default UI visuals were serialized into prefabs/resources before runtime binding code.
- Framework loading boundaries were preserved: non-Config runtime resources go through `AssetManager` or another approved framework loader, no direct non-Config `Resources.Load(...)` calls were added, Config assets under `Resources/config/` were treated as exempt, and missing non-Config loader support was escalated to the user before adding APIs or fallbacks.
- HTML conversion, parser, screenshot, DOM mapping, and resource inference decisions were reconciled with Unity resource identity, serialized fields, GUID/fileID references, runtime/static boundaries, item extraction, and validation.

## Layout Checks

- Source files for runnable prototype DOM/CSS/JavaScript state logic were checked before opening the rendered page or relying on screenshots.
- Browser-computed layout was used.
- Uniform width scale was used.
- Browser `getBoundingClientRect()` values were recorded for meaningful elements.
- Generated or exported Unity rects were recorded for matching meaningful elements.
- Layout quality was compared with `scripts/compare_layout_quality.py` or an equivalent report when comparison data was available.
- Position delta is <= 4 scaled pixels and size delta is <= 2 percent for required elements, unless the user or project approved a different threshold.
- Required visual elements have source-backed or plan-documented generated `asset_status`; missing, unknown, inferred, placeholder, or substitute visual evidence was treated as a blocker unless explicitly accepted.
- Required style features have supported or rasterized `style_status`; missing, unknown, inferred, or unsupported style evidence was treated as a blocker unless explicitly accepted.
- Browser screenshot versus Unity screenshot or overlay/diff was produced when Unity screenshot automation was practical; visible mismatch was resolved or reported as unfinished work.
- Generated View structure matches `UIStartView.prefab`: full-stretch root, `mask` as the background/mask layer with its FULL notch reverse-fill script preserved, and `view` as the content container.
- Root remains thin and does not contain visible or interactive UI controls unless explicitly required by the user or same-project samples.
- Every visible control is a named child object with stable English naming; visible controls are not placed on the prefab root unless explicitly required.
- Default nodes use centered anchors unless edge anchoring was explicit.
- Text RectTransform sizes are large enough to avoid clipping.
- ScrollView content, viewport, and item template are sensible.
- Sibling order follows z-index then DOM order.
- Screenshots, when supplied, were reviewed only after source inspection and did not override source files, explicit user instructions, target project rules, same-project Unity samples, or Unity output rules.
- UI element evidence answers why each affected element exists; why its image/color/font/material/atlas entry is used; why its position, size, anchor, sibling order, mask, and hierarchy are used; which states and serialized changes exist; which View/model/event binding owns interactions; which parts are static data versus runtime behavior; and whether evidence is missing or inferred.
- Evidence distinguishes measured, source-authored, inherited, generated, and inferred values; "looks similar", current-prefab habit, or another-screen similarity was not treated as proof.
- Styled labels with source-backed background, border, radius, padding, pill, badge, chip, disabled, hover, or state-decoration semantics were generated as visual containers with child text, not collapsed into bare `Text` objects.
- Styled visual containers were not auto-filled from common atlases, button sprites, panel sprites, frame sprites, or stretchable project sprites when no source-proven or plan-documented generated sprite existed.
- Repeated cells/cards/rows were extracted as item prefabs, nested/static instances, or item-prefab pools, or the structured spec records an explicit exception.
- Common prefab extraction was evaluated when prefabs shared structure, components, resources, naming semantics, or maintenance purpose; confirmed common prefabs were generated before dependent prefabs.

## Serialization Checks

- Same-project samples were checked before generating serialized fields: prefabs, scene objects, `.meta` files, nested prefab examples, prefab instance overrides, class IDs, fileIDs, object order, component fields, and external references.
- New local fileIDs are unique within each prefab and local references are updated consistently.
- Asset and script references came from target `.meta` GUIDs.
- Complex MonoBehaviour, UI, renderer, animation, physics, or package-specific fields were copied from project samples or explicitly reduced in scope.

## Static And Import Validation

- `scripts/validate_unity_prefab.py` was run on every generated or modified prefab.
- `scripts/check_static_ui_compliance.py` was run for UI prefab work when a project root was available.
- Static UI compliance covered root-only View prefabs, generated View masks missing the `UIStartView` Full script, non-ASCII GameObject names, visible or interactive components on a View root, direct non-Config `Resources.Load(...)` calls, built-in font fallback, runtime raw UI construction, and suspicious runtime visual repair.
- Validator errors were treated as blockers; warnings were resolved or reported as risk.
- Unity batchmode import validation was attempted when a Unity Editor executable was available and practical.
- Unity import logs were checked for YAML parse errors, missing scripts, asset import errors, prefab load failures, and missing GUIDs.
- Runtime View code was edited only after prefab/resource validation; runtime code consumes completed prefab nodes and complete item prefabs instead of constructing raw product UI controls.
- Runtime View code does not repair missing default UI visuals with ad-hoc sprite/color/font/resource fallback logic.
- Runtime instantiation of complete `UIXXXItem.prefab` instances is allowed when the static container is configured; runtime construction of the item's raw controls is not allowed.

## Report These Items

Always report:

- generated prefabs
- source/generated prefab classification and owning source/generator
- generated or moved assets
- unsupported CSS features
- CSS visuals rasterized to PNG
- automatically generated or renamed nodes
- missing source images
- nodes with inferred component types
- suspected nine-slice assets without confirmed slice data
- repeated groups promoted to item prefabs
- item prefabs not statically referenced because they belong to ScrollView
- common prefabs extracted and which prefabs reference them
- static prefab validator result and Unity batchmode result or skip reason
- layout quality gate result, thresholds, and worst element deltas
- screenshot or overlay/diff result when available, or skip reason
- asset and script GUID dependencies
- skipped validation checks and why they were skipped
- questions that need human confirmation
- remaining manual checks needed inside Unity
- any mismatch between screenshots and source-backed prototype logic or browser measurements

## Stop Conditions

Stop and ask the user before destructive or ambiguous work when:

- project rules conflict
- TexturePacker is missing
- Unity project root or Unity version cannot be identified and the user has not approved continuing with higher risk
- HTML design size is missing and cannot be inferred safely
- UI element evidence is missing for a material prefab/resource change
- a prefab is generated but its owning source/tool/input cannot be identified
- the target prefab exists but the user did not ask to regenerate it
- naming or item extraction would create unstable business-facing references
- required art assets are missing
- a proposed solution requires modifying any project path containing `MiniGameKit` without explicit approval for the exact files
