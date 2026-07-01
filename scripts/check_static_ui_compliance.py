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


def _scan_prefab(path: Path, report: ComplianceReport) -> None:
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

    for match in NAME_RE.finditer(text):
        name = match.group("name").strip()
        if name and not _is_ascii_name(name):
            report.errors.append(f"{path}: GameObject name is not ASCII: {name}")


def _scan_code(path: Path, report: ComplianceReport) -> None:
    text = path.read_text(encoding="utf-8", errors="ignore")
    if "Resources.GetBuiltinResource<Font>" in text or "LegacyRuntime.ttf" in text or "Arial.ttf" in text:
        report.errors.append(f"{path}: runtime built-in font fallback is not allowed for product UI")

    if re.search(r"\bResources\.Load\s*<", text):
        report.warnings.append(f"{path}: direct Resources.Load usage must be justified by project rules")

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

    for prefab in assets.rglob("*.prefab"):
        _scan_prefab(prefab, report)

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
