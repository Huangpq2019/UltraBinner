# UltraBinner

Use DAS Tool(v1.1.1) to integrate the results of three binners (CONCOCT V1.1.0, MetaBAT V2.12.1, MetaBinner) to calculate an optimized, non-redundant set of bins from a single assembly. 

## CONCOCT v1.1.0
CONCOCT is a program for unsupervised binning of metagenomic contigs by using nucleotide composition, coverage data in multiple samples and linkage data from paired end reads. You can get it from (https://github.com/BinPro/CONCOCT).<br>
###  Installation
You can install CONCOCT via Bioconda/Docker. If you want to modify the source code, a manual installation might be needed. Here, we show you the easiest and recommended way to install concoct via Bioconda and conda in an isolated environment: 
```
conda config --add channels defaults
conda config --add channels bioconda
conda config --add channels conda-forge

conda create -n concoct_env python=3 concoct
```
Other ways to install CONCOCT is hosted on [eadthedocs](https://concoct.readthedocs.org/)

## Data preprocessing
The preprocessing steps aim to generate coverage profile as input to our program.<br>

### Composition Profile
Composition profile is the vector representation of contigs and we use kmer to generate this information.
```
python gen_kmer.py /path/to/data/contig.fasta 1000 4
```
Here we choose k=4. By default we usually keep contigs longer than 1000, you can specify a different number. The kmer_file will be generated in the /path/to/data

example:
```
python gen_kmer.py /path/marine_gold_assembly/input/marmgCAMI2_short_read_pooled_gold_standard_assembly.fasta 1000 4
```

You should download the raw data and input it into the /input directory. You input directory should look like this:<br>
```.
+-- assembly.fasta
+-- sr
|   +-- short_read_sample_1
|   +-- short_read_sample_2
+-- pb
|   +-- pacbio_sample_1
|   +-- pacbio_sample_2
|   +-- pacbio_sample_3
```
download data from (https://data.cami-challenge.org/participate) and 

## MetaBAT v2.12.1

## MetaBinner

## DAS Tool
