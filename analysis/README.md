# Analysis

## Entry points

- `run_all.py` — reproduces everything in one command: statistics → figures →
  verification. See [Running](#running).
- `verify_package.py` — independent check that the deposited workbook matches
  the code (66 checks, 53 in `--quick` mode; exit status 0/1). See [Verification](#verification).

## Figure scripts

- `fig_data.py` — single data loader; reads every plotted value from
  `coding_data/per_image_coding_table_v1.0.xlsx` (the coding workbook is the
  single source of truth; no plotted value is hard-coded).
- `fig_style.py` — shared plotting style.
- `draw_fig1.py` … `draw_fig4.py` — Figs. 1–4.

## Statistical scripts

- `cart_analysis.py` — shallow regression CART (`max_depth=3`,
  `min_samples_leaf=15`) and the leave-one-model-out indicator-stability
  procedure reported in Table 2.
- `bootstrap_selection.py` — bootstrap selection frequency `pi_j`
  (B=10000, resampled within the 18 model × condition strata).
- `kappa_calculation.py` — linear-weighted kappa for each dimension, the
  pooled kappa, and the criterion-Y kappa, with 95% percentile bootstrap CI
  (B=10^6, stratified by the 18 model × condition cells). The point estimate
  is printed to 3 decimals, the CI endpoints to 2 — see below.

## Seed policy

All random processes use the preregistered seed **20260824**.

| Process | B | Seed setting |
|---|---|---|
| CART fit (full-data tree and all six leave-one-model-out refits) | — | `random_state=20260824` |
| Bootstrap selection frequency `pi_j` | 10000 | resampling stream `20260824`; CART `random_state=20260824` |
| Kappa 95% CI | 10^6 | resampling stream `20260824` |
| Condition contrasts (Fig. 4b) | 10^6 | resampling stream `20260824` |

The CART seed only breaks ties between features with identical split gains,
so it does not affect the full-data tree (depth 3, 6 terminal nodes, splits
f2/f12/f16/f18) or any of the six leave-one-model-out inclusion counts.
Across CART seeds `pi_j` moves by at most 0.007, which never changes the
`pi >= 0.60` decision or the stable set {f2, f18}.

Image generation is the only random process that is deliberately *not*
seeded: the study characterises the default probabilistic behaviour of the
six models under ordinary use, so each image was generated independently
with a random seed.

Because the CART seed only breaks ties between features with identical split
gains, `pi_j` is stable to within roughly ±0.007 across seeds and no
threshold decision (π ≥ 0.60) or stable-set membership is affected.

### Why the condition contrasts use a larger B

A Fig. 4b contrast is a difference between two means of 54 consensus scores,
and each consensus score lies on the 0.5 grid (it is the mean of two integer
ratings). The bootstrap distribution of the contrast is therefore *discrete*,
with spacing 0.5/54 = 0.00926, and the 97.5th percentile of such a
distribution does not converge smoothly at small B — it hops between
adjacent mass points from one RNG stream to the next. Measured over 200
seeds at B = 10^4:

| Endpoint | Values observed | Split |
|---|---|---|
| D1 P2−P1 upper | +0.1944 / +0.2037 | 125 / 71 |
| D5 P2−P1 lower | −0.0833 / −0.0741 | 122 / 72 |
| D1 P3−P2 upper | +0.3889 / +0.3796 | 108 / 90 |
| D5 P3−P2 lower | +0.0370 / +0.0278 | 134 / 60 |

At B = 10^4 the third decimal is a property of the seed rather than of the
data, and for D1 P2−P1 it decides whether the upper limit "slightly exceeds"
±0.20. At B = 10^6 every endpoint is identical across all seeds tested
(8 seeds per endpoint), so the reported limits are reproducible. The seed is
still 20260824; at this B it no longer affects the result.

### Why the kappa CIs are reported to two decimals at B = 10^6

The kappa CIs (B = 10^6) are **not** affected by the discreteness described
above — kappa is a ratio of counts and its bootstrap distribution is
continuous. They are affected by plain Monte Carlo error, which shrinks with
B: the endpoint standard deviation is SD(q) = sqrt(p(1-p)/B) / f(q), about
0.0021 on average at B = 2000 (range 0.0006–0.0036 over the 14 endpoints) and
about 0.0001 at B = 10^6.

Reporting two decimals *alone* does not deliver reproducibility. Measured
over 300 random streams at B = 2000, only 5 of the 14 endpoints reproduce
their stored two-decimal value in every stream; the D5 lower limit (converged
value 0.42461, boundary at 0.425, a 0.11 SD margin) reproduces in only 52% of
streams. At B = 10^6 every endpoint clears its nearest two-decimal boundary
by at least 2.5 SD (D5 lower) and typically >17 SD, so the two-decimal values
reproduce — verified 6/6 over independent streams.

Raising B further does not rescue the third decimal: the distance from any
value to the nearest three-decimal boundary is at most 0.0005 regardless of
B, and several endpoints sit within 0.0002 of one (the D1 upper limit
converges to 0.6815, the criterion-Y lower limit to 0.3476).

The convention adopted here is therefore:

- **kappa_g (the point estimate)** — deterministic, reported to **3 decimals**;
- **95% CI endpoints** — bootstrap estimates, reported to **2 decimals** at
  **B = 10^6**.

At B = 10^6 the endpoints reproduce the values stored in
`coding_data/per_image_coding_table_v1.0.xlsx` (sheet `维度_Kappa`) in every
random stream tested. Rounding the previously published three-decimal
endpoints to two decimals changes exactly one number, D1's lower limit
(0.48 → 0.47).

### Krippendorff alpha as a cross-check

`kappa_calculation.py` also prints **Krippendorff's alpha** (interval metric)
over exactly the same pairs, so the two coefficients are directly comparable.
It is a deterministic quantity — no bootstrap, hence no CI.

| Level | kappa_g | alpha | alpha − kappa |
|---|---|---|---|
| Pooled (2828 pairs) | 0.671 | 0.773 | +0.102 |
| D1 建筑与场景时代一致性 | 0.579 | 0.674 | +0.095 |
| D2 服饰、器物与武备 | 0.649 | 0.740 | +0.091 |
| D3 族群身份与社会关系 | 0.788 | 0.872 | +0.085 |
| D4 空间构图与历史视觉语法 | 0.407 | 0.510 | +0.103 |
| D5 生成完整性与提示词遵循 | 0.535 | 0.591 | +0.055 |
| Criterion Y | 0.460 | 0.539 | +0.080 |

Alpha exceeds kappa at every level, by 0.055–0.103, and lifts D1, D3 and D4 by
one reliability band (D1 moderate → substantial, D3 substantial → almost
perfect, D4 fair → moderate). That gap is the **kappa paradox**: kappa is
deflated when one category dominates the marginal distribution, alpha is not.
Reporting both therefore separates "the coders disagree" from "the scale is
dominated by one category", which is the argument the manuscript's reliability
section relies on. The values are stored in the `维度_Kappa` sheet (column J,
and cell E4 for the criterion Y).

## Running

One command runs everything and then checks the result:

```bash
python run_all.py                 # statistics + figures + verification (~4 min)
python run_all.py --no-figures    # statistics + verification only
python run_all.py --quick         # skip the B = 10^6 kappa bootstrap
python run_all.py --list          # show the step plan
```

Or run the pieces by hand, in this order:

```bash
cd analysis
python cart_analysis.py         # CART: full-data tree + leave-one-model-out counts
python bootstrap_selection.py   # bootstrap selection frequency pi_j (B = 10000)
python kappa_calculation.py     # kappa_g + 95% CI (B = 10^6, ~90 s)
python draw_fig1.py             # Fig. 1
python draw_fig2.py             # Fig. 2 (reads pi and kappa from the workbook)
python draw_fig3.py             # Fig. 3
python draw_fig4.py             # Fig. 4 (recomputes condition contrasts)
python verify_package.py        # assert the workbook matches the code
```

The three statistical scripts only print; they never write to the workbook.
The four `draw_fig*.py` scripts **overwrite** the committed files in this
directory, which is the point of a reproduction run.

The results recorded in `coding_data/per_image_coding_table_v1.0.xlsx`
(sheets 稳定性_留一 and 维度_Kappa) were produced with the same seed.

## Verification

`verify_package.py` is an independent check, not a re-run. It re-derives the
consensus criterion Y, the condition summary, the dimension means, `pi_j`, the
leave-one-model-out inclusion counts and the kappa values directly from the two
coder sheets, and compares each quantity with the value stored in the
workbook — 66 checks in total (53 in `--quick` mode), including the seed policy, the presence of the
committed figures, the `正文填数索引` cross-references, and the absence of stale
text. It exits 0 when everything matches and 1 otherwise, so it can gate CI.

```bash
python verify_package.py            # full check (~3 min)
python verify_package.py --quick    # skip the B = 10^6 kappa bootstrap (~1 min)
python verify_package.py --full     # also re-check contrast endpoint stability across seeds
```

Quantities stored rounded (dimension means and `kappa_g` to 3 decimals, CI
endpoints to 2) are compared against the half-unit-in-the-last-place
criterion, i.e. the gap must not exceed half of the last stored digit. This is
stricter than comparing `round(x, k)` and avoids the boundary ambiguity where
`round()` and `format()` disagree about a value sitting exactly on a `.5` of
the last place.


## Figure outputs

The manuscript uses the **grayscale** versions, so every `draw_fig*.py` script
writes, when run with the default `save=True`:

- `<stem>.png` — 200-dpi colour raster preview
- `<stem>_gray.png` — 300-dpi grayscale raster (**the version used in the manuscript**)

(`<stem>.pdf` is written for Figs. 1, 2 and 4 only — see the table below.)

No TIFF is written: the 600-dpi TIFFs were 35–60 MB each (uncompressed,
~150 MB across figures) and were never used by the manuscript or committed.

Committed figure files:

| Figure | Committed | Note |
|---|---|---|
| Fig. 1 | `fig1.pdf`, `fig1.png`, `fig1_gray.png` | vector + colour preview + grayscale |
| Fig. 2 | `fig2.pdf`, `fig2.png`, `fig2_gray.png` | vector + colour preview + grayscale |
| Fig. 3 | `fig3.png`, `fig3_gray.png` | raster panels of real images; `draw_fig3.py` is called with `pdf=False`, so no PDF is produced — one would only re-embed the same bitmaps (~20 MB) with no vector benefit |
| Fig. 4 | `fig4.pdf`, `fig4.png`, `fig4_gray.png` | vector + colour preview + grayscale |

Colour is never the only visual channel: bars and markers also differ in fill
(solid vs. hatched vs. open) and the error bars are drawn in black, so the
grayscale versions remain readable.
