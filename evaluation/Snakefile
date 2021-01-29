# config for string length scaling
LENGTHS1 = list(range(20, 101, 10))
ALPHABET_SIZES1 = [6, 10, 16, 20]
# config for alphabet size scaling
LENGTHS2 = list(range(20, 81, 20))
ALPHABET_SIZES2 = list(range(6, 23, 2))

ALGORITHMS = ["dp", "ilp", "auto"]
RUNS = 20
SEED = 11111

rule all:
	input:
		expand("results/result_{algo}_{length}_{alpha}", algo=ALGORITHMS, length=LENGTHS1, alpha=ALPHABET_SIZES1),
		expand("results/result_{algo}_{length}_{alpha}", algo=ALGORITHMS, length=LENGTHS2, alpha=ALPHABET_SIZES2)
		
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