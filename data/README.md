# Input data

This exploratory prototype uses two CBCT scans, represented in the notebooks as
`Person1.nii.gz` and `Person2.nii.gz`. Selected derived results are presented;
source scans and segmentation masks are not distributed. The labels are case aliases.

The broader research proposal plans a head CT study. That planned dataset is separate
from the two CBCT scans used for the present prototype. Acquisition parameters and
the exact historical input versions are not documented in this release.

Reading the README, notebooks and saved summaries needs no data download.
Running the original analysis would require authorized NIfTI inputs, the original
folder layout or adapted paths, the relevant TotalSegmentator tasks and sufficient
compute resources. Raw images and masks must remain outside Git. Notebook paths and
the historical `ct_size` result column are preserved; they do not change the confirmed
CBCT modality of the prototype inputs.
