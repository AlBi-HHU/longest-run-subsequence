import os
import time
import sys
import resource

from longestrunsubsequence import lrs, Solver

def main(argv):
	if len(argv) != 4:
		print("Error: Incorrect number of arguments. Please use format: eval <input-path> <output-path> naive|auto|dp|ilp")
		return
	in_path = argv[1]
	out_path = argv[2]
	
	string_to_solver = {"auto": Solver.AUTO, "naive": Solver.NAIVE, "dp": Solver.DP, "ilp": Solver.ILP}
	if argv[3] not in string_to_solver:
		print("Error: Unknown solver provided. Please use format: eval <input-path> <output-path> naive|auto|dp|ilp")
		return
	
	solver = string_to_solver[argv[3]]
	
	total_time = 0
	instances = 0
	max_consumption = 0
	with open(in_path, 'r') as strings, open(out_path, 'a') as results:
		lines = [line.rstrip("\n") for line in strings.readlines()]
		length = len(lines[0])
		alphabet_size = len(set([c for c in lines[0]]))
		
		start = time.time()
		for line in lines:
			if line.startswith("[") and line.endswith("]"):
				line = line[1:-1].split(',')
			result = lrs(line, solver, verbosity=0)
			#print(result)
			if sys.platform == "linux":
				memory_kb = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss + resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
				max_consumption = max(max_consumption, memory_kb)
		
		total_time = time.time() - start
		instances = len(lines)
		avg_time = total_time/len(lines)
			
		results.write("{};{};{};{};{}".format(argv[3], length, alphabet_size, avg_time, max_consumption))
	print("Processed {} instances in {} seconds total".format(instances, total_time))
	if sys.platform == "linux":
		memory_kb = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss + resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
		print("Maximum memory usage: {} MB".format(memory_kb / 1024))

if __name__ == "__main__":
	main(sys.argv)
