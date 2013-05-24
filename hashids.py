from itertools import chain


def _replace_index(list, index, object):
    list.insert(index, object)
    return list.pop(index + 1)

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
    PRIMES = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43)

    def __init__(self, salt='', min_length=0,
                 alphabet='xcS4F6h89aUbideAI7tkynuopqrXCgTE5GBKHLMjfRsz'):
        alphabet = [x for i, x in enumerate(alphabet) if alphabet.index(x) == i]
        self._min_length = max(int(min_length), 0)
        self._salt = salt

        self._guards = guards = []
        len_alphabet = len(alphabet)
        self._separators = separators = [_replace_index(alphabet, prime - 1, None)
                                         for prime in self.PRIMES
                                         if prime - 1 < len_alphabet]
        for index in (0, 4, 8, 12):
            if index < len(separators):
                guards.append(separators.pop(index))

        self._alphabet = tuple(_consistent_shuffle(filter(bool, alphabet), salt))

    def encrypt(self, *values):
        if not values:
            return ''

        return self._encode(values, self._alphabet, self._salt,
                            self._min_length)

    def _encode(self, values, alphabet, salt, min_length=0):
        num_length = len(values)
        str_values = [str(x) for x in values]
        separators = list(_consistent_shuffle(self._separators,
                                              ''.join(str_values)))
        num_separators = len(separators)

        lottery_salt = '-'.join(chain(str_values,
                                      (str((v + 1) * 2) for v in values)))
        lottery = list(_consistent_shuffle(alphabet, lottery_salt))
        hashed = lottery_char = lottery[0]
        alphabet = list(_to_front(lottery_char, alphabet))

        for i, value in enumerate(values):
            alphabet_salt = str(ord(lottery_char) & 12345) + salt
            alphabet = list(_consistent_shuffle(alphabet, alphabet_salt))
            hashed += _hash(value, alphabet)

            if i < num_length - 1:
                hashed += separators[(value + i) % num_separators]

        length = len(hashed)
        if length < min_length:
            first_index = sum((i + 1) * value
                              for i, value in enumerate(values))

            guards = self._guards
            num_guards = len(guards)
            guard_index = first_index % num_guards
            hashed = guards[guard_index] + hashed
            length += 1

            if length < min_length:
                hashed += guards[(guard_index + length) % num_guards]
                length += 1

        while length < min_length:
            pad = ord(alphabet[1]), ord(alphabet[0])
            pad_left = self._encode(pad, alphabet, salt)
            pad_right = self._encode(pad, alphabet, '%d%d' % pad)
            hashed = pad_left + hashed + pad_right

            length = len(hashed)
            excess = length - min_length
            if excess > 0:
                hashed = hashed[excess//2:-excess//2]

            alphabet = list(_consistent_shuffle(alphabet, salt + hashed))

        return hashed

