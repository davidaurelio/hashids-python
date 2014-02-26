from unittest import TestCase, main
from hashids import Hashids


class TestInitHashids(TestCase):
    def test_construct(self):
        with self.assertRaises(AssertionError):
            Hashids(alphabet='abc')


class TestEncryptHashidsFunctions(TestCase):
    def test_empty_call(self):
        self.assertEqual(Hashids().encrypt(), '')

    def test_default(self):
        self.assertEqual(Hashids().encrypt(1, 2, 3), 'o2fXhV')

    def test_single_number(self):
        h = Hashids()
        self.assertEqual(h.encrypt(12345), 'j0gW')
        self.assertEqual(h.encrypt(1), 'jR')
        self.assertEqual(h.encrypt(22), 'Lw')
        self.assertEqual(h.encrypt(333), 'Z0E')
        self.assertEqual(h.encrypt(9999), 'w0rR')

    def test_multiple_numbers(self):
        h = Hashids()
        self.assertEqual(h.encrypt(683, 94108, 123, 5), 'vJvi7On9cXGtD')
        self.assertEqual(h.encrypt(1, 2), 'lYfo')
        self.assertEqual(h.encrypt(2, 3), 'nZhX')
        self.assertEqual(h.encrypt(99, 25), '3lKfD')

    def test_salt(self):
        h = Hashids(salt='this is my salt')
        self.assertEqual(h.encrypt(1, 2, 3), 'laHquq')
        self.assertEqual(h.encrypt(683, 94108, 123, 5), 'aBMswoO2UB3Sj')
        self.assertEqual(h.encrypt(1, 2), 'yzHD')
        self.assertEqual(h.encrypt(2, 3), 'rKux')
        self.assertEqual(h.encrypt(99, 25), '97Jun')

    def test_alphabet(self):
        h = Hashids(alphabet='!"#%&\',-/0123456789:;<=>ABCDEFGHIJKLMNOPQRSTUVWXYZ_`abcdefghijklmnopqrstuvwxyz~')
        self.assertEqual(h.encrypt(1, 2, 3), '7xfYh2')
        self.assertEqual(h.encrypt(1 << 30, 1 << 29), 'VM2<mQ~fNe9EY7')

    def test_min_length(self):
        h = Hashids(min_length=25)
        self.assertEqual(h.encrypt(1, 2, 3), 'gyOwl4B97bo2fXhVaDR0Znjrq')

    def test_all_parameters(self):
        h = Hashids('this is my salt', 16, 'abcdefghijklmnopqrstuvwxyz')
        self.assertEqual(h.encrypt(1, 2, 3), 'ypxbjmqrhqiykzar')

    def test_negative_call(self):
        h = Hashids()
        self.assertEqual(h.encrypt(1, -2, 3), '')

    def test_float_call(self):
        h = Hashids()
        self.assertEqual(h.encrypt(1, 2.5, 3), '')


class TestDecryptHashidsFunctions(TestCase):
    def test_empty_string(self):
        self.assertEqual(Hashids().decrypt(''), ())

    def test_non_string(self):
        self.assertEqual(Hashids().decrypt(object()), ())

    def test_default_salt(self):
        self.assertEqual(Hashids().decrypt('o2fXhV'), (1, 2, 3))

    def test_empty_call(self):
        self.assertEqual(Hashids().decrypt(''), ())

    def test_single_number(self):
        h = Hashids()
        self.assertEqual(h.decrypt('o2fXhV'), (1, 2, 3,))
        self.assertEqual(h.decrypt('jR'), (1,))
        self.assertEqual(h.decrypt('Lw'), (22,))
        self.assertEqual(h.decrypt('Z0E'), (333,))
        self.assertEqual(h.decrypt('w0rR'), (9999,))

    def test_multiple_numbers(self):
        h = Hashids()
        self.assertEqual(h.decrypt('vJvi7On9cXGtD'), (683, 94108, 123, 5,))
        self.assertEqual(h.decrypt('o2fXhV'), (1, 2, 3,))
        self.assertEqual(h.decrypt('xGhmsW'), (2, 4, 6,))
        self.assertEqual(h.decrypt('3lKfD'), (99, 25,))

    def test_salt(self):
        h = Hashids(salt='this is my salt')
        self.assertEqual(h.decrypt('aBMswoO2UB3Sj'), (683, 94108, 123, 5,))
        self.assertEqual(h.decrypt('laHquq'), (1, 2, 3,))
        self.assertEqual(h.decrypt('44uotN'), (2, 4, 6,))
        self.assertEqual(h.decrypt('97Jun'), (99, 25,))

    def test_alphabet(self):
        h = Hashids(alphabet='!"#%&\',-/0123456789:;<=>ABCDEFGHIJKLMNOPQRSTUVWXYZ_`abcdefghijklmnopqrstuvwxyz~')
        self.assertEqual(h.decrypt('7xfYh2'), (1, 2, 3,))

    def test_min_length(self):
        h = Hashids(min_length=25)
        self.assertEqual(h.decrypt('gyOwl4B97bo2fXhVaDR0Znjrq'), (1, 2, 3,))

    def test_all_parameters(self):
        h = Hashids('this is my salt', 16, 'abcdefghijklmnopqrstuvwxyz')
        self.assertEqual(h.decrypt('ypxbjmqrhqiykzar'), (1, 2, 3,))

    def test_invalid_hash(self):
        self.assertEqual(Hashids().decrypt('nopqrstuvw'), ())
        
if __name__ == '__main__':
    main()
