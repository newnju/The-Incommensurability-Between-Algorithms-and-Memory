# Codebook

## Atomic indicators

The 18 atomic indicators f1–f18, their meaning, and the 0/1/2/NA coding scale
are documented in the `说明` sheet of
`coding_data/per_image_coding_table_v1.0.xlsx`. Step-by-step decision criteria
for borderline cases are held by the authors and available on request.

## Coder training

Both coders completed a training session (>= 2 h) before formal coding, using
the 18 training images in `images/训练集/`; see
`ethics/ethics_self_assessment.md` §2 for the consent scope.

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
