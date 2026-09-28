# Methods represented in the notebooks

## Question and implementation
The opening notebook frames craniofacial shape analysis as a possible route toward
human identification. The implemented prototype extracts representations and records
overlap comparisons for two cases; it does not train an identity classifier.

1. Load NIfTI scans with NiBabel. Invoke TotalSegmentator tasks
   `craniofacial_structures` and `teeth`, with `fast=False` and NIfTI outputs.
2. Threshold each output at `> 0`. Use maximum projections along each of the three
   array axes to export axial, coronal and sagittal binary images.
3. Compare first and second runs for the same case; record mean Dice / IoU and timing.
4. Compare Person1 and Person2. The notebook resamples one volume to the other with
   an identity transform and nearest-neighbour interpolation. Differently sized PNGs
   are resized with nearest-neighbour interpolation. These implementation details
   define what the saved overlap numbers represent.
5. Collect tooth and pulp volumes and ratios in the separate `sex&age.ipynb` exploration.

## Reported results
`results/summary_report.csv` contains two rows with recorded timings, sizes and
within-case overlap. `results/p1vsp2_result.csv` contains volume and projection
comparisons between cases. The overview chart plots those stored values; seconds
are converted to minutes for readability. No segmentation or overlap was recomputed.

The original environment, input acquisition details and model weight versions are
not established by these files. The sample comprises two cases. No externally
validated identification claim or segmentation accuracy against ground truth is made.
