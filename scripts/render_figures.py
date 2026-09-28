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
    svg.write_text("\n".join(line.rstrip() for line in svg.read_text().splitlines()) + "\n")
    plt.close(fig)


summary = rows("summary_report.csv")
between = rows("p1vsp2_result.csv")
fig, (a, b) = plt.subplots(
    1, 2, figsize=(12.8, 5.4), gridspec_kw={"width_ratios": [1.12, 1]}
)
fig.subplots_adjust(left=0.12, right=0.97, top=0.78, bottom=0.22, wspace=0.5)
fig.suptitle(
    "From segmentation to a shape-comparison prototype",
    x=0.06,
    ha="left",
    y=0.97,
    fontsize=18,
    fontweight="bold",
)
fig.text(
    0.06,
    0.88,
    "Historical outputs from two cases • repeated runs and a between-case comparison",
    fontsize=11,
    color="#586777",
)
groups = [
    (
        "Person1 / volumes",
        float(summary[0]["vol_compare_dice"]),
        float(summary[0]["vol_compare_iou"]),
    ),
    (
        "Person1 / projections",
        float(summary[0]["pro_compare_dice"]),
        float(summary[0]["pro_compare_iou"]),
    ),
    (
        "Person2 / volumes",
        float(summary[1]["vol_compare_dice"]),
        float(summary[1]["vol_compare_iou"]),
    ),
    (
        "Person2 / projections",
        float(summary[1]["pro_compare_dice"]),
        float(summary[1]["pro_compare_iou"]),
    ),
    (
        "P1 vs P2 / volumes",
        float(between[0]["avg_dice_score"]),
        float(between[0]["avg_iou_score"]),
    ),
    (
        "P1 vs P2 / projections",
        float(between[1]["avg_dice_score"]),
        float(between[1]["avg_iou_score"]),
    ),
]
for i, (_, dice, iou) in enumerate(groups):
    a.barh(i - 0.16, dice, 0.28, color=TEAL, label="Dice" if i == 0 else None)
    a.barh(i + 0.16, iou, 0.28, color=NAVY, label="IoU" if i == 0 else None)
    a.text(dice + 0.012, i - 0.16, f"{dice:.3f}", va="center", fontsize=8)
    a.text(iou + 0.012, i + 0.16, f"{iou:.3f}", va="center", fontsize=8)
a.set(
    yticks=range(len(groups)),
    yticklabels=[r[0] for r in groups],
    xlim=(0, 1.19),
    xlabel="Saved mean overlap score",
)
a.invert_yaxis()
a.axhline(3.5, color="#D5DEE5", ls="--")
a.set_title("A  Mask and projection overlap", loc="left", pad=14)
a.legend(loc="lower left", bbox_to_anchor=(0, -0.36), ncol=2, frameon=False)
labels = []
seg = []
proj = []
for row in summary:
    for run in [1, 2]:
        labels.append(f"{row['person']} / run {run}")
        seg.append(float(row[f"segmention_time{run} (s)"]) / 60)
        proj.append(float(row[f"projection_time{run} (s)"]) / 60)
b.barh(range(4), seg, color=NAVY, label="Segmentation")
b.barh(range(4), proj, left=seg, color=ORANGE, label="Projection export")
for i, (s, p) in enumerate(zip(seg, proj)):
    b.text(s / 2, i, f"{s:.1f}", ha="center", va="center", color="white", fontsize=9)
    b.text(
        s + p / 2, i, f"{p:.1f}", ha="center", va="center", color="white", fontsize=9
    )
b.set(
    yticks=range(4),
    yticklabels=labels,
    xlabel="Recorded processing time (minutes)",
    xlim=(0, 16.8),
)
b.invert_yaxis()
b.set_title("B  Recorded processing time", loc="left", pad=14)
b.legend(loc="lower left", bbox_to_anchor=(0, -0.36), ncol=1, frameon=False)
save(
    fig,
    "prototype-overview",
    "Sources: summary_report.csv; p1vsp2_result.csv. Rounded for display. Same-case overlap is run agreement, not ground-truth accuracy.",
)
