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
"""METS Schema validation."""
import fnmatch
import logging
import os
from pathlib import Path

from lxml import etree
from lxml.isoschematron import Schematron

from importlib_resources import files

import eark_ip.api.manifests as MNFST
import eark_ip.api.resources.schemas as SCHEMA
import eark_ip.api.resources.schematron as SCHEMATRON
from eark_ip.model import (
    MetadataStatus,
    TestResult,
    Severity,
    MetadataChecks,
    MetadataResults,
    Checksum,
    ChecksumAlg,
    ProfileDetails
)

XLINK_NS = 'http://www.w3.org/1999/xlink'
METS_NS = 'http://www.loc.gov/METS/'
QUAL_METS_NS = '{{{}}}'.format(METS_NS)
METS_FILENAME = 'METS.xml'

DILCIS_EXT_NS = 'https://DILCIS.eu/XML/METS/CSIPExtensionMETS'
SCHEMATRON_NS = "{http://purl.oclc.org/dsdl/schematron}"
SVRL_NS = "{http://purl.oclc.org/dsdl/svrl}"
ALGS = vars(ChecksumAlg)

class FileRef():
    """Encapsulate the file reference and integrity details found in METS references."""
    def __init__(self, path, size, checksum):
        self._path = Path(path)
        self._size = size
        self._checksum = checksum

    @property
    def path(self):
        """Return the path of the file reference, will be relative to
        package/representation."""
        return self._path

    @property
    def size(self):
        """Return the stated size of the file in bytes."""
        return self._size

    @property
    def checksum(self):
        """Return the recorded Checksum of the file, includes algorithm and value."""
        return self._checksum

    def __str__(self):
        return '\'path\': \'{}\' \'size\': \'{}\' \'checksum\': \'{}\''.format(self.path,
                                                                               self.size,
                                                                               self.checksum)

class MetsValidator():
    """Encapsulates METS schema validation."""
    def __init__(self, root):
        self.validation_errors = []
        self.schema_wrapper = etree.XMLSchema(file=str(files(SCHEMA).joinpath('wrapper.xsd')))
        self.rootpath = root
        self.represent_mets = {}
        self.file_refs = []

    def validate_mets(self, mets):
        '''
        Validates a Mets file. The Mets file is parsed with etree.iterparse(),
        which allows event-driven parsing of large files. On certain events/conditions
        actions are taken, like file validation or adding Mets files found inside
        representations to a list so that they will be evaluated later on.

        @param mets:    Path leading to a Mets file that will be evaluated.
        @return:        Boolean validation result.
        '''
        # Handle relative package paths for representation METS files.
        self.rootpath, mets = _handle_rel_paths(self.rootpath, mets)
        try:
            parsed_mets = etree.iterparse(mets, events=('start', 'end'), schema=self.schema_wrapper)
            self._element_processor(parsed_mets)
        except etree.XMLSyntaxError as synt_err:
            self.validation_errors.append(TestResult(rule_id="METS", location=mets,
                                          message=synt_err.msg.replace(QUAL_METS_NS, "mets:"),
                                          severity=Severity.ERROR))
        except Exception as base_err:
            self.validation_errors.append(TestResult(rule_id="METS", location=mets,
                                          message=str(base_err), severity=Severity.ERROR))
        status = MetadataStatus.NOTVALID if self.validation_errors else MetadataStatus.VALID
        return status == MetadataStatus.VALID, MetadataChecks(status=status,
                                                              messages=self.validation_errors)

    def _element_processor(self, parsed_mets):
        for event, element in parsed_mets:
            # Define what to do with specific tags.
            if event == 'end' and element.tag == _q(METS_NS, 'file'):
                # files
                self.file_refs.append(_file_ref_from_ele(element))
            elif event == 'end' and \
                element.tag == _q(METS_NS, 'fileGrp') and \
                element.attrib.get('USE', '').startswith('Representations/'):
                # representation mets files
                self._rep_processor(element)
            elif event == 'end' and element.tag in [_q(METS_NS, 'dmdSec'), _q(METS_NS, 'amdSec')]:
                for ref in element.iter(_q(METS_NS, 'mdRef')):
                    self.file_refs.append(_file_ref_from_mdref_ele(ref))

    def _rep_processor(self, element):
        # representation mets files
        rep = element.attrib['USE'].rsplit('/', 1)[1]
        for file in element.iter(_q(METS_NS, 'file')):
            file_ref = _file_ref_from_ele(file)
            if os.path.basename(file_ref.path).casefold() == METS_FILENAME.casefold():
                self.represent_mets[rep] = file_ref
            else:
                self.file_refs.append(file_ref)

def _file_ref_from_ele(element):
    algid = element.attrib.get('CHECKSUMTYPE', None)
    chksm = element.attrib.get('CHECKSUM', None)
    size = element.attrib.get('SIZE', None)
    checksum = None
    ref = None
    for alg in ALGS:
        if getattr(ChecksumAlg, alg) == algid:
            checksum = Checksum(algid, chksm)
    for child in element.getchildren():
        if child.tag == _q(METS_NS, 'FLocat'):
            path = child.attrib[_q(XLINK_NS, 'href')]
            ref = FileRef(path, size, checksum)
    return ref

def _file_ref_from_mdref_ele(element):
    algid = element.attrib.get('CHECKSUMTYPE', None)
    chksm = element.attrib.get('CHECKSUM', None)
    size = element.attrib.get('SIZE', None)
    checksum = None
    ref = None
    for alg in ALGS:
        if getattr(ChecksumAlg, alg) == algid:
            checksum = Checksum(algid, chksm)
    path = element.attrib.get(_q(XLINK_NS, 'href'), None)
    ref = FileRef(path, size, checksum)
    return ref


def _handle_rel_paths(rootpath, metspath):
    if metspath.startswith('file://./'):
        relpath = os.path.join(rootpath, metspath[9:])
        # change self.rootpath to match any relative path found in the
        # current (subsequent) mets
        return relpath.rsplit('/', 1)[0], relpath
    return metspath.rsplit('/', 1)[0], metspath

def _q(_ns, _v):
    return '{{{}}}{}'.format(_ns, _v)

class ValidationRules():
    """Encapsulates a set of Schematron rules loaded from a single file."""
    REP_SKIPS = [
        'CSIP10',
        'CSIP11',
        'CSIP12',
        'CSIP13',
        'CSIP14',
        'CSIP15',
        'CSIP16',
        'CSIP101',
        'CSIP114'
    ]
    def __init__(self, name: str, rules_path: str=None):
        """Initialise a set of validation rules from a file or name.

        Retrieve a validation profile by type and version # noqa: E501

        :param name: The name of the rule set once loaded. If no path is provided
                     this param will be compared to the standard set of rules and
                     a matching rule set will be loaded if found. For reference the
                     standard ruleset corresponds to the different METS file sections
                     i.e. amd, dmd, file, hdr, root, structmap
        :type type: str
        :param rules_path: A complete path to a set of schematron rules to load
        :type version: str
        """
        self.name = name
        if not rules_path:
            # If no path is provided use the name param to try to load a standard ruleset
            rules_path = str(files(SCHEMATRON).joinpath('mets_{}_rules.xml'.format(name)))
        self.rules_path = rules_path
        logging.debug("path: %s", self.rules_path)
        # Load the schematron file from the path
        self.ruleset = Schematron(file=self.rules_path, store_schematron=True, store_report=True)

    def get_assertions(self):
        """Generator that returns the rules one at a time."""
        xml_rules = etree.XML(bytes(self.ruleset.schematron))

        for ele in xml_rules.iter():
            if ele.tag == SCHEMATRON_NS + 'assert':
                yield ele

    def validate(self, to_validate):
        """Validate a file against the loaded Schematron ruleset."""
        xml_file = etree.parse(to_validate)
        self.ruleset.validate(xml_file)

    def get_report(self, struct, rep_skips=False):
        """Get the report from the last validation."""
        xml_report = etree.XML(bytes(self.ruleset.validation_report))
        messages = []
        rule = None
        status = MetadataStatus.VALID
        for ele in xml_report.iter():
            if ele.tag == SVRL_NS + 'fired-rule':
                rule = ele
            elif ele.tag == SVRL_NS + 'failed-assert':
                rule_id = ele.get('id', '')
                if self._skip_assertion(rule_id, struct, rep_skips):
                    continue
                test_status, test_result = self._process_ele(rule_id, rule, ele)
                if test_status == MetadataStatus.NOTVALID:
                    status = MetadataStatus.NOTVALID
                messages.append(test_result)

        return MetadataChecks(status=status, messages=messages)

    def _skip_assertion(self, rule_id, struct, rep_skips):
        if rep_skips and rule_id in self.REP_SKIPS:
            return True
        if rule_id == 'CSIP60' and not struct.has_documentation():
            return True
        if rule_id == 'CSIP88' and not struct.has_metadata():
            return True
        if rule_id in ('CSIP97', 'CSIP113') and not struct.has_schemas():
            return True
        if rule_id == 'CSIP114' and not struct.has_representations():
            return True;
        return False
    
    def _process_ele(self, rule_id, rule, ele):
        status = MetadataStatus.VALID
        severity = Severity.WARN
        if ele.get('role') == 'ERROR':
            severity = Severity.ERROR
            status = MetadataStatus.NOTVALID
        elif ele.get('role') == 'INFO':
            severity = Severity.INFO
        return status, TestResult(
                        rule_id=rule_id,
                        location=rule.get('context').replace('/*[local-name()=\'', '') +
                        '/' + ele.get('test'),
                        message=ele.find(SVRL_NS + 'text').text,
                        severity=severity
                )

class ValidationProfile():
    """ A complete set of Schematron rule sets that comprise a complete validation profile."""
    NAMES = {
        'root': 'METS Root',
        'hdr': 'METS Header',
        'amd': 'Adminstrative Metadata',
        'dmd': 'Descriptive Metadata',
        'file': 'File Section',
        'structmap': 'Structural Map'
    }
    SECTIONS = NAMES.keys()

    def __init__(self):
        self.rulesets = {}
        self.is_valid = False
        self.results = {}
        self.messages = []
        for section in self.SECTIONS:
            self.rulesets[section] = ValidationRules(section)

    def validate(self, to_validate, structure, is_root=True):
        """Validates a file against each loaded ruleset."""
        is_valid = True
        self.results = {}
        self.messages = []
        for section in self.SECTIONS:
            try:
                self.rulesets[section].validate(to_validate)
            except etree.XMLSyntaxError as parse_err:
                self.is_valid = False
                self.messages.append(parse_err.msg)
                continue
            self.results[section] = self.rulesets[section].get_report(structure, not is_root)
            if self.results[section].status != MetadataStatus.VALID:
                is_valid = False
        self.is_valid = is_valid
        messages = []
        status = MetadataStatus.VALID
        for _, result in self.results.items():
            messages+=result.messages
            if result.status == MetadataStatus.NOTVALID:
                status = MetadataStatus.NOTVALID
        return status == MetadataStatus.VALID, MetadataChecks(status=status, messages=messages)

    def get_details(self):
        """Return the valiation profile details."""
        return ProfileDetails(name='E-ARK Specification for Information Packages',
                              type='SIP', version='2.0.4')

    def get_results(self):
        """Return the full set of results."""
        return self.results

    def get_result(self, name):
        """Return only the results for element name."""
        return self.results.get(name)

def validate_ip(to_validate, struct_map):
    # Schematron validation profile
    schema_results = {}
    schematron_results = {}
    mets_files = {}
    validator = MetsValidator(to_validate)
    mets_path = os.path.join(to_validate, METS_FILENAME)
    results = validator.validate_mets(mets_path)
    schema_results['root'] = results
    mets_files['root'] = validator.file_refs
    for key, file_ref in validator.represent_mets.items():
        print('METS_KEY: ', key, ", REF: ", file_ref)
        rep_validator = MetsValidator(file_ref.path)
        schema_results[key] = rep_validator.validate_mets(os.path.join(to_validate,
                                                                       file_ref.path))
        mets_files[key] = rep_validator.file_refs
    profile = ValidationProfile()
    schematron_results['root'] = profile.validate(mets_path, struct_map['root'])
    all_schm_status = MetadataStatus.VALID
    all_schm_mssg = []
    all_schmtrn_status = MetadataStatus.VALID
    all_schmtrn_mssg = []
    for key, (schema_valid, results) in schema_results.items():
        all_schm_mssg+=results.messages
        print('Checking METS validation: ', key)
        if schema_valid:
            print('Schema validation succeeded for: ', key)
            if key == 'root':
                print('root METS schematron: ')
                schematron_valid, schematron_result = schematron_results['root']
            else:
                mets_ref = validator.represent_mets[key]
                schematron_valid, schematron_result = profile.validate(os.path.join(to_validate,
                                                                                 mets_ref.path),
                                                                       struct_map[key], False)
            if not schematron_valid:
                all_schmtrn_status = MetadataStatus.NOTVALID
                all_schmtrn_mssg+=schematron_result.messages
        else:
            all_schm_status = MetadataStatus.NOTVALID
            all_schmtrn_status = MetadataStatus.NOTVALID
    manifest_errors = _check_manifest(to_validate, mets_files)
    if manifest_errors:
        all_schmtrn_status = MetadataStatus.NOTVALID
        all_schmtrn_mssg+=manifest_errors

    return profile.get_details(), MetadataResults(MetadataChecks(all_schm_status,
                                                                 all_schm_mssg),
                                                  MetadataChecks(all_schmtrn_status,
                                                                 all_schmtrn_mssg))

def _check_manifest(to_validate, mets_refs):
    algs = set()
    for refs in mets_refs.values():
        for ref in refs:
            if ref.checksum:
                algs.add(ref.checksum.algorithm)
    manifest = MNFST.manifest_from_directory(to_validate, checksum_algs=algs)
    return _get_manifest_errors(mets_refs, manifest)

def _get_manifest_errors(mets_refs, manifest):
    errors = []
    for key, refs in mets_refs.items():
        for file_ref in refs:
            errors += _proc_file_ref(file_ref, key, manifest)
    return errors

def _proc_file_ref(file_ref, key, manifest):
    errors = []
    ref_path = str(file_ref.path) if key == 'root' else os.path.join('representations',
                                                                        key,
                                                                        str(file_ref.path))
    for entry in manifest.entries:
        if entry.path == ref_path:
            errors += _check_manifest_entry(entry, file_ref, key)
    return errors

def _check_manifest_entry(entry, file_ref, key):
    errors = []
    if str(entry.size) != str(file_ref.size):
        errors.append(TestResult('CSIP69',
                                    'mets/fileSec/fileGrp/file/@SIZE',
                'mets/fileSec/fileGrp/file/@SIZE: {} declared in {} {} '
                'and size of file {}: {} isn\'t equal.'.format(file_ref.size,
                                                                key,
                                                                entry.path,
                                                                entry.size,
                                                                METS_FILENAME),
                        Severity.ERROR))
    checksum_matched = False
    if file_ref.checksum:
        for checksum in entry.checksums:
            if file_ref.checksum and checksum == file_ref.checksum:
                checksum_matched = True
        if not checksum_matched:
            errors.append(TestResult('CSIP71',
                                        'mets/fileSec/fileGrp/file/@CHECKSUM',
                    'mets/fileSec/fileGrp/file/@CHECKSUM: {} declared in {} {} '
                    'and checksum of file {} isn\'t equal.'.format(file_ref.checksum.value,
                                                                key,
                                                                entry.path,
                                                                METS_FILENAME),
                            Severity.ERROR))
    return errors
    