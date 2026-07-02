# Changelog

## 0.4.0

- Add a required layout quality gate for HTML-to-UGUI conversion completion.
- Add `scripts/compare_layout_quality.py` to compare browser-measured HTML rects with generated Unity rects, visual evidence, and style support.
- Add tests for the layout quality comparison helper.
- Update the conversion workflow and completion checklist to require rect comparison, visual/style evidence, and screenshot or overlay/diff reporting when practical.
- Add `scripts/package-release.ps1` for release zip generation from `VERSION`.
