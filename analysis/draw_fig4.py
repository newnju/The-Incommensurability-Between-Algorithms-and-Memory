# -*- coding: utf-8 -*-
"""Figure 4 — Dimension scores by prompt condition, condition contrasts with
equivalence band, and exploratory grade-2 proportions with Wilson CIs.

Data sources (all directly from the manuscript / workbook):
- (a) sheet 提示条件汇总: D1/D5 means per condition, n = 54 per condition.
- (b) condition contrasts with 95% CI; grey band = preregistered equivalence
  margin +/-0.25.
- (c) grade-2 proportions 20/54, 16/54, 26/54; Wilson 95% CI.
"""
import numpy as np
from fig_style import apply_style, save_all
import matplotlib.pyplot as plt


def wilson_ci(k, n, z=1.96):
    p = k / n
    denom = 1 + z ** 2 / n
    center = (p + z ** 2 / (2 * n)) / denom
    half = z * np.sqrt(p * (1 - p) / n + z ** 2 / (4 * n ** 2)) / denom
    return center - half, center + half


def draw_fig4(save=True):
    apply_style()
    fig, axes = plt.subplots(
        1, 3, figsize=(13.5, 4.2),
        gridspec_kw={'width_ratios': [1.0, 1.2, 1.0]})
    conditions = ['P1', 'P2', 'P3']

    # (a) dimension-score means
    ax = axes[0]
    d1 = [1.528, 1.593, 1.852]
    d5 = [1.481, 1.528, 1.667]
    x = np.arange(3)
    width = 0.35
    ax.bar(x - width / 2, d1, width, color='black', edgecolor='black',
           linewidth=0.5, label='D1 建筑与场景')
    ax.bar(x + width / 2, d5, width, color='white', edgecolor='black',
           linewidth=0.5, hatch='///', label='D5 生成完整性')
    for i in range(3):
        ax.text(i - width / 2, d1[i] + 0.03, f'{d1[i]:.3f}',
                ha='center', fontsize=8)
        ax.text(i + width / 2, d5[i] + 0.03, f'{d5[i]:.3f}',
                ha='center', fontsize=8)
    ax.set_xticks(x)
    ax.set_xticklabels(conditions)
    ax.set_ylabel('维度分均值（0—2）')
    ax.set_ylim(0, 2.0)
    ax.legend(frameon=False, loc='upper left', fontsize=8)
    ax.set_title('(a) 稳定维度分均值', loc='left')
    ax.spines[['top', 'right']].set_visible(False)

    # (b) condition contrasts, forest plot with equivalence band
    ax = axes[1]
    labels = ['D1 建筑与场景\nP2-P1', 'D5 生成完整性\nP2-P1',
              'D1 建筑与场景\nP3-P2', 'D5 生成完整性\nP3-P2']
    means = np.array([0.065, 0.046, 0.259, 0.139])
    lower = np.array([-0.065, -0.083, 0.130, 0.028])
    upper = np.array([0.204, 0.176, 0.389, 0.241])
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
    ax.set_title('(b) 条件对比', loc='left')
    ax.text(-0.24, 3.55, '等效区间 ±0.25', fontsize=8, color='gray')
    ax.spines[['top', 'right']].set_visible(False)

    # (c) exploratory grade-2 proportions, Wilson 95% CI
    ax = axes[2]
    n = 54
    ks = np.array([20, 16, 26])
    props = ks / n
    lows, ups = zip(*(wilson_ci(k, n) for k in ks))
    lows, ups = np.array(lows), np.array(ups)
    ax.bar(x, props * 100, color='0.6', edgecolor='black',
           linewidth=0.5, width=0.6)
    ax.errorbar(x, props * 100,
                yerr=np.array([(props - lows) * 100, (ups - props) * 100]),
                fmt='none', ecolor='black',
                elinewidth=0.8, capsize=2.5, capthick=0.8)
    for i in range(3):
        ax.text(i, props[i] * 100 + 2,
                f'{props[i] * 100:.1f}%\n({ks[i]}/{n})',
                ha='center', fontsize=8)
    ax.set_xticks(x)
    ax.set_xticklabels(conditions)
    ax.set_ylabel('2级失真比例（%）')
    ax.set_ylim(0, 70)
    ax.set_title('(c) 探索性：2级比例', loc='left')
    ax.spines[['top', 'right']].set_visible(False)

    fig.tight_layout()
    if save:
        save_all(fig, 'fig4')
    return fig


if __name__ == '__main__':
    draw_fig4()
