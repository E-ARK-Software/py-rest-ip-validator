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
"""Module covering tests for package structure errors."""
import os
import unittest

from ip_validation.infopacks import information_package as IP
from ip_validation.infopacks.rules import Severity
from tests.utils import contains_rule_id

class StructValidationTests(unittest.TestCase):
    """Unit tests covering structural validation of information packages, spcifically
    unpacking archived packages and establishing that the files and folders specified
    if the CSIP are present."""

    def test_check_package_root_single(self):
        """Dedicated test for package root detection errors."""
        ip_path = os.path.join(os.path.dirname(__file__), 'resources', 'ips', 'unpacked',
                               'single_file')
        details = IP.check_package_root(ip_path)
        self.assertTrue(details.structure_status == IP.StructureStatus.NotWellFormed,
                        'Expecting status NotWellFormed, not {}'.format(details.structure_status))
        val_errors = details.errors
        self.assertTrue(len(val_errors) == 1,
                        'Expecting 1 errors but found {}'.format(len(val_errors)))
        self.assertTrue(contains_rule_id(val_errors, "CSIPSTR1",
                                         severity=Severity.Error))

    def test_check_package_root_multi_dir(self):
        """Dedicated test for package root detection errors."""
        ip_path = os.path.join(os.path.dirname(__file__), 'resources', 'ips', 'unpacked',
                               'multi_dir')
        details = IP.check_package_root(ip_path)
        self.assertTrue(details.structure_status == IP.StructureStatus.NotWellFormed,
                        'Expecting status NotWellFormed, not {}'.format(details.structure_status))
        val_errors = details.errors
        self.assertTrue(len(val_errors) == 1,
                        'Expecting 1 errors but found {}'.format(len(val_errors)))
        self.assertTrue(contains_rule_id(val_errors, "CSIPSTR1",
                                         severity=Severity.Error))

    def test_check_package_root_multi_file(self):
        """Dedicated test for package root detection errors."""
        ip_path = os.path.join(os.path.dirname(__file__), 'resources', 'ips', 'unpacked',
                               'multi_file')
        details = IP.check_package_root(ip_path)
        self.assertTrue(details.structure_status == IP.StructureStatus.NotWellFormed,
                        'Expecting status NotWellFormed, not {}'.format(details.structure_status))
        val_errors = details.errors
        self.assertTrue(len(val_errors) == 1,
                        'Expecting 1 errors but found {}'.format(len(val_errors)))
        self.assertTrue(contains_rule_id(val_errors, "CSIPSTR1",
                                         severity=Severity.Error))

    def test_check_package_root_multi_var(self):
        """Dedicated test for package root detection errors."""
        ip_path = os.path.join(os.path.dirname(__file__), 'resources', 'ips', 'unpacked',
                               'multi_var')
        details = IP.check_package_root(ip_path)
        self.assertTrue(details.structure_status == IP.StructureStatus.NotWellFormed,
                        'Expecting status NotWellFormed, not {}'.format(details.structure_status))
        val_errors = details.errors
        self.assertTrue(len(val_errors) == 1,
                        'Expecting 1 errors but found {}'.format(len(val_errors)))
        self.assertTrue(contains_rule_id(val_errors, "CSIPSTR1",
                                         severity=Severity.Error))

    def test_single_file_archive(self):
        """Test a package that's just a compressed single file."""
        ip_path = os.path.join(os.path.dirname(__file__), 'resources', 'ips', 'struct',
                               'empty.zip')
        details = IP.validate_package_structure(ip_path)

    def test_minimal(self):
        """Test minimal IP with schemas, the basic no errors but with warnings package."""
        ip_path = os.path.join(os.path.dirname(__file__), 'resources', 'ips', 'minimal',
                               'minimal_IP_with_schemas.zip')
        details = IP.validate_package_structure(ip_path)
        self.assertTrue(details.structure_status == IP.StructureStatus.WellFormed,
                        'Expecting status WellFormed, not {}'.format(details.structure_status))
        val_errors = details.errors
        self.assertTrue(len(val_errors) == 3,
                        'Expecting 3 errors but found {}'.format(len(val_errors)))
        self.assertTrue(contains_rule_id(val_errors, "CSIPSTR12",
                                         severity=Severity.Warn))
        self.assertTrue(contains_rule_id(val_errors, "CSIPSTR13",
                                         severity=Severity.Warn))
        self.assertTrue(contains_rule_id(val_errors, "CSIPSTR15",
                                         severity=Severity.Warn))

    def test_nomets(self):
        """Test package with no METS.xml file"""
        ip_path = os.path.join(os.path.dirname(__file__), 'resources', 'ips', 'struct',
                               'no_mets.tar.gz')
        details = IP.validate_package_structure(ip_path)
        self.assertTrue(details.structure_status == IP.StructureStatus.NotWellFormed,
                        'Expecting status NotWellFormed, not {}'.format(details.structure_status))
        val_errors = details.errors
        self.assertTrue(len(val_errors) == 4,
                        'Expecting 4 errors but found {}'.format(len(val_errors)))
        self.assertTrue(contains_rule_id(val_errors, "CSIPSTR4"))
        self.assertTrue(contains_rule_id(val_errors, "CSIPSTR12",
                                         severity=Severity.Warn))
        self.assertTrue(contains_rule_id(val_errors, "CSIPSTR13",
                                         severity=Severity.Warn))
        self.assertTrue(contains_rule_id(val_errors, "CSIPSTR15",
                                         severity=Severity.Warn))

    def test_nomd(self):
        # test as root
        ip_path = os.path.join(os.path.dirname(__file__), 'resources', 'ips', 'struct',
                               'no_md.tar.gz')
        details = IP.validate_package_structure(ip_path)
        self.assertTrue(details.structure_status == IP.StructureStatus.WellFormed,
                        'Expecting status WellFormed, not {}'.format(details.structure_status))
        val_errors = details.errors
        self.assertTrue(len(val_errors) == 4,
                        'Expecting 4 errors but found {}'.format(len(val_errors)))
        self.assertTrue(contains_rule_id(val_errors, "CSIPSTR5",
                                         severity=Severity.Warn))
        self.assertTrue(contains_rule_id(val_errors, "CSIPSTR12",
                                         severity=Severity.Warn))
        self.assertTrue(contains_rule_id(val_errors, "CSIPSTR13",
                                         severity=Severity.Warn))
        self.assertTrue(contains_rule_id(val_errors, "CSIPSTR15",
                                         severity=Severity.Warn))

    def test_noschema(self):
        # test as root
        ip_path = os.path.join(os.path.dirname(__file__), 'resources', 'ips', 'struct',
                               'no_schemas.tar.gz')
        details = IP.validate_package_structure(ip_path)
        self.assertTrue(details.structure_status == IP.StructureStatus.WellFormed,
                        'Expecting status WellFormed, not {}'.format(details.structure_status))
        val_errors = details.errors
        for err in val_errors:
            print(err.rule_id)
        self.assertTrue(len(val_errors) == 4,
                        'Expecting 4 errors but found {}'.format(len(val_errors)))
        self.assertTrue(contains_rule_id(val_errors, "CSIPSTR12",
                                         severity=Severity.Warn))
        self.assertTrue(contains_rule_id(val_errors, "CSIPSTR13",
                                         severity=Severity.Warn))
        self.assertTrue(contains_rule_id(val_errors, "CSIPSTR15",
                                         severity=Severity.Warn))

    def test_nodata(self):
        # test as root
        ip_path = os.path.join(os.path.dirname(__file__), 'resources', 'ips', 'struct',
                               'no_data.tar.gz')
        details = IP.validate_package_structure(ip_path)
        self.assertTrue(details.structure_status == IP.StructureStatus.WellFormed,
                        'Expecting status WellFormed, not {}'.format(details.structure_status))
        val_errors = details.errors
        self.assertTrue(len(val_errors) == 4,
                        'Expecting 4 errors but found {}'.format(len(val_errors)))
        self.assertTrue(contains_rule_id(val_errors, "CSIPSTR11",
                                         severity=Severity.Warn))
        self.assertTrue(contains_rule_id(val_errors, "CSIPSTR12",
                                         severity=Severity.Warn))
        self.assertTrue(contains_rule_id(val_errors, "CSIPSTR13",
                                         severity=Severity.Warn))
        self.assertTrue(contains_rule_id(val_errors, "CSIPSTR15",
                                         severity=Severity.Warn))

    def test_noreps(self):
        ip_path = os.path.join(os.path.dirname(__file__), 'resources', 'ips', 'struct',
                               'no_reps.tar.gz')
        details = IP.validate_package_structure(ip_path)
        self.assertTrue(details.structure_status == IP.StructureStatus.WellFormed,
                        'Expecting status WellFormed, not {}'.format(details.structure_status))
        val_errors = details.errors
        for err in val_errors:
            print(err.rule_id)
        self.assertTrue(len(val_errors) == 1,
                        'Expecting 1 errors but found {}'.format(len(val_errors)))
        self.assertTrue(contains_rule_id(val_errors, "CSIPSTR9",
                                         severity=Severity.Warn))
