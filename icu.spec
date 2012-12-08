%define major %(echo %version |cut -d. -f1)
%define libicudata %mklibname %{name}data %{major}
%define libicui18n %mklibname %{name}i18n %{major}
%define libicuio %mklibname %{name}io %{major}
%define libicule %mklibname %{name}le %{major}
%define libiculx %mklibname %{name}lx %{major}
%define libicutest %mklibname %{name}test %{major}
%define libicutu %mklibname %{name}tu %{major}
%define libicuuc %mklibname %{name}uc %{major}
%define develname %mklibname %{name} -d

%define tarballver %(echo %version|sed -e 's|\\.|_|g')

Summary:	International Components for Unicode
Name:		icu
Epoch:		1
Version:	49.1.1
Release:	2
License:	MIT
Group:		System/Libraries
URL:		http://www.icu-project.org/index.html
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

%package -n %{develname}
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
Provides:	lib%{name}-devel = %{EVRD}
Obsoletes:	%{mklibname -d icu 48} < 1:49
Obsoletes:	%{mklibname -d icu 36} < 1:49
Obsoletes:	%{mklibname -d icu 34} < 1:49
#define _requires_exceptions statically\\|linked

%description -n	%{develname}
Development files and headers for the International Components for Unicode.

%prep
%setup -q -n %{name}
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
%configure2_5x \
	--with-library-bits=64else32 \
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

%files -n %{develname}
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


%changelog
* Sat Apr 07 2012 Bernhard Rosenkraenzer <bero@bero.eu> 1:49.1.1-1
+ Revision: 789731
- Update to 49.1.1

* Fri Feb 17 2012 Matthew Dawkins <mattydaw@mandriva.org> 1:4.8-4
+ Revision: 776216
- rebuild to obsolete old lib pkg

* Fri Feb 17 2012 Matthew Dawkins <mattydaw@mandriva.org> 1:4.8-3
+ Revision: 776158
- split out individual libs

* Thu Jan 12 2012 Oden Eriksson <oeriksson@mandriva.com> 1:4.8-2
+ Revision: 760505
- sync with MDVSA-2011:194

* Sun Jun 05 2011 Funda Wang <fwang@mandriva.org> 1:4.8-1
+ Revision: 682800
- new version 4.8

* Wed May 04 2011 Oden Eriksson <oeriksson@mandriva.com> 1:4.6.1-3
+ Revision: 665501
- mass rebuild

* Mon Mar 14 2011 Funda Wang <fwang@mandriva.org> 1:4.6.1-2
+ Revision: 644587
- do not promote ldflags in icu-config

* Mon Mar 14 2011 Funda Wang <fwang@mandriva.org> 1:4.6.1-1
+ Revision: 644490
- update file list
- new version 4.6.1
- drop merged patches and old icu-config

* Mon Oct 04 2010 Funda Wang <fwang@mandriva.org> 1:4.4.2-1mdv2011.0
+ Revision: 582874
- new version 4.4.2

* Sat Jul 31 2010 Funda Wang <fwang@mandriva.org> 1:4.4.1-1mdv2011.0
+ Revision: 563953
- do not use strict alias patch but use cflags, upstream does not like the patch
- add upstream patch to deal with buffer overflow problem
- revert to 4.4.1 stable

  + Matthew Dawkins <mattydaw@mandriva.org>
    - new version 4.5.1
      patch applied upstream

* Sun Mar 21 2010 Funda Wang <fwang@mandriva.org> 1:4.4-2mdv2010.1
+ Revision: 526037
- install libicutest

* Sat Mar 20 2010 Emmanuel Andry <eandry@mandriva.org> 1:4.4-1mdv2010.1
+ Revision: 525429
- New version 4.4
- New major 44
- rediff p4

  + Funda Wang <fwang@mandriva.org>
    - build 64 bits at first

* Mon Jan 11 2010 Tomasz Pawel Gajc <tpg@mandriva.org> 1:4.2.1-2mdv2010.1
+ Revision: 489818
- Patch4: fix build
- really use 4.2.1 tarballs

* Sat Jul 25 2009 Frederik Himpe <fhimpe@mandriva.org> 1:4.2.1-1mdv2010.0
+ Revision: 399844
- update to new version 4.2.1

* Sun May 31 2009 Funda Wang <fwang@mandriva.org> 1:4.2-2mdv2010.0
+ Revision: 381588
- stil use fedora's icu-config

* Sun May 31 2009 Funda Wang <fwang@mandriva.org> 1:4.2-1mdv2010.0
+ Revision: 381575
- New version 4.2

  + Christophe Fergeau <cfergeau@mandriva.com>
    - fix compilation with gcc 4.4

* Tue Jan 20 2009 Tomasz Pawel Gajc <tpg@mandriva.org> 1:4.0.1-1mdv2009.1
+ Revision: 331791
- update to new version 4.0.1

* Sun Dec 21 2008 Oden Eriksson <oeriksson@mandriva.com> 1:4.0-3mdv2009.1
+ Revision: 316951
- fix build with -Werror=format-security (P3)
- rebuild

* Wed Jul 16 2008 Funda Wang <fwang@mandriva.org> 1:4.0-2mdv2009.0
+ Revision: 236515
- switch fedora's icu-config for the package's own icu-config breaks too much

* Fri Jul 04 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 1:4.0-1mdv2009.0
+ Revision: 231685
- enable epoch :(
- update to new version 4.0 (looks like the versioning has been broken, epoch needed ?)
- fix descriptions
- Patch1: enable build with strict-aliasing
- Patch2: add icu.pc
- add buildrequires on doxygen
- enable checks
- fix file list

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Fri May 30 2008 Funda Wang <fwang@mandriva.org> 4.0.d01-1mdv2009.0
+ Revision: 213349
- New version 4.0.d01

* Sat Jan 26 2008 Funda Wang <fwang@mandriva.org> 3.8.1-2mdv2008.1
+ Revision: 158374
- fix CVE 2007-4770 and 4771

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Fri Dec 14 2007 Funda Wang <fwang@mandriva.org> 3.8.1-1mdv2008.1
+ Revision: 120061
- New version 3.8.1

* Tue Dec 11 2007 Marcelo Ricardo Leitner <mrl@mandriva.com> 3.8-2mdv2008.1
+ Revision: 117322
- Added patch setBreakType, which makes that method public, as OOo requires it
  to be.

* Sat Oct 27 2007 Funda Wang <fwang@mandriva.org> 3.8-1mdv2008.1
+ Revision: 102667
- New version 3.8
- New major ( 36 -> 38 )

* Sat Sep 01 2007 Pascal Terjan <pterjan@mandriva.org> 3.6-4mdv2008.0
+ Revision: 77367
- Move icu-config to -devel package and fix it on x86_64

* Sun Jun 24 2007 Funda Wang <fwang@mandriva.org> 3.6-3mdv2008.0
+ Revision: 43594
- adopt to new devel package policy again

* Thu Jun 21 2007 Funda Wang <fwang@mandriva.org> 3.6-2mdv2008.0
+ Revision: 42306
- Really use correct tarball

* Wed Jun 20 2007 Funda Wang <fwang@mandriva.org> 3.6-1mdv2008.0
+ Revision: 41947
- correct tarball name
  remove invalid directory
  adopt to new develname
- New version
- Import icu



* Tue Jan  3 2006 Götz Waschk <waschk@mandriva.org> 3.4-2mdk
- drop devel package obsoletes
- drop prereq
- make the devel package installable

* Tue Jan 03 2006 Oden Eriksson <oeriksson@mandriva.com> 3.4-1mdk
- 3.4
- drop the upstream patch (P0)
- fix deps
- make it rpmbuildupdate aware

* Tue May 10 2005 Arnaud de Lorbeau <devel@mandriva.com> 3.2-2mdk
- Provides icu32-devel

* Tue May 10 2005 Arnaud de Lorbeau <devel@mandriva.com> 3.2-1mdk
- 3.2

* Mon Jun  7 2004 Götz Waschk <waschk@linux-mandrake.com> 2.8.d01-3mdk
- rebuild

* Fri Jun 04 2004 Marcel Pol <mpol@mandrake.org> 2.8.d01-2mdk
- rebuild

* Wed Dec 17 2003 Marcel Pol <mpol@mandrake.org> 2.8.d01-1mdk
- major is 28
- From Quel Qun <kelk1@hotmail.com>
    - Mandrake package.
