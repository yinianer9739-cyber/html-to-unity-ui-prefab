# Changelog

## 0.4.1

- Preserve `UIStartView` mask Full script requirements when generating new View prefabs.
- Block direct non-Config `Resources.Load(...)` calls in runtime and business code.
- Keep `Resources/config/` Config loads exempt from the AssetManager-only resource rule.
- Add static scanner coverage for Config `Resources.Load` exceptions and mixed Config/non-Config loads.
- Update English and Chinese skill docs, workflow notes, checklist, and README for the Config exception.

## 0.4.0

- Add a required layout quality gate for HTML-to-UGUI conversion completion.
- Add `scripts/compare_layout_quality.py` to compare browser-measured HTML rects with generated Unity rects, visual evidence, and style support.
- Add tests for the layout quality comparison helper.
- Update the conversion workflow and completion checklist to require rect comparison, visual/style evidence, and screenshot or overlay/diff reporting when practical.
- Add `scripts/package-release.ps1` for release zip generation from `VERSION`.
