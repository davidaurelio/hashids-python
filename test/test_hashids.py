from hashids import Hashids
import pytest

class TestConstructor(object):
    def test_small_alphabet(self):
        pytest.raises(ValueError, Hashids, alphabet='abcabc')


class TestEncryption(object):
    def test_empty_call(self):
        assert Hashids().encrypt() == ''

    def test_default_salt(self):
        assert Hashids().encrypt(1, 2, 3) == 'o2fXhV'

    def test_single_number(self):
        h = Hashids()
        assert h.encrypt(12345) == 'j0gW'
        assert h.encrypt(1) == 'jR'
        assert h.encrypt(22) == 'Lw'
        assert h.encrypt(333) == 'Z0E'
        assert h.encrypt(9999) == 'w0rR'

    def test_multiple_numbers(self):
        h = Hashids()
        assert h.encrypt(683, 94108, 123, 5) == 'vJvi7On9cXGtD'
        assert h.encrypt(1, 2, 3) == 'o2fXhV'
        assert h.encrypt(2, 4, 6) == 'xGhmsW'
        assert h.encrypt(99, 25) == '3lKfD'

    def test_salt(self):
        h = Hashids(salt='Arbitrary string')
        assert h.encrypt(683, 94108, 123, 5) == 'QWyf8yboH7KT2'
        assert h.encrypt(1, 2, 3) == 'neHrCa'
        assert h.encrypt(2, 4, 6) == 'LRCgf2'
        assert h.encrypt(99, 25) == 'JOMh1'

    def test_alphabet(self):
        h = Hashids(alphabet='!"#%&\',-/0123456789:;<=>ABCDEFGHIJKLMNOPQRSTUVWXYZ_`abcdefghijklmnopqrstuvwxyz~')
        assert h.encrypt(2839, 12, 32, 5) == '_nJUNTVU3'
        assert h.encrypt(1, 2, 3) == '7xfYh2'
        assert h.encrypt(23832) == 'Z6R>'
        assert h.encrypt(99, 25) == 'AYyIB'

    def test_min_length(self):
        h = Hashids(min_length=25)
        assert h.encrypt(7452, 2967, 21401) == 'pO3K69b86jzc6krI416enr2B5'
        assert h.encrypt(1, 2, 3) == 'gyOwl4B97bo2fXhVaDR0Znjrq'
        assert h.encrypt(6097) == 'Nz7x3VXyMYerRmWeOBQn6LlRG'
        assert h.encrypt(99, 25) == 'k91nqP3RBe3lKfDaLJrvy8XjV'

    def test_all_parameters(self):
        h = Hashids('arbitrary salt', 16, 'abcdefghijklmnopqrstuvwxyz')
        assert h.encrypt(7452, 2967, 21401) == 'wygqxeunkatjgkrw'
        assert h.encrypt(1, 2, 3) == 'pnovxlaxuriowydb'
        assert h.encrypt(60125) == 'jkbgxljrjxmlaonp'
        assert h.encrypt(99, 25) == 'erdjpwrgouoxlvbx'


    def test_negative_call(self):
        assert Hashids().encrypt(1, -2, 3) == ''

    def test_float_call(self):
        assert Hashids().encrypt(1, 2.5, 3) == ''

class TestDecryption(object):
    def test_empty_string(self):
        assert Hashids().decrypt('') == ()

    def test_non_string(self):
        assert Hashids().decrypt(object()) == ()

    def test_default_salt(self):
        assert Hashids().decrypt('o2fXhV') == (1, 2, 3)

    def test_empty_call(self):
        assert Hashids().decrypt('') == ()

    def test_single_number(self):
        h = Hashids()
        assert h.decrypt('j0gW') == (12345,)
        assert h.decrypt('jR') == (1,)
        assert h.decrypt('Lw') == (22,)
        assert h.decrypt('Z0E') == (333,)
        assert h.decrypt('w0rR') == (9999,)

    def test_multiple_numbers(self):
        h = Hashids()
        assert h.decrypt('vJvi7On9cXGtD') == (683, 94108, 123, 5,)
        assert h.decrypt('o2fXhV') == (1, 2, 3,)
        assert h.decrypt('xGhmsW') == (2, 4, 6,)
        assert h.decrypt('3lKfD') == (99, 25,)

    def test_salt(self):
        h = Hashids(salt='Arbitrary string')
        assert h.decrypt('QWyf8yboH7KT2') == (683, 94108, 123, 5,)
        assert h.decrypt('neHrCa') == (1, 2, 3,)
        assert h.decrypt('LRCgf2') == (2, 4, 6,)
        assert h.decrypt('JOMh1') == (99, 25,)

    def test_alphabet(self):
        h = Hashids(alphabet='!"#%&\',-/0123456789:;<=>ABCDEFGHIJKLMNOPQRSTUVWXYZ_`abcdefghijklmnopqrstuvwxyz~')
        assert h.decrypt('_nJUNTVU3') == (2839, 12, 32, 5,)
        assert h.decrypt('7xfYh2') == (1, 2, 3,)
        assert h.decrypt('Z6R>') == (23832,)
        assert h.decrypt('AYyIB') == (99, 25,)

    def test_min_length(self):
        h = Hashids(min_length=25)
        assert h.decrypt('pO3K69b86jzc6krI416enr2B5') == (7452, 2967, 21401,)
        assert h.decrypt('gyOwl4B97bo2fXhVaDR0Znjrq') == (1, 2, 3,)
        assert h.decrypt('Nz7x3VXyMYerRmWeOBQn6LlRG') == (6097,)
        assert h.decrypt('k91nqP3RBe3lKfDaLJrvy8XjV') == (99, 25,)

    def test_all_parameters(self):
        h = Hashids('arbitrary salt', 16, 'abcdefghijklmnopqrstuvwxyz')
        assert h.decrypt('wygqxeunkatjgkrw') == (7452, 2967, 21401,)
        assert h.decrypt('pnovxlaxuriowydb') == (1, 2, 3,)
        assert h.decrypt('jkbgxljrjxmlaonp') == (60125,)
        assert h.decrypt('erdjpwrgouoxlvbx') == (99, 25,)

    def test_invalid_hash(self):
        assert Hashids(alphabet='abcdefghijklmnop').decrypt('qrstuvwxyz') == ()
