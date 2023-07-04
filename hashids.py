"""Implements the hashids algorithm in python. For more information, visit http://hashids.org/"""

from __future__ import annotations

import functools
import math
import warnings
from collections.abc import Callable, Iterable, Iterator
from typing import TypeVar

from typing_extensions import ParamSpec

__version__ = "1.3.1"

_P = ParamSpec("_P")
_T = TypeVar("_T")

RATIO_SEPARATORS = 3.5
RATIO_GUARDS = 12


def _is_uint(number: int) -> bool:
    """Returns whether a value is an unsigned integer."""
    try:
        return number == int(number) and number >= 0
    except ValueError:
        return False


def _split(string: str, splitters: str) -> Iterator[str]:
    """Splits a string into parts at multiple characters"""
    part = ""
    for character in string:
        if character in splitters:
            yield part
            part = ""
        else:
            part += character
    yield part


def _hash(number: int, alphabet: str) -> str:
    """Hashes `number` using the given `alphabet` sequence."""
    hashed = ""
    len_alphabet = len(alphabet)
    while True:
        hashed = alphabet[number % len_alphabet] + hashed
        number //= len_alphabet
        if not number:
            return hashed


def _unhash(hashed: str, alphabet: str) -> int:
    """Restores a number tuple from hashed using the given `alphabet` index."""
    number = 0
    len_alphabet = len(alphabet)
    for character in hashed:
        position = alphabet.index(character)
        number *= len_alphabet
        number += position
    return number


def _reorder(string: str, salt: str) -> str:
    """Reorders `string` according to `salt`."""
    len_salt = len(salt)

    if len_salt != 0:
        chars = list(string)
        index, integer_sum = 0, 0
        for i in range(len(chars) - 1, 0, -1):
            integer = ord(salt[index])
            integer_sum += integer
            j = (integer + index + integer_sum) % i
            chars[i], chars[j] = chars[j], chars[i]
            index = (index + 1) % len_salt
        string = "".join(chars)

    return string


def _index_from_ratio(dividend: int, divisor: float) -> int:
    """Returns the ceiled ratio of two numbers as int."""
    return int(math.ceil(float(dividend) / divisor))


def _ensure_length(
    encoded: str, min_length: int, alphabet: str, guards: str, values_hash: int
) -> str:
    """Ensures the minimal hash length"""
    len_guards = len(guards)
    guard_index = (values_hash + ord(encoded[0])) % len_guards
    encoded = guards[guard_index] + encoded

    if len(encoded) < min_length:
        guard_index = (values_hash + ord(encoded[2])) % len_guards
        encoded += guards[guard_index]

    split_at = len(alphabet) // 2
    while len(encoded) < min_length:
        alphabet = _reorder(alphabet, alphabet)
        encoded = alphabet[split_at:] + encoded + alphabet[:split_at]
        excess = len(encoded) - min_length
        if excess > 0:
            from_index = excess // 2
            encoded = encoded[from_index : from_index + min_length]

    return encoded


def _encode(
    values: Iterable[int], salt: str, min_length: int, alphabet: str, separators: str, guards: str
) -> str:
    """Helper function that does the hash building without argument checks."""
    len_alphabet = len(alphabet)
    len_separators = len(separators)
    values_hash = sum(x % (i + 100) for i, x in enumerate(values))
    encoded = lottery = alphabet[values_hash % len(alphabet)]

    for i, value in enumerate(values):
        alphabet_salt = (lottery + salt + alphabet)[:len_alphabet]
        alphabet = _reorder(alphabet, alphabet_salt)
        last = _hash(value, alphabet)
        encoded += last
        value %= ord(last[0]) + i
        encoded += separators[value % len_separators]

    encoded = encoded[:-1]  # cut off last separator

    return (
        encoded
        if len(encoded) >= min_length
        else _ensure_length(encoded, min_length, alphabet, guards, values_hash)
    )


def _decode(hashid: str, salt: str, alphabet: str, separators: str, guards: str) -> Iterator[int]:
    """Helper method that restores the values encoded in a hashid without argument checks."""
    parts = tuple(_split(hashid, guards))
    hashid = parts[1] if 2 <= len(parts) <= 3 else parts[0]

    if not hashid:
        return

    lottery_char = hashid[0]
    hashid = hashid[1:]

    hash_parts = _split(hashid, separators)
    for part in hash_parts:
        alphabet_salt = (lottery_char + salt + alphabet)[: len(alphabet)]
        alphabet = _reorder(alphabet, alphabet_salt)
        yield _unhash(part, alphabet)


def _deprecated(func: Callable[_P, _T], name: str) -> Callable[_P, _T]:
    """A decorator that warns about deprecation when the passed-in function is invoked."""

    @functools.wraps(func)
    def with_warning(*args: _P.args, **kwargs: _P.kwargs) -> _T:
        msg = f"The {name} method is deprecated and will be removed in v2.*.*"
        warnings.warn(msg, DeprecationWarning)
        return func(*args, **kwargs)

    return with_warning


class Hashids:
    """Hashes and restores values using the "hashids" algorithm."""

    ALPHABET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"

    def __init__(self, salt: str = "", min_length: int = 0, alphabet: str = ALPHABET) -> None:
        """
        Initializes a Hashids object with salt, minimum length, and alphabet.

        :param salt: A string influencing the generated hash ids.
        :param min_length: The minimum length for generated hashes
        :param alphabet: The characters to use for the generated hash ids.
        """
        self._min_length = max(int(min_length), 0)
        self._salt = salt

        separators = "".join(x for x in "cfhistuCFHISTU" if x in alphabet)
        alphabet = "".join(
            x for i, x in enumerate(alphabet) if alphabet.index(x) == i and x not in separators
        )

        len_alphabet, len_separators = len(alphabet), len(separators)
        if len_alphabet + len_separators < 16:
            raise ValueError("Alphabet must contain at least 16 " "unique characters.")

        separators = _reorder(separators, salt)

        min_separators = _index_from_ratio(len_alphabet, RATIO_SEPARATORS)

        number_of_missing_separators = min_separators - len_separators
        if number_of_missing_separators > 0:
            separators += alphabet[:number_of_missing_separators]
            alphabet = alphabet[number_of_missing_separators:]
            len_alphabet = len(alphabet)

        alphabet = _reorder(alphabet, salt)
        num_guards = _index_from_ratio(len_alphabet, RATIO_GUARDS)
        if len_alphabet < 3:
            guards = separators[:num_guards]
            separators = separators[num_guards:]
        else:
            guards = alphabet[:num_guards]
            alphabet = alphabet[num_guards:]

        self._alphabet = alphabet
        self._guards = guards
        self._separators = separators

        # Support old API
        self.decrypt = _deprecated(self.decode, "decrypt")
        self.encrypt = _deprecated(self.encode, "encrypt")

    def encode(self, *values: int) -> str:
        """Builds a hash from the passed `values`.

        :param values: The values to transform into a hashid

        >>> hashids = Hashids('arbitrary salt', 16, 'abcdefghijkl0123456')
        >>> hashids.encode(1, 23, 456)
        '1d6216i30h53elk3'
        """
        if not (values and all(_is_uint(x) for x in values)):
            return ""

        return _encode(
            values, self._salt, self._min_length, self._alphabet, self._separators, self._guards
        )

    def decode(self, hashid: str) -> tuple[int, ...]:
        """Restore a tuple of numbers from the passed `hashid`.

        :param hashid: The hashid to decode

        >>> hashids = Hashids('arbitrary salt', 16, 'abcdefghijkl0123456')
        >>> hashids.decode('1d6216i30h53elk3')
        (1, 23, 456)
        """
        if not hashid or not isinstance(hashid, str):
            return ()
        try:
            numbers = tuple(
                _decode(hashid, self._salt, self._alphabet, self._separators, self._guards)
            )
            return numbers if hashid == self.encode(*numbers) else ()
        except ValueError:
            return ()

    def encode_hex(self, hex_str: str) -> str:
        """Converts a hexadecimal string (e.g. a MongoDB id) to a hashid.

        :param hex_str: The hexadecimal string to encodes

        >>> Hashids.encode_hex('507f1f77bcf86cd799439011')
        'y42LW46J9luq3Xq9XMly'
        """
        numbers = (int("1" + hex_str[i : i + 12], 16) for i in range(0, len(hex_str), 12))
        try:
            return self.encode(*numbers)
        except ValueError:
            return ""

    def decode_hex(self, hashid: str) -> str:
        """Restores a hexadecimal string (e.g. a MongoDB id) from a hashid.

        :param hashid: The hashid to decode

        >>> Hashids.decode_hex('y42LW46J9luq3Xq9XMly')
        '507f1f77bcf86cd799439011'
        """
        return "".join(("%x" % x)[1:] for x in self.decode(hashid))
