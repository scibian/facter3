# Only >=el7 and fedora have a sufficient version of ruby available
%if 0%{?rhel} >= 7 || 0%{?fedora}
%{!?vendor_ruby: %global vendor_ruby %(ruby -rrbconfig -e "puts RbConfig::CONFIG['vendordir']")}
%endif

# Building debuginfo is pointless, as this has no symbols.
%global debug_package %{nil}

# VERSION is subbed out during rake srpm process
%global realversion 3.10.0
%global rpmversion 3.10.0

%global build_prefix /opt/pl-build-tools
%global _prefix /usr
%global _libdir %{_prefix}/lib

Name:           facter
Summary:        A command line tool and library for collecting simple facts about a host operating system
Version:        %{rpmversion}
Release:        1%{?dist}
Epoch:          1
Vendor:         %{?_host_vendor}
License:        ASL 2.0
Group:          System Environment/Base
URL:            http://www.puppetlabs.com/puppet/related-projects/%{name}
# Note this     URL will only be valid at official tags from Puppet Labs
Source0:        http://puppetlabs.com/downloads/%{name}/%{name}-%{realversion}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# Only >=el7 and fedora have a sufficient version of ruby available
%if 0%{?rhel} >= 7 || 0%{?fedora}
BuildRequires:  ruby
BuildRequires:  ruby-devel
%endif
BuildRequires:  pl-gcc >= 4.8.2-4
BuildRequires:  pl-cmake >= 3.2.2-1
BuildRequires:  pl-libboost-devel >= 1.55.0-4
BuildRequires:  pl-libboost-static >= 1.55.0-4
BuildRequires:  pl-libyaml-cpp-devel >= 0.5.1-5
BuildRequires:  pl-libyaml-cpp-static >= 0.5.1-5

%if 0%{?rhel} > 5
BuildRequires:  openssl-devel
BuildRequires:  libblkid-devel
BuildRequires:  libcurl-devel
%endif

Requires: glibc
%if 0%{?rhel} > 5
Requires: libblkid
Requires: libcurl
%endif
# If we're linking against openssl, we need to ensure those libraries are available
# during runtime. On EL7, those dependency libraries are available via the openssl-libs
# package, but we don't have that package on earlier versions. We want to install as
# few extra packages as possible, which is why we're installing openssl-libs when available.
%if 0%{?rhel} >= 7
Requires: openssl-libs
%endif
%if 0%{?rhel} == 6
Requires: openssl
%endif

AutoReq:  0
AutoProv: 0

%description
A command line tool and library for collecting simple facts about a host Operating
system. Some of the facts are preconfigured, such as the hostname and the
operating system. Additional facts can be added through simple Ruby scripts

%prep
%setup -q  -n %{name}-%{realversion}

%build
rm -rf %{buildroot}
%{build_prefix}/bin/cmake \
  -DCMAKE_TOOLCHAIN_FILE=%{build_prefix}/pl-build-toolchain.cmake \
  -DCMAKE_VERBOSE_MAKEFILE=ON \
  -DCMAKE_INSTALL_PREFIX=%{_prefix} \
  -DBOOST_STATIC=ON \
  -DYAMLCPP_STATIC=ON \
  .
  make %{?_smp_mflags} DESTDIR=%{buildroot}

%install
make %{?_smp_mflags} install DESTDIR=%{buildroot}

%clean
rm -rf %{buildroot}

%check
%{build_prefix}/bin/ctest -V

%files
%defattr(-,root,root,-)
%{_bindir}/facter
%{_libdir}/libfacter.so*
%{_includedir}/facter
%{_mandir}/man8/facter.8.gz
%if 0%{?rhel} >= 7 || 0%{?fedora}
%{vendor_ruby}/facter.rb
%endif
%doc LICENSE README.md


%changelog
* Mon Feb 12 2018 Puppet Labs Release <info@puppetlabs.com> - 1:3.10.0-1
- Build for 3.10.0

* Fri Mar 20 2015 Michael Smith <michael.smith@puppetlabs.com> - 2.4.2-1
- Move from Ruby to C++ implementation.
