# -*- coding: utf-8 -*-
"""Figure 1 — Conceptual framework: ethical risk and resilient governance
of AIGC historical visual symbols.

Conceptual diagram (not a statistical chart). Layers:
theory resources -> algorithmic encoding -> incommensurability thesis
-> generation bias / risk-transformation conditions / resilient governance,
with a dashed feedback loop from governance back to encoding.

Design notes (v3 — connectors):
- straight edge-to-edge connectors (shortest visual path, diagonals allowed);
- every arrow starts/ends ON a box border with a small clearance gap, never
  entering or touching another box;
- fan-out from the thesis box to the three bottom boxes uses three
  non-overlapping diagonals with distinct anchor points.
"""
from matplotlib.patches import FancyBboxPatch
from fig_style import apply_style, save_all, save_all_gray
import matplotlib.pyplot as plt

GAP = 0.06  # clearance between arrowhead and box border


def draw_fig1(save=True):
    apply_style()
    fig, ax = plt.subplots(figsize=(7.2, 5.6))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 12)
    ax.axis('off')

    def box(x, y, w, h, text, fs=8):
        p = FancyBboxPatch(
            (x, y), w, h,
            boxstyle="round,pad=0.06,rounding_size=0.12",
            linewidth=0.9, edgecolor='black', facecolor='white')
        ax.add_patch(p)
        ax.text(x + w / 2, y + h / 2, text, ha='center', va='center',
                fontsize=fs, linespacing=1.35)
        # border rectangle with pad, for reference:
        # actual extent: x-pad .. x+w+pad, y-pad .. y+h+pad (pad=0.06)
        return (x - 0.06, y - 0.06, x + w + 0.06, y + h + 0.06)

    def arrow_towards(x1, y1, bx0, by0, bx1, by1, dashed=False):
        """Straight arrow from point (x1, y1) to the nearest point on the
        border of box (bx0, by0, bx1, by1), stopping GAP short of it."""
        cx, cy = (bx0 + bx1) / 2, (by0 + by1) / 2
        dx, dy = cx - x1, cy - y1
        # param t where segment from (x1,y1) crosses the box border
        ts = []
        if dx != 0:
            for bx in (bx0, bx1):
                t = (bx - x1) / dx
                yy = y1 + t * dy
                if by0 <= yy <= by1:
                    ts.append(t)
        if dy != 0:
            for by in (by0, by1):
                t = (by - y1) / dy
                xx = x1 + t * dx
                if bx0 <= xx <= bx1:
                    ts.append(t)
        t = min(t for t in ts if t > 0) - GAP / max(abs(dx), abs(dy), 1e-9)
        ax.annotate('', xy=(x1 + t * dx, y1 + t * dy), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle='-|>', lw=0.9,
                                    linestyle='--' if dashed else '-',
                                    color='black', shrinkA=0, shrinkB=0))

    # ---- boxes (store extents for connector routing) --------------------
    ext_th_l = box(0.6, 10.3, 4.0, 1.4, "第三持存（斯蒂格勒）\n历史记忆的技术化生产")
    ext_th_r = box(5.4, 10.3, 4.0, 1.4, "文化表征（霍尔）\n意义的选择、压缩与自然化")
    ext_enc = box(3.0, 7.9, 4.0, 1.3, "算法编码\n技术记忆与符号实践的接触界面")
    ext_thesis = box(3.0, 5.8, 4.0, 1.3, "“不可通约”\n概率优化目标 ≠ 历史证据标准")
    ext_bias = box(0.3, 1.6, 3.0, 2.4,
                   "生成端偏差\n\n时代与物质文化拼贴\n身份标签化与关系扁平化\n视觉语法替代与生成幻觉",
                   fs=7)
    ext_risk = box(3.5, 1.6, 3.0, 2.4,
                   "风险转化条件\n\n来源不透明与高拟真传播\n平台重复推荐与放大\n机构采用缺乏专家核验",
                   fs=7)
    ext_gov = box(6.7, 1.6, 3.0, 2.4,
                  "韧性治理\n\n生成端知识约束与校准\n传播端来源凭证与追溯\n使用端分级与核验",
                  fs=7)

    # ---- connectors: shortest straight paths, edge-to-edge ---------------
    # theory boxes -> encoding (bottom edges to top edge, no crossing)
    arrow_towards(2.6, 10.3, *ext_enc)     # from bottom of left theory box
    arrow_towards(7.4, 10.3, *ext_enc)     # from bottom of right theory box
    # encoding -> thesis
    arrow_towards(5.0, 7.9, *ext_thesis)
    # thesis -> three bottom boxes (distinct anchors on thesis bottom edge)
    arrow_towards(3.6, 5.8, *ext_bias)
    arrow_towards(5.0, 5.8, *ext_risk)
    arrow_towards(6.4, 5.8, *ext_gov)

    # dashed feedback loop: governance -> encoding, single straight diagonal
    # (shortest path, no bends; starts on governance top border, ends GAP
    # short of the encoding right border — never entering another box)
    arrow_towards(8.2, 4.0, *ext_enc, dashed=True)

    if save:
        save_all(fig, 'fig1')
        save_all_gray(fig, 'fig1')
    return fig


if __name__ == '__main__':
    draw_fig1()
