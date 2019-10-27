"""
Binary search function built on bisect_left
"""

from bisect import bisect_left, bisect_right
from typing import Optional, Sequence, TypeVar

# pylint: disable=invalid-name
T = TypeVar('T')
# pylint: enable=invalid-name

def binary_search(haystack: Sequence[T], needle: T,
                  low: int = 0, high: Optional[int] = None) -> int: # can't use a to specify default for high
    """
    Same as bisect_left but returns -1 if x is not in lst
    """
    high = high if high is not None else len(haystack) # high defaults to len(a)
    pos = bisect_left(haystack, needle, low, high) # find insertion position
    return pos if pos != high and haystack[pos] == needle else -1 # don't walk off the end

def list_up_to(lst: Sequence[T], limit: int) -> Sequence[T]:
    """
    lst - sorted list
    Returns elements of lst <= limit
    """
    return lst[:bisect_right(lst, limit)]
