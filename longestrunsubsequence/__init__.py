#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Computes the longest subsequence of a string/sequence, such that
only one run per character is contained. Implemented as described
in "The Longest Subsequence Run Problem".
"""

__author__ = 'Sven Schrinner, Manish Goel, Michael Wulfert, Philipp Spohr, Korbinian Schneeberger, Gunnar W. Klau'
__credits__ = ['Sven Schrinner', 'Manish Goel', 'Michael Wulfert', 'Philipp Spohr', 'Korbinian Schneeberger', 'Gunnar W. Klau']
__license__ = 'MIT'
__copyright__ = 'Copyright (C) 2021 by AlBi-HHU (gunnar.klau@hhu.de),  all rights reserved, MIT license.'
__email__ = 'gunnar.klau@hhu.de'
# __revision__ = ''
# __date__ = ''
# __version__ = ''
# __maintainer__ = ''
# __status__ = ''

from .lrs import lrs, Solver

__all__ = ['lrs', 'Solver']