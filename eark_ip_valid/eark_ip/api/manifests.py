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
"""
Factory methods for the manifest classes.
"""
import hashlib
import os

from eark_ip.api import MODEL

BLOCKSIZE = 1024 * 64

class Checksums():
    """Handy methods for creating Checksum instances."""
    @staticmethod
    def from_file(to_checksum, algorithm=MODEL.ChecksumAlg.SHA1, blocksize=BLOCKSIZE):
        """
        Returns a Checksum instance calculated from the passed file to_checksum.
        The algorithm is selectable and defaults to MD5.
        """
        hash_alg = _alg_instance(algorithm)
        with open(to_checksum, "rb") as _f:
            for chunk in iter(lambda: _f.read(blocksize), b""):
                hash_alg.update(chunk)
        return MODEL.Checksum(algorithm=algorithm, value=hash_alg.hexdigest())

    @staticmethod
    def from_data(to_checksum, algorithm=MODEL.ChecksumAlg.MD5):
        """
        Returns a Checksum instance calculated from the passed data to_checksum.
        The algorithm is selectable and defaults to MD5.
        """
        hash_alg = _alg_instance(algorithm)
        hash_alg.update(to_checksum)
        return MODEL.Checksum(algorithm=algorithm, value=hash_alg.hexdigest())

def _alg_instance(algorithm=MODEL.ChecksumAlg.MD5):
    if algorithm == MODEL.ChecksumAlg.SHA1:
        return hashlib.sha1()
    if algorithm == MODEL.ChecksumAlg.SHA256:
        return hashlib.sha256()
    if algorithm == MODEL.ChecksumAlg.SHA512:
        return hashlib.sha512()
    return hashlib.md5()

def entry_from_file(file_path, checksum_algs=None, entry_path=None):
    """Return a ManifestEntry based on a file path."""
    checksum_algs = checksum_algs if checksum_algs else [ MODEL.ChecksumAlg.MD5 ]
    entry_path = entry_path if entry_path else file_path
    size = os.path.getsize(file_path)
    checksums = [
        Checksums.from_file(file_path, alg) for alg in checksum_algs
    ]
    return MODEL.ManifestEntry(entry_path, size, checksums)

def manifest_from_directory(root_dir, checksum_algs=None, recurse=True):
    """Return a manfiest instance derived from scanning recursively from a root directory."""
    entries = entries_from_dir(root_dir, checksum_algs, recurse)
    summary = summary_from_entries(entries)
    return MODEL.Manifest(source="filesystem", summary=summary, entries=entries)

def summary_from_entries(entries=None):
    """ Returns a ManifestSummary created from the passed manifest entries."""
    entries = entries if entries else []
    total_size = 0
    file_count = 0
    for entry in entries:
        file_count += 1
        total_size += entry.size
    return MODEL.ManifestSummary(file_count=file_count, total_size=total_size)

def entries_from_dir(root_dir, checksum_algs=None, recurse=True):
    """Returns a List of ManifestEntrys created by walking the passed directory tree."""
    entries = []
    dir_path = ''
    for root, dirs, files in os.walk(root_dir):
        if recurse:
            for directory in dirs:
                dir_path = os.path.join(dir_path, directory) if dir_path else directory
        for file in files:
            entry_path = os.path.join(os.path.relpath(root, root_dir), file)
            entries.append(entry_from_file(os.path.join(root, file), checksum_algs, entry_path))
    return entries
