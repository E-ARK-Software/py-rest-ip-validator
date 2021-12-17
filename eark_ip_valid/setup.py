# coding: utf-8

import sys
from setuptools import setup, find_packages

NAME = 'eark_ip'
VERSION = '1.0.0'
# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = ['lxml==4.6.3', 'six==1.16.0', 'importlib-resources==5.4.0']

setup(
    name=NAME,
    version=VERSION,
    description='E-ARK IP Validation API and Library',
    author_email='carl@openpreservation.org',
    url='',
    keywords=['Information Package', 'E-ARK', 'E-ARK IP Validation Library'],
    install_requires=REQUIRES,
    packages=find_packages(),
    package_data={ 'api.resources.profiles': ['*.*'],
                   'api.resources.schemas': ['*.*'],
                   'api.resources.schematron': ['*.*'] },
    entry_points={
        'console_scripts': [
            'eark-ip = eark_ip.cli.app:main',
        ]},
    long_description="""\
    # REST API definition for E-ARK Information package validation For further details see [E-ARK information package validation](https://earkcsip.dilcis.eu/).
    """
)
