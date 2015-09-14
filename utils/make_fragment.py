import os

# Generate constraints files from the reactivity output

def main():
	gen_fragment(1, 1808)

def gen_fragment(start, stop):
	# start and stop are inclusive. they also start at 1
	input_filepath = os.path.expanduser("~/data/full_18s_reactivities.txt")
	output_filepath = os.path.expanduser("~/data/18s_constraints_rnastructure.txt")
	generate_rnastructure_constraints(input_filepath, output_filepath, start=start, stop=stop)

	fasta_filepath = os.path.expanduser("~/data/full_18s.fasta")
	output_filepath = os.path.expanduser("~/data/18s_constraints_vienna.txt")
	generate_vienna_constraints(input_filepath, fasta_filepath, output_filepath, start=start, stop=stop)

	fasta_input = os.path.expanduser("~/data/full_18s.fasta")
	fasta_output = os.path.expanduser("~/data/18s.fasta")
	slice_fasta(fasta_input, fasta_output, start=start, stop=stop)

	phylo_input = os.path.expanduser("~/data/full_18s_phylogenetic.txt")
	phylo_output = os.path.expanduser("~/data/18s_phylogenetic.txt")
	slice_phylo(phylo_input, phylo_output, start=start, stop=stop)

def generate_rnastructure_constraints(input_filepath, output_filepath, start, stop):
	outfile = open(output_filepath, "w")
	infile = open(input_filepath, "r")

	line = infile.readline()
	infile.close()

	bits = line.split("\t")[1:]
	pos = 1
	for value in bits[start - 1:stop]:
		if value != "NA":
			outfile.write(str(pos)+"\t"+value+"\n")
		pos += 1

	outfile.close()

def generate_vienna_constraints(input_filepath, fasta_filepath, output_filepath, start, stop):
	output_filepath = os.path.expanduser(output_filepath)
	paired_thresh = 0.3
	unpaired_thresh = 0.7

	# Grab the sequence out of the 18s.fasta
	f = open(fasta_filepath, "r")
	label = f.readline().strip()
	seq = f.readline().strip()[start-1: stop]
	f.close()

	# Grab the constraints
	f = open(input_filepath, "r")
	line = f.readline()
	f.close()
	bits = line.split("\t")[1:]

	# Generate Vienna constraints, this includes a sequence label, the sequence, 
	# and then the constraints.
	outfile = open(output_filepath, "w")
	outfile.write(label+"\n")
	outfile.write(seq+"\n")
	pos = 1
	for value in bits[start - 1:stop]:
		if value == "NA":
			# is G or U. no constraint
			char = "." 
		
		else:
			floatval = float(value)
			if floatval < paired_thresh:
				# below the paired constraint threshold
				char = "|" 

			elif floatval < unpaired_thresh: 
				# between the thresholds, no constraint
				char = "."

			else: 
				# above unpaired constraint threshold
				char = "x"

		outfile.write(char)
		pos += 1	

	outfile.write("\n")
	outfile.close()

def slice_fasta(input_filepath, output_filepath, start, stop):
	with open(input_filepath, "r") as r:
		seq_id = r.readline().strip()
		seq = r.readline().strip()[start - 1:stop]
		with open(output_filepath, "w") as w:
			w.write(seq_id+"\n")
			w.write(seq)

def slice_phylo(phylo_input, phylo_output, start, stop):
	buf = ""
	pos = 1
	with open(phylo_input, "r") as f:
		for line in f:
			if pos >= start and pos <= stop:
				buf += line
			pos += 1

	with open(phylo_output, "w") as f:
		f.write(buf)

# get the party started
main()
