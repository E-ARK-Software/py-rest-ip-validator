E-ARK Python IP Validator
=========================
*Web front end for E-ARK Information Package validation.*

[![Build Status](https://travis-ci.org/E-ARK-Software/py-rest-ip-validator.svg?branch=integration)](https://travis-ci.org/E-ARK-Software/py-rest-ip-validator "Travis-CI integration build")
[![CodeCov Coverage](https://img.shields.io/codecov/c/github/E-ARK-Software/py-rest-ip-validator.svg)](https://codecov.io/gh/E-ARK-Software/py-rest-ip-validator/ "CodeCov test coverage figure")
[![Codacy Badge](https://api.codacy.com/project/badge/Coverage/ab34b42c50954e4192987e060321ea17)](https://www.codacy.com/app/openpreserve/py-rest-ip-validator?utm_source=github.com&utm_medium=referral&utm_content=E-ARK-Software/py-rest-ip-validator&utm_campaign=Badge_Coverage)
[![GitHub issues](https://img.shields.io/github/issues/E-ARK-Software/py-rest-ip-validator.svg)](https://github.com/E-ARK-Software/py-rest-ip-validator/issues "Open issues on GitHub")

Quick Start
-----------
### Pre-requisites
Python 3.5+ OR [Docker](https://www.docker.com/).

### Getting the code
Clone the project move into the directory:

```shell
git clone https://github.com/E-ARK-Software/py-rest-ip-validator.git
cd py-rest-ip-validator
```

### Installation

#### Local virtual env setup
First set up a local virtual environment, this example assumes you'll do this in the project root directory on a linux box or Mac:

```shell
virtualenv -p python3 venv
source venv/bin/activate
```

Next set the environment variable for the Flask web app:

```shell
export FLASK_APP='ip_validation'
export EARK_PYIP_CONF_FILE='<pathtoproject>/conf/example.conf'
```

**NOTE** *these will need to be set for every new session for now*.

Finally install and run the  Flask application:

```shell
pip install -e .
flask run --port=5000
```

Then open your browser and navigate to http://localhost:5000

#### Local Docker instance

The `Dockerfile.dev` file in the project root is the easiest way to run the project if you use [Docker](https://www.docker.com/).

First you'll need to build a local instance the development Docker image:

```shell
docker build --tag=eark4all/py-ip-validator:dev -f Dockerfile.dev .
```

You then need to run a container instance, here's the command followed by a quick explanation:

```shell
docker run -p 5000:5000 -u $(id -u) -v "$PWD":/app -v /tmp:/tmp --detach --rm --name py-ip-dev eark4all/py-ip-validator:dev
```

Here's the options explained:
```
  -p 5000:5000      Map port 5000 from the host to the container
  -v "$PWD":/app    Map the host current directory to the container /app directory
  -v /tmp:/tmp      Map temp on the host to the container temp directory
  --detach          Detach from terminal session
  --rm              Remove container instance
  --name py-ip-dev  Give the container a name
```

Again open your browser and navigate to http://localhost:5000. You can work on the code and issue the command:

```shell
docker restart py-ip-dev
```

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
