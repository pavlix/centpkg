# Centpkg
Centpkg is a wrapper for [rpkg](https://fedorahosted.org/rpkg/) which interacts
with RPM git repositories like the ones hosted at http://git.centos.org. Rpkg also provides
some convenience methods/commands for local builds via mock or rpmbuild, for
interacting with koji, and for generating patches.

# Centpkg is in pre-alpha state, as of now this is a proof of concept.
For now only a very small subset of rpkg commands are enabled. 

Exception handling at the top level has been disabled for now to get better
tracebacks during development. 

## Current workflow
For a sig working on a package in git.centos.org, the following workflow is
recommended:

    # In this example a member of the virt sig would like to scratch-build a2ps on EL6
    $ centpkg clone -b virt6 a2ps
    $ cd a2ps
    $ centpkg build --srpm --scratch 

    # Tagged builds can be done also 
    $ centpkg build --srpm


## License

Unless otherwise specified, all files are licensed under GPLv2+.
See COPYING for more license information
