import unittest
import random
from math import sqrt
from primes import *

# assertRaisesRegex is called assertRaisesRegexp on <3.2
# Monkey patch it in on older versions to avoid DeprecationWarning
if not hasattr(unittest.TestCase, 'assertRaisesRegex'):
    if hasattr(unittest.TestCase, 'assertRaisesRegexp'):
        unittest.TestCase.assertRaisesRegex = unittest.TestCase.assertRaisesRegexp
    else: # assertRaisesRegexp is unavailable on <2.7, so fall back to assertRaises
        unittest.TestCase.assertRaisesRegex = lambda self, e, r, c, *a, **k: self.assertRaises(e, c, *a, **k)

class TestPrimesUpTo(unittest.TestCase):
    def testPrimesUpTo0(self):
        self.assertEqual(primes_up_to(0), [])

    def testPrimesUpTo1(self):
        self.assertEqual(primes_up_to(1), [])

    def testPrimesUpTo2(self):
        self.assertEqual(primes_up_to(2), [2])

    def testPrimesUpTo3(self):
        self.assertEqual(primes_up_to(3), [2, 3])

    def testPrimesUpTo4(self):
        self.assertEqual(primes_up_to(4), [2, 3])

    def testPrimesUpTo5(self):
        self.assertEqual(primes_up_to(5), [2, 3, 5])

    def testPrimesUpTo10(self):
        self.assertEqual(primes_up_to(10), [2, 3, 5, 7])

    def testPrimesUpTo100(self):
        self.assertEqual(len(primes_up_to(100)), 25)

    def testPrimesUpTo1000(self):
        self.assertEqual(len(primes_up_to(1000)), 168)

    def testPrimesUpTo10000(self):
        self.assertEqual(len(primes_up_to(10000)), 1229)

    def testPrimesUpTo100000(self):
        self.assertEqual(len(primes_up_to(100000)), 9592)

    def testPrimesUpTo1000000(self):
        self.assertEqual(len(primes_up_to(1000000)), 78498)

    def testPrimesUpTo1000WithLesserPassIn(self):
        for i in range(1000):
            lower_primes = primes_up_to(random.randint(0, i))
            self.assertEqual(primes_up_to(i), primes_up_to(i, lower_primes))

    def testPrimesUpTo1000WithGreaterPassIn(self):
        for i in range(1000):
            greater_primes = primes_up_to(random.randint(i, 2*i))
            self.assertEqual(primes_up_to(i), primes_up_to(i, greater_primes))

class TestIsPrime(unittest.TestCase):
    def testIsPrime0(self):
        self.assertFalse(is_prime(0))

    def testIsPrime1(self):
        self.assertFalse(is_prime(1))

    def testIsPrime2(self):
        self.assertTrue(is_prime(2))

    def testIsPrime3(self):
        self.assertTrue(is_prime(3))

    def testIsPrime4(self):
        self.assertFalse(is_prime(4))

    def testIsPrime5(self):
        self.assertTrue(is_prime(5))

    def testIsPrime100(self):
        self.assertFalse(is_prime(100))

    def testIsPrime40000(self):
        known_primes = primes_up_to(40000)
        for p in known_primes:
            self.assertTrue(is_prime(p))

        for p in known_primes:
            self.assertTrue(is_prime(p, known_primes[:random.randint(0, len(known_primes)-1)]))

    def testIsPrime40000Composites(self):
        known_composites = composites_up_to(40000)
        known_primes = primes_up_to(40000)
        for c in known_composites:
            self.assertFalse(is_prime(c))

        for c in known_composites:
            self.assertFalse(is_prime(c, known_primes[:random.randint(0, len(known_primes)-1)]))

    def testIsPrimeMersenne(self):
        for n in [2, 3, 5, 7, 13, 17, 19, 31]:
            self.assertTrue(is_prime(2**n - 1))

    def testIsPrimeFermat(self):
        for n in [0, 1, 2, 3, 4]:
            self.assertTrue(is_prime(2**(2**n) + 1))

        self.assertFalse(is_prime(2**32 + 1))

    def testIsPrimeWagstaff(self):
        for n in [3, 5, 7, 11, 13, 17, 19, 23, 31, 43]:
            self.assertTrue(is_prime((2**n + 1)//3))

    def testIsPrimeWoodall(self):
        for n in [2, 3, 6, 30]:
            self.assertTrue(is_prime(n * 2**n - 1))

    def testIsPrimeProth(self):
        self.assertTrue(all(map(is_prime, [3, 5, 13, 17, 41, 97, 113, 193, 241, 257, 353, 449, 577, 641, 673, 769, 929, 1153, 1217, 1409, 1601, 2113, 2689, 2753, 3137, 3329, 3457, 4481, 4993, 6529, 7297, 7681, 7937, 9473, 9601, 9857])))

    def testIsPrimeSolinas(self):
        self.assertTrue(all(map(is_prime, [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 47, 59, 61, 67, 71, 73, 79, 97])))

    def testIsPrime0WithPassIn(self):
        self.assertFalse(is_prime(0, [2, 3, 5]))

    def testIsPrime1WithPassIn(self):
        self.assertFalse(is_prime(1, [2, 3, 5]))

    def testIsPrime2WithPassIn(self):
        self.assertTrue(is_prime(2, [2, 3, 5]))

    def testIsPrime3WithPassIn(self):
        self.assertTrue(is_prime(3, [2, 3, 5]))

    def testIsPrime4WithPassIn(self):
        self.assertFalse(is_prime(4, [2, 3, 5]))

    def testIsPrime5WithPassIn(self):
        self.assertTrue(is_prime(5, [2, 3, 5]))

    def testIsPrimeMersenneWithPassInGreaterThanX(self):
        # 7th Mersenne prime
        # Pass in primes > x
        self.assertTrue(is_prime(int(2**19) - 1, primes_up_to(int(1.2 * 2**19))))

    def testIsPrimeMersenneWithPassInGreaterThanSqrt(self):
        # 7th Mersenne prime
        # Pass in primes between sqrt(x) and x
        self.assertTrue(is_prime(int(2**19) - 1, primes_up_to(int(sqrt(1.2 * 2**19)))))


class TestNPrimes(unittest.TestCase):
    def testNPrimes0(self):
        self.assertEqual(n_primes(0), [])

    def testNPrimes1(self):
        self.assertEqual(n_primes(1), [2])

    def testNPrimes2(self):
        self.assertEqual(n_primes(2), [2, 3])

    def testNPrimes5(self):
        self.assertEqual(n_primes(5), [2, 3, 5, 7, 11])

    def testNPrimes100(self):
        self.assertEqual(n_primes(100), primes_up_to(542))

    def testNPrimes500(self):
        for i in range(500):
            p = primes_up_to(i)
            self.assertEqual(n_primes(len(p)), p)

    def testNPrimes1000(self):
        for i in range(1000):
            self.assertEqual(len(n_primes(i)), i)

    def testNPrimes10000(self):
        for i in range(10000, 10050):
            self.assertEqual(len(n_primes(i)), i)

    def testNPrimes16000(self):
        for i in range(16000, 16005):
            self.assertEqual(len(n_primes(i)), i)

    def testNPrimes40000(self):
        for i in range(40000, 40005):
            self.assertEqual(len(n_primes(i)), i)

class TestNthPrime(unittest.TestCase):
    def testNthPrime1000(self):
        known_primes = primes_up_to(1000)
        for i in range(1, len(known_primes)):
            self.assertEqual(nth_prime(i), known_primes[i-1])

class TestCompositesUpTo(unittest.TestCase):
    def testCompositesUpTo0(self):
        self.assertEqual(composites_up_to(0), [])

    def testCompositesUpTo3(self):
        self.assertTrue(all([composites_up_to(i) == [] for i in range(4)]))

    def testCompositesUpTo4(self):
        self.assertEqual(composites_up_to(4), [4])

    def testCompositesUpTo5(self):
        self.assertEqual(composites_up_to(5), [4])

    def testCompositesUpTo6(self):
        self.assertEqual(composites_up_to(6), [4, 6])

    def testCompositesUpTo20(self):
        self.assertEqual(composites_up_to(20), [4, 6, 8, 9, 10, 12, 14, 15, 16, 18, 20])

    def testCompositesUpTo100(self):
        self.assertEqual(len(composites_up_to(100)), 74)

class TestNextPrime(unittest.TestCase):
    def testNextPrime10000(self):
        known_primes = primes_up_to(10000)
        for i in range(len(known_primes)):
            self.assertEqual(next_prime(known_primes[:i]), known_primes[i])

class TestTwinPrimesUpTo(unittest.TestCase):
    def testTwinPrimesUpTo4(self):
        self.assertEqual(list(twin_primes_up_to(4)), [])

    def testTwinPrimesUpTo5(self):
        self.assertEqual(list(twin_primes_up_to(5)), [(3, 5)])

    def testTwinPrimesUpTo6(self):
        self.assertEqual(list(twin_primes_up_to(6)), [(3, 5)])

    def testTwinPrimesUpTo7(self):
        self.assertEqual(list(twin_primes_up_to(7)), [(3, 5), (5, 7)])

    def testTwinPrimesUpTo13(self):
        self.assertEqual(list(twin_primes_up_to(13)), [(3, 5), (5, 7), (11, 13)])

    def testTwinPrimesUpTo31(self):
        self.assertEqual(list(twin_primes_up_to(31)), [(3, 5), (5, 7), (11, 13), (17, 19), (29, 31)])

    def testTwinPrimesUpTo73(self):
        self.assertEqual(list(twin_primes_up_to(73)), [(3, 5), (5, 7), (11, 13), (17, 19), (29, 31), (41, 43), (59, 61), (71, 73)])

    def testTwinPrimesUpTo139(self):
        self.assertEqual(list(twin_primes_up_to(139)), [(3, 5), (5, 7), (11, 13), (17, 19), (29, 31), (41, 43), (59, 61), (71, 73), (101, 103), (107, 109), (137, 139)])

    def testTwinPrimesUpTo620(self):
        self.assertEqual(list(twin_primes_up_to(620)), [(3, 5), (5, 7), (11, 13), (17, 19), (29, 31), (41, 43), (59, 61), (71, 73), (101, 103), (107, 109), (137, 139), (149, 151), (179, 181), (191, 193), (197, 199), (227, 229), (239, 241), (269, 271), (281, 283), (311, 313), (347, 349), (419, 421), (431, 433), (461, 463), (521, 523), (569, 571), (599, 601), (617, 619)])

    def testTwinPrimesWithPassIn(self):
        upto = 500
        p = primes_up_to(upto)
        for i in range(upto):
            self.assertEqual(list(twin_primes_up_to(i)), list(twin_primes_up_to(i, p[:random.randint(0, upto)])))

class TestCousinPrimesUpTo(unittest.TestCase):
    def testCousinPrimesUpTo6(self):
        self.assertEqual(list(cousin_primes_up_to(6)), [])

    def testCousinPrimesUpTo7(self):
        self.assertEqual(list(cousin_primes_up_to(7)), [(3, 7)])

    def testCousinPrimesUpTo17(self):
        self.assertEqual(list(cousin_primes_up_to(17)), [(3, 7), (7, 11), (13, 17)])

    def testCousinPrimesUpTo101(self):
        self.assertEqual(list(cousin_primes_up_to(101)), [(3, 7), (7, 11), (13, 17), (19, 23), (37, 41), (43, 47), (67, 71), (79, 83), (97, 101)])

    def testCousinPrimesUpTo617(self):
        self.assertEqual(len(list(cousin_primes_up_to(617))), 28)

    def testCousinPrimesUpTo971(self):
        self.assertEqual(len(list(cousin_primes_up_to(971))), 41)

    def testCousinPrimesWithPassIn(self):
        upto = 500
        p = primes_up_to(upto)
        for i in range(upto):
            self.assertEqual(list(cousin_primes_up_to(i)), list(cousin_primes_up_to(i, p[:random.randint(0, upto)])))

class TestSexyPrimesUpTo(unittest.TestCase):
    def testSexyPrimesUpTo10(self):
        self.assertEqual(list(sexy_primes_up_to(10)), [])

    def testSexyPrimesUpTo11(self):
        self.assertEqual(list(sexy_primes_up_to(11)), [(5, 11)])

    def testSexyPrimesUpTo37(self):
        self.assertEqual(list(sexy_primes_up_to(37)), [(5,11), (7,13), (11,17), (13,19), (17,23), (23,29), (31,37)])

    def testSexyPrimesUpTo199(self):
        self.assertEqual(list(sexy_primes_up_to(199)), [(5,11), (7,13), (11,17), (13,19), (17,23), (23,29), (31,37), (37,43), (41,47), (47,53), (53,59), (61,67), (67,73), (73,79), (83,89), (97,103), (101,107), (103,109), (107,113), (131,137), (151,157), (157,163), (167,173), (173,179), (191,197), (193,199)])

    def testSexyPrimesUpTo467(self):
        self.assertEqual(list(sexy_primes_up_to(467)), [(5,11), (7,13), (11,17), (13,19), (17,23), (23,29), (31,37), (37,43), (41,47), (47,53), (53,59), (61,67), (67,73), (73,79), (83,89), (97,103), (101,107), (103,109), (107,113), (131,137), (151,157), (157,163), (167,173), (173,179), (191,197), (193,199), (223,229), (227,233), (233,239), (251,257), (257,263), (263,269), (271,277), (277,283), (307,313), (311,317), (331,337), (347,353), (353,359), (367,373), (373,379), (383,389), (433,439), (443,449), (457,463), (461,467)])

    def testSexyPrimesWithPassIn(self):
        upto = 500
        p = primes_up_to(upto)
        for i in range(upto):
            self.assertEqual(list(sexy_primes_up_to(i)), list(sexy_primes_up_to(i, p[:random.randint(0, upto)])))

class TestPrimeTripletsUpTo(unittest.TestCase):
    def testPrimeTripletsUpTo10(self):
        self.assertEqual(list(prime_triplets_up_to(10)), [])

    def testPrimeTripletsUpTo11(self):
        self.assertEqual(list(prime_triplets_up_to(11)), [(5, 7, 11)])

    def testPrimeTripletsUpTo109(self):
        self.assertEqual(list(prime_triplets_up_to(109)), [(5, 7, 11), (7, 11, 13), (11, 13, 17), (13, 17, 19), (17, 19, 23), (37, 41, 43), (41, 43, 47), (67, 71, 73), (97, 101, 103), (101, 103, 107), (103, 107, 109)])

    def testPrimeTripletsUpTo467(self):
        self.assertEqual(list(prime_triplets_up_to(467)), [(5, 7, 11), (7, 11, 13), (11, 13, 17), (13, 17, 19), (17, 19, 23), (37, 41, 43), (41, 43, 47), (67, 71, 73), (97, 101, 103), (101, 103, 107), (103, 107, 109), (107, 109, 113), (191, 193, 197), (193, 197, 199), (223, 227, 229), (227, 229, 233), (277, 281, 283), (307, 311, 313), (311, 313, 317), (347, 349, 353), (457, 461, 463), (461, 463, 467)])

    def testPrimeTripletsUpTo887(self):
        self.assertEqual(list(prime_triplets_up_to(887)), [(5, 7, 11), (7, 11, 13), (11, 13, 17), (13, 17, 19), (17, 19, 23), (37, 41, 43), (41, 43, 47), (67, 71, 73), (97, 101, 103), (101, 103, 107), (103, 107, 109), (107, 109, 113), (191, 193, 197), (193, 197, 199), (223, 227, 229), (227, 229, 233), (277, 281, 283), (307, 311, 313), (311, 313, 317), (347, 349, 353), (457, 461, 463), (461, 463, 467), (613, 617, 619), (641, 643, 647), (821, 823, 827), (823, 827, 829), (853, 857, 859), (857, 859, 863), (877, 881, 883), (881, 883, 887)])

    def testPrimeTripletsWithPassIn(self):
        upto = 500
        p = primes_up_to(upto)
        for i in range(upto):
            self.assertEqual(list(prime_triplets_up_to(i)), list(prime_triplets_up_to(i, p[:random.randint(0, upto)])))

class TestPrimeQuadrupletsUpTo(unittest.TestCase):
    def testPrimeQuadrupletsUpTo12(self):
        self.assertEqual(list(prime_quadruplets_up_to(12)), [])

    def testPrimeQuadrupletsUpTo13(self):
        self.assertEqual(list(prime_quadruplets_up_to(13)), [(5, 7, 11, 13)])

    def testPrimeQuadrupletsUpTo829(self):
        self.assertEqual(list(prime_quadruplets_up_to(829)), [(5, 7, 11, 13), (11, 13, 17, 19), (101, 103, 107, 109), (191, 193, 197, 199), (821, 823, 827, 829)])

    def testPrimeQuadrupletsUpTo2090(self):
        self.assertEqual(list(prime_quadruplets_up_to(2090)), [(5, 7, 11, 13), (11, 13, 17, 19), (101, 103, 107, 109), (191, 193, 197, 199), (821, 823, 827, 829), (1481, 1483, 1487, 1489), (1871, 1873, 1877, 1879), (2081, 2083, 2087, 2089)])

    def testPrimeQuadrupletsUpTo100000(self):
        self.assertEqual(len(list(prime_quadruplets_up_to(100000))), 38)

    def testPrimeQuadrupletsWithPassIn(self):
        upto = 500
        p = primes_up_to(upto)
        for i in range(upto):
            self.assertEqual(list(prime_quadruplets_up_to(i)), list(prime_quadruplets_up_to(i, p[:random.randint(0, upto)])))

class TestPrimes(unittest.TestCase):
    def setUp(self):
        self.primes = Primes()

    def testMembershipSanity(self):
        for _ in range(5):
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

    def testMembership10000(self):
        p = primes_up_to(10000)
        for pr in p:
            self.assertTrue(pr in self.primes)

        c = composites_up_to(10000, p)
        for co in c:
            self.assertFalse(co in self.primes)

    def testMembership15000(self):
        p = primes_up_to(15000)
        for pr in p[::-1]:
            self.assertTrue(pr in self.primes)

        c = composites_up_to(15000, p)
        for co in c[::-1]:
            self.assertFalse(co in self.primes)

    def testIndexingSanity(self):
        self.assertEqual(self.primes[0], 2)
        self.assertEqual(self.primes[1], 3)
        self.assertEqual(self.primes[2], 5)
        self.assertEqual(self.primes[3], 7)
        self.assertEqual(self.primes[10], 31)
        self.assertEqual(self.primes[100], 547)
        self.assertEqual(self.primes[1000], 7927)
        self.assertEqual(self.primes[-1], 7927)

    def testIndexing1000(self):
        p = n_primes(1000)
        for i, pr in enumerate(p):
            self.assertEqual(self.primes[i], pr)

    def testSlicing(self):
        self.assertRaises(TypeError, lambda p: p[1,2,3], self.primes)
        self.assertEqual(self.primes[:1], [2])
        self.assertEqual(self.primes[0:2], [2, 3])
        self.assertEqual(self.primes[:2], [2, 3])
        self.assertEqual(self.primes[0:2:1], [2, 3])
        self.assertEqual(self.primes[::1], [2, 3])
        self.assertEqual(self.primes[1:], [3])
        self.assertEqual(self.primes[1::1], [3])
        self.assertEqual(self.primes[1:5:2], [3, 7])
        self.assertEqual(self.primes[::2], [2, 5, 11])
        self.assertEqual(self.primes[:], [2, 3, 5, 7, 11])
        self.assertEqual(self.primes[::-1], [11, 7, 5, 3, 2])
        self.assertEqual(self.primes[::-2], [11, 5, 2])
        self.assertEqual(self.primes[2::1], [5, 7, 11])
        self.assertEqual(self.primes[:3:1], [2, 3, 5])
        self.assertEqual(self.primes[:5:2], [2, 5, 11])

    def testSlicing5000(self):
        p = n_primes(1000)
        for _ in range(5000):
            start = None if random.randint(0, 1) == 0 else random.randint(0, 999)
            stop = random.randint(0, 999) # self.primes not guaranteed to have 1000 elements so passing in None could fail
            step = None if random.randint(0, 1) == 0 else random.randint(1, 100)
            self.assertEqual(self.primes[start:stop:step], p[start:stop:step], ' '.join(map(str, [start, stop, step])))

    def testSlicing1000Pos(self):
        p = n_primes(1000)
        for _ in range(1000):
            start = random.randint(0, 700)
            stop = random.randint(start, 999)
            step = random.randint(1, 100)
            self.assertEqual(self.primes[start:stop:step], p[start:stop:step])

    def testSlicing1000Neg(self):
        p = n_primes(1000)
        for _ in range(1000):
            start = random.randint(100, 999)
            stop = random.randint(0, start)
            step = random.randint(-100, -1)
            self.assertEqual(self.primes[start:stop:step], p[start:stop:step], ' '.join(map(str, [start, stop, step, list(self.primes)])))

    def testSlicingNoStop(self):
        self.assertEqual(self.primes[::3], [])
        self.assertEqual(self.primes[1::3], [3])
        self.assertEqual(self.primes[1::-1], [3, 2])
        self.assertEqual(self.primes[2::3], [5])
        self.assertEqual(self.primes[3::1], [7])
        self.assertEqual(self.primes[5::2], [13])
        self.assertEqual(self.primes[4::-2], [11, 5, 2])
        self.assertEqual(self.primes[1::2], [3, 7, 13])
        self.assertEqual(self.primes[2::3], [5, 13])
        self.assertEqual(self.primes[3:], [7, 11, 13])
        self.assertEqual(self.primes[::-3], [13, 5])

    def testSlicingEmpty(self):
        # Test primes aren't generated for empty sequences
        for _ in range(1000):
            start = random.randint(0, 1000)
            stop = random.randint(start+1, 1001)
            step = random.randint(-100, -1)
            self.assertEqual(self.primes[start:stop:step], [])
            self.assertEqual(len(self.primes), 0)

        for _ in range(1000):
            start = random.randint(1, 1000)
            stop = random.randint(0, start-1)
            step = random.randint(1, 100)
            self.assertEqual(self.primes[start:stop:step], [])
            self.assertEqual(len(self.primes), 0)

        self.assertRaisesRegex(ValueError, "slice step cannot be zero", lambda p: p[10:20:0], self.primes)
        self.assertEqual(len(self.primes), 0)
        self.assertRaisesRegex(ValueError, "slice step cannot be zero", lambda p: p[20:10:0], self.primes)
        self.assertEqual(len(self.primes), 0)

    def testLen(self):
        self.assertEqual(len(self.primes), 0, self.primes)
        self.primes[0]
        self.assertEqual(len(self.primes), 1, self.primes)
        self.primes[1]
        self.assertEqual(len(self.primes), 2, self.primes)
        self.primes[2]
        self.assertEqual(len(self.primes), 3, self.primes)
        self.primes[10]
        self.assertEqual(len(self.primes), 11, self.primes)
        self.primes[150]
        self.assertEqual(len(self.primes), 151)
        self.primes[1234]
        self.assertEqual(len(self.primes), 1235)

    def testIteration(self):
        self.primes[999]

        self.assertEqual(n_primes(1000), list(self.primes))

        self.assertEqual(n_primes(1000), [prime for prime in self.primes])

        for prime in self.primes:
            self.assertTrue(is_prime(prime))

    def testEquality(self):
        otherprimes = Primes()
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

class TestSieves(unittest.TestCase):
    def testSieves(self):
        for i in range(1000):
            self.assertEqual(sieve_of_eratosthenes(i), sieve_of_atkin(i))

        for _ in range(100):
            r = random.randint(1001, 500000)
            self.assertEqual(sieve_of_eratosthenes(r), sieve_of_atkin(r))

class TestFactorisation(unittest.TestCase):
    def test15(self):
        self.assertEqual(factorise(15), set([3, 5]))

    def test8051(self):
        self.assertEqual(factorise(8051), set([83, 97]))

    def test10403(self):
        self.assertEqual(factorise(10403), set([101, 103]))

    def test94904178409(self):
        self.assertEqual(factorise(94904178409), set([198031, 479239]))

    def testComprehensive(self):
        primes = primes_up_to(500000)
        random.shuffle(primes)
        for p, q in zip(primes[:1000], primes[1:]):
            self.assertEqual(factorise(p*q), set([p, q]))

if __name__ == '__main__':
    unittest.main()
