# Zenodo deposit package — v1.0 (README_ZENODO.md)

This package contains the **original full-resolution images** for Zenodo archiving
(thesis supplementary material). Repository `aigc-tang-visual-symbols` mirrors
downscaled copies; this package is the archival original.

## Contents

- `M1_P1_01.png … M6_P3_09.png` — 162 corpus images:
  6 models (M1–M6) × 3 prompt conditions (P1 low-constraint baseline,
  P2 evidentiary, P3 negative-frame) × 9 repetitions. Filenames encode model/condition/replicate;
  per-image metadata (generation date, status) is in the repository's
  `coding_data/per_image_coding_table_v1.0.xlsx`, sheet 样本清单.
- `训练集/` — 8 coder-training images (plus P2/P3 subfolders), generated on
  non-preregistered platforms for coder calibration only; **not part of the 162-sample corpus**.

## All images are AI-generated

No real photograph of any person or event is included. Images are published
solely for critical scholarly analysis of historical distortion in text-to-image
output. Suggested Zenodo record title: "AIGC and the Visual Symbol System of
Tang Historical Painting: Six-Model Corpus (AI-generated, for critical
scholarly analysis)".

## License

CC-BY-4.0 for text/tabular materials; image license and per-platform
redistribution restrictions are documented in
`ethics/model_terms_compliance.md` (repository). Images from platforms whose
terms prohibit redistribution must be removed from this package before the
deposit is published.

## Recommended upload procedure

1. Verify `model_terms_compliance.md` checklist; remove excluded images.
2. Create a Zenodo deposit (upload_type: dataset), attach this folder as a zip
   or individual files, paste metadata from the repository root `.zenodo.json`.
3. Publish, obtain the DOI, then record it in the repository README and the
   manuscript's Data Availability Statement.
