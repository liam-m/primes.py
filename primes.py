from binarySearch import binarySearch
from math import sqrt, log

def primesUpTo(x, primes = []):
    """
    Implementation of Sieve of Eratosthenes
    
    Returns all primes up to (and including) x

    Can pass in a list of known primes to decrease execution time
    """
    
    if x <= 1: #  No primes <= 1
        return []
    
    else: # Some primes
        lst = [True] * int((x-1)/2) # All odd numbers initially assumed prime. Each element refers to an odd number, starting at 3, i.e. lst[0] refers to 3, lst[4] refers to 11
        
        if primes: # Some primes have already been worked out
            if primes[-1] >= x: # Enough primes have already been worked out
                for index in range(len(primes)): # Return primes up to that number
                    if primes[index] > x:
                        return primes[:index]
                    return primes # All primes are there
            else: # Not all primes up to x have been worked out
                res = primes[:] 
                for num in res[1:]: # Skipping 2, go through the primes
                    for i in range(int((num**2 - 3)/2), len(lst), num): # Mark multiples of the prime as not prime
                        lst[i] = False
                start = int((res[-1] - 3) / 2)+1 # Start at the position of the last prime + 1
                        
        else: # No primes worked out
            res = [2] # Only going to work out odd primes so remember 2 is prime
            start = 0 # Start at 0
        for index in range(start, int((sqrt(x)-3)/2+1)): # Mark multiples of prime <= square root as not prime 
            if lst[index]: # If number at index is prime
                num = index*2 + 3 # Number index refers to is the index*2 + 3 i.e. lst[0] refers to 3, lst[2] refers to 7
                res.append(num) # It is prime, so add it to res
                for i in range(int((num**2 - 3)/2), len(lst), num): # Mark multiples of the prime as not prime
                    lst[i] = False
        res += [index*2+3 for index in range(int((sqrt(x)-3)/2+1), len(lst)) if lst[index]] # Get the primes above the square root
        return res

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
        upperBound = n*log(n) + n*(log(log(n)) - 0.9385)
    elif n >= 6:
        upperBound = n * (log(n) + log(log(n)))
    else:
        upperBound = 13
    upperBound = int(upperBound)
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
    primes = primesUpTo(x, primes)
    composites = []
    for index in range(len(primes)-1):
        composites += list(range(primes[index]+1, primes[index+1]))
    composites += list(range(composites[-1]+1, x+1))
    return composites
