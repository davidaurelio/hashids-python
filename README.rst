========================
hashids for Python 2.5–3
========================

Website: http://www.hashids.org/

Generate short hashes from unsigned integers (like YouTube and Bitly).

- obfuscate database IDs
- use them as forgotten password hashes
- invitation codes
- store shard numbers

Hashids was designed for use in URL shortening, tracking stuff, validating accounts or making pages private. Instead of showing items as ``1``, ``2``, or ``3``, you could show them as ``b9iLXiAa``, ``EATedTBy``, and ``Aaco9cy5``. Hashes depend on your salt value.

Usage
=====

Import the constructor from the ``hashids`` module:

.. code:: python

  from hashids import Hashids
  hashids = Hashids()

Basic Usage
-----------

Encrypt a single integer:

.. code:: python

  hashid = hashids.encrypt(123) # 'AjL'

Decrypt a hash:

.. code:: python

  ints = hashids.decrypt('b9a') # (456,)

To encrypt several integers, pass them all at once:

.. code:: python

  hashid = hashids.encrypt(123, 456, 789) # 'qa9t96h7G'

Decryption is done the same way:

.. code:: python

  ints = hashids.decrypt('yn8t46hen') # (517, 729, 185)

Using A Custom Salt
-------------------

Hashids supports personalizing your hashes by accepting a salt value. If you don’t want others to decrypt your hashes, provide a unique string to the constructor.

.. code:: python

  hashids = Hashids(salt='this is my salt 1')
  hashid = hashids.encrypt(123) # 'rnR'

The generated hash changes whenever the salt is changed:

.. code:: python

  hashids = Hashids(salt='this is my salt 2')
  hashid = hashids.encrypt(123) # 'XBn'

A salt string between 6 and 32 characters provides decent randomization.

Controlling Hash Length
-----------------------

By default, hashes are going to be the shortest possible. One reason you might want to increase the hash length is to obfuscate how large the integer behind the hash is.

This is done by passing the minimum hash length to the constructor. Hashes are padded with extra characters to make them seem longer.

.. code:: python

  hashids = Hashids(min_length=16)
  hashid = Hashids.encrypt(1) # 'Ee7uE4iyEiEG7ued'

Using A Custom Alphabet
-----------------------

It’s possible to set a custom alphabet for your hashes. The default alphabet is ``'xcS4F6h89aUbideAI7tkynuopqrXCgTE5GBKHLMjfRsz'``.

To have only lowercase letters in your hashes, pass in the following custom alphabet:

.. code:: python

  hashids = Hashids(alphabet='abcdefghijklmnopqrstuvwxyz')
  hashid = hashids.encrypt(123456789) # 'dpovunuo'

A custom alphabet must contain at least 4 letters, but should contain at least 16 characters.

#%@&
----

This code was written with the intent of placing generated hashes in visible places – like the URL.

Therefore, the algorithm tries to avoid generating most common English curse words by never placing the following letters next to each other: **c, C, s, S, f, F, h, H, u, U, i, I, t, T.**

Collisions
----------

There are no collisions. Your generated hashes should be unique.

Decryptable Hash ¿qué?
----------------------

A true cryptographic hash cannot be decrypted. However, to keep things simple the word hash is used loosely to refer to the random set of characters that are generated. Like a YouTube hash.
