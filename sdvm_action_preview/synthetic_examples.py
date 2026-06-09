"""Synthetic public-safe evidence fixtures for preview demonstration."""

from __future__ import annotations

from pathlib import Path

SYNTHETIC_EXAMPLE_NAMES = ("healthy", "partial_evidence", "pre_post_delta_skeleton")

_EXAMPLES: dict[str, str] = {
    "healthy": """\
{"run_id": "synthetic:demo_run_001", "ts": "2026-01-15T10:00:01Z", "actor": "planner", "event_type": "step", "payload": {"note": "synthetic preview fixture"}}
{"run_id": "synthetic:demo_run_001", "ts": "2026-01-15T10:00:02Z", "actor": "planner", "event_type": "turn", "payload": {"note": "synthetic preview fixture"}}
{"run_id": "synthetic:demo_run_001", "ts": "2026-01-15T10:00:03Z", "actor": "tool_runner", "event_type": "tool_call", "payload": {"target": "tool.lookup", "note": "synthetic preview fixture"}}
{"run_id": "synthetic:demo_run_001", "ts": "2026-01-15T10:00:04Z", "actor": "tool_runner", "event_type": "tool_result", "payload": {"note": "synthetic preview fixture"}}
{"run_id": "synthetic:demo_run_001", "ts": "2026-01-15T10:00:05Z", "actor": "planner", "event_type": "turn", "payload": {"note": "synthetic preview fixture"}}
""",
    "partial_evidence": """\
{"run_id": "synthetic:sparse_run_001", "ts": "2026-01-15T11:00:01Z", "actor": "agent", "event_type": "step", "payload": {"note": "synthetic sparse fixture"}}
{"broken_line_not_json
""",
    "pre_post_delta_skeleton": """\
{"run_id": "synthetic:workflow_pre_001", "ts": "2026-01-15T12:00:01Z", "actor": "agent", "event_type": "step", "payload": {"stage": "PRE", "note": "synthetic PRE fixture"}}
{"run_id": "synthetic:workflow_pre_001", "ts": "2026-01-15T12:00:02Z", "actor": "agent", "event_type": "turn", "payload": {"stage": "PRE", "note": "synthetic PRE fixture"}}
{"run_id": "synthetic:workflow_post_001", "ts": "2026-01-15T12:10:01Z", "actor": "agent", "event_type": "step", "payload": {"stage": "POST", "note": "synthetic POST fixture"}}
{"run_id": "synthetic:workflow_post_001", "ts": "2026-01-15T12:10:02Z", "actor": "agent", "event_type": "turn", "payload": {"stage": "POST", "note": "synthetic POST fixture"}}
{"run_id": "synthetic:workflow_delta_001", "ts": "2026-01-15T12:20:01Z", "actor": "reviewer", "event_type": "step", "payload": {"stage": "DELTA", "note": "synthetic DELTA skeleton"}}
""",
}


def example_names() -> tuple[str, ...]:
    return SYNTHETIC_EXAMPLE_NAMES


def example_content(name: str) -> str:
    if name not in _EXAMPLES:
        raise KeyError(f"Unknown synthetic example: {name}")
    return _EXAMPLES[name]


def write_example(name: str, dest_dir: Path) -> Path:
    dest_dir.mkdir(parents=True, exist_ok=True)
    path = dest_dir / "canonical.jsonl"
    path.write_text(example_content(name), encoding="utf-8", newline="\n")
    return path


def materialize_repo_examples(repo_root: Path) -> list[Path]:
    """Write bundled synthetic examples under examples/synthetic/."""
    written: list[Path] = []
    base = repo_root / "examples" / "synthetic"
    for name in SYNTHETIC_EXAMPLE_NAMES:
        written.append(write_example(name, base / name))
    return written
