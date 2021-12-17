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
""" Flask application routes for E-ARK Python IP Validator. """
import logging
import os
from datetime import datetime
from flask import render_template, request
from eark_ip_rest.controllers.validation_controller import (
    _check_validation_params
)
from eark_ip_rest import java_runner as JR
from eark_ip.model import StructStatus, MetadataStatus  # noqa: E501
import eark_ip.api.packages as PKG

LOG = logging.getLogger(__name__)

def home():
    """Application home page."""
    return render_template('home.html')

def result():
    """Application home page."""
    ip_file = request.files['ip_file']
    body = request.form
    dest_path = _check_validation_params(body, ip_file)
    ret_code, java_report, stderr = JR.validate_ip(dest_path)
    if ret_code != 0:
        LOG.error("Java Runner failed, ret_code: %d, stderr: %s", ret_code, stderr)
    java_summary = ResultSummary(java_report) if java_report else None
    print(str(java_summary))
    validator = PKG.PackageValidator(dest_path)
    python_report =  validator.validation_report
    python_summary = ResultSummary(python_report) if python_report else None
    print(str(python_summary))
    compliance = _comp_reps(python_summary, java_summary)
    if os.path.exists(dest_path):
        os.remove(dest_path)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return render_template('result.html', java_report=java_report,
                           python_report=python_report, timestamp=timestamp,
                           compliance=compliance, java_summary=java_summary,
                           python_summary=python_summary)

class ResultSummary():
    def __init__(self, report):
        self.errors, self.warnings, self.infos = _get_message_summary(report)
        self.structure = report.structure.status
        self.schema = report.metadata.schema_results.status if report.metadata else None
        self.schematron = report.metadata.schematron_results.status if report.metadata else None

    @property
    def is_valid(self):
        return self.structure.upper() == StructStatus.WELLFORMED.upper() and \
            self.schema.upper() == MetadataStatus.VALID.upper() and \
            self.schematron.upper() == MetadataStatus.VALID.upper()

    @property
    def result(self):
        return MetadataStatus.VALID if self.is_valid else MetadataStatus.NOTVALID

    def __repr__(self):
        return '{ResultSummary: { "is_valid"="%s", "result"="%s", "structure"="%s", "schema"="%s", "schematron"="%s"}}' \
                % (self.is_valid, self.result, self.structure, self.schema, self.schematron)

def _comp_reps(rep_one, rep_two):
    if not rep_one:
        if not rep_two:
            return 'Error'
        return 'Valid' if rep_two.is_valid else 'Invalid'
    if not rep_two:
        return 'Valid' if rep_one.is_valid else 'Invalid'
    if rep_one.is_valid != rep_two.is_valid:
        return 'Conflicted'
    return 'Valid' if rep_one.is_valid else 'Invalid'

def _get_message_summary(report):
    all_messages = []
    if report.structure:
        all_messages += report.structure.messages
    if report.metadata and report.metadata.schema_results:
        all_messages += report.metadata.schema_results.messages
    if report.metadata and report.metadata.schematron_results:
        all_messages += report.metadata.schematron_results.messages
    return _count_message_types(all_messages)

def _count_message_types(messages):
    infos = 0
    warns = 0
    errs = 0
    for message in messages:
        if message.severity.casefold() == 'info':
            infos+=1
        elif message.severity.casefold() == 'warn':
            warns+=1
        else:
            errs+=1
    return errs, warns, infos