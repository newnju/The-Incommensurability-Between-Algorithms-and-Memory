# -*- coding: utf-8 -*-
"""Figure 2 — Atomic-indicator Bootstrap selection frequency, leave-one-model-
out stability matrix, and dimension-level reliability (kappa forest plot).

Data sources:
- (a) pi values: sheet 稳定性_留一 of coding_data/per_image_coding_table_v1.0.xlsx.
  Values below are PARTLY APPROXIMATE (read from the manuscript figure);
  replace with the raw workbook values before publication.
- (b) leave-one-model-out inclusion matrix: same sheet, columns 剔除M1..剔除M6
  (partly approximate here).
- (c) kappa estimates and 95% CI: sheet 维度_Kappa (as reported in the paper).
"""
import numpy as np
from fig_style import apply_style, save_all
import matplotlib.pyplot as plt

# (a) Bootstrap selection frequency pi, f1..f18  [APPROXIMATE for f3-f15 etc.]
PI = np.array([
    0.273, 0.732, 0.128, 0.137, 0.145, 0.234,
    0.298, 0.124, 0.098, 0.132, 0.203, 0.166,
    0.342, 0.342, 0.171, 0.539, 0.081, 0.995])
THRESH = 0.60

# (b) leave-one-model-out inclusion matrix (18 x 6)  [PARTLY APPROXIMATE]
MAT = np.zeros((18, 6), dtype=int)
MAT[17, :] = [1, 1, 1, 1, 1, 1]   # f18  6/6
MAT[1, :] = [1, 1, 1, 1, 1, 0]    # f2   5/6
MAT[15, :] = [1, 1, 1, 1, 0, 0]   # f16  4/6 (pi below threshold)
MAT[0, :] = [1, 1, 0, 0, 0, 0]    # f1
MAT[12, :] = [1, 1, 1, 1, 0, 0]   # f13  approx
MAT[14, :] = [1, 0, 1, 0, 0, 0]   # f15  approx
MAT[6, :] = [1, 1, 0, 0, 0, 0]    # f7   approx
for i in (2, 3, 4, 5, 7, 8, 9, 10, 11, 13, 16):
    MAT[i, 0] = 1                 # approx: selected only when dropping M1

# (c) dimension-level linear-weighted kappa, 95% CI (from 维度_Kappa sheet)
K_LABELS = ['D1', 'D2', 'D3', 'D4', 'D5', '合并κ', '效标Y']
K_MEAN = np.array([0.579, 0.649, 0.788, 0.407, 0.535, 0.671, 0.460])
K_LOW = np.array([0.476, 0.610, 0.742, 0.350, 0.419, 0.650, 0.346])
K_UPP = np.array([0.676, 0.686, 0.831, 0.462, 0.640, 0.692, 0.568])


def draw_fig2(save=True):
    apply_style()
    f_labels = [f'f{i}' for i in range(1, 19)]
    fig, axes = plt.subplots(
        1, 3, figsize=(13.5, 4.2),
        gridspec_kw={'width_ratios': [1.35, 1.15, 1.10]})

    # (a) Bootstrap selection frequency
    ax = axes[0]
    colors = ['#BDBDBD'] * 18
    colors[1] = '#2F5597'
    colors[17] = '#2F5597'
    ax.bar(np.arange(18), PI, color=colors, edgecolor='black',
           linewidth=0.4, width=0.72)
    ax.axhline(THRESH, ls='--', lw=0.8, color='#D62728')
    ax.text(17.5, THRESH + 0.02, '阈值 0.60', ha='right', va='bottom',
            fontsize=8, color='#D62728')
    ax.set_xticks(np.arange(18))
    ax.set_xticklabels(f_labels, fontsize=8)
    ax.set_ylabel('Bootstrap选择频率 π')
    ax.set_ylim(0, 1.05)
    for idx in (1, 17):
        ax.text(idx, PI[idx] + 0.03, f'{PI[idx]:.3f}', ha='center', fontsize=8)
    ax.set_title('(a) 选择频率（B=10000）', loc='left')
    ax.spines[['top', 'right']].set_visible(False)

    # (b) leave-one-model-out inclusion matrix
    ax = axes[1]
    ax.imshow(MAT, cmap='Greys', vmin=0, vmax=1, aspect='auto')
    ax.set_xticks(range(6))
    ax.set_xticklabels([f'M{i}' for i in range(1, 7)], fontsize=8)
    ax.set_yticks(range(18))
    ax.set_yticklabels(f_labels, fontsize=8)
    ax.set_xticks(np.arange(-0.5, 6, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, 18, 1), minor=True)
    ax.grid(which='minor', color='black', lw=0.3)
    ax.tick_params(which='minor', length=0)
    for i, c in enumerate(MAT.sum(axis=1)):
        ax.text(6.1, i, f'{c}/6', va='center', ha='left', fontsize=8)
    ax.set_xlim(-0.5, 6.8)
    ax.set_title('(b) 留一模型入选矩阵', loc='left')

    # (c) dimension-level kappa forest plot
    ax = axes[2]
    y = np.arange(len(K_LABELS))
    for i, (m, l, u) in enumerate(zip(K_MEAN, K_LOW, K_UPP)):
        face = 'black' if i in (0, 4, 5) else 'white'
        ax.errorbar(m, y[i], xerr=np.array([[m - l], [u - m]]),
                    fmt='o', ms=3.5, color='black', ecolor='black',
                    elinewidth=0.8, capsize=2, capthick=0.8,
                    markerfacecolor=face, markeredgecolor='black',
                    markeredgewidth=0.6)
        ax.text(u + 0.01, y[i], f'{m:.3f} [{l:.3f}, {u:.3f}]',
                va='center', fontsize=7.5)
    ax.set_yticks(y)
    ax.set_yticklabels(K_LABELS)
    ax.set_xlabel('线性加权 Kappa（95% CI）')
    ax.set_xlim(0.30, 1.05)
    ax.axvline(0.60, ls=':', lw=0.6, color='gray')
    ax.set_title('(c) 维度级信度', loc='left')
    ax.spines[['top', 'right']].set_visible(False)

    fig.tight_layout()
    if save:
        save_all(fig, 'fig2')
    return fig


if __name__ == '__main__':
    draw_fig2()
