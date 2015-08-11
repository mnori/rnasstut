# Getting set up
Please ensure you have the following installed:

* [Vagrant](http://docs.vagrantup.com/v2/installation/)
* [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

After installing Vagrant and Git, enter your home directory, and run:

```
git clone https://github.com/mnori/rnasstut.git
cd rnasstut
vagrant up
```

This grabs the tutorial repository, and sets up an Ubuntu virtual machine, upon which you can play around and run various RNA structure prediction methods.

# Tutorial
We will be exploring two well established RNA structure prediction methods: `Fold` from the `RNAstructure` package, and `ViennaFold`, which is part of the `ViennaRNA` package.

## RNAstructure: prediction from nucleotide sequence alone
We will first try to predict the secondary structure of *A. thaliana* 18S rRNA from its sequence alone, using the `RNAstructure` `Fold` method. 

### Running `RNAstructure Fold` from the command line
RNAstructure can be run from the command line or using the [web interface](http://rna.urmc.rochester.edu/RNAstructureWeb/Servers/Predict1/Predict1.html). The web service is useful if you have a single sequence to analyse. If, however, you have a large batch of  sequences to process, the command line is a much better option. In this tutorial, we will be running everything from the command line.

Before running `Fold`, we must set an environmental variable, which points to some files describing thermodynamic parameters for folding:

```
export DATAPATH=~/RNAstructure/data_tables
```

We can now run `Fold` to predict the RNA structure.

```
~/RNAstructure/exe/Fold ~/data/ath_18S.fasta ~/ath_18s_pred.txt
```

`~/data/ath_18S.fasta` is the input sequence (18S rRNA in fasta format).
`~/ath_18s_pred.txt` is the output file.

### Examining the output
-----------------------

Open `~/ath_18s_pred.txt`

This is a Connectivity Table (CT) file, described in detail [here](http://rna.urmc.rochester.edu/Text/File_Formats.html).

The file consists of around 20 structures. For each structure, the first line indicates its Gibbs free energy estimate. Structures with lower free energies are described first, and are the most favourable. The first structure in the file is the called the minimum free energy (MFE) structure.

After the free energy line, the remaining lines describe the structure itself:

* Column 1: nucleotide position
* Column 2: nucleotide letter
* Column 5: nucleotide position this base pairs to. 0 indicates that this position is not paired.
 
