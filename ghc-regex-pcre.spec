#
# Conditional build:
%bcond_without	prof	# profiling library
#
%define		pkgname	regex-pcre
Summary:	Replaces/Enhances Text.Regex
Summary(pl.UTF-8):	Rozszerzenie Text.Regex
Name:		ghc-%{pkgname}
Version:	0.94.4
Release:	2
License:	BSD
Group:		Development/Languages
#Source0Download: http://hackage.haskell.org/package/regex-pcre
Source0:	http://hackage.haskell.org/package/%{pkgname}-%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	be3794c67959f2b3b840bd026ef0b9ea
URL:		http://hackage.haskell.org/package/regex-pcre
BuildRequires:	ghc >= 6.12.3
BuildRequires:	ghc-array
BuildRequires:	ghc-base >= 3.0
BuildRequires:	ghc-bytestring
BuildRequires:	ghc-containers
BuildRequires:	ghc-regex-base >= 0.93
%if %{with prof}
BuildRequires:	ghc-prof >= 6.12.3
BuildRequires:	ghc-array-prof
BuildRequires:	ghc-base-prof >= 3.0
BuildRequires:	ghc-bytestring-prof
BuildRequires:	ghc-containers-prof
BuildRequires:	ghc-regex-base-prof >= 0.93
%endif
BuildRequires:	rpmbuild(macros) >= 1.608
Requires(post,postun):	/usr/bin/ghc-pkg
%requires_eq	ghc
Requires:	ghc-array
Requires:	ghc-base >= 3.0
Requires:	ghc-bytestring
Requires:	ghc-containers
Requires:	ghc-regex-base >= 0.93
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

# don't compress haddock files
%define		_noautocompressdoc	*.haddock

%description
The PCRE backend to accompany regex-base, see <http://www.pcre.org/>.

%description -l pl.UTF-8
Backend PCRE towarzyszący regex-base wykorzystujący bibliotekę PCRE
(<http://www.pcre.org/>).

%package prof
Summary:	Profiling %{pkgname} library for GHC
Summary(pl.UTF-8):	Biblioteka profilująca %{pkgname} dla GHC.
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ghc-array-prof
Requires:	ghc-base-prof >= 3.0
Requires:	ghc-bytestring-prof
Requires:	ghc-containers-prof
Requires:	ghc-regex-base-prof >= 0.93

%description prof
Profiling %{pkgname} library for GHC. Should be installed when
GHC's profiling subsystem is needed.

%description prof -l pl.UTF-8
Biblioteka profilująca %{pkgname} dla GHC. Powinna być zainstalowana
kiedy potrzebujemy systemu profilującego z GHC.

%prep
%setup -q -n %{pkgname}-%{version}

%build
runhaskell Setup.hs configure -v2 \
	%{?with_prof:--enable-library-profiling} \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.hs build
runhaskell Setup.hs haddock --executables

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.hs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
%{__rm} -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} %{name}-%{version}-doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

runhaskell Setup.hs register \
	--gen-pkg-config=$RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%doc %{name}-%{version}-doc/*
%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/HSregex-pcre-%{version}.o
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSregex-pcre-%{version}.a

%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Regex
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Regex/*.hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Regex/PCRE
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Regex/PCRE/*.hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Regex/PCRE/ByteString
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Regex/PCRE/ByteString/*.hi

%if %{with prof}
%files prof
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSregex-pcre-%{version}_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Regex/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Regex/PCRE/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Regex/PCRE/ByteString/*.p_hi
%endif
