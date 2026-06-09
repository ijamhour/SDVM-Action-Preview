"""Public-safe canonical JSONL evidence validation."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

REQUIRED_EVENT_FIELDS = ("run_id", "ts", "actor", "event_type")

# Public-safe stage markers scanned in run_id and nested payload text.
_STAGE_MARKERS = {
    "pre": ("pre", ":pre", "_pre", "stage_pre"),
    "post": ("post", ":post", "_post", "stage_post"),
    "delta": ("delta", ":delta", "_delta", "stage_delta"),
}


@dataclass
class LineIssue:
    line_number: int
    message: str


@dataclass
class ParsedEvent:
    line_number: int
    run_id: str
    ts: str
    actor: str
    event_type: str
    raw: dict[str, Any]


@dataclass
class ValidationResult:
    input_path: Path
    total_lines: int = 0
    valid_events: list[ParsedEvent] = field(default_factory=list)
    line_issues: list[LineIssue] = field(default_factory=list)
    run_ids: set[str] = field(default_factory=set)
    event_types: set[str] = field(default_factory=set)
    actors: set[str] = field(default_factory=set)
    stage_hits: dict[str, bool] = field(
        default_factory=lambda: {"pre": False, "post": False, "delta": False}
    )

    @property
    def valid_count(self) -> int:
        return len(self.valid_events)

    @property
    def parse_success_ratio(self) -> float:
        if self.total_lines == 0:
            return 0.0
        return self.valid_count / self.total_lines


def resolve_evidence_path(path: Path) -> Path:
    """Resolve a JSONL file or directory containing canonical.jsonl."""
    resolved = path.resolve()
    if resolved.is_file():
        return resolved
    if resolved.is_dir():
        candidate = resolved / "canonical.jsonl"
        if candidate.is_file():
            return candidate
        raise FileNotFoundError(f"No canonical.jsonl found in directory: {resolved}")
    raise FileNotFoundError(f"Evidence path not found: {resolved}")


def _scan_stage_markers(text: str) -> set[str]:
    lowered = text.lower()
    hits: set[str] = set()
    for stage, markers in _STAGE_MARKERS.items():
        if any(marker in lowered for marker in markers):
            hits.add(stage)
    return hits


def _extract_stage_hits(obj: Any) -> set[str]:
    hits: set[str] = set()
    if isinstance(obj, dict):
        for key, value in obj.items():
            hits |= _scan_stage_markers(str(key))
            hits |= _extract_stage_hits(value)
    elif isinstance(obj, list):
        for item in obj:
            hits |= _extract_stage_hits(item)
    elif obj is not None:
        hits |= _scan_stage_markers(str(obj))
    return hits


def _validate_event_fields(data: dict[str, Any], line_number: int) -> ParsedEvent | LineIssue:
    missing = [name for name in REQUIRED_EVENT_FIELDS if not data.get(name)]
    if missing:
        return LineIssue(line_number, f"Missing required fields: {', '.join(missing)}")
    return ParsedEvent(
        line_number=line_number,
        run_id=str(data["run_id"]),
        ts=str(data["ts"]),
        actor=str(data["actor"]),
        event_type=str(data["event_type"]),
        raw=data,
    )


def validate_evidence(path: Path) -> ValidationResult:
    """Validate canonical JSONL evidence using public-safe structural checks."""
    evidence_path = resolve_evidence_path(path)
    result = ValidationResult(input_path=evidence_path)

    text = evidence_path.read_text(encoding="utf-8")
    lines = text.splitlines()
    result.total_lines = len([line for line in lines if line.strip()])

    for line_number, line in enumerate(lines, start=1):
        stripped = line.strip()
        if not stripped:
            continue
        try:
            data = json.loads(stripped)
        except json.JSONDecodeError as exc:
            result.line_issues.append(LineIssue(line_number, f"Invalid JSON: {exc.msg}"))
            continue
        if not isinstance(data, dict):
            result.line_issues.append(LineIssue(line_number, "Line is not a JSON object"))
            continue

        parsed = _validate_event_fields(data, line_number)
        if isinstance(parsed, LineIssue):
            result.line_issues.append(parsed)
            continue

        result.valid_events.append(parsed)
        result.run_ids.add(parsed.run_id)
        result.event_types.add(parsed.event_type)
        result.actors.add(parsed.actor)

        for stage in _extract_stage_hits(data):
            result.stage_hits[stage] = True

    return result
