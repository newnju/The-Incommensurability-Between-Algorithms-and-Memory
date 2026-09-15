# -*- coding: utf-8 -*-
"""Figure 1 — Conceptual framework: ethical risk and resilient governance
of AIGC historical visual symbols.

Conceptual diagram (not a statistical chart). Layers:
theory resources -> algorithmic encoding -> incommensurability thesis
-> generation bias / risk-transformation conditions / resilient governance,
with a dashed feedback loop from governance back to encoding.

Design notes (v2):
- straight orthogonal connectors with rounded corners (no long diagonals);
- single visual column: theory -> encoding -> thesis -> three bottom boxes;
- feedback loop routed along the right margin with two 90-degree turns;
- slightly larger boxes and tighter spacing for print legibility.
"""
from matplotlib.patches import FancyBboxPatch
from fig_style import apply_style, save_all
import matplotlib.pyplot as plt


def draw_fig1(save=True):
    apply_style()
    fig, ax = plt.subplots(figsize=(7.2, 5.6))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 12)
    ax.axis('off')

    def box(x, y, w, h, text, fs=8, bold_first=False):
        p = FancyBboxPatch(
            (x, y), w, h,
            boxstyle="round,pad=0.06,rounding_size=0.12",
            linewidth=0.9, edgecolor='black', facecolor='white')
        ax.add_patch(p)
        if bold_first:
            lines = text.split('\n')
            ax.text(x + w / 2, y + h / 2, '\n'.join(lines),
                    ha='center', va='center', fontsize=fs,
                    linespacing=1.35)
        else:
            ax.text(x + w / 2, y + h / 2, text,
                    ha='center', va='center', fontsize=fs,
                    linespacing=1.35)

    def connect_v(x, y1, y2):
        """Straight vertical connector with arrowhead at (x, y2)."""
        ax.annotate('', xy=(x, y2), xytext=(x, y1),
                    arrowprops=dict(arrowstyle='-|>', lw=0.9,
                                    color='black', shrinkA=0, shrinkB=0))

    def elbow(x1, y1, x2, y2, xm):
        """Orthogonal 3-segment connector: horizontal -> vertical -> horizontal,
        arrowhead at (x2, y2)."""
        ax.plot([x1, xm, xm], [y1, y1, y2], color='black', lw=0.9,
                solid_capstyle='round', zorder=1)
        ax.annotate('', xy=(x2, y2), xytext=(xm, y2),
                    arrowprops=dict(arrowstyle='-|>', lw=0.9,
                                    color='black', shrinkA=0, shrinkB=0))

    # ---- Layer 1: theoretical resources -------------------------------
    box(0.6, 10.3, 4.0, 1.4, "第三持存（斯蒂格勒）\n历史记忆的技术化生产")
    box(5.4, 10.3, 4.0, 1.4, "文化表征（霍尔）\n意义的选择、压缩与自然化")

    # ---- Layer 2: algorithmic encoding --------------------------------
    box(3.0, 7.9, 4.0, 1.3, "算法编码\n技术记忆与符号实践的接触界面")

    # ---- Layer 3: core thesis ------------------------------------------
    box(3.0, 5.8, 4.0, 1.3, "“不可通约”\n概率优化目标 ≠ 历史证据标准")

    # ---- Layer 4: three bottom boxes -----------------------------------
    box(0.3, 1.6, 3.0, 2.4,
        "生成端偏差\n\n时代与物质文化拼贴\n身份标签化与关系扁平化\n视觉语法替代与生成幻觉",
        fs=7)
    box(3.5, 1.6, 3.0, 2.4,
        "风险转化条件\n\n来源不透明与高拟真传播\n平台重复推荐与放大\n机构采用缺乏专家核验",
        fs=7)
    box(6.7, 1.6, 3.0, 2.4,
        "韧性治理\n\n生成端知识约束与校准\n传播端来源凭证与追溯\n使用端分级与核验",
        fs=7)

    # ---- Connectors -----------------------------------------------------
    # theory boxes converge into encoding: vertical drop then horizontal merge
    elbow(2.6, 10.3, 4.4, 9.2, 2.6)      # left theory -> encoding (left side)
    elbow(7.4, 10.3, 5.6, 9.2, 7.4)      # right theory -> encoding (right side)
    connect_v(5.0, 7.9, 7.1)             # encoding -> thesis

    # thesis fans out to the three bottom boxes (orthogonal)
    elbow(4.0, 5.8, 1.8, 4.0, 4.0)
    connect_v(5.0, 5.8, 4.0)
    elbow(6.0, 5.8, 8.2, 4.0, 6.0)

    # dashed feedback loop: governance -> encoding, routed on the right margin
    ax.plot([9.7, 9.7], [4.0, 8.55], ls='--', lw=0.9, color='black',
            solid_capstyle='round', zorder=1)
    ax.annotate('', xy=(7.0, 8.55), xytext=(9.7, 8.55),
                arrowprops=dict(arrowstyle='-|>', lw=0.9, ls='--',
                                color='black', shrinkA=0, shrinkB=0))

    if save:
        save_all(fig, 'fig1')
    return fig


if __name__ == '__main__':
    draw_fig1()
