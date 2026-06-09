"""Public-safe preview report generation."""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any

from sdvm_action_preview.evidence_validator import ValidationResult

PREVIEW_NOTICE = (
    "This is an SDVM Action **preview** report. It validates evidence shape and "
    "provides screening-oriented observations only. It is **not** pilot-grade SDVM "
    "analysis and does not expose scoring internals, statistical methodology, or "
    "intervention playbooks."
)


class SufficiencyStatus(str, Enum):
    SUFFICIENT = "sufficient"
    PARTIAL = "partial"
    INSUFFICIENT = "insufficient"


class ShapeStatus(str, Enum):
    YES = "yes"
    NO = "no"
    PARTIAL = "partial"


class NextStepCategory(str, Enum):
    REFINE_CAPTURE = "refine_capture"
    RUN_CONTROLLED_COMPARISON = "run_controlled_comparison"
    CANDIDATE_FOR_PILOT_SCREENING = "candidate_for_pilot_screening"
    NOT_ENOUGH_EVIDENCE_YET = "not_enough_evidence_yet"


@dataclass
class PrePostDeltaShape:
    pre_post_present: ShapeStatus
    delta_comparison_possible: ShapeStatus


@dataclass
class PreviewReport:
    run_label: str | None
    sufficiency: SufficiencyStatus
    pre_post_delta: PrePostDeltaShape
    evidence_summary: dict[str, Any]
    observations: list[str]
    limitations: list[str]
    next_step_category: NextStepCategory
    generated_at: str


def classify_sufficiency(result: ValidationResult) -> SufficiencyStatus:
    """
    Public-safe preview heuristics — not SDVM scoring.

    - sufficient: 3+ valid events with required fields and reasonable diversity
    - partial: 1-2 valid events, or sparse but parseable evidence
    - insufficient: no valid events or unreadable evidence
    """
    count = result.valid_count
    if count == 0:
        return SufficiencyStatus.INSUFFICIENT
    if count <= 2:
        return SufficiencyStatus.PARTIAL
    if count >= 3 and len(result.event_types) >= 2:
        return SufficiencyStatus.SUFFICIENT
    if count >= 5:
        return SufficiencyStatus.SUFFICIENT
    return SufficiencyStatus.PARTIAL


def detect_pre_post_delta_shape(result: ValidationResult) -> PrePostDeltaShape:
    """Detect PRE/POST/DELTA label presence without computing SDVM delta."""
    hits = result.stage_hits
    pre = hits.get("pre", False)
    post = hits.get("post", False)
    delta = hits.get("delta", False)

    if pre and post:
        pre_post = ShapeStatus.YES
    elif pre or post:
        pre_post = ShapeStatus.PARTIAL
    else:
        pre_post = ShapeStatus.NO

    if pre and post and (delta or len(result.run_ids) >= 2):
        delta_possible = ShapeStatus.YES
    elif pre or post:
        delta_possible = ShapeStatus.PARTIAL
    else:
        delta_possible = ShapeStatus.NO

    return PrePostDeltaShape(pre_post_present=pre_post, delta_comparison_possible=delta_possible)


def choose_next_step(
    sufficiency: SufficiencyStatus,
    shape: PrePostDeltaShape,
) -> NextStepCategory:
    if sufficiency == SufficiencyStatus.INSUFFICIENT:
        return NextStepCategory.NOT_ENOUGH_EVIDENCE_YET
    if sufficiency == SufficiencyStatus.PARTIAL:
        return NextStepCategory.REFINE_CAPTURE
    if shape.pre_post_present == ShapeStatus.YES and shape.delta_comparison_possible != ShapeStatus.YES:
        return NextStepCategory.RUN_CONTROLLED_COMPARISON
    if sufficiency == SufficiencyStatus.SUFFICIENT:
        return NextStepCategory.CANDIDATE_FOR_PILOT_SCREENING
    return NextStepCategory.REFINE_CAPTURE


def build_observations(result: ValidationResult, sufficiency: SufficiencyStatus) -> list[str]:
    observations: list[str] = []
    if result.valid_count:
        observations.append(
            f"Parsed {result.valid_count} valid event(s) from {result.total_lines} non-empty line(s)."
        )
        observations.append(
            f"Observed {len(result.run_ids)} distinct run label(s) and "
            f"{len(result.event_types)} event type(s)."
        )
    if result.line_issues:
        observations.append(f"{len(result.line_issues)} line(s) failed structural validation.")
    if sufficiency == SufficiencyStatus.SUFFICIENT:
        observations.append("Evidence shape meets preview sufficiency heuristics for screening.")
    elif sufficiency == SufficiencyStatus.PARTIAL:
        observations.append("Evidence is parseable but sparse for a confident preview screening.")
    else:
        observations.append("Evidence is not sufficient for preview screening.")
    return observations


def build_limitations() -> list[str]:
    return [
        "Preview heuristics only — no SDVM scores, weights, thresholds, or playbook logic.",
        "No statistical methodology or calibration is applied in this public slice.",
        "Full pilot-grade SDVM analysis remains available only through controlled pilot work.",
        "Do not treat this report as production diagnosis or guaranteed improvement.",
    ]


def build_preview_report(result: ValidationResult, *, run_label: str | None = None) -> PreviewReport:
    sufficiency = classify_sufficiency(result)
    shape = detect_pre_post_delta_shape(result)
    return PreviewReport(
        run_label=run_label,
        sufficiency=sufficiency,
        pre_post_delta=shape,
        evidence_summary={
            "input_path": str(result.input_path),
            "total_lines": result.total_lines,
            "valid_events": result.valid_count,
            "line_issues": len(result.line_issues),
            "distinct_run_ids": len(result.run_ids),
            "distinct_event_types": len(result.event_types),
            "distinct_actors": len(result.actors),
        },
        observations=build_observations(result, sufficiency),
        limitations=build_limitations(),
        next_step_category=choose_next_step(sufficiency, shape),
        generated_at=datetime.now(timezone.utc).isoformat(),
    )


def render_markdown(report: PreviewReport) -> str:
    label = report.run_label or "SDVM Action Preview"
    lines = [
        f"# {label}",
        "",
        PREVIEW_NOTICE,
        "",
        "## Evidence shape summary",
        "",
        f"- Valid events: **{report.evidence_summary['valid_events']}**",
        f"- Non-empty lines: **{report.evidence_summary['total_lines']}**",
        f"- Distinct run labels: **{report.evidence_summary['distinct_run_ids']}**",
        f"- Distinct event types: **{report.evidence_summary['distinct_event_types']}**",
        f"- Structural line issues: **{report.evidence_summary['line_issues']}**",
        "",
        "## Sufficiency classification",
        "",
        f"**{report.sufficiency.value}** (preview heuristic — not SDVM scoring)",
        "",
        "## PRE/POST/DELTA availability",
        "",
        f"- PRE/POST present: **{report.pre_post_delta.pre_post_present.value}**",
        f"- DELTA comparison possible: **{report.pre_post_delta.delta_comparison_possible.value}**",
        "",
        "## Public-safe observations",
        "",
    ]
    lines.extend(f"- {item}" for item in report.observations)
    lines.extend(["", "## Limitations", ""])
    lines.extend(f"- {item}" for item in report.limitations)
    lines.extend(
        [
            "",
            "## Next-step category",
            "",
            f"**{report.next_step_category.value}**",
            "",
            "Pilot screening: https://sdvm.tech/pilot/intake/",
            "",
            f"_Generated at {report.generated_at}_",
        ]
    )
    return "\n".join(lines) + "\n"


def render_json(report: PreviewReport) -> dict[str, Any]:
    return {
        "preview_notice": PREVIEW_NOTICE,
        "run_label": report.run_label,
        "sufficiency": report.sufficiency.value,
        "pre_post_delta": {
            "pre_post_present": report.pre_post_delta.pre_post_present.value,
            "delta_comparison_possible": report.pre_post_delta.delta_comparison_possible.value,
        },
        "evidence_summary": report.evidence_summary,
        "observations": report.observations,
        "limitations": report.limitations,
        "next_step_category": report.next_step_category.value,
        "generated_at": report.generated_at,
    }


def write_preview_outputs(
    report: PreviewReport,
    out_dir: Path,
    *,
    markdown_name: str = "preview_report.md",
    json_name: str = "preview_report.json",
) -> tuple[Path, Path]:
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    md_path = out / markdown_name
    json_path = out / json_name
    md_path.write_text(render_markdown(report), encoding="utf-8", newline="\n")
    json_path.write_text(
        json.dumps(render_json(report), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return md_path, json_path
