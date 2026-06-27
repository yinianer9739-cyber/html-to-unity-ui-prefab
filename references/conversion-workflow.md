# Conversion Workflow

## Project Rule Gate

Before any Unity edit:

1. Read the workspace `AGENTS.md`.
2. Follow triggered detail docs, especially UI module, resource, C# performance, logging, and verification rules.
3. Check whether `SubDoc/` exists beside `Docs/`; if it exists, read every `.md` directly under it.
4. If child-branch rules conflict with main rules, stop and ask the user which rule to follow.

## HTML/CSS Intake

Use the HTML as an input artifact, not as a final truth source. Render it with a browser engine and collect:

- viewport width and height
- DOM tree order
- `getBoundingClientRect()` for each visible node
- computed styles for position, display, width, height, color, font, background, overflow, transform, opacity, z-index
- image source URLs and natural image sizes
- text content after rendering

Do not hand-calculate flex, margin collapse, text metrics, or transforms from source CSS when browser-computed values are available.

## Supported CSS Bias

Try to support:

- `position`, `left`, `top`, `right`, `bottom`
- `width`, `height`, `margin`, `padding`
- `display: flex`
- `font-size`, `color`, `text-align`, `line-height`
- `background-image`, `background-color`
- `border-radius` when it can be rasterized or represented safely
- `overflow: scroll` and `overflow: auto`
- `transform: scale(...)` and `transform: translate(...)`

Do not force support for:

- CSS filter
- mask
- clip-path
- box-shadow
- gradients
- complex CSS grid
- pseudo-elements
- animations

Rasterize unsupported decorative CSS only when it is visually necessary and report the rasterization.

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

Apply the same scale to:

- node width
- node height
- centered x position
- centered y position
- font size unless the user requests exact pixel text

Do not use a separate height scale for y positions. The project is fixed-width and adaptive-height, so height changes should be handled by anchors, ScrollView, or root viewport behavior.

Coordinate conversion:

1. Use the rendered viewport center as `(0, 0)`.
2. Convert each node center from browser top-left coordinates into centered coordinates.
3. Multiply centered coordinates by `scale`.
4. Use centered anchors by default.
5. Use top, bottom, left, right, or stretch anchors only when the HTML semantics or `data-ui-anchor` clearly requires it.

## Stacking And Hierarchy

Use computed `z-index` first. For equal `z-index`, preserve DOM order. Later Unity siblings render above earlier siblings.

Preserve logical groups when they help readability or later binding. Do not flatten everything into one layer unless the HTML is already flat and no grouping is useful.

`position: fixed` maps relative to the prefab root. `position: absolute` maps relative to the nearest positioned ancestor. Normal flow nodes use browser-computed bounds.

## Assets

Split images by source size:

- Any side greater than `300` goes to `Assets/Resources/tex/`.
- Small sprites are grouped by interface/module source folder, such as `publish_xxx/art/Z-main@主界面`.
- Small sprite names use module prefix and function suffix, such as `main@confirm_button`.

For CSS-drawn visuals that are necessary for the UI, rasterize to PNG first, then apply the same split rules.

Build atlases with the project menu tool `Atlas/打包单个文件夹图集`. Source sprites are expected under `Resources/ui_source/` after atlas processing.

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

When creating a matching `UIXXXView.cs`, follow the `UIStartView.cs` registration pattern: subclass `UIView`, provide static `RegisterView()`, create `UIViewInfo`, set `viewName`, `canvasType`, `viewType`, and call `UIManager.Instance.RegisterView(info)`.

If the prefab already exists, delete and recreate it only when the user asked to regenerate the view. Attach `UIXXXView.cs` if a matching MonoBehaviour exists.

Root node:

- full stretch anchors
- full parent size
- no business logic

Use native UGUI components by default:

- WebglInput for input fields
- ScrollView for scrolling regions
- project font at `Assets/Resources/font/normal` for Text
- Image for atlas sprites and pure color blocks
- RawImage for large textures

For Text, set text content, font size, color, alignment, and RectTransform size so text is not clipped.

## Item Prefabs

Create `UIXXXItem.prefab` under `Assets/Resources/ui/` for repeated or complex groups:

- repeated 3 or more times
- list rows
- backpack cells
- reward cells
- repeated composite UI blocks

If the item belongs to a ScrollView, do not place it as a static View reference. For other cases, ask whether the item should be statically placed in the View.

