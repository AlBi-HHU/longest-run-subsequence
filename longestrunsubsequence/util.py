from collections import defaultdict, namedtuple


Run = namedtuple("Run", ["char", "length"])
Solution = namedtuple("Solution", ["size", "subsequences"])


def run_to_string(s):
	out = ""
	for run in s:
		if isinstance(run.char, str):
			out += run.char[0]*run.length
		else:
			out += str(run.char)[0]*run.length
	return out


def string_to_run(s):
	if len(s) == 0:
		return []
	runs = []
	char = s[0]
	length = 1
	for i in range(1, len(s)):
		if s[i] == char:
			length += 1
		else:
			runs.append(Run(char, length))
			char = s[i]
			length = 1
	runs.append(Run(char, length))
	return runs


def subsequence_to_indices(sub, ref):
	indices = get_selected_runs(sub, ref)
	char_indices = []
	char_pos = 0
	if indices is None:
		return None
	for i in range(len(ref)):
		if i in indices:
			char_indices += list(range(char_pos, char_pos+ref[i].length))
		char_pos += ref[i].length
	return char_indices


def get_selected_runs(sub, ref):
	'''
	Returns the positions in ref, which are covered by the subsequence sub.
	Returns None if sub is not a subsequence of ref
	'''
	indices = []
	sub_pos = 0
	for ref_pos in range(len(ref)):
		if sub_pos >= len(sub):
			break
		if ref[ref_pos] == sub[sub_pos]:
			indices.append(ref_pos)
			sub_pos += 1
	if sub_pos < len(sub):
		return None
	else:
		return indices