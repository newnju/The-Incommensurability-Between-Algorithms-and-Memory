# Coding data — field description (README_coding.md)

Source workbook: `per_image_coding_table_v1.0.xlsx` (renamed from the working template "AIGC历史视觉符号_六模型180样本_结果填写模板.xlsx"; identical content, 10 sheets).

Coders are identified only as Coder A / Coder B (匿名化标识, no personal identifiers). Original workbook retained by the authors; release version is v1.0.

## Sheets

| Sheet | Content |
|---|---|
| 说明 | Overview: 6 models × prompt conditions × 9 per cell = 162 images |
| 样本清单 | ImageID, model code/name (M1–M6), prompt condition (P1/P2/P3), replicate, corpus filename, generation date, generation status, failure/refusal reason |
| 编码员A | Coder A judgments: overall Y + 18 atomic indicators f1–f18 (values 0/1/2 or NA), coding notes |
| 编码员B | Coder B judgments, same structure |
| 共识效标Y | Y_A, Y_B, consensus Y (preregistered rule: mean on disagreement, decimals kept), agreement flag, review note |
| 提示条件汇总 | Per-condition distortion summary |
| 稳定性_留一 | Indicator stability: bootstrap selection frequency πj, leave-one-model-out inclusion counts (drop M1…M6), π ≥ 0.6 flag, final-stable flag |
| 维度_Kappa | Final dimensions and inter-coder reliability: kappa_g per dimension (3 decimals), pooled kappa, criterion-Y kappa, and their 95% bootstrap CI endpoints (2 decimals — see note below). Also the **Krippendorff alpha cross-check** (interval metric, deterministic, 3 decimals): column J for the five dimensions and the pooled row, cell E4 for the criterion Y |
| 正文填数索引 | Index mapping manuscript fields to source cells/formulas |
| 提示词全文 | Full English prompt text actually submitted, per condition (P1 baseline / P2 evidentiary / P3 negative-frame) |

## Notes

- Indicator definitions and decision criteria are documented in `codebook/`.
- **Precision of the reliability statistics (sheet `维度_Kappa`).** kappa_g is a
  deterministic function of the coded data and is given to 3 decimals. The 95%
  CI endpoints are bootstrap estimates (percentile method, B = 10^6, seed
  20260824) and are given to **2 decimals**. Two decimals *and* B = 10^6 are
  both required: at B = 2000 the endpoint Monte Carlo SD is 0.0006-0.0036
  (measured over 300 random streams), the same order as the 0.005 spacing
  between two-decimal boundaries, so only 5 of the 14 endpoints reproduce in
  every stream; at B = 10^6 the SD falls to about 0.0001 and all endpoints
  clear their boundary by >=2.5 SD. The third decimal is unreachable at any
  feasible B (the D1 upper limit converges to 0.6815, the criterion-Y lower
  limit to 0.3476). The full rationale is in `analysis/README.md` and in the
  `口径` note at `维度_Kappa!A17`.
- **Krippendorff alpha (`维度_Kappa`, column J and cell E4).** Reported alongside
  kappa_g as the cross-check the manuscript refers to. It uses the interval
  metric over exactly the same image x indicator pairs, so the two coefficients
  are directly comparable, and it is a deterministic quantity (no bootstrap,
  hence no CI). Alpha exceeds kappa_g at all seven levels (by 0.055-0.103),
  which is the signature of the kappa paradox: kappa is deflated when one
  category dominates the marginal distribution, alpha is not. Reporting both
  separates "the coders disagree" from "the scale is dominated by one
  category". See `analysis/README.md`.
- f11: records *labeled representation in the image* only; no inference about real ethnic groups from appearance (see `ethics/ethics_self_assessment.md` §3).
- Coder consent scope for public release: tracked in `ethics/ethics_self_assessment.md` §2.
