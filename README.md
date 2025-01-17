# UltraBinner

Use DAS Tool(v1.1.1) to integrate the results of three binners (MetaBinner, CONCOCT V1.1.0, MetaBAT V2.12.1) to calculate an optimized, non-redundant set of bins from a single assembly. <br>
IF you have the result of other binners(e.g. MaxBin, SolidBin), you can also add the results as the input of DAS Tool.<br>
<br>

## MetaBinner
A method imporves large scale binning performance with ensemble K-means by considering multiple types of features.You can get it from https://github.com/ziyewang/MetaBinner.

### Installation
We recommend using conda to run Metabinner. Download here
After installing Anaconda (or miniconda), fisrt obtain Metabinner:
```
git clone https://github.com/ziyewang/MetaBinner
```
Then simply create a metabinner environment
```
conda env create -f metabinner_env.yaml
conda activate metabinner_env
```
Set checkM data path as described in here
```
checkm data setRoot <checkm_data_dir>
```
You may need to run these commands to make the files executable
```
chmod +x ~path_to_MetaBinner/auxiliary/test_getmarker.pl
chmod +x ~path_to_MetaBinner/auxiliary/FragGeneScan1.19/run_FragGeneScan.pl
chmod +x ~path_to_MetaBinner/auxiliary/hmmer-3.1b1/bin/hmmsearch
chmod +x ~path_to_MetaBinner/auxiliary/FragGeneScan1.19/FragGeneScan
```

### Usage
#### Data preprocessing
#### Get Coverage Profile<br>
You download the data and put the files into your input directory. Then slightly modify `gen_cov.sh` and run it.<br>
Note that minimap2, samtools and bedtools are need to be installed to run `gen_cov.sh`.<br>

You input directory should look like this:
```
.
+-- assembly.fasta
+-- sr
|   +-- short_read_sample_1
|   +-- short_read_sample_2
+-- pb
|   +-- pacbio_sample_1
|   +-- pacbio_sample_2
|   +-- pacbio_sample_3
```
For conda environment, you should check whether perl is installed.
<br>

#### Input files<br>
You need to run like this to obtain the composition profiles and the coverage profiles (only short read samples; only long read samples)
```
scripts/run.sh input_path/contigs.fasta contigs_length_threshold kmer_length
```
"contigs_length_threshold" means only the contigs longer than the value are kept for binning. For example,
```
./run.sh input_path/contigs.fasta 1000 4
```
Note: The `coverage_new.tsv` file should be put into the "input_path" and if the sample numbers of the long read samples and the short read samples are different, you need to change the `split_coverage.py`.
<br>

#### Run MetaBinner<br>
```
OPENBLAS_NUM_THREADS=1 python Metabinner.py --contig_file input_path/contigs.fasta --coverage_profiles input_path/coverage_sr_new.tsv --composition_profiles input_path/kmer_4_f0.csv --output output_path/result.tsv --log output_path/result.log --pacbio_read_profiles input_path/coverage_pb_new.tsv --use_hmm --hmm_icm_path path_to_MetaBinner/hmm_data/hmm/
```
More information about the command line options can be viewed by typing `MetaBinner -h`.

### Example
#### Data preprocessing<br>
We downloaded the raw data from the 2nd CAMI Challenge Marine Dataset(https://data.cami-challenge.org/participate), and decompressed the data into /path/marine_gold_assembly/input/. Then modify gen_cov.sh and run it.<br>
Then we run `run.sh` to get the input files:
```
./run.sh /path/marine_gold_assembly/input/marmgCAMI2_short_read_pooled_gold_standard_assembly.fa 1000 4
```

#### Run MetaBinner<br>
```
OPENBLAS_NUM_THREADS=1 python Metabinner.py --contig_file /path/marine_gold_assembly/input/marmgCAMI2_short_read_pooled_gold_standard_assembly_f1k.fa --coverage_profiles /path/marine_gold_assembly/input/coverage_sr_new.tsv --composition_profiles /path/marine_gold_assembly/input/kmer_4_f0.csv --output /path/marine_gold_assembly/output/MetaBinner/result.tsv --log /path/marine_gold_assembly/output/MetaBinner/result.log --pacbio_read_profiles /path/marine_gold_assembly/input/coverage_pb_new.tsv --use_hmm --hmm_icm_path path_to_MetaBinner/hmm_data/hmm/
```
<br>

## CONCOCT v1.1.0
CONCOCT is a program for unsupervised binning of metagenomic contigs by using nucleotide composition, coverage data in multiple samples and linkage data from paired end reads. You can get it from https://github.com/BinPro/CONCOCT.

### Please cite
If you use CONCOCT in your publication, please cite:<br>
<br>
Johannes Alneberg, Brynjar Smári Bjarnason, Ino de Bruijn, Melanie Schirmer, Joshua Quick, Umer Z Ijaz, Leo Lahti, Nicholas J Loman, Anders F Andersson & Christopher Quince (2014). Binning metagenomic contigs by coverage and composition.<br>
Nature Methods, doi: 10.1038/nmeth.3103

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
Generate table with coverage depth information per sample and subcontig. This step assumes the directory 'mapping' contains sorted and indexed bam files where each sample has been mapped against the original contigs.
```
concoct_coverage_table.py contigs_1K.bed mapping/Sample*.sorted.bam > coverage_table.tsv
```
Run CONCOCT
```
concoct --composition_file contigs_10K.fa --coverage_file coverage_table.tsv -b concoct_output/
```
### Example:
We use the contigs.fasta and coverage profile in /path/marine_gold_assembly/input/ to run CONCOCT.<br>
Note: We only use the coverage profiles of the short read samples.
```
concoct --coverage_file /path/marine_gold_assembly/input/coverage_sr_new.tsv --composition_file /path/marine_gold_assembly/input/marmgCAMI2_short_read_pooled_gold_standard_assembly_f1k.fa -b /path/marine_gold_assembly/output/concoct/ -t 46
``` 
`-t` is the number of threads to use, more information about the command line options can be viewed by typing `concoct -h`.
<br>

## MetaBAT v2.12.1
MetaBAT integrates the Tetranucleotide frequency distance Probability (TDP) and the abundance distance probability (ADP) of each contig pair and modified k-medoid clustering algorithm is utilized for contig binning. You can get it from https://bitbucket.org/berkeleylab/metabat/src/master/.

### Please cite
If you use MetaBAT in your publication, please cite:<br>
<br>
Dongwan D. Kang, Jeff Froula, Rob Egan & Zhong Wang(2015). MetaBAT, an efficient tool for accurately reconstructing single genomes from complex microbial communities.<br>
PeerJ 3, 1165, doi: 10.7717/peerj.1165.

###  Installation
Requirements:<br>
* boost >= 1.59.0 (dev and libs for boost_graph, system, filesystem and serialization)
* python >= 2.7
* cmake >= 3.8.2
* gcc/g++ >= 4.9 or intel >= 18.0.1.163 or llvm >= 8.0<br>
(htslib 1.9 is downloaded and installed automatically if not present on the system)
```
#stable release version
wget https://bitbucket.org/berkeleylab/metabat/get/master.tar.gz
tar xzvf master.tar.gz
cd berkeleylab-metabat-*

#run the installation script
mkdir build && cd build && cmake .. && make && make install
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
#### Run MetaBAT<br>
We used the `sr*mapped.sorted.bam` files in /path/marine_gold_assembly/input/map/ to run MetaBAT2, the sorted files generated by `gen_cov.sh`.<br>
Note: We only use the coverage profiles of the short read samples.
```
jgi_summarize_bam_contig_depths --outputDepth /path/marine_gold_assembly/output/metabat/depth.txt /path/marine_gold_assembly/input/map/sr*mapped.sorted.bam

metabat2 -i /path/marine_gold_assembly/input/marmgCAMI2_short_read_pooled_gold_standard_assembly.fasta -m 1500 -a /path/marine_gold_assembly/output/metabat_bam/depth.txt --saveCls -l -o /path/marine_gold_assembly/output/metabat/marine_gold
```
`-m` means the minimum size of a contig for binning (should be >=1500); `--saveCls` represents to save cluster memberships as a matrix format; `-l` means to output only sequence labels as a list in a column without sequences. More information about the command line options can be viewed by typing `metabat2 -h`.

#### Processing MetaBAT output files<br>
Using `metabat2_to_binlabel.py` to convert bins file to a result file:
```
metabat2_to_binlabel.py --paths /path/marine_gold_assembly/output/metabat/marine_gold -o /path/marine_gold_assembly/output/metabat/marine_gold_metabinner_result.tsv
```
<br>

## DAS Tool v1.1.1
DAS Tool is an automated method that integrates the results of a flexible number of binning algorithms to calculate an optimized, non-redundant set of bins from a single assembly. You can git it from https://github.com/cmks/DAS_Tool.

### Please cite
If you use DAS Tool in your publication, please cite:<br>
<br>
Christian M. K. Sieber, Alexander J. Probst, Allison Sharrar, Brian C. Thomas, Matthias Hess, Susannah G. Tringe & Jillian F. Banfield (2018). Recovery of genomes from metagenomes via a dereplication, aggregation and scoring strategy. <br>
Nature Microbiology. https://doi.org/10.1038/s41564-018-0171-1.

### Installation
DAS Tool can be installed via bioconda and homebrew. You can also install DAS Tool manually，for details, see [install](https://github.com/cmks/DAS_Tool#installation). We install DAS Tool using conda:
```
conda config --add channels defaults
conda config --add channels bioconda
conda config --add channels conda-forge

conda install -c bioconda das_tool
```

### Usage
#### Preparation of input files
The input of DAS Tool should be a tab separated file of scaffold-IDs and bin-IDs, file example:
```
Scaffold_1	bin.01
Scaffold_8	bin.01
Scaffold_42	bin.02
Scaffold_49	bin.03
```
Some binning tools (such as CONCOCT) provide a comma separated tabular output. To convert a comma separated file into a tab separated file a one liner can be used: 
```
perl -pe "s/,/\t/g;" scaffolds2bin.csv > scaffolds2bin.tsv.
```
Some binning tools (such as MetaBinner) provide a CAMI verification format output:
```
@Version:0.9.0
@SampleID:a unique identifier for a sequence sample
@@SEQUENCEID    BINID
Scaffold_1	bin.01
Scaffold_8	bin.01
Scaffold_42	bin.02
Scaffold_49	bin.03
```
You should delete the header tag information.

#### Run DAS Tool
```
DAS_Tool -i methodA.scaffolds2bin,...,methodN.scaffolds2bin -l methodA,...,methodN -c contigs.fa -o myOutput
```

### Example:
#### Data preprocessing<br>
We use the output of the three methods mentioned above as the input of the DAS Tool:<br>
* MetaBinner output file: /path/marine_gold_assembly/output/MetaBinner/result.tsv<br>
  For MetaBinner output, you should put it into /path/marine_gold_assembly/output/das_tool/ and delete the header tags.<br>
* CONCOCT output file: /path/marine_gold_assembly/output/concoct/clustering_gt1000.csv<br>
* MetaBAT output file: /path/marine_gold_assembly/output/metabat/marine_gold_f1k_metabinner_result.tsv<br>

```
perl -pe "s/,/\t/g;" /path/marine_gold_assembly/output/concoct/clustering_gt1000.csv > /path/marine_gold_assembly/output/das_tool/concoct.scaffolds2bin.tsv
perl -pe "s/,/\t/g;" /path/marine_gold_assembly/output/metabat/marine_gold_metabinner_result.tsv > /path/marine_gold_assembly/output/das_tool/metabat.scaffolds2bin.tsv
```

#### Run DAS Tool:
```
cd /path/marine_gold_assembly/output/das_tool
DAS_Tool -i concoct.scaffolds2bin.tsv,metabat.scaffolds2bin.tsv,metabinner.scaffolds2bin.tsv -l concoct,metabat,metabinner -c /path/marine_gold_assembly/iutput/marmgCAMI2_short_read_pooled_gold_standard_assembly_f1k.fa -o ensemble --threads 25 --score_threshold 0.3
```
`--threads` is the number of threads we use;`--score_threshold` set the threshold to keep selecting bins(default: 0.5).More information about the command line options can be viewed by typing `DAS_Tool -h`.

#### Process DAS Tool output files to meet CAMI verification format：<br>
Add header tags (e.g. @Version, @SampleID, @@SEQUENCEID	TAXID	BINID) to the file, see [file_formats](https://github.com/CAMI-challenge/contest_information/blob/master/file_formats/CAMI_B_specification.mkd) for details.<br>
We use the `add_header_tags.py` to add header tags:
```
python add_header_tags.py -r /path/marine_gold_assembly/output/das_tool/ensemble_DASTool_scaffolds2bin.txt -f /path/marine_gold_assembly/iutput/marmgCAMI2_short_read_pooled_gold_standard_assembly_f1k.fa -o /path/marine_gold_assembly/output/das_tool/ensemble_DASTool_scaffolds2bin.tsv
```
<br>

## Contacts and bug reports
Please send bug reports or questions to PingqinHuang: 18210240092@fudan.edu.cm, Ziye Wang: zwang17@fudan.edu.cn and Dr. Shanfeng Zhu: zhusf@fudan.edu.cn
