[vagrant setup / ssh details go here]

There are two well established tools for predicting RNA structure. One is called "Fold" from the "RNAstructure" package. The other is ViennaFold, which is part of the ViennaRNA package.

We will first try to predict the secondary structure of 18S rRNA from its sequence alone, using the "RNAstructure" method. 

Before running Fold, we must set an environmental variable, which points to some files describing thermodynamic parameters for folding:
`export DATAPATH=~/RNAstructure/data_tables`

We can now run the Fold program. `~/data/ath_18S.fasta` is the input sequence (18S rRNA in fasta format) and `~/ath_18s_pred.txt` is the output file.
`~/RNAstructure/exe/Fold ~/data/ath_18S.fasta ~/ath_18s_pred.txt`

