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
import json
import os
import subprocess

from importlib_resources import files
from eark_ip.model import ValidationReport
import eark_ip_rest.resources as RES

MAIN_OPTS = [
    'java',
    '-jar',
    files(RES).joinpath('commons-ip2-cli-2.0.1.jar'),
    'validate',
    '-i'
]
REP_OPTS = [
    '-r',
    'eark'
]

def validate_ip(info_pack):
    """Returns a tuple comprising the process exit code, the validation report
    and the captured stderr."""
    ret_code, file_name, stderr = java_runner(info_pack)
    validation_report = None
    if ret_code == 0:
        with open(file_name, 'r', encoding='utf-8') as _f:
            contents = _f.read()
        os.remove(file_name)
        validation_report = ValidationReport.from_dict(json.loads(contents))
    return ret_code, validation_report, stderr

def java_runner(ip_root):
    command = MAIN_OPTS.copy()
    command.append(ip_root)
    command+=REP_OPTS
    proc_results = subprocess.run(command, capture_output=True)
    return proc_results.returncode, proc_results.stdout.rstrip(), proc_results.stderr
