from collections import defaultdict
from src.util import Run, Solution

'''
###############################
ILP MODEL
###############################
'''

def lrs_ilp(s):
	from pulp import LpVariable, LpProblem, LpMaximize, LpInteger
	
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
	
	model.solve()
	
	sol = [s[i] for i in range(len(s)) if x[i].varValue > 0.999]
	
	return Solution(sum([run.length for run in sol]), [sol])

'''
###############################
DP ALGORITHM
###############################
'''

def char_in_subalphabet(f, c_idx):
	t = 2**c_idx
	return (f % (2*t)) >= t


def add_char_to_subalphabet(f, c_idx):
	t = 2**c_idx
	if (f % (2*t)) >= t:
		return f
	else:
		return f + t
	
	
def subalphabet_to_chars(f, sigma):
	return [sigma[i] for i in range(len(sigma)) if char_in_subalphabet(f, i)]


def lrs_dp(s):
	# create alphabet with reverse index
	sigma = sorted(list(set([run.char for run in s])))
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
	B = [defaultdict(lambda : -float("inf")) for _ in range(len(s)+1)]
	D[0][0] = 0
	B[0][0] = (-1, 0)
	
	max_entry = (0, 0)
	max_sol = 0
	
	# iterate column-wise
	for col in range(1, len(s)+1):
		
		# iterate over all characters
		for char in sigma:
			c_idx = char_idx[char]
			c_idx_s = char_idx[s[col-1].char]
			pr = pred[col][c_idx]
			
			# case 1: char is same character as is current column -> extend previous solutions
			if c_idx == c_idx_s and pr > 0:
				for subalphabet in D[pr]:
					if D[pr][subalphabet] + s[col-1].length > D[col][subalphabet]:
						D[col][subalphabet] = D[pr][subalphabet] + s[col-1].length
						B[col][subalphabet] = (pr, subalphabet)
			
			# case 2: char is another character -> extend only solutions, which did not contain char yet
			else:
				for subalphabet in D[pr]:
					if not char_in_subalphabet(subalphabet, c_idx_s):
						new_subalphabet = add_char_to_subalphabet(subalphabet, c_idx_s)
						if D[pr][subalphabet] + s[col-1].length > D[col][new_subalphabet]:
							D[col][new_subalphabet] = D[pr][subalphabet] + s[col-1].length
							B[col][new_subalphabet] = (pr, subalphabet)
	
		# register new best solution
		for subalphabet in sorted(D[col]):
			if D[col][subalphabet] > max_sol:
				max_sol = D[col][subalphabet]
				max_entry = (col, subalphabet)
			
	# backtracking
	sol = []
	while max_entry[0] > 0:
		sol.append(s[max_entry[0]-1])
		max_entry = B[max_entry[0]][max_entry[1]]
		
	sol = sol[::-1]
	
	return Solution(sum([run.length for run in sol]), [sol])

'''
###############################
NAIVE BRANCH AND BOUND
###############################
'''

def lrs_branch_and_bound(s):
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