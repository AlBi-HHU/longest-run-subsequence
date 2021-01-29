from collections import defaultdict
from .util import Run, Solution

'''
###############################
ALGO-PICKER
###############################
'''

def lrs_auto(s, verbosity=0):
	if len(s) == 1:
		return Solution(1, [[s[0]]])
	
	sigma = list(set([run.char for run in s]))
	
	# if alphabet size is too large, use ILP instead of DP
	if (len(sigma)-13)*10 > len(s):
		try:
			from pulp import LpProblem
			if verbosity >= 1:
				print(" ... using ILP (expected to be faster).")
			return lrs_ilp(s, verbosity)
		except ModuleNotFoundError:
			if verbosity >= 1:
				print(" ... using DP (PuLP not found).")
			return lrs_dp(s)
	else:
		if verbosity >= 1:
			print(" ... using DP (expected to be faster).")
		return lrs_dp(s)

'''
###############################
ILP MODEL
###############################
'''

def lrs_ilp(s, verbosity=0):
	try:
		try:
			from pulp import LpVariable, LpProblem, LpMaximize, LpInteger, PulpSolverError

			model = LpProblem("LRS", LpMaximize)

			# create variables
			x = [LpVariable("x_{}".format(i), 0, 1, LpInteger) for i in range(len(s))]

			# node degree
			for j in range(len(s)):
				for i in range(j):
					if s[i].char == s[j].char:
						model += (j-i)*x[i] + sum([x[l] if s[l].char != s[i].char else 0 for l in range(i+1,j)]) + (j-i)*x[j] <= 2*(j-i)

			# objective
			model += sum([x[i]*s[i].length for i in range(len(s))])

			# depending on pulp version, the solvers have to be created differently
			try:
				from pulp import getSolver, listSolvers
				solvers = [getSolver(s, msg=0) for s in listSolvers()]
			except:
				from pulp import COIN_CMD, PULP_CBC_CMD, PulpSolverError
				solvers = [COIN_CMD(msg=0), PULP_CBC_CMD(msg=0)]

			solved = False
			for solver in solvers:
				if solved:
					break
				try:
					model.solve(solver)
					solved = True
				except PulpSolverError:
					pass

			if not solved:
				raise ImportError

			sol = [s[i] for i in range(len(s)) if x[i].varValue > 0.999]

			return Solution(sum([run.length for run in sol]), [sol])
		except (ModuleNotFoundError, ImportError) as e:
			if verbosity == 1:
				print("PuLP itself or some of its properties could not be loaded. Solving model with DP instead.")
			elif verbosity >= 2:
				print("Error loading PuLP solver:")
				print(e)
				print("Solving model with DP instead.")
			return lrs_dp(s)
	except:
		if verbosity >= 1:
			print("Unexpected error occured while loading PuLP. Solving model with DP instead.")
		return lrs_dp(s)

'''
###############################
DP ALGORITHM
###############################
'''

def char_in_subalphabet(f, c_idx):
	return f & (1 << c_idx) > 0


def add_char_to_subalphabet(f, c_idx):
	return f | (1 << c_idx)


def remove_char_from_subalphabet(f, c_idx):
	return f - ((f >> c_idx) % 2) * (1 << c_idx)


def popcount(f):
	cnt = 0
	while f > 0:
		cnt += f % 2
		f = f // 2
	return cnt


def lrs_dp(s, verbosity=0):
	# create alphabet with reverse index
	sigma = list(set([run.char for run in s]))
	char_idx = dict()
	for i, char in enumerate(sigma):
		char_idx[char] = i
		
	# compute predecessor for each char and for each run
	pred = [[0 for _ in sigma] for i in range(len(s)+1)]
	for pos in range(1, len(s)+1):
		for prev in range(pos-1, 0, -1):
			pred[pos][char_idx[s[prev-1].char]] = max(pred[pos][char_idx[s[prev-1].char]], prev)
	
	# initialize dp table (and backtracking table)
	D = [defaultdict(lambda : -float("inf")) for _ in range(len(s)+1)]
	B = [defaultdict(lambda : -1) for _ in range(len(s)+1)]
	D[0][0] = 0
	B[0][0] = -1
	# 0 is basically the empty sub-alphabet, considering that a subset from a finite superset can be represented as bit string
	
	max_entry = (0, 0)
	max_sol = 0
	
	# iterate column-wise
	for col in range(1, len(s)+1):
		
		# iterate over all characters
		c_idx_s = char_idx[s[col-1].char]
		last_occ = pred[col][c_idx_s]
		for char in sigma:
			c_idx = char_idx[char]
			pr = pred[col][c_idx]
			
			assert pr < col
			
			# case 0: predecessor is further back than last occurence of character at the current position -> skip
			if pr < last_occ:
				continue

			# case 1: char is same character as in current column -> extend previous solutions
			if c_idx == c_idx_s and pr > 0:
				for subalphabet in D[pr]:
					pr_val = D[pr][subalphabet]
					if pr_val + s[col-1].length > D[col][subalphabet]:
						D[col][subalphabet] = pr_val + s[col-1].length
						B[col][subalphabet] = pr
			
			# case 2: char is another character -> extend only solutions, which did not contain char yet
			else:
				for subalphabet in D[pr]:
					if not char_in_subalphabet(subalphabet, c_idx_s):
						pr_val = D[pr][subalphabet]
						new_subalphabet = add_char_to_subalphabet(subalphabet, c_idx_s)
						if pr_val + s[col-1].length > D[col][new_subalphabet]:
							D[col][new_subalphabet] = pr_val + s[col-1].length
							B[col][new_subalphabet] = pr
				
		if last_occ > 0:
			D[last_occ].clear()
	
		# register new best solution
		for subalphabet in sorted(D[col]):
			if D[col][subalphabet] > max_sol:
				max_sol = D[col][subalphabet]
				max_entry = (col, subalphabet)
			
	# backtracking
	sol = []
	while max_entry[0] > 0:
		sol.append(s[max_entry[0]-1])
		
		cur_col = max_entry[0]
		cur_char = char_idx[s[cur_col-1].char]
		next_col = B[max_entry[0]][max_entry[1]]
		next_char = char_idx[s[next_col-1].char]
		
		next_sub = max_entry[1] if cur_char == next_char else remove_char_from_subalphabet(max_entry[1], cur_char)
		max_entry = (next_col, next_sub)
		
	sol = sol[::-1]
	
	return Solution(sum([run.length for run in sol]), [sol])

'''
###############################
NAIVE BRANCH AND BOUND
###############################
'''

def lrs_branch_and_bound(s, verbosity=0):
	'''
	Naive branching algorithm to check solutions
	'''
	return naive_branch_single_rec(s, 0, None, set(), 0)


def naive_branch_single_rec(s, pos, char, used, score):
	'''
	s: The complete input string (= list of runs)
	pos: The position to process now
	char: The currently selected character (or None, if no char has been selected yet)
	used: List of already used characters
	'''
	if pos >= len(s):
		# if end is reached: create solution with final score and empty sequence (will be filled via backtracking)
		return Solution(score, [[]])
	elif s[pos].char == char:
		# if char of current run is active, it is always optimal to extend this solution
		sol = naive_branch_single_rec(s, pos+1, char, used, score + s[pos].length)
		return Solution(sol.size, [[s[pos]]+sol.subsequences[0]])
	elif s[pos].char in used:
		# if char of current run is not active and was used before, it must be skipped
		return naive_branch_single_rec(s, pos+1, char, used, score)
	else:
		# if char of current run is not active but could become active, we branch
		sol1 = naive_branch_single_rec(s, pos+1, char, used, score)
		used.add(s[pos].char)
		sol2 = naive_branch_single_rec(s, pos+1, s[pos].char, used, score + s[pos].length)
		used.remove(s[pos].char)
		if sol1.size > sol2.size:
			return sol1
		else:
			return Solution(sol2.size, [[s[pos]]+sol2.subsequences[0]])