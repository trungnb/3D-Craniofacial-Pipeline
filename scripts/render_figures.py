"""Render portfolio charts from saved CSV tables only. No notebook execution."""

import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
OUT = RESULTS / "figures"
OUT.mkdir(exist_ok=True)
NAVY, TEAL, ORANGE = "#17324D", "#168B8A", "#D17845"
plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "font.size": 10,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.labelcolor": NAVY,
        "text.color": NAVY,
        "axes.titleweight": "bold",
        "figure.facecolor": "white",
        "savefig.facecolor": "white",
        "svg.fonttype": "none",
    }
)


def rows(name):
    with (RESULTS / name).open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def save(fig, name, footer):
    fig.text(0.06, 0.018, footer, fontsize=8, color="#586777")
    fig.savefig(OUT / (name + ".png"), dpi=180, bbox_inches="tight")
    fig.savefig(OUT / (name + ".svg"), bbox_inches="tight")
    svg = OUT / (name + ".svg")
    svg.write_text(
        "\n".join(line.rstrip() for line in svg.read_text().splitlines()) + "\n"
    )
    plt.close(fig)


def size_mib(value):
    """Interpret historical 1024-based KB/MB strings in a common binary unit."""
    number, unit = value.split()
    return float(number) * {"KB": 1 / 1024, "MB": 1}[unit]


# Guard the unit conversion used for the saved size strings.
assert size_mib("1024 KB") == 1.0
assert size_mib("1.03 MB") == 1.03

summary = rows("summary_report.csv")
between = rows("p1vsp2_result.csv")
by_case = {r["person"]: r for r in summary}
by_comparison = {r["comparison_type"]: r for r in between}
case_names = ["Person1", "Person2"]

fig, (a, b) = plt.subplots(1, 2, figsize=(13, 5.6))
fig.subplots_adjust(left=0.11, right=0.98, top=0.77, bottom=0.23, wspace=0.52)
fig.suptitle(
    "Exploring a lighter representation for forensic comparison",
    x=0.04,
    ha="left",
    y=0.97,
    fontsize=17,
    fontweight="bold",
)
fig.text(
    0.04,
    0.88,
    "Two-CBCT prototype • saved storage footprints and comparison times",
    fontsize=11,
    color="#586777",
)

for label, column, color, offset, marker in [
    ("Input NIfTI", "ct_size", "#8996A6", -0.20, "s"),
    ("3D output", "total_volume_size1", NAVY, 0, "o"),
    ("2D output", "total_projection_size1", TEAL, 0.20, "D"),
]:
    values = [size_mib(by_case[c][column]) for c in case_names]
    positions = [i + offset for i in range(2)]
    a.scatter(
        values, positions, color=color, marker=marker, s=70, label=label, zorder=3
    )
    for value, pos in zip(values, positions):
        a.annotate(
            f"{value:.2f}",
            (value, pos),
            xytext=(7, 0),
            textcoords="offset points",
            va="center",
            fontsize=10,
        )
a.set_xscale("log")
a.set(
    xlim=(0.5, 1500),
    ylim=(1.45, -0.45),
    yticks=[0, 1],
    yticklabels=["Person1 / run 1", "Person2 / run 1"],
    xlabel="Stored size (MiB; logarithmic scale)",
)
a.set_xticks([1, 10, 100, 1000], labels=["1", "10", "100", "1,000"])
a.grid(axis="x", which="major", alpha=0.2)
a.set_title("A  Storage footprint", loc="left", pad=15)
a.legend(
    loc="upper left",
    bbox_to_anchor=(-0.04, -0.22),
    ncol=3,
    frameon=False,
    fontsize=9,
    columnspacing=0.8,
    handletextpad=0.4,
)

labels = ["Person1 / repeat runs", "Person2 / repeat runs", "Person1 vs Person2"]
volume_times = [
    float(by_case[c]["total_volume_comparison_time (s)"]) for c in case_names
]
projection_times = [
    float(by_case[c]["total_pro_comparison_time (s)"]) for c in case_names
]
volume_times.append(
    float(
        by_comparison["Volumes (Person1 vs Person2)"]["total_comparison_time_seconds"]
    )
)
projection_times.append(
    float(
        by_comparison["Projections (Person1 vs Person2)"][
            "total_comparison_time_seconds"
        ]
    )
)
for values, offset, color, label in [
    (volume_times, -0.17, NAVY, "3D comparison"),
    (projection_times, 0.17, TEAL, "2D comparison"),
]:
    b.barh([i + offset for i in range(3)], values, 0.28, color=color, label=label)
    for i, value in enumerate(values):
        b.text(value + 10, i + offset, f"{value:.2f}", va="center", fontsize=9)
b.set(
    yticks=range(3),
    yticklabels=labels,
    xlim=(0, 730),
    xlabel="Recorded comparison time (seconds)",
)
b.invert_yaxis()
b.set_title("B  Comparing the representations", loc="left", pad=15)
b.grid(axis="x", alpha=0.12)
b.legend(loc="upper left", bbox_to_anchor=(0, -0.22), ncol=2, frameon=False, fontsize=9)
save(
    fig,
    "prototype-overview",
    "Sources: summary_report.csv; p1vsp2_result.csv. Size labels converted from 1024-based exports. Comparison times exclude representation generation.",
)

fig, ax = plt.subplots(figsize=(11.8, 5.5))
fig.subplots_adjust(left=0.26, right=0.95, top=0.76, bottom=0.19)
fig.suptitle(
    "Checking overlap across runs and cases",
    x=0.04,
    ha="left",
    y=0.97,
    fontsize=18,
    fontweight="bold",
)
fig.text(
    0.04,
    0.88,
    "Saved mean Dice and IoU • two CBCT cases • no identification rate estimated",
    fontsize=11,
    color="#586777",
)
groups = []
for case in case_names:
    r = by_case[case]
    groups.extend(
        [
            (
                f"{case} / repeated volumes",
                float(r["vol_compare_dice"]),
                float(r["vol_compare_iou"]),
            ),
            (
                f"{case} / repeated projections",
                float(r["pro_compare_dice"]),
                float(r["pro_compare_iou"]),
            ),
        ]
    )
for key, label in [
    ("Volumes (Person1 vs Person2)", "P1 vs P2 / volumes"),
    ("Projections (Person1 vs Person2)", "P1 vs P2 / projections"),
]:
    r = by_comparison[key]
    groups.append((label, float(r["avg_dice_score"]), float(r["avg_iou_score"])))
for i, (_, dice, iou) in enumerate(groups):
    for value, offset, color, label in [
        (dice, -0.17, TEAL, "Dice"),
        (iou, 0.17, NAVY, "IoU"),
    ]:
        ax.barh(i + offset, value, 0.28, color=color, label=label if i == 0 else None)
        ax.text(value + 0.015, i + offset, f"{value:.6f}", va="center", fontsize=9)
ax.set(
    yticks=range(6),
    yticklabels=[g[0] for g in groups],
    xlim=(0, 1.18),
    xlabel="Saved mean overlap score",
)
ax.invert_yaxis()
ax.axhline(3.5, color="#D5DEE5", ls="--")
ax.legend(loc="upper left", bbox_to_anchor=(0, -0.15), ncol=2, frameon=False)
save(
    fig,
    "overlap-comparison",
    "Sources: summary_report.csv; p1vsp2_result.csv. Repeated-run agreement describes output consistency; these scores do not establish identification accuracy.",
)
