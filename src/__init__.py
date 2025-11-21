"""
Suffix Array and BWT/FM-index library for exact pattern matching.
"""

from .sa import build_suffix_array
from .sa_search import lower_bound, upper_bound, find_all
from .bwt import (
    build_bwt,
    build_c_table,
    build_occ_table,
    fm_search,
    fm_find_all
)

__all__ = [
    'build_suffix_array',
    'lower_bound',
    'upper_bound',
    'find_all',
    'build_bwt',
    'build_c_table',
    'build_occ_table',
    'fm_search',
    'fm_find_all',
]
