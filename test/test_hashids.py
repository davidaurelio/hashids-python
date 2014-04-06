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
        assert Hashids().decrypt('katKSA') == (1, 2, 3)

    def test_empty_call(self):
        assert Hashids().decrypt('') == ()

    def test_single_number(self):
        h = Hashids()
        assert h.decrypt('rGAx') == (12345,)
        assert h.decrypt('yE') == (1,)
        assert h.decrypt('B8') == (22,)
        assert h.decrypt('7G9') == (333,)
        assert h.decrypt('zpz5') == (9999,)

    def test_multiple_numbers(self):
        h = Hashids()
        assert h.decrypt('6nph8p9duq8u9') == (683, 94108, 123, 5,)
        assert h.decrypt('katKSA') == (1, 2, 3,)
        assert h.decrypt('5jhof9') == (2, 4, 6,)
        assert h.decrypt('nq4CG') == (99, 25,)

    def test_salt(self):
        h = Hashids(salt='Arbitrary string')
        assert h.decrypt('q9khp7X9u6BuE') == (683, 94108, 123, 5,)
        assert h.decrypt('a7tLSG') == (1, 2, 3,)
        assert h.decrypt('Xbh4fp') == (2, 4, 6,)
        assert h.decrypt('K6nCz') == (99, 25,)

    def test_alphabet(self):
        h = Hashids(alphabet='!"#%&\',-/0123456789:;<=>ABCDEFGHIJKLMNOPQRSTUVWXYZ_`abcdefghijklmnopqrstuvwxyz~')
        assert h.decrypt('!%u#Y=%#v') == (2839, 12, 32, 5,)
        assert h.decrypt(':Y9c#2') == (1, 2, 3,)
        assert h.decrypt('cZKL') == (23832,)
        assert h.decrypt('aNCEI') == (99, 25,)

    def test_min_length(self):
        h = Hashids(min_length=25)
        assert h.decrypt('4ARhAecbrrGh8K7FBBbi4nkhL') == (7452, 2967, 21401,)
        assert h.decrypt('IeRX9XtbpTkatKSAcXe4tALde') == (1, 2, 3,)
        assert h.decrypt('aULxKgxFpEi7prdcK7LFLz4Lk') == (6097,)
        assert h.decrypt('UrBa8pCqLTnq4CGTaMpC7Kj6x') == (99, 25,)

    def test_all_parameters(self):
        h = Hashids('arbitrary salt', 16, 'abcdefghijklmnopqrstuvwxyz')
        assert h.decrypt('mjpnilkonugzfjub') == (7452, 2967, 21401,)
        assert h.decrypt('nqyjbjpcfeymvfiq') == (1, 2, 3,)
        assert h.decrypt('vxwfjmrnfvtmpdow') == (60125,)
        assert h.decrypt('hsnymlyueozbnijs') == (99, 25,)

    def test_invalid_hash(self):
        assert Hashids(alphabet='abcdefghijklm').decrypt('nopqrstuvw') == ()
