from collections import defaultdict, namedtuple
from itertools import product

from .util import Run, Solution, string_to_run, run_to_string


def reduce_and_solve(s, solver, verbosity=0):
	'''
	Input: A Run object, that does not contain $ as a character
	Output: A solution object
	'''
	
	if verbosity >= 1:
		print("Solving instance: {} ({} runs, {} characters)".format(run_to_string(s), len(s), len(set([run.char for run in s]))))
	
	return reduce_concat(s, solver, verbosity)


def solve_instance(s, solver, verbosity=0):
	if verbosity >= 1 and len(s) > 1:
		print("Solving sub-instance: {} ({} runs, {} characters)".format(run_to_string(s), len(s), len(set([run.char for run in s]))))
	return solver(s, verbosity=verbosity)


def get_first_and_last_occurences(s):
	'''
	Returns two dictionaries, which for each character in s contain the first and last run index (respectively) of its occurences
	'''
	first_occ = dict()
	last_occ = dict()	
	for i, run in enumerate(s):
		if run.char not in first_occ:
			first_occ[run.char] = i
			last_occ[run.char] = i
		last_occ[run.char] = i
	return first_occ, last_occ


def reduce_concat(s, solver, verbosity=0):
	'''
	Input: List of Runs
	Output: Solution
	'''
	sigma = list(set([run.char for run in s]))
	intervals = []
	partial_solutions = []
	
	# find first and last occurence for each character
	first_occ, last_occ = get_first_and_last_occurences(s)
	
	# take first run and extend it to the left, until a secluded prefix is found
	pos = 0
	current_end = 0
	while pos < len(s):
		# invariant: all positions before current_end (exclusive) have been processed
		current_start = current_end
		current_end = last_occ[s[current_start].char]+1
		pos = current_start+1
		while pos < current_end:
			# invariant: all runs before pos (exclusive) have been used to extend the interval
			current_end = max(current_end, last_occ[s[pos].char]+1)
			pos += 1
	
		# use nested reduction rule on complete interval
		intervals.append((current_start, current_end))
		partial_solutions.append(reduce_nested(s[current_start:current_end], solver, verbosity))
		
	# concatenate solutions
	size = sum([sol.size for sol in partial_solutions])
	partial_subs = [sol.subsequences for sol in partial_solutions]
	subsequences = []
	for comb in product(*partial_subs):
		subsequences.append([subseq for sublist in comb for subseq in sublist])
		
	return Solution(size, subsequences)

	
def reduce_nested(s, solver, verbosity=0):
	'''
	Input: List of Runs
	Output: Solution
	'''
	sigma = list(set([run.char for run in s]))
	
	# find first and last occurence for each character
	first_occ, last_occ = get_first_and_last_occurences(s)
	
	checked_chars = set()
	independent = []

	# idea: check for each character, whether it is part of a nested interval
	# 1. start with the characters borders as candidate interval
	# 2. for every other character inside the current interval, extend the borders
	# 3. proceed, until interval contains all occurences of any character inside
	
	# process wider spread chars first to avoid "nested" independent intervals
	sigma.sort(key=lambda char: last_occ[char] - first_occ[char], reverse=True)
	
	for char in sigma:
		if char in checked_chars:
			continue
		
		# initialize the candidate interval with first and last occurence of examined char
		left_bound = first_occ[char]
		right_bound = last_occ[char]+1 # right_bound is exclusive
		chars_in_interval = set([char])
		
		# these pointers indicate up to which position (from left_bound) we already read
		left = left_bound - 1
		right = left_bound + 1
		
		# if both pointers reached the bounds, the interval is closed
		# the borders itself must be characters we have already seen, so no check
		while left > left_bound or right < right_bound - 1:
			if right < right_bound - 1:
				c = s[right].char
				chars_in_interval.add(c)
				left_bound = min(left_bound, first_occ[c])
				right_bound = max(right_bound, last_occ[c]+1)
				right += 1
			else:
				c = s[left].char
				chars_in_interval.add(c)
				left_bound = min(left_bound, first_occ[c])
				right_bound = max(right_bound, last_occ[c]+1)
				left -= 1
				
		# only create sub instance, if it is not the entire string
		if left_bound > 0 or right_bound < len(s):
			independent.append((left_bound, right_bound))
			checked_chars.update(chars_in_interval)
			
	# if no intervals found, solve entire string
	if len(independent) == 0:
		return solve_instance(s, solver, verbosity)
			
	# sort independent intervals by position (they cannot overlap, so left bound is sufficient)
	independent.sort(key=lambda interval: interval[0])
	
	# contract adjacent independent intervals and run concat-rule on them again, if longer than one block
	# save the solution and the bounds for every sub-instance solved
	partial_solutions = []
	intervals = []
	left = independent[0][0]
	right = independent[0][0]
	for interval in independent:
		if interval[0] == right:
			# interval extends current sub-instance
			right = interval[1]
		else:
			# interval does not extend current sub-instance. solve latter (if not singleton block) and open new sub-instance
			if right - left >= 2:
				intervals.append((left, right))
				partial_solutions.append(reduce_concat(s[left:right], solver, verbosity))
			left = interval[0]
			right = interval[1]
			
	# solve unclosed sub instance (if not singleton block)
	if right - left >= 2:
		intervals.append((left, right))
		partial_solutions.append(reduce_concat(s[left:right], solver, verbosity))
		
	# again, if no sub-instance was solved, we have to solve the entire string as one instance
	if len(intervals) == 0:
		return solve_instance(s, solver, verbosity)
		
	# replace all sub-instance intervals with a single run of a new character. length = solution size of sub-instance
	s0 = []
	pos = 0
	for i in range(len(intervals)):
		s0 += s[pos:intervals[i][0]]
		s0.append(Run('$'+str(i), partial_solutions[i].size))
		pos = intervals[i][1]
	s0 += s[pos:]
	
	# solve modified instance
	sol = solve_instance(s0, solver, verbosity)
	
	# for every solution in modified instance: replace any run of $-chars with all solutions of the respective sub-instance
	final_subseqs = []
	for seq in sol.subsequences:
		# start with just the solution of the outer problem
		expanded_solutions = [seq]
		for i in range(len(intervals)):
			# replace the placeholder block for every solution in expanded_solutions with every sub-instance solution
			expanded_expanded_solutions = []
			for expanded_solution in expanded_solutions:
				# find index of placeholder block if existent
				idx = -1
				for j, run in enumerate(expanded_solution):
					if run.char == '$'+str(i):
						idx = j
						break
				if idx >= 0:
					for subsol in partial_solutions[i].subsequences:
						expanded_expanded_solutions.append(expanded_solution[:idx]+subsol+expanded_solution[idx+1:])
				else:
					expanded_expanded_solutions.append(expanded_solution)
			
			# continue next iteration with the now extended solutions
			expanded_solutions = expanded_expanded_solutions
		final_subseqs += expanded_solutions
	#print("final_subseqs: {}".format(final_subseqs))

	return Solution(sol.size, final_subseqs)