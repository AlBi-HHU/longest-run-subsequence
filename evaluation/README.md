# Evaluation

This sub-folder contains the code, which was used in REF WABI to generate the synthetic instances, as well as running time and memory consumption for several combinations of string lengths and alphabet sizes as input.

## Creating and solving instances

The process of creating and solving the instances is done using the provided ``Snakefile``. The package ``snakemake`` is required to execute it. Once ``snakemake`` is installed, the script can be run with:

      snakemake all

It creates two subfolders ``instances`` and ``results``. Afterwards the python script ``aggregate.py`` can be run to summarize the results into a csv file.
