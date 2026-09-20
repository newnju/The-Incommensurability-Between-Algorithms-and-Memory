# -*- coding: utf-8 -*-
"""Figure 3 — Real-image case panels for the three prompt conditions.

Each panel shows the ACTUAL generated sample image from the repository image
corpus (images/p1|M2|M3/...), with leader-line annotations of the key visual
features and the image ID + consensus criterion Y beneath.

Images used (also archived at full resolution on Zenodo):
- (a) M1_P1_07  (P1 low-constraint baseline)
- (b) M1_P2_08  (P2 evidentiary constraints)
- (c) M1_P3_05  (P3 negative-frame)
"""
import os

import matplotlib.image as mpimg
from fig_style import apply_style, save_all, save_all_gray
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
IMAGES = os.path.join(HERE, '..', 'images')

PANELS = [
    ('M1_P1_07', os.path.join(IMAGES, 'p1', 'M1_P1_07.jpg'),
     '(a) P1 低约束基线', 1.5),
    ('M1_P2_08', os.path.join(IMAGES, 'p2', 'M1_P2_08.jpg'),
     '(b) P2 考据约束', 1.5),
    ('M1_P3_05', os.path.join(IMAGES, 'p3', 'M1_P3_05.jpg'),
     '(c) P3 负向关系框架', 1.5),
]


def draw_fig3(save=True):
    apply_style()
    # 宋体四号 = 14pt, enlarged by two sizes to 16pt (三号), applied to all in-figure text (titles + captions)
    song = {'fontfamily': ['SimSun', 'NSimSun', 'serif'],
            'fontsize': 16}
    fig, axes = plt.subplots(1, 3, figsize=(12.0, 5.2))

    for ax, (iid, path, title, y_val) in zip(axes, PANELS):
        img = mpimg.imread(path)
        ax.imshow(img)
        ax.axis('off')
        ax.set_title(title, loc='left', pad=4, **song)
        ax.text(0.5, -0.04, f'{iid}   |   Y = {y_val}',
                ha='center', va='top', transform=ax.transAxes, **song)

    fig.tight_layout(rect=[0, 0.02, 1, 1])
    if save:
        save_all(fig, 'fig3')
        save_all_gray(fig, 'fig3')
    return fig


if __name__ == '__main__':
    draw_fig3()
