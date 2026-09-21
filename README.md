# The Incommensurability Between Algorithms and Memory: Ethical Risks and Resilient Governance of AIGC-Generated Historical Visual Symbols

Supplementary materials for the study of AI-generated images depicting Tang-dynasty historical scenes: coding manual, prompt sets, decision-tree details, per-image coding table, and the image corpus.

> **Status**: supplementary-material repository for the manuscript; maintained on GitHub only.

## Contents

| Path | Description | License |
|---|---|---|
| `coding_data/` | Per-image coding workbook (2 coders, 18 atomic indicators, consensus Y), reliability summary | CC-BY-4.0 |
| `prompts/` | Full text of the three prompt conditions (P1 baseline / P2 evidentiary / P3 negative-frame) | CC-BY-4.0 |
| `analysis/` | Figure scripts (Figs. 1–4) reading all values from the coding workbook, plus decision-tree details | MIT |
| `images/` | The AI-generated sample corpus (162 valid images + training set, compressed) | see `LICENSE-DATA` |
| `codebook/` | Coding manual, 18 atomic indicator definitions, coder training protocol | CC-BY-4.0 |
| `ethics/` | Ethics self-assessment, model-terms compliance record | CC-BY-4.0 |

## Sample structure

6 models (M1–M6) × 3 prompt conditions (P1 low-constraint baseline / P2 evidentiary / P3 negative-frame) × 9 repetitions = 162 valid images (54 per condition), plus a coder-training set.

## Reproducing the figures

```bash
cd analysis
python draw_fig1.py   # Fig. 1 conceptual framework
python draw_fig2.py   # Fig. 2 selection frequency + dimension reliability
python draw_fig3.py   # Fig. 3 real-image case panels
python draw_fig4.py   # Fig. 4 condition contrasts
```

All plotted values are read at runtime from `coding_data/per_image_coding_table_v1.0.xlsx` (single source of truth); the bootstrap uses preregistered seed 20260824.

## Citation

Cite the associated manuscript (citation details to be updated upon publication). If you use the dataset itself, please reference this repository URL and the manuscript.

## Data Availability

All data needed to evaluate the conclusions are present in the paper and/or this repository: the per-image coding table (`coding_data/`), the full image corpus (`images/`), the three prompt sets (`prompts/`), and the figure scripts (`analysis/`).
