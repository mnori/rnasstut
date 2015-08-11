[vagrant setup / ssh details go here]

There are two well established tools for predicting RNA structure. One is called "Fold" from the "RNAstructure" package. The other is ViennaFold, which is part of the ViennaRNA package.

We will first try to predict the secondary structure of 18S rRNA from its sequence alone, using the "RNAstructure" method. We'll do the predictions using the command line; there is also a web based version of RNAstructure which can be found here: <LINKY>

Before running Fold, we must set an environmental variable, which points to some files describing thermodynamic parameters for folding:

```
export DATAPATH=~/RNAstructure/data_tables
```

We can now run the Fold program. `~/data/ath_18S.fasta` is the input sequence (18S rRNA in fasta format) and `~/ath_18s_pred.txt` is the output file.

```
~/RNAstructure/exe/Fold ~/data/ath_18S.fasta ~/ath_18s_pred.txt
```

File format description
=======================

Open `~/ath_18s_pred.txt`

The minimum free energy structure is the first one listed in the file.
The bits we're interested in are Column 1 and Column 5.

Column 1: nucleotide position
Column 2: nucleotide letter
Column 5: nucleotide position this base pairs to. 0 indicates that this position is not paired.

The official description of this file format can be found here: 

