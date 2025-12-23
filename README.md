# Suffix Array and BWT/FM-Index for Exact Pattern Matching

Efficient suffix array construction in Python via prefix-doubling, plus exact pattern matching with binary search and BWT/FM-index; includes correctness tests and runtime experiments.

## Overview

This repository provides a complete implementation of:

- **Suffix Array Construction** using the prefix-doubling algorithm (O(n log² n) with Python's Timsort)
- **Pattern Matching** via binary search on suffix arrays
- **Burrows-Wheeler Transform (BWT)** and **FM-Index** for compressed pattern matching
- Comprehensive test suite verifying correctness against naive oracles
- Performance benchmarks and analysis

## Features

### Algorithms Implemented

1. **Suffix Array (src/sa.py)**
   - Prefix-doubling construction: O(n log² n)
   - Space-efficient with rank-based sorting

2. **SA Search (src/sa_search.py)**
   - `lower_bound`: Find first occurrence in SA
   - `upper_bound`: Find last occurrence in SA
   - `find_all`: Return all pattern positions
   - Time complexity: O(m log n + k) where m=pattern length, k=occurrences

3. **BWT and FM-Index (src/bwt.py)**
   - BWT construction from SA: O(n)
   - C-table construction: O(n + σ) where σ=alphabet size
   - Occ table construction: O(σn)
   - FM backward search: O(m + k)

## Installation

```bash
# Clone the repository
git clone https://github.com/PabloBondia/sa-bwt-exact-matching-Prefix-Doubling-SA-and-BWT-Search-in-Python.-.git
cd sa-bwt-exact-matching-Prefix-Doubling-SA-and-BWT-Search-in-Python.-

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Basic Example

```python
from src.sa import build_suffix_array
from src.sa_search import find_all as sa_find_all
from src.bwt import build_bwt, build_c_table, build_occ_table, fm_find_all

# Prepare text (must end with sentinel '$')
text = "banana$"

# Build suffix array
sa = build_suffix_array(text)

# Search using suffix array
positions = sa_find_all(text, sa, "ana")
print(f"Pattern 'ana' found at positions: {positions}")
# Output: [1, 3]

# Build FM-index
bwt = build_bwt(text, sa)
c_table = build_c_table(bwt)
occ = build_occ_table(bwt)

# Search using FM-index
positions = fm_find_all("ana", text, sa, bwt, c_table, occ)
print(f"Pattern 'ana' found at positions: {positions}")
# Output: [1, 3]
```

### Running Tests

```bash
# Run all tests
python tests/test_sa.py
python tests/test_sa_search.py
python tests/test_bwt.py

# Or use pytest
pytest tests/
```

### Jupyter Notebook

Explore the interactive demo and performance experiments:

```bash
jupyter notebook notebooks/suffix_array_demo.ipynb
```

The notebook includes:
- Step-by-step explanations of algorithms
- Visual demonstrations
- Runtime experiments with 100-character patterns on 1M text
- Performance comparisons between SA and FM-index search

## Directory Structure

```
.
├── src/                    # Source code
│   ├── __init__.py        # Package initialization
│   ├── sa.py              # Suffix array construction
│   ├── sa_search.py       # Binary search on SA
│   └── bwt.py             # BWT and FM-index
├── tests/                  # Test suite
│   ├── test_sa.py         # SA tests vs naive oracle
│   ├── test_sa_search.py  # Search tests vs naive search
│   └── test_bwt.py        # BWT/FM tests and SA↔FM equivalence
├── notebooks/              # Jupyter notebooks
│   └── suffix_array_demo.ipynb  # Demo and experiments
├── data/                   # Data files (empty)
├── requirements.txt        # Python dependencies
├── .gitignore             # Git ignore rules
└── README.md              # This file
```

## Algorithm Details

### Prefix-Doubling Suffix Array Construction

The algorithm sorts suffixes by comparing increasingly longer prefixes:
1. Initialize ranks based on first character
2. In each iteration k, sort by (rank[i], rank[i+2^k]) pairs
3. Update ranks for next iteration
4. Double comparison length each time
5. Continue until all ranks are unique

**Time Complexity:** O(n log² n) - O(log n) iterations × O(n log n) sorting with Timsort

### FM-Index Backward Search

The FM-index uses the LF mapping property:
1. Start with full range [0, n-1]
2. Process pattern right-to-left
3. For each character c, update range using: `top = C[c] + Occ[c][top]` and `bottom = C[c] + Occ[c][bottom+1] - 1`
4. Final range gives all occurrences

**Time Complexity:** O(m + k) where m=pattern length, k=occurrences

## Performance

Experiments on 1M character text with 100-character patterns show:
- **FM-index search** is faster than SA binary search
- **Build time** (excluded from search timing): ~10-20 seconds for 1M text
- **Search time** (per query): Sub-millisecond for both methods
- **Memory**: FM-index uses O(σn) additional space for Occ table

See `notebooks/suffix_array_demo.ipynb` for detailed performance analysis.

## Testing

All implementations are tested against naive oracles:
- **SA construction**: Verified against naive suffix sorting
- **SA search**: Verified against linear pattern scanning
- **FM search**: Verified for equivalence with SA search
- **Random testing**: Multiple random strings to ensure robustness

## Requirements

- Python 3.7+
- NumPy (for experiments)
- Pytest (for testing)
- Jupyter (for notebooks)
- Matplotlib (for visualizations)

## License

MIT License

## References

1. Manber, U., & Myers, G. (1993). Suffix arrays: a new method for on-line string searches.
2. Burrows, M., & Wheeler, D. J. (1994). A block-sorting lossless data compression algorithm.
3. Ferragina, P., & Manzini, G. (2000). Opportunistic data structures with applications.
