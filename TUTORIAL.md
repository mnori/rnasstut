# Installation
First, make you have the following installed:

* [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
* [Vagrant](http://docs.vagrantup.com/v2/installation/)

After installing Vagrant and Git, enter your home directory, and run:

```
git clone https://github.com/mnori/rnasstut.git
cd rnasstut
vagrant up
```

This grabs the tutorial repository, and sets up an Ubuntu virtual machine, upon which you can play around and run various RNA structure prediction methods.

# Tutorial
We will be exploring two well established RNA structure prediction methods: `Fold` from the `RNAstructure` package, and `RNAfold`, which is part of the `ViennaRNA` package. Both methods use thermodynamic modelling to find optimum folds.

## `RNAstructure`: prediction from nucleotide sequence alone
We will first try to predict the secondary structure of *A. thaliana* 18S rRNA from its sequence alone, using the `RNAstructure` `Fold` method.

### Running `RNAstructure Fold` from the command line
`RNAstructure` can be run from the command line or using the [web interface](http://rna.urmc.rochester.edu/RNAstructureWeb/Servers/Predict1/Predict1.html). The web version is useful if you have a single sequence to analyse. If, however, you have a large batch of  sequences to process, the command line is a much better option, since the analysis can be automated. In this tutorial, we will be running everything from the command line.

Before running `Fold`, we must set an environmental variable, which points to a folder containing thermodynamic parameters for folding. These are provided as part of the `RNAstructure` package:

```
export DATAPATH=~/RNAstructure/data_tables
```

We can now run `Fold` to predict the RNA structure:

```
~/RNAstructure/exe/Fold ~/data/ath_18S.fasta ~/ath_18s_rnastructure_pred.txt
```

`~/data/ath_18S.fasta` is the input sequence (18S rRNA in fasta format).
`~/ath_18s_rnastructure_pred.txt` is the output file.

### The output

Open `~/ath_18s_rnastructure_pred.txt`

This is a Connectivity Table (CT) file, described in detail [here](http://rna.urmc.rochester.edu/Text/File_Formats.html).

The file consists of around 20 structures. For each structure, the first line indicates its Gibbs free energy estimate. Structures with lower free energies are listed first, and are the most favourable. The first structure in the file is the minimum free energy (MFE) structure.

After the free energy value, the remaining lines describe the structure itself:

* Column 1: nucleotide position
* Column 2: nucleotide letter
* Column 5: nucleotide position that this position pairs to. 0 indicates that this position is not paired.

## `ViennaFold`: prediction from nucleotide sequence alone
`ViennaFold` is an alternative thermodynamics-based RNA structure prediction method. We will try running this from the command line to make new predictions that will complement those produced earlier.

### Running `Vienna RNAfold` from the command line
As with `RNAstructure`, there is a web based equivalent for the command we're about to run, which can be found [here](http://rna.tbi.univie.ac.at/cgi-bin/RNAfold.cgi). To run from the command line:

```
RNAfold < ~/data/ath_18S.fasta > ~/ath_18s_vienna_pred.txt
```

### Examining the output
After opening the output file `~/ath_18s_vienna_pred.txt`, note the different format used to describe the secondary structure. This file is in Vienna's "dot bracket" notation. Paired bases are indicated using round brackets, whilst unpaired bases are denoted using dots. 

In this example, only the MFE structure is listed. The free energy estimate is provided at the end of the file.

## Viewing predicted structures
We're going to compare `RNAstructure` and `Vienna` predictions, but first we need to make sure both structure files are in the same format. To convert RNAstructure's quirky CT file into dot bracket notation, use:

```
~/RNAstructure/exe/ct2dot ~/ath_18s_rnastructure_pred.txt 1 ~/ath_18s_rnastructure_pred.dot.txt 
```

The first parameter is the raw CT file, and "1" indicates that we want to convert the first entry in the CT file, i.e. the MFE structure. The last parameter is the output file.

Before we plot the structures, we should add a better label  to the beginning of each file. This can be done in a text editor, or quickly using the command line:

```
sed "1s/.*/\>rnastructure/" ~/ath_18s_rnastructure_pred.dot.txt > rnastructure.dot
sed "1s/.*/\>vienna/" ~/ath_18s_vienna_pred.txt > vienna.dot
```

We can now generate structure diagrams for both predictions using the `Vienna`'s `RNAplot`:

```
RNAplot -o svg < ~/rnastructure.dot
RNAplot -o svg < ~/vienna.dot
```
The generated images are named according to the labels that we added in the previous step. To access the images on your host machine, you can copy them to the `/vagrant` folder:

`cp ~/*.svg /vagrant`

Then open the `*.svg` files from the tutorial install folder using a modern web browser. By looking at the structures, you should be able to see some agreement between the methods for shorter range interactions, with less agreement for longer range interactions.