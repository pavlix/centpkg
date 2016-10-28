'''
    The main behavior of centpkg
'''
#
# Author(s):
#            Jesse Keating <jkeating@redhat.com>
#            Pat Riehecky <riehecky@fnal.gov>
#            Brian Stinson <bstinson@ksu.edu>
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version.  See http://www.gnu.org/copyleft/gpl.html for
# the full text of the license.

from __future__ import absolute_import
from __future__ import print_function
import os
import sys
import logging
from six.moves import configparser
import argparse

import pyrpkg
import centpkg

def main():
    '''
        Where things actually happen
    '''
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('-C', '--config', help='The rpkg config file to use',
                        default='/etc/rpkg/centpkg.conf')
    parser.add_argument('command')

    (args, other) = parser.parse_known_args()

    # Make sure we have a sane config file
    if not os.path.exists(args.config) and not other[-1] in ['--help', '-h']:
        sys.stderr.write('Invalid config file %s\n' % args.config)
        sys.exit(1)

    config = configparser.ConfigParser()
    config.read(args.config)

    client = centpkg.cli.centpkgClient(config)
    client.do_imports(site='centpkg')
    client.parse_cmdline()

    if not client.args.path:
        try:
            client.args.path = os.getcwd()
        except OSError as err_msg:
            print('Could not get current path')
            print(err_msg)
            sys.exit(1)

    log = pyrpkg.log
    client.setupLogging(log)

    if client.args.v:
        log.setLevel(logging.DEBUG)
    elif client.args.q:
        log.setLevel(logging.WARNING)
    else:
        log.setLevel(logging.INFO)

    # Run the necessary command
    try:
        sys.exit(client.args.command())
    except KeyboardInterrupt:
        pass
    except Exception as e:
        log.error('Could not execute %s: %s' % (client.args.command.__name__, e))
        if client.args.v:
            raise
        sys.exit(1)

if __name__ == '__main__':
    main()
