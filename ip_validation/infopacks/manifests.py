#!/usr/bin/env python
# coding=UTF-8
#
# E-ARK Validation
# Copyright (C) 2019
# All rights reserved.
#
# Licensed to the E-ARK project under one
# or more contributor license agreements. See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership. The E-ARK project licenses
# this file to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License. You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied. See the License for the
# specific language governing permissions and limitations
# under the License.
#
"""Module for types and logic covering information package manifests."""
from enum import Enum, unique
import hashlib
import os

BUFF_SIZE = 1024 * 64

@unique
class DigestAlgorithm(Enum):
    """Enum class for supported digest algorithms."""
    Unknown = 1
    MD5 = 2
    SHA1 = 3
    SHA256 = 4
    SHA512 = 5

class Source(Enum):
    """Enum class for source of manifests."""
    Unknown = 1
    METS = 2
    Directory = 3
    Archive = 4

class Digest():
    """Calculated digest value, includes hex value and algorithm id."""
    MD5_EMPTY = 'd41d8cd98f00b204e9800998ecf8427e'
    SHA1_EMPTY = 'da39a3ee5e6b4b0d3255bfef95601890afd80709'
    SHA256_EMPTY = 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'
    SHA512_EMPTY = \
        'cf83e1357eefb8bdf1542850d66d8007d620e4050b5715dc83f4a921d36ce9ce47d0d13c5d85f2b0ff8318d2877eec2f63b931bd47417a81a538327af927da3e'
    def __init__(self, algorithm=DigestAlgorithm.Unknown, value=""):
        self.algorithm = algorithm
        self._value = value

    @property
    def algorithm(self):
        """Return the name of the digest algorithm used to calculate the value."""
        return self._algorithm

    @algorithm.setter
    def algorithm(self, value):
        """Set the algorithm digest to a legal value."""
        if not value in list(DigestAlgorithm):
            raise ValueError("Illegal digest algorithm value.")
        self._algorithm = value

    @property
    def value(self):
        """Returns the hex digest value."""
        return self._value

    @staticmethod
    def from_file(algorithm, file):
        """Create a manfest entry from the passed file."""
        if not os.path.isfile(file):
            raise ValueError("Passed value {} must be an existing file".format(file))
        if algorithm not in list(DigestAlgorithm):
            raise ValueError("Illegal digest algorithm value {}".format(algorithm))
        return Digest.calculate(algorithm, file)

    @staticmethod
    def calculate(algorithm, to_hash):
        """Calculate the digest value according to the passed alg."""
        if algorithm == DigestAlgorithm.MD5:
            return Digest.md5(to_hash)
        if algorithm == DigestAlgorithm.SHA1:
            return Digest.sha1(to_hash)
        if algorithm == DigestAlgorithm.SHA256:
            return Digest.sha256(to_hash)
        if algorithm == DigestAlgorithm.SHA512:
            return Digest.sha512(to_hash)
        return Digest(DigestAlgorithm.Unknown, "")

    @staticmethod
    def md5(to_hash):
        """Calculate the MD5 of the passed file and return a digest value."""
        md5 = hashlib.md5()
        digest = Digest._calc_digest(to_hash, md5)
        return Digest(DigestAlgorithm.MD5, digest)

    @staticmethod
    def sha1(to_hash):
        """Calculate the SHA1 of the passed file and return a digest value."""
        sha1 = hashlib.sha1()
        digest = Digest._calc_digest(to_hash, sha1)
        return Digest(DigestAlgorithm.SHA1, digest)

    @staticmethod
    def sha256(to_hash):
        """Calculate the SHA256 of the passed file and return a digest value."""
        sha256 = hashlib.sha256()
        digest = Digest._calc_digest(to_hash, sha256)
        return Digest(DigestAlgorithm.SHA256, digest)

    @staticmethod
    def sha512(to_hash):
        """Calculate the SHA512 of the passed file and return a digest value."""
        sha512 = hashlib.sha512()
        digest = Digest._calc_digest(to_hash, sha512)
        return Digest(DigestAlgorithm.SHA512, digest)

    @staticmethod
    def _calc_digest(to_hash, hasher):
        with open(to_hash, 'rb') as source:
            while True:
                data = source.read(BUFF_SIZE)
                if not data:
                    break
                hasher.update(data)
        return hasher.hexdigest()

class ManifestEntry():
    """Hold a manifest entry for a package file, path, size and list of digest values."""
    def __init__(self, path, size=0, digests=None):
        self._path = path
        self._size = size
        if digests is None:
            self._digests = []
        else:
            self._digests = digests

    @property
    def path(self):
        """Return the entry's path."""
        return self._path

    @property
    def name(self):
        """Get the file name of the entry."""
        return os.path.basename(self._path)

    @property
    def size(self):
        """Return the entry's size in bytes."""
        return self._size

    @property
    def digests(self):
        """Return the list of calculated digest values."""
        return self._digests

    @digests.setter
    def digests(self, value):
        """Sets the list of digests values."""
        self._digests.append(value)

    @staticmethod
    def from_file(file, algorithm=DigestAlgorithm.SHA1):
        """Create a manfest entry from the passed file."""
        digests = []
        digests.append(Digest.from_file(algorithm, file))
        size = os.path.getsize(file)
        return ManifestEntry(file, size, digests)

class Manifest():
    """Holds a full manifest of files."""
    def __init__(self, source, entries=None):
        self.source = source
        if entries is None:
            self._entries = []
        else:
            self._entries = entries

    @property
    def source(self):
        """Return the source of the manifest."""
        return self._source

    @source.setter
    def source(self, value):
        """Set the source of the manifest from allowed values."""
        if value not in list(Source):
            raise ValueError("Illegal source value")
        self._source = value

    def add_entry(self, value):
        """Add and entry to the list."""
        self._source.append(value)

    @property
    def entries(self):
        """Returns the list of entries."""
        return self._entries

    @entries.setter
    def entries(self, values):
        """Add a list of entries."""
        self._entries.apppend(values)
