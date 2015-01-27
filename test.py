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
            passInL = primes.primesUpTo(random.randint(0, i))
            self.assertEqual(primes.primesUpTo(i), primes.primesUpTo(i, passInL))

    def testPrimesUpTo1000WithGreaterPassIn(self):
        for i in range(1000):
            passInG = primes.primesUpTo(random.randint(i, 2*i))
            self.assertEqual(primes.primesUpTo(i), primes.primesUpTo(i, passInG))

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
    def testNPrimes0(self):
        self.assertEqual(primes.nPrimes(0), [])

    def testNPrimes1(self):
        self.assertEqual(primes.nPrimes(1), [2])

    def testNPrimes2(self):
        self.assertEqual(primes.nPrimes(2), [2, 3])

    def testNPrimes5(self):
        self.assertEqual(primes.nPrimes(5), [2, 3, 5, 7, 11])

    def testNPrimes100(self):
        self.assertEqual(primes.nPrimes(100), primes.primesUpTo(542))

    def testNPrimes500(self):
        for i in range(500):
            p = primes.primesUpTo(i)
            self.assertEqual(primes.nPrimes(len(p)), p)
    
    def testNPrimes1000(self):
        for i in range(1000):
            self.assertEqual(len(primes.nPrimes(i)), i)

    def testNPrimes10000(self):
        for i in range(10000, 10050):
            self.assertEqual(len(primes.nPrimes(i)), i)

class TestNthPrime(unittest.TestCase):
    def setUp(self):
        self.pri = primes.primesUpTo(1000)

    def testNthPrime1000(self):
        for i in range(1, len(self.pri)):
            self.assertEqual(primes.nthPrime(i), self.pri[i-1])

class TestCompositesUpTo(unittest.TestCase):
    def testCompositesUpTo0(self):
        self.assertEqual(primes.compositesUpTo(0), [])
    
    def testCompositesUpTo3(self):
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

class TestTwinPrimesUpTo(unittest.TestCase):
    def testTwinPrimesUpTo4(self):
        self.assertEqual(list(primes.twinPrimesUpTo(4)), [])

    def testTwinPrimesUpTo5(self):
        self.assertEqual(list(primes.twinPrimesUpTo(5)), [(3, 5)])

    def testTwinPrimesUpTo6(self):
        self.assertEqual(list(primes.twinPrimesUpTo(6)), [(3, 5)])

    def testTwinPrimesUpTo7(self):
        self.assertEqual(list(primes.twinPrimesUpTo(7)), [(3, 5), (5, 7)])

    def testTwinPrimesUpTo13(self):
        self.assertEqual(list(primes.twinPrimesUpTo(13)), [(3, 5), (5, 7), (11, 13)])

    def testTwinPrimesUpTo31(self):
        self.assertEqual(list(primes.twinPrimesUpTo(31)), [(3, 5), (5, 7), (11, 13), (17, 19), (29, 31)])

    def testTwinPrimesUpTo73(self):
        self.assertEqual(list(primes.twinPrimesUpTo(73)), [(3, 5), (5, 7), (11, 13), (17, 19), (29, 31), (41, 43), (59, 61), (71, 73)])

    def testTwinPrimesUpTo139(self):
        self.assertEqual(list(primes.twinPrimesUpTo(139)), [(3, 5), (5, 7), (11, 13), (17, 19), (29, 31), (41, 43), (59, 61), (71, 73), (101, 103), (107, 109), (137, 139)])

    def testTwinPrimesUpTo620(self):
        self.assertEqual(list(primes.twinPrimesUpTo(620)), [(3, 5), (5, 7), (11, 13), (17, 19), (29, 31), (41, 43), (59, 61), (71, 73), (101, 103), (107, 109), (137, 139), (149, 151), (179, 181), (191, 193), (197, 199), (227, 229), (239, 241), (269, 271), (281, 283), (311, 313), (347, 349), (419, 421), (431, 433), (461, 463), (521, 523), (569, 571), (599, 601), (617, 619)])

    def testTwinPrimesWithPassIn(self):
        upto = 500
        p = primes.primesUpTo(upto)
        for i in range(upto):
            self.assertEqual(list(primes.twinPrimesUpTo(i)), list(primes.twinPrimesUpTo(i, p[:random.randint(0, upto)])))

class TestCousinPrimesUpTo(unittest.TestCase):
    def testCousinPrimesUpTo6(self):
        self.assertEqual(list(primes.cousinPrimesUpTo(6)), [])

    def testCousinPrimesUpTo7(self):
        self.assertEqual(list(primes.cousinPrimesUpTo(7)), [(3, 7)])

    def testCousinPrimesUpTo17(self):
        self.assertEqual(list(primes.cousinPrimesUpTo(17)), [(3, 7), (7, 11), (13, 17)])

    def testCousinPrimesUpTo101(self):
        self.assertEqual(list(primes.cousinPrimesUpTo(101)), [(3, 7), (7, 11), (13, 17), (19, 23), (37, 41), (43, 47), (67, 71), (79, 83), (97, 101)])

    def testCousinPrimesUpTo617(self):
        self.assertEqual(len(list(primes.cousinPrimesUpTo(617))), 28)

    def testCousinPrimesUpTo971(self):
        self.assertEqual(len(list(primes.cousinPrimesUpTo(971))), 41)

    def testCousinPrimesWithPassIn(self):
        upto = 500
        p = primes.primesUpTo(upto)
        for i in range(upto):
            self.assertEqual(list(primes.cousinPrimesUpTo(i)), list(primes.cousinPrimesUpTo(i, p[:random.randint(0, upto)])))
            
class TestSexyPrimesUpTo(unittest.TestCase):
    def testSexyPrimesUpTo10(self):
        self.assertEqual(list(primes.sexyPrimesUpTo(10)), [])

    def testSexyPrimesUpTo11(self):
        self.assertEqual(list(primes.sexyPrimesUpTo(11)), [(5, 11)])

    def testSexyPrimesUpTo37(self):
        self.assertEqual(list(primes.sexyPrimesUpTo(37)), [(5,11), (7,13), (11,17), (13,19), (17,23), (23,29), (31,37)])

    def testSexyPrimesUpTo199(self):
        self.assertEqual(list(primes.sexyPrimesUpTo(199)), [(5,11), (7,13), (11,17), (13,19), (17,23), (23,29), (31,37), (37,43), (41,47), (47,53), (53,59), (61,67), (67,73), (73,79), (83,89), (97,103), (101,107), (103,109), (107,113), (131,137), (151,157), (157,163), (167,173), (173,179), (191,197), (193,199)])
        
    def testSexyPrimesUpTo467(self):
        self.assertEqual(list(primes.sexyPrimesUpTo(467)), [(5,11), (7,13), (11,17), (13,19), (17,23), (23,29), (31,37), (37,43), (41,47), (47,53), (53,59), (61,67), (67,73), (73,79), (83,89), (97,103), (101,107), (103,109), (107,113), (131,137), (151,157), (157,163), (167,173), (173,179), (191,197), (193,199), (223,229), (227,233), (233,239), (251,257), (257,263), (263,269), (271,277), (277,283), (307,313), (311,317), (331,337), (347,353), (353,359), (367,373), (373,379), (383,389), (433,439), (443,449), (457,463), (461,467)])

    def testSexyPrimesWithPassIn(self):
        upto = 500
        p = primes.primesUpTo(upto)
        for i in range(upto):
            self.assertEqual(list(primes.sexyPrimesUpTo(i)), list(primes.sexyPrimesUpTo(i, p[:random.randint(0, upto)])))
            
class TestPrimeTripletsUpTo(unittest.TestCase):
    def testPrimeTripletsUpTo10(self):
        self.assertEqual(list(primes.primeTripletsUpTo(10)), [])
        
    def testPrimeTripletsUpTo11(self):
        self.assertEqual(list(primes.primeTripletsUpTo(11)), [(5, 7, 11)])

    def testPrimeTripletsUpTo109(self):
        self.assertEqual(list(primes.primeTripletsUpTo(109)), [(5, 7, 11), (7, 11, 13), (11, 13, 17), (13, 17, 19), (17, 19, 23), (37, 41, 43), (41, 43, 47), (67, 71, 73), (97, 101, 103), (101, 103, 107), (103, 107, 109)])

    def testPrimeTripletsUpTo467(self):
        self.assertEqual(list(primes.primeTripletsUpTo(467)), [(5, 7, 11), (7, 11, 13), (11, 13, 17), (13, 17, 19), (17, 19, 23), (37, 41, 43), (41, 43, 47), (67, 71, 73), (97, 101, 103), (101, 103, 107), (103, 107, 109), (107, 109, 113), (191, 193, 197), (193, 197, 199), (223, 227, 229), (227, 229, 233), (277, 281, 283), (307, 311, 313), (311, 313, 317), (347, 349, 353), (457, 461, 463), (461, 463, 467)])

    def testPrimeTripletsUpTo887(self):
        self.assertEqual(list(primes.primeTripletsUpTo(887)), [(5, 7, 11), (7, 11, 13), (11, 13, 17), (13, 17, 19), (17, 19, 23), (37, 41, 43), (41, 43, 47), (67, 71, 73), (97, 101, 103), (101, 103, 107), (103, 107, 109), (107, 109, 113), (191, 193, 197), (193, 197, 199), (223, 227, 229), (227, 229, 233), (277, 281, 283), (307, 311, 313), (311, 313, 317), (347, 349, 353), (457, 461, 463), (461, 463, 467), (613, 617, 619), (641, 643, 647), (821, 823, 827), (823, 827, 829), (853, 857, 859), (857, 859, 863), (877, 881, 883), (881, 883, 887)])

    def testPrimeTripletsWithPassIn(self):
        upto = 500
        p = primes.primesUpTo(upto)
        for i in range(upto):
            self.assertEqual(list(primes.primeTripletsUpTo(i)), list(primes.primeTripletsUpTo(i, p[:random.randint(0, upto)])))
            
class TestPrimeQuadrupletsUpTo(unittest.TestCase):
    def testPrimeQuadrupletsUpTo12(self):
        self.assertEqual(list(primes.primeQuadrupletsUpTo(12)), [])

    def testPrimeQuadrupletsUpTo13(self):
        self.assertEqual(list(primes.primeQuadrupletsUpTo(13)), [(5, 7, 11, 13)])

    def testPrimeQuadrupletsUpTo829(self):
        self.assertEqual(list(primes.primeQuadrupletsUpTo(829)), [(5, 7, 11, 13), (11, 13, 17, 19), (101, 103, 107, 109), (191, 193, 197, 199), (821, 823, 827, 829)])

    def testPrimeQuadrupletsUpTo2090(self):
        self.assertEqual(list(primes.primeQuadrupletsUpTo(2090)), [(5, 7, 11, 13), (11, 13, 17, 19), (101, 103, 107, 109), (191, 193, 197, 199), (821, 823, 827, 829), (1481, 1483, 1487, 1489), (1871, 1873, 1877, 1879), (2081, 2083, 2087, 2089)])

    def testPrimeQuadrupletsUpTo100000(self):
        self.assertEqual(len(list(primes.primeQuadrupletsUpTo(100000))), 38)

    def testPrimeQuadrupletsWithPassIn(self):
        upto = 500
        p = primes.primesUpTo(upto)
        for i in range(upto):
            self.assertEqual(list(primes.primeQuadrupletsUpTo(i)), list(primes.primeQuadrupletsUpTo(i, p[:random.randint(0, upto)])))

class TestPrimes(unittest.TestCase):
    def setUp(self):
        self.primes = primes.Primes()
    
    def testMembershipSanity(self):
        self.assertFalse(1 in self.primes)
        self.assertTrue(2 in self.primes)
        self.assertTrue(3 in self.primes)
        self.assertFalse(4 in self.primes)
        self.assertTrue(5 in self.primes)
        self.assertFalse(6 in self.primes)
        self.assertTrue(7 in self.primes)
        self.assertFalse(8 in self.primes)
        self.assertFalse(9 in self.primes)
        self.assertFalse(10 in self.primes)

    def testMembership1000(self):
        p = primes.primesUpTo(1000)
        for pr in p:
            self.assertTrue(pr in self.primes)

        c = primes.compositesUpTo(1000, p)
        for co in c:
            self.assertFalse(co in self.primes)

    def testIndexingSanity(self):
        self.assertEqual(self.primes[0], 2)
        self.assertEqual(self.primes[1], 3)
        self.assertEqual(self.primes[2], 5)
        self.assertEqual(self.primes[3], 7)
        self.assertEqual(self.primes[10], 31)
        self.assertEqual(self.primes[100], 547)
        self.assertEqual(self.primes[1000], 7927)

    def testIndexing1000(self):
        p = primes.nPrimes(1000)
        for i, pr in enumerate(p):
            self.assertEqual(self.primes[i], pr)

    def testLen(self):
        self.assertEqual(len(self.primes), 0)
        self.primes[0]
        self.assertEqual(len(self.primes), 1)
        self.primes[1]
        self.assertEqual(len(self.primes), 2)
        self.primes[2]
        self.assertEqual(len(self.primes), 3)
        self.primes[10]
        self.assertEqual(len(self.primes), 11)
        self.primes[150]
        self.assertEqual(len(self.primes), 151)
        self.primes[1234]
        self.assertEqual(len(self.primes), 1235)

    def testIteration(self):
        self.primes[999]
        
        self.assertEqual(primes.nPrimes(1000), list(self.primes))

        self.assertEqual(primes.nPrimes(1000), [prime for prime in self.primes])
        
        for prime in self.primes:
            self.assertTrue(primes.isPrime(prime))

    def testEquality(self):
        otherprimes = primes.Primes()
        self.assertEqual(self.primes, otherprimes)
        self.assertEqual(self.primes, [])
        self.assertNotEqual(self.primes, [2])
        self.assertFalse(self.primes != otherprimes)

        self.primes[0]
        self.assertNotEqual(self.primes, otherprimes)
        self.assertEqual(self.primes, [2])
        self.assertNotEqual(self.primes, [])
        self.assertNotEqual(self.primes, [3])
        self.assertNotEqual(self.primes, [2, 3])
        self.assertFalse(self.primes == otherprimes)

        otherprimes[0]
        self.assertEqual(self.primes, otherprimes)
        self.assertEqual(otherprimes, [2])
        self.assertFalse(self.primes != otherprimes)

        self.primes[100]
        otherprimes[100]
        otherprimes[50]
        self.assertEqual(self.primes, otherprimes)

        self.primes[200]
        self.assertNotEqual(self.primes, otherprimes)

            
if __name__ == '__main__':
    unittest.main()
