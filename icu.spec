%define major %(echo %{version} |cut -d. -f1)
%define libicudata %mklibname %{name}data %{major}
%define libicui18n %mklibname %{name}i18n %{major}
%define libicuio %mklibname %{name}io %{major}
%define libicule %mklibname %{name}le %{major}
%define libiculx %mklibname %{name}lx %{major}
%define libicutest %mklibname %{name}test %{major}
%define libicutu %mklibname %{name}tu %{major}
%define libicuuc %mklibname %{name}uc %{major}
%define devname %mklibname %{name} -d

%define tarballver %(echo %{version}|sed -e 's|\\.|_|g')
%bcond_with	crosscompile

Summary:	International Components for Unicode
Name:		icu
Epoch:		1
Version:	51.2
Release:	5
License:	MIT
Group:		System/Libraries
Url:		http://www.icu-project.org/index.html
Source0:	http://download.icu-project.org/files/icu4c/%{version}/%{name}4c-%{tarballver}-src.tgz
Source1:	http://download.icu-project.org/files/icu4c/%{version}/%{name}4c-%{tarballver}-docs.zip
Patch0:		%{name}4c-49.1-setBreakType.patch
Patch6:		icu-4.6.1-do-not-promote-ldflags.patch
BuildRequires:	doxygen

%description
The International Components for Unicode (ICU) libraries provide robust and
full-featured Unicode services on a wide variety of platforms. ICU supports
the most current version of the Unicode standard, and they provide support
for supplementary Unicode characters (needed for GB 18030 repertoire support).

As computing environments become more heterogeneous, software portability
becomes more important. ICU lets you produce the same results across all the
various platforms you support, without sacrificing performance. It offers
great flexibility to extend and customize the supplied services, which 
include:

  * Text: Unicode text handling, full character properties and character set
    conversions (500+ codepages)
  * Analysis: Unicode regular expressions; full Unicode sets; character, word
    and line boundaries
  * Comparison: Language sensitive collation and searching
  * Transformations: normalization, upper/lowercase, script transliterations 
    (50+ pairs)
  * Locales: Comprehensive locale data (230+) and resource bundle architecture
  * Complex Text Layout: Arabic, Hebrew, Indic and Thai
  * Time: Multi-calendar and time zone
  * Formatting and Parsing: dates, times, numbers, currencies, messages and   
    rule based

%package doc
Summary:	Documentation for the International Components for Unicode
Group:		System/Libraries
Requires:	%{name} >= %{EVRD}

%description doc
Documentation for the International Components for Unicode.

%package -n %{libicudata}
Summary:	Library for the International Components for Unicode - icudata
Group:		System/Libraries
Obsoletes:	%{mklibname icu 44} <= 4.4.2

%description -n %{libicudata}
Library for the International Components for Unicode - icudata.

%package -n %{libicui18n}
Summary:	Library for the International Components for Unicode - icui18n
Group:		System/Libraries

%description -n %{libicui18n}
Library for the International Components for Unicode - icui18n.

%package -n %{libicuio}
Summary:	Library for the International Components for Unicode - icuio
Group:		System/Libraries

%description -n %{libicuio}
Library for the International Components for Unicode - icuio.

%package -n %{libicule}
Summary:	Library for the International Components for Unicode - icule
Group:		System/Libraries

%description -n %{libicule}
Library for the International Components for Unicode - icule.

%package -n %{libiculx}
Summary:	Library for the International Components for Unicode - iculx
Group:		System/Libraries

%description -n %{libiculx}
Library for the International Components for Unicode - iculx.

%package -n %{libicutest}
Summary:	Library for the International Components for Unicode - icutest
Group:		System/Libraries

%description -n %{libicutest}
Library for the International Components for Unicode - icutest.

%package -n %{libicutu}
Summary:	Library for the International Components for Unicode - icutu
Group:		System/Libraries

%description -n %{libicutu}
Library for the International Components for Unicode - icutu.

%package -n %{libicuuc}
Summary:	Library for the International Components for Unicode - icuuc
Group:		System/Libraries

%description -n %{libicuuc}
Library for the International Components for Unicode - icuuc.

%package -n %{devname}
Summary:	Development files for the International Components for Unicode
Group:		Development/Other
Requires:	%{libicudata} >= %{EVRD}
Requires:	%{libicui18n} >= %{EVRD}
Requires:	%{libicuio} >= %{EVRD}
Requires:	%{libicule} >= %{EVRD}
Requires:	%{libiculx} >= %{EVRD}
Requires:	%{libicutest} >= %{EVRD}
Requires:	%{libicutu} >= %{EVRD}
Requires:	%{libicuuc} >= %{EVRD}
Provides:	%{name}%{major}-devel = %{EVRD}
Provides:	%{name}-devel = %{EVRD}
#define _requires_exceptions statically\\|linked

%description -n	%{devname}
Development files and headers for the International Components for Unicode.

%prep
%setup -qn %{name}
%patch0 -p1 -b .setBreakType
%patch6 -p0 -b .ldflags

mkdir -p docs
cd docs
unzip -q %{SOURCE1}
cd -

%build
pushd source
# (tpg) needed for patch 2
export CFLAGS='%{optflags} -fno-strict-aliasing'
export CXXFLAGS='%{optflags} -fno-strict-aliasing'
# If we want crosscompile icu we need to built ICU package
# and add --with-cross-build=/path/to/icu
# disable bits and do unset TARGET twice, after configure
# and before makeinstall
%configure2_5x \
%if !%{with crosscompile}
	--with-library-bits=64else32 \
%endif
	--with-data-packaging=library \
%if %{with crosscompile}
	--with-cross-build=/path/to/built/icu/source/ \
%endif
	--disable-samples
%if %{with crosscompile}
unset TARGET
%endif
%make
%make doc
popd

%check
pushd source
make check
popd

%install
%if %{with crosscompile}
unset TARGET
%endif
%makeinstall_std -C source

%files
%{_bindir}/*
%exclude %{_bindir}/icu-config
%{_sbindir}/*

%files doc
%doc readme.html docs/*
%{_mandir}/man1/*
%{_mandir}/man8/*

%files -n %{libicudata}
%{_libdir}/libicudata.so.%{major}*

%files -n %{libicui18n}
%{_libdir}/libicui18n.so.%{major}*

%files -n %{libicuio}
%{_libdir}/libicuio.so.%{major}*

%files -n %{libicule}
%{_libdir}/libicule.so.%{major}*

%files -n %{libiculx}
%{_libdir}/libiculx.so.%{major}*

%files -n %{libicutest}
%{_libdir}/libicutest.so.%{major}*

%files -n %{libicutu}
%{_libdir}/libicutu.so.%{major}*

%files -n %{libicuuc}
%{_libdir}/libicuuc.so.%{major}*

%files -n %{devname}
%{_bindir}/icu-config
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%dir %{_includedir}/layout
%dir %{_includedir}/unicode
%{_includedir}/layout/*
%{_includedir}/unicode/*
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/*
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*

