# primes.py

Prime number library for Python 2 and 3

If you want to help develop, [open an issue](https://github.com/liam-m/primes.py/issues/new) or [fork the repo](https://github.com/liam-m/primes.py/fork), make your changes and [submit a pull request](https://github.com/liam-m/primes.py/compare/).

[![Build Status](https://travis-ci.org/liam-m/primes.py.svg?branch=master)](https://travis-ci.org/liam-m/primes.py)

## Primes

A list-like object that automatically generates additional prime numbers as required. Supports membership testing and slicing for sequences of prime numbers

```python
>>> primes = Primes()
>>> 10 in primes
False
>>> 11 in primes
True
>>> primes[10:20]
[31, 37, 41, 43, 47, 53, 59, 61, 67, 71]
>>> primes[15:10:-2]
[53, 43, 37]
>>> primes[100]
547
```

---

There are also a number of functions for prime generation and primality testing:

## primes_up_to
    
Implementation of Sieve of Eratosthenes

Returns all primes up to (and including) x

Can pass in primes to decrease execution time

```python
>>> primes_up_to(10)
[2, 3, 5, 7]

>>> primes_up_to(20, [2, 3, 5, 7])
[2, 3, 5, 7, 11, 13, 17, 19]
```

## is_prime

Returns True if x is a prime number, False if it is not

Can pass in known primes to decrease execution time

```python
>>> is_prime(191)
True

>>> is_prime(192)
False
```

## n_primes

Returns the first n primes

Can pass in known primes to decrease execution time

```python
>>> n_primes(5)
[2, 3, 5, 7, 11]

>>> n_primes(10, [2, 3, 5, 7, 11])
[2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
```

## nth_prime

Returns the n<sup>th</sup> prime (i.e. the 3<sup>rd</sup> prime, the 6<sup>th</sup> prime)

Can pass in known primes to decrease execution time 

```python
>>> nth_prime(1000)
7919

>>> nth_prime(4, [2, 3, 5, 7, 11])
7
```

## composites_up_to

Returns all composite (non-prime greater than 1) numbers up to (and including) x

Can pass in known primes to decrease execution time

```python
>>> composites_up_to(10)
[4, 6, 8, 9, 10]

>>> composites_up_to(20, [2, 3, 5, 7, 11, 13, 17, 19, 23])
[4, 6, 8, 9, 10, 12, 14, 15, 16, 18, 20]
```

## next_prime

Given primes, returns the next prime

Uses method of trial division
    
This is much less efficient than primes_up_to for generating ranges of primes

```python
>>> next_prime([2, 3, 5, 7, 11])
13

>>> next_prime(primesUpTo(1000000))
1000003
```
