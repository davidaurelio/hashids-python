"""Implements the hashids algorithm in python. For more information, visit
http://www.hashids.org/. Compatible with Python 2.5--3"""
from itertools import chain
import re

__version__ = '0.8.3'

# Python 2/3 compatibility code
try:
    _STR_TYPE = basestring
except NameError:
    _STR_TYPE = str

def _head(iterable):
    """Extracts the first value from an iterable."""
    # Python < 2.6 does not have `next()`
    # Python 3 does not have generator.next()
    for value in iterable:
        return value

# end of compatibility code

def _is_str(candidate):
    """Returns whether a value is a string."""
    return isinstance(candidate, _STR_TYPE)

def _is_uint(number):
    """Returns whether a value is an unsigned integer."""
    try:
        return number == int(number) and number >= 0
    except ValueError:
        return False

def _replace_index(list_object, index, value):
    """Replaces a value in a list_object with another value. Returns the
    replaced value."""
    list_object.insert(index, value)
    return list_object.pop(index + 1)

def _to_front(value, iterator):
    """Yields `value`, then all other elements from `iterator` if they are not
    equal to `value`."""
    return chain((value,), (x for x in iterator if x != value))

def _hash(number, alphabet):
    """Hashes `number` using the given `alphabet` sequence."""
    hashed = ''
    len_alphabet = len(alphabet)
    while True:
        hashed = alphabet[number % len_alphabet] + hashed
        number //= len_alphabet
        if not number:
            return hashed

def _unhash(hashed, alphabet):
    """Restores a number tuple from hashed using the given `alphabet` index."""
    number = 0
    len_hash = len(hashed)
    len_alphabet = len(alphabet)
    for i, character in enumerate(hashed):
        position = alphabet.index(character)
        number += position * len_alphabet ** (len_hash - i - 1)

    return number

def _reorder(iterable, salt):
    """Yields all values from `iterable` in an order derived from the
    given `salt`."""
    sorting = [ord(x) for x in salt] if salt else [0]
    len_sorting = len(sorting)
    values = list(iterable)

    for i in range(len_sorting):
        add = True
        for k in range(i, len_sorting + i - 1):
            diff = sorting[(k + 1) % len_sorting]
            sorting[i] += diff + (k * i) if add else -diff
            add = not add

        sorting[i] = abs(sorting[i])

    i = -1
    while values:
        i = (i + 1) % len_sorting
        pos = sorting[i] % len(values)
        yield values.pop(pos)

def _re_class(characters):
    """Creates a regular expression with a character class matching
    all `characters`."""
    return re.compile('[%s]' % re.escape(''.join(characters)))

class Hashids(object):
    """Hashes and restores values using the "hashids" algorithm."""
    PRIMES = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43)

    def __init__(self, salt='', min_length=0,
                 alphabet='xcS4F6h89aUbideAI7tkynuopqrXCgTE5GBKHLMjfRsz'):
        """
        Initializes a Hashids object with salt, minimum length, and alphabet.

        :param salt: A string influencing the generated hash ids.
        :param min_length: The minimum length for generated hashes
        :param alphabet: The characters to use for the generated hash ids.
        """
        alphabet = [x for i, x in enumerate(alphabet) if alphabet.index(x) == i]
        if len(alphabet) < 4:
            raise ValueError('Alphabet must contain at least 4 '
                             'unique characters.')

        self._min_length = max(int(min_length), 0)
        self._salt = salt

        len_alphabet = len(alphabet)
        separators = [_replace_index(alphabet, prime - 1, None)
                      for prime in self.PRIMES if prime - 1 < len_alphabet]

        self._guards = guards = tuple(separators.pop(index)
                                      for index in (0, 4, 8, 12)
                                      if index < len(separators))
        self._guards_re = _re_class(guards)
        self._separators = tuple(separators)
        self._separators_re = _re_class(separators)
        alphabet = (x for x in alphabet if x)
        self._alphabet = tuple(_reorder(alphabet, salt))

    def encrypt(self, *values):
        """Builds a hash from the passed `values`.

        :param values The values to transform into a hashid

        >>> hashids = Hashids('arbitrary salt', 16, 'abcdefghijkl')
        >>> hashids.encrypt(1, 23, 456)
        'fhblhkfjejddjbdl'
        """
        if not (values and all(_is_uint(x) for x in values)):
            return ''

        hashed, alphabet = self._encode(values, self._alphabet, self._salt)
        return self._ensure_length(hashed, values, alphabet)

    def _encode(self, values, alphabet, salt):
        """Helper method that does the hash building without argument checks."""
        len_values = len(values)
        str_values = [str(x) for x in values]
        separators = list(_reorder(self._separators, ''.join(str_values)))
        len_separators = len(separators)

        lottery_salt = '-'.join(chain(str_values,
                                      (str((v + 1) * 2) for v in values)))
        hashed = lottery_char = _head(_reorder(alphabet, lottery_salt))
        alphabet = list(_to_front(lottery_char, alphabet))

        for i, value in enumerate(values):
            alphabet_salt = '%d%s' % (ord(lottery_char) & 12345, salt)
            alphabet = list(_reorder(alphabet, alphabet_salt))
            hashed += _hash(value, alphabet)

            if i < len_values - 1:
                hashed += separators[(value + i) % len_separators]

        return hashed, alphabet

    def _ensure_length(self, hashid, values, alphabet):
        """Helper method that extends a hashid if it does not have the
        minimum lenght."""
        length = self._min_length
        salt = self._salt
        len_hashed = len(hashid)
        if len_hashed < length:
            first_index = sum((i + 1) * value for i, value in enumerate(values))

            guards = self._guards
            len_guards = len(guards)
            guard_index = first_index % len_guards
            hashid = guards[guard_index] + hashid
            len_hashed += 1

            if len_hashed < length:
                hashid += guards[(guard_index + len_hashed) % len_guards]
                len_hashed += 1

        while len_hashed < length:
            pad = ord(alphabet[1]), ord(alphabet[0])
            pad_left = self._encode(pad, alphabet, salt)[0]
            pad_right = self._encode(pad, alphabet, '%d%d' % pad)[0]
            hashid = pad_left + hashid + pad_right

            len_hashed = len(hashid)
            excess = len_hashed - length
            if excess > 0:
                hashid = hashid[excess//2:-excess//2]

            alphabet = list(_reorder(alphabet, salt + hashid))

        return hashid

    def decrypt(self, hashid):
        """Restore a tuple of numbers from the passed `hashid`.

        :param hashid The hashid to decrypt

        >>> hashids = Hashids('arbitrary salt', 16, 'abcdefghijkl')
        >>> hashids.decrypt('fhblhkfjejddjbdl')
        (1, 23, 456)
        """
        if not hashid or not _is_str(hashid):
            return ()
        try:
            return tuple(self._decode(hashid))
        except:
            return ()

    def _decode(self, hashid):
        """Helper method that restores the values encoded in a hashid without
        argument checks."""
        parts = self._guards_re.split(hashid)
        hashid = parts[1] if 2 <= len(parts) <= 3 else parts[0]

        lottery_char = None
        hash_parts = self._separators_re.split(hashid)
        for part in ((i, x) for i, x in enumerate(hash_parts) if x):
            i, sub_hash = part
            if i == 0:
                lottery_char = hashid[0]
                sub_hash = sub_hash[1:]
                alphabet = _to_front(lottery_char, self._alphabet)

            if lottery_char and alphabet:
                salt = '%d%s' % (ord(lottery_char) & 12345, self._salt)
                alphabet = list(_reorder(alphabet, salt))
                yield _unhash(sub_hash, alphabet)
