# TODO:
# - prebuilt kernel modules as kernel-oss subpackage
# - cleanup/PLDify scripts (soundon, soundoff, init)
Summary:	Open Sound System (OSS) v4
Summary(pl.UTF-8):	Podsystem dźwięku OSS (Open Sound System) w wersji 4
Name:		oss
%define	ver	4.2
%define	subver	2008
Version:	%{ver}.%{subver}
Release:	0.1
License:	GPL v2
Group:		Libraries
Source0:	http://www.4front-tech.com/developer/sources/stable/gpl/%{name}-v%{ver}-build%{subver}-src-gpl.tar.bz2
# Source0-md5:	cc5c982a3d9da51ff612285db61b4952
Patch0:		%{name}-install.patch
URL:		http://www.opensound.com/
BuildRequires:	alsa-lib-devel
BuildRequires:	gawk
BuildRequires:	gtk+2-devel >= 2.0
BuildRequires:	libvorbis-devel
BuildRequires:	pkgconfig
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
It is an open source version of the Open Sound System (OSS) sound
subsystem software released under the GPL license.

%description -l pl.UTF-8
Wersja podsystemu dźwięku Open Sound System o otwartych źródłach
wydana na licencji GPL.

%package init
Summary:	SysV init script for OSS v4
Summary(pl.UTF-8):	Skrypt SysV init dla OSS v4
Group:		Applications/System
Requires(post,preun):	/sbin/chkconfig
Requires:	%{name} = %{version}-%{release}

%description init
SysV init script for OSS v4.

%description init -l pl.UTF-8
Skrypt SysV init dla OSS v4.

%package gui
Summary:	OSS v4 mixer with GUI
Summary(pl.UTF-8):	Mikser OSS v4 z graficznym interfejsem użytkownika
Group:		X11/Applications/Sound
Requires:	%{name} = %{version}-%{release}

%description gui
OSS v4 mixer with GUI.

%description gui -l pl.UTF-8
Mikser OSS v4 z graficznym interfejsem użytkownika.

%package libs
Summary:	OSS v4 support libraries
Summary(pl.UTF-8):	Biblioteki wspomagające OSS v4
Group:		Libraries

%description libs
OSS v4 support libraries.

%description libs -l pl.UTF-8
Biblioteki wspomagające OSS v4.

%package devel
Summary:	Header files for OSS v4 API
Summary(pl.UTF-8):	Pliki nagłówkowe API OSS v4
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header files for OSS v4 API.

%description devel -l pl.UTF-8
Pliki nagłówkowe API OSS v4.

%prep
%setup -q -n %{name}-v%{ver}-build%{subver}-src-gpl
%patch0 -p1

%build
install -d build
cd build
# not autoconf configure
CC="%{__cc}" \
../configure \
%ifarch %{ix86}
	--regparm
%else
	--noregparm
%endif

%{__make}

%{__cc} -o oss/lib/libflashsupport.so -shared \
	%{rpmldflags} %{rpmcflags} %{rpmcppflags} \
	../oss/lib/flashsupport.c -Wall -lssl

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/oss,/etc/rc.d/init.d,%{_includedir}}

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

# install in system lib and include dirs
%{__mv} $RPM_BUILD_ROOT%{_libdir}/oss/lib/lib* $RPM_BUILD_ROOT%{_libdir}
%{__rm} -r $RPM_BUILD_ROOT%{_libdir}/oss/lib
install build/oss/lib/libflashsupport.so $RPM_BUILD_ROOT%{_libdir}
/sbin/ldconfig -n $RPM_BUILD_ROOT%{_libdir}
%{__mv} $RPM_BUILD_ROOT%{_libdir}/oss/include $RPM_BUILD_ROOT%{_includedir}/oss

# init script
%{__mv} $RPM_BUILD_ROOT%{_libdir}/oss/etc/S89oss $RPM_BUILD_ROOT/etc/rc.d/init.d/oss

# configuration
%{__mv} $RPM_BUILD_ROOT%{_libdir}/oss/conf.tmpl $RPM_BUILD_ROOT%{_sysconfdir}/oss/conf
ln -sf %{_sysconfdir}/oss/conf $RPM_BUILD_ROOT%{_libdir}/oss/conf
%{__mv} $RPM_BUILD_ROOT%{_libdir}/oss/soundon.user $RPM_BUILD_ROOT%{_sysconfdir}/oss
ln -sf %{_susconfdir}/oss/soundon.user $RPM_BUILD_ROOT%{_libdir}/oss/soundon.user

# - cleanups:
# kernel modules (re)building infrastructure
%{__rm} -r $RPM_BUILD_ROOT%{_libdir}/oss/{build,cuckoo,modules.*,objects.*}
# not for rpm system
%{__rm} $RPM_BUILD_ROOT%{_libdir}/oss/scripts/{remove_drv.sh,restore_drv.sh,setup-alsa.sh} \
	$RPM_BUILD_ROOT%{_libdir}/oss/sysfiles.list
rmdir $RPM_BUILD_ROOT%{_libdir}/oss/save
# obsolete hal support
%{__rm} $RPM_BUILD_ROOT%{_libdir}/oss/scripts/90-oss_usb-create-device.fdi

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc COPYING Changelog RELNOTES.txt 
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/oss.conf
%dir %{_sysconfdir}/oss
%dir %{_sysconfdir}/oss/conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/oss/conf/*.conf
%attr(755,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/oss/soundon.user
%attr(755,root,root) %{_bindir}/ossinfo
%attr(755,root,root) %{_bindir}/ossmix
%attr(755,root,root) %{_bindir}/osspartysh
%attr(755,root,root) %{_bindir}/ossphone
%attr(755,root,root) %{_bindir}/ossplay
%attr(755,root,root) %{_bindir}/ossrecord
%attr(755,root,root) %{_bindir}/osstest
%attr(755,root,root) %{_sbindir}/ossdetect
%attr(755,root,root) %{_sbindir}/ossdevlinks
%attr(755,root,root) %{_sbindir}/ossmixd
%attr(755,root,root) %{_sbindir}/ossvermagic
%attr(755,root,root) %{_sbindir}/savemixer
%attr(755,root,root) %{_sbindir}/soundoff
%attr(755,root,root) %{_sbindir}/soundon
%attr(755,root,root) %{_sbindir}/vmixctl
%dir %{_libdir}/oss
%{_libdir}/oss/conf
%dir %{_libdir}/oss/etc
%{_libdir}/oss/etc/devices.list
# to /var/lib ?
#%{_libdir}/oss/etc/installed_drivers
# XXX: move to /etc/oss
#%{_libdir}/oss/etc/userdefs
%{_libdir}/oss/soundon.user
%{_libdir}/oss/version.dat
%dir %{_libdir}/oss/scripts
%attr(755,root,root) %{_libdir}/oss/scripts/killprocs.sh
%attr(755,root,root) %{_libdir}/oss/scripts/oss_usb-create-devices
%attr(755,root,root) %{_libdir}/oss/scripts/showprocs.sh
%{_mandir}/man1/ossinfo.1*
%{_mandir}/man1/ossmix.1*
%{_mandir}/man1/osspartysh.1*
%{_mandir}/man1/ossphone.1*
%{_mandir}/man1/ossplay.1*
%{_mandir}/man1/ossrecord.1*
%{_mandir}/man1/osstest.1*
%{_mandir}/man1/soundoff.1*
%{_mandir}/man1/soundon.1*
%{_mandir}/man7/dsp.7*
%{_mandir}/man7/midi.7*
%{_mandir}/man7/mixer.7*
%{_mandir}/man7/oss_*.7*
%{_mandir}/man7/osscore.7*
%{_mandir}/man7/sndstat.7*
%{_mandir}/man8/ossdetect.8*
%{_mandir}/man8/ossdevlinks.8*
%{_mandir}/man8/savemixer.8*
%{_mandir}/man8/vmixctl.8*

%files init
%defattr(644,root,root,755)
%attr(754,root,root) /etc/rc.d/init.d/oss

%files gui
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/ossxmix
%{_mandir}/man1/ossxmix.1*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libOSSlib.so
%attr(755,root,root) %{_libdir}/libossmix.so
%attr(755,root,root) %{_libdir}/libsalsa.so.2.0.0
%attr(755,root,root) %ghost %{_libdir}/libsalsa.so.2
%attr(755,root,root) %{_libdir}/libflashsupport.so

%files devel
%defattr(644,root,root,755)
%{_includedir}/oss
