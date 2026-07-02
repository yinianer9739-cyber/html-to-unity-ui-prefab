from __future__ import print_function

import argparse
import codecs
import json
import math
import sys


RECT_KEYS = ("x", "y", "width", "height")
BAD_VISUAL_STATUSES = set(["missing", "unknown", "inferred", "placeholder", "substitute"])
BAD_STYLE_STATUSES = set(["unsupported", "missing", "unknown", "inferred"])


def _read_json(path):
    with codecs.open(path, "r", "utf-8") as handle:
        return json.load(handle)


def _number(value, default=0.0):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _rect(data):
    return {key: _number((data or {}).get(key)) for key in RECT_KEYS}


def _element_id(element, index):
    return element.get("id") or element.get("name") or element.get("path") or "element_%d" % (index + 1)


def _position_delta(html_rect, unity_rect):
    return math.sqrt(
        math.pow(unity_rect["x"] - html_rect["x"], 2)
        + math.pow(unity_rect["y"] - html_rect["y"], 2)
    )


def _size_delta_percent(html_rect, unity_rect):
    html_width = max(abs(html_rect["width"]), 1.0)
    html_height = max(abs(html_rect["height"]), 1.0)
    width_percent = abs(unity_rect["width"] - html_rect["width"]) / html_width * 100.0
    height_percent = abs(unity_rect["height"] - html_rect["height"]) / html_height * 100.0
    return max(width_percent, height_percent)


def evaluate_quality(source, max_position_delta=4.0, max_size_delta_percent=2.0):
    data = _read_json(source)
    errors = []
    warnings = []
    rows = []

    elements = data.get("elements", [])
    if not elements:
        errors.append("No elements were provided for layout quality comparison")

    for index, element in enumerate(elements):
        item_id = _element_id(element, index)
        html_rect = _rect(element.get("html_rect"))
        unity_rect = _rect(element.get("unity_rect"))
        position_delta = _position_delta(html_rect, unity_rect)
        size_delta = _size_delta_percent(html_rect, unity_rect)

        row = {
            "id": item_id,
            "position_delta": round(position_delta, 3),
            "size_delta_percent": round(size_delta, 3),
            "asset_status": element.get("asset_status", "unknown"),
            "style_status": element.get("style_status", "unknown"),
        }
        rows.append(row)

        if position_delta > max_position_delta:
            errors.append(
                "%s position delta %.3f exceeds %.3f" % (item_id, position_delta, max_position_delta)
            )
        if size_delta > max_size_delta_percent:
            errors.append(
                "%s size delta %.3f%% exceeds %.3f%%" % (item_id, size_delta, max_size_delta_percent)
            )

        visual_required = bool(element.get("visual_required", False))
        asset_status = str(element.get("asset_status", "unknown")).lower()
        if visual_required and asset_status in BAD_VISUAL_STATUSES:
            errors.append("%s missing visual evidence: asset_status=%s" % (item_id, asset_status))
        elif asset_status in BAD_VISUAL_STATUSES:
            warnings.append("%s has weak visual evidence: asset_status=%s" % (item_id, asset_status))

        style_required = bool(element.get("style_required", False))
        style_status = str(element.get("style_status", "unknown")).lower()
        if style_required and style_status in BAD_STYLE_STATUSES:
            errors.append("%s missing style support: style_status=%s" % (item_id, style_status))
        elif style_status in BAD_STYLE_STATUSES:
            warnings.append("%s has weak style support: style_status=%s" % (item_id, style_status))

    return {
        "ok": not errors,
        "errors": errors,
        "warnings": warnings,
        "elements": rows,
        "thresholds": {
            "max_position_delta": max_position_delta,
            "max_size_delta_percent": max_size_delta_percent,
        },
    }


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Compare browser-measured HTML rects against generated Unity rects and visual evidence."
    )
    parser.add_argument("quality_json", help="JSON file containing elements with html_rect and unity_rect fields")
    parser.add_argument("--max-position-delta", type=float, default=4.0)
    parser.add_argument("--max-size-delta-percent", type=float, default=2.0)
    parser.add_argument("--json", action="store_true", help="Print the full JSON report")
    args = parser.parse_args(argv)

    report = evaluate_quality(
        args.quality_json,
        max_position_delta=args.max_position_delta,
        max_size_delta_percent=args.max_size_delta_percent,
    )

    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        for item in report["errors"]:
            print("ERROR: %s" % item)
        for item in report["warnings"]:
            print("WARNING: %s" % item)
        if report["ok"]:
            print("OK: %s" % args.quality_json)

    return 0 if report["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
