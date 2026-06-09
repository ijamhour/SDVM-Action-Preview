# GitHub Action workflow example (public-safe slice)

Copy-paste workflow for the **SDVM Action Preview** public-safe slice.

## Scope

| Item | Value |
|------|-------|
| Modes | `validate-only`, `preview-report`, `synthetic` |
| Input | `evidence_path` — canonical JSONL on runner |
| Output dir | `sdvm_preview_artifacts` |
| Artifacts | `preview_report.md`, `preview_report.json`, `validation.json`, `job_summary.md` |

This is **not** the full SDVM engine and **not** pilot-grade analysis.

## Pin (when public repo exists)

```yaml
uses: ijamhour/SDVM-Action-Preview@sdvm-action-preview-v0.2
```

## Local checkout

```yaml
uses: ./
```

See root [`action.yml`](../../action.yml) and [`docs/ACTION_USAGE.md`](../../docs/ACTION_USAGE.md).

## Synthetic fixture

[`examples/synthetic/healthy/canonical.jsonl`](../synthetic/healthy/canonical.jsonl)
