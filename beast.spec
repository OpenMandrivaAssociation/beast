%define _disable_ld_no_undefined 1

# maintainer is lazy, just using version number as API version and library
# major -- Abel
%define api_version	0.8
%define major		2
%define libname		%mklibname %{name} %{api_version} %{major}
%define develname	%mklibname %{name} -d

%define custom_dsp 0
%{?dsp_device: %global custom_dsp 1}

%define custom_midi 0
%{?midi_device: %global custom_midi 1}

Name:		beast
Summary:	Music composition and audio synthesis framework and tool
Version:	0.8.2
Release:	2
Source0:	ftp://beast.gtk.org/pub/beast/v0.7/%{name}-%{version}.tar.bz2
Source1:	bseapi.idl
URL:		https://beast.gtk.org/
License:	GPLv2+
Group:		Sound
BuildRequires:	groff
BuildRequires:	imagemagick
BuildRequires:	perl-XML-Parser
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(flac)
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(guile-1.8)
BuildRequires:	pkgconfig(libgnomecanvas-2.0)
BuildRequires:	pkgconfig(mad)
BuildRequires:	pkgconfig(pango)
BuildRequires:	pkgconfig(vorbis)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	rapicorn-devel
BuildRequires:	rapicorn
Requires:	%{libname} = %{version}-%{release}

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

%package -n %{libname}
Summary:	Dynamic libraries from %{name}
Group:		System/Libraries
License:	LGPLv2+

%description -n %{libname}
BEAST (the BEdevilled Audio System) is a GTK+/GNOME-based frontend to
BSE (the Bedevilled Sound Engine). BSE comes with the abilities to
load/store songs and synthesis networks (in .bse files), play them
modify them, etc. BEAST provides the necessary GUI to make actual
use of BSE. Synthesis filters (BseSources) are implemented in shared
library modules, and get loaded on demand.

You must install this library before running %{name}.

%package -n %{develname}
Summary:	Header files and static libraries from %{name}
Group: 		Development/C
License:	LGPLv2+
Requires:	%{libname} = %{version}-%{release}
Provides:	%{libname}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{develname}
Libraries and includes files for developing programs based on %{name}.

%prep
%setup -q
perl -p -i -e 's/-DG_DISABLE_DEPRECATED//' bse/Makefile.in bse/Makefile.am

# missing file
cp %{SOURCE1} bse/bseapi.idl

%build
# FIXME: gold linker dies with internal error in convert_types, at ../../gold/gold.h:192 on i586
#%ifarch %{ix86}
#export CC="%{__cc} -fuse-ld=bfd"
#export CXX="%{__cxx} -fuse-ld=bfd"
#%endif
export CFLAGS="$RPM_OPT_FLAGS -fpermissive -fno-strict-aliasing" 
export CXXFLAGS="$RPM_OPT_FLAGS -fpermissive -fno-strict-aliasing" 
%configure2_5x \
%if %{custom_dsp}
	--enable-osspcm=%{dsp_device} \
%else
	--enable-osspcm=/dev/dsp \
%endif
%if %{custom_midi}
	--enable-ossmidi=%{midi_device} \
%else
	--enable-ossmidi=/dev/midi \
%endif

%make

%install
%makeinstall_std UPDATE_MIME_DATABASE=

#icons
mkdir -p %{buildroot}%{_iconsdir} \
         %{buildroot}%{_miconsdir}
install -D -m 644       data/beast.png %{buildroot}%{_liconsdir}/%{name}.png
convert -geometry 32x32 data/beast.png %{buildroot}%{_iconsdir}/%{name}.png
convert -geometry 16x16 data/beast.png %{buildroot}%{_miconsdir}/%{name}.png

# remove files not bundled
rm -f %{buildroot}%{_libdir}/bse/v*/plugins/*.la

%find_lang %{name} --all-name

%files -f %{name}.lang
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

%files -n %{libname}
%{_libdir}/libbse-%{api_version}.so.%{major}*

%files -n %{develname}
%doc ChangeLog
%{_includedir}/*
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.so
%{_mandir}/man5/*


