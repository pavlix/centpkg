from setuptools import setup

setup(
    name = "centpkg",
    version = "0.4.4",
    author = "Brian Stinson",
    author_email = "bstinson@ksu.edu",
    description = "CentOS Plugin to rpkg for managing RPM package sources",
    url = "http://bitbucket.org/bstinsonmhk/centpkg.git",
    license = "GPLv2+",
    package_dir = {'': 'src'},
    packages = ['centpkg'],
    scripts = ['src/bin/centpkg'],
    data_files = [('/etc/rpkg',['src/centpkg.conf']),]
)
