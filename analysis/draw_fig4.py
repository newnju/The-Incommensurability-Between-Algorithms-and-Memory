# -*- coding: utf-8 -*-
"""Figure 4 — Dimension scores by prompt condition and condition contrasts
with equivalence band (two panels).

ALL data read from the coding workbook via fig_data (single source of truth):
- (a) dimension means per condition: sheet 提示条件汇总
- (b) contrasts + 95% CI: recomputed from sheets 编码员A/编码员B with the
  preregistered bootstrap (B=10000, seed 20260824, model-stratified;
  consensus = mean of coders, NA -> 0)

Note: the exploratory grade-2 proportions (20/54, 16/54, 26/54; Wilson CI)
are intentionally NOT plotted — they are reported in the manuscript text,
and the full counts remain in the public coding workbook (sheet
提示条件汇总).
"""
import numpy as np
from fig_style import apply_style, save_all
import matplotlib.pyplot as plt
import fig_data


def draw_fig4(save=True):
    apply_style()
    conds, dim_means, _g2 = fig_data.condition_summary()
    contrasts = fig_data.condition_contrasts()

    fig, axes = plt.subplots(
        1, 2, figsize=(9.5, 4.2),
        gridspec_kw={'width_ratios': [1.0, 1.25]})

    # (a) dimension-score means (D1 and D5, from workbook)
    ax = axes[0]
    d1 = dim_means['D1']
    d5 = dim_means['D5']
    x = np.arange(len(conds))
    width = 0.35
    ax.bar(x - width / 2, d1, width, color='black', edgecolor='black',
           linewidth=0.5, label='D1 建筑与场景')
    ax.bar(x + width / 2, d5, width, color='white', edgecolor='black',
           linewidth=0.5, hatch='///', label='D5 生成完整性')
    for i in range(len(conds)):
        ax.text(i - width / 2, d1[i] + 0.03, f'{d1[i]:.3f}',
                ha='center', fontsize=8)
        ax.text(i + width / 2, d5[i] + 0.03, f'{d5[i]:.3f}',
                ha='center', fontsize=8)
    ax.set_xticks(x)
    ax.set_xticklabels(conds)
    ax.set_ylabel('维度分均值（0—2）')
    ax.set_ylim(0, 2.0)
    ax.legend(frameon=False, loc='upper left', fontsize=8)
    ax.set_title('(a) 稳定维度分均值', loc='left')
    ax.spines[['top', 'right']].set_visible(False)

    # (b) condition contrasts, forest plot with equivalence band
    ax = axes[1]
    order = ['D1 P2-P1', 'D5 P2-P1', 'D1 P3-P2', 'D5 P3-P2']
    name_map = {
        'D1 P2-P1': 'D1 建筑与场景\nP2-P1',
        'D5 P2-P1': 'D5 生成完整性\nP2-P1',
        'D1 P3-P2': 'D1 建筑与场景\nP3-P2',
        'D5 P3-P2': 'D5 生成完整性\nP3-P2',
    }
    labels = [name_map[k] for k in order]
    means = np.array([contrasts[k][0] for k in order])
    lower = np.array([contrasts[k][1] for k in order])
    upper = np.array([contrasts[k][2] for k in order])
    y = np.arange(len(labels))
    ax.axvspan(-0.25, 0.25, color='0.90', zorder=0)
    ax.axvline(0, color='black', lw=0.8, zorder=1)
    for i in range(len(labels)):
        ax.errorbar(means[i], y[i],
                    xerr=np.array([[means[i] - lower[i]],
                                   [upper[i] - means[i]]]),
                    fmt='o', ms=4, color='black', ecolor='black',
                    elinewidth=0.9, capsize=2.5, capthick=0.9, zorder=3)
        ax.text(upper[i] + 0.01, y[i],
                f'{means[i]:+.3f} [{lower[i]:+.3f}, {upper[i]:+.3f}]',
                va='center', fontsize=8)
    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=8)
    ax.set_xlabel('维度分差异（95% CI）')
    ax.set_xlim(-0.30, 0.55)
    ax.set_title('(b) 条件对比：点估计与95% CI', loc='left')
    ax.text(-0.24, 3.55, '等效区间 ±0.25', fontsize=8, color='gray')
    ax.spines[['top', 'right']].set_visible(False)

    fig.tight_layout()
    if save:
        save_all(fig, 'fig4')
    return fig


if __name__ == '__main__':
    draw_fig4()
