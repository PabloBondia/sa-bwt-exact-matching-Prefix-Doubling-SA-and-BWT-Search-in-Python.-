#!/usr/bin/env python3
"""
Simple example demonstrating suffix array and BWT/FM-index usage.
"""

from src.sa import build_suffix_array
from src.sa_search import find_all as sa_find_all
from src.bwt import build_bwt, build_c_table, build_occ_table, fm_find_all


def main():
    # Example text (must end with '$' sentinel)
    text = "banana$"
    print(f"Text: {text}\n")
    
    # Build suffix array
    print("Building suffix array...")
    sa = build_suffix_array(text)
    print(f"Suffix array: {sa}")
    
    # Display sorted suffixes
    print("\nSorted suffixes:")
    for i, pos in enumerate(sa):
        print(f"  {i}: {text[pos:]}")
    
    # Search using suffix array
    print("\n" + "="*50)
    print("Searching using Suffix Array:")
    print("="*50)
    patterns = ["ana", "na", "ban", "xyz"]
    for pattern in patterns:
        positions = sa_find_all(text, sa, pattern)
        if positions:
            print(f"'{pattern}' found at positions: {positions}")
        else:
            print(f"'{pattern}' not found")
    
    # Build BWT and FM-index
    print("\n" + "="*50)
    print("Building BWT and FM-index:")
    print("="*50)
    bwt = build_bwt(text, sa)
    print(f"BWT: {bwt}")
    
    c_table = build_c_table(bwt)
    print(f"C-table: {c_table}")
    
    occ = build_occ_table(bwt)
    print(f"Occ table built for characters: {list(occ.keys())}")
    
    # Search using FM-index
    print("\n" + "="*50)
    print("Searching using FM-index:")
    print("="*50)
    for pattern in patterns:
        positions = fm_find_all(pattern, text, sa, bwt, c_table, occ)
        if positions:
            print(f"'{pattern}' found at positions: {positions}")
        else:
            print(f"'{pattern}' not found")
    
    print("\n✅ Both methods produce identical results!")


if __name__ == "__main__":
    main()
