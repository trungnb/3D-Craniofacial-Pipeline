# 3D-to-2D craniofacial comparison

A two-CBCT prototype exploring multi-view silhouettes for forensic identification.
The idea is to compare compact 2D projections of segmented anatomy instead of comparing
only the full 3D volumes.

## Four prototype goals

| Goal | Saved result in this prototype |
|---|---|
| **1. Comparing projections takes less time than comparing 3D volumes.** | Across the three saved comparisons: **6.80–7.92 s for 2D**, versus **392.51–608.80 s for 3D**. |
| **2. Projections need less storage than 3D volumes.** | Person1: **160.34 MB → 1.03 MB**. Person2: **119.27 MB → 897.77 KB** (3D output → 2D output, run 1). |
| **3. Projections from the same person are similar.** | Projection Dice and IoU are **approximately 1.00** for both repeated-run comparisons. |
| **4. Projections from two different people differ.** | Person1 vs Person2: projection Dice **0.324**, IoU **0.313**. |

**Dice and IoU measure overlap: both range from 0 (no overlap) to 1 (identical masks).** Values above are rounded; the CSVs retain the original precision.

![Four prototype checks: comparison time, storage, same-person overlap and between-person overlap](results/figures/prototype-overview.png)

## How I approached it

```mermaid
flowchart TD
    A["Two CBCT scans in NIfTI format<br/>Run the pipeline twice on each scan"] --> B["SEGMENT<br/>TotalSegmentator: craniofacial structures + teeth"]
    B --> C["3D binary masks<br/>One mask per anatomical structure"]
    C --> D["PROJECT TO 2D<br/>Maximum projection along each axis<br/>Axial, coronal and sagittal silhouettes"]
    C --> E["EFFICIENCY<br/>Compare 3D vs 2D storage<br/>and comparison time"]
    D --> E
    C --> F["PAIR CORRESPONDING STRUCTURES<br/>For 2D, also match the projection view"]
    D --> F
    F --> G["SAME PERSON<br/>Run 1 vs run 2 of the same scan<br/>Measure Dice + IoU"]
    F --> H["DIFFERENT PEOPLE<br/>Person1 vs Person2, run 1<br/>Measure Dice + IoU"]
    classDef compact fill:#168B8A,stroke:#168B8A,color:#FFFFFF
    classDef result fill:#17324D,stroke:#17324D,color:#FFFFFF
    class D compact
    class E,G,H result
```

**Idea:** preserve anatomical shape in three compact silhouettes per structure, then
check whether they retain similarity while reducing storage and comparison time.
I connected segmentation, projection and baseline Dice / IoU comparison. For
between-person comparisons, the code resamples 3D masks to the reference grid
and resizes 2D masks when dimensions differ before calculating overlap.

## Read the code and results

- [Segmentation and projection notebook](notebooks/3D_Shape_Analysis_Pipeline.ipynb)
- [Comparison notebook](notebooks/Comparison.ipynb)
- [Repeated-run results and storage](results/summary_report.csv)
- [Between-person results](results/p1vsp2_result.csv)
- [Figure script](scripts/render_figures.py) — reads the two saved CSVs; requires Matplotlib.

**Scope:** “same person” here means two pipeline runs on the **same CBCT scan**.
The saved comparisons demonstrate these observations in two cases; they do not
estimate identification accuracy in a larger population. AM–PM matching is the
intended research application.

**Reading the numbers:** comparison times exclude segmentation and projection generation.
Storage strings retain their original labels; the figure uses MiB because the original
formatter divided by 1024. Exact hardware conditions are not documented in the tables.

Source scans and masks are not distributed. Notebook code is preserved; historical
outputs are presented through the saved tables. No analysis was rerun for this release.

[trungnb](https://github.com/trungnb) · [Academic website](https://trungnb.github.io/)
