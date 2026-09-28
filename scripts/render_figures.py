"""Draw the prototype summary from saved CSVs. Requires Matplotlib; no analysis rerun."""

import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

RESULTS = Path(__file__).resolve().parents[1] / "results"
NAVY, TEAL = "#17324D", "#168B8A"


def read_rows(name):
    with (RESULTS / name).open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def size_mib(text):
    number, unit = text.split()
    return float(number) * {"MB": 1, "KB": 1 / 1024}[unit]


def comparison_panel(ax, labels, volumes, projections, title, xlabel):
    """Use identical colors and layout for the time and storage comparisons."""
    limit = max(volumes + projections)
    for values, offset, color in [(volumes, -0.16, NAVY), (projections, 0.16, TEAL)]:
        ax.barh([i + offset for i in range(len(labels))], values, 0.27, color=color)
        for i, value in enumerate(values):
            ax.text(value + limit * 0.025, i + offset, f"{value:.2f}", va="center")
    ax.set(
        yticks=range(len(labels)),
        yticklabels=labels,
        xlim=(0, limit * 1.24),
        xlabel=xlabel,
    )
    ax.invert_yaxis()
    ax.set_title(title, loc="left", pad=14, fontsize=12)


assert size_mib("1024 KB") == 1.0  # Check the historical formatter's binary units.
summary = read_rows("summary_report.csv")
between = {r["comparison_type"]: r for r in read_rows("p1vsp2_result.csv")}
cases = [r["person"] for r in summary]
labels = [f"{name} / repeat" for name in cases] + ["Person1 vs Person2"]

plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "font.size": 10,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.titleweight": "bold",
        "text.color": NAVY,
    }
)
fig = plt.figure(figsize=(12, 8))
grid = fig.add_gridspec(
    2, 2, left=0.17, right=0.97, top=0.81, bottom=0.15, hspace=0.63, wspace=0.43
)
time_ax, size_ax, similarity_ax = (
    fig.add_subplot(grid[0, 0]),
    fig.add_subplot(grid[0, 1]),
    fig.add_subplot(grid[1, :]),
)
fig.suptitle(
    "3D vs 2D: time, storage and similarity",
    x=0.035,
    ha="left",
    y=0.975,
    fontsize=16,
    fontweight="bold",
)
fig.text(
    0.035,
    0.925,
    "Two CBCT scans • results from earlier prototype runs",
    fontsize=11,
    color="#586777",
)
fig.legend(
    handles=[
        plt.Rectangle((0, 0), 1, 1, color=NAVY),
        plt.Rectangle((0, 0), 1, 1, color=TEAL),
    ],
    labels=["3D volumes", "2D projections"],
    loc="upper right",
    bbox_to_anchor=(0.98, 0.90),
    ncol=2,
    frameon=False,
)

comparison_panel(
    time_ax,
    labels,
    [float(r["total_volume_comparison_time (s)"]) for r in summary]
    + [float(between["Volumes (Person1 vs Person2)"]["total_comparison_time_seconds"])],
    [float(r["total_pro_comparison_time (s)"]) for r in summary]
    + [
        float(
            between["Projections (Person1 vs Person2)"]["total_comparison_time_seconds"]
        )
    ],
    "1  Projections take less time to compare",
    "Comparison time (seconds)",
)
comparison_panel(
    size_ax,
    cases,
    [size_mib(r["total_volume_size1"]) for r in summary],
    [size_mib(r["total_projection_size1"]) for r in summary],
    "2  Projections take less storage",
    "Stored output size (MiB; run 1)",
)

for metric, offset, color in [("dice", -0.16, TEAL), ("iou", 0.16, "#A3D9D5")]:
    scores = [float(r[f"pro_compare_{metric}"]) for r in summary] + [
        float(between["Projections (Person1 vs Person2)"][f"avg_{metric}_score"])
    ]
    similarity_ax.barh(
        [i + offset for i in range(len(scores))],
        scores,
        0.27,
        color=color,
        label="Dice" if metric == "dice" else "IoU",
    )
    for i, score in enumerate(scores):
        label = f"≈ {score:.2f}" if i < len(summary) else f"{score:.3f}"
        similarity_ax.text(score + 0.018, i + offset, label, va="center", fontsize=10)
similarity_ax.legend(loc="lower right", frameon=False, title="2D overlap")
similarity_ax.set(
    yticks=range(len(labels)),
    yticklabels=labels,
    xlim=(0, 1.14),
    xlabel="Projection overlap score · closer to 1 = more similar",
)
similarity_ax.set_xticks([0, 0.25, 0.5, 0.75, 1])
similarity_ax.invert_yaxis()
similarity_ax.axhline(len(summary) - 0.5, color="#D5DEE5", linestyle="--")
similarity_ax.set_title(
    "3–4  Same-person projections are similar; the two cases differ",
    loc="left",
    pad=14,
    fontsize=12,
)

fig.text(
    0.035,
    0.066,
    "Same-person checks repeat the pipeline on the same scan. Comparison times exclude segmentation and projection generation.",
    fontsize=9,
    color="#586777",
)
fig.text(
    0.035,
    0.025,
    "Sources: summary_report.csv and p1vsp2_result.csv. Stored sizes use the original 1024-based units. Scores are rounded for display.",
    fontsize=8,
    color="#586777",
)
output = RESULTS / "figures" / "prototype-overview.png"
output.parent.mkdir(exist_ok=True)
fig.savefig(output, dpi=180, bbox_inches="tight", facecolor="white")
plt.close(fig)
