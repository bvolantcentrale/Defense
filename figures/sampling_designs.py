"""Generate the two transparent sampling illustrations for slide 37."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import qmc


OUTPUT = Path(__file__).resolve().parent
PART_COLOR = "#E44F64"


def main():
    plt.rcdefaults()
    # A power of two preserves the balance properties of the Sobol sequence.
    samples = {
        "sobol": qmc.Sobol(d=2, scramble=True, seed=42).random_base2(m=6),
        "monte_carlo": np.random.default_rng(42).random((64, 2)),
    }
    for name, points in samples.items():
        fig, ax = plt.subplots(figsize=(6.4, 6.4))
        ax.scatter(points[:, 0], points[:, 1], color=PART_COLOR)
        ax.set(xlim=(0, 1), ylim=(0, 1), aspect="equal")
        fig.savefig(OUTPUT / f"sampling_{name}.svg", transparent=True)
        plt.close(fig)


if __name__ == "__main__":
    main()
