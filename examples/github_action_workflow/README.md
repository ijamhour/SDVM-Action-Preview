# GitHub Action workflow example (public-safe slice)

Copy-paste workflow for the **SDVM Action Preview** public-safe slice.

## Scope

| Item | Value |
|------|-------|
| Modes | `validate-only`, `preview-report`, `synthetic` |
| Input | `evidence_path` — canonical JSONL on runner |
| Output dir | `sdvm_preview_artifacts` |
| Artifacts | `validation.json`, `preview_report.json`, `preview_report.md`, `job_summary.md` |

Outputs are limited Markdown and JSON preview reports — no HTML report generation.

This is **not** the full SDVM engine and **not** pilot-grade analysis.

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
```

See [`sdvm-preview-example.yml`](sdvm-preview-example.yml) for a full workflow file.

## Local development usage

Testing this Action from a checkout of this repository:

```yaml
uses: ./
```

See root [`action.yml`](../../action.yml) and [`docs/ACTION_USAGE.md`](../../docs/ACTION_USAGE.md).

## Synthetic fixture

[`examples/synthetic/healthy/canonical.jsonl`](../synthetic/healthy/canonical.jsonl)
