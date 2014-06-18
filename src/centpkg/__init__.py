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
        for f in files:
            if f.endswith('.spec') and not f.startswith('.'):
                self._spec = os.path.join('SPECS',f)
                return

        raise pyrpkg.rpkgError('No spec file found.')


    # These are the commands defined in the base pyrpkg.Commands class
    def load_kojisession(self, *args, **kwargs):
        raise NotImplementedError("This command is not yet implemented in centpkg")

    def add_tag(self, *args, **kwargs):
        raise NotImplementedError("This command is not yet implemented in centpkg")

    def clean(self, *args, **kwargs):
        raise NotImplementedError("This command is not yet implemented in centpkg")

    def clone(self, *args, **kwargs):
        super(Commands,self).clone(*args, **kwargs)

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

    def sources(self, outdir=None):
        """Download source files"""

        # We are not using sources() in super because the metadata file is
        # hard-coded into the first open() call. Otherwise this is copied from
        # upstream pyrpkg

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
            # There is some code here for using pycurl, but for now,
            # just use subprocess
            #output = open(file, 'wb')
            #curl = pycurl.Curl()
            #curl.setopt(pycurl.URL, url)
            #curl.setopt(pycurl.FOLLOWLOCATION, 1)
            #curl.setopt(pycurl.MAXREDIRS, 5)
            #curl.setopt(pycurl.CONNECTTIMEOUT, 30)
            #curl.setopt(pycurl.TIMEOUT, 300)
            #curl.setopt(pycurl.WRITEDATA, output)
            #try:
            #    curl.perform()
            #except:
            #    print "Problems downloading %s" % url
            #    curl.close()
            #    output.close()
            #    return 1
            #curl.close()
            #output.close()
            # These options came from Makefile.common.
            # Probably need to support wget as well
            command = ['curl', '-H', 'Pragma:', '-o', outfile, '-R', '-S', '--fail']
            if self.quiet:
                command.append('-s')
            command.append(url)
            self._run_command(command)
            if not self._verify_file(outfile, csum, self.lookasidehash):
                raise pyrpkg.rpkgError('%s failed checksum' % file)
        return

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
