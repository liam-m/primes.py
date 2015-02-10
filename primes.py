"""
Several prime number functions
"""

from __future__ import division
from binary_search import binary_search
from math import sqrt, log, ceil
from bisect import bisect_right

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
    return ceil(above/x) * x

class _IsPrimeList(object):
    """
    Helper class used in primes_up_to.
    List of booleans representing whether odd numbers from x-y are prime.
    Behaviour is undefined for numbers not in this range.

    As only odd numbers are represented, the amount of work in primes_up_to
    is effectively halved. Even less work is necessary when the lower bound
    is greater than 3.

    Initially, all numbers are 'uncrossed' (True), when a prime is found,
    call mark_multiples_as_composite
    """

    def _pos_of(self, num):
        """
        Position of num in self.lst
        """
        return (num-self.min_num) // 2

    def __init__(self, min_num, max_num):
        """
        Initialise a representation of a list of crossed and uncrossed numbers
        between min_num and max_num. All numbers are initially uncrossed
        """
        self.min_num = min_num
        self.max_num = max_num
        self.lst = [True] * (self._pos_of(max_num)+1)

    def __getitem__(self, num):
        """
        If num is an odd number between min_num and max_num, return True if num
        hasn't been crossed out yet, False if num has been crossed out
        """
        return self.lst[self._pos_of(num)]

    def __setitem__(self, num, item):
        """
        If num is an odd number between min_num and max_num, set it to item,
        which must be a bool. Only used in mark_multiples_as_composite for
        crossing out numbers
        """
        if num%2 == 1:
            self.lst[self._pos_of(num)] = item

    def mark_multiples_as_composite(self, prime):
        """
        Mark multiples of prime as composite

        Start at the square as multiples less than this will already have been
        marked as composite. If prime^2 < min_num, start at the first multiple
        of prime above min_num
        """
        start = max(prime**2, _first_multiple_of(prime, self.min_num))

        for index in range(int(start), self.max_num+1, prime):
            self[index] = False

def primes_up_to(x, primes=None):
    """
    Implementation of Sieve of Eratosthenes

    Returns a list of all primes up to (and including) x

    Can pass in a list of known primes to decrease execution time
    """

    # The Sieve of Eratosthenes works by making a list of numbers 2..x.
    # Each consecutive number is tested - if it is not crossed out, then
    # it is prime and multiples of this number up to n are crossed out.

    # A helper class represents crossed and uncrossed numbers as False and True
    # and has multiple other optimisations for efficiency

    if x <= 1:
        return []

    # If a list of primes is passed in, take advantage of this
    # The helper class effectively already has even numbers crossed out,
    # so this would not be useful to know
    if primes and primes != [2]:
        # If enough primes are passed in, we can simply return the primes up to x
        if primes[-1] >= (x-1):
            # Primes is a sorted list so we can binary search (bisect_right)
            return primes[:bisect_right(primes, x)]

        else:
            lst = _IsPrimeList(primes[-1]+2, x)

            # Only go up to the sqrt(x) as all composites <= x have a factor <= sqrt(x)
            for prime in primes[1:bisect_right(primes, int(sqrt(x)))]:
                lst.mark_multiples_as_composite(prime)
    else:
        lst = _IsPrimeList(3, x)
        # Remember that 2 is prime, as it isn't referred to in the helper class
        primes = [2]

    # Only go up to the position of the square root of x as all composites <= x have
    # a factor <= x, so all composites will have been marked by square root of x
    for num in range(lst.min_num, int(sqrt(x))+1, 2):
        # Hasn't been crossed yet, so it's prime
        if lst[num]:
            primes.append(num)
            # Start at the square as multiples < the square have already been marked
            lst.mark_multiples_as_composite(num)

    # Now all composites up to x are known, add the uncrossed numbers to the list of primes

    # Start at the position of the square root + 1, rounded up to be odd
    # If primes passed in were > sqrt(x), start at the position of the
    # highest known prime + 1
    start = (max(primes[-1], int(sqrt(x))) + 1) | 1

    primes.extend(num for num in range(start, x+1, 2) if lst[num])

    return primes

def _trial_division(n, primes):
    """
    Simple trial division algorithm, check if n is prime by remainder dividing
    it by a list of known primes
    """
    return all(n%p != 0 for p in primes[:bisect_right(primes, sqrt(n))])

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

    return _trial_division(x, primes_up_to(int(sqrt(x)), primes))

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
    if x <= 3:
        return []
    elif x == 4:
        return [4]
    primes = primes_up_to(x, primes)
    composites = []
    for p1, p2 in zip(primes, primes[1:]): # Add numbers between primes to composites
        composites.extend(list(range(p1+1, p2)))
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
    for num in range(p + p%2+1, 2*p, 2): # Odd numbers from highest known to double it
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

