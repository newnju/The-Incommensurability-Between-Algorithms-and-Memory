# Coding data — field description (README_coding.md)

Source workbook: `per_image_coding_table_v1.0.xlsx` (renamed from the working template "AIGC历史视觉符号_六模型180样本_结果填写模板.xlsx"; identical content, 9 sheets).

Coders are identified only as Coder A / Coder B (匿名化标识, no personal identifiers). Original workbook retained by the authors; release version is v1.0.

## Sheets

| Sheet | Content |
|---|---|
| 说明 | Overview: 6 models × prompt conditions × 9 per cell = 162 images |
| 样本清单 | ImageID, model code/name (M1–M6), prompt condition (P1/P2), replicate, suggested filename, generation date, generation status, failure/refusal reason |
| 编码员A | Coder A judgments: overall Y + 18 atomic indicators f1–f18 (values 0/1/2 or NA), coding notes |
| 编码员B | Coder B judgments, same structure |
| 共识效标Y | Y_A, Y_B, consensus Y (preregistered rule: mean on disagreement, decimals kept), agreement flag, review note |
| 提示条件汇总 | Per-condition distortion summary |
| 稳定性_留一 | Indicator stability: bootstrap selection frequency πj, leave-one-model-out inclusion counts (drop M1…M6), π ≥ 0.6 flag, final-stable flag |
| 维度_Kappa | Final dimensions and inter-coder reliability (kappa) fill-in area |
| 正文填数索引 | Index mapping manuscript fields to source cells/formulas |
| 提示词全文 | Full English prompt text actually submitted, per condition (P1 baseline / P2 evidentiary / P3 negative-frame) |

## Notes

- Indicator definitions and decision criteria are documented in `codebook/` (to be added).
- f11: records *labeled representation in the image* only; no inference about real ethnic groups from appearance (see `ethics/ethics_self_assessment.md` §3).
- Coder consent scope for public release: tracked in `ethics/ethics_self_assessment.md` §2.
