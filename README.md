# Longest Run Subsequence

Implementation of a solver for the Longest Run Subsequence Problem. Given a
sequence as input, compute a longest subsequence such that there is at most
one run for every character.

## Example

A longest run subsequence of the string `aababbbdccddd` is `aaabbbccddd`.

## Algorithms

Depending on the properties of an instance the solver uses one of two algorithms to solve the problem.
For long strings with small alphabets a dynamic
programming approach is used, while short strings with large alphabets are
solved via Integer Linear Programming. Every input instance is processed by
reduction rules first to split it into smaller instances, if possible. Details can be found in

REF WABI, then ALMOB paper

Please consider citing this paper if you find the implementation useful for your work.

## Installation

The Integer Linear Program algorithm is only available if PuLP is
installed on the system. PuLP is a free API for modelling linear programs
and available on PyPI or conda.

## Usage

To solve Longest Run Subsequence instances, the function ``lrs`` has to be
imported from the module.

Example code::

    from longestrunsubsequence import lrs
    print(lrs('aababbbdccddd'))
    > [0, 1, 3, 4, 5, 6, 8, 9, 10, 11, 12]

The output is a list of indices, which represent the elements of the longest
subsequence. The input can be a string or a list with arbitrary elements.

