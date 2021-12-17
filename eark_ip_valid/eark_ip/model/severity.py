# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from eark_ip.model.base_model_ import Model
from eark_ip import util


class Severity(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    """
    allowed enum values
    """
    INFO = "Info"
    WARN = "Warn"
    ERROR = "Error"
    def __init__(self):  # noqa: E501
        """Severity - a model defined in Swagger

        """
        self.swagger_types = {
        }

        self.attribute_map = {
        }

    @classmethod
    def from_dict(cls, dikt) -> 'Severity':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The severity of this Severity.  # noqa: E501
        :rtype: Severity
        """
        return util.deserialize_model(dikt, cls)
