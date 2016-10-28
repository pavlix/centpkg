'''
    Command line behavior for centpkg
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
import sys
import os
import logging

from pyrpkg.cli import cliClient

class centpkgClient(cliClient):
    '''
        Where we import our custom stuff
    '''
    def __init__(self, config, name='centpkg'):
        '''init'''
        super(centpkgClient, self).__init__(config, name)


if __name__ == '__main__':
    client = centpkgClient()
    client.do_imports()
    client.parse_cmdline()

    if not client.args.path:
        try:
            client.args.path = os.getcwd()
        except OSError as err_msg:
            print('Could not get current path')
            print(err_msg)
            sys.exit(1)

    log = client.site.log
    client.setupLogging(log)

    if client.args.v:
        log.setLevel(logging.DEBUG)
    elif client.args.q:
        log.setLevel(logging.WARNING)
    else:
        log.setLevel(logging.INFO)

    # Run the necessary command
    try:
        client.args.command()
    except KeyboardInterrupt:
        pass
