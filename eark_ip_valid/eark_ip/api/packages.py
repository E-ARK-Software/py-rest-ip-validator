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
Factory methods for the package classes.
"""
import os
import shutil
from pathlib import Path
import tarfile
import tempfile
import zipfile
import uuid

from eark_ip.api import manifests
from eark_ip.api import structure, metadata
from eark_ip.model import PackageDetails, ValidationReport, InformationPackage

class ArchivePackageHandler():
    """Class to handle archive / compressed information packages."""
    def __init__(self, unpack_root=tempfile.gettempdir()):
        self._unpack_root = unpack_root

    @property
    def unpack_root(self):
        """Returns the root directory for archive unpacking."""
        return self._unpack_root

    def unpack_package(self, to_unpack, dest=None):
        """Unpack an archived package to a destination (defaults to tempdir).
        returns the destination folder."""
        if not os.path.isfile(to_unpack) or not self.is_archive(to_unpack):
            raise ValueError('Parameter "to_unpack": {} does not reference a file'
                'of known archive format (zip or tar).'.format(to_unpack))
        sha1 = manifests.Checksums.from_file(to_unpack)
        dest_root = dest if dest else self.unpack_root
        destination = os.path.join(dest_root, sha1.value)
        self._unpack(to_unpack, destination)

        children = []
        for path in Path(destination).iterdir():
            children.append(path)
        if len(children) != 1:
            # Dir unpacks to more than a single folder
            shutil.rmtree(destination)
            raise ValidationError('Unpacking archive yields'
                                  '{} children.'.format(len(children)))
        if not os.path.isdir(children[0]):
            shutil.rmtree(destination)
            raise ValidationError('Unpacking archive yields'
                                  'a single file child {}.'.format(children[0]))
        return children[0]

    @staticmethod
    def _unpack(to_unpack, destination):
        if zipfile.is_zipfile(to_unpack):
            with zipfile.ZipFile(to_unpack) as zip_ip:
                zip_ip.extractall(path=destination)
        elif tarfile.is_tarfile(to_unpack):
            with tarfile.open(to_unpack) as tar_ip:
                tar_ip.extractall(path=destination)

    @staticmethod
    def is_archive(to_test):
        """Return True if the file is a recognised archive type, False otherwise."""
        if os.path.isfile(to_test):
            if zipfile.is_zipfile(to_test):
                return True
            return tarfile.is_tarfile(to_test)
        return False

def validate(to_validate, check_metadata=True, is_archive=False):
    """Returns the validation report that results from validating the path
    to_validate as a folder. The method does not validate archive files."""
    struct_valid, struct_checker = structure.validate(to_validate, is_archive)
    if not struct_valid or not check_metadata:
        package = _get_info_pack(name=os.path.basename(to_validate))
        return ValidationReport(uid=uuid.uuid4(), package=package,
                                structure=struct_checker.get_test_results())
    prof_details, md_results = metadata.validate_ip(to_validate, struct_checker.get_struct_map())
    package = _get_info_pack(name=os.path.basename(to_validate), profile=prof_details)
    return ValidationReport(uid=uuid.uuid4(), package=package,
                            structure=struct_checker.get_test_results(),
                            metadata=md_results)

class ValidationError(Exception):
    """Exception used to mark validation error when unpacking archive."""

class PackageValidator():
    """Class for performing full package validation."""
    _archive_handler = ArchivePackageHandler()
    def __init__(self, package_path, check_metadata=True):
        self._orig_path = Path(package_path)
        self._name = os.path.basename(package_path)
        if not os.path.exists(package_path):
            self._report = _report_from_bad_path(self.name, package_path)
            return
        self._report = None
        self._is_archive = False
        if os.path.isdir(package_path):
            # If a directory
            self._to_proc = self._orig_path.absolute()
        elif ArchivePackageHandler.is_archive(package_path):
            self._is_archive = True
            try:
                self._to_proc = Path(self._archive_handler.unpack_package(package_path)).absolute()
            except ValidationError:
                self._report = _report_from_unpack_except(self.name, package_path)
                return
        elif self._name == 'METS.xml':
            mets_path = Path(package_path)
            self._to_proc = mets_path.parent.absolute()
            self._name = os.path.basename(self._to_proc)
        else:
            # If not an archive we can't process
            self._report = _report_from_bad_path(self.name, package_path)
            return
        self._report = validate(self._to_proc, check_metadata, self.is_archive)

    @property
    def original_path(self):
        """Returns the original parsed path."""
        return self._orig_path

    @property
    def is_archive(self):
        """Returns the original parsed path."""
        return self._is_archive

    @property
    def name(self):
        """Returns the package name."""
        return self._name

    @property
    def validation_report(self):
        """Returns the valdiation report for the package."""
        return self._report

def _report_from_unpack_except(name, package_path):
    struct_results = structure.get_multi_root_results(package_path)
    package = _get_info_pack(name)
    return ValidationReport(uid=uuid.uuid4(), package=package, structure=struct_results)

def _report_from_bad_path(name, package_path):
    struct_results = structure.get_bad_path_results(package_path)
    package = _get_info_pack(name)
    return ValidationReport(uid=uuid.uuid4(), package=package, structure=struct_results)

def _get_info_pack(name, profile=None):
    pkg_dets =  PackageDetails(name=name)
    return InformationPackage(details=pkg_dets, profile=profile)
