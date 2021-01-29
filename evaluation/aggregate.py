import os

def collect_results():
	dir = "./results"
	out = "./aggregate.csv"
	with open(out, 'w') as all_results:
		for filename in sorted(os.listdir(dir)):
			with open(dir+'/'+filename, 'r') as partial_result:
				lines = [line for line in partial_result.readlines()]
			for line in lines:
				all_results.write(line)
				all_results.write('\n')
				
if __name__ == "__main__":
	collect_results()