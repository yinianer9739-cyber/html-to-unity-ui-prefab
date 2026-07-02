import json
import codecs
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import compare_layout_quality as quality


def write_json(data):
    root = tempfile.mkdtemp()
    path = os.path.join(root, "quality.json")
    with codecs.open(path, "w", "utf-8") as handle:
        handle.write(json.dumps(data))
    return path


class LayoutQualityTests(unittest.TestCase):
    def test_matching_rects_pass(self):
        source = write_json(
            {
                "elements": [
                    {
                        "id": "bt_start",
                        "html_rect": {"x": 100, "y": 50, "width": 200, "height": 80},
                        "unity_rect": {"x": 101, "y": 52, "width": 201, "height": 79},
                        "asset_status": "source",
                        "style_status": "supported",
                    }
                ]
            }
        )
        report = quality.evaluate_quality(source)
        self.assertEqual([], report["errors"])

    def test_large_position_delta_fails(self):
        source = write_json(
            {
                "elements": [
                    {
                        "id": "panel",
                        "html_rect": {"x": 0, "y": 0, "width": 300, "height": 100},
                        "unity_rect": {"x": 12, "y": 0, "width": 300, "height": 100},
                    }
                ]
            }
        )
        report = quality.evaluate_quality(source, max_position_delta=4)
        self.assertTrue(any("position delta" in item for item in report["errors"]))

    def test_missing_visual_evidence_fails_for_required_element(self):
        source = write_json(
            {
                "elements": [
                    {
                        "id": "reward_badge",
                        "html_rect": {"x": 0, "y": 0, "width": 80, "height": 32},
                        "unity_rect": {"x": 0, "y": 0, "width": 80, "height": 32},
                        "visual_required": True,
                        "asset_status": "missing",
                    }
                ]
            }
        )
        report = quality.evaluate_quality(source)
        self.assertTrue(any("missing visual evidence" in item for item in report["errors"]))


if __name__ == "__main__":
    unittest.main()
