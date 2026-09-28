# Saved results

| File | Contents | Original notebook |
|---|---|---|
| [summary_report.csv](summary_report.csv) | Two cases; two runs; sizes, timings and mean overlap | `Comparison.ipynb` |
| [p1vsp2_result.csv](p1vsp2_result.csv) | Between-case mean Dice / IoU for volumes and projections | `Comparison.ipynb` |
| [Overview PNG](figures/prototype-overview.png) / [SVG](figures/prototype-overview.svg) | Run-1 storage footprint and saved 3D / 2D comparison times | `scripts/render_figures.py` |
| [Overlap PNG](figures/overlap-comparison.png) / [SVG](figures/overlap-comparison.svg) | Saved repeated-run and between-case Dice / IoU | `scripts/render_figures.py` |

The historical headers `ct_size` and `segmention_time1 (s)` are preserved verbatim.
The author confirmed the prototype input modality as CBCT.
The size formatter uses 1024-based units with KB/MB labels. Chart sizes are expressed
in MiB; original rounded strings remain unchanged in the CSV and README table.
Comparison timings exclude the separately recorded segmentation and projection-export steps.
Image arrays, masks and identifiable anatomy are excluded from the public release.
