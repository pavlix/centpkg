#pylint: disable=line-too-long,abstract-class-not-used
'''
    Top level function library for centpkg
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



import pyrpkg
import os
import re

from . import cli

class Commands(pyrpkg.Commands):
    '''
        For the pyrpkg commands with centpkg behavior
    '''
    def __init__(self, path, lookaside, lookasidehash, lookaside_cgi,
                 gitbaseurl, anongiturl, branchre, kojiconfig,
                 build_client, user=None, dist=None, target=None,
                 quiet=False):
        '''
            Init the object and some configuration details.
        '''
        super(Commands, self).__init__(path, lookaside, lookasidehash,
                                      lookaside_cgi, gitbaseurl, anongiturl,
                                      branchre, kojiconfig, build_client,
                                      user, dist, target, quiet)

    # redefined loaders
    def load_rpmdefines(self):
        '''
            Populate rpmdefines based on branch data
        '''
        try:
            osver = re.search(r'\d.*$', self.branch_merge).group()
        except AttributeError:
            raise pyrpkg.rpkgError('Could not find the base OS ver from branch name'
                            ' %s' % self.branch_merge)
        self._distval = osver
        self._distval = self._distval.replace('.', '_')
        self._disttag = 'el%s' % self._distval
        self._rpmdefines = ["--define '_topdir {0}'".format(self.path),
                            "--define 'dist .{0}'".format(self._disttag),
                            # int and float this to remove the decimal
                            "--define '{0} 1'".format(self._disttag)]

    def load_spec(self):
        """This sets the spec attribute"""

        # We are not using the upstream load_spec because the file structure is
        # hard-coded

        # Get a list of files in the path we're looking at
        files = os.listdir(os.path.join(self.path,'SPECS'))
        # Search the files for the first one that ends with ".spec"
        for __f in files:
            if __f.endswith('.spec') and not __f.startswith('.'):
                self._spec = os.path.join('SPECS', __f)
                return

        raise pyrpkg.rpkgError('No spec file found.')

    # These are the commands defined in the base pyrpkg.Commands class
    # and have been implemented here

    def sources(self, outdir=None):
        """Download source files"""

        #  See also:
        # https://lists.fedoraproject.org/pipermail/buildsys/2014-July/004313.html
        #
        # in 'super' the sources function expects a file named 'sources' to be in the base directory.
        # A patch has been sent to upstream to allow a more flexible location.
        #
        # This code doesn't work due to:
        #              archive.strip().split('  ', 1) # patch provided to upstream to fix
        #
        #              url = '%s/%s/%s/%s/%s' % (self.lookaside, self.module_name,
        #                                        file.replace(' ', '%20'),
        #                                        csum, file.replace(' ', '%20'))
        #
        #os.symlink(os.path.join(self.path, '.{0}.metadata'.format(self.module_name)), os.path.join(self.path, 'sources'))
        #super(Commands, self).sources(outdir=None)
        #os.unlink(os.path.join(self.path, 'sources'))

        # The following is copied from rpkg/__init__.py:sources with minor changes
        try:
            archives = open(os.path.join(self.path,
                                         '.{0}.metadata'.format(self.module_name)),
                            'r').readlines()
        except IOError, e:
            raise pyrpkg.rpkgError('%s is not a valid repo: %s' % (self.path, e))
        # Default to putting the files where the module is
        if not outdir:
            outdir = self.path
        for archive in archives:
            try:
                # This strip / split is kind a ugly, but checksums shouldn't have
                # two spaces in them.  sources file might need more structure in the
                # future
                csum, file = archive.strip().split(None, 1)
            except ValueError:
                raise pyrpkg.rpkgError('Malformed sources file.')
            # See if we already have a valid copy downloaded
            outfile = os.path.join(outdir, file)
            if os.path.exists(outfile):
                if self._verify_file(outfile, csum, self.lookasidehash):
                    continue
            self.log.info("Downloading %s" % (file))
            url = '%s/%s/%s/%s' % (self.lookaside, self.module_name,
                                      self.branch_merge,
                                      csum,
                                      )
            command = ['curl', '-H', 'Pragma:', '-o', outfile, '-R', '-S', '--fail']
            if self.quiet:
                command.append('-s')
            command.append(url)
            self._run_command(command)
            if not self._verify_file(outfile, csum, self.lookasidehash):
                raise pyrpkg.rpkgError('%s failed checksum' % file)

        return

    # These are the commands defined in the base pyrpkg.Commands class
    # and have not been implemented here, yet

    def load_kojisession(self, *args, **kwargs):
        raise NotImplementedError("This command is not yet implemented in centpkg")

    def get_latest_commit(self, *args, **kwargs):
        raise NotImplementedError("This command is not yet implemented in centpkg")

    def gitbuildhash(self, *args, **kwargs):
        raise NotImplementedError("This command is not yet implemented in centpkg")

    def import_srpm(self, *args, **kwargs):
        raise NotImplementedError("This command is not yet implemented in centpkg")

    def new(self, *args, **kwargs):
        raise NotImplementedError("This command is not yet implemented in centpkg")

    def patch(self, *args, **kwargs):
        raise NotImplementedError("This command is not yet implemented in centpkg")

    def push(self, *args, **kwargs):
        raise NotImplementedError("This command is not yet implemented in centpkg")

    def file_exists(self, *args, **kwargs):
        raise NotImplementedError("This command is not yet implemented in centpkg")

    def upload_file(self, *args, **kwargs):
        raise NotImplementedError("This command is not yet implemented in centpkg")

    def build(self, *args, **kwargs):
        raise NotImplementedError("This command is not yet implemented in centpkg")

    def clog(self, *args, **kwargs):
        raise NotImplementedError("This command is not yet implemented in centpkg")

    def koji_upload(self, *args, **kwargs):
        raise NotImplementedError("This command is not yet implemented in centpkg")

    def install(self, *args, **kwargs):
        raise NotImplementedError("This command is not yet implemented in centpkg")

    def lint(self, *args, **kwargs):
        raise NotImplementedError("This command is not yet implemented in centpkg")

    def mock_config(self, *args, **kwargs):
        raise NotImplementedError("This command is not yet implemented in centpkg")

    def mockbuild(self, *args, **kwargs):
        raise NotImplementedError("This command is not yet implemented in centpkg")

    def upload(self, *args, **kwargs):
        raise NotImplementedError("This command is not yet implemented in centpkg")

    def prep(self, *args, **kwargs):
        raise NotImplementedError("This command is not yet implemented in centpkg")

    def srpm(self, *args, **kwargs):
        raise NotImplementedError("This command is not yet implemented in centpkg")

    def unused_patches(self, *args, **kwargs):
        raise NotImplementedError("This command is not yet implemented in centpkg")

