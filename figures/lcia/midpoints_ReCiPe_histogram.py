# Traduit de LCA/examples/chapter_lca/midpoints_ReCiPe_histogram.py ; valeurs sources conservées.
from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FuncFormatter

DEFAULT_OUTPUT = Path(__file__).with_name("midpoints_ReCiPe_histogram.svg")
FIGURE_WIDTH = 40 / 3
FIGURE_HEIGHT = 6
AXIS_LABEL_FONT_SIZE = 14
TICK_FONT_SIZE = 14

IMPACT_CATEGORIES = [
    "Formation de particules fines",
    "Raréfaction des ressources fossiles",
    "Écotoxicité en eau douce",
    "Eutrophisation des eaux douces",
    "Changement climatique",
    "Toxicité humaine cancérogène",
    "Toxicité humaine non cancérogène",
    "Rayonnements ionisants",
    "Utilisation des sols",
    "Écotoxicité marine",
    "Eutrophisation marine",
    "Raréfaction des ressources minérales",
    "Formation d’ozone : santé humaine",
    "Formation d’ozone : écosystèmes terrestres",
    "Appauvrissement de l’ozone stratosphérique",
    "Acidification terrestre",
    "Écotoxicité terrestre",
    "Consommation d’eau"
]

BRUT_IMPACT_VALUES = {
    "LFP": [
        10.33413, 1116.68399, 1204.61337, 3.41374, 4489.17732, 5.94337E4,
        5.54666E6, 401.83124, 57.74173, 6.76509E6, 0.19257, 101.58093,
        13.84829, 13.98165, 0.00254, 22.28916, 1.13117E4, 43.30929,
    ],
    "LTO": [
        62.95796, 5813.97946, 5462.19299, 17.25381, 2.19537E4, 2.23875E5,
        2.52378E7, 3423.57697, 358.53458, 3.06152E7, 3.08794, 889.97276,
        66.02100, 66.79219, 0.01342, 160.37640, 8.64581E4, 417.55079,
    ],
    "NMC": [
        44.14736, 4227.66177, 3891.69125, 13.92748, 1.54307E4, 1.63282E5,
        1.76676E7, 2340.88686, 290.98044, 2.14005E7, 2.51412, 600.32140,
        47.18342, 47.76675, 0.00984, 111.61424, 9.12098E4, 307.58246,
    ],
}


def normalize_on_max(impact_values: dict[str, list[float]]) -> dict[str, list[float]]:
    keys = list(impact_values.keys())
    n_categories = len(next(iter(impact_values.values())))
    max_per_category = [max(impact_values[key][i] for key in keys) for i in range(n_categories)]

    return {
        key: [
            value / max_value if max_value != 0 else 0.0
            for value, max_value in zip(values, max_per_category)
        ]
        for key, values in impact_values.items()
    }


IMPACT_VALUES = normalize_on_max(BRUT_IMPACT_VALUES)


def build_histogram(output_path: Path) -> Path:
    x = np.arange(len(IMPACT_CATEGORIES))
    width = 0.24
    offsets = (-width, 0.0, width)
    series = list(IMPACT_VALUES.items())
    colors = plt.cm.magma(np.linspace(0.18, 0.82, len(series)))

    fig, ax = plt.subplots(figsize=(FIGURE_WIDTH, FIGURE_HEIGHT), constrained_layout=True)
    fig.patch.set_facecolor("none")
    fig.patch.set_alpha(0)
    ax.set_facecolor("none")

    for offset, color, (chemistry, values) in zip(offsets, colors, series):
        ax.bar(
            x + offset,
            values,
            width=width,
            label=chemistry,
            color=color,
            edgecolor="none",
            linewidth=0,
        )

    ax.set_ylabel("Normalisation 0–maximum", fontsize=AXIS_LABEL_FONT_SIZE)
    ax.set_xticks(x)
    ax.set_xticklabels(IMPACT_CATEGORIES, rotation=35, ha="right", fontsize=TICK_FONT_SIZE)
    ax.legend(title="Technologie de batterie", frameon=False, fontsize=12, ncol=3, loc="lower left", bbox_to_anchor=(0, 1.02))
    ax.set_ylim(0, 1.05)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda value, _: f"{value:.1f}".replace(".", ",")))
    ax.tick_params(axis="y", labelsize=TICK_FONT_SIZE)
    ax.tick_params(axis="both", length=0)
    for spine in ax.spines.values():
        spine.set_visible(False)
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
        help="Chemin du fichier de sortie (par defaut: single_score_histogram.svg).",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output_path = build_histogram(args.output)
    print(output_path)


if __name__ == "__main__":
    main()
