%define version	0.7.1

# maintainer is lazy, just using version number as API version and library
# major -- Abel
%define api_version	0.7
%define major		1
%define libname %mklibname %{name} %{api_version}
%define develname %mklibname %{name} -d

%define custom_dsp 0
%{?dsp_device: %global custom_dsp 1}

%define custom_midi 0
%{?midi_device: %global custom_midi 1}

Name: 	 	beast
Summary: 	Music composition and audio synthesis framework and tool
Version: 	%{version}
Release: 	%mkrel 5
Source0:	ftp://beast.gtk.org/pub/beast/v0.7/%{name}-%{version}.tar.bz2
Patch0:		%{name}-tests-bse-filtertest.cc.diff
Patch1:		%{name}-data-desktop.in.diff
Patch2:		%{name}-guile-fix.patch
# ubuntuu patches
Patch101: 100_deprecated.diff
Patch102: 200_signal_h.diff
Patch103: 201_sparc_alignment.diff
Patch104:  202_gcc43.diff
Patch105:  203_fix_buffer_overflow.diff
Patch106:  300_mksignals_bashism.diff
URL:		http://beast.gtk.org/
License:	GPLv2+
Group:		Sound
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	guile-devel >= 1.6
BuildRequires:	gtk2-devel >= 2.4.11
BuildRequires:	imagemagick
BuildRequires:	libgnomecanvas2-devel
BuildRequires:	libmad-devel
BuildRequires:	libvorbis-devel >= 1.0
BuildRequires:	X11-devel
BuildRequires:	perl-XML-Parser
BuildRequires:	desktop-file-utils
Requires:	%{libname}_%{major} = %{version}

%description
BEAST (the BEdevilled Audio System) is a GTK+/GNOME-based frontend to
BSE (the Bedevilled Sound Engine). BSE comes with the abilities to
load/store songs and synthesis networks (in .bse files), play them
modify them, etc. BEAST provides the necessary GUI to make actual
use of BSE. Synthesis filters (BseSources) are implemented in shared
library modules, and get loaded on demand.

NOTE: This package assumes audio device of your sound card is /dev/dsp,
and MIDI device is /dev/midi; this setting may not fit your machine. If
this is the case, please rebuild this RPM with the following options
(assuming audio device is /dev/dsp2 and MIDI device is /dev/midi1):

    rpmbuild --rebuild --define='dsp_device /dev/dsp2' \
        --define='midi_device /dev/midi1' beast-?.?.?-?mdk.src.rpm



%package -n 	%{libname}_%{major}
Summary:        Dynamic libraries from %{name}
Group:          System/Libraries
License:	LGPLv2+
Provides:	%{libname} = %{version}-%{release}

%description -n %{libname}_%{major}
BEAST (the BEdevilled Audio System) is a GTK+/GNOME-based frontend to
BSE (the Bedevilled Sound Engine). BSE comes with the abilities to
load/store songs and synthesis networks (in .bse files), play them
modify them, etc. BEAST provides the necessary GUI to make actual
use of BSE. Synthesis filters (BseSources) are implemented in shared
library modules, and get loaded on demand.

You must install this library before running %{name}.

%package -n 	%{develname}
Summary: 	Header files and static libraries from %{name}
Group: 		Development/C
License:	LGPLv2+
Requires: 	%{libname}_%{major} = %{version}
Provides: 	%{libname}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release} 
Obsoletes: 	%{libname}_%{major}-devel

%description -n %{develname}
Libraries and includes files for developing programs based on %{name}.

%prep
%setup -q
%patch0
%patch1
%patch2
%patch101 -p1
%patch102 -p1
%patch103 -p1
%patch104 -p1
%patch105 -p1
%patch106 -p1

%build
%configure2_5x \
%if %custom_dsp
	--enable-osspcm=%dsp_device \
%else
	--enable-osspcm=/dev/dsp \
%endif
%if %custom_midi
	--enable-ossmidi=%midi_device \
%else
	--enable-ossmidi=/dev/midi \
%endif

%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std UPDATE_MIME_DATABASE=

desktop-file-install --vendor="" \
  --remove-category="Application" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications $RPM_BUILD_ROOT%{_datadir}/applications/*

#icons
mkdir -p $RPM_BUILD_ROOT%{_iconsdir} \
         $RPM_BUILD_ROOT%{_miconsdir}
install -D -m 644       data/beast.png $RPM_BUILD_ROOT%{_liconsdir}/%{name}.png
convert -geometry 32x32 data/beast.png $RPM_BUILD_ROOT%{_iconsdir}/%{name}.png
convert -geometry 16x16 data/beast.png $RPM_BUILD_ROOT%{_miconsdir}/%{name}.png

# remove files not bundled
rm -f $RPM_BUILD_ROOT%{_libdir}/bse/v*/plugins/*.la

%find_lang %{name} --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post
%if %mdkversion < 200900
%update_menus
%endif
update-mime-database %{_datadir}/mime > /dev/null
		
%postun
%if %mdkversion < 200900
%clean_menus
%endif
update-mime-database %{_datadir}/mime > /dev/null

%if %mdkversion < 200900
%post -n %{libname}_%{major} -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %{libname}_%{major} -p /sbin/ldconfig
%endif

%files -f %{name}.lang
%defattr(-,root,root)
%doc README AUTHORS COPYING* NEWS TODO
%{_bindir}/*
%{_datadir}/application-registry/*.applications
%{_datadir}/applications/*.desktop
%{_datadir}/bse
%{_datadir}/%{name}
%{_datadir}/mime/packages/*.xml
%{_datadir}/mime-info/*
%{_datadir}/pixmaps/*
%{_libdir}/bse
%{_mandir}/man1/*
%{_liconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_miconsdir}/%{name}.png

%files -n %{libname}_%{major}
%defattr(-,root,root)
%{_libdir}/libbse-%{api_version}.so.%{major}*

%files -n %{develname}
%defattr(-,root,root)
%doc ChangeLog
%{_includedir}/*
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.so
%{_libdir}/*.la
%{_mandir}/man5/*


