# SDVM GitHub Action — usage (public-safe preview)

Public-safe extract for the composite Action at repository root (`action.yml`).

## Modes

| Mode | Description |
|------|-------------|
| `validate-only` | Structural JSONL validation only |
| `preview-report` | Validation + limited preview report (default) |
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
- Validates evidence shape and emits a limited screening report.
- **Does not** run full SDVM scoring, playbooks, or statistical methodology.
- No GitHub API calls, PR comments, repository writes, or external telemetry.

## Example workflow snippet

```yaml
- uses: actions/checkout@v4
- uses: ./
  with:
    mode: preview-report
    evidence_path: path/to/canonical.jsonl
- uses: actions/upload-artifact@v4
  with:
    path: sdvm_preview_artifacts/
```

## Privacy

Canonical privacy policy: **https://sdvm.tech/privacy/**

For published pins, use `ijamhour/SDVM-Action-Preview@sdvm-action-preview-v0.2` after the public repository is created.
