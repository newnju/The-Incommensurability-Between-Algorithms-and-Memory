# -*- coding: utf-8 -*-
"""CART specification and leave-one-model-out indicator stability.

Reproduces the shallow regression CART reported in the manuscript
(Table 2; the "决策树细节" deposited for editorial reference).

Preregistered specification
---------------------------
- Target: consensus criterion Y (sheet 共识效标Y)
- Features: f1..f18, coder A/B mean, NA -> 0
- Estimator: sklearn DecisionTreeRegressor
- max_depth = 3, min_samples_leaf = 15, random_state = SEED
- Leave-one-model-out: 6 folds; each fold drops one model's 27 images and
  refits with the *same* hyperparameters and the *same* seed, so the six
  refits differ only in the training data.

Seed
----
SEED = 20260824 is used for every CART fit (full-data tree and all six
leave-one-out refits). See analysis/README.md for the seed policy.
"""
import numpy as np

from fig_data import full_dataset

SEED = 20260824
MAX_DEPTH = 3
MIN_SAMPLES_LEAF = 15

MODELS = ['M1', 'M2', 'M3', 'M4', 'M5', 'M6']


def fit_tree(X, y):
    """Fit the preregistered CART. Imported lazily to keep the module light."""
    from sklearn.tree import DecisionTreeRegressor
    return DecisionTreeRegressor(
        max_depth=MAX_DEPTH,
        min_samples_leaf=MIN_SAMPLES_LEAF,
        random_state=SEED,
    ).fit(X, y)


def splitting_variables(tree):
    """Indices (1-based, matching f1..f18) of features used for splitting."""
    return sorted({int(v) + 1 for v in tree.tree_.feature if v >= 0})


def full_tree_report():
    X, y, _meta = full_dataset()
    tree = fit_tree(X, y)
    return {
        'depth': tree.get_depth(),
        'leaves': int(tree.tree_.n_leaves),
        'splits': splitting_variables(tree),
    }


def leave_one_model_out():
    """Returns {model_dropped: [splitting variables]}."""
    X, y, meta = full_dataset()
    models = np.array([m for m, _ in meta])
    out = {}
    for m in MODELS:
        keep = models != m
        out[m] = splitting_variables(fit_tree(X[keep], y[keep]))
    return out


def main():
    rep = full_tree_report()
    print('Full-data tree')
    print(f'  depth            = {rep["depth"]}')
    print(f'  terminal nodes   = {rep["leaves"]}')
    print(f'  splitting vars   = {["f%d" % v for v in rep["splits"]]}')

    loo = leave_one_model_out()
    print('\nLeave-one-model-out (splitting variables per fold)')
    counts = {j: 0 for j in range(1, 19)}
    for m in MODELS:
        print(f'  drop {m}: {["f%d" % v for v in loo[m]]}')
        for v in loo[m]:
            counts[v] += 1
    print('\nInclusion counts (of 6 folds)')
    for j in range(1, 19):
        print(f'  f{j:<3} {counts[j]}/6')


if __name__ == '__main__':
    main()
