 #!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Longest Run Subsequence
Sven Schrinner, Manish Goel, Michael Wulfert, Philipp Spohr, Korbinian Schneeberger, Gunnar W. Klau
"""

from enum import Enum
from .reduction import reduce_and_solve
from .util import Run, Solution, string_to_run, subsequence_to_indices
from .algorithms import lrs_auto, lrs_branch_and_bound, lrs_dp, lrs_ilp


class Solver(Enum):
	AUTO = 0
	NAIVE = 1
	DP = 2
	ILP = 3


def lrs(s, algo=Solver.AUTO, verbosity=0):
	'''
	Main method. Call with a regular python string or a list.
	'''

	r = string_to_run(s)

	if algo == Solver.AUTO:
		solver = lrs_auto
	elif algo == Solver.NAIVE:
		solver = lrs_branch_and_bound
	elif algo == Solver.DP:
		solver = lrs_dp
	elif algo == Solver.ILP:
		solver = lrs_ilp
	else:
		raise ValueError("LRS received an unexpected algorithm type: {}".format(algo))
	sol = reduce_and_solve(r, solver, verbosity)
	result = subsequence_to_indices(sub=sol.subsequences[0], ref=r)
		
	return result
