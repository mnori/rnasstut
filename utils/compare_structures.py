# Compares ViennaRNA or RNAstructure predicted structures against a phylogenetic structure
# @author Matthew Norris <matthew.norris@jic.ac.uk>

import os, sys

def main():

	if len(sys.argv) != 3:
		print ("Must call compare_structures.py with exactly 2 arguments")
		exit()

	pred_arg = sys.argv[1]
	ref_arg = sys.argv[2]

	# Path to the non-constrained RNAstructure prediction
	flag = pred_arg[:3]
	pred_filepath = pred_arg.split("=")[1]
	if flag == "-r=":
		pred_structure = get_rnastructure_pred(os.path.expanduser(pred_filepath))

	elif flag == "-v=":
		

	else:
		print ("Invalid flag ["+flag+"]")
		exit()

	# Path to the phylogenetic reference structure, to compare against
	ref_structure = get_ref_structure(os.path.expanduser(ref_arg))

	compare_structures(ref_structure, pred_structure)

# Compare predicted structure against ref. Calculate similarity statistics
def compare_structures(pred, ref):

	# Initialise some counters (ss = single stranded, ds = double stranded)
	# The tot values are tot predicted
	true_ss = true_ds = tot_ss = tot_ds = 0

	# Count up how many SS and DS predictions were correct, relative to the phylo structure
	n_nucs = len(ref)
	for i in range(0, n_nucs):
		if pred[i] == "s":
			tot_ss += 1
			if ref[i] == "s":
				true_ss += 1

		elif pred[i] == "d":
			tot_ds += 1
			if ref[i] == "d":
				true_ds += 1

	# print(str(true_ss)+" "+str(true_ds)+" "+str(tot_ss)+" "+str(tot_ds))

	true_ss = float(true_ss)
	true_ds = float(true_ds)

	# Calculate some summary stats
	pc_ss_true 	= round(100 * (true_ss / tot_ss), 2)
	pc_ds_true 	= round(100 * (true_ds / tot_ds), 2)
	pc_tot_true = round(100 * ((true_ss + true_ds) / (tot_ss + tot_ds)), 2)

	# Get TP, FP, TN, FN with respect SS predictions. Calc sens and spec
	tp_ss = true_ss
	tn_ss = true_ds
	fp_ss = tot_ss - true_ss
	fn_ss = tot_ds - true_ds

	sens_ss = round((100 * tp_ss) / (tp_ss + fn_ss), 2)
	spec_ss = round((100 * tn_ss) / (tn_ss + fp_ss), 2)

	# Get the same but with DS predictions. Basically same as SS but inverted.
	tp_ds = true_ds
	tn_ds = true_ss
	fp_ds = tot_ds - true_ds
	fn_ds = tot_ss - true_ss

	sens_ds = round((100 * tp_ds) / (tp_ds + fn_ds), 2)
	spec_ds = round((100 * tn_ds) / (tn_ds + fp_ds), 2)

	print("")
	print("RESULTS:")
	print("")
	print("Single stranded sensitivity:   % "+str(sens_ss))
	print("Single stranded specificity:   % "+str(spec_ss))
	print("Single stranded correct:       % "+str(pc_ss_true))
	print("")
	print("Double stranded sensitivity:   % "+str(sens_ds))
	print("Double stranded specificity:   % "+str(spec_ds))
	print("Double stranded correct:       % "+str(pc_ds_true))
	print("")
	print("Percentage agreement:          % "+str(pc_tot_true))
	print("")


# Load reference secondary structure into an array
def get_ref_structure(reference_filepath):
	ss_values = []
	with open(reference_filepath) as f:
		for line in f:
			bits = line.strip().split("\t")
			ss_values.append(bits[2])

	return ss_values

# Load RNAstructure prediction into an array
def get_rnastructure_pred(pred_filepath):
	ss_values = []
	with open(pred_filepath) as f:
		f.readline() # skip past the first line
		for line in f:
			if "ENERGY" in line: # found the next structure
				break

			bits = line.strip().split()
			ss_values.append("s" if bits[4] == "0" else "d")

	return ss_values

# Load Vienna prediction into an array
def get_vienna_pred(pred_filepath):
	print(pred_filepath)

# get the party started
main()