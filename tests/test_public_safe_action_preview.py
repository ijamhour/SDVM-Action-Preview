"""Tests for the public-safe SDVM Action Preview slice."""

from __future__ import annotations

import ast
import json
import subprocess
import sys
from pathlib import Path

import pytest

from sdvm_action_preview.cli import main as cli_main
from sdvm_action_preview.evidence_validator import validate_evidence
from sdvm_action_preview.preview_report import (
    NextStepCategory,
    SufficiencyStatus,
    build_preview_report,
    classify_sufficiency,
    detect_pre_post_delta_shape,
    render_markdown,
)
from sdvm_action_preview.synthetic_examples import example_content, example_names, write_example

REPO_ROOT = Path(__file__).resolve().parent.parent
MODULE_ROOT = REPO_ROOT / "sdvm_action_preview"
BUILD_SCRIPT = REPO_ROOT / "tools" / "build_public_distribution_staging_v0_1.py"
STAGING_ROOT = REPO_ROOT / "build" / "public_distribution_staging" / "SDVM-Action-Preview"

FORBIDDEN_IMPORT_PREFIXES = ("sdvm", "sdvm_playbooks", "sdvm_baseline")


@pytest.fixture
def healthy_fixture(tmp_path: Path) -> Path:
    return write_example("healthy", tmp_path / "healthy")


@pytest.fixture
def partial_fixture(tmp_path: Path) -> Path:
    return write_example("partial_evidence", tmp_path / "partial")


@pytest.fixture
def pre_post_fixture(tmp_path: Path) -> Path:
    return write_example("pre_post_delta_skeleton", tmp_path / "pre_post")


def test_synthetic_example_names() -> None:
    assert "healthy" in example_names()
    assert "partial_evidence" in example_names()
    assert "pre_post_delta_skeleton" in example_names()


def test_jsonl_validation_healthy(healthy_fixture: Path) -> None:
    result = validate_evidence(healthy_fixture)
    assert result.valid_count == 5
    assert result.line_issues == []


def test_sufficiency_classifications(
    healthy_fixture: Path,
    partial_fixture: Path,
    tmp_path: Path,
) -> None:
    healthy = validate_evidence(healthy_fixture)
    partial = validate_evidence(partial_fixture)
    empty = tmp_path / "empty.jsonl"
    empty.write_text("\n", encoding="utf-8")
    insufficient = validate_evidence(empty)

    assert classify_sufficiency(healthy) == SufficiencyStatus.SUFFICIENT
    assert classify_sufficiency(partial) == SufficiencyStatus.PARTIAL
    assert classify_sufficiency(insufficient) == SufficiencyStatus.INSUFFICIENT


def test_pre_post_delta_shape_detection(pre_post_fixture: Path) -> None:
    result = validate_evidence(pre_post_fixture)
    shape = detect_pre_post_delta_shape(result)
    assert shape.pre_post_present.value == "yes"
    assert shape.delta_comparison_possible.value == "yes"


def test_markdown_report_generation(healthy_fixture: Path) -> None:
    result = validate_evidence(healthy_fixture)
    report = build_preview_report(result, run_label="test-run")
    text = render_markdown(report)
    assert "preview" in text.lower()
    assert report.next_step_category == NextStepCategory.CANDIDATE_FOR_PILOT_SCREENING
    assert "sufficient" in text


def test_cli_preview_report_smoke(healthy_fixture: Path, tmp_path: Path) -> None:
    out = tmp_path / "out"
    rc = cli_main(
        [
            "--input",
            str(healthy_fixture),
            "--output",
            str(out),
            "--mode",
            "preview-report",
            "--run-label",
            "cli-smoke",
        ]
    )
    assert rc == 0
    assert (out / "preview_report.md").is_file()
    assert (out / "preview_report.json").is_file()
    assert (out / "validation.json").is_file()


def test_cli_synthetic_mode(tmp_path: Path) -> None:
    out = tmp_path / "synthetic_out"
    rc = cli_main(["--mode", "synthetic", "--output", str(out), "--synthetic-example", "healthy"])
    assert rc == 0
    assert (out / "preview_report.md").is_file()


def test_no_forbidden_imports_in_public_module() -> None:
    for path in MODULE_ROOT.rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    root = alias.name.split(".")[0]
                    assert root not in FORBIDDEN_IMPORT_PREFIXES, f"{path}: import {alias.name}"
            elif isinstance(node, ast.ImportFrom) and node.module:
                root = node.module.split(".")[0]
                assert root not in FORBIDDEN_IMPORT_PREFIXES, f"{path}: from {node.module}"


def test_staging_builder_excludes_private_engine(tmp_path: Path) -> None:
    forbidden = [
        REPO_ROOT / "sdvm",
        REPO_ROOT / "sdvm_playbooks",
        REPO_ROOT / "sdvm_baseline",
    ]
    for path in forbidden:
        assert not path.exists(), f"Forbidden staging path present: {path}"
    assert (REPO_ROOT / "sdvm_action_preview").is_dir()


def test_staging_package_contains_public_slice_files() -> None:
    if not STAGING_ROOT.is_dir():
        pytest.skip("staging not built in this session")
    required = [
        "action.yml",
        "README.md",
        "sdvm_action_preview/cli.py",
        "examples/synthetic/healthy/canonical.jsonl",
        "tests/test_public_safe_action_preview.py",
    ]
    for rel in required:
        assert (STAGING_ROOT / rel).is_file(), rel
