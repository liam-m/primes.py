from bisect import bisect_left

def binarySearch(lst, x, lo=0, hi=None):   # can't use a to specify default for hi
    """
    Same as bisect_left but returns -1 if x is not in lst
    """
    hi = hi if hi is not None else len(lst) # hi defaults to len(a)   
    pos = bisect_left(lst,x,lo,hi)          # find insertion position
    return (pos if pos != hi and lst[pos] == x else -1) # don't walk off the end
