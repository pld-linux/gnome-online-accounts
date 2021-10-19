#
# Conditional build:
%bcond_with	kerberos5	# Kerberos 5 support [TODO: heimdal support; needs MIT currently]
%bcond_with	webkitinspector	# WebKitInspector for the embedded web view

Summary:	Provide online accounts information
Summary(pl.UTF-8):	Dostarczanie informacji o kontach w serwisach sieciowych
Name:		gnome-online-accounts
Version:	3.40.1
Release:	1
License:	LGPL v2+
Group:		Libraries
Source0:	https://download.gnome.org/sources/gnome-online-accounts/3.40/%{name}-%{version}.tar.xz
# Source0-md5:	1de58590b3ee3259fe00bdb4effb4051
URL:		https://wiki.gnome.org/Projects/GnomeOnlineAccounts
BuildRequires:	autoconf >= 2.64
BuildRequires:	automake >= 1:1.11
BuildRequires:	dbus-glib-devel
BuildRequires:	gettext-tools >= 0.19.8
BuildRequires:	glib2-devel >= 1:2.52.0
BuildRequires:	gobject-introspection-devel >= 0.6.2
BuildRequires:	gtk+3-devel >= 3.20.0
BuildRequires:	gtk-doc >= 1.3
BuildRequires:	gtk-webkit4-devel >= 2.26.0
BuildRequires:	json-glib-devel
BuildRequires:	libsecret-devel >= 0.5
BuildRequires:	libsoup-devel >= 2.42.0
BuildRequires:	libtool >= 2:2.2
BuildRequires:	libxml2-devel >= 2
BuildRequires:	libxslt-progs
BuildRequires:	pkgconfig >= 1:0.16
BuildRequires:	rest-devel >= 0.7
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.752
BuildRequires:	tar >= 1:1.22
BuildRequires:	udev-glib-devel
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xz
%if %{with kerberos5}
BuildRequires:	gcr-devel >= 3
BuildRequires:	krb5-devel
%endif
Requires:	%{name}-libs = %{version}-%{release}
Requires(post,postun):	gtk-update-icon-cache
Requires:	hicolor-icon-theme
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
gnome-online-accounts provides interfaces so applications and
libraries in GNOME can access the user's online accounts.

%description -l pl.UTF-8
gnome-online-accounts udostępnia interfejsy pozwalające aplikacjom i
bibliotekom GNOME na dostęp do kont użytkownika w serwisach
sieciowych.

%package libs
Summary:	gnome-online-accounts libraries
Summary(pl.UTF-8):	Biblioteki gnome-online-accounts
Group:		Libraries
Requires:	glib2 >= 1:2.52.0
Requires:	gtk+3 >= 3.20.0
Requires:	gtk-webkit4 >= 2.26.0
Requires:	libsecret >= 0.5
Requires:	libsoup >= 2.42.0
Conflicts:	gnome-online-accounts < 3.8.2-1.1

%description libs
gnome-online-accounts libraries.

%description libs -l pl.UTF-8
Biblioteki gnome-online-accounts.

%package devel
Summary:	Development files for gnome-online-accounts libraries
Summary(pl.UTF-8):	Pliki programistyczne bibliotek gnome-online-accounts
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	glib2-devel >= 1:2.52.0
Requires:	gtk+3-devel >= 3.20.0

%description devel
The gnome-online-accounts-devel package contains the header files for
developing applications that use gnome-online-accounts.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe do tworzenia aplikacji
wykorzystujących gnome-online-accounts.

%package apidocs
Summary:	GOA API documentation
Summary(pl.UTF-8):	Dokumentacja API GOA
Group:		Documentation
Requires:	gtk-doc-common
BuildArch:	noarch

%description apidocs
GOA API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API GOA.

%package -n vala-gnome-online-accounts
Summary:	Vala API for gnome-online-accounts libraries
Summary(pl.UTF-8):	API języka Vala do bibliotek gnome-online-accounts
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	vala >= 2:0.16.0
BuildArch:	noarch

%description -n vala-gnome-online-accounts
Vala API for gnome-online-accounts libraries.

%description -n vala-gnome-online-accounts -l pl.UTF-8
API języka Vala do bibliotek gnome-online-accounts.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
# "fedora" is krb5+gcr
%configure \
	--disable-silent-rules \
	--disable-static \
	--enable-documentation \
	%{!?with_kerberos:--disable-fedora} \
	--enable-gtk-doc \
	%{?with_webkitinspector:--enable-inspector} \
	%{__enable_disable kerberos5 kerberos} \
	--enable-lastfm \
	--enable-media-server \
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la
%{__rm} $RPM_BUILD_ROOT%{_libdir}/goa-1.0/web-extensions/lib*.la

%find_lang gnome-online-accounts --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_icon_cache hicolor

%postun
%update_icon_cache hicolor

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files -f gnome-online-accounts.lang
%defattr(644,root,root,755)
%doc NEWS README
%attr(755,root,root) %{_libexecdir}/goa-daemon
%dir %{_libdir}/goa-1.0
%dir %{_libdir}/goa-1.0/web-extensions
%attr(755,root,root) %{_libdir}/goa-1.0/web-extensions/libgoawebextension.so
%{_datadir}/dbus-1/services/org.gnome.OnlineAccounts.service
%{_datadir}/glib-2.0/schemas/org.gnome.online-accounts.gschema.xml
%{_iconsdir}/hicolor/scalable/apps/goa-account*.svg
%{_iconsdir}/hicolor/symbolic/apps/goa-account*-symbolic.svg
%{_mandir}/man8/goa-daemon.8*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgoa-1.0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgoa-1.0.so.0
%attr(755,root,root) %{_libdir}/libgoa-backend-1.0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgoa-backend-1.0.so.1
%{_libdir}/girepository-1.0/Goa-1.0.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgoa-1.0.so
%attr(755,root,root) %{_libdir}/libgoa-backend-1.0.so
%dir %{_libdir}/goa-1.0
%{_libdir}/goa-1.0/include
%{_includedir}/goa-1.0
%{_datadir}/gir-1.0/Goa-1.0.gir
%{_pkgconfigdir}/goa-1.0.pc
%{_pkgconfigdir}/goa-backend-1.0.pc

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/goa

%files -n vala-gnome-online-accounts
%defattr(644,root,root,755)
%{_datadir}/vala/vapi/goa-1.0.deps
%{_datadir}/vala/vapi/goa-1.0.vapi
