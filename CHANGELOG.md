# Changelog

## 0.4.1

- Preserve the `UIStartView` mask Full script requirement for generated View prefabs.
- Treat direct non-Config `Resources.Load(...)` calls as static compliance errors.
- Keep Config assets under `Resources/config/` exempt from the AssetManager-only resource rule.
- Add scanner tests for mask Full script preservation, non-Config resource loading errors, Config load exceptions, and mixed Config/non-Config loading.
- Update README, skill docs, workflow notes, and output checklist for the 0.4.1 loading boundary.

## 0.4.0

- Add a required layout quality gate for HTML-to-UGUI conversion completion.
- Add `scripts/compare_layout_quality.py` to compare browser-measured HTML rects with generated Unity rects, visual evidence, and style support.
- Add tests for the layout quality comparison helper.
- Update the conversion workflow and completion checklist to require rect comparison, visual/style evidence, and screenshot or overlay/diff reporting when practical.
- Add `scripts/package-release.ps1` for release zip generation from `VERSION`.
