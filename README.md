# Centpkg
Centpkg is a wrapper for [rpkg](https://fedorahosted.org/rpkg/) which interacts
with RPM git repositories like the ones hosted at http://git.centos.org. Rpkg also provides
some convenience methods/commands for local builds via mock or rpmbuild, for
interacting with koji, and for generating patches.

# Centpkg is in pre-alpha state, as of now this is a proof of concept.
For now only a very small subset of rpkg commands are enabled. 

Exception handling at the top level has been disabled for now to get better
tracebacks during development. 



## Installing
Centpkg currently requires the [EPEL](https://fedoraproject.org/wiki/EPEL) repository for pyrpkg and other dependencies. 

    root# <Install and configure EPEL-Release>
    root# yum install pyrpkg
    root# git clone https://bitbucket.org/bstinsonmhk/centpkg.git
    root# cd centpkg
    root# python setup.py install

## Currently Somewhat-working Commands

### Git Operations
    $ centpkg clone --anonymous -b c7 a2ps        # clones the CentOS 7 branch of the a2ps package
    $ centpkg add-tag                             # Adds a git tag to the repo
    $ centpkg list-tag                            # Shows the relevant git tags
    $ centpkg delete-tag                          # Shows the relevant git tags
    $ centpkg commit                              # Commits to the current branch
    $ centpkg pull                                # Pulls from the git remote
    $ centpkg switch-branch                       # Switch to a git branch (if it exists upstream it will track it for you)

### File/Working directory operations 
    $ centpkg sources                             # Downloads the binary sources from lookaside and checks hashes
    $ centpkg clean                               # Removes untracked files

### rpmbuild Operations
    $ centpkg local                               # Runs a full rpmbuild
    $ centpkg compile                             # Runs rpmbuild -bc
    $ centpkg verify-files                        # Runs rpmbuild -bl

## License

Unless otherwise specified, all files are licensed under GPLv2+.
See COPYING for more license information
