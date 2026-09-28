# ADR-0002 — Present the projection proposal and the CBCT prototype

Status: ACCEPTED

## Context
The owner identified this repository as a prototype of the proposal on 3D-to-2D
projections for human identification, confirmed that the prototype uses two CBCT
scans, and requested the revised presentation.

## Decision
Explain the AM–PM research motivation and the proposed use of compact multi-view
silhouettes. Prioritize saved storage footprints and 3D / 2D comparison times in the
main figure. Present overlap separately. Distinguish the current two-case CBCT
prototype from the planned head CT study and its scale/degradation experiments.

## Rationale
This connects the implemented prototype to the owner's research question while
keeping claims within the evidence available in the notebooks and saved results.

## Allowed
Update public documentation and redraw charts from existing result tables.
Describe input modality and case count. Preserve original analysis code and results.

## Not allowed
Add personal image-source information, run the analysis again without authorization,
or describe proposal hypotheses and future experiments as completed results.

## Consequences
Publication communicates both the intended application and the current scope.
Comparison timings exclude segmentation and projection generation.

## Supersedes / Superseded by
None. Complements ADR-0001.
