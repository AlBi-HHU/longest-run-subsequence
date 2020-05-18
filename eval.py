import os
import time
import sys

from lrs import lrs, Solver

def main(argv):
	if len(argv) != 4:
		print("Error: Incorrect number of arguments. Please use format: eval <input-path> <output-path> naive|dp|ilp|dp2|ilp2")
		return
	in_path = argv[1]
	out_path = argv[2]
	
	string_to_solver = {"naive": Solver.NAIVE, "dp": Solver.DP, "ilp": Solver.ILP, "dp2": Solver.DP2, "ilp2": Solver.ILP2}
	if argv[3] not in string_to_solver:
		print("Error: Unknown solver provided. Please use format: eval <input-path> <output-path> naive|dp|ilp|dp2|ilp2")
		return
	
	solver = string_to_solver[argv[3]]
	
	total_time = 0
	instances = 0
	with open(in_path, 'r') as strings, open(out_path, 'a') as results:
		lines = [line.rstrip("\n") for line in strings.readlines()]
		length = len(lines[0])
		alphabet_size = len(set([c for c in lines[0]]))
		
		start = time.time()
		for line in lines:
			if line.startswith("[") and line.endswith("]"):
				line = line[1:-1].split(',')
			result = lrs(line, solver)
		
		total_time = time.time() - start
		instances = len(lines)
		avg_time = total_time/len(lines)
			
		results.write("{};{};{};{}".format(argv[3], length, alphabet_size, avg_time))
	print("Processed {} instances in {} seconds total".format(instances, total_time))

if __name__ == "__main__":
	main(sys.argv)