# Security Policy

## Status

SDVM is currently provided as a **preview** GitHub Action and documentation package. This policy describes how to report security concerns for the preview path. It does **not** establish an enterprise SLA, paid support contract, or production incident response guarantee.

## Reporting a vulnerability

For **non-sensitive** security concerns, open a GitHub issue with enough detail to reproduce or assess the concern.

Do **not** post secrets, credentials, private traces, customer data, or sensitive payloads in public issues.

For **sensitive** reports, use a private contact channel documented by the repository owner. If no private channel is available, do not disclose sensitive details publicly — wait until a private reporting path is established.

## Supported versions

| Version | Status |
|---------|--------|
| `sdvm-action-preview-public-v0.1` | Current preview tag |

## Scope

This policy covers:

- this repository and documentation;
- the composite GitHub Action at repository root (`action.yml`);
- example workflows and usage docs that describe Action usage.

Experimental lab paths are **not** included in this distribution package.

## Data handling

The Action runs on your GitHub Actions runner, reads runner-local input paths, writes artifacts locally, and does not call external services or the GitHub API for PR comments or repository writes. See [`docs/ACTION_USAGE.md`](docs/ACTION_USAGE.md).

## Privacy

Canonical privacy policy: **https://sdvm.tech/privacy/**

## Non-goals

This preview does **not** provide:

- enterprise SLA or guaranteed incident response;
- hosted SaaS processing of your traces;
- autonomous remediation or policy enforcement.
