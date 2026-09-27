# The Incommensurability Between Algorithms and Memory: Ethical Risks and Resilient Governance of AIGC-Generated Historical Visual Symbols

Supplementary materials for the study of AI-generated images depicting Tang-dynasty historical scenes: coding manual, prompt sets, decision-tree details, per-image coding table, and the image corpus.

> **Status**: supplementary-material repository for the manuscript; maintained on GitHub only.

## Contents

| Path | Description | License |
|---|---|---|
| `coding_data/` | Per-image coding workbook (2 coders, 18 atomic indicators, consensus Y), reliability summary | CC-BY-4.0 |
| `prompts/` | Full text of the three prompt conditions (P1 baseline / P2 evidentiary / P3 negative-frame) | CC-BY-4.0 |
| `analysis/` | Figure scripts (Figs. 1–4), CART and leave-one-model-out stability analysis, bootstrap selection frequency, kappa computation, one-command reproduction and self-verification | MIT |
| `images/` | The AI-generated sample corpus (162 coded images + 18 training images, JPEG) | see `LICENSE-DATA` |
| `codebook/` | Coding manual, 18 atomic indicator definitions, coder training protocol | CC-BY-4.0 |
| `ethics/` | Ethics self-assessment, model use compliance record | CC-BY-4.0 |
| `requirements.txt`, `environment.yml` | Pinned dependency sets (the verified environment) | MIT |

## Sample structure

6 models (M1–M6) × 3 prompt conditions (P1 low-constraint baseline / P2 evidentiary / P3 negative-frame) × 9 repetitions = 162 coded images (54 per condition). Each model × condition cell produced 10 shots: 9 entered the coded corpus and 1 was set aside for the coder-training set (`images/训练集/`, 6 × 3 = 18 images). No generation was refused or failed, so no replacement shot was needed.

## Requirements

The analysis scripts need Python ≥ 3.12 (the floor is set by the pinned numpy) with numpy, scikit-learn, matplotlib, openpyxl and Pillow. Install the verified versions:

```bash
python -m pip install -r requirements.txt      # or: conda env create -f environment.yml
```

`requirements.txt` pins exact versions because the CART seed only breaks ties between features with identical split gains, which makes the bootstrap selection frequency `pi_j` sensitive to the scikit-learn version (spread up to ≈ 0.007, enough to move the third decimal). The pinned set is the one under which every number in the workbook is reproduced.

## Reproducing the analysis

One command runs the statistics, regenerates Figs. 1–4 from the workbook, and then verifies the workbook against the code:

```bash
python analysis/run_all.py                 # everything, ~4 min
python analysis/run_all.py --no-figures    # statistics + verification only
python analysis/run_all.py --quick         # skip the B = 10^6 kappa bootstrap
python analysis/run_all.py --list          # show the step plan
```

To run the pieces by hand:

```bash
cd analysis
python cart_analysis.py         # CART: full-data tree + leave-one-model-out counts
python bootstrap_selection.py   # bootstrap selection frequency pi_j (B = 10000)
python kappa_calculation.py     # kappa_g + 95% CI (B = 10^6)
python draw_fig1.py             # Fig. 1 conceptual framework
python draw_fig2.py             # Fig. 2 selection frequency + dimension reliability
python draw_fig3.py             # Fig. 3 real-image case panels
python draw_fig4.py             # Fig. 4 condition contrasts
python verify_package.py        # assert the workbook matches the code
```

All plotted values are read at runtime from `coding_data/per_image_coding_table_v1.0.xlsx` (single source of truth); nothing is hard-coded. All random processes use the preregistered seed 20260824; see `analysis/README.md` for the full seed policy.

`verify_package.py` is an independent check rather than a re-run: it re-derives the consensus criterion Y, the condition summary, the dimension means, `pi_j`, the leave-one-model-out inclusion counts and the kappa values from the two coder sheets and compares each one with the value stored in the workbook (66 checks; 53 in `--quick` mode; exit status 0 on success, 1 otherwise, so it can gate CI).

**Reported precision.** Reliability point estimates (kappa_g) are deterministic and given to 3 decimals. Bootstrap-derived interval endpoints are given to the precision at which they are reproducible: the Fig. 4b condition contrasts at 3 decimals (B = 10^6), and the kappa 95% CIs at 2 decimals (B = 10^6). Rationale and measurements are in `analysis/README.md`.

**Krippendorff alpha.** `analysis/kappa_calculation.py` also reports Krippendorff's alpha (interval metric) over the same pairs as a cross-check: it exceeds kappa_g at every level (by 0.055–0.103), which is the kappa-paradox signature of a skewed marginal distribution rather than genuine coder disagreement. Values are in the `维度_Kappa` sheet (column J, cell E4 for the criterion Y).

## Citation

Cite the associated manuscript (citation details to be updated upon publication). If you use the dataset itself, please reference this repository URL and the manuscript.

## Data Availability

Everything needed to evaluate the conclusions is in this repository: the per-image coding table (`coding_data/`), the complete image corpus — all 162 coded images and all 18 training images at each model's native resolution (`images/`) — the three prompt sets (`prompts/`), the coding manual (`codebook/`), the ethics records (`ethics/`), and the analysis code with its pinned environment (`analysis/`, `requirements.txt`). No external archive is required.

