# Codebook

This directory will contain:

- `18_atomic_indicators.md` — definitions and decision criteria for indicators
  f1–f18 (to be added; the f1–f18 indicator definitions and the 0/1/2/NA
  coding scale are already documented in the 说明 sheet of
  `coding_data/per_image_coding_table_v1.0.xlsx`).
- `training_protocol.md` — coder training and calibration protocol
  (to be added).

Note: the per-image coding workbook (`coding_data/`) is complete (both coders,
all 162 images) and includes indicator definitions; step-by-step decision
criteria for borderline cases are held by the authors and available on
request.

## Training images (`images/训练集/`)

This folder holds the **coder-training images** used in the calibration
session (>= 2 h) that preceded formal coding, plus one exemplar per prompt
condition for coder warm-up. They are **AI-generated images produced by the
six studied models** (ChatGPT Images 2.0, gemini-3.1-flash-image,
MAI-Image-2.5-Pro, Reve 2.1, Seedream 5.0 Lite, HunyuanImage-3.0), not
third-party copyrighted archaeological material.

Structure (6 models × 3 conditions = 18 training images):
- `训练集/p1/` — one training image per model (P1 condition)
- `训练集/p2/` — one training image per model (P2 condition)
- `训练集/p3/` — one training image per model (P3 condition)

Training images are excluded from the formal analysis (18 units × 10 shots
= 180 generated; 1 training shot discarded per unit; 162 images coded).
All images are generative outputs of the studied models, shared for
reproducibility and scientific verification under the repository license;
the accompanying paper documents prompt wording and generation settings.
