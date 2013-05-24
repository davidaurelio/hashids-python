from hashids import Hashids

def test_empty_call():
    assert Hashids().encrypt() == ''

def test_default_salt():
    assert Hashids().encrypt(1, 2, 3) == 'katKSA'

def test_single_number():
    h = Hashids()
    assert h.encrypt(12345) == 'rGAx'
    assert h.encrypt(1) == 'yE'
    assert h.encrypt(22) == 'B8'
    assert h.encrypt(333) == '7G9'
    assert h.encrypt(9999) == 'zpz5'

def test_multiple_numbers():
    h = Hashids()
    assert h.encrypt(683, 94108, 123, 5) == '6nph8p9duq8u9'
    assert h.encrypt(1, 2, 3) == 'katKSA'
    assert h.encrypt(2, 4, 6) == '5jhof9'
    assert h.encrypt(99, 25) == 'nq4CG'

def test_salt():
    h = Hashids(salt='Arbitrary string')
    assert h.encrypt(683, 94108, 123, 5) == 'q9khp7X9u6BuE'
    assert h.encrypt(1, 2, 3) == 'a7tLSG'
    assert h.encrypt(2, 4, 6) == 'Xbh4fp'
    assert h.encrypt(99, 25) == 'K6nCz'

def test_alphabet():
    h = Hashids(alphabet='!"#%&\',-/0123456789:;<=>ABCDEFGHIJKLMNOPQRSTUVWXYZ_`abcdefghijklmnopqrstuvwxyz~')
    assert h.encrypt(2839, 12, 32, 5) == '!%u#Y=%#v'
    assert h.encrypt(1, 2, 3) == ':Y9c#2'
    assert h.encrypt(23832) == 'cZKL'
    assert h.encrypt(99, 25) == 'aNCEI'

def test_min_length():
    h = Hashids(min_length=25)
    assert h.encrypt(7452, 2967, 21401) == '4ARhAecbrrGh8K7FBBbi4nkhL'
    assert h.encrypt(1, 2, 3) == 'IeRX9XtbpTkatKSAcXe4tALde'
    assert h.encrypt(6097) == 'aULxKgxFpEi7prdcK7LFLz4Lk'
    assert h.encrypt(99, 25) == 'UrBa8pCqLTnq4CGTaMpC7Kj6x'

def test_all_parameters():
    h = Hashids('arbitrary salt', 16, 'abcdefghijklmnopqrstuvwxyz')
    assert h.encrypt(7452, 2967, 21401) == 'mjpnilkonugzfjub'
    assert h.encrypt(1, 2, 3) == 'nqyjbjpcfeymvfiq'
    assert h.encrypt(60125) == 'vxwfjmrnfvtmpdow'
    assert h.encrypt(99, 25) == 'hsnymlyueozbnijs'

def test_negative_call():
    assert Hashids().encrypt(1, -2, 3) == ''

def test_float_call():
    assert Hashids().encrypt(1, 2.5, 3) == ''

if __name__ == '__main__':
    test_salt()
