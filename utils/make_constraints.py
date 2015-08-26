import os

# Generate constraints files from the reactivity output

def main():
	input_filepath = os.path.expanduser("~/data/18s_reactivities.txt")
	output_filepath = os.path.expanduser("~/data/18s_constraints_rnastructure.txt")
	generate_rnastructure_constraints(input_filepath, output_filepath)

	fasta_filepath = os.path.expanduser("~/data/18s.fasta")
	output_filepath = os.path.expanduser("~/data/18s_constraints_vienna.txt")
	generate_vienna_constraints(input_filepath, fasta_filepath, output_filepath)

def generate_rnastructure_constraints(input_filepath, output_filepath):

	outfile = open(output_filepath, "w")

	infile = open(input_filepath, "r")
	line = infile.readline()
	infile.close()

	bits = line.split("\t")
	pos = 0
	for value in bits:
		if pos != 0 and value != "NA":
			outfile.write(str(pos)+"\t"+value+"\n")
		pos += 1

	outfile.close()

def generate_vienna_constraints(input_filepath, fasta_filepath, output_filepath):
	fasta_filepath = os.path.expanduser("~/data/18s.fasta")
	output_filepath = os.path.expanduser("~/data/18s_constraints_vienna.txt")
	paired_thresh = 0.3
	unpaired_thresh = 0.7

	# Grab the sequence out of the 18s.fasta
	f = open(fasta_filepath, "r")
	label = f.readline().strip()
	seq = f.readline().strip()
	f.close()

	# Grab the constraints
	f = open(input_filepath, "r")
	line = f.readline()
	f.close()
	bits = line.split("\t")

	# Generate Vienna constraints, this includes a sequence label, the sequence, 
	# and then the constraints.
	outfile = open(output_filepath, "w")
	outfile.write(label+"\n")
	outfile.write(seq+"\n")
	pos = 0
	for value in bits:
		if pos != 0:
			if value == "NA":
				# is G or U. no constraint
				char = "." 
			
			else:
				floatval = float(value)
				if floatval < paired_thresh:
					# below the threshold, unpaired constraint
					char = "x" 

				elif floatval < unpaired_thresh: 
					# between the thresholds, no constraint
					char = "."

				else: 
					# above unpaired threshold, paired constraint
					char = "|" # 

			outfile.write(char)
		pos += 1	

	outfile.write("\n")
	outfile.close()

# get the party started
main()
