# -*- coding: utf-8 -*-
"""Shared matplotlib style for manuscript figures (SCI print standards).

Single-column ~3.5 in, double-column ~7.2 in; 7-9 pt fonts; 600 dpi output;
Type-42 (embedded, editable) fonts in PDF/PS.
"""
import matplotlib.pyplot as plt

RC = {
    'font.family': 'sans-serif',
    'font.sans-serif': ['SimHei', 'Microsoft YaHei', 'Noto Sans CJK SC',
                        'Arial Unicode MS', 'Arial'],
    'axes.unicode_minus': False,
    # Word-safe sizes: figure is rendered at ~7.2 in wide, then shrunk in
    # Word to ~6.3 cm column width (~35%). Fonts below survive that shrink.
    'font.size': 10,
    'axes.labelsize': 10,
    'axes.titlesize': 10,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'legend.fontsize': 8.5,
    'axes.linewidth': 1.0,
    'xtick.major.width': 1.0,
    'ytick.major.width': 1.0,
    'xtick.major.size': 3.5,
    'ytick.major.size': 3.5,
    'savefig.dpi': 600,
    'figure.dpi': 150,
    'pdf.fonttype': 42,
    'ps.fonttype': 42,
}


def apply_style():
    plt.rcParams.update(RC)


def save_all(fig, stem):
    """Save one figure as PDF (vector) and 600-dpi TIFF/PNG."""
    fig.savefig(f'{stem}.pdf', bbox_inches='tight')
    fig.savefig(f'{stem}.tiff', dpi=600, bbox_inches='tight')
    fig.savefig(f'{stem}.png', dpi=200, bbox_inches='tight')  # preview only


def save_all_gray(fig, stem):
    """Grayscale variants for print: render PNG then convert to 8-bit gray."""
    import io
    from PIL import Image
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=600, bbox_inches='tight')
    buf.seek(0)
    Image.open(buf).convert('L').save(f'{stem}_gray.png')
    fig.savefig(f'{stem}_gray.pdf', bbox_inches='tight')
