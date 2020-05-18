# config for string length scaling
LENGTHS = list(range(20, 41, 10))
ALPHABET_SIZES = [6, 10, 16]
# config for alphabet size scaling
#LENGTHS = list(range(20, 81, 20))
#ALPHABET_SIZES = list(range(6, 25, 2))

ALGORITHMS = ["dp", "ilp"]
RUNS = 20
SEED = 11111

rule all:
	input:
		expand("results/result_{algo}_{length}_{alpha}", algo=ALGORITHMS, length=LENGTHS, alpha=ALPHABET_SIZES)
		
rule evaluate:
	input:
		"instances/gen_{length}_{alpha}"
	output:
		"results/result_{algo}_{length}_{alpha}"
	shell:
		"python3 eval.py {input} {output} {wildcards.algo}"
		
rule generate:
	output:
		"instances/gen_{length}_{alpha}"
	shell:
		"python3 generator.py {output} {RUNS} {wildcards.length} {wildcards.alpha} {SEED}"