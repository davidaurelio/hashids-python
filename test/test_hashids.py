from hashids import Hashids
import pytest

class TestConstructor(object):
    def test_small_alphabet(self):
        pytest.raises(ValueError, Hashids, alphabet='abcabc')


class TestEncryption(object):
    def test_empty_call(self):
        assert Hashids().encrypt() == ''

    def test_default_salt(self):
        assert Hashids().encrypt(1, 2, 3) == 'katKSA'

    def test_single_number(self):
        h = Hashids()
        assert h.encrypt(12345) == 'rGAx'
        assert h.encrypt(1) == 'yE'
        assert h.encrypt(22) == 'B8'
        assert h.encrypt(333) == '7G9'
        assert h.encrypt(9999) == 'zpz5'

    def test_multiple_numbers(self):
        h = Hashids()
        assert h.encrypt(683, 94108, 123, 5) == '6nph8p9duq8u9'
        assert h.encrypt(1, 2, 3) == 'katKSA'
        assert h.encrypt(2, 4, 6) == '5jhof9'
        assert h.encrypt(99, 25) == 'nq4CG'

    def test_salt(self):
        h = Hashids(salt='Arbitrary string')
        assert h.encrypt(683, 94108, 123, 5) == 'q9khp7X9u6BuE'
        assert h.encrypt(1, 2, 3) == 'a7tLSG'
        assert h.encrypt(2, 4, 6) == 'Xbh4fp'
        assert h.encrypt(99, 25) == 'K6nCz'

    def test_alphabet(self):
        h = Hashids(alphabet='!"#%&\',-/0123456789:;<=>ABCDEFGHIJKLMNOPQRSTUVWXYZ_`abcdefghijklmnopqrstuvwxyz~')
        assert h.encrypt(2839, 12, 32, 5) == '!%u#Y=%#v'
        assert h.encrypt(1, 2, 3) == ':Y9c#2'
        assert h.encrypt(23832) == 'cZKL'
        assert h.encrypt(99, 25) == 'aNCEI'

    def test_min_length(self):
        h = Hashids(min_length=25)
        assert h.encrypt(7452, 2967, 21401) == '4ARhAecbrrGh8K7FBBbi4nkhL'
        assert h.encrypt(1, 2, 3) == 'IeRX9XtbpTkatKSAcXe4tALde'
        assert h.encrypt(6097) == 'aULxKgxFpEi7prdcK7LFLz4Lk'
        assert h.encrypt(99, 25) == 'UrBa8pCqLTnq4CGTaMpC7Kj6x'

    def test_all_parameters(self):
        h = Hashids('arbitrary salt', 16, 'abcdefghijklmnopqrstuvwxyz')
        assert h.encrypt(7452, 2967, 21401) == 'mjpnilkonugzfjub'
        assert h.encrypt(1, 2, 3) == 'nqyjbjpcfeymvfiq'
        assert h.encrypt(60125) == 'vxwfjmrnfvtmpdow'
        assert h.encrypt(99, 25) == 'hsnymlyueozbnijs'

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
