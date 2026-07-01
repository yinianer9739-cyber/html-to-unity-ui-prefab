import tempfile
import unittest
from pathlib import Path

import check_static_ui_compliance as scanner


VALID_PREFAB = """%YAML 1.1
%TAG !u! tag:unity3d.com,2011:
--- !u!1 &1000
GameObject:
  m_Component:
  - component: {fileID: 1100}
  m_Name: UIMainView
--- !u!224 &1100
RectTransform:
  m_GameObject: {fileID: 1000}
  m_Father: {fileID: 0}
--- !u!1 &2000
GameObject:
  m_Name: view
"""


class StaticUiComplianceTests(unittest.TestCase):
    def make_project(self):
        root = Path(tempfile.mkdtemp())
        (root / "Assets" / "Resources" / "ui").mkdir(parents=True)
        (root / "Assets" / "Scripts").mkdir(parents=True)
        return root

    def test_valid_view_prefab_passes(self):
        root = self.make_project()
        (root / "Assets" / "Resources" / "ui" / "UIMainView.prefab").write_text(VALID_PREFAB, encoding="utf-8")
        report = scanner.scan_project(root)
        self.assertEqual([], report.errors)

    def test_root_only_view_prefab_is_error(self):
        root = self.make_project()
        (root / "Assets" / "Resources" / "ui" / "UIMainView.prefab").write_text(
            "%YAML 1.1\n--- !u!1 &1000\nGameObject:\n  m_Name: UIMainView\n",
            encoding="utf-8",
        )
        report = scanner.scan_project(root)
        self.assertTrue(any("root-only" in item for item in report.errors))

    def test_root_canvas_renderer_is_error(self):
        root = self.make_project()
        prefab = VALID_PREFAB + """--- !u!222 &3000
CanvasRenderer:
  m_GameObject: {fileID: 1000}
"""
        (root / "Assets" / "Resources" / "ui" / "UIMainView.prefab").write_text(prefab, encoding="utf-8")
        report = scanner.scan_project(root)
        self.assertTrue(any("root contains visible or interactive component" in item for item in report.errors))

    def test_builtin_font_fallback_is_error(self):
        root = self.make_project()
        (root / "Assets" / "Scripts" / "UIView.cs").write_text(
            'var f = Resources.GetBuiltinResource<Font>("Arial.ttf");',
            encoding="utf-8",
        )
        report = scanner.scan_project(root)
        self.assertTrue(any("built-in font fallback" in item for item in report.errors))

    def test_runtime_raw_ui_construction_is_error(self):
        root = self.make_project()
        (root / "Assets" / "Scripts" / "UIView.cs").write_text(
            "var go = new GameObject(); go.AddComponent<Image>();",
            encoding="utf-8",
        )
        report = scanner.scan_project(root)
        self.assertTrue(any("runtime construction" in item for item in report.errors))


if __name__ == "__main__":
    unittest.main()
