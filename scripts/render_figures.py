"""Regenerate the deterministic SVG overview from the saved prototype CSVs."""

import csv
from pathlib import Path

RESULTS = Path(__file__).resolve().parents[1] / "results"
OUT = RESULTS / "figures" / "prototype-overview.svg"
NAVY, TEAL, LIGHT = "#17324D", "#168B8A", "#A3D9D5"


def read_rows(name):
    with (RESULTS / name).open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def size_mib(text):
    number, unit = text.split()
    return float(number) * {"MB": 1, "KB": 1 / 1024}[unit]


summary = read_rows("summary_report.csv")
between = {r["comparison_type"]: r for r in read_rows("p1vsp2_result.csv")}

time_3d = [float(r["total_volume_comparison_time (s)"]) for r in summary]
time_3d.append(float(between["Volumes (Person1 vs Person2)"]["total_comparison_time_seconds"]))
time_2d = [float(r["total_pro_comparison_time (s)"]) for r in summary]
time_2d.append(float(between["Projections (Person1 vs Person2)"]["total_comparison_time_seconds"]))
size_3d = [size_mib(r["total_volume_size1"]) for r in summary]
size_2d = [size_mib(r["total_projection_size1"]) for r in summary]
dice = [float(r["pro_compare_dice"]) for r in summary]
dice.append(float(between["Projections (Person1 vs Person2)"]["avg_dice_score"]))
iou = [float(r["pro_compare_iou"]) for r in summary]
iou.append(float(between["Projections (Person1 vs Person2)"]["avg_iou_score"]))


def bar(value, maximum, width):
    return max(3.0, value / maximum * width)


def rect(x, y, width, height, fill):
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{width:.1f}" height="{height}" fill="{fill}"/>'


labels = ["Person1 / repeat", "Person2 / repeat", "Person1 vs Person2"]
parts = [
    '<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="690" viewBox="0 0 1200 690">',
    '<style>text{font-family:Arial,Helvetica,sans-serif;fill:#17324D}.title{font-size:27px;font-weight:700}.sub{font-size:15px;fill:#586777}.h{font-size:17px;font-weight:700}.lab{font-size:13px}.small{font-size:12px;fill:#586777}.val{font-size:12px;font-weight:700}.panel{fill:#fff;stroke:#E3E9ED;stroke-width:1.2}</style>',
    '<rect width="1200" height="690" fill="#fff"/>',
    '<text class="title" x="55" y="48">Prototype 3D-to-2D craniofacial comparison</text>',
    '<text class="sub" x="55" y="76">Two CBCT scans · historical proof-of-concept results</text>',
    '<rect class="panel" x="55" y="110" width="520" height="240" rx="6"/>',
    '<text class="h" x="80" y="142">A  Saved prototype comparison time</text>',
    '<text class="small" x="80" y="164">Comparison only; segmentation and projection generation excluded</text>',
]
for i, label in enumerate(labels):
    y = 194 + i * 52
    parts += [
        f'<text class="lab" x="80" y="{y + 13}">{label}</text>',
        rect(205, y, bar(time_3d[i], 650, 300), 14, NAVY),
        rect(205, y + 21, bar(time_2d[i], 650, 300), 14, TEAL),
        f'<text class="val" x="{215 + bar(time_3d[i], 650, 300):.1f}" y="{y + 12}">{time_3d[i]:.2f} s</text>',
        f'<text class="val" x="{215 + bar(time_2d[i], 650, 300):.1f}" y="{y + 33}">{time_2d[i]:.2f} s</text>',
    ]

parts += [
    '<rect class="panel" x="600" y="110" width="545" height="240" rx="6"/>',
    '<text class="h" x="625" y="142">B  Saved output size (run 1)</text>',
    '<text class="small" x="625" y="164">Historical NIfTI-mask output versus PNG-projection output</text>',
]
for i, label in enumerate(["Person1", "Person2"]):
    y = 199 + i * 70
    parts += [
        f'<text class="lab" x="625" y="{y + 18}">{label}</text>',
        rect(710, y, bar(size_3d[i], 170, 340), 16, NAVY),
        rect(710, y + 26, bar(size_2d[i], 170, 340), 16, TEAL),
        f'<text class="val" x="{720 + bar(size_3d[i], 170, 340):.1f}" y="{y + 13}">{size_3d[i]:.2f} MiB</text>',
        f'<text class="val" x="{720 + bar(size_2d[i], 170, 340):.1f}" y="{y + 39}">{size_2d[i]:.2f} MiB</text>',
    ]

parts += [
    '<rect class="panel" x="55" y="380" width="1090" height="235" rx="6"/>',
    '<text class="h" x="80" y="414">C  Projection overlap</text>',
    '<text class="small" x="80" y="436">Repeated same-scan overlap assesses computational repeatability, not identification accuracy</text>',
]
for i, label in enumerate(labels):
    y = 464 + i * 51
    parts += [
        f'<text class="lab" x="80" y="{y + 14}">{label}</text>',
        rect(330, y, dice[i] * 750, 13, TEAL),
        rect(330, y + 17, iou[i] * 750, 13, LIGHT),
        f'<text class="val" x="{342 + dice[i] * 750:.1f}" y="{y + 12}">{dice[i]:.3f}</text>',
        f'<text class="val" x="{342 + iou[i] * 750:.1f}" y="{y + 29}">{iou[i]:.3f}</text>',
    ]
parts += [
    '<rect x="55" y="640" width="14" height="14" fill="#17324D"/><text class="small" x="78" y="652">3D masks</text>',
    '<rect x="160" y="640" width="14" height="14" fill="#168B8A"/><text class="small" x="183" y="652">2D projections / Dice</text>',
    '<rect x="350" y="640" width="14" height="14" fill="#A3D9D5"/><text class="small" x="373" y="652">IoU</text>',
    '<text class="small" x="455" y="652">Exploratory two-case prototype; between-case overlap may reflect acquisition and alignment as well as anatomy.</text>',
    '</svg>',
]
OUT.parent.mkdir(exist_ok=True)
OUT.write_text("\n".join(parts) + "\n", encoding="utf-8")
print(f"Wrote {OUT}")
