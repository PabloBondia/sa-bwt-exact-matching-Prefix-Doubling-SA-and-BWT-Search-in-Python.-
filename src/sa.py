"""
Suffix Array Construction using Prefix Doubling Algorithm.

This module implements the prefix-doubling algorithm for constructing suffix arrays
in O(n log^2 n) time complexity using Python's Timsort for sorting.
"""


def build_suffix_array(text):
    """
    Build a suffix array using the prefix-doubling algorithm.
    
    The algorithm sorts suffixes by their first 2^k characters in each iteration,
    doubling k each time. Time complexity: O(n log^2 n) with Timsort.
    
    Args:
        text (str): Input text string. Should end with a sentinel character (e.g., '$')
                   that is lexicographically smaller than all other characters.
    
    Returns:
        list: Suffix array - a list of integers where sa[i] is the starting position
              of the i-th smallest suffix in lexicographic order.
    
    Example:
        >>> build_suffix_array("banana$")
        [6, 5, 3, 1, 0, 4, 2]
    """
    n = len(text)
    
    # Initialize suffix array with positions 0 to n-1
    sa = list(range(n))
    
    # rank[i] is the rank of suffix starting at position i
    # Initially, rank by first character
    rank = [ord(c) for c in text]
    
    # tmp will store the new ranks in each iteration
    tmp = [0] * n
    
    # k is the current comparison length (we compare first 2^k characters)
    k = 1
    
    while k < n:
        # Sort by (rank[i], rank[i+k]) pairs
        # Python's sort is stable and uses Timsort (O(n log n))
        sa.sort(key=lambda i: (rank[i], rank[i + k] if i + k < n else -1))
        
        # Compute new ranks based on sorted order
        tmp[sa[0]] = 0
        for i in range(1, n):
            # Same rank if both pairs are identical
            prev = sa[i - 1]
            curr = sa[i]
            prev_pair = (rank[prev], rank[prev + k] if prev + k < n else -1)
            curr_pair = (rank[curr], rank[curr + k] if curr + k < n else -1)
            
            if prev_pair == curr_pair:
                tmp[curr] = tmp[prev]
            else:
                tmp[curr] = tmp[prev] + 1
        
        # Update ranks for next iteration
        rank = tmp[:]
        
        # Double k for next iteration
        k *= 2
        
        # Early termination: if all ranks are unique, we're done
        if rank[sa[-1]] == n - 1:
            break
    
    return sa
