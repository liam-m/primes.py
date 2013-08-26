from binarySearch import binarySearch
from math import sqrt, log
from bisect import bisect_right

def primesUpTo(x, primes = []):
    """
    Implementation of Sieve of Eratosthenes
    
    Returns all primes up to (and including) x

    Can pass in a list of known primes to decrease execution time
    """

    def _posOf(num, offset = 3):
        # Position of number in lst
        return int((num - offset) / 2)

    def _numAt(pos, offset = 3):
        # Number at position in lst e.g. lst[0] refers to 3, lst[2] refers to 7
        return pos * 2 + offset

    if primes == [2]:
        primes = [] # Not particularly useful as we only list odd numbers
    
    if x <= 1: #  No primes <= 1
        return []

    elif x == 3: # Bug fix. May need to change logic in future so this isn't necessary
        return [2, 3]
    
    # Some primes
    # All odd numbers initially assumed prime. Each element in lst refers to an odd number, starting at 3, i.e. lst[0] refers to 3, lst[4] refers to 11
    lst = [True] * int((x-1)/2)
    
    if primes: # Some primes have already been worked out
        
        if primes[-1] >= x: # Enough primes have already been worked out
            return primes[:bisect_right(primes, x)] # Binary search to position of x and return list up to that point
                
        else: # Not all primes up to x have been worked out
            
            for num in primes[1:]: # Skipping 2, go through the primes
                for i in range(_posOf(num**2), len(lst), num): # Mark multiples of the prime above its square as not prime
                    lst[i] = False
            start = _posOf(primes[-1])+1 # Start at the position of the last prime + 1
                    
    else: # No primes worked out
        primes = [2] # Only going to work out odd primes so remember 2 is prime
        start = 0 # Start at 0

    for index in range(start, _posOf(int(sqrt(x)))+1): # Mark multiples of prime <= square root as not prime
        if lst[index]: # If number at index is prime
            num = _numAt(index) # Number index refers to
            primes.append(num) # It is prime, so add it to list of primes
            for i in range(_posOf(num**2), len(lst), num): # Mark multiples of the prime above its square as not prime
                lst[i] = False

    start = max(_posOf(primes[-1]), _posOf(int(sqrt(x)))) + 1

    primes += [_numAt(index) for index in range(start, len(lst)) if lst[index]] # Get the primes above the square root (or above primes[-1])
    
    return primes

def isPrime(x, primes = []):
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

def nPrimes(n, primes = []):
    """
    Returns the first n primes

    Can pass in a list of known primes to decrease execution time
    """
    if n >= 8602:
        upperBound = int(n*log(n) + n*(log(log(n)) - 0.9385))
    elif n >= 6:
        upperBound = int(n * (log(n) + log(log(n))))
    else:
        upperBound = 13
    primes = primesUpTo(upperBound, primes)
    return primes[:n]

def nthPrime(n, primes = []):
    """
    Returns the nth prime (i.e. the 3rd prime, the 6th prime)

    Can pass in a list of known primes to decrease execution time    
    """
    return nPrimes(n, primes)[-1]

def compositesUpTo(x, primes = []):
    """
    Returns all composite (non-prime greater than 1) numbers up to (and including) x

    Can pass in a list of known primes to decrease execution time
    """
    if x <= 3:
        return []
    elif x == 4:
        return [4]
    primes = primesUpTo(x, primes)
    composites = []
    for index in range(len(primes)-1):
        composites += list(range(primes[index]+1, primes[index+1]))
    composites += list(range(composites[-1]+1, x+1))
    return composites
