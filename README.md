# BaitsFinder
BaitsFinder is a combination of several python scripts (python 2.7) and freely available bioinformatic tools (see the step-by-step guide for further details) allowing bait sequences to be generated. It involves up to seven steps:

(1) Identifying single (low) copy genes (SCGs) in species that are closely related to the group of interest and for which whole genome data are available (henceforth called reference species).

(2) Identifying single copy genes in the focal species (i.e., the species of interest).

(3) Extract sequences from both reference and focal species.

(4) Sequence alignment.

(5) Extraction of exon sequences and removal of those of insufficient length.

(6) Extraction of bait sequences.

(7) Data cleansing.

Details for tasks of step 1 likely will differ strongly among study groups (and may be skipped altogether, if reference data are already available). Therefore, the few scripts pertaining to this step (all in the folder "scripts_part1") are tailored for the study groups used by us and will have to be modified, where needed.
Steps 2 to 7 are done by three scripts: blast_tcl.py (first part of step 2), combined_ini.py (second part of step 2 until first part of step 7), and remove-plastid.py (last part of step 7). See the step-by-step guide for further details. The script combined-ini.py requires a config file, an example of which is provided (file "config.ini").

Example data (reference species and four focal species) are provided in the archive "example-data.rar". 
