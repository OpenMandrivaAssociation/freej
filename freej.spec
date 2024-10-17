Name:           freej
Version:        0.10
Release:        %mkrel 3
Summary:        Vision mixer

Group:          Video
License:        GPL
URL:            https://freej.org/
Source0:        ftp://ftp.dyne.org/freej/releases/%{name}-%{version}.tar.gz
Source1:	ipernav.png
Patch0:		freej-0.9-slang.patch
# (fc) 0.9-2mdv V4L2 support (Arnaud Patard)
Patch1:		freej-0.9-v4l2.patch
Patch2:		freej-0.10-new-ffmpeg-header-location.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires:  SDL-devel slang-devel libshout-devel
BuildRequires:	libogg-devel freetype2-devel
BuildRequires:  libpng-devel libjpeg-devel
BuildRequires:	ffmpeg-devel fftw3-devel bluez-devel jackit-devel

%description
FreeJ is a vision mixer: a digital instrument for realtime video
manipulation used in the fields of dance teather, veejaying, medical
visualisation and TV.

It runs a video engine in which multiple layers can be filtered thru
effect chains and then mixed together with images, movies, live
cameras, particle generators, text scrollers and more.  All the
resulting video mix can be shown on multiple and remote screens,
encoded into a movie and streamed live to the internet.

FreeJ can be controlled locally or remotely, also from multiple places
at the same time, using its slick console interface; can be automated
via javascript and operated via MIDI and Joystick.


%prep
%setup -q -n %{name}-%{version}
#%patch0 -p1 -b .slang
#%patch1 -p1 -b .v4l2
%patch2 -p0

%build
autoreconf -i
%configure2_5x
make 

%install
rm -rf %{buildroot}
%makeinstall_std
mkdir -p %{buildroot}%{_datadir}/applications
mkdir -p %{buildroot}%{_datadir}/pixmaps
cp %SOURCE1 %{buildroot}/%{_datadir}/pixmaps/ipernav.png

cat > %{buildroot}%{_datadir}/applications/%{name}.desktop <<EOF
[Desktop Entry]
Name=freej
Comment=Freej is a Vision Mixer
Exec=freej
Icon=ipernav
Categories=AudioVideo;Video;
Terminal=true
Type=Application
EOF

sed -i -e 's,/usr/local/bin,/usr/bin,g' $RPM_BUILD_ROOT%{_datadir}/freej/pan.js doc/freejscript-example.js

# remove unpackaged files
rm -rf %buildroot%_datadir/doc/


%clean
rm -rf %{buildroot}

%files 
%defattr(-,root,root,-)
%doc API AUTHORS COPYING NEWS README TODO USAGE doc/*
%{_bindir}/%{name}
%{_includedir}/%{name}*.h
%{_prefix}/lib/%{name}/*.la
%{_prefix}/lib/%{name}/*.so
%{_datadir}/%{name}/*
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/ipernav.png
%{_mandir}/man1/%{name}*

