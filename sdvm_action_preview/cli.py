"""CLI entrypoint for the public-safe SDVM Action Preview slice."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from sdvm_action_preview.evidence_validator import ValidationResult, validate_evidence
from sdvm_action_preview.preview_report import (
    build_preview_report,
    render_json,
    render_markdown,
    write_preview_outputs,
)
from sdvm_action_preview.synthetic_examples import example_content, example_names, write_example

SUPPORTED_MODES = frozenset({"validate-only", "preview-report", "synthetic"})


def _write_validation_json(result: ValidationResult, out_dir: Path) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / "validation.json"
    payload = {
        "input_path": str(result.input_path),
        "total_lines": result.total_lines,
        "valid_events": result.valid_count,
        "line_issues": [{"line": issue.line_number, "message": issue.message} for issue in result.line_issues],
        "distinct_run_ids": sorted(result.run_ids),
        "distinct_event_types": sorted(result.event_types),
        "stage_hits": result.stage_hits,
    }
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    return path


def run_validate_only(input_path: Path, out_dir: Path) -> ValidationResult:
    result = validate_evidence(input_path)
    _write_validation_json(result, out_dir)
    return result


def run_preview_report(input_path: Path, out_dir: Path, *, run_label: str | None) -> Path:
    result = validate_evidence(input_path)
    _write_validation_json(result, out_dir)
    report = build_preview_report(result, run_label=run_label)
    md_path, _ = write_preview_outputs(report, out_dir)
    return md_path


def run_synthetic(example_name: str, out_dir: Path, *, run_label: str | None) -> Path:
    if example_name not in example_names():
        raise ValueError(f"Unknown synthetic example: {example_name}")
    tmp_dir = out_dir / "_synthetic_input"
    evidence_path = write_example(example_name, tmp_dir)
    return run_preview_report(evidence_path, out_dir, run_label=run_label or f"synthetic:{example_name}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="SDVM Action Preview (public-safe slice)")
    parser.add_argument("--input", help="Canonical JSONL file or directory")
    parser.add_argument("--output", help="Output directory or markdown file path")
    parser.add_argument(
        "--mode",
        choices=sorted(SUPPORTED_MODES),
        default="preview-report",
        help="validate-only | preview-report | synthetic",
    )
    parser.add_argument("--format", choices=("markdown",), default="markdown")
    parser.add_argument("--run-label", default=None, help="Optional label for the preview report")
    parser.add_argument(
        "--synthetic-example",
        default="healthy",
        help="Synthetic example name when --mode synthetic",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.mode == "synthetic":
        out_dir = Path(args.output or "sdvm_preview_out")
        run_synthetic(args.synthetic_example, out_dir, run_label=args.run_label)
        return 0

    if not args.input:
        parser.error("--input is required unless --mode synthetic")

    input_path = Path(args.input)
    out_arg = Path(args.output) if args.output else Path("sdvm_preview_out")

    if args.mode == "validate-only":
        if out_arg.suffix == ".md":
            out_dir = out_arg.parent
        else:
            out_dir = out_arg
        run_validate_only(input_path, out_dir)
        return 0

    if out_arg.suffix == ".md":
        out_dir = out_arg.parent
        md_name = out_arg.name
    else:
        out_dir = out_arg
        md_name = "preview_report.md"

    result = validate_evidence(input_path)
    _write_validation_json(result, out_dir)
    report = build_preview_report(result, run_label=args.run_label)
    md_path = out_dir / md_name
    md_path.write_text(render_markdown(report), encoding="utf-8", newline="\n")
    json_path = out_dir / "preview_report.json"
    json_path.write_text(
        json.dumps(render_json(report), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    if md_path != out_dir / "preview_report.md":
        # Also write canonical names for Action artifact checks.
        (out_dir / "preview_report.md").write_text(md_path.read_text(encoding="utf-8"), encoding="utf-8", newline="\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
