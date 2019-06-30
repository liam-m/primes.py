"""
Several prime number functions
"""

from __future__ import division
from math import log

try:
    from sys import maxint
except ImportError: # pragma: no cover
    maxint = 9223372036854775807

try:
    from math import gcd
except ImportError: # pragma: no cover
    from fractions import gcd

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
        super(self.__class__, self).__init__()

    def __contains__(self, item):
        """
        Check if a number is prime:
        >>> primes = Primes()
        >>> 31 in primes
        True
        """
        return is_prime(item, self)

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

    def index(self, prime):
        """
        The index of the prime
        """
        if len(self) == 0 or self[-1] < prime:
            super(self.__class__, self).extend(primes_up_to(prime, self)[len(self):])
        return super(self.__class__, self).index(prime)

def _first_multiple_of(num, above):
    """
    Returns first multiple of num >= above
    """
    return above + ((num-(above%num)) % num)

def sieve_of_eratosthenes(limit, primes=None):
    """
    Implementation of Sieve of Eratosthenes

    Returns all primes up to (and including) limit

    Can pass in known primes to decrease execution time
    """

    # The Sieve of Eratosthenes works by making a list of numbers 2..limit.
    # Each consecutive number is tested - if it is not crossed out, then
    # it is prime and multiples of this number up to n are crossed out.

    # Crossed and uncrossed numbers are represented as False and True
    # Only odd numbers are included, to reduce memory usage

    if limit <= 1:
        return []

    # If primes are passed in, take advantage of this
    # Even numbers aren't included in the list, so this isn't useful to know
    if primes and len(primes) > 1:
        # If enough primes are passed in, simply return the primes up to limit
        if primes[-1] >= (limit-1):
            # Primes is a sorted list so binary search is possible
            return list_up_to(primes, limit)

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

    Returns all primes up to (and including) x

    See http://compoasso.free.fr/primelistweb/page/prime/atkin_en.php for the range values
    """

    if limit <= 6:
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
    Returns primes up to (and including) limit

    Uses (hopefully) the faster sieving algorithm available
    """

    return sieve_of_eratosthenes(limit, primes)

def _trial_division(num, primes):
    """
    Simple trial division algorithm, check if num is prime by dividing
    it by known primes
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

def _jacobi_symbol(a, n):
    """
    Calculate the Jacobi symbol (a/n)
    """
    if n == 1: # pragma: no cover
        return 1
    elif a == 0:
        return 0
    elif a == 1:
        return 1
    elif a == 2:
        if n % 8 in [3, 5]:
            return -1
        elif n % 8 in [1, 7]:
            return 1
    elif a < 0:
        return (-1)**((n-1)//2) * _jacobi_symbol(-1*a, n)

    if a % 2 == 0:
        return _jacobi_symbol(2, n) * _jacobi_symbol(a // 2, n)
    elif a % n != a:
        return _jacobi_symbol(a % n, n)
    else:
        if a % 4 == n % 4 == 3:
            return -1 * _jacobi_symbol(n, a)
        else:
            return _jacobi_symbol(n, a)

def _D_chooser(num):
    """
    Choose a D value suitable for the Baillie-PSW test
    """
    D = 5
    while _jacobi_symbol(D, num) != -1:
        D += 2 if D > 0 else -2
        D *= -1
    return D

def _U_V_subscript(k, n, U, V, P, Q, D):
    k, n, U, V, P, Q, D = map(int, (k, n, U, V, P, Q, D))
    digits = list(map(int, str(bin(k))[2:]))
    subscript = 1
    for digit in digits[1:]:
        U, V = U*V % n, (pow(V, 2, n) - 2*pow(Q, subscript, n)) % n
        subscript *= 2
        if digit == 1:
            if not (P*U + V) & 1:
                if not (D*U + P*V) & 1:
                    U, V = (P*U + V) >> 1, (D*U + P*V) >> 1
                else: # pragma: no cover
                    U, V = (P*U + V) >> 1, (D*U + P*V + n) >> 1
            elif not (D*U + P*V) & 1: # pragma: no cover
                U, V = (P*U + V + n) >> 1, (D*U + P*V) >> 1
            else:
                U, V = (P*U + V + n) >> 1, (D*U + P*V + n) >> 1
            subscript += 1
            U, V = U % n, V % n
    return U, V

def _lucas_pp(num):
    """
    Perform the Lucas probable prime test

    Returns True if num is probably prime, False if n is composite
    """
    if num == 2:
        return True

    D = _D_chooser(num)
    P = 1
    Q = (1-D)//4
    U, V = _U_V_subscript(num+1, num, 1, P, P, Q, D)

    if U != 0:
        return False

    d = num + 1
    s = 0
    while not d & 1:
        d = d >> 1
        s += 1

    U, V = _U_V_subscript(num+1, num, 1, P, P, Q, D)

    if U == 0:
        return True
    else: # pragma: no cover
        for r in range(s):
            U, V = (U*V) % num, (pow(V, 2, num) - 2*pow(Q, d*(2**r), num)) % num
            if V == 0:
                return True

        return False

def is_prime(num, primes=None):
    """
    Returns True if num is a prime number, False if it is not

    Can pass in known primes to decrease execution time
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

    return _miller_rabin_2(num) and _lucas_pp(num)

def n_primes(num, primes=None):
    """
    Returns the first num primes

    Can pass in known primes to decrease execution time
    """
    if not primes:
        primes = Primes()
    
    if len(primes) < num:
        if num < 6:
            upper_bound = 13
        else:
            logn = log(num)
            log2n = log(logn)
            
            if num >= 46254381: # Axler 2017, p. 2 # pragma: no cover
                upper_bound = int(num*(logn + log2n - 1.0 + ((log2n-2.00)/logn) - ((log2n*log2n-6*log2n+10.667)/(2*logn*logn))))
            elif num >= 8009824: # Axler 2013, p. 8
                upper_bound = int(num*(logn + log2n - 1.0 + ((log2n-2.00)/logn) - ((log2n*log2n-6*log2n+10.273)/(2*logn*logn))))
            elif num >= 688383: # Dusart 2010, p. 2
                upper_bound = int(num*(logn + log2n - 1.0 + ((log2n-2.00)/logn)))
            elif num >= 178974: # Dusart 2010, p. 7
                upper_bound = int(num*(logn + log2n - 1.0 + ((log2n-1.95)/logn)))
            elif num >= 39017: # Dusart 1999, p. 14
                upper_bound = int(num*(logn + log2n - 0.9484))
            elif num >= 15985: # Massias & Robin 1996, p. 4
                upper_bound = int(num*(logn + log2n - 0.9427))
            elif num >= 8602: # Robin 1983, corrected
                upper_bound = int(num*(logn + log2n - 0.9385))
            elif num >= 13: # Massias & Robin 1996, p. 4
                upper_bound = int(num*(logn + log2n - 1.0 + 1.8*(log2n/logn)))
            else:
                upper_bound = int(num*(logn + log2n))
        primes = primes_up_to(upper_bound, primes)
    return primes[:num]

def nth_prime(num, primes=None):
    """
    Returns the numth prime (e.g. the 3rd prime, the 6th prime)

    Can pass in known primes to decrease execution time
    """
    return n_primes(num, primes)[-1]

def composites_up_to(limit, primes=None):
    """
    Returns all composite (non-prime greater than 1) numbers up to (and including) limit

    Can pass in known primes to decrease execution time
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
    Given primes, returns the next prime

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
    if not primes:
        primes = Primes()

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
    if not primes:
        primes = Primes()

    for prime in primes_up_to(limit-6, primes):
        if is_prime(prime+2, primes) and is_prime(prime+6, primes):
            yield (prime, prime+2, prime+6)
        if is_prime(prime+4, primes) and is_prime(prime+6, primes):
            yield (prime, prime+4, prime+6)

def prime_quadruplets_up_to(limit, primes=None):
    """
    Prime quadruplets up to limit
    """
    if not primes:
        primes = Primes()

    for prime in primes_up_to(limit-8, primes):
        if is_prime(prime+2, primes) and is_prime(prime+6, primes) and is_prime(prime+8, primes):
            yield (prime, prime+2, prime+6, prime+8)

def prime_gaps_up_to(limit, primes=None):
    """
    Difference between successive primes up to limit
    """
    if not primes:
        primes = Primes()

    primes = primes_up_to(limit, primes)
    for prime1, prime2 in zip(primes, primes[1:]):
        yield prime2 - prime1

def pollards_rho(num, starting_point=2):
    """
    Return a factor of num using Pollard's rho algorithm, or num if one is not found
    """
    starting_point_fixed = starting_point
    cycle_size = 2
    factor = 1

    while factor == 1:
        count = 1
        while count <= cycle_size and factor <= 1:
            starting_point = (starting_point*starting_point + 1) % num
            factor = gcd(abs(starting_point - starting_point_fixed), num)
            count += 1
        cycle_size *= 2
        starting_point_fixed = starting_point
    return factor

def factorise(num, include_trivial=False, primes=None):
    """
    Factorise a number

    Returns the prime factors of num
    Excludes trivial factors unless include_trivial = True
    """
    if not primes:
        primes = Primes()

    factors = set([1, num]) if include_trivial else set()

    if is_prime(num, primes):
        return factors

    while num > 1 and not is_prime(num, primes):
        starting_point = 2
        factor = pollards_rho(num, starting_point)
        while factor == num:
            factor = pollards_rho(num, starting_point)
            starting_point += 1

        if is_prime(factor, primes):
            factors.add(factor)
        else:
            factors |= factorise(factor, primes=primes)

        while num % factor == 0:
            num //= factor
    if num > 1:
        factors.add(num)
    return factors
