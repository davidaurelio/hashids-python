from hashids import Hashids
import pytest

class TestConstructor(object):
    def test_small_alphabet(self):
        pytest.raises(ValueError, Hashids, alphabet='abcabc')


class TestEncryption(object):
    def test_empty_call(self):
        assert Hashids().encode() == ''

    def test_default_salt(self):
        assert Hashids().encode(1, 2, 3) == 'o2fXhV'

    def test_single_number(self):
        h = Hashids()
        assert h.encode(12345) == 'j0gW'
        assert h.encode(1) == 'jR'
        assert h.encode(22) == 'Lw'
        assert h.encode(333) == 'Z0E'
        assert h.encode(9999) == 'w0rR'

    def test_multiple_numbers(self):
        h = Hashids()
        assert h.encode(683, 94108, 123, 5) == 'vJvi7On9cXGtD'
        assert h.encode(1, 2, 3) == 'o2fXhV'
        assert h.encode(2, 4, 6) == 'xGhmsW'
        assert h.encode(99, 25) == '3lKfD'

    def test_salt(self):
        h = Hashids(salt='Arbitrary string')
        assert h.encode(683, 94108, 123, 5) == 'QWyf8yboH7KT2'
        assert h.encode(1, 2, 3) == 'neHrCa'
        assert h.encode(2, 4, 6) == 'LRCgf2'
        assert h.encode(99, 25) == 'JOMh1'

    def test_alphabet(self):
        h = Hashids(alphabet='!"#%&\',-/0123456789:;<=>ABCDEFGHIJKLMNOPQRSTUVWXYZ_`abcdefghijklmnopqrstuvwxyz~')
        assert h.encode(2839, 12, 32, 5) == '_nJUNTVU3'
        assert h.encode(1, 2, 3) == '7xfYh2'
        assert h.encode(23832) == 'Z6R>'
        assert h.encode(99, 25) == 'AYyIB'

    def test_min_length(self):
        h = Hashids(min_length=25)
        assert h.encode(7452, 2967, 21401) == 'pO3K69b86jzc6krI416enr2B5'
        assert h.encode(1, 2, 3) == 'gyOwl4B97bo2fXhVaDR0Znjrq'
        assert h.encode(6097) == 'Nz7x3VXyMYerRmWeOBQn6LlRG'
        assert h.encode(99, 25) == 'k91nqP3RBe3lKfDaLJrvy8XjV'

    def test_all_parameters(self):
        h = Hashids('arbitrary salt', 16, 'abcdefghijklmnopqrstuvwxyz')
        assert h.encode(7452, 2967, 21401) == 'wygqxeunkatjgkrw'
        assert h.encode(1, 2, 3) == 'pnovxlaxuriowydb'
        assert h.encode(60125) == 'jkbgxljrjxmlaonp'
        assert h.encode(99, 25) == 'erdjpwrgouoxlvbx'

    def test_alphabet_without_standard_separators(self):
        h = Hashids(alphabet='abdegjklmnopqrvwxyzABDEGJKLMNOPQRVWXYZ1234567890')
        assert h.encode(7452, 2967, 21401) == 'X50Yg6VPoAO4'
        assert h.encode(1, 2, 3) == 'GAbDdR'
        assert h.encode(60125) == '5NMPD'
        assert h.encode(99, 25) == 'yGya5'

    def test_alphabet_with_two_standard_separators(self):
        h = Hashids(alphabet='abdegjklmnopqrvwxyzABDEGJKLMNOPQRVWXYZ1234567890uC')
        assert h.encode(7452, 2967, 21401) == 'GJNNmKYzbPBw'
        assert h.encode(1, 2, 3) == 'DQCXa4'
        assert h.encode(60125) == '38V1D'
        assert h.encode(99, 25) == '373az'

    def test_negative_call(self):
        assert Hashids().encode(1, -2, 3) == ''

    def test_float_call(self):
        assert Hashids().encode(1, 2.5, 3) == ''

class TestDecryption(object):
    def test_empty_string(self):
        assert Hashids().decode('') == ()

    def test_non_string(self):
        assert Hashids().decode(object()) == ()

    def test_default_salt(self):
        assert Hashids().decode('o2fXhV') == (1, 2, 3)

    def test_empty_call(self):
        assert Hashids().decode('') == ()

    def test_single_number(self):
        h = Hashids()
        assert h.decode('j0gW') == (12345,)
        assert h.decode('jR') == (1,)
        assert h.decode('Lw') == (22,)
        assert h.decode('Z0E') == (333,)
        assert h.decode('w0rR') == (9999,)

    def test_multiple_numbers(self):
        h = Hashids()
        assert h.decode('vJvi7On9cXGtD') == (683, 94108, 123, 5)
        assert h.decode('o2fXhV') == (1, 2, 3)
        assert h.decode('xGhmsW') == (2, 4, 6)
        assert h.decode('3lKfD') == (99, 25)

    def test_salt(self):
        h = Hashids(salt='Arbitrary string')
        assert h.decode('QWyf8yboH7KT2') == (683, 94108, 123, 5)
        assert h.decode('neHrCa') == (1, 2, 3)
        assert h.decode('LRCgf2') == (2, 4, 6)
        assert h.decode('JOMh1') == (99, 25)

    def test_alphabet(self):
        h = Hashids(alphabet='!"#%&\',-/0123456789:;<=>ABCDEFGHIJKLMNOPQRSTUVWXYZ_`abcdefghijklmnopqrstuvwxyz~')
        assert h.decode('_nJUNTVU3') == (2839, 12, 32, 5)
        assert h.decode('7xfYh2') == (1, 2, 3)
        assert h.decode('Z6R>') == (23832,)
        assert h.decode('AYyIB') == (99, 25)

    def test_min_length(self):
        h = Hashids(min_length=25)
        assert h.decode('pO3K69b86jzc6krI416enr2B5') == (7452, 2967, 21401)
        assert h.decode('gyOwl4B97bo2fXhVaDR0Znjrq') == (1, 2, 3)
        assert h.decode('Nz7x3VXyMYerRmWeOBQn6LlRG') == (6097,)
        assert h.decode('k91nqP3RBe3lKfDaLJrvy8XjV') == (99, 25)

    def test_all_parameters(self):
        h = Hashids('arbitrary salt', 16, 'abcdefghijklmnopqrstuvwxyz')
        assert h.decode('wygqxeunkatjgkrw') == (7452, 2967, 21401)
        assert h.decode('pnovxlaxuriowydb') == (1, 2, 3)
        assert h.decode('jkbgxljrjxmlaonp') == (60125,)
        assert h.decode('erdjpwrgouoxlvbx') == (99, 25)

    def test_invalid_hash(self):
        assert Hashids(alphabet='abcdefghijklmnop').decode('qrstuvwxyz') == ()

    def test_alphabet_without_standard_separators(self):
        h = Hashids(alphabet='abdegjklmnopqrvwxyzABDEGJKLMNOPQRVWXYZ1234567890')
        assert h.decode('X50Yg6VPoAO4') == (7452, 2967, 21401)
        assert h.decode('GAbDdR') == (1, 2, 3)
        assert h.decode('5NMPD') == (60125,)
        assert h.decode('yGya5') == (99, 25)

    def test_alphabet_with_two_standard_separators(self):
        h = Hashids(alphabet='abdegjklmnopqrvwxyzABDEGJKLMNOPQRVWXYZ1234567890uC')
        assert h.decode('GJNNmKYzbPBw') == (7452, 2967, 21401)
        assert h.decode('DQCXa4') == (1, 2, 3)
        assert h.decode('38V1D') == (60125,)
        assert h.decode('373az') == (99, 25)

    def test_only_one_valid(self):
        h = Hashids(min_length=6)
        assert h.decode(h.encode(1)[:-1] + '0') == ()
