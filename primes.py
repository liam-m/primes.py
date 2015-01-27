from binarySearch import binarySearch
from math import sqrt, log, ceil
from bisect import bisect_right

try:
    from sys import maxint
except ImportError:
    maxint = 9223372036854775807

class Primes:
    def __init__(self):
        self.primes = []
        self.highest_known = 0

    def __iter__(self):
        return self.primes.__iter__()

    def __len__(self):
        return len(self.primes)

    def __contains__(self, item):
        if item > self.highest_known:
            self.primes = primesUpTo(item, self.primes)
        return item in self.primes

    def __getitem__(self, key):
        if isinstance(key, slice):
            l = max(len(self), key.stop if key.stop not in [None, maxint] else 0)-1
            start, stop, step = key.indices(l)
        elif isinstance(key, int):
            start, stop, step = 0, key, 1
        
        if len(self)-1 < stop:
            self.primes = nPrimes(stop+1, self.primes)
        return self.primes[key]

    def __eq__(self, other):
        return self.primes == other

    def __ne__(self, other):
        return self.primes != other

def primesUpTo(x, primes=[]):
    """
    Implementation of Sieve of Eratosthenes
    
    Returns a list of all primes up to (and including) x

    Can pass in a list of known primes to decrease execution time
    """
    
    # The Sieve of Eratosthenes works by making a list of numbers 2..n.
    # Each consecutive number is tested - if it is not crossed out, then
    # it is prime and multiples of this number up to n are crossed out.

    # In this implementation, uncrossed numbers in the list are
    # represented by True and crossed numbers are represented by False.
    # In addition, this implementation also takes advantage of the fact
    # that the only even prime is 2. Only odd numbers 3..n are listed,
    # meaning that only half the 'crossing out' is necessary.
    
    def _posOf(num, offset=3):
        # Position of number in lst
        return int((num-offset) / 2)

    def _numAt(pos, offset=3):
        # Number at position in lst e.g. lst[0] refers to 3, lst[2] refers to 7
        return pos*2 + offset

    def _firstMultipleOf(x, above):
        # Returns first multiple of x >= above
        return ceil(above/x) * x

    def _markAsComposite(lst, start, step):
        # Mark items in lst as composite (False) from start, increasing in increments of step
        for index in range(start, len(lst), step):
            lst[index] = False
    
    if x <= 1: 
        return []

    elif x == 3: # Bug fix. May need to change logic in future so this isn't necessary
        return [2, 3]

    # As this function takes advantage of 2 being the only even prime,
    # passing in 2 is not useful, so we'll strip that out
    elif primes == [2]:
        primes = []

    # If a list of primes is passed in, take advantage of this
    if primes:
        # If enough primes are passed in, we can simply return the primes up to x
        if primes[-1] >= (x-1):
            # Primes is a sorted list so we can binary search (bisect_right)
            return primes[:bisect_right(primes, x)]

        # We have a partial list of primes
        else:
            # Offset is the number the first element of the list refers to.
            # To reduce memory usage, this should be primes[-1]+2
            # i.e. the next odd number above highest known prime)
            offset = 3 # primes[-1]+2
            # lst is the list of (initially) uncrossed numbers from offset to x
            # _posOf(x) will be the position of the last element - so we want a list
            # this of this length + 1
            lst = [True] * (_posOf(x, offset)+1)

            # Mark all multiples of the known primes as not prime
            # Only go up to the sqrt(x) as all composites <= x have a factor <= sqrt(x)
            for prime in primes[1:bisect_right(primes, int(sqrt(x)))]:
                # Start at the square as multiples < the square have already been marked
                # If the square isn't in the list (because offset > than the square),
                # then start marking from the first multiple of the prime above offset
                start = _posOf(max(prime**2, _firstMultipleOf(prime, offset)), offset)
                _markAsComposite(lst, start, prime)

            # Start the main algorithm at the position of highest known prime + 1
            start = _posOf(primes[-1], offset) + 1

    # When no primes are known prior to the main algorithm                   
    else:
        # The list will refer to 3, 5 .. x-2, x
        offset = 3
        lst = [True] * (_posOf(x, offset)+1)
        # Remember that 2 is prime, as it isn't referred to in the list
        primes = [2]
        # Start the main algorithm at the first element of the list - 3
        start = 0 

    # Go through the numbers in the list up to the square root of x
    # Only go up to the position of the square root of x as all composites <= x have
    # a factor <= x, so all composites will have been marked by square root of x
    for index in range(start, _posOf(int(sqrt(x)), offset)+1):
        # If the number at the index is True, then it's prime
        if lst[index]:
            num = _numAt(index, offset)
            primes.append(num)
            # Start at the square as multiples < the square have already been marked
            _markAsComposite(lst, _posOf(num**2, offset), num)

    # Now all non-primes are now False, so go through the rest of the numbers
    # and add the ones that aren't crossed out to the list of primes

    # Start at the position of the square root + 1
    # If primes passed in were > sqrt(x), then we'll start at the position of the
    # highest known prime + 1
    start = _posOf(max(primes[-1], int(sqrt(x))), offset) + 1

    primes.extend(_numAt(index, offset) for index in range(start, len(lst)) if lst[index])
    
    return primes

def isPrime(x, primes=[]):
    """
    Returns True if x is a prime number, False if it is not

    Can pass in a list of known primes to decrease execution time
    """
    if x <= 1:
        return False
    
    if primes:
        if primes[-1] >= x: # If it's prime, it'll be in the list
            return not binarySearch(primes, x) == -1
        elif primes[-1] >= sqrt(x): # If it's prime, none of the primes up to its square root will be a factor of it
            for prime in primes:
                if prime > sqrt(x):
                    break
                if x % prime == 0:
                    return False
            return True
    # Not enough primes have been worked out
    primes = primesUpTo(int(sqrt(x)), primes)
    for prime in primes:
        if x % prime == 0:
            return False
    return True

def nPrimes(n, primes=[]):
    """
    Returns a list of the first n primes

    Can pass in a list of known primes to decrease execution time
    """
    if len(primes) < n:
        if n >= 8602:
            upperBound = int(n*log(n) + n*(log(log(n)) - 0.9385))
        elif n >= 6:
            upperBound = int(n * (log(n) + log(log(n))))
        else:
            upperBound = 13
        primes = primesUpTo(upperBound, primes)
    return primes[:n]

def nthPrime(n, primes=[]):
    """
    Returns the nth prime (e.g. the 3rd prime, the 6th prime)

    Can pass in a list of known primes to decrease execution time    
    """
    return nPrimes(n, primes)[-1]

def compositesUpTo(x, primes=[]):
    """
    Returns a list of all composite (non-prime greater than 1) numbers up to (and including) x

    Can pass in a list of known primes to decrease execution time
    """
    if x <= 3:
        return []
    elif x == 4:
        return [4]
    primes = primesUpTo(x, primes)
    composites = []
    for p1, p2 in zip(primes, primes[1:]): # Add numbers between primes to composites
        composites.extend(list(range(p1+1, p2)))
    composites.extend(range(primes[-1]+1, x+1)) # Add numbers between last prime and x
    return composites

def nextPrime(primes):
    """
    Given a list of primes, returns the next prime

    Uses method of trial division
    
    This is much less efficient than primesUpTo for generating ranges of primes
    """
    if not primes:
        return 2
    p = primes[-1]
    for num in range(p + p%2+1, 2*p, 2): # Odd numbers from highest known to double it
        if isPrime(num, primes):
            return num

def primesWithDifferenceUpTo(x, difference, primes=[]):
    return ((p, p+difference) for p in primesUpTo(x-difference, primes) if isPrime(p+difference, primes))

def twinPrimesUpTo(x, primes=[]):
    return primesWithDifferenceUpTo(x, 2, primes)

def cousinPrimesUpTo(x, primes=[]):
    return primesWithDifferenceUpTo(x, 4, primes)

def sexyPrimesUpTo(x, primes=[]):
    return primesWithDifferenceUpTo(x, 6, primes)

def primeTripletsUpTo(x, primes=[]):
    for p in primesUpTo(x-6, primes):
        if isPrime(p+2, primes) and isPrime(p+6, primes):
            yield (p, p+2, p+6)
        if isPrime(p+4, primes) and isPrime(p+6, primes):
            yield (p, p+4, p+6)

def primeQuadrupletsUpTo(x, primes=[]):
    for p in primesUpTo(x-8, primes):
        if isPrime(p+2, primes) and isPrime(p+6, primes) and isPrime(p+8, primes):
            yield (p, p+2, p+6, p+8)

