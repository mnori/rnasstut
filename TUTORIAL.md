# Installation
First, make you have the following installed:

* [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
* [Vagrant](http://docs.vagrantup.com/v2/installation/)

After installing Git and Vagrant, enter your home directory, and run:

```
git clone https://github.com/mnori/rnasstut.git
cd rnasstut
vagrant up
```

This grabs the tutorial repository, and sets up an Ubuntu virtual machine (VM), upon which you can play around and run various RNA structure prediction methods.

Before running commands, you'll need to log into the VM by running `vagrant ssh` inside the tutorial folder. All of the tutorial commands should be executed within the VM.

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
~/RNAstructure/exe/Fold ~/data/18s.fasta ~/18s_rnastructure_pred.txt
```

`~/data/18S_rRNA.fasta` is the input sequence (18S rRNA in fasta format).
`~/18s_rnastructure_pred.txt` is the output file.

### The output

Open `~/18s_rnastructure_pred.txt`

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
RNAfold < ~/data/18s.fasta > ~/18s_vienna_pred.txt
```
`
### Examining the output
After opening the output file `~/18s_vienna_pred.txt`, note the different format used to describe the secondary structure. This file is in Vienna's "dot bracket" notation. Paired bases are indicated using round brackets, whilst unpaired bases are denoted using dots. 

In this example, only the MFE structure is listed. The free energy estimate is provided at the end of the file.

## Viewing predicted structures
We're going to compare `RNAstructure` and `Vienna` predictions, but first we need to make sure both structure files are in the same format. To convert RNAstructure's quirky CT file into dot bracket notation, use:

```
~/RNAstructure/exe/ct2dot ~/18s_rnastructure_pred.txt 1 ~/18s_rnastructure_pred.dot.txt 
```

The first parameter is the raw CT file, and "1" indicates that we want to convert the first entry in the CT file, i.e. the MFE structure. The last parameter is the output file.

Before we plot the structures, we should add a better label  to the beginning of each file. This can be done in a text editor, or quickly using the command line:

```
sed "1s/.*/\>rnastructure/" ~/18s_rnastructure_pred.dot.txt > rnastructure.dot
sed "1s/.*/\>vienna/" ~/18s_vienna_pred.txt > vienna.dot
```

We can now generate structure diagrams for both predictions using `Vienna`'s `RNAplot`:

```
RNAplot -o svg < ~/rnastructure.dot
RNAplot -o svg < ~/vienna.dot
```
The generated images are named according to the labels that we added in the previous step. To access the images on your host machine, you can copy them to the `/vagrant` folder:

`cp ~/*.svg /vagrant`

Then open the `*.svg` files from the tutorial install folder. By comparing the diagrams, you should be able to see some agreement between the methods for shorter range interactions, with less agreement for longer range interactions.

## `RNAstructure`: prediction using sequence and constraints
So far, we've predicted RNA structures using sequence alone. This is not particularly accurate. We can try to improve the prediction by including extra information from a chemical probing experiment. These extra data are called constraints, and *RNAstructure* uses these in the thermodynamics calculations as pseudo free energy terms.

We'll be using constraints generated from a dimethyl sulfate (DMS) probing experiment of the 18S rRNA. DMS reacts with C and A nucleotides that are not involved in base pairing. The experiment produces normalised reactivity values. Values approaching 1 or above indicate a strong reactivity and thus a high probability that the corresponding base is unpaired.

### The constraints file

The file `~/data/18s_constraints.txt` contains normalised DMS reactivities in a format that `RNAstructure` understands. The first 10 lines look like this:

```
2	0.012685795205
3	0.0
4	0.0
11	0.369865767367
13	0.0
14	0.0
17	0.0
18	0.0
19	0.0
22	0.291074839291
...
```

The first column is the sequence position and the 2nd is the normalised DMS reactivity. Missing positions are for G or U nucleotides, where DMS reactivity does not apply.

We'll now run a prediction using these constraints:

```
~/RNAstructure/exe/Fold ~/data/18s.fasta ~/18s_rnastructure_pred_constrained.txt -dms ~/data/18s_constraints_rnastructure.txt
```

You can check out the output by drawing a structure plot as described earlier.

## `ViennaFold`: prediction from sequence and constraints
Unlike `RNAstructure`, `ViennaFold` does not support quantitative "soft" reactivity values; it is only able to handle "hard" constraints encoded as "unconstrained", "paired" or "unpaired" states. The file `~/data/18s_constraints_vienna.txt` contains some constraints in `ViennaRNA`'s format:

```
>Ath_18S
TACCTGGTTGATCCTGCCAGTAGTCATATGCTTGTCTCAAAGATTAAG ...
.|||........||..|||..|..||.|..|....|...x..x..... ...
```

The first two lines describe the sequence, and the last line describes the constraints. `.` indicates no constraint, `|` that the base must be paired, and `x` that the base must be unpaired. A detailed description of the format can be found [here](http://www.tbi.univie.ac.at/RNA/RNAfold.html).

These Vienna constraints have been generated by considering any base with a reactivity value under 0.3 as paired, and any value above 0.7 as unpaired. Bases with reactivities between 0.3 and 0.7 are considered ambiguous and are not constrained. This is a pretty crude way of treating the data; in practice, one might want to experiment with different classification thresholds.

To run ViennaFold with the constraints, use:

`RNAfold < ~/data/18s_constraints_vienna.txt > ~/18s_vienna_pred_constrained.txt -C`

The extra `-C` option indicates that we are running in constraints mode. As with the earlier example, the output will be in dot bracket notation. Try generating a structure diagram, and compare it against the results you made earlier.

## Determining structure prediction accuracy

We can assess the performance of each prediction by comparing against a high-confidence reference stucture. The best structure available for the 18S rRNA comes from phylogenetic comparisons. The file `18s_phylogenetic.txt` contains a summary of this structure:

```
1	T	s
2	A	s
3	C	s
4	C	d
5	T	d
6	G	d
7	G	d
8	T	s
9	T	s
10	G	s
...
```

Column 1 is the position, column 2 the base. In column 3, `s` indicates that the base is single stranded, whilst `d` denotes that the base is paired (i.e. double stranded). To assess the accuracy, we'll compare each prediction against the reference, and count the true positives (TPs), true negatives (TNs), false positives (FNs) and false negatives (FNs) at each position. We'll do this using a python script. To compare against 



