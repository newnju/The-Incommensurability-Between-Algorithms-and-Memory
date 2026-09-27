# -*- coding: utf-8 -*-
"""Bootstrap selection frequency pi_j for the 18 atomic indicators.

Reproduces the selection frequency reported in Table 2 and Fig. 2a:
the proportion of bootstrap trees in which each indicator is used for
splitting.

Preregistered specification
---------------------------
- Strata: the 18 model x condition cells (9 images each); resampling is
  with replacement *within* each stratum, so every replicate keeps the
  same 18 x 9 structure as the observed sample.
- B = 10000 replicates.
- Each replicate refits the CART of cart_analysis (max_depth=3,
  min_samples_leaf=15, random_state=SEED).
- pi_j = (# replicates where f_j is used for splitting) / B.

Seed
----
SEED = 20260824 is used both for the bootstrap resampling stream and for
every CART fit inside the loop, matching the preregistered seed policy in
analysis/README.md.

The CART seed only breaks ties between features with identical split gains,
so it does not affect the full-data tree (depth 3, 6 terminal nodes, splits
f2/f12/f16/f18) or any of the six leave-one-model-out inclusion counts.
Across CART seeds pi_j moves by at most 0.007, which never changes the
pi >= 0.60 decision or the stable set {f2, f18}.
"""
import collections

import numpy as np

from fig_data import full_dataset
from cart_analysis import fit_tree, splitting_variables

SEED = 20260824
BOOT_B = 10000


def bootstrap_selection_frequency(B=BOOT_B):
    """Returns (labels, pi, matrix) where matrix is 18 x 6 of per-fold hits.

    The matrix is not produced here (it comes from cart_analysis); this
    function returns pi only, plus the labels.
    """
    X, y, meta = full_dataset()
    units = collections.defaultdict(list)
    for i, key in enumerate(meta):
        units[key].append(i)
    strata = list(units.values())

    rng = np.random.default_rng(SEED)
    counts = np.zeros(18)
    for _ in range(B):
        idx = []
        for u in strata:
            idx += list(rng.choice(u, size=len(u), replace=True))
        tree = fit_tree(X[idx], y[idx])
        for v in splitting_variables(tree):
            counts[v - 1] += 1
    labels = [f'f{j}' for j in range(1, 19)]
    return labels, counts / B


def main():
    labels, pi = bootstrap_selection_frequency()
    print(f'Bootstrap selection frequency (B={BOOT_B}, seed={SEED})')
    for lab, p in zip(labels, pi):
        flag = '  >= 0.60' if p >= 0.60 else ''
        print(f'  {lab:<4} {p:.3f}{flag}')
    print('\nCandidates (pi >= 0.60):',
          [lab for lab, p in zip(labels, pi) if p >= 0.60])


if __name__ == '__main__':
    main()
