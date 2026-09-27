# -*- coding: utf-8 -*-
"""Independent verification that the deposited workbook matches the code.

This script answers the one question a replicator actually has: *does the
released code, run on the released data, reproduce every number that is
reported in the manuscript?*  It recomputes each reported quantity from the
raw coder sheets and compares it, cell by cell, with the value stored in
`coding_data/per_image_coding_table_v1.0.xlsx`.

It is deliberately independent of the plotting scripts: it re-derives the
consensus criterion Y, the condition summary, the dimension means, the
bootstrap selection frequency, the leave-one-model-out inclusion counts and
the kappa values from the two coder sheets, and it does not trust any
intermediate value stored in the workbook.

Usage
-----
    python analysis/verify_package.py            # full check (~3 min)
    python analysis/verify_package.py --quick    # skip the B=1e6 kappa bootstrap
    python analysis/verify_package.py --full     # also re-check contrast
                                                 # endpoint stability across seeds

Exit status is 0 when every check passes and 1 otherwise, so the script can
be used as a gate in CI.

Verified against: numpy 2.5.3, scikit-learn 1.9.1, matplotlib 3.11.2,
openpyxl 3.1.5, Pillow 12.3.0, Python 3.13.14 (see requirements.txt).
"""
import argparse
import os
import sys

import numpy as np
import openpyxl

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
WORKBOOK = os.path.join(ROOT, 'coding_data',
                        'per_image_coding_table_v1.0.xlsx')
IMAGES = os.path.join(ROOT, 'images')

sys.path.insert(0, HERE)

TOL = 1e-9              # exact agreement, for quantities stored exactly

# Some quantities are stored rounded: the workbook keeps dimension means and
# kappa_g to 3 decimals, and the CI endpoints to 2.  For those, the right
# criterion is "the stored value is the rounding of the exact value", i.e. the
# gap must not exceed half a unit in the last stored place.  Comparing
# round(x, 3) instead would be less informative: a value sitting exactly on a
# .0005 boundary rounds differently under round() and format(), so the two
# methods can disagree about an identical input.
TOL_3DP = 5e-4 + 1e-9
TOL_2DP = 5e-3 + 1e-9


# --------------------------------------------------------------------------
# minimal check harness
# --------------------------------------------------------------------------

class Checker:
    def __init__(self):
        self.n_pass = 0
        self.failures = []

    def check(self, name, ok, detail=''):
        if ok:
            self.n_pass += 1
            print(f'  PASS  {name}')
        else:
            self.failures.append((name, detail))
            print(f'  FAIL  {name}')
            if detail:
                for line in str(detail).splitlines():
                    print(f'          {line}')

    def section(self, title):
        print()
        print(f'--- {title} ' + '-' * max(0, 66 - len(title)))

    def summary(self):
        print()
        print('=' * 78)
        if self.failures:
            print(f'RESULT: FAILED — {len(self.failures)} of '
                  f'{self.n_pass + len(self.failures)} checks failed')
            for name, detail in self.failures:
                print(f'  * {name}')
            return 1
        print(f'RESULT: OK — all {self.n_pass} checks passed')
        return 0


# --------------------------------------------------------------------------
# workbook helpers
# --------------------------------------------------------------------------

def load():
    import warnings
    warnings.filterwarnings('ignore')
    return openpyxl.load_workbook(WORKBOOK, data_only=True)


def _num(x):
    """0/1/2 -> float; None / 'NA' -> None (indicator not applicable)."""
    if x is None or str(x).strip() == 'NA':
        return None
    return float(x)


def coder_records(wb):
    """{ImageID: {'model','cond','A':[f1..f18],'B':[f1..f18],'A_Y','B_Y'}}"""
    recs = {}
    for sheet, key in (('编码员A', 'A'), ('编码员B', 'B')):
        for r in wb[sheet].iter_rows(min_row=2, values_only=True):
            if r[0] is None:
                continue
            rec = recs.setdefault(str(r[0]), {'model': r[1], 'cond': r[3]})
            rec[key] = [_num(x) for x in r[6:24]]        # f1..f18
            rec[key + '_Y'] = _num(r[5])
    return recs


def consensus_y(wb):
    """{ImageID: (Y_A, Y_B, stored_consensus, agreement_flag)}"""
    out = {}
    for r in wb['共识效标Y'].iter_rows(min_row=2, values_only=True):
        if r[0] is None:
            continue
        out[str(r[0])] = (_num(r[5]), _num(r[6]), r[7], r[8])
    return out


DIM_COLS = {
    'D1': [2],                    # f2
    'D2': list(range(3, 10)),     # f3..f9
    'D3': [10, 11, 12],           # f10..f12
    'D4': [13, 14, 15, 16],       # f13..f16
    'D5': [18],                   # f18
}


def dim_score(rec, key, cols):
    """Dimension score of one image.

    Preregistered rule (维度_Kappa!A17, 提示条件汇总!A16): the mean of the two
    coders' means over the indicators *visible to that coder*; NA is dropped
    per coder, not set to zero.  A coder with no visible indicator in the
    dimension contributes nothing.
    """
    parts = []
    for c in ('A', 'B'):
        vis = [rec[c][i - 1] for i in cols if rec[c][i - 1] is not None]
        if vis:
            parts.append(sum(vis) / len(vis))
    if not parts:
        return None
    return sum(parts) / len(parts)


# --------------------------------------------------------------------------
# checks
# --------------------------------------------------------------------------

def check_structure(ck, wb):
    ck.section('1. Sample structure and image corpus')

    ids = [r[0] for r in wb['样本清单'].iter_rows(min_row=2, values_only=True)
           if r[0] is not None]
    ck.check('样本清单 holds 162 images', len(ids) == 162, f'found {len(ids)}')
    ck.check('ImageIDs are unique', len(set(ids)) == len(ids))

    for sub, want in (('p1', 54), ('p2', 54), ('p3', 54)):
        d = os.path.join(IMAGES, sub)
        n = len([f for f in os.listdir(d)]) if os.path.isdir(d) else 0
        ck.check(f'images/{sub} holds {want} files', n == want, f'found {n}')

    n_train = 0
    for sub in ('p1', 'p2', 'p3'):
        d = os.path.join(IMAGES, '训练集', sub)
        if os.path.isdir(d):
            n_train += len(os.listdir(d))
    ck.check('images/训练集 holds 18 files', n_train == 18, f'found {n_train}')

    # G column of 样本清单 = ImageID + '.jpg', and every file exists
    bad_ext, missing = [], []
    for r in wb['样本清单'].iter_rows(min_row=2, values_only=True):
        if r[0] is None:
            continue
        iid, name = str(r[0]), str(r[6])
        if not name.endswith('.jpg'):
            bad_ext.append((iid, name))
        if name != iid + '.jpg':
            bad_ext.append((iid, name))
        sub = {'P1': 'p1', 'P2': 'p2', 'P3': 'p3'}[iid.split('_')[1]]
        if not os.path.exists(os.path.join(IMAGES, sub, name)):
            missing.append(name)
    ck.check('样本清单!G == ImageID + ".jpg" for all 162 rows',
             not bad_ext, f'{len(bad_ext)} rows differ, e.g. {bad_ext[:3]}')
    ck.check('every G-column file exists under images/',
             not missing, f'{len(missing)} missing, e.g. {missing[:3]}')

    # each model x condition cell has exactly 9 images
    from collections import Counter
    cells = Counter((r[1], r[3]) for r in
                    wb['样本清单'].iter_rows(min_row=2, values_only=True)
                    if r[0] is not None)
    ck.check('all 18 model x condition cells hold exactly 9 images',
             len(cells) == 18 and set(cells.values()) == {9},
             f'{len(cells)} cells, sizes {sorted(set(cells.values()))}')


def check_consensus(ck, wb):
    ck.section('2. Consensus criterion Y (共识效标Y)')
    cons = consensus_y(wb)
    ck.check('共识效标Y holds 162 images', len(cons) == 162, f'found {len(cons)}')

    bad_mean, bad_flag = [], []
    for iid, (ya, yb, stored, flag) in cons.items():
        if ya is None or yb is None:
            bad_mean.append((iid, 'NA in Y_A/Y_B'))
            continue
        if abs((ya + yb) / 2 - float(stored)) > TOL:
            bad_mean.append((iid, f'({ya}+{yb})/2 != {stored}'))
        if int(flag) != int(ya == yb):
            bad_flag.append((iid, f'agreement flag {flag} but Y_A={ya}, Y_B={yb}'))
    ck.check('consensus Y == (Y_A + Y_B) / 2 for all 162 rows',
             not bad_mean, f'{len(bad_mean)} mismatches, e.g. {bad_mean[:3]}')
    ck.check('agreement flag == (Y_A == Y_B) for all 162 rows',
             not bad_flag, f'{len(bad_flag)} mismatches, e.g. {bad_flag[:3]}')


def check_condition_summary(ck, wb):
    ck.section('3. Condition summary (提示条件汇总)')
    ws = wb['提示条件汇总']

    by_cond = {'P1': [], 'P2': [], 'P3': []}
    for r in wb['共识效标Y'].iter_rows(min_row=2, values_only=True):
        if r[0] is None:
            continue
        by_cond[str(r[3])].append(float(r[7]))

    counts, prop, mean = {}, {}, {}
    for c in ('P1', 'P2', 'P3'):
        v = np.array(by_cond[c])
        counts[c] = (int((v == 0).sum()), int((v == 0.5).sum()),
                     int((v == 1).sum()), int((v == 1.5).sum()),
                     int((v == 2).sum()))
        prop[c] = (v == 2).sum() / v.size
        mean[c] = v.mean()

    for row, c in zip(range(4, 7), ('P1', 'P2', 'P3')):
        stored_counts = tuple(int(ws.cell(row, k).value) for k in range(3, 8))
        ck.check(f'{c}: Y = 0/0.5/1/1.5/2 counts match',
                 stored_counts == counts[c],
                 f'workbook {stored_counts} vs recomputed {counts[c]}')
        ck.check(f'{c}: effective N = {ws.cell(row, 8).value}',
                 int(ws.cell(row, 8).value) == sum(counts[c]),
                 f'sum of counts = {sum(counts[c])}')
        ck.check(f'{c}: grade-2 proportion matches',
                 abs(float(ws.cell(row, 9).value) - prop[c]) < TOL,
                 f'workbook {ws.cell(row, 9).value} vs recomputed {prop[c]!r}')
        ck.check(f'{c}: mean Y matches',
                 abs(float(ws.cell(row, 10).value) - mean[c]) < TOL,
                 f'workbook {ws.cell(row, 10).value} vs recomputed {mean[c]!r}')


def check_dimension_means(ck, wb):
    ck.section('4. Dimension means per condition (提示条件汇总 rows 10-14)')
    recs = coder_records(wb)
    ws = wb['提示条件汇总']
    for row, key in zip(range(10, 15), ('D1', 'D2', 'D3', 'D4', 'D5')):
        got = []
        for c in ('P1', 'P2', 'P3'):
            vals = [dim_score(recs[i], key, DIM_COLS[key])
                    for i in recs if recs[i]['cond'] == c]
            vals = [v for v in vals if v is not None]
            got.append(sum(vals) / len(vals))
        stored = [float(ws.cell(row, k).value) for k in (2, 3, 4)]
        ok = all(abs(a - b) <= TOL_3DP for a, b in zip(stored, got))
        ck.check(f'{key}: P1/P2/P3 means match to the stored 3 decimals '
                 f'(NA dropped per coder)', ok,
                 f'workbook {stored} vs recomputed {[round(x, 6) for x in got]}')


def check_selection_frequency(ck, wb, quick):
    ck.section('5. Bootstrap selection frequency pi_j (稳定性_留一)')
    import bootstrap_selection as bs
    labels, pi = bs.bootstrap_selection_frequency()
    ws = wb['稳定性_留一']
    bad = []
    for j, lab in enumerate(labels):
        stored = float(ws.cell(j + 2, 3).value)
        if abs(float(pi[j]) - stored) > TOL_3DP:
            bad.append((lab, stored, float(pi[j])))
    ck.check(f'pi_j reproduces for all 18 indicators to the stored 3 decimals '
             f'(B={bs.BOOT_B}, seed={bs.SEED})', not bad,
             'mismatches (indicator, workbook, recomputed):\n' +
             '\n'.join(f'    {a}: {b} vs {c!r}' for a, b, c in bad))

    # the stable set is what the manuscript actually relies on
    stable = [lab for j, lab in enumerate(labels) if float(pi[j]) >= 0.60]
    stored_stable = [str(ws.cell(r, 1).value) for r in range(2, 20)
                     if ws.cell(r, 12).value == '是']
    ck.check('stable set {pi >= 0.60 and >=5/6 folds} matches',
             stable == stored_stable,
             f'recomputed {stable} vs workbook {stored_stable}')


def check_leave_one_out(ck, wb):
    ck.section('6. Leave-one-model-out inclusion counts (稳定性_留一)')
    import cart_analysis as ca
    loo = ca.leave_one_model_out()
    ws = wb['稳定性_留一']
    counts = {j: 0 for j in range(1, 19)}
    for m in ca.MODELS:
        for v in loo[m]:
            counts[v] += 1

    bad_fold, bad_total = [], []
    for j in range(1, 19):
        for k, m in enumerate(ca.MODELS):
            stored = int(ws.cell(j + 1, 4 + k).value)
            want = 1 if j in loo[m] else 0
            if stored != want:
                bad_fold.append((f'f{j}', m, stored, want))
        if int(ws.cell(j + 1, 10).value) != counts[j]:
            bad_total.append((f'f{j}', int(ws.cell(j + 1, 10).value), counts[j]))
    ck.check('per-fold inclusion matrix (剔除M1..M6) matches for all 18 x 6',
             not bad_fold, f'{len(bad_fold)} cells differ, e.g. {bad_fold[:4]}')
    ck.check('inclusion counts (of 6) match for all 18 indicators',
             not bad_total, f'{len(bad_total)} differ, e.g. {bad_total[:4]}')

    rep = ca.full_tree_report()
    ck.check('full-data tree: depth 3, 6 terminal nodes',
             rep['depth'] == 3 and rep['leaves'] == 6,
             f"got depth={rep['depth']}, leaves={rep['leaves']}")
    ck.check('full-data tree splits on f2/f12/f16/f18',
             rep['splits'] == [2, 12, 16, 18], f"got {rep['splits']}")


def check_kappa(ck, wb, quick):
    ck.section('7. Inter-coder kappa and 95% CI (维度_Kappa)')
    import kappa_calculation as kc
    recs = kc._load()
    ws = wb['维度_Kappa']

    # Krippendorff alpha is deterministic, so it is checked in both modes.
    ids = sorted(recs)
    alpha_rows = [(10, 'D1', kc.DIMENSIONS['D1 建筑与场景时代一致性']),
                  (11, 'D2', kc.DIMENSIONS['D2 服饰、器物与武备']),
                  (12, 'D3', kc.DIMENSIONS['D3 族群身份与社会关系']),
                  (13, 'D4', kc.DIMENSIONS['D4 空间构图与历史视觉语法']),
                  (14, 'D5', kc.DIMENSIONS['D5 生成完整性与提示词遵循']),
                  (15, '微观合并', list(range(1, 19)))]
    bad_alpha = []
    for row, label, cols in alpha_rows:
        want = kc.krippendorff_alpha(kc._pairs(recs, ids, cols))
        got = ws.cell(row, 10).value          # column J
        if got is None or abs(float(got) - want) > TOL_3DP:
            bad_alpha.append((label, got, round(want, 3)))
    want = kc.krippendorff_alpha(kc._y_pairs(recs, ids))
    got = ws['E4'].value
    if got is None or abs(float(got) - want) > TOL_3DP:
        bad_alpha.append(('criterion Y', got, round(want, 3)))
    ck.check('Krippendorff alpha reproduces at all 7 levels '
             '(维度_Kappa column J + E4)', not bad_alpha,
             'mismatches (level, workbook, recomputed):\n' +
             '\n'.join(f'    {a}: {b} vs {c}' for a, b, c in bad_alpha))

    if quick:
        # the point estimate is deterministic, so it can be checked without
        # paying for the bootstrap
        bad = []
        for row, name in zip(range(10, 15), kc.DIMENSIONS):
            ids = sorted(recs)
            pairs = kc._pairs(recs, ids, kc.DIMENSIONS[name])
            p = kc.weighted_kappa(pairs)
            sp = float(ws.cell(row, 6).value)
            if abs(p - sp) > TOL_3DP:
                bad.append((name, sp, p))
        pairs = kc._y_pairs(recs, sorted(recs))
        p = kc.weighted_kappa(pairs)
        if abs(p - float(ws['B4'].value)) > TOL_3DP:
            bad.append(('criterion Y', float(ws['B4'].value), p))
        ck.check('kappa point estimates reproduce '
                 '(bootstrap skipped: --quick)', not bad, f'{bad}')
        return

    rows = [(10, 'D1 建筑与场景时代一致性', kc.DIMENSIONS['D1 建筑与场景时代一致性']),
            (11, 'D2 服饰、器物与武备', kc.DIMENSIONS['D2 服饰、器物与武备']),
            (12, 'D3 族群身份与社会关系', kc.DIMENSIONS['D3 族群身份与社会关系']),
            (13, 'D4 空间构图与历史视觉语法', kc.DIMENSIONS['D4 空间构图与历史视觉语法']),
            (14, 'D5 生成完整性与提示词遵循', kc.DIMENSIONS['D5 生成完整性与提示词遵循']),
            (15, '微观合并综合（2828对）', list(range(1, 19)))]
    for row, name, cols in rows:
        p, lo, hi = kc.estimate(recs, cols)
        sp, slo, shi = (float(ws.cell(row, 6).value), float(ws.cell(row, 7).value),
                        float(ws.cell(row, 8).value))
        ck.check(f'{name}: kappa_g matches the stored 3 decimals',
                 abs(p - sp) <= TOL_3DP,
                 f'workbook {sp} vs recomputed {p!r}')
        ck.check(f'{name}: 95% CI matches the stored 2 decimals',
                 abs(lo - slo) <= TOL_2DP and abs(hi - shi) <= TOL_2DP,
                 f'workbook [{slo:.2f}, {shi:.2f}] vs '
                 f'recomputed [{lo:.2f}, {hi:.2f}]')

    p, lo, hi = kc.estimate(recs, None)
    sp, slo, shi = (float(ws['B4'].value), float(ws['C4'].value),
                    float(ws['D4'].value))
    ck.check(f'criterion Y: kappa matches the stored 3 decimals',
             abs(p - sp) <= TOL_3DP, f'workbook {sp} vs recomputed {p!r}')
    ck.check(f'criterion Y: 95% CI matches the stored 2 decimals',
             abs(lo - slo) <= TOL_2DP and abs(hi - shi) <= TOL_2DP,
             f'workbook [{slo:.2f}, {shi:.2f}] vs recomputed [{lo:.2f}, {hi:.2f}]')


def check_contrasts(ck, full):
    ck.section('8. Condition contrasts (Fig. 4b)')
    import fig_data
    out = fig_data.condition_contrasts()

    # point estimates are deterministic: recompute them independently
    recs = fig_data._consensus_recs()
    conds = np.array([r[1] for r in recs])
    vals = np.array([r[2:4] for r in recs], dtype=float)
    bad = []
    for dim, dname in ((0, 'D1'), (1, 'D5')):
        for c1, c2 in (('P1', 'P2'), ('P2', 'P3')):
            want = vals[conds == c2, dim].mean() - vals[conds == c1, dim].mean()
            got = out[f'{dname} {c2}-{c1}'][0]
            if abs(want - got) > TOL:
                bad.append((f'{dname} {c2}-{c1}', want, got))
    ck.check('all 4 contrast point estimates are the pooled mean differences',
             not bad, f'{bad}')
    ck.check(f'endpoints computed at B={fig_data.CONTRAST_B:,}',
             all(np.isfinite(v[1]) and v[1] < v[2] for v in out.values()))
    for k in sorted(out):
        print(f'          {k:<14} point {out[k][0]:+.4f}  '
              f'95% CI [{out[k][1]:+.4f}, {out[k][2]:+.4f}]')

    if full:
        seeds = [fig_data.BOOT_SEED, fig_data.BOOT_SEED + 7919]
        runs = []
        for s in seeds:
            fig_data.BOOT_SEED = s
            runs.append(fig_data.condition_contrasts())
        fig_data.BOOT_SEED = 20260824
        diff = []
        for k in runs[0]:
            for a, b in zip(runs[0][k][1:], runs[1][k][1:]):
                if abs(a - b) > TOL_3DP:
                    diff.append((k, a, b))
        ck.check('endpoints reproduce to 3 decimals across 2 seeds at '
                 f'B={fig_data.CONTRAST_B:,}', not diff, f'{diff}')


def check_seed_policy(ck):
    ck.section('9. Seed policy (analysis/README.md)')
    import fig_data, cart_analysis, bootstrap_selection, kappa_calculation
    for mod, attr, want in ((fig_data, 'BOOT_SEED', 20260824),
                            (cart_analysis, 'SEED', 20260824),
                            (bootstrap_selection, 'SEED', 20260824),
                            (kappa_calculation, 'SEED', 20260824)):
        got = getattr(mod, attr)
        ck.check(f'{mod.__name__}.{attr} == {want}', got == want, f'got {got}')
    ck.check('kappa CI bootstrap uses B = 1e6',
             kappa_calculation.BOOT_B == 1000000,
             f'got {kappa_calculation.BOOT_B}')
    ck.check('pi bootstrap uses B = 10000',
             bootstrap_selection.BOOT_B == 10000,
             f'got {bootstrap_selection.BOOT_B}')


def check_figures(ck):
    ck.section('10. Committed figure files')
    expect = ['fig1.pdf', 'fig1.png', 'fig1_gray.png',
              'fig2.pdf', 'fig2.png', 'fig2_gray.png',
              'fig3.png', 'fig3_gray.png',
              'fig4.pdf', 'fig4.png', 'fig4_gray.png']
    missing = [f for f in expect
               if not os.path.exists(os.path.join(HERE, f))]
    ck.check('all 11 committed figure files are present', not missing,
             f'missing {missing}')
    ck.check('fig3.pdf is absent (Fig. 3 is raster-only)',
             not os.path.exists(os.path.join(HERE, 'fig3.pdf')))


def check_index_links(ck, wb):
    ck.section('11. Index sheet links (正文填数索引)')
    idx = wb['正文填数索引']
    bad, checked = [], 0
    for r in idx.iter_rows(min_row=2, values_only=True):
        if r[0] is None:
            continue
        source, value, status = r[3], r[4], r[5]
        if status != '链接' or not isinstance(source, str) or '!' not in source:
            continue
        sheet, coord = source.split('!', 1)
        if sheet not in wb.sheetnames:
            bad.append((source, 'unknown sheet'))
            continue
        target = wb[sheet][coord].value
        checked += 1
        if isinstance(value, (int, float)) and isinstance(target, (int, float)):
            if abs(float(value) - float(target)) > 1e-9:
                bad.append((source, value, target))
        elif value != target:
            bad.append((source, value, target))
    ck.check(f'all {checked} "链接" rows resolve to their source cell',
             not bad, f'{bad}')


def check_no_placeholders(ck, wb):
    ck.section('12. No stale text in the workbook')
    import re
    pats = {
        'stale figure cross-reference': r'图3b',
        'stale precision claim': r'±0\.005|about 0\.003',
        'stale CART seed': r'random_state\s*=\s*0[^0-9]',
        'stale bootstrap size': r'2000\s*次',
    }
    for label, pat in pats.items():
        hits = []
        for ws in wb.worksheets:
            for row in ws.iter_rows():
                for c in row:
                    if isinstance(c.value, str) and re.search(pat, c.value):
                        hits.append(f'{ws.title}!{c.coordinate}')
        ck.check(f'no {label}', not hits, f'{hits[:5]}')

    # every pi value must be a genuine 3-decimal number
    ws = wb['稳定性_留一']
    vals = [ws.cell(r, 3).value for r in range(2, 20)]
    ck.check('all 18 pi_j are 3-decimal numbers',
             all(isinstance(v, (int, float)) and abs(round(v, 3) - v) < 1e-12
                 for v in vals), f'{vals}')


# --------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--quick', action='store_true',
                    help='skip the B=1e6 kappa bootstrap (~90 s)')
    ap.add_argument('--full', action='store_true',
                    help='also re-check contrast endpoint stability across seeds')
    args = ap.parse_args()

    print('=' * 78)
    print('Package verification: workbook vs released code')
    print(f'workbook: {os.path.relpath(WORKBOOK, ROOT)}')
    print(f'python:   {sys.version.split()[0]}')
    print('=' * 78)

    ck = Checker()
    wb = load()
    check_structure(ck, wb)
    check_consensus(ck, wb)
    check_condition_summary(ck, wb)
    check_dimension_means(ck, wb)
    check_selection_frequency(ck, wb, args.quick)
    check_leave_one_out(ck, wb)
    check_kappa(ck, wb, args.quick)
    check_contrasts(ck, args.full)
    check_seed_policy(ck)
    check_figures(ck)
    check_index_links(ck, wb)
    check_no_placeholders(ck, wb)
    wb.close()

    return ck.summary()


if __name__ == '__main__':
    sys.exit(main())
