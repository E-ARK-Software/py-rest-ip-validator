E-ARK Python IP Validator
=========================
*Web front end for E-ARK Information Package validation.*

[![Build Status](https://travis-ci.org/carlwilson/eark-py-ip-validator.svg?branch=integration)](https://travis-ci.org/carlwilson/eark-py-ip-validator "Travis-CI integration build")
[![CodeCov Coverage](https://img.shields.io/codecov/c/github/carlwilson/eark-py-ip-validator.svg)](https://codecov.io/gh/carlwilson/eark-py-ip-validator/ "CodeCov test coverage figure")
[![Codacy Badge](https://api.codacy.com/project/badge/Coverage/ab34b42c50954e4192987e060321ea17)](https://www.codacy.com/app/openpreserve/eark-py-ip-validator?utm_source=github.com&utm_medium=referral&utm_content=carlwilson/eark-py-ip-validator&utm_campaign=Badge_Coverage)
[![GitHub issues](https://img.shields.io/github/issues/carlwilson/eark-py-ip-validator.svg)](https://github.com/carlwilson/eark-py-ip-validator/issues "Open issues on GitHub")

Description
-----------
The `eark-py-ip-validator` project provides a set of Python tools that

Quick Start
-----------
### Pre-requisites
- Python 3.5+

### Dependencies

### Installation
#### Local virtual env setup
First set up a local virtual environment, this example assumes you'll do this in the project root directory on a linux box or Mac:

    virtualenv -p python3 venv
    source venv/bin/activate
Next set the environment variable for the Flask web app:

    export FLASK_APP='ip_validation'
    export EARK_PYIP_CONF_FILE='<pathtoproject>/conf/example.conf'
**NOTE** *these will need to be set for every new session for now*.

Finally install and run the  Flask application:

    pip install -e .
    flask run --port=8080
    The open your browser and navigate to http://localhost:8080

### Configuration
The application has built in application profiles that can be augmented and over-ridden by a user configuration file.

Development
-----------
### Python development utilities
These are useful for ensuring your code follows best practise and establishing whether it's tested.

 - pylint for static source code checking
 - pep8 for complimentary similar
 - pytest for running unit tests
 - pytest-cov for generating test coverage reports

#### Running tests

You can run unit tests by:

    pytest ./tests/
and generate test coverage figures by:

    pytest --cov=ip_validation ./tests/
If you want to see which parts of your code aren't tested then:

     pytest --cov=ip_validation --cov-report=html ./tests/
After this you can open the file [`<projectRoot>/htmlcov/index.html`](./htmlcov/index.html) in your browser and survey the gory details.

### Tips
#### setup.py doesn't install....
These are all issues I encountered when developing this as a Python noob. All commands are Linux and if not stated they are run from the project root.
 - This is can be caused by caching of old compiled files. You can use this `find ./ip_validation -name '*.pyc' -delete` to remove all the compiled files below the current directory.
 - The build directory is out of synch, delete it: `rm -rf ./build`.
