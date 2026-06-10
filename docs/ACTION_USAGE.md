# SDVM GitHub Action — usage (public-safe preview)

Public-safe extract for the composite Action at repository root (`action.yml`).

## Modes

| Mode | Description |
|------|-------------|
| `validate-only` | Structural JSONL validation only |
| `preview-report` | Validation + limited Markdown/JSON preview report (default) |
| `synthetic` | Run bundled synthetic example |

## Inputs

| Input | Default | Notes |
|-------|---------|-------|
| `evidence_path` | (required*) | Runner-local canonical JSONL file or directory |
| `mode` | `preview-report` | `validate-only` \| `preview-report` \| `synthetic` |
| `run_label` | (optional) | Report header label |
| `out_dir` | `sdvm_preview_artifacts` | Output directory |
| `synthetic_example` | `healthy` | When `mode=synthetic` |
| `write_job_summary` | `true` | Writes `job_summary.md` + `GITHUB_STEP_SUMMARY` |

*Not required when `mode=synthetic`.

## Outputs

| Output | Description |
|--------|-------------|
| `preview_report_path` | Path to `preview_report.md` |
| `validation_path` | Path to `validation.json` |
| `artifacts_dir` | Output directory |
| `preview_mode` | Mode executed |

## Behavior

- Installs the public-safe preview package with `pip install -e .` on the runner.
- Validates evidence shape and emits a limited Markdown/JSON screening report.
- **Does not** run full SDVM scoring, playbooks, or statistical methodology.
- No GitHub API calls, PR comments, repository writes, or external telemetry.

## Published Action usage

Pin the public preview tag in consumer workflows:

```yaml
- uses: actions/checkout@v4
- uses: actions/setup-python@v5
  with:
    python-version: "3.11"
- uses: ijamhour/SDVM-Action-Preview@sdvm-action-preview-public-v0.1
  with:
    mode: preview-report
    evidence_path: path/to/canonical.jsonl
    out_dir: sdvm_preview_artifacts
    write_job_summary: "true"
- uses: actions/upload-artifact@v4
  with:
    path: sdvm_preview_artifacts/
```

**Artifacts** (under `out_dir`): `validation.json`, `preview_report.json`, `preview_report.md`, `job_summary.md`.

For a human-friendly illustration of how public-safe screening can be presented, see [`docs/demo/`](demo/).

## Local development usage

Testing this Action from a checkout of this repository (CI or local workflow development):

```yaml
- uses: actions/checkout@v4
- uses: actions/setup-python@v5
  with:
    python-version: "3.11"
- uses: ./
  with:
    mode: preview-report
    evidence_path: examples/synthetic/healthy/canonical.jsonl
    out_dir: sdvm_preview_artifacts
- uses: actions/upload-artifact@v4
  with:
    path: sdvm_preview_artifacts/
```

## Privacy

Canonical privacy policy: **https://sdvm.tech/privacy/**
