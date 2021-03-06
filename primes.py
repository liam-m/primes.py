"""
Several prime number functions
"""
from math import gcd, log
from typing import Any, Iterator, Iterable, List, Optional, Tuple, Sequence, Set

from numpy import ones, zeros

from binary_search import binary_search, list_up_to

class Primes(Sequence[int]):
    """
    List subclass that supports slicing and membership checking, automatically
    generating new primes when needed
    """

    def __init__(self) -> None:
        self.primes: List[int] = []

    def __contains__(self, item: Any) -> bool:
        """
        Check if a number is prime:
        >>> primes = Primes()
        >>> 31 in primes
        True
        """
        return is_prime(item, self)

    def __getitem__(self, key: Any) -> Any:
        """
        Used in slicing to get a single prime or a sequence of primes
        """
        if isinstance(key, slice):
            if key.step == 0:
                raise ValueError("slice step cannot be zero")

            if all((s is not None for s in [key.start, key.stop, key.step])):
                if key.start > key.stop and key.step > 0 or key.stop > key.start and key.step < 0:
                    return []

        num_required = max((key.start or -1)+1, key.stop or 0) if isinstance(key, slice) else key+1
        if len(self) < num_required:
            self.primes += n_primes(num_required, self)[len(self):]

        return self.primes[key]

    def index(self, prime: int, start: int = 0, stop: Optional[int] = None) -> int:
        """
        The index of the prime
        """
        if not self or self[-1] < prime:
            self.primes += primes_up_to(prime, self)[len(self):]
        idx = binary_search(self.primes, prime, start, stop)
        if idx < 0:
            raise ValueError(f"{prime} is not prime")
        return idx

    def __eq__(self, other: Any) -> Any:
        if isinstance(other, Primes):
            other = other.primes
        return self.primes == other

    def __iter__(self) -> Iterator[int]:
        return iter(self.primes)

    def __len__(self) -> int:
        return len(self.primes)

def _first_multiple_of(num: int, above: int) -> int:
    """
    Returns first multiple of num >= above
    """
    return above + ((num-(above%num)) % num)

def sieve_of_eratosthenes(limit: int, primes: Optional[Sequence[int]] = None) -> Sequence[int]:
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

    l_primes = list(primes)

    # Only go up to the position of the sqrt as all composites <= limit have
    # a factor <= limit, so all composites will have been marked by sqrt(limit)
    for num in range(offset, int(limit**0.5)+1, 2):
        # Hasn't been crossed yet, so it's prime
        if lst[(num-offset) // 2]:
            l_primes.append(num)

            lst[(num**2 - offset)//2::num] = False

    # Now all composites <= limit are known, add the uncrossed numbers to the list of primes

    # Start at the position of the square root + 1, rounded up to be odd
    # If primes passed in were > sqrt(limit), start at the position of the
    # highest known prime + 1
    start = (max(l_primes[-1], int(limit ** 0.5)) + 1) | 1

    l_primes.extend(num for num in range(start, limit+1, 2) if lst[(num-offset) // 2])

    return l_primes

def _range24(start: int, stop: int, step: int = 2) -> Iterable[int]:
    """
    Like range(), but step is alternating between 2 and 4
    (or 4 and 2 if step is initially 4)
    """
    while start < stop:
        yield start
        start += step
        step = 2+(step&2)

def sieve_of_atkin(limit: int) -> Sequence[int]:
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

    squares = {x: x**2 for x in range(1, limit_sqrt+1)}

    range24_1_4 = list(_range24(1, limit_sqrt + 1, 4)) # +4, +2, +4.. from 1
    range24_2_2 = list(_range24(2, limit_sqrt + 1, 2)) # +2, +4, +2.. from 2
    range_1_2 = list(range(1, limit_sqrt + 1, 2))

    # pylint: disable=invalid-name
    s1, s2, s3 = set([1, 13, 17, 29, 37, 41, 49, 53]), set([7, 19, 31, 43]), set([11, 23, 47, 59])

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
    # pylint: enable=invalid-name

    # Exclude multiples of 2, 3 and 5
    for num in list_up_to([i+n for i in range(1, limit_sqrt+1, 30)
                           for n in (0, 6, 10, 12, 16, 18, 22, 28)], limit_sqrt):
        if lst[num]:
            res.append(num)
            lst[squares[num]::num*2] = False

    return res + [num for num in range(_first_multiple_of(2, limit_sqrt)+1, limit+1, 2) if lst[num]]

def primes_up_to(limit: int, primes: Optional[Sequence[int]] = None) -> Sequence[int]:
    """
    Returns primes up to (and including) limit

    Uses (hopefully) the faster sieving algorithm available
    """
    return sieve_of_eratosthenes(limit, primes)

def _trial_division(num: int, primes: Sequence[int]) -> bool:
    """
    Simple trial division algorithm, check if num is prime by dividing
    it by known primes
    """
    return all(num%p != 0 for p in list_up_to(primes, int(num ** 0.5)))

def _miller_rabin_2(num: int) -> bool:
    """
    Single application of the Miller-Rabin primality test base-2

    Returns True if num is probably prime, False if n is composite
    """
    if num in (2, 3):
        return True

    # pylint: disable=invalid-name
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
    # pylint: enable=invalid-name

    return False

# pylint: disable=invalid-name,too-many-return-statements
def _jacobi_symbol(a: int, n: int) -> int:
    """
    Calculate the Jacobi symbol (a/n)
    """
    if n == 1: # pragma: no cover
        return 1
    if a == 0:
        return 0
    if a == 1:
        return 1
    if a == 2:
        if n % 8 in [3, 5]:
            return -1
        if n % 8 in [1, 7]:
            return 1
    elif a < 0:
        return int((-1)**((n-1)//2) * _jacobi_symbol(-1*a, n))

    if a % 2 == 0:
        return _jacobi_symbol(2, n) * _jacobi_symbol(a // 2, n)
    if a % n != a:
        return _jacobi_symbol(a % n, n)

    if a % 4 == n % 4 == 3:
        return -1 * _jacobi_symbol(n, a) # pylint: disable=arguments-out-of-order
    return _jacobi_symbol(n, a) # pylint: disable=arguments-out-of-order
# pylint: enable=invalid-name,too-many-return-statements

def _D_chooser(num: int) -> int:
    """
    Choose a D value suitable for the Baillie-PSW test
    """
    # pylint: disable=invalid-name
    D = 5
    while _jacobi_symbol(D, num) != -1:
        D += 2 if D > 0 else -2
        D *= -1
    # pylint: enable=invalid-name
    return D

# pylint: disable=invalid-name,too-many-arguments
def _U_V_subscript(k: int, n: int, U: int, V: int, P: int, Q: int, D: int) -> Tuple[int, int]:
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
# pylint: enable=invalid-name,too-many-arguments

def _lucas_pp(num: int) -> bool:
    """
    Perform the Lucas probable prime test

    Returns True if num is probably prime, False if n is composite
    """
    if num == 2:
        return True

    # pylint: disable=invalid-name
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

    # pylint: disable=no-else-return
    if U == 0:
        return True
    else: # pragma: no cover
        for r in range(s):
            U, V = (U*V) % num, (pow(V, 2, num) - 2*pow(Q, d*(2**r), num)) % num
            if V == 0:
                return True

        return False
    # pylint: enable=no-else-return
    # pylint: enable=invalid-name

def is_prime(num: int, primes: Optional[Sequence[int]] = None) -> bool:
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
        if primes[-1] >= num**0.5:
            # If it's prime, none of the primes up to its square root will be a factor of it
            return _trial_division(num, primes)

    if not _trial_division(num, [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]):
        return False

    return _miller_rabin_2(num) and _lucas_pp(num)

def n_primes(num: int, primes: Optional[Sequence[int]] = None) -> Sequence[int]:
    """
    Returns the first num primes

    Can pass in known primes to decrease execution time
    """
    primes = primes or Primes()

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

def nth_prime(num: int, primes: Optional[Sequence[int]] = None) -> int:
    """
    Returns the numth prime (e.g. the 3rd prime, the 6th prime)

    Can pass in known primes to decrease execution time
    """
    return n_primes(num, primes)[-1]

def composites_up_to(limit: int, primes: Optional[Sequence[int]] = None) -> Sequence[int]:
    """
    Returns all composite (non-prime greater than 1) numbers up to (and including) limit

    Can pass in known primes to decrease execution time
    """
    primes = primes_up_to(limit, primes)
    composites: List[int] = []
    for prime1, prime2 in zip(primes, primes[1:]):
        # Add numbers between primes to composites
        composites.extend(range(prime1+1, prime2))
    if primes:
        # Add numbers between last prime and x
        composites.extend(range(primes[-1]+1, limit+1))
    return composites

def next_prime(primes: Sequence[int]) -> int:
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

    raise RuntimeError("Unreachable code") # pragma: no cover

def primes_with_difference_up_to(limit: int, difference: int,
                                 primes: Optional[Sequence[int]] = None) -> Iterable[Tuple[int, int]]:
    """
    Primes with difference up to limit
    """
    primes = primes or Primes()

    return ((prime, prime+difference) for prime in primes_up_to(limit-difference, primes)
            if is_prime(prime+difference, primes))

def twin_primes_up_to(limit: int, primes: Optional[Sequence[int]] = None) -> Iterable[Tuple[int, int]]:
    """
    Primes with difference 2 up to limit
    """
    return primes_with_difference_up_to(limit, 2, primes)

def cousin_primes_up_to(limit: int, primes: Optional[Sequence[int]] = None) -> Iterable[Tuple[int, int]]:
    """
    Primes with difference 4 up to limit
    """
    return primes_with_difference_up_to(limit, 4, primes)

def sexy_primes_up_to(limit: int, primes: Optional[Sequence[int]] = None) -> Iterable[Tuple[int, int]]:
    """
    Primes with difference 6 up to limit
    """
    return primes_with_difference_up_to(limit, 6, primes)

def prime_triplets_up_to(limit: int, primes: Optional[Sequence[int]] = None) -> Iterable[Tuple[int, int, int]]:
    """
    Prime triplets up to limit
    """
    primes = primes or Primes()

    for prime in primes_up_to(limit-6, primes):
        if is_prime(prime+2, primes) and is_prime(prime+6, primes):
            yield (prime, prime+2, prime+6)
        if is_prime(prime+4, primes) and is_prime(prime+6, primes):
            yield (prime, prime+4, prime+6)

def prime_quadruplets_up_to(limit: int, primes: Optional[Sequence[int]] = None) -> Iterable[Tuple[int, int, int, int]]:
    """
    Prime quadruplets up to limit
    """
    primes = primes or Primes()

    for prime in primes_up_to(limit-8, primes):
        if is_prime(prime+2, primes) and is_prime(prime+6, primes) and is_prime(prime+8, primes):
            yield (prime, prime+2, prime+6, prime+8)

def prime_gaps_up_to(limit: int, primes: Optional[Sequence[int]] = None) -> Iterable[int]:
    """
    Difference between successive primes up to limit
    """
    primes = primes_up_to(limit, primes)
    for prime1, prime2 in zip(primes, primes[1:]):
        yield prime2 - prime1

def brents_rho(num: int, starting_point: int = 2) -> int:
    """
    Return a factor of num using Brent's variant of Pollard's rho algorithm, or num if one is not found
    """
    # pylint: disable=invalid-name
    y, m = starting_point, 1000 # http://xn--2-umb.com/09/12/brent-pollard-rho-factorisation suggests 1000 is optimal
    g, r, q = 1, 1, 1

    while g == 1:
        x = y
        for _ in range(r):
            y = (pow(y, 2, num) + 1) % num

        k = 0
        while k < r and g == 1:
            ys = y
            for _ in range(min(m, r-k)):
                y = (pow(y, 2, num) + 1) % num
                q = q * (abs(x-y)) % num
            g = gcd(q, num)
            k += m

        r *= 2

    if g != num:
        return g

    g = 1
    while g == 1:
        ys = (pow(ys, 2, num) + 1) % num
        g = gcd(abs(x - ys), num)
    # pylint: enable=invalid-name

    return g

def factorise(num: int, include_trivial: bool = False, primes: Optional[Sequence[int]] = None) -> Set[int]:
    """
    Factorise a number

    Returns the prime factors of num
    Excludes trivial factors unless include_trivial = True
    """
    primes = primes or Primes()

    factors = set([1, num]) if include_trivial else set()

    if is_prime(num, primes):
        return factors

    if primes:
        sqrt_num = num ** 0.5
        for prime in primes:
            if prime > sqrt_num or is_prime(num, primes):
                break
            if num % prime == 0:
                factors.add(prime)
                while num % prime == 0:
                    num //= prime
                sqrt_num = num ** 0.5

    while num > 1 and not is_prime(num, primes):
        starting_point = 2
        factor = brents_rho(num, starting_point)
        while factor == num:
            factor = brents_rho(num, starting_point)
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
