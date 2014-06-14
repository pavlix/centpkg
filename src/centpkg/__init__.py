import pyrpkg
import os
import re

from . import cli

class Commands(pyrpkg.Commands):
    def __init__(self, path, lookaside, lookasidehash, lookaside_cgi,
                 gitbaseurl, anongiturl, branchre, kojiconfig,
                 build_client, user=None, dist=None, target=None,
                 quiet=False):

        super(Commands,self).__init__(path, lookaside, lookasidehash,
                                      lookaside_cgi, gitbaseurl, anongiturl,
                                      branchre, kojiconfig, build_client,
                                      user, dist, target,
                                      quiet)


    # redefined loaders
    def load_rpmdefines(self):
        try:
            osver = re.search(r'\d.*$', self.branch_merge).group()
        except AttributeError:
            raise pyrpkg.rpkgError('Could not find the base OS ver from branch name'
                            ' %s' % self.branch_merge)
        self._distval = osver
        self._distval = self._distval.replace('.', '_')
        self._disttag = 'el%s' % self._distval
        self._rpmdefines = ["--define '_sourcedir %s'" % os.path.join(self.path,'SOURCES'),
                            "--define '_specdir %s'" % os.path.join(self.path,'SPECS'),
                            "--define '_builddir %s'" % os.path.join(self.path,'BUILD'),
                            "--define '_srcrpmdir %s'" % os.path.join(self.path,'SRPMS'),
                            "--define '_rpmdir %s'" % os.path.join(self.path, 'RPMS'),
                            "--define 'dist .%s'" % self._disttag,
                            # int and float this to remove the decimal
                            "--define '%s 1'" % self._disttag]

    def load_spec(self):
        """This sets the spec attribute"""

        # We are not using the upstream load_spec because the file structure is
        # hard-coded

        deadpackage = False

        # Get a list of files in the path we're looking at
        files = os.listdir(os.path.join(self.path,'SPECS'))
        # Search the files for the first one that ends with ".spec"
        for f in files:
            if f.endswith('.spec') and not f.startswith('.'):
                self._spec = os.path.join('SPECS',f)
                return
            if f == 'dead.package':
                deadpackage = True
        if deadpackage:
            raise pyrpkg.rpkgError('No spec file found. This package is retired')
        else:
            raise pyrpkg.rpkgError('No spec file found.')


    # These are the commands defined in the base pyrpkg.Commands class
    def load_kojisession(self, *args, **kwargs):
        raise NotImplementedError("This command is not yet implemented in centpkg")

    def add_tag(self, *args, **kwargs):
        raise NotImplementedError("This command is not yet implemented in centpkg")

    def clean(self, *args, **kwargs):
        raise NotImplementedError("This command is not yet implemented in centpkg")

    def clone(self, *args, **kwargs):
        raise NotImplementedError("This command is not yet implemented in centpkg")

    def clone_with_dirs(self, *args, **kwargs):
        raise NotImplementedError("This command is not yet implemented in centpkg")

    def commit(self, *args, **kwargs):
        raise NotImplementedError("This command is not yet implemented in centpkg")

    def delete_tag(self, *args, **kwargs):
        raise NotImplementedError("This command is not yet implemented in centpkg")

    def get_latest_commit(self, *args, **kwargs):
        raise NotImplementedError("This command is not yet implemented in centpkg")

    def gitbuildhash(self, *args, **kwargs):
        raise NotImplementedError("This command is not yet implemented in centpkg")

    def import_srpm(self, *args, **kwargs):
        raise NotImplementedError("This command is not yet implemented in centpkg")

    def list_tag(self, *args, **kwargs):
        raise NotImplementedError("This command is not yet implemented in centpkg")

    def new(self, *args, **kwargs):
        raise NotImplementedError("This command is not yet implemented in centpkg")

    def patch(self, *args, **kwargs):
        raise NotImplementedError("This command is not yet implemented in centpkg")

    def pull(self, *args, **kwargs):
        raise NotImplementedError("This command is not yet implemented in centpkg")

    def push(self, *args, **kwargs):
        raise NotImplementedError("This command is not yet implemented in centpkg")

    def sources(self, *args, **kwargs):
        raise NotImplementedError("This command is not yet implemented in centpkg")

    def switch_branch(self, *args, **kwargs):
        raise NotImplementedError("This command is not yet implemented in centpkg")

    def file_exists(self, *args, **kwargs):
        raise NotImplementedError("This command is not yet implemented in centpkg")

    def upload_file(self, *args, **kwargs):
        raise NotImplementedError("This command is not yet implemented in centpkg")

    def build(self, *args, **kwargs):
        raise NotImplementedError("This command is not yet implemented in centpkg")

    def clog(self, *args, **kwargs):
        raise NotImplementedError("This command is not yet implemented in centpkg")

    def compile(self, *args, **kwargs):
        raise NotImplementedError("This command is not yet implemented in centpkg")

    def giturl(self, *args, **kwargs):
        raise NotImplementedError("This command is not yet implemented in centpkg")

    def koji_upload(self, *args, **kwargs):
        raise NotImplementedError("This command is not yet implemented in centpkg")

    def install(self, *args, **kwargs):
        raise NotImplementedError("This command is not yet implemented in centpkg")

    def lint(self, *args, **kwargs):
        raise NotImplementedError("This command is not yet implemented in centpkg")

    def local(self, *args, **kwargs):
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

    def verify_files(self, *args, **kwargs):
        raise NotImplementedError("This command is not yet implemented in centpkg")
