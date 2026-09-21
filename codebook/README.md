# Codebook

This directory will contain:

- `coding_manual.pdf` — full coding manual (to be added; the manual itself is
  complete and used for coder training, only the PDF deposit is pending).
- `18_atomic_indicators.md` — definitions and decision criteria for indicators
  f1–f18 (to be extracted from the manual).
- `training_protocol.md` — coder training and calibration protocol
  (to be added).

Until these files are deposited, the authoritative reference for indicator
definitions is the coding manual held by the authors; the coding table in
`coding_data/` is already complete (both coders, all 162 images).

## Training images (`images/训练集/`)

This folder holds the **coder-training images** used in the calibration
session (>= 2 h) that preceded formal coding, plus one exemplar per prompt
condition for coder warm-up. They are **AI-generated images produced by the
six studied models** (ChatGPT Images 2.0, gemini-3.1-flash-image,
MAI-Image-2.5-Pro, Reve 2.1, Seedream 5.0 Lite, HunyuanImage-3.0), not
third-party copyrighted archaeological material.

Structure:
- `训练集/*.jpg` — one training image per model (P1 condition)
- `训练集/p2/` — one training image per model (P2 condition)
- `训练集/p3/` — one training image per model (P3 condition)

Training images are excluded from the formal analysis (18 units × 10 shots
= 180 generated; 1 training shot discarded per unit; 162 images coded).
All images are generative outputs of the studied models, shared for
reproducibility and scientific verification under the repository license;
the accompanying paper documents prompt wording and generation settings.
