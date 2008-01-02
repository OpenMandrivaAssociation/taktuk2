%define name taktuk2
%define version 0.5
%define pre 7
%define release %mkrel 6

Summary: 	Parallel, scalable launcher for cluster and lightweight grids
Name: 		%{name}
Version: 	%{version}
Release: 	%{release}
Source0: 	%{name}_%{version}-%{pre}.tar.bz2
Patch0: 	taktuk2-0.5.patch
Patch1: 	taktuk2-x86_64.patch
Patch2:		taktuk-includes.patch
Patch3:		taktuk-IOredir.patch
Patch4:		taktuk-CoreTCP.patch
Patch5:		taktuk-ldouble.patch
Patch6:		taktuk2-0.5-ppclinux.patch
License: 	GPL
Group: 		Networking/Remote access
Url: 		http://www-id.imag.fr/Logiciels/TakTuk/
BuildRoot:	 %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:  autoconf2.1, automake
Provides: 	parallel-tools

%description
Taktuk is a parallel and scalable remote execution tool for cluster. 
It works by propagating the execution of a parallel program on all 
target nodes, using standard remote execution protocols (rsh, ssh, 
etc...). Remote call scheduling automatically adapts its behavior to 
the remote execution protocol used, and to the load of the network 
and remote hosts. This tool is completely independent of the remote 
protocol used. All remote execution protocols providing an IO redirection
of the remote process launched may be used. A grammar may be optionally 
provided to describe the environment, hence providing increased overall 
deployment speed in the context of a complex topology (for instance in 
a grid environment). For a more responsive deployment a remote launch 
(rsh ssh or other) delay can be bounded to bypass slow nodes and ignore
the specific timeout provided by the protocol used. Taktuk provides full
IO and signal redirection to the original console user.


%package -n %{name}-devel
Summary:        Taktuk header files and static libraries
Group:          Development/Other
Requires:       %{name} = %{version}

%description -n %{name}-devel
Taktuk header files and static libraries

%package -n %{name}-viewnet
Summary:        Taktuk viewnet tool
Requires:       %{name} = %{version}
Group: 		Networking/Remote access
Requires:	gv

%description -n %{name}-viewnet
This rpm allow to to graph the taktuk network using gv


%prep
%setup -q -n %name-%version
%patch0 -p1 
%patch1 -p0
%patch2 -p0
%patch3 -p0
%patch4 -p0
%patch5 -p0
%patch6 -p1 -b .ppclinux

%build
aclocal
autoheader-2.13
automake
autoconf
%configure --with-pthread --with-psocket --with-netcore --with-taktuk --with-doc
#	--enable-debug \
#	--enable-staticbin \
#	--enable-static \
make CXXFLAGS="-O3 -fpermissive"

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall CXXFLAGS="-O3 -fpermissive"
#remove unwanted files
rm %{buildroot}/usr/doc/AUTHORS
rm %{buildroot}/usr/doc/CHANGES_VERSIONS
rm %{buildroot}/usr/doc/DEVELOPERS
rm %{buildroot}/usr/doc/README

# rename to avoidconflit with ka-run-2.0
mv %{buildroot}%{_bindir}/mput %{buildroot}%{_bindir}/mput2
mv %{buildroot}%{_bindir}/rshp %{buildroot}%{_bindir}/rshp2
mv %{buildroot}%{_mandir}/man1/mput.1 %{buildroot}%{_mandir}/man1/mput2.1
mv %{buildroot}%{_mandir}/man1/rshp.1 %{buildroot}%{_mandir}/man1/rshp2.1
%multiarch_includes $RPM_BUILD_ROOT%{_includedir}/inuk/inuk_conf.h

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc README COPYING DEVELOPERS CHANGES_VERSIONS AUTHORS
%attr(755,root,root) %{_bindir}/mput2
%attr(755,root,root) %{_bindir}/rshp2
%attr(755,root,root) %{_bindir}/sentinelle
%attr(755,root,root) %{_bindir}/taktukdbx
%attr(755,root,root) %{_bindir}/taktukdrawnet
%attr(755,root,root) %{_bindir}/taktukrun
%{_mandir}/man1/*

%files -n %{name}-devel
%defattr(-,root,root)
%doc README COPYING DEVELOPERS CHANGES_VERSIONS AUTHORS
%{_libdir}/*.a
%{_includedir}/*
%multiarch %{multiarch_includedir}/inuk/inuk_conf.h

%files -n %{name}-viewnet
%defattr(-,root,root)
%attr(755,root,root) %{_bindir}/viewnet


