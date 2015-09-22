# Compares ViennaRNA or RNAstructure predicted structures against a phylogenetic structure
# @author Matthew Norris <matthew.norris@jic.ac.uk>

import os, sys

def main():

	if len(sys.argv) != 3:
		print ("Must call compare_structures.py with exactly 2 arguments")
		exit()

	pred_arg = sys.argv[1]
	ref_arg = os.path.expanduser(sys.argv[2])

	# Path to the non-constrained RNAstructure prediction
	flag = pred_arg[:3]
	pred_filepath = os.path.expanduser(pred_arg.split("=")[1])
	if flag == "-r=":
		pred_structure = get_rnastructure_pred(pred_filepath)

	elif flag == "-v=":
		pred_structure = get_vienna_pred(pred_filepath)

	else:
		print ("Invalid flag ["+flag+"]")
		exit()

	# Path to the phylogenetic reference structure, to compare against
	ref_structure = get_ref_structure(ref_arg)

	compare_structures(pred_structure, ref_structure)

# Compare predicted structure against ref. Calculate similarity statistics
def compare_structures(pred, ref):

	pred_p = pred_n = tp = tn = 0

	# Count up how many SS and DS predictions were correct, relative to the phylo structure
	n_nucs = len(ref)
	for i in range(0, n_nucs):

		if pred[i] == "d":
			pred_p += 1
			if ref[i] == "d":
				tp += 1

		elif pred[i] == "s":
			pred_n += 1
			if ref[i] == "s":
				tn += 1

	# print(str(true_ss)+" "+str(true_ds)+" "+str(tot_ss)+" "+str(tot_ds))
	fp = pred_p - tp
	fn = pred_n - tn
	fp = float(fp)
	tp = float(tp)
	fn = float(fn)
	fp = float(fp)

	ppv 		= round((100 * tp) / (tp + fp), 2)
	sensitivity	= round((100 * tp) / (tp + fn), 2)
	npv			= round((100 * tn) / (tn + fn), 2)
	specificity	= round((100 * tn) / (tn + fp), 2)
	accuracy 	= round((100 * (tp + tn)) / (tp + fp + tn + fn), 2)

	print("")
	print("    Results with respect to double stranded")
	print("    ---------------------------------------")
	print("")
	print("    Positive predictive value: "+str(ppv))
	print("    Sensitivity:               "+str(sensitivity))
	print("    Negative predictive value: "+str(npv))
	print("    Specificity:               "+str(specificity))
	print("    Overall accuracy:          "+str(accuracy))
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
	ss_values = []
	with open(pred_filepath) as f:
		dotbracket = f.readlines()[2]
		for pos in range(0, len(dotbracket)):
			ss_values.append("s" if dotbracket[pos] == "." else "d")

	return ss_values

# get the party started
main()