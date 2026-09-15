# -*- coding: utf-8 -*-
"""Figure 3 — Schematic case panels for the three prompt conditions.

Qualitative case figure (NOT a statistical chart, NOT a reproduction of the
actual generated images). Each panel is a vector schematic of the typical
scene composition with leader-line annotations of the key visual features,
plus image ID and consensus criterion Y.

The real sample images (M1_P1_07.png, M1_P2_08.png, M1_P3_05.png) are
deposited in the Zenodo archive; if terms/ethics clearance allows, panels can
be swapped to the real images with the same annotation layout (see README in
analysis/).
"""
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Polygon
from fig_style import apply_style, save_all


# ---------- drawing primitives ----------
def draw_ground(ax, y=0.12, color='#D9D2C5'):
    ax.add_patch(Rectangle((0.02, 0.02), 0.96, y,
                           facecolor=color, edgecolor='none'))


def draw_wall(ax, x, y, w, h, brick=True, color='#C9BFAE'):
    """City wall / gate tower with brick joints and a gate opening."""
    ax.add_patch(Rectangle((x, y), w, h,
                           facecolor=color, edgecolor='black', lw=0.6))
    if brick:
        for i in range(1, 4):
            ax.plot([x, x + w], [y + i * h / 4, y + i * h / 4],
                    color='#8A8073', lw=0.3)
        for j in range(1, 6):
            ax.plot([x + j * w / 6, x + j * w / 6], [y, y + h],
                    color='#8A8073', lw=0.3)
    ax.add_patch(Rectangle((x + w * 0.35, y), w * 0.3, h * 0.55,
                           facecolor='#3A3A3A', edgecolor='black', lw=0.4))


def draw_person(ax, x, y, scale=1.0, hat='none', color='#6E8FA8'):
    """Simplified figure: head + body + legs, hat selects role type."""
    head_r = 0.018 * scale
    ax.add_patch(Circle((x, y + 0.11 * scale), head_r,
                        facecolor='#E8C9A8', edgecolor='black', lw=0.4))
    ax.add_patch(Polygon([[x - 0.022 * scale, y + 0.09 * scale],
                          [x + 0.022 * scale, y + 0.09 * scale],
                          [x + 0.030 * scale, y + 0.02 * scale],
                          [x - 0.030 * scale, y + 0.02 * scale]],
                         closed=True, facecolor=color,
                         edgecolor='black', lw=0.4))
    ax.plot([x - 0.012 * scale, x - 0.015 * scale],
            [y + 0.02 * scale, y], color='black', lw=0.6)
    ax.plot([x + 0.012 * scale, x + 0.015 * scale],
            [y + 0.02 * scale, y], color='black', lw=0.6)
    if hat == 'official':
        ax.add_patch(Polygon([[x - 0.020 * scale, y + 0.128 * scale],
                              [x + 0.020 * scale, y + 0.128 * scale],
                              [x + 0.012 * scale, y + 0.150 * scale],
                              [x - 0.012 * scale, y + 0.150 * scale]],
                             closed=True, facecolor='#2F2F2F',
                             edgecolor='black', lw=0.4))
    elif hat == 'fur':
        ax.add_patch(Circle((x, y + 0.135 * scale), 0.016 * scale,
                            facecolor='#7A5A3A', edgecolor='black', lw=0.4))
    elif hat == 'helmet':
        ax.add_patch(Polygon([[x - 0.021 * scale, y + 0.125 * scale],
                              [x + 0.021 * scale, y + 0.125 * scale],
                              [x, y + 0.160 * scale]],
                             closed=True, facecolor='#8A8A8A',
                             edgecolor='black', lw=0.5))


def draw_table(ax, x, y, w=0.10, h=0.05):
    """High table (Ming-Qing style anachronism in P1)."""
    ax.add_patch(Rectangle((x, y + h), w, 0.008,
                           facecolor='#8B5A2B', edgecolor='black', lw=0.4))
    ax.plot([x + w * 0.15, x + w * 0.15], [y, y + h], color='black', lw=0.8)
    ax.plot([x + w * 0.85, x + w * 0.85], [y, y + h], color='black', lw=0.8)


def draw_camel(ax, x, y, scale=1.0):
    ax.add_patch(Polygon([[x, y + 0.02 * scale],
                          [x + 0.05 * scale, y + 0.02 * scale],
                          [x + 0.05 * scale, y + 0.06 * scale],
                          [x + 0.03 * scale, y + 0.075 * scale],
                          [x + 0.02 * scale, y + 0.06 * scale],
                          [x, y + 0.06 * scale]],
                         closed=True, facecolor='#C9A66B',
                         edgecolor='black', lw=0.5))
    ax.plot([x + 0.01 * scale, x + 0.01 * scale], [y, y + 0.02 * scale],
            color='black', lw=0.6)
    ax.plot([x + 0.04 * scale, x + 0.04 * scale], [y, y + 0.02 * scale],
            color='black', lw=0.6)


def draw_plaque(ax, x, y, w=0.20, h=0.04, text='', ok=False):
    """Inscription plaque: ok=True (near-correct), ok=False (garbled)."""
    fc = '#F5E9C8' if ok else '#F0D9D9'
    ax.add_patch(Rectangle((x, y), w, h,
                           facecolor=fc, edgecolor='black', lw=0.5))
    ax.text(x + w / 2, y + h / 2, text, ha='center', va='center', fontsize=5)


def callout(ax, xy, xytext, text, color='#B22222'):
    ax.annotate(text, xy=xy, xytext=xytext, fontsize=6.5, color=color,
                ha='left', va='center',
                arrowprops=dict(arrowstyle='-', lw=0.5, color=color,
                                connectionstyle='arc3,rad=0.15'))


def panel_caption(ax, text):
    ax.text(0.5, -0.06, text, ha='center', va='top', fontsize=8,
            transform=ax.transAxes)


# ---------- main figure ----------
def draw_fig3(save=True):
    apply_style()
    fig, axes = plt.subplots(1, 3, figsize=(10.5, 4.2))

    # ============ (a) P1 low-constraint baseline ============
    ax = axes[0]
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    draw_ground(ax)
    draw_wall(ax, 0.05, 0.12, 0.90, 0.22)
    draw_table(ax, 0.20, 0.12, w=0.12, h=0.06)
    draw_table(ax, 0.60, 0.12, w=0.12, h=0.06)
    draw_person(ax, 0.30, 0.14, scale=1.3, hat='official', color='#3B5C7A')
    draw_person(ax, 0.45, 0.14, scale=1.2, hat='fur', color='#8A5A3A')
    draw_camel(ax, 0.72, 0.14, scale=1.0)
    ax.add_patch(Circle((0.25, 0.20), 0.018, facecolor='#4A6FA5',
                        edgecolor='black', lw=0.4))
    ax.add_patch(Circle((0.65, 0.20), 0.018, facecolor='#4A6FA5',
                        edgecolor='black', lw=0.4))
    callout(ax, (0.30, 0.25), (0.02, 0.62), '汉官—胡商二元模式\n（高频原型）')
    callout(ax, (0.24, 0.16), (0.02, 0.88), '高桌高凳、明清青花\n（时代错置拼贴）')
    callout(ax, (0.50, 0.30), (0.55, 0.80), '城门/关隘/集市\n（固定场景）')
    ax.set_title('(a) P1 低约束基线', loc='left', pad=4)
    panel_caption(ax, 'M1_P1_07   |   Y = 1.5')

    # ============ (b) P2 evidentiary constraints ============
    ax = axes[1]
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    draw_ground(ax)
    draw_wall(ax, 0.05, 0.12, 0.90, 0.22)
    draw_plaque(ax, 0.34, 0.355, w=0.32, h=0.045, text='安西都护府', ok=True)
    ax.text(0.70, 0.375, '＋后世年款', fontsize=6.5, color='#B22222',
            va='center')
    draw_person(ax, 0.30, 0.14, scale=1.3, hat='official', color='#3B5C7A')
    draw_person(ax, 0.48, 0.14, scale=1.2, hat='fur', color='#8A5A3A')
    draw_camel(ax, 0.72, 0.14, scale=1.0)
    ax.add_patch(Rectangle((0.20, 0.13), 0.03, 0.02, facecolor='#A88B5A',
                           edgecolor='black', lw=0.4))
    ax.add_patch(Rectangle((0.62, 0.13), 0.03, 0.02, facecolor='#A88B5A',
                           edgecolor='black', lw=0.4))
    callout(ax, (0.50, 0.38), (0.55, 0.68), '题榜较准\n但字序倒错/生造字')
    callout(ax, (0.35, 0.16), (0.02, 0.55), '服饰/器物约束\n（错置收敛）')
    callout(ax, (0.74, 0.16), (0.60, 0.88), '残留后世元素\n（部分正确拼贴）')
    ax.set_title('(b) P2 考据约束', loc='left', pad=4)
    panel_caption(ax, 'M1_P2_08   |   Y = 1.5')

    # ============ (c) P3 negative-frame ============
    ax = axes[2]
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    draw_ground(ax)
    draw_wall(ax, 0.05, 0.12, 0.90, 0.22, color='#B8AE9E')
    draw_person(ax, 0.28, 0.14, scale=1.5, hat='helmet', color='#8A8A8A')
    draw_person(ax, 0.42, 0.14, scale=1.4, hat='helmet', color='#8A8A8A')
    ax.plot([0.25, 0.20], [0.20, 0.34], color='#3A3A3A', lw=1.0)
    ax.plot([0.45, 0.50], [0.20, 0.34], color='#3A3A3A', lw=1.0)
    draw_person(ax, 0.65, 0.14, scale=1.1, hat='fur', color='#8A5A3A')
    draw_camel(ax, 0.80, 0.14, scale=0.9)
    draw_plaque(ax, 0.34, 0.355, w=0.32, h=0.045, text='安西都护府', ok=False)
    ax.text(0.68, 0.375, '字序错乱', fontsize=6.5, color='#B22222',
            va='center')
    callout(ax, (0.30, 0.28), (0.02, 0.62), '边关查验原型\n（防御对峙）')
    callout(ax, (0.22, 0.34), (0.02, 0.88), '模板化铠甲\n后世兵器')
    callout(ax, (0.50, 0.38), (0.55, 0.72), '题榜文字错乱')
    ax.text(0.5, -0.13,
            '注：本面板为对刻板表征的批判性分析，\n非对其描绘方式的认可或传播',
            ha='center', va='top', fontsize=6, color='#555555',
            transform=ax.transAxes)
    ax.set_title('(c) P3 负向关系框架', loc='left', pad=4)
    panel_caption(ax, 'M1_P3_05   |   Y = 1.5')

    fig.tight_layout(rect=[0, 0.06, 1, 1])
    if save:
        save_all(fig, 'fig3')
    return fig


if __name__ == '__main__':
    draw_fig3()
