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
E-ARK : Information package validation
        E-ARK Test Case processing
"""
import os.path

import lxml.etree as ET

from importlib_resources import files

import ip_validation.cli.resources as RES
DEFAULT_NAME='testCase.xml'
TC_SCHEMA = ET.XMLSchema(file=str(files(RES).joinpath('testCase.xsd')))

class TestCase():
    """
    Encapsulates the E-ARK XML Test Case files.

    Parameters / attributes
     - case_id: a CaseId instance that is the compound test case id.
     - testable: boolean, True if test case is "testable", False otherwise
     - references: a list of references to relavent requirements.
    """
    def __init__(self, case_id, valid, testable=True, references=None, req=None, rules=None):
        self._case_id = case_id
        self._valid = valid
        self._testable = testable
        self._references = [] if references is None else references
        self._req = req
        self._rules = [] if rules is None else rules
        self._package_count = 0
        self._existing_package_count = 0

    @property
    def case_id(self):
        """Return the test case id instance."""
        return self._case_id

    @property
    def valid(self):
        """Return True if the test case is valid XML against the schema supplied."""
        return self._valid

    @property
    def testable(self):
        """Return True if the test case is considered testable, otherwise False."""
        return self._testable == 'TRUE'

    @property
    def unknown(self):
        """Return True if the test case testability is unknown, otherwise False."""
        return self._testable == 'UNKNOWN'

    @property
    def status(self):
        """Return the test case status."""
        return self._testable

    @property
    def references(self):
        """Return the list of relavent requirements."""
        return self._references

    @property
    def requirement(self):
        """Return the requirement."""
        return self._req

    @property
    def rules(self):
        """Return the rules associated with the test case."""
        return self._rules

    def resolve_package_paths(self, case_root):
        """Resolve package paths for all rule packages."""
        for rule in self.rules:
            for package in rule.packages:
                package.resolve_path(case_root)

    @property
    def package_count(self):
        """Return the number of packages in the test case."""
        count = 0
        for rule in self.rules:
            count+=len(rule.packages)
        return count

    @property
    def missing_package_count(self):
        """Return the number of packages in the test case."""
        count = 0
        for rule in self.rules:
            count+=len(rule.missing_packages)
        return count

    def __str__(self):
        return "case_id:" + str(self.case_id) + ", testable:" + \
            str(self.testable) + ", requirement:" + self.requirement

    class CaseId():
        """
        Encapsulates an E-ARK XML Test Case ID.

        Parameters / attributes
         - requirement_id: a requirement ID string from the specification.
         - specification: the name of the specification.
         - version: the version of the specifciation.
        """
        def __init__(self, requirement_id, specification="CSIP", version="2.0"):
            self._requirement_id = requirement_id
            self._specification = specification
            self._version = version

        @property
        def requirement_id(self):
            """Return the requirement ID."""
            return self._requirement_id

        @property
        def specification(self):
            """Return the specification name."""
            return self._specification

        @property
        def version(self):
            """Return the version."""
            return self._version

        @classmethod
        def from_element(cls, case_id_ele):
            """Create a TestCase from an XML element."""
            requirement_id = case_id_ele.get('requirementId')
            specification = case_id_ele.get('specification')
            version = case_id_ele.get('version')
            return cls(requirement_id, specification, version)

        def __str__(self):
            return "req_id:" + str(self.requirement_id) + ", specification:" + \
                str(self.specification) + ", version:" + str(self.version)

    class Requirement():
        """Requirment docstring."""
        def __init__(self, name, location, cardinality, level, description):
            self._name = name
            self._location = location
            self._cardinality = cardinality
            self._level = level
            self._description = description

        @property
        def name(self):
            """Return the name."""
            return self._name

        @property
        def location(self):
            """Return the location."""
            return self._location

        @property
        def cardinality(self):
            """Return the cardinality."""
            return self._cardinality

        @property
        def level(self):
            """Return the level."""
            return self._level

        @property
        def description(self):
            """Return the description."""
            return self._description

        @classmethod
        def from_element(cls, req_ele):
            """Create a Requirment from an XML element."""
            name = ""
            location = ""
            cardinality = ""
            level = ""
            description = ""
            for child in req_ele:
                if child.tag == 'name':
                    name = child.text
                elif child.tag == 'description':
                    description = child.text
                elif child.tag == 'cardinality':
                    cardinality = child.text
                elif child.tag == 'level':
                    level = child.get('level')
                elif child.tag == 'location':
                    location = child.text
            return cls(name, location, cardinality, level, description)



    class Rule():
        """docstring for Rule."""
        def __init__(self, rule_id, description, error, packages):
            self._rule_id = rule_id
            self._description = description
            self._error = error
            self._packages = packages

        @property
        def rule_id(self):
            """Return the rule ID."""
            return self._rule_id

        @property
        def description(self):
            """Return the description."""
            return self._description

        @property
        def error(self):
            """Return the error."""
            return self._error

        @property
        def packages(self):
            """Return the corpus packages."""
            return self._packages

        @property
        def missing_packages(self):
            """Return a list of missing packages."""
            missing = []
            for package in self.packages:
                if not package.exists:
                    missing.append(package)
            return missing

        @property
        def existing_packages(self):
            """Return a list of existing packages."""
            existing = []
            for package in self.packages:
                if package.exists:
                    existing.append(package)
            return existing

        def resolve_package_paths(self, case_root):
            """Resolve package paths for all rule packages."""
            for package in self.packages:
                package.resolve_path(case_root)

        def __str__(self):
            return "rule_id:" + self.rule_id + ", description:" + \
                self.description + ", error:" + str(self.error)

        @classmethod
        def from_element(cls, rule_ele):
            """Create a Rule from an XML element."""
            rule_id = rule_ele.get('id')
            description = ""
            error = None
            packages = []
            for child in rule_ele:
                if child.tag == 'description':
                    description = child.text
                elif child.tag == 'error':
                    error = cls.Error.from_element(child)
                elif child.tag == 'corpusPackages':
                    packages = cls._parse_package_list(child)
            return cls(rule_id, description, error, packages)

        @staticmethod
        def _parse_package_list(packages_ele):
            packages = []
            for child in packages_ele:
                if child.tag == 'package':
                    packages.append(TestCase.Rule.Package.from_element(child))
            return packages

        class Error():
            """docstring for Error."""
            def __init__(self, level, message):
                self._level = level
                self._message = message

            @property
            def level(self):
                """Return the level."""
                return self._level

            @property
            def message(self):
                """Return the message."""
                return self._message

            @classmethod
            def from_element(cls, error_ele):
                """Return a Errpr instance from an XML element."""
                level = error_ele.get('level')
                message = ''
                for child in error_ele:
                    if child.tag == 'message':
                        message = child.text
                return cls(level, message)

        class Package():
            """docstring for Package."""
            def __init__(self, name, path, is_valid, is_implemented, description, validation_report=None):
                self._name = name
                self._path = path
                self._is_valid = is_valid
                self._description = description
                self._validation_report = validation_report
                self._is_implemented = is_implemented

            @property
            def name(self):
                """Return the name."""
                return self._name

            @property
            def path(self):
                """Return the path."""
                return self._path

            def resolve_path(self, case_root):
                """Resolve the path to the corpus package given the test case root."""
                if self.path:
                    self._path = os.path.join(case_root, self.name)
                    if not self.exists:
                        self._path = os.path.join(case_root, self.path)
                return self.path

            @property
            def exists(self):
                """Check if the corpus package exists given the test case root."""
                if not self.path:
                    return False
                return os.path.exists(self.path)

            @property
            def is_valid(self):
                """Return the is_valid."""
                return self._is_valid

            @property
            def implemented(self):
                """Return True if the test case is valid XML against the schema supplied."""
                return self._is_implemented

            @property
            def description(self):
                """Return the description."""
                return self._description

            @property
            def validation_report(self):
                """Return the validation report for the package."""
                return self._validation_report

            @classmethod
            def from_element(cls, package_ele):
                """Return a Package instance from an XML element."""
                is_valid = package_ele.get('isValid')
                is_implemented = package_ele.get('isImplemented')
                name = package_ele.get('name')
                path = ""
                description = ""
                for child in package_ele:
                    if child.tag == 'path':
                        path = child.text
                    elif child.tag == 'description':
                        description = child.text
                return cls(name, path, is_valid, is_implemented, description)

    @classmethod
    def from_xml_string(cls, xml, schema=TC_SCHEMA):
        """Create a test case from an XML string."""
        tree = ET.fromstring(xml)
        return cls._from_xml(tree, schema)

    @classmethod
    def from_xml_file(cls, xml_file, schema=TC_SCHEMA):
        """Create a test case from an XML file."""
        tree = ET.parse(xml_file)
        return  cls._from_xml(tree, schema, xml_file=xml_file)

    @classmethod
    def _from_xml(cls, tree, schema, xml_file=None):
        case = cls.from_element(tree.getroot(), schema)
        if xml_file:
            case.resolve_package_paths(os.path.abspath(os.path.join(xml_file, os.pardir)))
        return case



    @classmethod
    def from_element(cls, case_ele, schema):
        """Create a TestCase from an XML element."""
        # Grab the testable att
        is_valid = schema.validate(case_ele)
        testable = case_ele.get('testable')
        req_id = None
        req = None
        rules = []
        # Loop through the child eles
        for child in case_ele:
            if child.tag == 'id':
                # Process the id element
                req_id = cls.CaseId.from_element(child)
            elif child.tag == 'requirementText':
                # Grab the requirement text value
                req = cls.Requirement.from_element(child)
            elif child.tag == 'rules':
                for rule_ele in child:
                    if rule_ele.tag == 'rule':
                        rules.append(cls.Rule.from_element(rule_ele))

        # Return the TestCase instance
        return cls(req_id, is_valid, testable=testable, req=req, rules=rules)
