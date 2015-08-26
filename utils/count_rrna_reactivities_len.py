# count up lengths of rRNA reactivities (sanity check)

with open("data/rRNA_reactivities.txt") as f:
	for line in f:
		bits = line.strip().split("\t")
		transcript_id = bits[0]
		n_nucs = len(bits[1:])
		print("["+transcript_id+"]: ["+str(n_nucs)+"]")

		