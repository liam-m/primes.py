import unittest
import primes
import random
from math import sqrt

class TestPrimesUpTo(unittest.TestCase):
    def testPrimesUpTo0(self):
        self.assertEqual(primes.primesUpTo(0), [])

    def testPrimesUpTo1(self):
        self.assertEqual(primes.primesUpTo(1), [])

    def testPrimesUpTo2(self):
        self.assertEqual(primes.primesUpTo(2), [2])

    def testPrimesUpTo3(self):
        self.assertEqual(primes.primesUpTo(3), [2, 3])

    def testPrimesUpTo4(self):
        self.assertEqual(primes.primesUpTo(4), [2, 3])

    def testPrimesUpTo5(self):
        self.assertEqual(primes.primesUpTo(5), [2, 3, 5])

    def testPrimesUpTo10(self):
        self.assertEqual(primes.primesUpTo(10), [2, 3, 5, 7])

    def testPrimesUpTo100(self):
        self.assertEqual(len(primes.primesUpTo(100)), 25)

    def testPrimesUpTo1000(self):
        self.assertEqual(len(primes.primesUpTo(1000)), 168)

    def testPrimesUpTo10000(self):
        self.assertEqual(len(primes.primesUpTo(10000)), 1229)

    def testPrimesUpTo100000(self):
        self.assertEqual(len(primes.primesUpTo(100000)), 9592)

    def testPrimesUpTo1000000(self):
        self.assertEqual(len(primes.primesUpTo(1000000)), 78498)

    def testPrimesUpTo1000WithLesserPassIn(self):
        for i in range(1000):
            passIn = primes.primesUpTo(random.randint(0, i))
            self.assertEqual(primes.primesUpTo(i), primes.primesUpTo(i, passIn))

    def testPrimesUpTo1000WithGreaterPassIn(self):
        for i in range(1000):
            passIn = primes.primesUpTo(random.randint(i, 2*i))
            self.assertEqual(primes.primesUpTo(i), primes.primesUpTo(i, passIn))

class TestIsPrime(unittest.TestCase):
    def testIsPrime0(self):
        self.assertFalse(primes.isPrime(0))

    def testIsPrime1(self):
        self.assertFalse(primes.isPrime(1))

    def testIsPrime2(self):
        self.assertTrue(primes.isPrime(2))

    def testIsPrime3(self):
        self.assertTrue(primes.isPrime(3))

    def testIsPrime4(self):
        self.assertFalse(primes.isPrime(4))

    def testIsPrime5(self):
        self.assertTrue(primes.isPrime(5))

    def testIsPrime100(self):
        self.assertFalse(primes.isPrime(100))

    def testIsPrimeMersenne(self):
        # 8th Mersenne prime
        self.assertTrue(primes.isPrime(2**31 - 1))

    def testIsPrime0WithPassIn(self):
        self.assertFalse(primes.isPrime(0, [2, 3, 5]))

    def testIsPrime1WithPassIn(self):
        self.assertFalse(primes.isPrime(1, [2, 3, 5]))

    def testIsPrime2WithPassIn(self):
        self.assertTrue(primes.isPrime(2, [2, 3, 5]))

    def testIsPrime3WithPassIn(self):
        self.assertTrue(primes.isPrime(3, [2, 3, 5]))

    def testIsPrime4WithPassIn(self):
        self.assertFalse(primes.isPrime(4, [2, 3, 5]))

    def testIsPrime5WithPassIn(self):
        self.assertTrue(primes.isPrime(5, [2, 3, 5]))

    def testIsPrimeMersenneWithPassInGreaterThanX(self):
        # 7th Mersenne prime
        # Pass in primes > x
        self.assertTrue(primes.isPrime(2**19 - 1, primes.primesUpTo(1.2 * 2**19)))

    def testIsPrimeMersenneWithPassInGreaterThanSqrt(self):
        # 7th Mersenne prime
        # Pass in primes between sqrt(x) and x
        self.assertTrue(primes.isPrime(2**19 - 1, primes.primesUpTo(sqrt(1.2 * 2**19))))
    

class TestNPrimes(unittest.TestCase):
    def testNPrimes1000(self):
        for i in range(1000):
            self.assertEqual(len(primes.nPrimes(i)), i)

class TestNthPrime(unittest.TestCase):
    def setUp(self):
        self.pri = primes.primesUpTo(1000)

    def testNthPrime1000(self):
        for i in range(1, len(self.pri)):
            self.assertEqual(primes.nthPrime(i), self.pri[i-1])

class TestCompositesUpTo(unittest.TestCase):
    def testCompositesUpTo4(self):
        self.assertTrue(all([primes.compositesUpTo(i) == [] for i in range(4)]))

    def testCompositesUpTo4(self):
        self.assertEqual(primes.compositesUpTo(4), [4])

    def testCompositesUpTo5(self):
        self.assertEqual(primes.compositesUpTo(5), [4])

    def testCompositesUpTo6(self):
        self.assertEqual(primes.compositesUpTo(6), [4, 6])

    def testCompositesUpTo20(self):
        self.assertEqual(primes.compositesUpTo(20), [4, 6, 8, 9, 10, 12, 14, 15, 16, 18, 20])

    def testCompositesUpTo100(self):
        self.assertEqual(len(primes.compositesUpTo(100)), 74)

class TestNextPrime(unittest.TestCase):
    def setUp(self):
        self.pri = primes.primesUpTo(10000)

    def testNextPrime10000(self):
        for i in range(len(self.pri)):
            self.assertEqual(primes.nextPrime(self.pri[:i]), self.pri[i])

if __name__ == '__main__':
    unittest.main()
