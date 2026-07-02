from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import argparse
import re

UI_COMPONENTS = (
    "Image",
    "RawImage",
    "Text",
    "Button",
    "Toggle",
    "Slider",
    "ScrollRect",
    "GridLayoutGroup",
    "HorizontalLayoutGroup",
    "VerticalLayoutGroup",
    "LayoutGroup",
)

FORBIDDEN_ROOT_COMPONENT_TYPES = {
    "CanvasRenderer",
    "Image",
    "RawImage",
    "Text",
    "Button",
    "Toggle",
    "Slider",
    "ScrollRect",
    "GridLayoutGroup",
    "HorizontalLayoutGroup",
    "VerticalLayoutGroup",
    "LayoutGroup",
}

OBJECT_HEADER_RE = re.compile(r"^--- !u!(?P<class_id>\d+) &(?P<file_id>-?\d+)", re.MULTILINE)
NAME_RE = re.compile(r"^\s*m_Name:\s*(?P<name>.*)$", re.MULTILINE)
GAME_OBJECT_RE = re.compile(r"^\s*GameObject:\s*$", re.MULTILINE)
GAME_OBJECT_REF_RE = re.compile(r"m_GameObject:\s*\{fileID:\s*(?P<file_id>-?\d+)\}")
SCRIPT_GUID_RE = re.compile(r"m_Script:\s*\{fileID:\s*11500000,\s*guid:\s*(?P<guid>[0-9a-fA-F]{32}),\s*type:\s*3\}")
RESOURCES_LOAD_CALL_RE = re.compile(r"\bResources\.Load\s*(?:<[^>]*>)?\s*\(", re.IGNORECASE)
RESOURCES_LOAD_LITERAL_RE = re.compile(
    r'\bResources\.Load\s*(?:<[^>]*>)?\s*\(\s*[$@]{0,2}"(?P<path>(?:[^"\\]|\\.)*)"',
    re.IGNORECASE,
)


@dataclass
class ComplianceReport:
    root: Path
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors


def _is_ascii_name(value: str) -> bool:
    return all(ord(ch) < 128 for ch in value)


def _parse_objects(text: str) -> list[tuple[str, str, str]]:
    matches = list(OBJECT_HEADER_RE.finditer(text))
    objects: list[tuple[str, str, str]] = []
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        body = text[start:end]
        type_match = re.search(r"^\s*([A-Za-z0-9_]+):", body, re.MULTILINE)
        type_name = type_match.group(1) if type_match else ""
        objects.append((match.group("file_id"), type_name, body))
    return objects


def _game_object_name(body: str) -> str:
    match = NAME_RE.search(body)
    return match.group("name").strip() if match else ""


def _view_root_id(path: Path, objects: list[tuple[str, str, str]]) -> str | None:
    first_game_object: str | None = None
    for file_id, type_name, body in objects:
        if type_name != "GameObject":
            continue
        first_game_object = first_game_object or file_id
        if _game_object_name(body) == path.stem:
            return file_id
    return first_game_object


def _named_game_object_id(objects: list[tuple[str, str, str]], name: str) -> str | None:
    for file_id, type_name, body in objects:
        if type_name == "GameObject" and _game_object_name(body) == name:
            return file_id
    return None


def _mono_behaviour_script_guids_for_game_object(
    objects: list[tuple[str, str, str]], game_object_id: str | None
) -> set[str]:
    if not game_object_id:
        return set()

    guids: set[str] = set()
    for _, type_name, body in objects:
        if type_name != "MonoBehaviour":
            continue
        owner = GAME_OBJECT_REF_RE.search(body)
        if not owner or owner.group("file_id") != game_object_id:
            continue
        script = SCRIPT_GUID_RE.search(body)
        if script:
            guids.add(script.group("guid").lower())
    return guids


def _mask_mono_behaviour_script_guids(text: str) -> set[str]:
    objects = _parse_objects(text)
    mask_id = _named_game_object_id(objects, "mask")
    return _mono_behaviour_script_guids_for_game_object(objects, mask_id)


def _ui_start_mask_script_guids(root: Path) -> set[str]:
    start_prefab = root / "Assets" / "Resources" / "ui" / "UIStartView.prefab"
    if not start_prefab.exists():
        return set()
    text = start_prefab.read_text(encoding="utf-8", errors="ignore")
    return _mask_mono_behaviour_script_guids(text)


def _scan_prefab(path: Path, report: ComplianceReport, start_mask_script_guids: set[str]) -> None:
    text = path.read_text(encoding="utf-8", errors="ignore")
    game_object_count = len(GAME_OBJECT_RE.findall(text))
    objects = _parse_objects(text)

    if path.stem.startswith("UI") and path.stem.endswith("View") and game_object_count <= 1:
        report.errors.append(f"{path}: UI View prefab appears root-only")

    if path.stem.startswith("UI") and path.stem.endswith("View"):
        root_id = _view_root_id(path, objects)
        if root_id:
            for file_id, type_name, body in objects:
                if type_name not in FORBIDDEN_ROOT_COMPONENT_TYPES:
                    continue
                owner = GAME_OBJECT_REF_RE.search(body)
                if owner and owner.group("file_id") == root_id:
                    report.errors.append(
                        f"{path}: root contains visible or interactive component {type_name} ({file_id})"
                    )

        if path.stem != "UIStartView" and start_mask_script_guids:
            mask_id = _named_game_object_id(objects, "mask")
            actual_mask_script_guids = _mono_behaviour_script_guids_for_game_object(objects, mask_id)
            if not actual_mask_script_guids.intersection(start_mask_script_guids):
                report.errors.append(f"{path}: mask is missing UIStartView Full script")

    for match in NAME_RE.finditer(text):
        name = match.group("name").strip()
        if name and not _is_ascii_name(name):
            report.errors.append(f"{path}: GameObject name is not ASCII: {name}")


def _scan_code(path: Path, report: ComplianceReport) -> None:
    text = path.read_text(encoding="utf-8", errors="ignore")
    if "Resources.GetBuiltinResource<Font>" in text or "LegacyRuntime.ttf" in text or "Arial.ttf" in text:
        report.errors.append(f"{path}: runtime built-in font fallback is not allowed for product UI")

    for match in RESOURCES_LOAD_CALL_RE.finditer(text):
        literal_match = RESOURCES_LOAD_LITERAL_RE.match(text, match.start())
        if literal_match and literal_match.group("path").lower().startswith("config/"):
            continue
        report.errors.append(
            f"{path}: direct Resources.Load usage is not allowed outside Config; use AssetManager or ask before extending it"
        )
        break

    if "new GameObject" in text:
        for component in UI_COMPONENTS:
            if re.search(rf"\.AddComponent\s*<\s*{component}\s*>", text):
                report.errors.append(f"{path}: runtime construction of raw UI control {component} is not allowed")

    if "SetSprite(" in text or "SetFlatBackground(" in text:
        report.warnings.append(f"{path}: runtime visual repair helper usage must not replace prefab defaults")
    if re.search(r"\.\s*sprite\s*=", text) or re.search(r"\.\s*color\s*=", text):
        report.warnings.append(f"{path}: direct runtime sprite/color assignment must be dynamic state binding, not default visual repair")


def scan_project(project_root: str | Path) -> ComplianceReport:
    root = Path(project_root)
    report = ComplianceReport(root)

    if not root.exists():
        report.errors.append(f"Project root does not exist: {root}")
        return report

    assets = root / "Assets"
    if not assets.exists():
        report.errors.append(f"Assets directory does not exist under project root: {root}")
        return report

    start_mask_script_guids = _ui_start_mask_script_guids(root)
    for prefab in assets.rglob("*.prefab"):
        _scan_prefab(prefab, report, start_mask_script_guids)

    for script in assets.rglob("*.cs"):
        _scan_code(script, report)

    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Static UI compliance scanner for generated Unity UI prefabs and View code.")
    parser.add_argument("project_root", help="Unity project root")
    args = parser.parse_args(argv)

    report = scan_project(args.project_root)
    for item in report.errors:
        print(f"ERROR: {item}")
    for item in report.warnings:
        print(f"WARNING: {item}")
    if report.ok:
        print(f"OK: {report.root}")
    return 0 if report.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
