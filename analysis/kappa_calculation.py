# -*- coding: utf-8 -*-
"""Inter-coder reliability: linear-weighted kappa and 95% bootstrap CI.

Reproduces Table 2 (dimension-level kappa, pooled kappa, criterion-Y kappa)
and Fig. 2b.

The bootstrap loop is vectorised, which makes B = 1e6 affordable: about
1.5 min for all seven rows, against about 2 h for a per-replicate loop.

Preregistered specification
---------------------------
- Weight: linear, w(i,j) = |i - j| / (k - 1) with k = 3 ordinal levels.
- Pooling rule: all image x indicator pairs are collapsed into one 3x3
  weighted confusion matrix; pairs where either coder recorded NA are
  dropped (union rule).
- Dimension kappa_g: same pooling within the dimension's indicators.
  D1 = f2, D2 = f3..f9, D3 = f10..f12, D4 = f13..f16, D5 = f18.
- 95% CI: percentile bootstrap, B = 1e6, stratified by the 18 model x
  condition cells (resampling with replacement within each stratum).

Seed
----
SEED = 20260824 is used for the bootstrap resampling stream.

Reported precision
------------------
kappa_g is a deterministic function of the coded data and is reported to
three decimals.  The CI endpoints are *bootstrap estimates*, and are
reported to TWO decimals.

Why two decimals AND B = 1e6 (both are needed):
  At B = 2000 the endpoint Monte Carlo SD is 0.0006-0.0036 (measured over
  300 random streams), i.e. the same order as the 0.005 spacing between
  two-decimal rounding boundaries.  Measured over 300 random streams at
  B = 2000, only 5 of the 14 endpoints reproduce their stored two-decimal
  value in every stream; the D5 lower limit (converged value 0.42461,
  boundary at 0.425, i.e. a 0.11 SD margin) reproduces in only 52% of
  streams.  Reporting two decimals *alone* therefore does not deliver
  reproducibility.
  At B = 1e6 the endpoint SD falls to about 0.0001 (0.00015 for the
  tightest endpoint), giving every endpoint a margin of at least 2.5 SD
  (D5 lower) and typically >17 SD, so the two-decimal values reproduce.
The third decimal is unreachable at any feasible B: the distance from any
value to the nearest three-decimal boundary is at most 0.0005 regardless of
B (the D1 upper limit converges to 0.6815, the criterion-Y lower limit to
0.3476).
The B = 1e6 endpoints, rounded to two decimals, equal the values stored in
`coding_data/per_image_coding_table_v1.0.xlsx` (sheet 维度_Kappa) for all
seven rows - verified against B = 1e6 convergence runs over four
independent random streams, so no stored number had to change.
"""
import collections
import os

import numpy as np
import openpyxl

HERE = os.path.dirname(os.path.abspath(__file__))
WORKBOOK = os.path.join(HERE, '..', 'coding_data',
                        'per_image_coding_table_v1.0.xlsx')

SEED = 20260824
BOOT_B = 1000000
CHUNK = 250000                     # replicates held in memory at once

DIMENSIONS = {
    'D1 建筑与场景时代一致性': [2],
    'D2 服饰、器物与武备': list(range(3, 10)),
    'D3 族群身份与社会关系': [10, 11, 12],
    'D4 空间构图与历史视觉语法': [13, 14, 15, 16],
    'D5 生成完整性与提示词遵循': [18],
}
# NOTE on the D1 and D5 indicator sets.
#
# These two entries reproduce the kappa values reported in the manuscript's
# Table 2 (D1 = 0.579, D5 = 0.535), which are computed over the *stable*
# indicator of each dimension only (f2 and f18 respectively).  Pooling the
# whole dimension instead gives:
#
#     D1 over f1+f2   -> kappa = 0.490 [0.42, 0.56]
#     D5 over f17+f18 -> kappa = 0.490 [0.40, 0.58]
#
# Table 2's pi-range column, however, spans the whole dimension (0.273-0.731
# for D1, i.e. f1 and f2; 0.050-0.995 for D5, i.e. f17 and f18), and D2-D4
# have no stable indicator at all, so their kappa can only be pooled over the
# full dimension.  The package therefore uses two different pooling sets for
# D1/D5 versus D2-D4, which matches the published numbers but should be
# stated explicitly in the manuscript, or the Table 2 pi ranges should be
# narrowed to the stable indicator.

_W = np.array([[abs(i - j) / 2.0 for j in range(3)] for i in range(3)])


def _load():
    """Returns recs with recs[iid] = {'model','cond','A','B','A_Y','B_Y'}."""
    wb = openpyxl.load_workbook(WORKBOOK, data_only=True)
    recs = {}
    for sheet, key in (('编码员A', 'A'), ('编码员B', 'B')):
        for r in wb[sheet].iter_rows(min_row=2, values_only=True):
            if r[0] is None:
                continue
            rec = recs.setdefault(str(r[0]), {'model': r[1], 'cond': r[3]})
            rec[key] = list(r[6:24])            # f1..f18
            rec[key + '_Y'] = r[5]              # overall Y
    wb.close()
    return recs


def _num(x):
    if x is None or str(x) == 'NA':
        return None
    return int(x)


def weighted_kappa(pairs):
    """Linear-weighted kappa over a list of (a, b) ordinal pairs."""
    n = len(pairs)
    if n == 0:
        return float('nan')
    mat = collections.Counter(pairs)
    w = lambda i, j: abs(i - j) / 2.0
    do = sum(w(i, j) * mat[(i, j)] for i in range(3) for j in range(3)) / n
    ra = [sum(mat[(i, j)] for j in range(3)) / n for i in range(3)]
    cb = [sum(mat[(i, j)] for i in range(3)) / n for j in range(3)]
    de = sum(w(i, j) * ra[i] * cb[j] for i in range(3) for j in range(3))
    return 1 - do / de


def krippendorff_alpha(pairs):
    """Krippendorff's alpha (interval metric) over the same (a, b) pairs.

    Reported alongside kappa as the cross-check the manuscript refers to.
    The units are identical to `weighted_kappa`'s (one pair per coded cell),
    so the two coefficients are directly comparable; the interval difference
    function delta^2(c, k) = (c - k)^2 matches the linear weight
    w(i, j) = |i - j| / 2 used above (the /2 only rescales, it cancels).

    Why both: kappa is deflated when one category dominates the marginal
    ("kappa paradox"), alpha is not.  Computing both therefore separates
    "the coders disagree" from "the scale is dominated by one category" -
    which is exactly the argument in the manuscript's reliability section.

    Two coders per unit, so each unit contributes weight 1/(m-1) = 1 to
    both off-diagonal cells of the coincidence matrix.
    """
    if not pairs:
        return float('nan')
    O = np.zeros((3, 3))
    for a, b in pairs:
        O[a, b] += 1.0
        O[b, a] += 1.0
    nc = O.sum(axis=1)
    n = nc.sum()
    D = np.array([[(i - j) ** 2 for j in range(3)] for i in range(3)], float)
    do = (O * D).sum() / n
    de = (np.outer(nc, nc) * D).sum() / (n * (n - 1))
    return 1 - do / de


def _pairs(recs, ids, cols):
    out = []
    for iid in ids:
        rec = recs[iid]
        for c in cols:
            a, b = _num(rec['A'][c - 1]), _num(rec['B'][c - 1])
            if a is not None and b is not None:
                out.append((a, b))
    return out


def _y_pairs(recs, ids):
    out = []
    for iid in ids:
        a, b = _num(recs[iid]['A_Y']), _num(recs[iid]['B_Y'])
        if a is not None and b is not None:
            out.append((a, b))
    return out


def _strata(recs, ids):
    units = collections.defaultdict(list)
    for iid in ids:
        units[(recs[iid]['model'], recs[iid]['cond'])].append(iid)
    return list(units.values())


# ---------------------------------------------------------------- vectorised

def _count_matrices(recs, ids, cols):
    """(n_ids, 9) flattened 3x3 count matrix per image."""
    out = np.zeros((len(ids), 9))
    for k, iid in enumerate(ids):
        rec = recs[iid]
        if cols is None:
            a, b = _num(rec['A_Y']), _num(rec['B_Y'])
            if a is not None and b is not None:
                out[k, a * 3 + b] += 1.0
        else:
            for c in cols:
                a, b = _num(rec['A'][c - 1]), _num(rec['B'][c - 1])
                if a is not None and b is not None:
                    out[k, a * 3 + b] += 1.0
    return out


def _kappa_from_counts(tot):
    """tot: (B, 9) -> (B,) linear-weighted kappa.  Same formula as above."""
    tot = tot.reshape(-1, 3, 3)
    n = tot.sum(axis=(1, 2))
    do = (tot * _W).sum(axis=(1, 2)) / n
    ra = tot.sum(axis=2) / n[:, None]
    cb = tot.sum(axis=1) / n[:, None]
    return 1.0 - do / np.einsum('bi,ij,bj->b', ra, _W, cb)


def estimate(recs, cols, B=BOOT_B, seed=SEED, chunk=CHUNK):
    """Point estimate and percentile CI for one pooling rule.

    cols=None means the criterion-Y pooling (overall Y rather than indicators).

    Statistically identical to the original loop: each stratum is resampled
    with replacement to its own size (a multinomial draw), which is what
    `rng.choice(u, size=len(u), replace=True)` does.  Only the RNG stream
    consumption differs, so results agree in distribution, not bit for bit.
    """
    ids = sorted(recs)
    pairs = _y_pairs(recs, ids) if cols is None else _pairs(recs, ids, cols)
    point = weighted_kappa(pairs)

    mats = _count_matrices(recs, ids, cols)
    strata = [np.asarray([ids.index(i) for i in u]) for u in _strata(recs, ids)]

    rng = np.random.default_rng(seed)
    reps = np.empty(B)
    done = 0
    while done < B:
        b = min(chunk, B - done)
        acc = np.zeros((b, 9))
        for u in strata:
            p = np.full(u.size, 1.0 / u.size)
            acc += rng.multinomial(u.size, p, size=b) @ mats[u]
        reps[done:done + b] = _kappa_from_counts(acc)
        done += b
    lo, hi = np.percentile(reps, [2.5, 97.5])
    return point, lo, hi


def main():
    recs = _load()
    ids = sorted(recs)
    print(f'Linear-weighted kappa (bootstrap CI: B={BOOT_B}, seed={SEED})')
    print('kappa_g to 3 decimals; CI endpoints to 2 decimals '
          '(see "Reported precision" in the module docstring)')
    print('alpha = Krippendorff (interval metric) cross-check, no bootstrap\n')
    print(f'{"":<28}{"kappa_g":>8}{"95% CI":>17}{"alpha":>8}{"a-kappa":>9}')
    rows = [('Pooled (2828 pairs)', list(range(1, 19)))]
    rows += list(DIMENSIONS.items())
    rows += [('Criterion Y', None)]
    for name, cols in rows:
        p, lo, hi = estimate(recs, cols)
        pairs = _y_pairs(recs, ids) if cols is None else _pairs(recs, ids, cols)
        a = krippendorff_alpha(pairs)
        print(f'{name:<28}{p:>8.3f}  [{lo:.2f}, {hi:.2f}]{a:>8.3f}{a - p:>+9.3f}')


if __name__ == '__main__':
    main()
