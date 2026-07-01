import tempfile
import unittest
from pathlib import Path

import validate_unity_prefab as validator


VALID_PREFAB = """%YAML 1.1
%TAG !u! tag:unity3d.com,2011:
--- !u!1 &1000
GameObject:
  m_Component:
  - component: {fileID: 2000}
  m_Name: Root
--- !u!4 &2000
Transform:
  m_GameObject: {fileID: 1000}
  m_Father: {fileID: 0}
  m_Children: []
"""


class ValidatorTests(unittest.TestCase):
    def write_prefab(self, text):
        root = Path(tempfile.mkdtemp())
        prefab = root / "Assets" / "Generated" / "Widget.prefab"
        prefab.parent.mkdir(parents=True)
        prefab.write_text(text, encoding="utf-8")
        return root, prefab

    def test_valid_minimal_prefab_has_no_errors(self):
        project, prefab = self.write_prefab(VALID_PREFAB)
        report = validator.validate_prefab(prefab, project)
        self.assertEqual([], report.errors)

    def test_duplicate_file_id_is_error(self):
        project, prefab = self.write_prefab(VALID_PREFAB + "--- !u!1 &1000\nGameObject: {}\n")
        report = validator.validate_prefab(prefab, project)
        self.assertTrue(any("Duplicate fileID 1000" in item for item in report.errors))

    def test_missing_component_target_is_error(self):
        text = VALID_PREFAB.replace("{fileID: 2000}", "{fileID: 9999}")
        project, prefab = self.write_prefab(text)
        report = validator.validate_prefab(prefab, project)
        self.assertTrue(any("dangling local fileID 9999" in item for item in report.errors))

    def test_external_guid_without_meta_is_warning(self):
        text = VALID_PREFAB + "  m_Material: {fileID: 2100000, guid: 0123456789abcdef0123456789abcdef, type: 2}\n"
        project, prefab = self.write_prefab(text)
        report = validator.validate_prefab(prefab, project)
        self.assertTrue(any("0123456789abcdef0123456789abcdef" in item for item in report.warnings))


if __name__ == "__main__":
    unittest.main()
