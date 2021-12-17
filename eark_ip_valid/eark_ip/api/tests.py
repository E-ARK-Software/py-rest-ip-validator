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
Factory methods for validation testing classes.
"""
from functools import total_ordering

from eark_ip.model import (
    Severity,
    TestResult
)

def compare_result_lists(tests_a, tests_b):
    """Return true if the two lists have the same number of errors in them."""
    try:
        errs_only_a = _errs_only(tests_a)
        errs_only_b = _errs_only(tests_b)
        if len(errs_only_a) != len(errs_only_b):
            return False
        for error in errs_only_a:
            if not error in errs_only_b:
                return False
            errs_only_b.remove(error)
    except ValueError:
        return False
    return True

@total_ordering
class ShortResult():
    """Short result that cares not for location or message."""
    def __init__(self, test_result):
        self._rule_id = test_result.rule_id.upper()
        self._severity = test_result.severity.upper()

    @property
    def rule_id(self):
        """Return the rule_id."""
        return self._rule_id

    @property
    def severity(self):
        """Return the severity."""
        return self._severity

    def __eq__(self, other):
        if not isinstance(other, ShortResult) and not isinstance(other, TestResult):
            return False
        return (self._rule_id, self._severity) == (other._rule_id, other._severity)

    def __ne__(self, other):
        return not self == other

    def __lt__(self, other):
        return (self._rule_id, self._severity) < (other._rule_id, other._severity)

    def __hash__(self):
        return hash((self._rule_id, self._severity))

    def __repr__(self):
        return "%s %s" % (self.rule_id, self.severity)

def _errs_only(to_strip):
    errs_only = []
    for test in to_strip:
        if test.severity == Severity.ERROR:
            errs_only.append(ShortResult(test))
    return errs_only
