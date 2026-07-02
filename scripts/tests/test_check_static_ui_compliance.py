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

START_VIEW_WITH_MASK_FULL = """%YAML 1.1
%TAG !u! tag:unity3d.com,2011:
--- !u!1 &1000
GameObject:
  m_Component:
  - component: {fileID: 1100}
  m_Name: UIStartView
--- !u!224 &1100
RectTransform:
  m_GameObject: {fileID: 1000}
  m_Father: {fileID: 0}
--- !u!1 &2000
GameObject:
  m_Component:
  - component: {fileID: 2100}
  m_Name: mask
--- !u!114 &2100
MonoBehaviour:
  m_GameObject: {fileID: 2000}
  m_Script: {fileID: 11500000, guid: 11111111111111111111111111111111, type: 3}
--- !u!1 &3000
GameObject:
  m_Name: view
"""

VIEW_WITH_MASK_WITHOUT_FULL = """%YAML 1.1
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
  m_Name: mask
--- !u!1 &3000
GameObject:
  m_Name: view
"""

VIEW_WITH_MASK_FULL = """%YAML 1.1
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
  m_Component:
  - component: {fileID: 2100}
  m_Name: mask
--- !u!114 &2100
MonoBehaviour:
  m_GameObject: {fileID: 2000}
  m_Script: {fileID: 11500000, guid: 11111111111111111111111111111111, type: 3}
--- !u!1 &3000
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

    def test_view_prefab_missing_mask_full_script_is_error(self):
        root = self.make_project()
        ui_dir = root / "Assets" / "Resources" / "ui"
        (ui_dir / "UIStartView.prefab").write_text(START_VIEW_WITH_MASK_FULL, encoding="utf-8")
        (ui_dir / "UIMainView.prefab").write_text(VIEW_WITH_MASK_WITHOUT_FULL, encoding="utf-8")
        report = scanner.scan_project(root)
        self.assertTrue(any("mask is missing UIStartView Full script" in item for item in report.errors))

    def test_view_prefab_with_mask_full_script_passes(self):
        root = self.make_project()
        ui_dir = root / "Assets" / "Resources" / "ui"
        (ui_dir / "UIStartView.prefab").write_text(START_VIEW_WITH_MASK_FULL, encoding="utf-8")
        (ui_dir / "UIMainView.prefab").write_text(VIEW_WITH_MASK_FULL, encoding="utf-8")
        report = scanner.scan_project(root)
        self.assertEqual([], report.errors)

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

    def test_direct_resources_load_is_error(self):
        root = self.make_project()
        (root / "Assets" / "Scripts" / "Runtime" / "UIView.cs").parent.mkdir(parents=True)
        (root / "Assets" / "Scripts" / "Runtime" / "UIView.cs").write_text(
            'var prefab = Resources.Load<GameObject>("ui/UIPlayerProfileAvatarSlot");',
            encoding="utf-8",
        )
        report = scanner.scan_project(root)
        self.assertTrue(any("direct Resources.Load usage is not allowed" in item for item in report.errors))

    def test_config_text_asset_resources_load_is_allowed(self):
        root = self.make_project()
        (root / "Assets" / "Scripts" / "Runtime" / "ConfigLoader.cs").parent.mkdir(parents=True)
        (root / "Assets" / "Scripts" / "Runtime" / "ConfigLoader.cs").write_text(
            'var config = Resources.Load<TextAsset>("config/ConfigMainEntry");',
            encoding="utf-8",
        )
        report = scanner.scan_project(root)
        self.assertFalse(any("direct Resources.Load usage is not allowed" in item for item in report.errors))

    def test_config_resources_load_does_not_hide_non_config_load(self):
        root = self.make_project()
        (root / "Assets" / "Scripts" / "Runtime" / "ConfigLoader.cs").parent.mkdir(parents=True)
        (root / "Assets" / "Scripts" / "Runtime" / "ConfigLoader.cs").write_text(
            '\n'.join(
                [
                    'var config = Resources.Load<TextAsset>("config/ConfigMainEntry");',
                    'var prefab = Resources.Load<GameObject>("ui/UIPlayerProfileAvatarSlot");',
                ]
            ),
            encoding="utf-8",
        )
        report = scanner.scan_project(root)
        self.assertTrue(any("direct Resources.Load usage is not allowed" in item for item in report.errors))

    def test_asset_manager_usage_is_not_resources_load_error(self):
        root = self.make_project()
        (root / "Assets" / "Scripts" / "Runtime" / "UIView.cs").parent.mkdir(parents=True)
        (root / "Assets" / "Scripts" / "Runtime" / "UIView.cs").write_text(
            'var prefab = AssetManager.Instance.LoadPrefab("UIPlayerProfileAvatarSlot");',
            encoding="utf-8",
        )
        report = scanner.scan_project(root)
        self.assertFalse(any("direct Resources.Load usage is not allowed" in item for item in report.errors))


if __name__ == "__main__":
    unittest.main()
