"""
Several prime number functions
"""

from __future__ import division
from binary_search import binary_search, list_up_to
from math import sqrt, log, ceil
from numpy import ones, zeros

try:
    from sys import maxint
except ImportError: # pragma: no cover
    maxint = 9223372036854775807

try:
    range = xrange
except NameError: # pragma: no cover
    pass

class Primes(object):
    """
    List-like object that supports slicing and membership checking, automatically
    generating new primes when needed
    """

    def __init__(self):
        """
        Initialise an instance of the primes object
        """
        self.primes = []
        self.highest_known = 0

    def __iter__(self):
        """
        Iterate through the primes that have been generated
        """
        return self.primes.__iter__()

    def __len__(self):
        """
        Number of primes that have been generated
        """
        return len(self.primes)

    def __contains__(self, item):
        """
        Check if a number is prime:
        >>> primes = Primes()
        >>> 31 in primes
        True
        """
        if item > self.highest_known:
            self.primes = primes_up_to(item, self.primes)
        return not binary_search(self.primes, item) == -1

    def __getitem__(self, key):
        """
        Used in slicing to get a single prime or a sequence of primes
        """
        if isinstance(key, slice):
            if key.step == 0:
                raise ValueError("slice step cannot be zero")

            if all((s not in [None, maxint] for s in [key.start, key.stop, key.step])):
                if key.start > key.stop and key.step > 0 or key.stop > key.start and key.step < 0:
                    return []

            if key.start not in [None, maxint] and len(self)-1 < key.start:
                self.primes = n_primes(key.start+1, self.primes)
            if key.stop not in [None, maxint] and len(self) < key.stop:
                self.primes = n_primes(key.stop, self.primes)
        elif isinstance(key, int):
            if len(self)-1 < key:
                self.primes = n_primes(key+1, self.primes)
        else:
            raise TypeError()

        return self.primes[key]

    def __eq__(self, other):
        """
        Check for equality with a list of primes
        """
        return self.primes == other

    def __ne__(self, other):
        """
        Check for inequality with a list of primes
        """
        return self.primes != other

def _first_multiple_of(x, above):
    """
    Returns first multiple of x >= above
    """
    return above + ((x-(above%x)) % x)

def sieve_of_eratosthenes(x, primes=None):
    """
    Implementation of Sieve of Eratosthenes

    Returns a list of all primes up to (and including) x

    Can pass in a list of known primes to decrease execution time
    """

    # The Sieve of Eratosthenes works by making a list of numbers 2..x.
    # Each consecutive number is tested - if it is not crossed out, then
    # it is prime and multiples of this number up to n are crossed out.

    # Crossed and uncrossed numbers are represented as False and True
    # Only odd numbers are included, to reduce memory usage

    if x <= 1:
        return []

    # If a list of primes is passed in, take advantage of this
    # Even numbers aren't included in the list, so this isn't useful to know
    if primes and primes != [2]:
        # If enough primes are passed in, simply return the primes up to x
        if primes[-1] >= (x-1):
            # Primes is a sorted list so binary search is possible
            return list_up_to(primes, x)

        else:
            offset = primes[-1]+2
            lst = ones((x-offset)//2 + 1, dtype=bool)

            # Only go up to the sqrt(x) as all composites <= x have a factor <= sqrt(x)
            for prime in list_up_to(primes, int(sqrt(x)))[1:]:
                start = max(prime**2, _first_multiple_of(prime, offset))
                if start % 2 == 0:
                    start += prime

                lst[(start-offset)//2::prime] = False

    else:
        offset = 3
        lst = ones((x-offset)//2 + 1, dtype=bool)
        # Remember that 2 is prime, as it isn't referred to in the list
        primes = [2]

    # Only go up to the position of the square root of x as all composites <= x have
    # a factor <= x, so all composites will have been marked by square root of x
    for num in range(offset, int(sqrt(x))+1, 2):
        # Hasn't been crossed yet, so it's prime
        if lst[(num-offset) // 2]:
            primes.append(num)

            lst[(num**2 - offset)//2::num] = False

    # Now all composites up to x are known, add the uncrossed numbers to the list of primes

    # Start at the position of the square root + 1, rounded up to be odd
    # If primes passed in were > sqrt(x), start at the position of the
    # highest known prime + 1
    start = (max(primes[-1], int(sqrt(x))) + 1) | 1

    primes.extend(num for num in range(start, x+1, 2) if lst[(num-offset) // 2])

    return primes

def _range24(start, stop, step=2):
    """
    Like range(), but step is alternating between 2 and 4
    (or 4 and 2 if step is initially 4)
    """
    while start < stop:
        yield start
        start += step
        step = 2+(step&2)

def sieve_of_atkin(limit):
    """
    Implementation of Sieve of Atkin

    Returns a list of all primes up to (and including) x

    See http://compoasso.free.fr/primelistweb/page/prime/atkin_en.php for the range values 
    """

    if limit <= 5:
        return list_up_to([2, 3, 5], limit)

    res = [2, 3, 5]
    lst = zeros(limit+1, dtype=bool)
    s1, s2, s3 = set([1,13,17,29,37,41,49,53]), set([7,19,31,43]), set([11,23,47,59])

    squares = dict([(x, x**2) for x in range(1, int(sqrt(limit))+1)])

    range24_1_4 = list(_range24(1, int(sqrt(limit)) + 1, 4)) # +4, +2, +4.. from 1
    range24_2_2 = list(_range24(2, int(sqrt(limit)) + 1, 2)) # +2, +4, +2.. from 2
    range_1_2 = list(range(1, int(sqrt(limit)) + 1, 2))

    for x in range(1, int(sqrt(limit//4)) + 1):
        for y in list_up_to(range24_1_4 if x%3 == 0 else range_1_2, int(sqrt(limit - 4*squares[x]))):
            n = 4*squares[x] + squares[y]
            if n%60 in s1:
                lst[n] = True

    for x in range(1, int(sqrt(limit//3)) + 1, 2):
        for y in list_up_to(range24_2_2, int(sqrt(limit - 3*squares[x]))):
            n = 3*squares[x] + squares[y]
            if n%60 in s2:
                lst[n] = True

    for x in range(1, int(sqrt(limit)) + 1):
        for y in list_up_to(range24_1_4 if x%2 == 0 else range24_2_2, x):
            n = 3*squares[x] - squares[y]
            if n<=limit and n%60 in s3:
                lst[n] = True

    # Exclude multiples of 2, 3 and 5
    for num in list_up_to([i+n for i in range(1, int(sqrt(limit))+1, 30) for n in (0, 6, 10, 12, 16, 18, 22, 28)], int(sqrt(limit))):
        if lst[num]:
            res.append(num)
            lst[squares[num]::num*2] = False

    return res + [num for num in range(_first_multiple_of(2, int(sqrt(limit)))+1, limit+1, 2) if lst[num]]

def primes_up_to(x, primes=None):
    """
    Returns a list of primes up to (and including) x

    Uses (hopefully) the faster sieving algorithm available
    """

    return sieve_of_eratosthenes(x, primes)

def _trial_division(n, primes):
    """
    Simple trial division algorithm, check if n is prime by remainder dividing
    it by a list of known primes
    """
    return all(n%p != 0 for p in list_up_to(primes, int(sqrt(n))))

def _miller_rabin_2(n):
    """
    Single application of the Miller-Rabin primality test base-2

    Returns True if n is probably prime, False if n is composite
    """
    if n in (2, 3):
        return True

    d, s = n-1, 0
    while d%2 == 0:
        d //= 2
        s += 1

    x = pow(2, d, n)
    if x in (1, n-1):
        return True
    for _ in range(s-1):
        x = pow(x, 2, n)
        if x == 1:
            return False
        if x == n-1:
            return True

    return False

def is_prime(x, primes=None):
    """
    Returns True if x is a prime number, False if it is not

    Can pass in a list of known primes to decrease execution time
    """
    if x <= 1:
        return False

    if primes:
        if primes[-1] >= x:
            # If it's prime, it'll be in the list
            return not binary_search(primes, x) == -1
        elif primes[-1] >= sqrt(x):
            # If it's prime, none of the primes up to its square root will be a factor of it
            return _trial_division(x, primes)

    if not _trial_division(x, [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]):
        return False

    if not _miller_rabin_2(x):
        return False

    # Skip first 15 primes tried earlier
    return _trial_division(x, primes_up_to(int(sqrt(x)), primes)[15:])

def n_primes(n, primes=None):
    """
    Returns a list of the first n primes

    Can pass in a list of known primes to decrease execution time
    """
    if not primes:
        primes = []
    if len(primes) < n:
        if n >= 39017:
            upper_bound = int(n*(log(n) + log(log(n)) - 0.9484))
        elif n >= 15985:
            upper_bound = int(n*(log(n) + log(log(n)) - 0.9427))
        elif n >= 8602:
            upper_bound = int(n*(log(n) + log(log(n)) - 0.9385))
        elif n >= 6:
            upper_bound = int(n*(log(n) + log(log(n))))
        else:
            upper_bound = 13
        primes = primes_up_to(upper_bound, primes)
    return primes[:n]

def nth_prime(n, primes=None):
    """
    Returns the nth prime (e.g. the 3rd prime, the 6th prime)

    Can pass in a list of known primes to decrease execution time
    """
    return n_primes(n, primes)[-1]

def composites_up_to(x, primes=None):
    """
    Returns a list of all composite (non-prime greater than 1) numbers up to (and including) x

    Can pass in a list of known primes to decrease execution time
    """
    primes = primes_up_to(x, primes)
    composites = []
    for p1, p2 in zip(primes, primes[1:]): # Add numbers between primes to composites
        composites.extend(range(p1+1, p2))
    if primes:
        composites.extend(range(primes[-1]+1, x+1)) # Add numbers between last prime and x
    return composites

def next_prime(primes):
    """
    Given a list of primes, returns the next prime

    Uses method of trial division

    This is much less efficient than primes_up_to for generating ranges of primes
    """
    if not primes:
        return 2
    p = primes[-1]
    for num in range(_first_multiple_of(2, p)+1, 2*p, 2): # Odd numbers from highest known to double it
        if is_prime(num, primes):
            return num

def primes_with_difference_up_to(x, difference, primes=None):
    """
    Primes with difference up to x
    """
    return ((p, p+difference) for p in primes_up_to(x-difference, primes) if is_prime(p+difference, primes))

def twin_primes_up_to(x, primes=None):
    """
    Primes with difference 2 up to x
    """
    return primes_with_difference_up_to(x, 2, primes)

def cousin_primes_up_to(x, primes=None):
    """
    Primes with difference 4 up to x
    """
    return primes_with_difference_up_to(x, 4, primes)

def sexy_primes_up_to(x, primes=None):
    """
    Primes with difference 6 up to x
    """
    return primes_with_difference_up_to(x, 6, primes)

def prime_triplets_up_to(x, primes=None):
    """
    Prime triplets up to x
    """
    for p in primes_up_to(x-6, primes):
        if is_prime(p+2, primes) and is_prime(p+6, primes):
            yield (p, p+2, p+6)
        if is_prime(p+4, primes) and is_prime(p+6, primes):
            yield (p, p+4, p+6)

def prime_quadruplets_up_to(x, primes=None):
    """
    Prime quadruplets up to x
    """
    for p in primes_up_to(x-8, primes):
        if is_prime(p+2, primes) and is_prime(p+6, primes) and is_prime(p+8, primes):
            yield (p, p+2, p+6, p+8)

