# SDVM Action Preview public-safe v0.1 — Release Notes

**Status:** Public release notes (documentation only)  
**Public tag:** `sdvm-action-preview-public-v0.1`  
**Release status:** draft — the public repository and public tag are live; the GitHub Release remains draft  
**Marketplace:** on hold

## Status

`sdvm-action-preview-public-v0.1` is the **current preview tag** for this public repository.

It remains a preview release. It does **not** represent commercial maturity, autonomous tuning, automatic remediation, causal proof, or guaranteed workflow improvement.

The public repository and public tag are live. The GitHub Release remains **draft**, and Marketplace publication remains **on hold**.

## Public-safe slice note

This package provides a **limited public-safe Action slice** (`sdvm_action_preview/`). It validates evidence structure, detects PRE/POST/DELTA shape, and produces limited Markdown and JSON preview reports suitable for screening.

**Full SDVM diagnostic analysis** (compute, scoring, playbooks, calibration) remains in the private repository and controlled pilot work only.

Internal preview tags on the private monorepo are **not** mirrored to this public repository.

## What this public preview package is for

- Evidence structure validation over canonical JSONL
- Limited sufficiency screening (`sufficient` / `partial` / `insufficient`)
- PRE/POST/DELTA shape detection without SDVM delta scoring
- Limited Markdown/JSON preview reports for pilot screening support
- Synthetic examples for demonstration

## What this public preview package is not

This package does **not** provide:

- the full private SDVM engine or pilot-grade analysis;
- SDVM scoring internals, statistical methodology, or playbook recommendations;
- commercial maturity or Gate 3 completion;
- GitHub Marketplace publication (on hold);
- autonomous tuning, automatic remediation, causal proof, or guaranteed improvement.

## How to use (public-safe slice)

```yaml
- uses: ijamhour/SDVM-Action-Preview@sdvm-action-preview-public-v0.1
  with:
    mode: preview-report
    evidence_path: path/to/canonical.jsonl
    out_dir: sdvm_preview_artifacts
    write_job_summary: "true"
```

**Artifacts** (under `out_dir`): `validation.json`, `preview_report.json`, `preview_report.md`, `job_summary.md`.

See [`README.md`](../README.md) and [`examples/github_action_workflow/README.md`](../examples/github_action_workflow/README.md).

## Privacy

Canonical privacy policy: **https://sdvm.tech/privacy/**
