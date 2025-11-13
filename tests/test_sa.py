"""
Tests for suffix array construction.

Tests the prefix-doubling algorithm against a naive oracle implementation.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.sa import build_suffix_array


def naive_suffix_array(text):
    """
    Naive suffix array construction by sorting all suffixes.
    Used as an oracle for testing.
    
    Args:
        text (str): Input text.
    
    Returns:
        list: Suffix array.
    """
    n = len(text)
    suffixes = [(text[i:], i) for i in range(n)]
    suffixes.sort()
    return [pos for _, pos in suffixes]


def test_simple_examples():
    """Test with simple, hand-verifiable examples."""
    # Test case 1: banana$
    text = "banana$"
    sa = build_suffix_array(text)
    expected = naive_suffix_array(text)
    assert sa == expected, f"Expected {expected}, got {sa}"
    
    # Verify the sorted order
    assert text[sa[0]:] == "$"
    assert text[sa[1]:] == "a$"
    assert text[sa[2]:] == "ana$"
    
    # Test case 2: mississippi$
    text = "mississippi$"
    sa = build_suffix_array(text)
    expected = naive_suffix_array(text)
    assert sa == expected, f"Expected {expected}, got {sa}"
    
    # Test case 3: Single character
    text = "$"
    sa = build_suffix_array(text)
    assert sa == [0]
    
    # Test case 4: Two characters
    text = "a$"
    sa = build_suffix_array(text)
    assert sa == [1, 0]
    
    print("✓ All simple examples passed")


def test_repeated_characters():
    """Test with strings containing repeated characters."""
    text = "aaaa$"
    sa = build_suffix_array(text)
    expected = naive_suffix_array(text)
    assert sa == expected
    
    text = "aaaaabbbbb$"
    sa = build_suffix_array(text)
    expected = naive_suffix_array(text)
    assert sa == expected
    
    print("✓ Repeated characters tests passed")


def test_random_strings():
    """Test with various random strings against naive oracle."""
    import random
    
    test_cases = [
        "abcdef$",
        "fedcba$",
        "abracadabra$",
        "thequickbrownfox$",
        "aabbccddee$",
        "xyxyxyxy$",
    ]
    
    for text in test_cases:
        sa = build_suffix_array(text)
        expected = naive_suffix_array(text)
        assert sa == expected, f"Failed for text: {text}"
    
    # Generate some random strings
    for _ in range(10):
        length = random.randint(5, 50)
        chars = [random.choice('abcdefgh') for _ in range(length)]
        text = ''.join(chars) + '$'
        
        sa = build_suffix_array(text)
        expected = naive_suffix_array(text)
        assert sa == expected, f"Failed for random text: {text}"
    
    print("✓ Random strings tests passed")


def test_longer_text():
    """Test with longer text."""
    # Create a longer text
    text = "the quick brown fox jumps over the lazy dog" * 10 + "$"
    sa = build_suffix_array(text)
    expected = naive_suffix_array(text)
    assert sa == expected
    
    print("✓ Longer text test passed")


if __name__ == "__main__":
    test_simple_examples()
    test_repeated_characters()
    test_random_strings()
    test_longer_text()
    print("\n✅ All suffix array tests passed!")
