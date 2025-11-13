"""
Burrows-Wheeler Transform (BWT) and FM-index for exact pattern matching.

This module implements BWT construction from a suffix array, the C-table and
Occ table for FM-index, and backward search for pattern matching.
"""


def build_bwt(text, sa):
    """
    Build the Burrows-Wheeler Transform from a suffix array.
    
    BWT[i] is the character that precedes the suffix at position SA[i].
    
    Args:
        text (str): The original text (should end with sentinel '$').
        sa (list): Suffix array of text.
    
    Returns:
        str: The BWT string.
    
    Example:
        >>> text = "banana$"
        >>> sa = build_suffix_array(text)
        >>> build_bwt(text, sa)
        'annb$aa'
    """
    bwt = []
    for i in range(len(sa)):
        if sa[i] == 0:
            # The character before position 0 is the last character
            bwt.append(text[-1])
        else:
            bwt.append(text[sa[i] - 1])
    return ''.join(bwt)


def build_c_table(bwt):
    """
    Build the C-table for FM-index.
    
    C[c] = number of characters in BWT that are lexicographically smaller than c.
    Time complexity: O(n + σ) where σ is alphabet size.
    
    Args:
        bwt (str): The BWT string.
    
    Returns:
        dict: C-table mapping each character to its count.
    """
    # Count occurrences of each character
    counts = {}
    for c in bwt:
        counts[c] = counts.get(c, 0) + 1
    
    # Build C-table: cumulative counts in lexicographic order
    c_table = {}
    total = 0
    for c in sorted(counts.keys()):
        c_table[c] = total
        total += counts[c]
    
    return c_table


def build_occ_table(bwt):
    """
    Build the Occ table for FM-index.
    
    Occ[c][i] = number of occurrences of character c in BWT[0:i].
    Time complexity: O(σn) where σ is alphabet size and n is text length.
    Space complexity: O(σn).
    
    Args:
        bwt (str): The BWT string.
    
    Returns:
        dict: Occ table - dict mapping each character to a list of cumulative counts.
    """
    n = len(bwt)
    
    # Get all unique characters in BWT
    alphabet = sorted(set(bwt))
    
    # Initialize Occ table
    occ = {c: [0] * (n + 1) for c in alphabet}
    
    # Build Occ table
    for i in range(n):
        # Copy previous counts
        for c in alphabet:
            occ[c][i + 1] = occ[c][i]
        # Increment count for current character
        occ[bwt[i]][i + 1] += 1
    
    return occ


def fm_search(pattern, bwt, c_table, occ):
    """
    Perform backward search using FM-index to find all occurrences of pattern.
    
    Time complexity: O(m + k) where m is pattern length and k is number of occurrences.
    
    Args:
        pattern (str): Pattern to search for.
        bwt (str): The BWT string.
        c_table (dict): C-table for the BWT.
        occ (dict): Occ table for the BWT.
    
    Returns:
        tuple: (top, bottom) representing the range in suffix array where
               pattern occurs. If top > bottom, pattern is not found.
               The number of occurrences is (bottom - top + 1) if found.
    
    Example:
        >>> text = "banana$"
        >>> sa = build_suffix_array(text)
        >>> bwt = build_bwt(text, sa)
        >>> c_table = build_c_table(bwt)
        >>> occ = build_occ_table(bwt)
        >>> fm_search("ana", bwt, c_table, occ)
        (2, 3)  # Two occurrences
    """
    top = 0
    bottom = len(bwt) - 1
    
    # Process pattern from right to left (backward search)
    for i in range(len(pattern) - 1, -1, -1):
        c = pattern[i]
        
        # Check if character exists in the text
        if c not in c_table:
            return (1, 0)  # Not found (top > bottom)
        
        # Update range using LF mapping
        # LF(i) = C[BWT[i]] + Occ[BWT[i]][i]
        top = c_table[c] + occ[c][top]
        bottom = c_table[c] + occ[c][bottom + 1] - 1
        
        # Check if range is empty
        if top > bottom:
            return (top, bottom)  # Not found
    
    return (top, bottom)


def fm_find_all(pattern, text, sa, bwt, c_table, occ):
    """
    Find all occurrences of pattern using FM-index and return positions.
    
    Args:
        pattern (str): Pattern to search for.
        text (str): Original text (used for verification).
        sa (list): Suffix array.
        bwt (str): The BWT string.
        c_table (dict): C-table for the BWT.
        occ (dict): Occ table for the BWT.
    
    Returns:
        list: Sorted list of starting positions where pattern occurs.
    """
    top, bottom = fm_search(pattern, bwt, c_table, occ)
    
    if top > bottom:
        return []
    
    # Extract positions from suffix array
    positions = [sa[i] for i in range(top, bottom + 1)]
    
    return sorted(positions)
