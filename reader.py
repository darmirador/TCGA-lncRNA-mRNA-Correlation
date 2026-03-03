#!/usr/bin/env python3
"""
correlation_mRNA_lncRNA.py

For each per-cancer lncRNA output file in `pathname` (files starting with "output"),
cross-reference TCGA sample barcodes against the TCGA PanCan mRNA matrix, extract the
mRNA expression for a single gene symbol, and write a merged table:

    barcode_prefix, [lncRNA_fpkm], [mRNA_value]

Output (per cancer type)
------------------------
[ENSGID]-[GENE]_[TCGA]_output-summary.csv
Columns:
  barcode,ENSG...,GENE

--------------
-l / --lncRNA : lncRNA ENSG accession (used in output filename + header)
-m / --mRNA   : mRNA gene symbol (used to select row in mRNA matrix)
"""

import os
import csv
import argparse
import numpy  # kept
from scipy import stats  # kept


def parse_args():
    parser = argparse.ArgumentParser(
        description="Merge per-cancer lncRNA outputs with TCGA mRNA matrix by barcode prefix."
    )
    parser.add_argument(
        "-l", "--lncRNA",
        required=True,
        help="lncRNA ENSG accession to use in output header/filename (e.g., ENSG00000270195.1)."
    )
    parser.add_argument(
        "-m", "--mRNA",
        required=True,
        help="mRNA gene symbol to extract (e.g., SLBP)."
    )
    return parser.parse_args()


# User parameters (paths)
pathname = "/Users/darmirador/Desktop/Python Scripts/correlation_mRNA_lncRNA"
mRNA_file = "EBPlusPlusAdjustPANCAN_IlluminaHiSeq_RNASeqV2.geneExp.tsv"


def main():
    args = parse_args()
    ensgId = args.lncRNA
    geneId = args.mRNA

    # Discover input files (lncRNA outputs)
    directoryFiles = os.listdir(pathname)
    filenameArray = []
    cancerTypes = []

    for csvFile in directoryFiles:
        if csvFile[:6] == "output":
            filenameArray.append(csvFile)
    filenameArray = sorted(filenameArray)

    # Extract cancer types (first 4 chars only; preserved)
    for cancerFilename in filenameArray:
        cancerTypes.append(cancerFilename.split("_")[1][:4])

    processCounter = 0
    for filename in filenameArray:

        class referenceState:
            def __init__(self, tcgaId, transcriptLevels_lncRNA, transcriptLevels_mRNA):
                self.tcgaId = tcgaId
                self.transcriptLevels_lncRNA = transcriptLevels_lncRNA
                self.transcriptLevels_mRNA = transcriptLevels_mRNA

        unfiltered = referenceState([], [], [])
        filtered = referenceState([], [], [])

        # Step 1: Load the mRNA matrix header and extract gene row
        with open(mRNA_file) as file:
            tsv_file = csv.reader(file, delimiter="\t")
            unfiltered.tcgaId = next(tsv_file)

            counter = 0
            for line in tsv_file:
                rowGeneName = line[0].split("|")[0]
                if rowGeneName == geneId:
                    unfiltered.transcriptLevels_mRNA = line
                counter += 1

        # Step 2: Load lncRNA per-cancer file and cross-reference
        with open(filename) as file:
            csv_file = csv.reader(file, delimiter=",")

            for line in csv_file:
                counter = 0
                for barcode in unfiltered.tcgaId:
                    if line[1][:15] == unfiltered.tcgaId[counter][:15]:
                        filtered.tcgaId.append(line[1])
                        filtered.transcriptLevels_lncRNA.append(float(line[2]))
                        filtered.transcriptLevels_mRNA.append(float(unfiltered.transcriptLevels_mRNA[counter]))
                    counter += 1

        # Step 3: Write merged output for this cancer type
        out_name = ensgId + "-" + geneId + "_" + cancerTypes[processCounter] + "_output-summary.csv"

        csvOutput = open(out_name, "w")
        csvOutput.write("barcode," + ensgId + "," + geneId + "\n")
        csvOutput.close()

        for i in range(0, len(filtered.tcgaId)):
            csvOutput = open(out_name, "a")
            csvOutput.write(
                filtered.tcgaId[i][:15] + "," +
                str(filtered.transcriptLevels_lncRNA[i]) + "," +
                str(filtered.transcriptLevels_mRNA[i]) + "\n"
            )
            csvOutput.close()

        processCounter += 1

        # Progress indicator
        print("Finished processing cancer type:", cancerTypes[processCounter - 1])


if __name__ == "__main__":
    main()