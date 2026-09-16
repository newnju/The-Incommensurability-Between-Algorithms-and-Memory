# -*- coding: utf-8 -*-
"""Figure 4 — Dimension scores by prompt condition, condition contrasts with
equivalence band, and exploratory grade-2 proportions with Wilson CIs.

ALL data read from the coding workbook via fig_data (single source of truth):
- (a) dimension means per condition: sheet 提示条件汇总
- (b) contrasts + 95% CI: recomputed from sheets 编码员A/编码员B with the
  preregistered bootstrap (B=10000, seed 20260824, model-stratified;
  consensus = mean of coders, NA -> 0)
- (c) grade-2 proportions: sheet 提示条件汇总 (Y=2 counts / effective N);
  Wilson 95% CI computed analytically
"""
import numpy as np
from fig_style import apply_style, save_all
import matplotlib.pyplot as plt
import fig_data


def wilson_ci(k, n, z=1.96):
    p = k / n
    denom = 1 + z ** 2 / n
    center = (p + z ** 2 / (2 * n)) / denom
    half = z * np.sqrt(p * (1 - p) / n + z ** 2 / (4 * n ** 2)) / denom
    return center - half, center + half


def draw_fig4(save=True):
    apply_style()
    conds, dim_means, g2 = fig_data.condition_summary()
    contrasts = fig_data.condition_contrasts()

    fig, axes = plt.subplots(
        1, 3, figsize=(13.5, 4.2),
        gridspec_kw={'width_ratios': [1.0, 1.2, 1.0]})

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

    # (c) exploratory grade-2 proportions, Wilson 95% CI (counts from sheet)
    ax = axes[2]
    n = g2[0][2]
    ks = np.array([k for _, k, _ in g2], dtype=float)
    props = ks / n
    lows, ups = zip(*(wilson_ci(int(k), n) for k in ks))
    lows, ups = np.array(lows), np.array(ups)
    ax.bar(x, props * 100, color='0.6', edgecolor='black',
           linewidth=0.5, width=0.6)
    ax.errorbar(x, props * 100,
                yerr=np.array([(props - lows) * 100, (ups - props) * 100]),
                fmt='none', ecolor='black',
                elinewidth=0.8, capsize=2.5, capthick=0.8)
    for i in range(len(conds)):
        ax.text(i, props[i] * 100 + 2,
                f'{props[i] * 100:.1f}%\n({int(ks[i])}/{n})',
                ha='center', fontsize=8)
    ax.set_xticks(x)
    ax.set_xticklabels(conds)
    ax.set_ylabel('2级失真比例（%）')
    ax.set_ylim(0, 70)
    ax.set_title('(c) 探索性：2级比例及Wilson 95% CI', loc='left')
    ax.spines[['top', 'right']].set_visible(False)

    fig.tight_layout()
    if save:
        save_all(fig, 'fig4')
    return fig


if __name__ == '__main__':
    draw_fig4()
