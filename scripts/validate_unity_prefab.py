from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import argparse
import re

OBJECT_HEADER_RE = re.compile(r"^--- !u!(?P<class_id>\d+) &(?P<file_id>-?\d+)", re.MULTILINE)
REF_BLOCK_RE = re.compile(r"\{(?P<body>[^{}]*fileID:\s*(?P<file_id>-?\d+)[^{}]*)\}")
GUID_RE = re.compile(r"guid:\s*(?P<guid>[0-9a-fA-F]{32})")
GAME_OBJECT_COMPONENT_RE = re.compile(r"component:\s*\{fileID:\s*(?P<file_id>-?\d+)\}")
TRANSFORM_PARENT_RE = re.compile(r"m_Father:\s*\{fileID:\s*(?P<file_id>-?\d+)\}")
TRANSFORM_CHILD_RE = re.compile(r"- \{fileID:\s*(?P<file_id>-?\d+)\}")


@dataclass
class UnityObject:
    class_id: str
    file_id: str
    type_name: str
    body: str


@dataclass
class ValidationReport:
    path: Path
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors


def parse_objects(text: str) -> list[UnityObject]:
    matches = list(OBJECT_HEADER_RE.finditer(text))
    objects: list[UnityObject] = []
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        body = text[start:end]
        type_match = re.search(r"^\s*([A-Za-z0-9_]+):", body, re.MULTILINE)
        objects.append(
            UnityObject(
                class_id=match.group("class_id"),
                file_id=match.group("file_id"),
                type_name=type_match.group(1) if type_match else "",
                body=body,
            )
        )
    return objects


def find_meta_for_guid(project_root: Path, guid: str) -> Path | None:
    for meta in project_root.rglob("*.meta"):
        try:
            if f"guid: {guid}" in meta.read_text(encoding="utf-8", errors="ignore"):
                return meta
        except OSError:
            continue
    return None


def _default_project_root(path: Path) -> Path:
    assets_parent = next((parent for parent in path.parents if parent.name == "Assets"), None)
    if assets_parent and assets_parent.parent:
        return assets_parent.parent
    return path.parent


def _local_reference_ids(body: str) -> list[str]:
    file_ids: list[str] = []
    for match in REF_BLOCK_RE.finditer(body):
        if "guid:" in match.group("body"):
            continue
        file_ids.append(match.group("file_id"))
    return file_ids


def validate_prefab(prefab_path: str | Path, project_root: str | Path | None = None) -> ValidationReport:
    path = Path(prefab_path)
    root = Path(project_root) if project_root else _default_project_root(path)
    report = ValidationReport(path)

    if not path.exists():
        report.errors.append(f"Prefab does not exist: {path}")
        return report

    text = path.read_text(encoding="utf-8", errors="ignore")
    objects = parse_objects(text)

    if not text.startswith("%YAML"):
        report.warnings.append("File does not start with Unity YAML header")
    if not objects:
        report.errors.append("No Unity object blocks found")
        return report

    by_file_id: dict[str, UnityObject] = {}
    for obj in objects:
        if obj.file_id in by_file_id:
            report.errors.append(f"Duplicate fileID {obj.file_id}")
        by_file_id[obj.file_id] = obj

    if not any(obj.type_name == "GameObject" for obj in objects):
        report.errors.append("No GameObject object found")
    if not any(obj.type_name in {"Transform", "RectTransform"} for obj in objects):
        report.errors.append("No Transform or RectTransform object found")

    for obj in objects:
        for file_id in _local_reference_ids(obj.body):
            if file_id != "0" and file_id not in by_file_id:
                report.errors.append(f"{obj.type_name or 'Object'} {obj.file_id} has dangling local fileID {file_id}")

    for obj in objects:
        if obj.type_name == "GameObject":
            for ref in GAME_OBJECT_COMPONENT_RE.finditer(obj.body):
                file_id = ref.group("file_id")
                target = by_file_id.get(file_id)
                if target and f"m_GameObject: {{fileID: {obj.file_id}}}" not in target.body:
                    report.warnings.append(
                        f"Component {file_id} is listed on GameObject {obj.file_id} but does not point back with m_GameObject"
                    )

        if obj.type_name in {"Transform", "RectTransform"}:
            known_file_ids = {"0", *by_file_id.keys()}
            parent = TRANSFORM_PARENT_RE.search(obj.body)
            if parent and parent.group("file_id") not in known_file_ids:
                report.errors.append(f"{obj.type_name} {obj.file_id} has missing parent fileID {parent.group('file_id')}")
            for child in TRANSFORM_CHILD_RE.finditer(obj.body):
                file_id = child.group("file_id")
                if file_id not in known_file_ids:
                    report.errors.append(f"{obj.type_name} {obj.file_id} has missing child fileID {file_id}")

    for guid in sorted(set(match.group("guid").lower() for match in GUID_RE.finditer(text))):
        if not find_meta_for_guid(root, guid):
            report.warnings.append(f"GUID {guid} was referenced, but no matching .meta file was found under {root}")

    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Static validator for Unity .prefab files.")
    parser.add_argument("prefab", help="Path to a .prefab file")
    parser.add_argument("--project-root", help="Unity project root used to search .meta files")
    args = parser.parse_args(argv)

    report = validate_prefab(args.prefab, args.project_root)
    for item in report.errors:
        print(f"ERROR: {item}")
    for item in report.warnings:
        print(f"WARNING: {item}")
    if report.ok:
        print(f"OK: {report.path}")
    return 0 if report.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
