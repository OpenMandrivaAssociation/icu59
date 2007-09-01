%define major 36
%define libname %mklibname icu %{major}
%define develname %mklibname icu -d
%define realversion 3.6
%define tarballver %(echo %realversion|sed -e 's|\\.|_|')

Summary:	International Components for Unicode
Name:		icu
Version:	%realversion
Release:	%mkrel 4
License:	MIT
Group:		System/Libraries
URL:		http://www.icu-project.org/index.html
Source0:	ftp://ftp.software.ibm.com/software/globalization/icu/%version/%{name}4c-%{tarballver}-src.tgz
Source1:	ftp://ftp.software.ibm.com/software/globalization/icu/%version/%{name}4c-%{tarballver}-docs.zip
Requires:	%{libname} = %{version}-%{release}
BuildRoot:	%{_tmppath}/%{name}-%{version}-root

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
                    
%package	doc
Summary:	Documentation for the International Components for Unicode
Group:		System/Libraries

%description	doc
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
                    

%package -n	%{libname}
Summary:	Libraries for the International Components for Unicode
Group:		System/Libraries
Provides:	lib%name = %{version}-%{release}
Obsoletes:	%mklibname %{name} 34

%description -n	%{libname}
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
                    
%package -n	%{develname}
Summary:	Tools required to embed the International Components for Unicode
Group:		Development/Other
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}%{major}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}
Obsoletes:	%{libname}-devel
%define _requires_exceptions statically\\|linked

%description -n	%{develname}
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
                    

%prep

%setup -q -n %{name}

mkdir -p docs
cd docs
unzip -q %SOURCE1
cd -

%build
cd source
chmod +x runConfigureICU configure install-sh
CFLAGS="%{optflags}" CXXFLAGS="%{optflags}" ./runConfigureICU LinuxRedHat \
    --prefix=%{_prefix} \
    --sysconfdir=%{_sysconfdir} \
    --mandir=%{_mandir} \
    --infodir=%{_infodir}

make
## make check
sed -i -e "s|/lib\([\"/]\)|/%{_lib}\1|" config/icu-config

%install
rm -rf %{buildroot}
cd source
%makeinstall

# fix attribs
chmod 755 %{buildroot}%{_libdir}/*.so*

%clean
rm -rf %{buildroot}

%post -n %{libname} -p /sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/*
%exclude %{_bindir}/icu-config
%{_sbindir}/*
%{_datadir}/%{name}/

%files doc
%defattr(-,root,root)
%doc readme.html docs/*
%{_mandir}/man1/*
%{_mandir}/man8/*

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.*

%files -n %{develname}
%defattr(-,root,root)
%{_bindir}/icu-config
%{_libdir}/*.so
%dir %{_includedir}/layout
%dir %{_includedir}/unicode
%{_includedir}/layout/*
%{_includedir}/unicode/*
#%dir %{_libdir}/%{name}/%{version}
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/*
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*
