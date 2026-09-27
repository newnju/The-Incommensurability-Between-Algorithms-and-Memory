# -*- coding: utf-8 -*-
"""One-command reproduction of every number and figure in this repository.

    python analysis/run_all.py                 # everything (~4 min)
    python analysis/run_all.py --no-figures    # statistics + verification only
    python analysis/run_all.py --no-verify     # statistics + figures only
    python analysis/run_all.py --quick         # skip the B=1e6 kappa bootstrap
    python analysis/run_all.py --list          # show the plan and exit

What it does, in order:

1. `cart_analysis.py`        CART: full-data tree + leave-one-model-out counts
2. `bootstrap_selection.py`  bootstrap selection frequency pi_j (B = 10000)
3. `kappa_calculation.py`    kappa_g + 95% CI per dimension (B = 1e6, ~90 s)
4. `draw_fig1..4.py`         regenerate Figs. 1-4 (overwrites the committed files)
5. `verify_package.py`       assert the workbook matches the code

Steps 1-3 only print; they never write to the workbook.  Step 4 *does*
overwrite `analysis/fig1..fig4.*`, which is the point of a reproduction run —
pass `--no-figures` if you want to keep the committed files untouched.

Each step runs in its own interpreter, exactly as a reader would run it by
hand, so no step can be silently affected by another's import state.  The
script stops at the first failure and exits non-zero.
"""
import argparse
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
PY = sys.executable

STAT_STEPS = [
    ('cart_analysis.py',
     'CART: full-data tree + leave-one-model-out inclusion counts'),
    ('bootstrap_selection.py',
     'Bootstrap selection frequency pi_j (B = 10000)'),
    ('kappa_calculation.py',
     'Dimension / pooled / criterion-Y kappa with 95% CI (B = 1e6)'),
]
FIG_STEPS = [
    ('draw_fig1.py', 'Fig. 1 — conceptual framework'),
    ('draw_fig2.py', 'Fig. 2 — selection frequency + dimension reliability'),
    ('draw_fig3.py', 'Fig. 3 — real-image case panels'),
    ('draw_fig4.py', 'Fig. 4 — condition contrasts'),
]


def run_step(script, description, idx, total):
    print()
    print('=' * 78)
    print(f'[{idx}/{total}] {description}')
    print(f'        python {script}')
    print('=' * 78)
    t0 = time.time()
    proc = subprocess.run([PY, os.path.join(HERE, script)],
                          cwd=HERE, text=True)
    dt = time.time() - t0
    if proc.returncode != 0:
        print(f'\n!! {script} exited with code {proc.returncode} '
              f'after {dt:.1f} s — stopping.')
        return False
    print(f'-- ok ({dt:.1f} s)')
    return True


def main():
    ap = argparse.ArgumentParser(
        description='Reproduce every number and figure in this repository.')
    ap.add_argument('--no-figures', action='store_true',
                    help='skip the four plotting scripts (keeps committed files)')
    ap.add_argument('--no-verify', action='store_true',
                    help='skip the final workbook-vs-code verification')
    ap.add_argument('--quick', action='store_true',
                    help='pass --quick to verify_package.py (skips B=1e6 kappa)')
    ap.add_argument('--list', action='store_true',
                    help='show the step plan and exit')
    args = ap.parse_args()

    plan = list(STAT_STEPS)
    if not args.no_figures:
        plan += FIG_STEPS
    if not args.no_verify:
        plan += [('verify_package.py', 'Verify the workbook against the code')]

    if args.list:
        print('Planned steps:')
        for i, (s, d) in enumerate(plan, 1):
            print(f'  {i}. {s:<26} {d}')
        return 0

    print('=' * 78)
    print('Reproducing "The Incommensurability Between Algorithms and Memory"')
    print(f'python: {PY}')
    print(f'steps:  {len(plan)}')
    print('=' * 78)

    t0 = time.time()
    for i, (script, description) in enumerate(plan, 1):
        if script == 'verify_package.py':
            argv = [PY, os.path.join(HERE, script)]
            if args.quick:
                argv.append('--quick')
            print()
            print('=' * 78)
            print(f'[{i}/{len(plan)}] {description}')
            print('=' * 78)
            proc = subprocess.run(argv, cwd=HERE, text=True)
            if proc.returncode != 0:
                print(f'\n!! verification failed (exit {proc.returncode}).')
                return proc.returncode
        else:
            if not run_step(script, description, i, len(plan)):
                return 1

    dt = time.time() - t0
    print()
    print('=' * 78)
    print(f'ALL STEPS COMPLETED in {dt / 60:.1f} min')
    if not args.no_figures:
        print('Figures in analysis/ were regenerated from the workbook.')
    print('=' * 78)
    return 0


if __name__ == '__main__':
    sys.exit(main())
