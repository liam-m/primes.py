#primes.py

Several prime number functions in Python

If you want to help develop, [open an issue](https://github.com/liam-m/primes.py/issues/new) or [fork the repo](https://github.com/liam-m/primes.py/fork), make your changes and [submit a pull request](https://github.com/liam-m/primes.py/compare/).

##primesUpTo
    
Implementation of Sieve of Eratosthenes

Returns a list of all primes up to (and including) x

Can pass in a list of primes to decrease execution time

### Example usage

```
>>> primesUpTo(10)
[2, 3, 5, 7]

>>> primesUpTo(20, [2, 3, 5, 7])
[2, 3, 5, 7, 11, 13, 17, 19]
```

##isPrime

Returns True if x is a prime number, False if it is not

Can pass in a list of known primes to decrease execution time

### Example usage

```
>>> isPrime(191)
True

>>> isPrime(192)
False
```

##nPrimes

Returns a list of the first n primes

Can pass in a list of known primes to decrease execution time

### Example usage

```
>>> nPrimes(5)
[2, 3, 5, 7, 11]

>>> nPrimes(10, [2, 3, 5, 7, 11])
[2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
```

##nthPrime

Returns the nth prime (i.e. the 3rd prime, the 6th prime)

Can pass in a list of known primes to decrease execution time 

### Example usage

```
>>> nthPrime(1000)
7919

>>> nthPrime(4, [2, 3, 5, 7, 11])
7
```

##compositesUpTo

Returns a list of all composite (non-prime greater than 1) numbers up to (and including) x

Can pass in a list of known primes to decrease execution time

### Example usage

```
>>> compositesUpTo(10)
[4, 6, 8, 9, 10]

>>> compositesUpTo(20, [2, 3, 5, 7, 11, 13, 17, 19, 23])
[4, 6, 8, 9, 10, 12, 14, 15, 16, 18, 20]
```

##nextPrime

Given a list of primes, returns the next prime

Uses method of trial division
    
This is much less efficient than primesUpTo for generating ranges of primes

### Example usage

```
>>> nextPrime([2, 3, 5, 7, 11])
13

>>> nextPrime(primesUpTo(1000000))
1000003
```
