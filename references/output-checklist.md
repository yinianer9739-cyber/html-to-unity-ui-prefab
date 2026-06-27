# Output Checklist

Before reporting completion, verify and summarize:

## Required Files

- `UIXXXView.prefab` created or regenerated under `Assets/Resources/ui/`.
- `UIXXXItem.prefab` files created for repeated or complex items when applicable.
- New Unity files have `.meta` files.
- Matching `UIXXXView.cs` was attached if it exists.

## Resource Checks

- TexturePacker was found before atlas work.
- Large images were placed under `Assets/Resources/tex/`.
- Small sprites were grouped and packed through the atlas workflow.
- Image and RawImage references resolve.
- Text font uses `Assets/Resources/font/normal`.

## Layout Checks

- Browser-computed layout was used.
- Uniform width scale was used.
- Generated View structure matches `UIStartView.prefab`: full-stretch root, `mask` as the background/mask layer with its FULL notch reverse-fill script preserved, and `view` as the content container.
- Default nodes use centered anchors unless edge anchoring was explicit.
- Text RectTransform sizes are large enough to avoid clipping.
- ScrollView content, viewport, and item template are sensible.
- Sibling order follows z-index then DOM order.

## Report These Items

Always report:

- generated prefabs
- generated or moved assets
- unsupported CSS features
- CSS visuals rasterized to PNG
- automatically generated or renamed nodes
- missing source images
- nodes with inferred component types
- suspected nine-slice assets without confirmed slice data
- repeated groups promoted to item prefabs
- item prefabs not statically referenced because they belong to ScrollView
- questions that need human confirmation

## Stop Conditions

Stop and ask the user before destructive or ambiguous work when:

- project rules conflict
- TexturePacker is missing
- HTML design size is missing and cannot be inferred safely
- the target prefab exists but the user did not ask to regenerate it
- naming or item extraction would create unstable business-facing references
- required art assets are missing

