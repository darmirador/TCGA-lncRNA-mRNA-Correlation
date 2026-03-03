Before starting, download the following file from the GDC Pan-Cancer Atlas portal:

EBPlusPlusAdjustPANCAN_IlluminaHiSeq_RNASeqV2.geneExp.tsv
https://gdc.cancer.gov/about-data/publications/pancanatlas

This matrix contains normalized mRNA expression values across TCGA samples and is required for extracting gene-level expression data.

This workflow depends on mRNA output files generated from prior TCGA processing pipelines available in:

https://github.com/darmirador

These outputs are used for sample-level alignment and cross-referencing. In particular, outputs of the following projects are needed:
https://github.com/darmirador/DeepBase-v3.0-RNAseq-analysis-for-lncRNAs (for lncRNA data)
https://github.com/darmirador/TCGA-DEmRNA (for mRNA data)

This repository performs expression integration only.

