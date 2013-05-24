from collections import OrderedDict
from itertools import chain

alphabet = 'xcS4F6h89aUbideAI7tkynuopqrXCgTE5GBKHLMjfRsz'
primes = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43)

def _to_front(element, iterator):
    return chain((element,), (x for x in iterator if x != element))

def _hash(number, alphabet):
    h = ''
    n = len(alphabet)
    while True:
        h = alphabet[number % n] + h
        number //= n
        if not number:
            return h

def _consistent_shuffle(iterable, salt):
    sorting = [ord(x) for x in salt] if salt else [0]
    n = len(sorting)
    l = list(iterable)

    for i in range(n):
        add = True
        for k in range(i, n + i - 1):
            diff = sorting[(k + 1) % n]
            sorting[i] += diff + (k * i) if add else -diff
            add = not add

        sorting[i] = abs(sorting[i])

    i = -1
    while l:
        i = (i + 1) % n
        pos = sorting[i] % len(l)
        yield l.pop(pos)


class Hashids(object):
    def __init__(self, salt='', alphabet=alphabet):
        alphabet = OrderedDict(enumerate(alphabet))
        self._salt = salt

        self._guards = guards = []
        self._separators = separators = [alphabet.pop(prime - 1)
                                         for prime in primes
                                         if prime - 1 in alphabet]
        for index in (0, 4, 8, 12):
            if index < len(separators):
                guards.append(separators.pop(index))

        self._alphabet = tuple(_consistent_shuffle(alphabet.values(), salt))

    def encrypt(self, *values):
        if not len(values):
            return ''

        salt = self._salt

        str_values = [str(x) for x in values]
        separators = list(_consistent_shuffle(self._separators, ''.join(str_values)))
        num_separators = len(separators)

        lottery_salt = '-'.join(chain(str_values, (str((v + 1) * 2) for v in values)))
        lottery = list(_consistent_shuffle(self._alphabet, lottery_salt))
        hashed = lottery_char = lottery[0]
        alphabet = list(_to_front(lottery_char, self._alphabet))

        n = len(values)
        for i, value in enumerate(values):
            alphabet_salt = str(ord(lottery_char) & 12345) + salt
            alphabet = list(_consistent_shuffle(alphabet, alphabet_salt))
            hashed += _hash(value, alphabet)

            if i < n - 1:
                hashed += separators[(value + i) % num_separators]

        return hashed
