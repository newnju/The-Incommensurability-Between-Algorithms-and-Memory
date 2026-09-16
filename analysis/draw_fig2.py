# -*- coding: utf-8 -*-
"""Figure 2 — Atomic-indicator Bootstrap selection frequency and dimension-
level reliability (two panels).

ALL data read from the coding workbook via fig_data (single source of truth):
- (a) pi values: sheet 稳定性_留一, column Bootstrap选择频率πj
- (b) kappa + 95% CI: sheet 维度_Kappa

Note: the leave-one-model-out inclusion matrix (sheet 稳定性_留一, cols
剔除M1..剔除M6) is intentionally NOT plotted as a panel — the counts are
already reported in manuscript Table 2 and the text; the full matrix remains
available in the public coding workbook.
"""
import numpy as np
from fig_style import apply_style, save_all
import matplotlib.pyplot as plt
import fig_data


def draw_fig2(save=True):
    apply_style()
    f_labels, PI, _MAT = fig_data.stability_data()
    KD = fig_data.kappa_data()
    n_f = len(f_labels)

    fig, axes = plt.subplots(
        1, 2, figsize=(11.0, 4.2),
        gridspec_kw={'width_ratios': [1.5, 1.1]})

    # (a) Bootstrap selection frequency
    ax = axes[0]
    colors = ['#BDBDBD'] * n_f
    for i, p in enumerate(PI):
        if p >= 0.60:
            colors[i] = '#2F5597'
    ax.bar(np.arange(n_f), PI, color=colors, edgecolor='black',
           linewidth=0.4, width=0.72)
    ax.axhline(0.60, ls='--', lw=0.8, color='#D62728')
    ax.text(n_f - 0.5, 0.62, '阈值 0.60', ha='right', va='bottom',
            fontsize=8, color='#D62728')
    ax.set_xticks(np.arange(n_f))
    ax.set_xticklabels(f_labels, fontsize=8)
    ax.set_ylabel('Bootstrap选择频率 π')
    ax.set_ylim(0, 1.05)
    for i, p in enumerate(PI):
        ax.text(i, p + 0.02, f'{p:.3f}', ha='center', va='bottom',
                fontsize=6.5, rotation=90)
    ax.set_title('(a) 10000次模型分层Bootstrap选择频率', loc='left')
    ax.spines[['top', 'right']].set_visible(False)

    # (b) dimension-level kappa forest plot (values from workbook)
    ax = axes[1]
    labels = list(KD['dims']) + ['合并κ', '效标Y']
    means = np.array([KD['dims'][d][0] for d in KD['dims']] +
                     [KD['pooled'][0], KD['criterion_Y'][0]])
    lower = np.array([KD['dims'][d][1] for d in KD['dims']] +
                     [KD['pooled'][1], KD['criterion_Y'][1]])
    upper = np.array([KD['dims'][d][2] for d in KD['dims']] +
                     [KD['pooled'][2], KD['criterion_Y'][2]])
    y = np.arange(len(labels))
    for i in range(len(labels)):
        face = 'black' if i in (0, 4, 5) else 'white'
        ax.errorbar(means[i], y[i],
                    xerr=np.array([[means[i] - lower[i]],
                                   [upper[i] - means[i]]]),
                    fmt='o', ms=3.5, color='black', ecolor='black',
                    elinewidth=0.8, capsize=2, capthick=0.8,
                    markerfacecolor=face, markeredgecolor='black',
                    markeredgewidth=0.6)
        ax.text(upper[i] + 0.01, y[i],
                f'{means[i]:.3f} [{lower[i]:.3f}, {upper[i]:.3f}]',
                va='center', fontsize=7.5)
    ax.set_yticks(y)
    ax.set_yticklabels(labels)
    ax.set_xlabel('线性加权 Kappa（95% CI）')
    ax.set_xlim(0.30, 1.05)
    ax.axvline(0.60, ls=':', lw=0.6, color='gray')
    ax.set_title('(b) 维度信度≠筛选稳定性', loc='left')
    ax.spines[['top', 'right']].set_visible(False)

    fig.tight_layout()
    if save:
        save_all(fig, 'fig2')
    return fig


if __name__ == '__main__':
    draw_fig2()
