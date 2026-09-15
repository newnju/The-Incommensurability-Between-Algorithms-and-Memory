# Model Terms Compliance Record (model_terms_compliance.md)

> **Status: PENDING** — each of the six platforms (M1–M6) must be verified against
> the terms of service in force at generation time (2026-08/09) before public release.

Per-image platform identity is recorded in `coding_data/` (模型名称 column of the
sample list sheet). Verification checklist per platform:

| # | Check item | M1 | M2 | M3 | M4 | M5 | M6 |
|---|---|---|---|---|---|---|---|
| 1 | Output ownership granted to user | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 2 | Redistribution in academic publication / public repository permitted | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 3 | Feedback/license-back scope does not bar redistribution | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 4 | No "no resale / no redistribution" restriction applying here | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |

## Decision rule (preregistered)

- All four checks pass → image may be published at full size.
- Redistribution restricted → thumbnail-only (≤512 px, non-print) in this repo;
  exclusion from the Zenodo original archive.
- Redistribution prohibited → excluded from all public deposits; noted in the
  coding table (presence/absence counts remain reportable).

## Filled findings (to complete)

_(fill one section per platform with: terms URL, access date, clause citations, decision)_

- M1 (ChatGPT Images 2.0):
- M2:
- M3:
- M4:
- M5:
- M6:

## Training-set images

The 8 training-set images were generated on non-preregistered platforms for coder
calibration only and are excluded from the public corpus by default.
