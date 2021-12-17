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
"""Structural requirements as a dictionary."""
from enum import Enum, unique
import os

from eark_ip.model import (
    Severity,
    TestResult,
    StructResults,
    StructStatus,
    Representation,
    PackageDetails
)

METS_NAME = 'METS.xml'
DATA = 'data'

DIR_NAMES = {
    'DATA': 'data',
    'DESC': 'descriptive',
    'DOCS': 'documentation',
    'META': 'metadata',
    'OTHR': 'other',
    'PRES': 'preservation',
    'REPS': 'representations',
    'SCHM': 'schemas'
}

@unique
class Level(Enum):
    """Enum covering information package validation statuses."""
    MAY = 'MAY'
    # Package has basic parse / structure problems and can't be validated
    SHOULD = 'SHOULD'
    # Package structure is OK
    MUST = 'MUST'

REQUIREMENTS = {
    1: {
           'id': 'CSIPSTR1',
           'level': Level.MUST,
           'message': """Any Information Package MUST be included within a single physical root """
              """folder (known as the “Information Package root folder”). For packages """
              """presented in an archive format, see CSIPSTR3, the archive MUST unpack to """
              """a single root folder."""
        },
    2: {
            'id': 'CSIPSTR2',
            'level': Level.SHOULD,
            'message': """The Information Package root folder SHOULD be named with the ID or """
               """name of the Information Package, that is the value of the package """
               """METS.xml’s root <mets> element’s @OBJID attribute."""
        },
    3: {
            'id': 'CSIPSTR3',
            'level': Level.MAY,
            'message': """The Information Package root folder MAY be compressed (for example by """
               """using TAR or ZIP). Which specific compression format to use needs to be """
               """stated in the Submission Agreement."""
        },
    4: {
            'id': 'CSIPSTR4',
            'level': Level.MUST,
            'message': """The Information Package root folder MUST include a file named """
               """METS.xml. This file MUST contain metadata that identifies the package, """
               """provides a high-level package description, and describes its structure, """
               """including pointers to constituent representations."""
        },
    5: {
            'id': 'CSIPSTR5',
            'level': Level.SHOULD,
            'message': """The Information Package root folder SHOULD include a folder named """
                       """metadata, which SHOULD include metadata relevant to the whole package."""
        },
    6: {
            'id': 'CSIPSTR6',
            'level': Level.SHOULD,
            'message': """If preservation metadata are available, they SHOULD be included """
                       """in sub-folder preservation."""
        },
    7: {
            'id': 'CSIPSTR7',
            'level': Level.SHOULD,
            'message': """If descriptive metadata are available, they SHOULD be included in """
               """sub-folder descriptive."""
        },
    8: {
           'id': 'CSIPSTR8',
           'level': Level.MAY,
           'message': """If any other metadata are available, they MAY be included in """
              """separate sub-folders, for example an additional folder named other."""
       },
    9: {
           'id': 'CSIPSTR9',
           'level': Level.SHOULD,
           'message': """The Information Package folder SHOULD include a folder named """
              """representations."""
       },
    10: {
            'id': 'CSIPSTR10',
            'level': Level.SHOULD,
            'message': """The representations folder SHOULD include a sub-folder for each """
                """individual representation (i.e. the “representation folder”). Each """
                """representation folder should have a string name that is unique within """
                """the package scope. For example the name of the representation and/or its """
                """creation date might be good candidates as a representation sub-folder """
                """name."""
        },
    11: {
            'id': 'CSIPSTR11',
            'level': Level.SHOULD,
            'message': """The representation folder SHOULD include a sub-folder named data """
                """which MAY include all data constituting the representation."""
        },
    12: {
            'id': 'CSIPSTR12',
            'level': Level.SHOULD,
            'message': """The representation folder SHOULD include a metadata file named """
                """METS.xml which includes information about the identity and structure of """
                """the representation and its components. The recommended best practice is """
                """to always have a METS.xml in the representation folder."""
        },
    13: {
            'id': 'CSIPSTR13',
            'level': Level.SHOULD,
            'message': """The representation folder SHOULD include a sub-folder named metadata """
                """which MAY include all metadata about the specific representation."""
        },
    14: {
            'id': 'CSIPSTR14',
            'level': Level.MAY,
            'message': """The Information Package MAY be extended with additional sub-folders."""
        },
    15: {
            'id': 'CSIPSTR15',
            'level': Level.SHOULD,
            'message': """We recommend including all XML schema documents for any structured """
                """metadata within package. These schema documents SHOULD be placed in a """
                """sub-folder called schemas within the Information Package root folder """
                """and/or the representation folder."""
        },
    16: {
            'id': 'CSIPSTR16',
            'level': Level.SHOULD,
            'message': """We recommend including any supplementary documentation for the """
                """package or a specific representation within the package. Supplementary """
                """documentation SHOULD be placed in a sub-folder called documentation """
                """within the Information Package root folder and/or the representation """
                """folder."""
        }
}

def severity_from_level(level):
    """Return the correct test result severity from a Level instance."""
    if level == Level.MUST:
        return Severity.ERROR
    if level == Level.SHOULD:
        return Severity.WARN
    return Severity.INFO

def severity_from_id(requirement_id):
    """Return the correct test result severity from a Level instance."""
    level = REQUIREMENTS[requirement_id]['level']
    if level == Level.MUST:
        return Severity.ERROR
    if level == Level.SHOULD:
        return Severity.WARN
    return Severity.INFO

def test_result_from_id(requirement_id, location, message=None):
    """Return a TestResult instance created from the requirment ID and location."""
    req = REQUIREMENTS[requirement_id]
    test_msg = message if message else req['message']
    return TestResult(req['id'], location, test_msg, severity_from_level(req['level']))

def _mets_tests(path, filename):
    if filename.casefold() != filename.casefold():
        return False
    if filename != METS_NAME:
        # TODO: Name-shadowing, case-insensitive match for METS.xml only
        return False
    return os.path.isfile(path)

def _test_severity(base, to_test):
    if base == Severity.INFO:
        return True
    if to_test == Severity.INFO:
        return False
    if base == Severity.WARN:
        return True
    if to_test == Severity.WARN:
        return False
    return to_test == Severity.ERROR

class StructTests():
    """Encapsulates the set of tests carried out on folder structure."""
    def __init__(self, dir_to_scan):
        self.folders, self.files = _folders_and_files(dir_to_scan)
        if DIR_NAMES['META'] in self.folders:
            self.md_folders, _ = _folders_and_files(os.path.join(dir_to_scan, DIR_NAMES['META']))
        else:
            self.md_folders = set()

    def has_data(self):
        """Returns True if the package/representation has a structure folder."""
        return DIR_NAMES['DATA'] in self.folders

    def has_descriptive_md(self):
        """Returns True if the package/representation has a descriptive metadata folder."""
        return DIR_NAMES['DESC'] in self.md_folders

    def has_documentation(self):
        """Returns True if the package/representation has a documentation folder."""
        return DIR_NAMES['DOCS'] in self.folders

    def has_mets(self):
        """Returns True if the package/representation has a root METS.xml file."""
        return METS_NAME in self.files

    def has_metadata(self):
        """Returns True if the package/representation has a metadata folder."""
        return DIR_NAMES['META'] in self.folders

    def has_other_md(self):
        """Returns True if the package/representation has extra metadata folders
        after preservation and descriptive."""
        md_folder_count = len(self.md_folders)
        if self.has_preservation_md():
            md_folder_count-=1
        if self.has_descriptive_md():
            md_folder_count-=1
        return md_folder_count > 0

    def has_preservation_md(self):
        """Returns True if the package/representation has a preservation metadata folder."""
        return DIR_NAMES['PRES'] in self.md_folders

    def has_representations(self):
        """Returns True if the package/representation has a representations folder."""
        return DIR_NAMES['REPS'] in self.folders

    def has_schemas(self):
        """Returns True if the package/representation has a schemas folder."""
        return DIR_NAMES['SCHM'] in self.folders

class PackageStructTests():
    def __init__(self, dir_to_scan, is_archive=False):
        self.name = os.path.basename(dir_to_scan)
        self.struct_tests = StructTests(dir_to_scan)
        self.representations = {}
        self.is_archive = is_archive
        _reps = os.path.join(dir_to_scan, DIR_NAMES['REPS'])
        if os.path.isdir(_reps):
            for entry in  os.listdir(_reps):
                self.representations[entry] = StructTests(os.path.join(_reps, entry))

    def get_test_results(self):
        results = self.get_root_results()
        results = results + self.get_package_results()

        for name, tests in self.representations.items():
            location = 'Representation {}'.format(name)
            if not tests.has_data():
                results.append(test_result_from_id(11, location))
            if not tests.has_mets():
                results.append(test_result_from_id(12, location))
            if not tests.has_metadata():
                results.append(test_result_from_id(13, location))
        return StructResults(self.get_status(results), results)

    def get_representations(self):
        reps = []
        for rep in self.representations.keys():
            reps.append(Representation(name=rep))
        return reps

    def get_root_results(self):
        results = []
        if not self.is_archive:
            results.append(test_result_from_id(3, self.name))
        if not self.struct_tests.has_mets():
            results.append(test_result_from_id(4, self.name))
        if not self.struct_tests.has_metadata():
            results.append(test_result_from_id(5, self.name))
        if not self.struct_tests.has_preservation_md():
            results.append(test_result_from_id(6, self.name))
        if not self.struct_tests.has_descriptive_md():
            results.append(test_result_from_id(7, self.name))
        if not self.struct_tests.has_other_md():
            results.append(test_result_from_id(8, self.name))
        if not self.struct_tests.has_representations():
            results.append(test_result_from_id(9, self.name))
        return results

    def get_package_results(self):
        results = self.check_schema()
        results += self.check_docs()
        return results

    def check_docs(self):
        results = []
        if not self.struct_tests.has_documentation():
            has_dox = False
            for tests in self.representations.values():
                if not has_dox:
                    has_dox = tests.has_documentation()
            if not has_dox:
                results.append(test_result_from_id(16, self.name))
        return results

    def check_schema(self):
        results = []
        if not self.struct_tests.has_schemas():
            has_schema = False
            for tests in self.representations.values():
                if not has_schema:
                    has_schema = tests.has_schemas()
            if not has_schema:
                results.append(test_result_from_id(15, self.name))
        return results

    def get_struct_map(self):
        struct_map = self.representations.copy()
        struct_map['root'] = self.struct_tests
        return struct_map

    @classmethod
    def get_status(cls, results):
        status = StructStatus.WELLFORMED
        for result in results:
            if result.severity == Severity.ERROR:
                status = StructStatus.NOTWELLFORMED
        return status


def _folders_and_files(dir_to_scan):
    folders = set()
    files = set()
    if os.path.isdir(dir_to_scan):
        for entry in os.listdir(dir_to_scan):
            path = os.path.join(dir_to_scan, entry)
            if os.path.isfile(path):
                files.add(entry)
            elif os.path.isdir(path):
                folders.add(entry)
    return folders, files

def get_multi_root_results(name):
    return StructResults(StructStatus.NOTWELLFORMED, [ test_result_from_id(1, name) ])

def get_bad_path_results(path):
    return StructResults(StructStatus.NOTWELLFORMED, [ test_result_from_id(1, path) ])

def validate(to_validate, is_archive=False):
    struct_tests = PackageStructTests(to_validate, is_archive)
    return struct_tests.get_test_results().status == StructStatus.WELLFORMED, struct_tests
