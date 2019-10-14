# UltraBinner

Use DAS Tool(v1.1.1) to integrate the results of three binners (CONCOCT V1.1.0, MetaBAT V2.12.1, MetaBinner) to calculate an optimized, non-redundant set of bins from a single assembly. 

## CONCOCT v1.1.0
CONCOCT is a program for unsupervised binning of metagenomic contigs by using nucleotide composition, coverage data in multiple samples and linkage data from paired end reads. You can get it from https://github.com/BinPro/CONCOCT.

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
MetaBAT integrates the Tetranucleotide frequency distance Probability (TDP) and the abundance distance probability (ADP) of each contig pair and modified k-medoid clustering algorithm is utilized for contig binning. You can get it from https://bitbucket.org/berkeleylab/metabat/src/master/.

###  Installation
Requirements:<br>
* boost >= 1.59.0 (dev and libs for boost_graph, system, filesystem and serialization)
* python >= 2.7
* cmake >= 3.8.2
* gcc/g++ >= 4.9 or intel >= 18.0.1.163 or llvm >= 8.0
(htslib 1.9 is downloaded and installed automatically if not present on the system)
```
# MetaBAT 2 (Linux 64-bit)
wget https://bitbucket.org/berkeleylab/metabat/downloads/metabat-static-binary-linux-x64_v2.12.1.tar.gz
tar xzvf metabat-static-binary-linux-x64_v2.12.1.tar.gz
mv metabat-static-binary-linux-x64_v2.12.1 metabat

cd metabat
mkdir build 
cd build
cmake -DCMAKE_INSTALL_PREFIX=$HOME/metabat ..
make
make install
cd ..
rm -rf build
```
MetaBAT can also run with Docker:
```
docker run <docker options> metabat/metabat:latest runMetaBat.sh

# For example:
docker run --workdir $(pwd) --volume $(pwd):$(pwd) metabat/metabat:latest runMetaBat.sh test/contigs.fa  test/contigs-1000.fastq.bam
```
You can see [INSTALL.md](https://bitbucket.org/berkeleylab/metabat/src/master/INSTALL.md) for Operating System specific installation instructions.

### Basic Usage
The easy way:
```
runMetaBat.sh <options> assembly.fasta sample1.bam [sample2.bam ...]
```
The slightly less easy way:<br>
a) Generate a depth file from BAM files
```
jgi_summarize_bam_contig_depths --outputDepth depth.txt *.bam 
```
b) Run metabat
```
metabat2 -i assembly.fasta -a depth.txt -o bins_dir/bin 
```
### Example:
We use the sorted data in the directory /path//marine_gold_assembly/input/map/ and the `original_contigs.fa` file to run MetaBAT:
```
jgi_summarize_bam_contig_depths --outputDepth /path/marine_gold_assembly/output/metabat/depth.txt /path/marine_gold_assembly/input/map/sr*mapped.sorted.bam

metabat2 -i /path/marine_gold_assembly/input/marmgCAMI2_short_read_pooled_gold_standard_assembly.fasta -m 1500 -a /path/marine_gold_assembly/output/metabat_bam/depth.txt --saveCls -l -o /path/marine_gold_assembly/output/metabat/marine_gold_f1k
```
`--saveCls` represents to save cluster memberships as a matrix format; `-l` means to output only sequence labels as a list in a column without sequences. More information about the command line options can be viewed by typing `metabat2 -h`.
## MetaBinner

## DAS Tool

###  Installation
Requirements:<br>
* boost >= 1.59.0 (dev and libs for boost_graph, system, filesystem and serialization)
* python >= 2.7
* cmake >= 3.8.2
* gcc/g++ >= 4.9 or intel >= 18.0.1.163 or llvm >= 8.0
(htslib 1.9 is downloaded and installed automatically if not present on the system)
```
# MetaBAT 2 (Linux 64-bit)
wget https://bitbucket.org/berkeleylab/metabat/downloads/metabat-static-binary-linux-x64_v2.12.1.tar.gz
tar xzvf metabat-static-binary-linux-x64_v2.12.1.tar.gz
mv metabat-static-binary-linux-x64_v2.12.1 metabat

cd metabat
mkdir build 
cd build
cmake -DCMAKE_INSTALL_PREFIX=$HOME/metabat ..
make
make install
cd ..
rm -rf build
```
MetaBAT can also run with Docker:
```
docker run <docker options> metabat/metabat:latest runMetaBat.sh

# For example:
docker run --workdir $(pwd) --volume $(pwd):$(pwd) metabat/metabat:latest runMetaBat.sh test/contigs.fa  test/contigs-1000.fastq.bam
```
You can see [INSTALL.md](https://bitbucket.org/berkeleylab/metabat/src/master/INSTALL.md) for Operating System specific installation instructions.

### Basic Usage
The easy way:
```
runMetaBat.sh <options> assembly.fasta sample1.bam [sample2.bam ...]
```
The slightly less easy way:<br>
a) Generate a depth file from BAM files
```
jgi_summarize_bam_contig_depths --outputDepth depth.txt *.bam 
```
b) Run metabat
```
metabat2 -i assembly.fasta -a depth.txt -o bins_dir/bin 
```
### Example:
We use the sorted data in the directory /path//marine_gold_assembly/input/map/ and the `original_contigs.fa` file to run MetaBAT:
```
jgi_summarize_bam_contig_depths --outputDepth /path/marine_gold_assembly/output/metabat/depth.txt /path/marine_gold_assembly/input/map/sr*mapped.sorted.bam

metabat2 -i /path/marine_gold_assembly/input/marmgCAMI2_short_read_pooled_gold_standard_assembly.fasta -m 1500 -a /path/marine_gold_assembly/output/metabat_bam/depth.txt --saveCls -l -o /path/marine_gold_assembly/output/metabat/marine_gold_f1k
```
