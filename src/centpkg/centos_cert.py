from __future__ import absolute_import
from __future__ import print_function
import os
from OpenSSL import crypto
import urlgrabber
import datetime

# This file was modified from the fedora_cert section in fedora-packager written
# by Dennis Gilmore (https://fedorahosted.org/fedora-packager/)


# Define our own error class
class centos_cert_error(Exception):
    pass

def _open_cert():
    """
    Read in the certificate so we dont duplicate the code 
    """
     # Make sure we can even read the thing.
    cert_file = os.path.join(os.path.expanduser('~'), ".koji", "client.crt")
    if not os.access(cert_file, os.R_OK):
        raise centos_cert_error("""!!!    cannot read your centos cert file   !!!
!!! Ensure the file is readable and try again !!!""")
    raw_cert = open(cert_file).read()
    my_cert = crypto.load_certificate(crypto.FILETYPE_PEM, raw_cert)
    return my_cert

def verify_cert():
    """
    Check that the user cert is valid.
    things to check/return
    not revoked
    Expiry time warn if less than 21 days
    """
    my_cert = _open_cert()
    serial_no = my_cert.get_serial_number()
    valid_until = my_cert.get_notAfter()[:8]
    # CRL verification would go here
    #crl = urlgrabber.urlread("https://<url_to_crl>/ca/crl.pem")
    dateFmt = '%Y%m%d'
    delta = datetime.datetime.now() + datetime.timedelta(days=21)
    warn = datetime.datetime.strftime(delta, dateFmt)

    print('cert expires: %s-%s-%s' % (valid_until[:4], valid_until[4:6], valid_until[6:8]))

    if valid_until < warn:
        print('WARNING: Your cert expires soon.')


def certificate_expired():
    """
    Check to see if client cert is expired
    Returns True or False

    """
    my_cert = _open_cert()

    if my_cert.has_expired():
        return True
    else:
        return False

def read_user_cert():
    """
    Figure out the Fedora user name from client cert

    """
    my_cert = _open_cert()

    subject = str(my_cert.get_subject())
    subject_line = subject.split("CN=")
    cn_parts = subject_line[1].split("/")
    username = cn_parts[0]
    return username

