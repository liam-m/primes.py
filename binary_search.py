"""
Binary search function built on bisect_left
"""

from bisect import bisect_left, bisect_right
from typing import Sequence, TypeVar

def binary_search(haystack, needle, low=0, high=None) -> int: # can't use a to specify default for high
    """
    Same as bisect_left but returns -1 if x is not in lst
    """
    high = high if high is not None else len(haystack) # high defaults to len(a)
    pos = bisect_left(haystack, needle, low, high) # find insertion position
    return pos if pos != high and haystack[pos] == needle else -1 # don't walk off the end

T = TypeVar('T')

def list_up_to(lst: Sequence[T], limit: int) -> Sequence[T]:
    """
    lst - sorted list
    Returns elements of lst <= limit
    """
    return lst[:bisect_right(lst, limit)]
