"""
Tests for BWT and FM-index operations.

Tests BWT construction, C-table, Occ table, and FM search. Also tests
equivalence between SA search and FM search.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.sa import build_suffix_array
from src.sa_search import find_all as sa_find_all
from src.bwt import (
    build_bwt,
    build_c_table,
    build_occ_table,
    fm_search,
    fm_find_all
)


def test_bwt_construction():
    """Test BWT construction from suffix array."""
    text = "banana$"
    sa = build_suffix_array(text)
    bwt = build_bwt(text, sa)
    
    # Expected BWT for banana$
    # SA positions: [6, 5, 3, 1, 0, 4, 2]
    # Characters before each suffix:
    # Before position 6 ($): a (text[5])
    # Before position 5 (a$): n (text[4])
    # Before position 3 (ana$): n (text[2])
    # Before position 1 (anana$): b (text[0])
    # Before position 0 (banana$): $ (text[6])
    # Before position 4 (na$): a (text[3])
    # Before position 2 (nana$): a (text[1])
    expected = "annb$aa"
    assert bwt == expected, f"Expected BWT '{expected}', got '{bwt}'"
    
    # Test with mississippi
    text = "mississippi$"
    sa = build_suffix_array(text)
    bwt = build_bwt(text, sa)
    assert len(bwt) == len(text)
    assert sorted(bwt) == sorted(text)  # BWT is a permutation
    
    print("✓ BWT construction tests passed")


def test_c_table():
    """Test C-table construction."""
    bwt = "annb$aa"
    c_table = build_c_table(bwt)
    
    # Characters in sorted order: $, a, b, n
    # Counts: $ = 1, a = 3, b = 1, n = 2
    # C-table: $ -> 0, a -> 1, b -> 4, n -> 5
    assert c_table['$'] == 0
    assert c_table['a'] == 1
    assert c_table['b'] == 4
    assert c_table['n'] == 5
    
    print("✓ C-table tests passed")


def test_occ_table():
    """Test Occ table construction."""
    bwt = "annb$aa"
    occ = build_occ_table(bwt)
    
    # Check that all characters are in the table
    assert set(occ.keys()) == set(bwt)
    
    # Check length of each list (should be len(bwt) + 1)
    for c in occ:
        assert len(occ[c]) == len(bwt) + 1
    
    # Check specific values
    # bwt = "annb$aa"
    # For 'a': [0, 1, 1, 1, 1, 1, 2, 3]
    assert occ['a'][0] == 0
    assert occ['a'][1] == 1  # One 'a' in bwt[0:1]
    assert occ['a'][7] == 3  # Three 'a's in bwt[0:7]
    
    # For 'n': [0, 0, 1, 2, 2, 2, 2, 2]
    assert occ['n'][0] == 0
    assert occ['n'][2] == 1  # One 'n' in bwt[0:2]
    assert occ['n'][3] == 2  # Two 'n's in bwt[0:3]
    
    print("✓ Occ table tests passed")


def test_fm_search_basic():
    """Test FM search with basic examples."""
    text = "banana$"
    sa = build_suffix_array(text)
    bwt = build_bwt(text, sa)
    c_table = build_c_table(bwt)
    occ = build_occ_table(bwt)
    
    # Search for "ana"
    top, bottom = fm_search("ana", bwt, c_table, occ)
    assert top <= bottom, "Pattern 'ana' should be found"
    count = bottom - top + 1
    assert count == 2, f"Expected 2 occurrences of 'ana', got {count}"
    
    # Search for "ban"
    top, bottom = fm_search("ban", bwt, c_table, occ)
    assert top <= bottom, "Pattern 'ban' should be found"
    count = bottom - top + 1
    assert count == 1, f"Expected 1 occurrence of 'ban', got {count}"
    
    # Search for non-existent pattern
    top, bottom = fm_search("xyz", bwt, c_table, occ)
    assert top > bottom, "Pattern 'xyz' should not be found"
    
    print("✓ FM search basic tests passed")


def test_fm_vs_sa_equivalence():
    """Test that FM search gives the same results as SA search."""
    test_cases = [
        ("banana$", ["ana", "na", "ban", "a", "banana", "xyz"]),
        ("mississippi$", ["issi", "ss", "i", "ssi", "miss", "xyz"]),
        ("abracadabra$", ["abra", "bra", "a", "cadabra", "xyz"]),
    ]
    
    for text, patterns in test_cases:
        sa = build_suffix_array(text)
        bwt = build_bwt(text, sa)
        c_table = build_c_table(bwt)
        occ = build_occ_table(bwt)
        
        for pattern in patterns:
            # Get results from SA search
            sa_results = sa_find_all(text, sa, pattern)
            
            # Get results from FM search
            fm_results = fm_find_all(pattern, text, sa, bwt, c_table, occ)
            
            # They should be identical
            assert sa_results == fm_results, \
                f"Mismatch for pattern '{pattern}' in '{text}': SA={sa_results}, FM={fm_results}"
    
    print("✓ FM vs SA equivalence tests passed")


def test_fm_comprehensive():
    """Comprehensive test of FM-index operations."""
    text = "thequickbrownfoxjumpsoverthelazydog$"
    sa = build_suffix_array(text)
    bwt = build_bwt(text, sa)
    c_table = build_c_table(bwt)
    occ = build_occ_table(bwt)
    
    patterns = ["the", "fox", "lazy", "jump", "o", "xyz", "quick"]
    
    for pattern in patterns:
        sa_results = sa_find_all(text, sa, pattern)
        fm_results = fm_find_all(pattern, text, sa, bwt, c_table, occ)
        assert sa_results == fm_results, \
            f"Mismatch for pattern '{pattern}': SA={sa_results}, FM={fm_results}"
    
    print("✓ Comprehensive FM tests passed")


def test_edge_cases():
    """Test edge cases for BWT and FM operations."""
    # Single character
    text = "$"
    sa = build_suffix_array(text)
    bwt = build_bwt(text, sa)
    assert bwt == "$"
    
    # Two characters
    text = "a$"
    sa = build_suffix_array(text)
    bwt = build_bwt(text, sa)
    c_table = build_c_table(bwt)
    occ = build_occ_table(bwt)
    
    fm_results = fm_find_all("a", text, sa, bwt, c_table, occ)
    sa_results = sa_find_all(text, sa, "a")
    assert fm_results == sa_results
    
    print("✓ Edge cases tests passed")


if __name__ == "__main__":
    test_bwt_construction()
    test_c_table()
    test_occ_table()
    test_fm_search_basic()
    test_fm_vs_sa_equivalence()
    test_fm_comprehensive()
    test_edge_cases()
    print("\n✅ All BWT and FM-index tests passed!")
