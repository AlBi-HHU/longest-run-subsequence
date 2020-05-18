import random
import sys
import os


def generate_random_string(length, alphabet):
	gen = alphabet[:]
	for i in range(len(alphabet), length):
		gen.append(alphabet[random.randint(0, len(alphabet)-1)])
		
	random.shuffle(gen)
	return "".join(gen)


def main(argv):
	if len(argv) < 5 or len(argv) > 6:
		print("Error: Incorrect number of arguments. Please use format: generator <path> <num-strings> <length> <alphabet-size> [<random-seed>]")
		return
	path = argv[1]
	random.seed(a=argv[5] if len(argv) == 6 else None, version=2)
	alphabet = [chr(c) for c in range(65, 65+int(argv[4]))]
	
	with open(path, 'w') as file:
		for i in range(int(argv[2])):
			s = generate_random_string(int(argv[3]), alphabet)
			file.write(s)
			file.write('\n')


if __name__ == "__main__":
	main(sys.argv)