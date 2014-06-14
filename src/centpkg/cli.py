import sys
import os
import logging

from pyrpkg.cli import cliClient


class centpkgClient(cliClient):
    def __init__(self, config, name='centpkg'):
        super(centpkgClient, self).__init__(config, name)


if __name__ == '__main__':
    client = centpkgClient()
    client.do_imports()
    client.parse_cmdline()

    if not client.args.path:
        try:
            client.args.path=os.getcwd()
        except:
            print('Could not get current path')
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
