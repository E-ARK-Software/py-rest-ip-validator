import os
import tempfile

import connexion
import six
from werkzeug.exceptions import BadRequest

from eark_ip.model.validation_report import ValidationReport  # noqa: E501
from eark_ip.api.manifests import Checksums
from eark_ip_rest import java_runner as JR
import eark_ip.api.packages as PKG

TEMP = tempfile.gettempdir()
UPLOADS_TEMP = os.path.join(TEMP, 'ip-uploads')
if not os.path.isdir(UPLOADS_TEMP):
    os.makedirs(UPLOADS_TEMP)
ALLOWED_EXTENSIONS = {'zip', 'tar', 'gz', 'gzip'}

def validate(body=None, ip_file=None):  # noqa: E501
    """Synchronous package valdition.

    Upload a package binary for validation and return validation result immediately. # noqa: E501

    :param sha1:
    :type sha1: str
    :param ip_file:
    :type ip_file: strstr

    :rtype: ValidationReport
    """
    dest_path = _check_validation_params(body, ip_file)
    validator = PKG.PackageValidator(dest_path)
    if os.path.exists(dest_path):
        os.remove(dest_path)
    return validator.validation_report

def java_validate(body=None, ip_file=None):  # noqa: E501
    """Synchronous package valdition.

    Upload a package binary for validation and return validation result immediately. # noqa: E501

    :param sha1:
    :type sha1: str
    :param ip_file:
    :type ip_file: strstr

    :rtype: ValidationReport
    """
    dest_path = _check_validation_params(body, ip_file)
    _, java_report, _ = JR.validate_ip(dest_path)
    if os.path.exists(dest_path):
        os.remove(dest_path)
    return java_report

def _check_validation_params(body, ip_file):
    if not ip_file:
        raise BadRequest('No file uploaded (form param ip_file), '
                         'file upload with accompanying sha1 required.')
    if not body.get('sha1', None):
        raise BadRequest('No sha1 digest supplied (form param sha1), '
                         'file upload with accompanying sha1 required.')
    if not _allowed_file(ip_file.filename):
        raise BadRequest('Bad file extenstion uploaded, file extension must be'
                         'one of {}'.format(', '.join(ALLOWED_EXTENSIONS)))
    sha1 = body.get('sha1')
    dest_path = os.path.join(UPLOADS_TEMP, ip_file.filename)
    if os.path.exists(dest_path):
        os.remove(dest_path)
    ip_file.save(dest_path)
    calc_sha1 = Checksums.from_file(dest_path)
    if calc_sha1.value.casefold() != sha1.casefold():
        raise BadRequest('Calculated uploaded file SHA1: {} does not equal'
                         'supplied SHA1 parameter: {}'.format(str(calc_sha1), sha1))
    return dest_path

def _allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
