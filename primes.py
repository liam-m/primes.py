"""
Several prime number functions
"""

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

def primes_up_to(x, primes=None):
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

    def _pos_of(num, offset=3):
        """
        Position of number in lst
        """
        return int((num-offset) / 2)

    def _num_at(pos, offset=3):
        """
        Number at position in lst e.g. lst[0] refers to 3, lst[2] refers to 7
        """
        return pos*2 + offset

    def _first_multiple_of(x, above):
        """
        Returns first multiple of x >= above
        """
        return ceil(above/x) * x

    def _mark_as_composite(lst, start, step):
        """
        Mark items in lst as composite (False) from start, increasing in increments of step
        """
        for index in range(start, len(lst), step):
            lst[index] = False

    if x <= 1:
        return []

    elif x == 3: # Bug fix. May need to change logic in future so this isn't necessary
        return [2, 3]

    # As this function takes advantage of 2 being the only even prime,
    # passing in 2 is not useful, so we'll strip that out
    elif not primes or primes == [2]:
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
            # _pos_of(x) will be the position of the last element - so we want a list
            # this of this length + 1
            lst = [True] * (_pos_of(x, offset)+1)

            # Mark all multiples of the known primes as not prime
            # Only go up to the sqrt(x) as all composites <= x have a factor <= sqrt(x)
            for prime in primes[1:bisect_right(primes, int(sqrt(x)))]:
                # Start at the square as multiples < the square have already been marked
                # If the square isn't in the list (because offset > than the square),
                # then start marking from the first multiple of the prime above offset
                start = _pos_of(max(prime**2, _first_multiple_of(prime, offset)), offset)
                _mark_as_composite(lst, start, prime)

            # Start the main algorithm at the position of highest known prime + 1
            start = _pos_of(primes[-1], offset) + 1

    # When no primes are known prior to the main algorithm
    else:
        # The list will refer to 3, 5 .. x-2, x
        offset = 3
        lst = [True] * (_pos_of(x, offset)+1)
        # Remember that 2 is prime, as it isn't referred to in the list
        primes = [2]
        # Start the main algorithm at the first element of the list - 3
        start = 0

    # Go through the numbers in the list up to the square root of x
    # Only go up to the position of the square root of x as all composites <= x have
    # a factor <= x, so all composites will have been marked by square root of x
    for index in range(start, _pos_of(int(sqrt(x)), offset)+1):
        # If the number at the index is True, then it's prime
        if lst[index]:
            num = _num_at(index, offset)
            primes.append(num)
            # Start at the square as multiples < the square have already been marked
            _mark_as_composite(lst, _pos_of(num**2, offset), num)

    # Now all non-primes are now False, so go through the rest of the numbers
    # and add the ones that aren't crossed out to the list of primes

    # Start at the position of the square root + 1
    # If primes passed in were > sqrt(x), then we'll start at the position of the
    # highest known prime + 1
    start = _pos_of(max(primes[-1], int(sqrt(x))), offset) + 1

    primes.extend(_num_at(index, offset) for index in range(start, len(lst)) if lst[index])

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
        if n >= 8602:
            upper_bound = int(n*log(n) + n*(log(log(n)) - 0.9385))
        elif n >= 6:
            upper_bound = int(n * (log(n) + log(log(n))))
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

