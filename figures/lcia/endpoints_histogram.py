# Traduit de LCA/examples/chapter_lca/endpoints_histogram.py ; valeurs sources conservées.
from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FuncFormatter

DEFAULT_OUTPUT = Path(__file__).with_name("endpoints_histogram.svg")
Y_AXIS_UNIT = ""
AXIS_LABEL_FONT_SIZE = 14
TICK_FONT_SIZE = 14
BAR_LABEL_FONT_SIZE = 14
LEGEND_FONT_SIZE = 14

IMPACT_CATEGORIES = [
    "Qualité des écosystèmes",
    "Santé humaine",
    "Ressources",
]

IMPACT_VALUES = {
    "LFP": [287.23464, 2037.72124, 221.86873],
    "LTO": [1365.42909, 9225.41477, 1392.98574],
    "NMC": [968.88599, 6425.61728, 1020.69912],
}


def build_histogram(output_path: Path) -> Path:
    x = np.arange(len(IMPACT_CATEGORIES))
    width = 0.24
    offsets = (-width, 0.0, width)
    series = list(IMPACT_VALUES.items())
    colors = plt.cm.magma(np.linspace(0.18, 0.82, len(series)))

    fig, ax = plt.subplots(figsize=(10, 6), constrained_layout=True)
    fig.patch.set_facecolor("none")
    fig.patch.set_alpha(0)
    ax.set_facecolor("none")

    for offset, color, (chemistry, values) in zip(offsets, colors, series):
        bars = ax.bar(
            x + offset,
            values,
            width=width,
            label=chemistry,
            color=color,
            edgecolor="none",
            linewidth=0,
        )
        ax.bar_label(
            bars,
            labels=[f"{value:,.0f}".replace(",", " ") for value in values],
            padding=3,
            fontsize=BAR_LABEL_FONT_SIZE,
        )

    ax.set_ylabel("Points", fontsize=AXIS_LABEL_FONT_SIZE)
    ax.set_xticks(x, IMPACT_CATEGORIES)
    ax.tick_params(axis="x", labelsize=TICK_FONT_SIZE)
    ax.tick_params(axis="y", labelsize=TICK_FONT_SIZE)
    ax.yaxis.set_major_formatter(
        FuncFormatter(lambda value, _: f"{value:,.0f} {Y_AXIS_UNIT}".replace(",", " "))
    )
    ax.tick_params(axis="both", length=0)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.legend(
        title="Technologie de batterie",
        fontsize=LEGEND_FONT_SIZE,
        title_fontsize=LEGEND_FONT_SIZE,
        frameon=False,
    )
    ax.grid(axis="y", linestyle="--", alpha=0.35)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=300, transparent=True)
    plt.close(fig)
    return output_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Cree un histogramme groupe pour les impacts LFP, LTO et NMC."
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Chemin du fichier de sortie (par defaut: endpoints_histogram.svg).",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output_path = build_histogram(args.output)
    print(output_path)


if __name__ == "__main__":
    main()
