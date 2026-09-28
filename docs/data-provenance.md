# Provenance of this portfolio release

Packaged on 2026-09-28 from the author's existing project notebooks and result files.
No segmentation, synthesis, model training, evaluation, or reproduction run was performed.

## Notebooks
[notebook-provenance.json](notebook-provenance.json) records SHA-256 fingerprints of
the original and published notebook files. Original analysis cell sources and their
order are unchanged. No heading cell was inserted, so zero-based source references
still match. Publication clears session metadata, widget state and output previews.
Published notebooks have their outputs cleared. Original notebooks remain in an
ignored `.local-originals/` directory on the author's machine.

## Result tables
The published input CSVs are existing saved result files, byte-for-byte unchanged.

See [the result index](../results/README.md) and [table fingerprints](result-sources.json).
Original CSV / notebook files do not establish the exact historical data version,
execution date, hardware or analysis package versions; those details remain unverified.

## Figures
`scripts/render_figures.py` reads the published CSVs and renders PNG and SVG figures.
It performs chart formatting and display-unit conversion only; it does not import
segmentation libraries. The overview uses saved run-1 sizes and comparison timings;
the supplementary figure uses saved overlap scores. The Python lockfile covers these
portfolio tools. Figure sources are documented in the result index and figure captions.

## Research framing and modality
The research framing follows the author's proposal, *3D to 2D Projections Analysis
of Teeth, Jaws and Sinuses for Human Identification*, and the author's clarification
that this repository is its prototype. The author confirmed that the two prototype
inputs are CBCT scans. The proposal's planned head CT study is described as future work.
Only modality and case count are included in the public dataset description.

## Publication scope
Source CBCT scans, segmentation masks, unrelated notebooks and local backups are
excluded. Code links to external packages do not transfer their licenses. See [LICENSE](../LICENSE).
