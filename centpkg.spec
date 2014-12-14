%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}

Name:		centpkg
Version:	0.4.1
Release:	1%{?dist}
Summary:	CentOS utility for working with dist-git

Group:	    Applications/System
License:	GPLv2+
URL:		https://git.centos.org/summary/centpkg.git
Source0:	centpkg-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root%(%{__id_u} -n)

# CentOS Distributed Packages
Requires:   redhat-rpm-config	
Requires:   python-pycurl

# EPEL Distributed Packages
Requires:   pyrpkg >= 1.17 
Requires:   koji 

BuildArch:  noarch

# CentOS Distributed build-requires
BuildRequires: python-devel, python-setuptools

# EPEL Distributed build-requires
BuildRequires: pyrpkg

%description
Provides the centpkg command for working with dist-git

%prep
%setup -q


%build
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc README.md COPYING
%config(noreplace) %{_sysconfdir}/rpkg
%{_bindir}/%{name}
%{python_sitelib}/*


%changelog
* Sun Dec 14 2014 Brian Stinson bstinson@ksu.edu - 0.4.1-1
- Fix a disttag regression and add a "patch" version number

* Sat Nov 23 2014 Brian Stinson bstinson@ksu.edu - 0.2-1
- The srpm workflow to the CBS works now

* Sat Jul 05 2014 Brian Stinson bstinson@ksu.edu - 0.1-2
- Update readme and add exception checking when running toplevel commands

* Sat Jul 05 2014 Brian Stinson bstinson@ksu.edu - 0.1-1
- Local builds and mockbuilds work 



