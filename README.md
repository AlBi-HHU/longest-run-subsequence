## Reproducing publication results

The results from the publication "The Longest Run Subsequence" can be reproduced via Snakemake. For this, a Snakemake installation is required, as well as Python and PuLP (https://github.com/coin-or/pulp). Once all dependencies are resolved, the pipeline can be started with

snakemake all

This creates a file with random strings in the "instances"-folder and the resulting runtime in "results"-folder. A random seed for the instance generated is used and specified in the snakefile. The initial configuration produces results for the string length scaling, while there is a second coniguration (commented out in the snakefile) for the alphabet size scaling. The single results can be collected in a file "aggregated.csv" by running

python3 aggregate.py

## Running LRS on the command line

LRS can be called from the command line for test purposes. The command has to look like this:

python3 lrs.py <input> [naive|dp|ilp|dp2|ilp2]

The input can either be an arbitrary string or a list, which starts with "[", ends with "]" and separates elements with ",". The last parameter is the algorithm to use. dp2 and ilp2 are alternative implementations to the used dp and ilp algorithms used for the publication results.

## Using LRS in an implementation

There is currently no dedicated python package available. The main algorithm can, however, be used by importing the `lrs` function from "lrs.py". Dependencies are this file itself and all files in the "src"-folder.
