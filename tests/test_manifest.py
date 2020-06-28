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
"""Module containing tests covering the manifest module."""
import unittest
import os

import ip_validation.infopacks.manifests as MFST

MIN_TAR_MD5 = 'c0da9e5433a4c0a88b516ef509da4ce5'
MIN_TAR_SHA1 = '47ca3a9d7f5f23bf35b852a99785878c5e543076'
MIN_TAR_SHA256 = '798658e7a11c6c6edd446610392b837868604b7a0dd031dde0548c0412e92761'
MIN_TAR_SHA512 = 'c0622e684b325a98f9bb4190c782f6ccc26226785354bfcc5cbbdb175a17b9862219d78a6c862a00b7429d2b0af9c922338df62922318d36c6d287a28ea75982'

class DigestTests(unittest.TestCase):
    """Unit test cases for digest classes."""
    empty_path = os.path.join(os.path.dirname(__file__), 'resources', 'empty.file')
    min_tar_path = os.path.join(os.path.dirname(__file__), 'resources', 'ips', 'minimal',
                                'minimal_IP_with_schemas.tar')

    def test_digest_md5(self):
        md5 = MFST.Digest.md5(self.empty_path)
        self.assertTrue(md5.value == MFST.Digest.MD5_EMPTY,
                        'Expecting {} value but calculated {}'.format(MFST.Digest.MD5_EMPTY,
                                                                      md5.value))
        md5 = MFST.Digest.md5(self.min_tar_path)
        self.assertTrue(md5.value == MIN_TAR_MD5,
                        'Expecting {} value but calculated {}'.format(MIN_TAR_MD5,
                                                                      md5.value))

    def test_digest_sha1(self):
        sha1 = MFST.Digest.sha1(self.empty_path)
        self.assertTrue(sha1.value == MFST.Digest.SHA1_EMPTY,
                        'Expecting {} value but calculated {}'.format(MFST.Digest.SHA1_EMPTY,
                                                                      sha1.value))
        sha1 = MFST.Digest.sha1(self.min_tar_path)
        self.assertTrue(sha1.value == MIN_TAR_SHA1,
                        'Expecting {} value but calculated {}'.format(MIN_TAR_SHA1,
                                                                      sha1.value))

    def test_digest_sha256(self):
        sha256 = MFST.Digest.sha256(self.empty_path)
        self.assertTrue(sha256.value == MFST.Digest.SHA256_EMPTY,
                        'Expecting {} value but calculated {}'.format(MFST.Digest.SHA256_EMPTY,
                                                                      sha256.value))
        sha256 = MFST.Digest.sha256(self.min_tar_path)
        self.assertTrue(sha256.value == MIN_TAR_SHA256,
                        'Expecting {} value but calculated {}'.format(MIN_TAR_SHA256,
                                                                      sha256.value))

    def test_digest_sha512(self):
        sha512 = MFST.Digest.sha512(self.empty_path)
        self.assertTrue(sha512.value == MFST.Digest.SHA512_EMPTY,
                        'Expecting {} value but calculated {}'.format(MFST.Digest.SHA512_EMPTY,
                                                                      sha512.value))
        sha512 = MFST.Digest.sha512(self.min_tar_path)
        self.assertTrue(sha512.value == MIN_TAR_SHA512,
                        'Expecting {} value but calculated {}'.format(MIN_TAR_SHA512,
                                                                      sha512.value))
