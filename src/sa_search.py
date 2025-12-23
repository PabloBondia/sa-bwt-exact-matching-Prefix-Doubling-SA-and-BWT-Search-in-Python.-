"""
Binary search operations on suffix arrays for exact pattern matching.

This module provides efficient search operations on suffix arrays including
lower bound, upper bound, and finding all occurrences of a pattern.
"""


def lower_bound(text, sa, pattern):
    """
    Find the leftmost position in SA where pattern could be inserted.
    
    Uses binary search to find the first suffix that is >= pattern.
    
    Args:
        text (str): The original text.
        sa (list): Suffix array of text.
        pattern (str): Pattern to search for.
    
    Returns:
        int: Index in suffix array of the first suffix >= pattern.
    """
    left, right = 0, len(sa)
    
    while left < right:
        mid = (left + right) // 2
        suffix = text[sa[mid]:]
        
        # Compare suffix with pattern
        if suffix < pattern:
            left = mid + 1
        else:
            right = mid
    
    return left


def upper_bound(text, sa, pattern):
    """
    Find the rightmost position in SA where pattern could be inserted.
    
    Uses binary search to find the first suffix that is > pattern.
    
    Args:
        text (str): The original text.
        sa (list): Suffix array of text.
        pattern (str): Pattern to search for.
    
    Returns:
        int: Index in suffix array of the first suffix > pattern.
    """
    left, right = 0, len(sa)
    
    while left < right:
        mid = (left + right) // 2
        suffix = text[sa[mid]:]
        
        # Compare suffix with pattern (checking if suffix starts with pattern)
        # We need suffix > pattern, which means:
        # - suffix doesn't start with pattern, OR
        # - suffix == pattern (and we want the upper bound)
        if suffix[:len(pattern)] <= pattern:
            left = mid + 1
        else:
            right = mid
    
    return left


def find_all(text, sa, pattern):
    """
    Find all occurrences of pattern in text using the suffix array.
    
    Uses binary search to find the range of suffixes that start with the pattern,
    then returns all corresponding positions.
    
    Args:
        text (str): The original text.
        sa (list): Suffix array of text.
        pattern (str): Pattern to search for.
    
    Returns:
        list: Sorted list of starting positions where pattern occurs in text.
              Returns empty list if pattern is not found.
    
    Example:
        >>> text = "banana$"
        >>> sa = build_suffix_array(text)
        >>> find_all(text, sa, "ana")
        [1, 3]
    """
    # Find the range in SA where all suffixes start with pattern
    left = lower_bound(text, sa, pattern)
    right = upper_bound(text, sa, pattern)
    
    # Extract positions from SA
    positions = [sa[i] for i in range(left, right)]
    
    # Verify that these suffixes actually start with the pattern
    # (Important when pattern might not exist in text)
    valid_positions = []
    for pos in positions:
        if text[pos:pos + len(pattern)] == pattern:
            valid_positions.append(pos)
    
    return sorted(valid_positions)
