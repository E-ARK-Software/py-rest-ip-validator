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
import os
import unittest

from ip_validation.infopacks import information_package as IP
from ip_validation.infopacks.rules import Severity

class StructValidationTests(unittest.TestCase):
    def test_manifest_nomets(self):
        # test as root
        man_no_mets = IP.PackageManifest("no_mets", has_mets=False)
        val_errors = IP.validate_manifest(man_no_mets)
        self.assertTrue(len(val_errors) == 1)
        self.assertTrue(self._contains_rule_id(val_errors, "CSIPSTR4"))
        val_errors = IP.validate_manifest(man_no_mets, is_root=False)
        self.assertTrue(len(val_errors) == 2)
        self.assertTrue(self._contains_rule_id(val_errors, "CSIPSTR12",
                                               severity=Severity.Warn))
        self.assertTrue(self._contains_rule_id(val_errors, "CSIPSTR11",
                                               severity=Severity.Warn))

    def test_manifest_nomd(self):
        # test as root
        man_no_md = IP.PackageManifest("no_md", has_md=False)
        val_errors = IP.validate_manifest(man_no_md)
        self.assertTrue(len(val_errors) == 1)
        self.assertTrue(self._contains_rule_id(val_errors, "CSIPSTR5",
                                               severity=Severity.Warn))
        val_errors = IP.validate_manifest(man_no_md, is_root=False)
        self.assertTrue(len(val_errors) == 2)
        self.assertTrue(self._contains_rule_id(val_errors, "CSIPSTR13",
                                               severity=Severity.Warn))
        self.assertTrue(self._contains_rule_id(val_errors, "CSIPSTR11",
                                               severity=Severity.Warn))

    def test_manifest_noschema(self):
        # test as root
        man_no_schema = IP.PackageManifest("no_schema", has_schema=False)
        val_errors = IP.validate_manifest(man_no_schema)
        self.assertTrue(len(val_errors) == 1)
        self.assertTrue(self._contains_rule_id(val_errors, "CSIPSTR15",
                                               severity=Severity.Warn))
        val_errors = IP.validate_manifest(man_no_schema, is_root=False)
        self.assertTrue(len(val_errors) == 2)
        self.assertTrue(self._contains_rule_id(val_errors, "CSIPSTR15",
                                               severity=Severity.Warn))
        self.assertTrue(self._contains_rule_id(val_errors, "CSIPSTR11",
                                               severity=Severity.Warn))

    def test_manifest_data(self):
        # test as root
        man_data = IP.PackageManifest("data", has_data=True)
        val_errors = IP.validate_manifest(man_data)
        self.assertTrue(len(val_errors) == 0)
        val_errors = IP.validate_manifest(man_data, is_root=False)
        self.assertTrue(len(val_errors) == 0)

    def test_manifest_noreps(self):
        man_no_reps = IP.PackageManifest("no_reps", has_reps=False)
        val_errors = IP.validate_manifest(man_no_reps)
        self.assertTrue(len(val_errors) == 1)
        self.assertTrue(self._contains_rule_id(val_errors, "CSIPSTR9",
                                               severity=Severity.Warn))
        val_errors = IP.validate_manifest(man_no_reps, is_root=False)
        self.assertTrue(len(val_errors) == 1)
        self.assertTrue(self._contains_rule_id(val_errors, "CSIPSTR11",
                                               severity=Severity.Warn))

    def test_minimal(self):
        # test as root
        ip_path = os.path.join(os.path.dirname(__file__), 'resources', 'minimal_IP_with_schemas.zip')
        details = IP.validate_package_structure(ip_path)
        self.assertTrue(details.package_status == IP.PackageStatus.WellFormed,
                        'Expecting status WellFormed, not {}'.format(details.package_status))
        val_errors = details.errors
        self.assertTrue(len(val_errors) == 3, 'Expecting 3 errors but found {}'.format(len(val_errors)))
        self.assertTrue(self._contains_rule_id(val_errors, "CSIPSTR12",
                                               severity=Severity.Warn))
        self.assertTrue(self._contains_rule_id(val_errors, "CSIPSTR13",
                                               severity=Severity.Warn))
        self.assertTrue(self._contains_rule_id(val_errors, "CSIPSTR15",
                                               severity=Severity.Warn))

    def test_nomets(self):
        # test as root
        ip_path = os.path.join(os.path.dirname(__file__), 'resources', 'no_mets.tar.gz')
        details = IP.validate_package_structure(ip_path)
        self.assertTrue(details.package_status == IP.PackageStatus.NotWellFormed,
                        'Expecting status NotWellFormed, not {}'.format(details.package_status))
        val_errors = details.errors
        self.assertTrue(len(val_errors) == 4, 'Expecting 4 errors but found {}'.format(len(val_errors)))
        self.assertTrue(self._contains_rule_id(val_errors, "CSIPSTR4"))
        self.assertTrue(self._contains_rule_id(val_errors, "CSIPSTR12",
                                               severity=Severity.Warn))
        self.assertTrue(self._contains_rule_id(val_errors, "CSIPSTR13",
                                               severity=Severity.Warn))
        self.assertTrue(self._contains_rule_id(val_errors, "CSIPSTR15",
                                               severity=Severity.Warn))

    def test_nomd(self):
        # test as root
        ip_path = os.path.join(os.path.dirname(__file__), 'resources', 'no_md.tar.gz')
        details = IP.validate_package_structure(ip_path)
        self.assertTrue(details.package_status == IP.PackageStatus.WellFormed,
                        'Expecting status WellFormed, not {}'.format(details.package_status))
        val_errors = details.errors
        self.assertTrue(len(val_errors) == 4, 'Expecting 4 errors but found {}'.format(len(val_errors)))
        self.assertTrue(self._contains_rule_id(val_errors, "CSIPSTR5",
                                               severity=Severity.Warn))
        self.assertTrue(self._contains_rule_id(val_errors, "CSIPSTR12",
                                               severity=Severity.Warn))
        self.assertTrue(self._contains_rule_id(val_errors, "CSIPSTR13",
                                               severity=Severity.Warn))
        self.assertTrue(self._contains_rule_id(val_errors, "CSIPSTR15",
                                               severity=Severity.Warn))

    def test_noschema(self):
        # test as root
        ip_path = os.path.join(os.path.dirname(__file__), 'resources', 'no_schemas.tar.gz')
        details = IP.validate_package_structure(ip_path)
        self.assertTrue(details.package_status == IP.PackageStatus.WellFormed,
                        'Expecting status WellFormed, not {}'.format(details.package_status))
        val_errors = details.errors
        for err in val_errors:
            print(err.rule_id)
        self.assertTrue(len(val_errors) == 4, 'Expecting 4 errors but found {}'.format(len(val_errors)))
        self.assertTrue(self._contains_rule_id(val_errors, "CSIPSTR12",
                                               severity=Severity.Warn))
        self.assertTrue(self._contains_rule_id(val_errors, "CSIPSTR13",
                                               severity=Severity.Warn))
        self.assertTrue(self._contains_rule_id(val_errors, "CSIPSTR15",
                                               severity=Severity.Warn))

    def test_nodata(self):
        # test as root
        ip_path = os.path.join(os.path.dirname(__file__), 'resources', 'no_data.tar.gz')
        details = IP.validate_package_structure(ip_path)
        self.assertTrue(details.package_status == IP.PackageStatus.WellFormed,
                        'Expecting status WellFormed, not {}'.format(details.package_status))
        val_errors = details.errors
        self.assertTrue(len(val_errors) == 4, 'Expecting 4 errors but found {}'.format(len(val_errors)))
        self.assertTrue(self._contains_rule_id(val_errors, "CSIPSTR11",
                                               severity=Severity.Warn))
        self.assertTrue(self._contains_rule_id(val_errors, "CSIPSTR12",
                                               severity=Severity.Warn))
        self.assertTrue(self._contains_rule_id(val_errors, "CSIPSTR13",
                                               severity=Severity.Warn))
        self.assertTrue(self._contains_rule_id(val_errors, "CSIPSTR15",
                                               severity=Severity.Warn))

    def test_noreps(self):
        ip_path = os.path.join(os.path.dirname(__file__), 'resources', 'no_reps.tar.gz')
        details = IP.validate_package_structure(ip_path)
        self.assertTrue(details.package_status == IP.PackageStatus.WellFormed,
                        'Expecting status WellFormed, not {}'.format(details.package_status))
        val_errors = details.errors
        for err in val_errors:
            print(err.rule_id)
        self.assertTrue(len(val_errors) == 1, 'Expecting 1 errors but found {}'.format(len(val_errors)))
        self.assertTrue(self._contains_rule_id(val_errors, "CSIPSTR9",
                                               severity=Severity.Warn))

    @classmethod
    def _contains_rule_id(cls, error_list, rule_id, severity=Severity.Error):
        for val_error in error_list:
            if val_error.rule_id == rule_id:
                if val_error.severity == severity:
                    return True
        return False
