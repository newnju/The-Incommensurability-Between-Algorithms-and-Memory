# -*- coding: utf-8 -*-
"""Data loader: reads ALL figure data directly from the coding workbook.

The workbook coding_data/per_image_coding_table_v1.0.xlsx is the single
source of truth (ground truth). No figure values are hard-coded.

Sheets used:
- 稳定性_留一: Bootstrap selection frequency pi_j and leave-one-model-out
  inclusion matrix (f1..f18 x M1..M6).
- 维度_Kappa: dimension-level linear-weighted kappa with 95% CI, pooled
  kappa, and overall criterion-Y kappa.
- 提示条件汇总: dimension means per condition and grade-2 proportions.
- 编码员A / 编码员B: per-image atomic indicators (condition contrasts for
  Fig. 4b are recomputed from these with the preregistered bootstrap:
  B=10000, seed 20260824, stratified by model, consensus = mean of coders,
  NA -> 0).
"""
import os
import warnings

import numpy as np
import openpyxl

HERE = os.path.dirname(os.path.abspath(__file__))
WORKBOOK = os.path.join(HERE, '..', 'coding_data',
                        'per_image_coding_table_v1.0.xlsx')

BOOT_B = 10000
BOOT_SEED = 20260824


def _load_workbook():
    warnings.filterwarnings('ignore')
    return openpyxl.load_workbook(WORKBOOK, data_only=True)


def stability_data():
    """Returns (labels, pi, matrix) from sheet 稳定性_留一."""
    wb = _load_workbook()
    ws = wb['稳定性_留一']
    labels, pi, mat = [], [], []
    for r in ws.iter_rows(min_row=2, values_only=True):
        if r[0] is None or not str(r[0]).startswith('f'):
            break
        labels.append(str(r[0]))
        pi.append(float(r[2]))
        mat.append([int(x) for x in r[3:9]])
    wb.close()
    return labels, np.array(pi), np.array(mat, dtype=int)


def kappa_data():
    """Returns dict with per-dimension kappa, pooled kappa, criterion-Y."""
    wb = _load_workbook()
    ws = wb['维度_Kappa']
    dims = {}
    pooled = crity = None
    for r in ws.iter_rows(min_row=1, values_only=True):
        key = r[0]
        if key is None:
            continue
        key = str(key)
        if key.startswith(('D1', 'D2', 'D3', 'D4', 'D5')):
            short = key.split()[0]          # 'D1' ... 'D5'
            dims[short] = (float(r[5]), float(r[6]), float(r[7]))
        elif key.startswith('微观合并'):
            pooled = (float(r[5]), float(r[6]), float(r[7]))
        elif key == '线性加权Kappa':        # criterion-Y row
            crity = (float(r[1]), float(r[2]), float(r[3]))
    wb.close()
    return {'dims': dims, 'pooled': pooled, 'criterion_Y': crity}


def condition_summary():
    """Returns (conditions, dim_means, grade2) from sheet 提示条件汇总.

    dim_means: {dim_short: [P1, P2, P3]} for D1..D5
    grade2: list of (condition, k, n) grade-2 counts.
    """
    wb = _load_workbook()
    ws = wb['提示条件汇总']
    rows = list(ws.iter_rows(values_only=True))
    conds, g2 = [], []
    for r in rows:
        if r[0] in ('P1', 'P2', 'P3') and isinstance(r[2], (int, float)):
            # Y=0..Y=2 counts at idx2..6, effective N at idx7
            g2.append((r[0], int(r[6]), int(r[7])))
    dim_means = {}
    for r in rows:
        if r[0] is None:
            continue
        key = str(r[0])
        if key[:2] in ('D1', 'D2', 'D3', 'D4', 'D5') and \
                all(isinstance(v, (int, float)) for v in r[1:4]):
            dim_means[key[:2]] = [float(r[1]), float(r[2]), float(r[3])]
    conds = ['P1', 'P2', 'P3']
    wb.close()
    return conds, dim_means, g2


def _consensus_recs():
    """Per-image records: (model, condition, D1, D5) with consensus scoring
    (mean of coder A and B, NA -> 0) for dimensions D1=f2 and D5=f18."""
    wb = _load_workbook()
    recs = {}
    for sheet in ('编码员A', '编码员B'):
        ws = wb[sheet]
        for r in ws.iter_rows(min_row=2, values_only=True):
            if r[0] is None:
                continue
            v = lambda x: 0.0 if x is None else float(x)
            rec = recs.setdefault(str(r[0]), {'model': r[1], 'cond': r[3]})
            rec.setdefault('vals', []).append((v(r[7]), v(r[23])))
    wb.close()
    out = []
    for iid in sorted(recs):
        rec = recs[iid]
        a, b = rec['vals']
        out.append((rec['model'], rec['cond'], (a[0] + b[0]) / 2,
                    (a[1] + b[1]) / 2))
    return out


def condition_contrasts():
    """Fig. 4b contrasts: {label: (point, lo, hi)} via preregistered
    stratified bootstrap (B=10000, seed 20260824)."""
    recs = _consensus_recs()
    models = sorted({r[0] for r in recs})
    vals = np.array([r[2:4] for r in recs], dtype=float)
    conds = np.array([r[1] for r in recs])
    idx = {m: {c: np.where((np.array([r[0] for r in recs]) == m) &
                           (conds == c))[0]
               for c in ('P1', 'P2', 'P3')}
           for m in models}
    rng = np.random.default_rng(BOOT_SEED)

    def boot(c1, c2, dim):
        diffs = np.empty(BOOT_B)
        for b in range(BOOT_B):
            s1, s2 = [], []
            for m in models:
                i1, i2 = idx[m][c1], idx[m][c2]
                s1 += list(vals[rng.choice(i1, i1.size, replace=True), dim])
                s2 += list(vals[rng.choice(i2, i2.size, replace=True), dim])
            diffs[b] = np.mean(s2) - np.mean(s1)
        point = np.mean(vals[:, dim][conds == c2]) - \
            np.mean(vals[:, dim][conds == c1])
        lo, hi = np.percentile(diffs, [2.5, 97.5])
        return point, lo, hi

    out = {}
    for dim, dname in ((0, 'D1'), (1, 'D5')):
        for c1, c2 in (('P1', 'P2'), ('P2', 'P3')):
            out[f'{dname} {c2}-{c1}'] = boot(c1, c2, dim)
    return out
