# UltraBinner

Use DAS Tool(v1.1.1) to integrate the results of three binners (CONCOCT V1.1.0, MetaBAT V2.12.1, MetaBinner) to calculate an optimized, non-redundant set of bins from a single assembly. 

## CONCOCT v1.1.0
CONCOCT is a program for unsupervised binning of metagenomic contigs by using nucleotide composition, coverage data in multiple samples and linkage data from paired end reads. You can get it from (https://github.com/BinPro/CONCOCT).

###  Installation
You can install CONCOCT via Bioconda/Docker. If you want to modify the source code, a manual installation might be needed. Here, we show you the easiest and recommended way to install concoct via Bioconda and conda in an isolated environment: 
```
conda config --add channels defaults
conda config --add channels bioconda
conda config --add channels conda-forge

conda create -n concoct_env python=3 concoct
```
Other ways to install CONCOCT is hosted on [readthedocs](https://concoct.readthedocs.org/)

### Basic Usage
Cut contigs into smaller parts
```
cut_up_fasta.py original_contigs.fa -c 1000 -o 0 --merge_last -b contigs_1K.bed > contigs_1K.fa
```
Generate table with coverage depth information per sample and subcontig. This step assumes the directory 'map' contains sorted and indexed bam files where each sample has been mapped against the original contigs.
```
concoct_coverage_table.py contigs_1K.bed map/Sample*.sorted.bam > coverage_table.tsv
```
Run CONCOCT
```
concoct --composition_file contigs_10K.fa --coverage_file coverage_table.tsv -b concoct_output/
```
### Example:
We downloaded the raw data from the 2nd CAMI Challenge Marine Dataset(https://data.cami-challenge.org/participate), and decompressed the data into /path/marine_gold_assembly/input/. Then we mapped reads from samples to the file `original_contigs.fa` into .bam files, sorted these .bam files to get `.sorted.bam` files and put these sorted files into /path//marine_gold_assembly/input/map/. We used the command below to run CONCOCT:
```
concoct --coverage_file /path/marine_gold_assembly/input/coverage_f1k_sr.tsv --composition_file /path/marine_gold_assembly/input/marmgCAMI2_short_read_pooled_gold_standard_assembly_f1k.fa -b /path/marine_gold_assembly/output/concoct/ -t 46
``` 
`-t` is the number of threads to use, more information about the command line options can be viewed by typing `concoct -h`.

## MetaBAT v2.12.1


## MetaBinner

## DAS Tool
