# SDVM Action Preview v0.2 — Release Notes

**Status:** Public release notes (documentation only)  
**Preview tag:** `sdvm-action-preview-v0.2` → commit `2f32e94` (immutable when published)  
**Prior preview tag:** `sdvm-action-preview-v0.1` → commit `1afc731` (immutable, preserved)

## Status

`sdvm-action-preview-v0.2` is the **current preview tag** for technical evaluators.

It remains a preview release. It does **not** represent commercial maturity, autonomous tuning, automatic remediation, causal proof, or guaranteed workflow improvement.

**Marketplace publication remains on hold.**

## Public-safe slice note

When published from a future `SDVM-Action-Preview` public repository, this package provides a **limited public-safe Action slice** (`sdvm_action_preview/`). It validates evidence structure, detects PRE/POST/DELTA shape, and produces a preview report suitable for screening.

**Full SDVM diagnostic analysis** (compute, scoring, playbooks, calibration) remains in the private repository and controlled pilot work only.

Private-repo tags `sdvm-action-preview-v0.1` (`1afc731`) and `sdvm-action-preview-v0.2` (`2f32e94`) are **historical preview pins** on the private monorepo — not automatically mirrored to the future public distribution repository.

## What this public preview package is for

- Evidence structure validation over canonical JSONL
- Limited sufficiency screening (`sufficient` / `partial` / `insufficient`)
- PRE/POST/DELTA shape detection without SDVM delta scoring
- Limited preview report for pilot screening support
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
- uses: ijamhour/SDVM-Action-Preview@sdvm-action-preview-v0.2
  with:
    mode: preview-report
    evidence_path: path/to/canonical.jsonl
    out_dir: sdvm_preview_artifacts
    write_job_summary: "true"
```

See [`README.md`](../README.md) and [`examples/github_action_workflow/README.md`](../examples/github_action_workflow/README.md).

## Privacy

Canonical privacy policy: **https://sdvm.tech/privacy/**
