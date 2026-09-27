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


def save_all(fig, stem, pdf=True):
    """Save one figure as a 200-dpi PNG preview, plus a vector PDF.

    Set pdf=False for figures built from bitmaps (e.g. Fig. 3, whose panels
    are real images): a PDF of those only re-embeds the same bitmaps with no
    vector benefit, and came to ~20 MB.

    No TIFF is written: the manuscript uses the grayscale PNGs produced by
    save_all_gray, and the 600-dpi TIFFs were 35-60 MB each (uncompressed,
    ~150 MB across figures) for an output nobody consumed.

    CreationDate is suppressed so the PDFs are byte-reproducible: matplotlib
    otherwise stamps the current time into /CreationDate, which also changes
    the derived /ID.  Re-running run_all.py then rewrites three PDFs that git
    reports as modified even though not a single glyph has changed.
    """
    if pdf:
        fig.savefig(f'{stem}.pdf', bbox_inches='tight',
                    metadata={'CreationDate': None})
    fig.savefig(f'{stem}.png', dpi=200, bbox_inches='tight')  # preview only


def save_all_gray(fig, stem):
    """Grayscale variant (the version used in the manuscript).

    300 dpi is the print standard for raster figures and keeps the files
    small; the colour PNG preview is 200 dpi.
    """
    import io
    from PIL import Image
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=300, bbox_inches='tight')
    buf.seek(0)
    Image.open(buf).convert('L').save(f'{stem}_gray.png', optimize=True)
