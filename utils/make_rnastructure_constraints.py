import os

# Generate an RNAstructure constraints file from the reactivities output

input_filepath = os.path.expanduser("~/data/18s_reactivities.txt")
output_filepath = os.path.expanduser("~/data/18s_constraints.txt")

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
		