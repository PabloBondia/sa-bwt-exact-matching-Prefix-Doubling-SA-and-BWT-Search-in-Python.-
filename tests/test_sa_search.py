"""
Tests for suffix array search operations.

Tests binary search functions against naive linear search.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.sa import build_suffix_array
from src.sa_search import lower_bound, upper_bound, find_all


def naive_find_all(text, pattern):
    """
    Naive pattern matching by checking every position.
    Used as an oracle for testing.
    
    Args:
        text (str): The text to search in.
        pattern (str): Pattern to search for.
    
    Returns:
        list: Sorted list of positions where pattern occurs.
    """
    positions = []
    for i in range(len(text) - len(pattern) + 1):
        if text[i:i + len(pattern)] == pattern:
            positions.append(i)
    return positions


def test_find_all_basic():
    """Test find_all with basic examples."""
    text = "banana$"
    sa = build_suffix_array(text)
    
    # Test finding "ana"
    result = find_all(text, sa, "ana")
    expected = naive_find_all(text, "ana")
    assert result == expected, f"Expected {expected}, got {result}"
    assert result == [1, 3]
    
    # Test finding "na"
    result = find_all(text, sa, "na")
    expected = naive_find_all(text, "na")
    assert result == expected
    assert result == [2, 4]
    
    # Test finding "ban"
    result = find_all(text, sa, "ban")
    expected = naive_find_all(text, "ban")
    assert result == expected
    assert result == [0]
    
    # Test non-existent pattern
    result = find_all(text, sa, "xyz")
    expected = naive_find_all(text, "xyz")
    assert result == expected
    assert result == []
    
    print("✓ Basic find_all tests passed")


def test_find_all_mississippi():
    """Test with mississippi example."""
    text = "mississippi$"
    sa = build_suffix_array(text)
    
    # Test finding "issi"
    result = find_all(text, sa, "issi")
    expected = naive_find_all(text, "issi")
    assert result == expected
    assert result == [1, 4]
    
    # Test finding "ss"
    result = find_all(text, sa, "ss")
    expected = naive_find_all(text, "ss")
    assert result == expected
    assert result == [2, 5]
    
    # Test finding "i"
    result = find_all(text, sa, "i")
    expected = naive_find_all(text, "i")
    assert result == expected
    assert sorted(result) == [1, 4, 7, 10]
    
    print("✓ Mississippi tests passed")


def test_find_all_comprehensive():
    """Test find_all with various patterns and texts."""
    test_cases = [
        ("abracadabra$", "abra", [0, 7]),
        ("abracadabra$", "bra", [1, 8]),
        ("abracadabra$", "a", [0, 3, 5, 7, 10]),
        ("thequickbrownfox$", "the", [0]),
        ("thequickbrownfox$", "o", [10, 14]),
        ("aaaaaa$", "aa", [0, 1, 2, 3, 4]),
        ("aaaaaa$", "aaa", [0, 1, 2, 3]),
    ]
    
    for text, pattern, expected in test_cases:
        sa = build_suffix_array(text)
        result = find_all(text, sa, pattern)
        naive_result = naive_find_all(text, pattern)
        assert result == naive_result, f"Failed for text={text}, pattern={pattern}"
        assert result == expected, f"Expected {expected}, got {result} for pattern '{pattern}' in '{text}'"
    
    print("✓ Comprehensive find_all tests passed")


def test_bounds():
    """Test lower_bound and upper_bound functions."""
    text = "banana$"
    sa = build_suffix_array(text)
    
    # The sorted suffixes are:
    # 0: $ (sa[0] = 6)
    # 1: a$ (sa[1] = 5)
    # 2: ana$ (sa[2] = 3)
    # 3: anana$ (sa[3] = 1)
    # 4: banana$ (sa[4] = 0)
    # 5: na$ (sa[5] = 4)
    # 6: nana$ (sa[6] = 2)
    
    # Test bounds for "ana"
    lb = lower_bound(text, sa, "ana")
    ub = upper_bound(text, sa, "ana")
    # "ana$" and "anana$" start with "ana", so they should be at indices 2 and 3
    assert lb == 2, f"Lower bound for 'ana' should be 2, got {lb}"
    assert ub == 4, f"Upper bound for 'ana' should be 4, got {ub}"
    
    print("✓ Bounds tests passed")


def test_edge_cases():
    """Test edge cases."""
    text = "a$"
    sa = build_suffix_array(text)
    
    # Pattern not in text
    result = find_all(text, sa, "b")
    assert result == []
    
    # Pattern longer than text
    result = find_all(text, sa, "abc")
    assert result == []
    
    # Empty pattern (should return all positions or empty)
    result = find_all(text, sa, "")
    # Empty pattern matches everywhere, but we may choose to return empty
    # This is implementation-dependent
    
    # Single character text
    text = "$"
    sa = build_suffix_array(text)
    result = find_all(text, sa, "$")
    assert result == [0]
    
    print("✓ Edge cases tests passed")


if __name__ == "__main__":
    test_find_all_basic()
    test_find_all_mississippi()
    test_find_all_comprehensive()
    test_bounds()
    test_edge_cases()
    print("\n✅ All search tests passed!")
