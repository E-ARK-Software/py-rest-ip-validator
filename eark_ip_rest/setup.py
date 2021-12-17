# coding: utf-8

import sys
from setuptools import setup, find_packages

NAME = "eark_ip_rest"
VERSION = "1.0.0"
# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = ["connexion[swagger-ui]==2.9.0"]

setup(
    name=NAME,
    version=VERSION,
    description="E-ARK IP Validation REST API",
    author_email="carl@openpreservation.org",
    url="",
    keywords=["E-ARK", "E-ARK IP Validation REST API"],
    install_requires=REQUIRES,
    packages=find_packages(),
    package_data={'': ['swagger/swagger.yaml']},
    include_package_data=True,
    entry_points={
        'console_scripts': ['eark_ip_rest=eark_ip_rest.__main__:main']},
    long_description="""\
    # REST API definition for E-ARK Information package validation For further details see [E-ARK information package validation](https://earkcsip.dilcis.eu/).
    """
)
