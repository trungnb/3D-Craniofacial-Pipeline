# Methods represented in the notebooks

## Research question and prototype scope
This is an early prototype of the proposal **3D to 2D Projections Analysis of Teeth,
Jaws and Sinuses for Human Identification**. Its central idea is to explore multi-view
silhouettes as compact representations for forensic ante-mortem (AM) versus post-mortem
(PM) comparison, with lower storage and comparison demands than volumetric representations.

The proposal plans a head CT study; the present prototype uses two CBCT scans.
The implemented checks compare repeated pipeline runs and two different cases.
They are preliminary technical checks, not evaluation of independently acquired AM–PM pairs.

| Proposal objective | Evidence in this prototype | Remaining proposal work |
|---|---|---|
| SO1: segmentation and multi-view projections | TotalSegmentator calls and three-view binary projection code | Study-level preprocessing and evaluation on the proposed head CT dataset |
| SO2: pipeline stability across two runs | Saved repeated-run Dice / IoU for two cases | The proposed one-month interval is not established by available records |
| SO3: storage footprint | Saved input, segmented-output and projection-output sizes | Larger projection database evaluation |
| SO4: baseline comparison and resource benchmark | Dice / IoU and recorded 3D / 2D comparison times | CPU/GPU utilization, controlled hardware benchmark and identification accuracy |
| SO5: scale and missing-structure simulations | No implementation identified in the three notebooks | Planned database sizes of 50, 100, 150 and 200; missing-structure scenarios and top-1 / top-5 rates |

The proposal's hypotheses and planned outcomes remain research aims. They are not
reported as results of this two-case prototype.

## Implemented steps

1. Load NIfTI scans with NiBabel. Invoke TotalSegmentator tasks
   `craniofacial_structures` and `teeth`, with `fast=False` and NIfTI outputs.
2. Threshold each output at `> 0`. Use maximum projections along each of the three
   array axes to export axial, coronal and sagittal binary images.
3. Compare first and second runs for the same case; record mean Dice / IoU and timing.
4. Compare Person1 and Person2. The notebook resamples one volume to the other with
   an identity transform and nearest-neighbour interpolation. Differently sized PNGs
   are resized with nearest-neighbour interpolation. These implementation details
   define what the saved overlap numbers represent.
5. Collect tooth and pulp volumes and ratios in the supplementary `sex&age.ipynb`
   exploration. This is not an implemented age or sex prediction component.

## Reported results
`results/summary_report.csv` contains two rows with recorded timings, sizes and
within-case overlap. `results/p1vsp2_result.csv` contains volume and projection
comparisons between cases. No segmentation or overlap was recomputed for presentation.

The overview figure shows run-1 storage footprints and saved **comparison** times.
Storage is measured from the exported files/folders, not from in-memory array sizes.
The notebook's `format_size` divides by 1024 but labels values KB/MB. The plot converts
those displayed values to MiB; the README table preserves their original labels.
Source sizes were already rounded, and the converted sizes are approximate.
The storage axis is logarithmic and labeled explicitly.

Within-case times use `total_volume_comparison_time (s)` and
`total_pro_comparison_time (s)`. Between-case times use
`total_comparison_time_seconds`. Segmentation and projection-export timings remain
in the source table, but are not added to the comparison times. Neither identical
hardware conditions nor an end-to-end identification speedup is established here.

The separate overlap figure presents the saved mean Dice and IoU for both representations.
Repeated-run agreement concerns consistency of outputs. Between-case overlap is not
an identification rate or a validated decision threshold.

The original environment, input acquisition details and model weight versions are
not established by these files. The sample comprises two cases. No externally
validated identification claim or segmentation accuracy against ground truth is made.
