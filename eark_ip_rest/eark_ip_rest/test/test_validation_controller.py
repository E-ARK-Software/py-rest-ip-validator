# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from eark_ip_rest.model.validation_report import ValidationReport  # noqa: E501
from eark_ip_rest.test import BaseTestCase


class TestValidationController(BaseTestCase):
    """ValidationController integration test stubs"""

    def test_validate(self):
        """Test case for validate

        Synchronous package valdition.
        """
        data = dict(sha1='sha1_example',
                    ip_file='ip_file_example')
        response = self.client.open(
            '/validate',
            method='POST',
            data=data,
            content_type='multipart/form-data')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
