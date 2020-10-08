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
import unittest

from importlib_resources import files

from ip_validation.cli import testcases as TC

import tests.resources.test_cases as CASES

class TestCasesTest(unittest.TestCase):
    """Tests for E-ARK XML Test Case classes."""
    def test_load_schematron(self):
        case = TC.TestCase.from_xml_file(str(files(CASES).joinpath('csipstr1.xml')))
        self.assertTrue(case.case_id.requirement_id == 'CSIP1')
        self.assertFalse(case.testable)
        self.assertTrue(len(case.requirement_text) > 0)
