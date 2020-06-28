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
import os

from ip_validation.infopacks.digests import DigestAlgorithm, Digest

@unique
class Source(Enum):
    """Enum class for source of manifests."""
    Unknown = 1
    METS = 2
    Directory = 3
    Archive = 4

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
