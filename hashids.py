"""Implements the hashids algorithm in python. For more information, visit
http://www.hashids.org/. Compatible with Python 2.5--3"""
__version__ = '0.0.1'


def _is_uint(number):
    """Returns whether a value is an unsigned integer."""
    try:
        return number == int(number) and number >= 0
    except ValueError:
        return False


class Hashids(object):
    MIN_ALPHABET_LENGTH = 16
    _seps = 'cfhistuCFHISTU'
    _sep_div = 3.5
    _guard_div = 12

    def __init__(self, salt='', min_length=0,
                 alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'):
        self._salt = salt
        self._min_length = max(int(min_length), 0)

        unique_alphabet = [x for i, x in enumerate(alphabet) if alphabet.index(x) == i]
        assert len(unique_alphabet) >= Hashids.MIN_ALPHABET_LENGTH, \
            'error: alphabet must contain at least %d unique characters' % (Hashids.MIN_ALPHABET_LENGTH,)

        assert ' ' not in unique_alphabet, \
            'error: alphabet cannot contain spaces'

        self._seps = [val for val in unique_alphabet if val in self._seps]
        self._alphabet = [val for val in unique_alphabet if val not in self._seps]

        self._seps = self._consistent_shuffle(self._seps, self._salt)

        if not len(self._seps) or len(self._alphabet) / len(self._seps) > self._sep_div:
            len_seps = len(self._alphabet) // self._sep_div
            if 1 == len_seps:
                len_seps += 1

            if len_seps > len(self._seps):
                diff = int(len_seps - len(self._seps))
                self._seps += self._alphabet[:diff]
                self._alphabet = self._alphabet[diff:]
            else:
                self._seps = self._seps[:len_seps]

        self._alphabet = self._consistent_shuffle(self._alphabet, self._salt)
        guard_count = len(self._alphabet) // self._guard_div

        if len(self._alphabet) < 3:
            self._guards = self._seps[:guard_count]
            self._seps = self._seps[guard_count:]
        else:
            self._guards = self._alphabet[:guard_count]
            self._alphabet = self._alphabet[guard_count:]

        self._alphabet = ''.join(self._alphabet)

    def encrypt(self, *numbers):
        if not len(numbers):
            return ''

        if not (numbers and all(_is_uint(x) for x in numbers)):
            return ''

        return self.encode(numbers)

    def decrypt(self, hashed):
        if not hashed:
            return ()

        try:
            numbers = tuple(self._decode(hashed))
            return numbers if hashed == self.encode(numbers) else ()
        except:
            return ()

    def encode(self, numbers):
        alphabet = self._alphabet

        numbers_hash_int = 0
        for i, x in enumerate(numbers):
            numbers_hash_int += x % (i + 100)

        numbers_size = len(numbers)

        lottery = alphabet[numbers_hash_int % len(alphabet)]
        ret = lottery

        for i, number in enumerate(numbers):
            buffer = lottery + self._salt + alphabet
            alphabet = self._consistent_shuffle(alphabet, buffer[:len(alphabet)])
            last = self._hash(number, alphabet)

            ret += last

            if i + 1 < numbers_size:
                number %= (ord(last[0]) + i)
                seps_index = number % len(self._seps)
                ret += self._seps[seps_index]

        if len(ret) < self._min_length:
            guard_index = (numbers_hash_int + ord(ret[0])) % len(self._guards)
            guard = self._guards[guard_index]

            ret = guard + ret

            if len(ret) < self._min_length:
                guard_index = (numbers_hash_int + ord(ret[2])) % len(self._guards)
                guard = self._guards[guard_index]

                ret += guard

        half_len = len(alphabet) // 2
        while len(ret) < self._min_length:
            alphabet = self._consistent_shuffle(alphabet, alphabet)
            ret = alphabet[half_len:] + ret + alphabet[:half_len]

            excess = len(ret) - self._min_length
            if excess > 0:
                ret = ret[excess // 2:-excess // 2]

        return ret

    def _decode(self, hash):
        alphabet = self._alphabet

        import re

        guard_re = re.compile('[%s]' % re.escape(''.join(self._guards)))
        seps_re = re.compile('[%s]' % re.escape(''.join(self._seps)))

        parts = guard_re.split(hash)
        hash = parts[1] if 2 <= len(parts) <= 3 else parts[0]

        lottery = hash[0]
        hash = hash[1:]

        parts = seps_re.split(hash)
        for part in parts:
            buffer = lottery + self._salt + alphabet

            alphabet = self._consistent_shuffle(alphabet, buffer[:len(alphabet)])
            yield self._unhash(part, alphabet)


    @staticmethod
    def _unhash(hashed, alphabet):
        number = 0
        len_hash = len(hashed)
        len_alphabet = len(alphabet)
        for i, character in enumerate(hashed):
            position = alphabet.index(character)
            number += position * len_alphabet ** (len_hash - i - 1)

        return number

    @staticmethod
    def _hash(number, alphabet):
        hashed = ''
        alphabet_len = len(alphabet)

        while True:
            hashed = alphabet[number % alphabet_len] + hashed
            number //= alphabet_len
            if not number:
                return hashed

    @staticmethod
    def _consistent_shuffle(alphabet, salt):
        if not len(salt):
            return alphabet

        len_salt = len(salt)

        integer, j, temp, i, v, p = 0, 0, 0, 0, 0, 0

        i = len(alphabet) - 1
        for v in range(i):
            v %= len_salt
            integer = ord(salt[v])
            p += integer
            j = (integer + v + p) % i
            temp = alphabet[j]
            alphabet = alphabet[:j] + alphabet[i] + alphabet[j + 1:]
            alphabet = alphabet[:i] + temp + alphabet[i + 1:]

            i -= 1

        return alphabet
