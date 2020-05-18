from collections import defaultdict, namedtuple
from enum import Enum
import sys

from src.reduction import reduce_and_solve
from src.util import Run, Solution, run_to_string, string_to_run, subsequence_to_indices
from src.gbr import stringProcessor, takeParameter
from src.algorithms import lrs_branch_and_bound, lrs_dp, lrs_ilp


class Solver(Enum):
	NAIVE = 1
	DP = 2
	ILP = 3
	DP2 = 4
	ILP2 = 5


Run = namedtuple("Run", ["char", "length"])
Solution = namedtuple("Solution", ["size", "subsequences"])


def lrs(s, algo=Solver.DP, verbosity=0):
	'''
	Main method. Call with a regular a python string or a list.
	'''

	r = string_to_run(s)

	if algo in [Solver.NAIVE, Solver.DP, Solver.ILP]:
		if algo == Solver.NAIVE:
			solver = lrs_branch_and_bound
		elif algo == Solver.DP:
			solver = lrs_dp
		else:
			solver = lrs_ilp
		sol = reduce_and_solve(r, solver, verbosity)
		result = subsequence_to_indices(sub=sol.subsequences[0], ref=r)
		
	else:
		if algo == Solver.DP2:
			block_list = stringProcessor(takeParameter(["gbr", s, "dag"]))[0][0]
		elif algo == Solver.ILP2:
			block_list = stringProcessor(takeParameter(["gbr", s, "ilp"]))[0][0]
		else:
			raise ValueError("lrs received an unexpected algorithm type")
		ungapped_result = [Run(char=str(block.getBlockLetter()), length=block.getBlockValue()) for block in block_list]

		result = subsequence_to_indices(sub=ungapped_result, ref=r)
		
	return result


def main(argv):
	'''
	Command line interface for testing. Call as:
	lrs <string> [naive|dp|ilp|dp2|ilp2]
	'''

	if len(argv) < 2:
		print("Error: No input string provided. Please use format: lrs <string> [naive|dp|ilp|dp2|ilp2]")
		return
    
	s = argv[1]
	if s.startswith("[") and s.endswith("]"):
		s = s[1:-1].split(',')
    
	if len(argv) < 3:
		result = lrs(s, verbosity=1)
	elif len(argv) == 3:
		string_to_solver = {"naive": Solver.NAIVE, "dp": Solver.DP, "ilp": Solver.ILP, "dp2": Solver.DP2, "ilp2": Solver.ILP2}
		if argv[2] not in string_to_solver:
			print("Error: Unknown solver provided. Please use format: lrs <string> [naive|dp|ilp|dp2|ilp2]")
			return
		result = lrs(s, algo=string_to_solver[argv[2]], verbosity=0)
	else:
		print("Error: Excess arguments provided. Please use format: lrs <string> [naive|dp|ilp|dp2|ilp2]")
		return
	
	print("Solution: {} characters".format(len(result)))
	print("Input: {}".format(s))
	if isinstance(s, list):
		print("LRS:   {}".format([s[i] if i in result else ' '*len(s[i]) for i in range(len(s))]))
	else:
		print("LRS:   {}".format("".join([s[i] if i in result else ' '*len(s[i]) for i in range(len(s))])))


if __name__ == "__main__":
	main(sys.argv)