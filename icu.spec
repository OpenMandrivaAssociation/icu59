%define major 46
%define libname %mklibname icu %{major}
%define develname %mklibname icu -d
%define realversion 4.6.1
%define tarballver %(echo %realversion|sed -e 's|\\.|_|g')

Summary:	International Components for Unicode
Name:		icu
Version:	4.6.1
Release:	%mkrel 1
Epoch:		1
License:	MIT
Group:		System/Libraries
URL:		http://www.icu-project.org/index.html
Source0:	http://download.icu-project.org/files/icu4c/%{version}/%{name}4c-%{tarballver}-src.tgz
Source1:	http://download.icu-project.org/files/icu4c/%{version}/%{name}4c-%{tarballver}-docs.zip
Patch0:		%{name}4c-3_8-setBreakType.patch
Patch3:		icu4c-4_0-format_not_a_string_literal_and_no_format_arguments.diff
Patch5:		icu-4.4.1-pkgdata.patch
BuildRequires:	doxygen
Requires:	%{libname} = %{epoch}:%{version}-%{release}
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

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
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description doc
Documentation for the International Components for Unicode.

%package -n %{libname}
Summary:	Libraries for the International Components for Unicode
Group:		System/Libraries

%description -n %{libname}
Libraries for the International Components for Unicode.

%package -n %{develname}
Summary:	Development files for the International Components for Unicode
Group:		Development/Other
Requires:	%{libname} = %{epoch}:%{version}-%{release}
Provides:	%{name}%{major}-devel = %{epoch}:%{version}-%{release}
Provides:	%{name}-devel = %{epoch}:%{version}-%{release}
Provides:	lib%{name}-devel = %{epoch}:%{version}-%{release}
Obsoletes:	%mklibname -d icu 36
Obsoletes:	%mklibname -d icu 34
#define _requires_exceptions statically\\|linked

%description -n	%{develname}
Development files and headers for the International Components for Unicode.

%prep
%setup -q -n %{name}
%patch0 -p1 -b .setBreakType
%patch3 -p0 -b .format_not_a_string_literal_and_no_format_arguments

mkdir -p docs
cd docs
unzip -q %{SOURCE1}
cd -

%build
pushd source
# (tpg) needed for patch 2
export CFLAGS='%optflags -fno-strict-aliasing'
export CXXFLAGS='%optflags -fno-strict-aliasing'
%configure2_5x \
	--with-library-bits=64else32 \
	--disable-rpath \
	--with-data-packaging=library \
	--disable-samples
%make
%make doc
popd

%check
pushd source
make check
popd

%install
rm -rf %{buildroot}
pushd source
%makeinstall_std
popd

%clean
rm -rf %{buildroot}

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%files
%defattr(-,root,root)
%{_bindir}/*
%exclude %{_bindir}/icu-config
%{_sbindir}/*

%files doc
%defattr(-,root,root)
%doc readme.html docs/*
%{_mandir}/man1/*
%{_mandir}/man8/*

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.%{major}*

%files -n %{develname}
%defattr(-,root,root)
%{_bindir}/icu-config
%{_libdir}/*.so
%{_libdir}/pkgconfig/icu.pc
%dir %{_includedir}/layout
%dir %{_includedir}/unicode
%{_includedir}/layout/*
%{_includedir}/unicode/*
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/*
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*
