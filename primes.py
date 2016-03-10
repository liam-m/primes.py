"""
Several prime number functions
"""

from __future__ import division
from math import log

try:
    from sys import maxint
except ImportError: # pragma: no cover
    maxint = 9223372036854775807

from numpy import ones, zeros

from binary_search import binary_search, list_up_to

try:
    range = xrange
except NameError: # pragma: no cover
    pass

class Primes(list):
    """
    List subclass that supports slicing and membership checking, automatically
    generating new primes when needed
    """

    def __init__(self):
        """
        Initialise an instance of the primes object
        """
        self.highest_known = 0
        super(self.__class__, self).__init__()

    def __contains__(self, item):
        """
        Check if a number is prime:
        >>> primes = Primes()
        >>> 31 in primes
        True
        """
        if item > self.highest_known:
            super(self.__class__, self).extend(primes_up_to(item, self)[len(self):])
        return not binary_search(self, item) == -1

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
                super(self.__class__, self).extend(n_primes(key.start+1, list(self))[len(self):])
            if key.stop not in [None, maxint] and len(self) < key.stop:
                super(self.__class__, self).extend(n_primes(key.stop, list(self))[len(self):])
        elif isinstance(key, int):
            if len(self)-1 < key:
                super(self.__class__, self).extend(n_primes(key+1, list(self))[len(self):])
        else:
            raise TypeError()

        return super(self.__class__, self).__getitem__(key)

    def __getslice__(self, i, j): # pragma: no cover
        """
        list still implements __getslice__ in 2.x, so it is overriden and calls __getitem__
        """
        return self[slice(i, j)]

def _first_multiple_of(num, above):
    """
    Returns first multiple of num >= above
    """
    return above + ((num-(above%num)) % num)

def sieve_of_eratosthenes(limit, primes=None):
    """
    Implementation of Sieve of Eratosthenes

    Returns a list of all primes up to (and including) limit

    Can pass in a list of known primes to decrease execution time
    """

    # The Sieve of Eratosthenes works by making a list of numbers 2..limit.
    # Each consecutive number is tested - if it is not crossed out, then
    # it is prime and multiples of this number up to n are crossed out.

    # Crossed and uncrossed numbers are represented as False and True
    # Only odd numbers are included, to reduce memory usage

    if limit <= 1:
        return []

    # If a list of primes is passed in, take advantage of this
    # Even numbers aren't included in the list, so this isn't useful to know
    if primes and primes != [2]:
        # If enough primes are passed in, simply return the primes up to limit
        if primes[-1] >= (limit-1):
            # Primes is a sorted list so binary search is possible
            return list_up_to(primes, limit)

        else:
            offset = primes[-1]+2
            lst = ones((limit-offset)//2 + 1, dtype=bool)

            # Only go up to the sqrt as all composites <= limit have a factor <= sqrt(limit)
            for prime in list_up_to(primes, int(limit ** 0.5))[1:]:
                start = max(prime**2, _first_multiple_of(prime, offset))
                if start % 2 == 0:
                    start += prime

                lst[(start-offset)//2::prime] = False

    else:
        offset = 3
        lst = ones((limit-offset)//2 + 1, dtype=bool)
        # Remember that 2 is prime, as it isn't referred to in the list
        primes = [2]

    # Only go up to the position of the sqrt as all composites <= limit have
    # a factor <= limit, so all composites will have been marked by sqrt(limit)
    for num in range(offset, int(limit**0.5)+1, 2):
        # Hasn't been crossed yet, so it's prime
        if lst[(num-offset) // 2]:
            primes.append(num)

            lst[(num**2 - offset)//2::num] = False

    # Now all composites <= limit are known, add the uncrossed numbers to the list of primes

    # Start at the position of the square root + 1, rounded up to be odd
    # If primes passed in were > sqrt(limit), start at the position of the
    # highest known prime + 1
    start = (max(primes[-1], int(limit ** 0.5)) + 1) | 1

    primes.extend(num for num in range(start, limit+1, 2) if lst[(num-offset) // 2])

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
    limit_sqrt = int(limit ** 0.5)
    s1, s2, s3 = set([1, 13, 17, 29, 37, 41, 49, 53]), set([7, 19, 31, 43]), set([11, 23, 47, 59])

    squares = dict([(x, x**2) for x in range(1, limit_sqrt+1)])

    range24_1_4 = list(_range24(1, limit_sqrt + 1, 4)) # +4, +2, +4.. from 1
    range24_2_2 = list(_range24(2, limit_sqrt + 1, 2)) # +2, +4, +2.. from 2
    range_1_2 = list(range(1, limit_sqrt + 1, 2))

    for x in range(1, int((limit//4) ** 0.5) + 1):
        for y in list_up_to(range24_1_4 if x%3 == 0 else range_1_2, int((limit-4*squares[x]) ** 0.5)):
            n = 4*squares[x] + squares[y]
            if n%60 in s1:
                lst[n] = True

    for x in range(1, int((limit//3) ** 0.5) + 1, 2):
        for y in list_up_to(range24_2_2, int((limit - 3*squares[x]) ** 0.5)):
            n = 3*squares[x] + squares[y]
            if n%60 in s2:
                lst[n] = True

    for x in range(1, limit_sqrt + 1):
        for y in list_up_to(range24_1_4 if x%2 == 0 else range24_2_2, x):
            n = 3*squares[x] - squares[y]
            if n <= limit and n%60 in s3:
                lst[n] = True

    # Exclude multiples of 2, 3 and 5
    for num in list_up_to([i+n for i in range(1, limit_sqrt+1, 30)
                           for n in (0, 6, 10, 12, 16, 18, 22, 28)], limit_sqrt):
        if lst[num]:
            res.append(num)
            lst[squares[num]::num*2] = False

    return res + [num for num in range(_first_multiple_of(2, limit_sqrt)+1, limit+1, 2) if lst[num]]

def primes_up_to(limit, primes=None):
    """
    Returns a list of primes up to (and including) limit

    Uses (hopefully) the faster sieving algorithm available
    """

    return sieve_of_eratosthenes(limit, primes)

def _trial_division(num, primes):
    """
    Simple trial division algorithm, check if num is prime by dividing
    it by a list of known primes
    """
    return all(num%p != 0 for p in list_up_to(primes, int(num ** 0.5)))

def _miller_rabin_2(num):
    """
    Single application of the Miller-Rabin primality test base-2

    Returns True if num is probably prime, False if n is composite
    """
    if num in (2, 3):
        return True

    d, s = num-1, 0
    while d%2 == 0:
        d //= 2
        s += 1

    x = pow(2, d, num)
    if x in (1, num-1):
        return True
    for _ in range(s-1):
        x = pow(x, 2, num)
        if x == 1:
            return False
        if x == num-1:
            return True

    return False

def is_prime(num, primes=None):
    """
    Returns True if num is a prime number, False if it is not

    Can pass in a list of known primes to decrease execution time
    """
    if num <= 1:
        return False

    if primes:
        if primes[-1] >= num:
            # If it's prime, it'll be in the list
            return not binary_search(primes, num) == -1
        elif primes[-1] >= num**0.5:
            # If it's prime, none of the primes up to its square root will be a factor of it
            return _trial_division(num, primes)

    if not _trial_division(num, [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]):
        return False

    if not _miller_rabin_2(num):
        return False

    # Skip first 15 primes tried earlier
    return _trial_division(num, primes_up_to(int(num ** 0.5), primes)[15:])

def n_primes(num, primes=None):
    """
    Returns a list of the first num primes

    Can pass in a list of known primes to decrease execution time
    """
    if not primes:
        primes = []
    if len(primes) < num:
        if num >= 39017:
            upper_bound = int(num*(log(num) + log(log(num)) - 0.9484))
        elif num >= 15985:
            upper_bound = int(num*(log(num) + log(log(num)) - 0.9427))
        elif num >= 8602:
            upper_bound = int(num*(log(num) + log(log(num)) - 0.9385))
        elif num >= 6:
            upper_bound = int(num*(log(num) + log(log(num))))
        else:
            upper_bound = 13
        primes = primes_up_to(upper_bound, primes)
    return primes[:num]

def nth_prime(num, primes=None):
    """
    Returns the numth prime (e.g. the 3rd prime, the 6th prime)

    Can pass in a list of known primes to decrease execution time
    """
    return n_primes(num, primes)[-1]

def composites_up_to(limit, primes=None):
    """
    Returns a list of all composite (non-prime greater than 1) numbers up to (and including) limit

    Can pass in a list of known primes to decrease execution time
    """
    primes = primes_up_to(limit, primes)
    composites = []
    for prime1, prime2 in zip(primes, primes[1:]):
        # Add numbers between primes to composites
        composites.extend(range(prime1+1, prime2))
    if primes:
        # Add numbers between last prime and x
        composites.extend(range(primes[-1]+1, limit+1))
    return composites

def next_prime(primes):
    """
    Given a list of primes, returns the next prime

    Uses method of trial division

    This is much less efficient than primes_up_to for generating ranges of primes
    """
    if not primes:
        return 2

    # Odd numbers from highest known to double it
    for num in range(_first_multiple_of(2, primes[-1])+1, 2*primes[-1], 2):
        if is_prime(num, primes):
            return num

def primes_with_difference_up_to(limit, difference, primes=None):
    """
    Primes with difference up to limit
    """
    return ((prime, prime+difference) for prime in primes_up_to(limit-difference, primes)
            if is_prime(prime+difference, primes))

def twin_primes_up_to(limit, primes=None):
    """
    Primes with difference 2 up to limit
    """
    return primes_with_difference_up_to(limit, 2, primes)

def cousin_primes_up_to(limit, primes=None):
    """
    Primes with difference 4 up to limit
    """
    return primes_with_difference_up_to(limit, 4, primes)

def sexy_primes_up_to(limit, primes=None):
    """
    Primes with difference 6 up to limit
    """
    return primes_with_difference_up_to(limit, 6, primes)

def prime_triplets_up_to(limit, primes=None):
    """
    Prime triplets up to limit
    """
    for prime in primes_up_to(limit-6, primes):
        if is_prime(prime+2, primes) and is_prime(prime+6, primes):
            yield (prime, prime+2, prime+6)
        if is_prime(prime+4, primes) and is_prime(prime+6, primes):
            yield (prime, prime+4, prime+6)

def prime_quadruplets_up_to(limit, primes=None):
    """
    Prime quadruplets up to limit
    """
    for prime in primes_up_to(limit-8, primes):
        if is_prime(prime+2, primes) and is_prime(prime+6, primes) and is_prime(prime+8, primes):
            yield (prime, prime+2, prime+6, prime+8)

def gcd(a, b):
    """
    The greatest common denominator of a and b
    """
    while b > 0:
        r = a % b
        a = b
        b = r
    return a

def pollards_rho(num, starting_point=2):
    """
    Return a factor of num using Pollard's rho algorithm
    """
    f = lambda x: (pow(x, 2, num) + 1) % num
    x, y = starting_point, starting_point
    while True:
        x = f(x)
        y = f(f(y))
        d = gcd((x-y) % num, num)
        if d == num:
            return pollards_rho(num, starting_point+1)
        elif d != 1:
            return d

def factorise(num):
    """
    Factorise a semiprime number
    """
    factor = pollards_rho(num)
    return set([factor, num//factor])
