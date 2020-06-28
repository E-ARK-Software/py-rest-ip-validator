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
"""Module to cover the handling of information packages in archive formats."""
import os
import tarfile
import tempfile
import zipfile

from ip_validation.infopacks.digests import Digest
from ip_validation.infopacks.exceps import PackageStructError

class ArchivePackageHandler():
    """Class to handle archive / compressed information packages."""
    def __init__(self, unpack_root=tempfile.gettempdir()):
        self._unpack_root = unpack_root

    @property
    def unpack_root(self):
        """Returns the root directory for archive unpacking."""
        return self._unpack_root

    @staticmethod
    def is_archive(to_test):
        """Return True if the file is a recognised archive type, False otherwise."""
        if zipfile.is_zipfile(to_test):
            return True
        return tarfile.is_tarfile(to_test)

    def unpack_package(self, to_unpack, dest=None):
        """Unpack an archived package to a destination (defaults to tempdir)."""
        if not os.path.isfile(to_unpack) or not self.is_archive(to_unpack):
            raise PackageStructError("File is not an archive file.")
        sha1 = Digest.sha1(to_unpack)
        dest_root = dest if dest else self.unpack_root
        destination = os.path.join(dest_root, sha1.value)
        if zipfile.is_zipfile(to_unpack):
            zip_ip = zipfile.ZipFile(to_unpack)
            zip_ip.extractall(path=destination)
        elif tarfile.is_tarfile(to_unpack):
            tar_ip = tarfile.open(to_unpack)
            tar_ip.extractall(path=destination)
        return destination
