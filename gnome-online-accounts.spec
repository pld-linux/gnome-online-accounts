#
# Conditional build:
%bcond_with	kerberos5	# Kerberos 5 support [TODO: heimdal vs MIT]
#
Summary:	Provide online accounts information
Summary(pl.UTF-8):	Dostarczanie informacji o kontach w serwisach sieciowych
Name:		gnome-online-accounts
Version:	3.6.3
Release:	1
License:	LGPL v2+
Group:		Libraries
Source0:	http://ftp.gnome.org/pub/GNOME/sources/gnome-online-accounts/3.6/%{name}-%{version}.tar.xz
# Source0-md5:	7ab4e7b22a629a32bf794f9c2e52e66d
Patch0:		format-security.patch
URL:		http://www.gnome.org/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake >= 1:1.9
BuildRequires:	gettext-devel >= 0.17
BuildRequires:	glib2-devel >= 1:2.32.0
BuildRequires:	gnome-common
BuildRequires:	gnome-doc-utils >= 0.12.1
BuildRequires:	gobject-introspection-devel >= 0.6.2
BuildRequires:	gtk+3-devel >= 3.5.1
BuildRequires:	gtk-doc >= 1.3
BuildRequires:	gtk-webkit3-devel
BuildRequires:	intltool >= 0.40.1
BuildRequires:	json-glib-devel
BuildRequires:	libgnome-keyring-devel
BuildRequires:	libnotify-devel >= 0.7
BuildRequires:	libsecret-devel
BuildRequires:	libsoup-gnome-devel >= 2.38
BuildRequires:	libtool
BuildRequires:	libxml2-devel >= 2
BuildRequires:	libxslt-progs
BuildRequires:	pkgconfig
BuildRequires:	rest-devel >= 0.7
BuildRequires:	rpmbuild(macros) >= 1.311
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
%if %{with kerberos5}
BuildRequires:	/usr/bin/krb5-config
BuildRequires:	gcr-devel >= 3
%endif
Requires(post,postun):	gtk-update-icon-cache
Requires:	glib2 >= 1:2.32.0
Requires:	gtk+3 >= 3.5.1
Requires:	hicolor-icon-theme
Requires:	libnotify >= 0.7
Requires:	libsoup-gnome >= 2.38
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
gnome-online-accounts provides interfaces so applications and
libraries in GNOME can access the user's online accounts.

%description -l pl.UTF-8
gnome-online-accounts udostępnia interfejsy pozwalające aplikacjom i
bibliotekom GNOME na dostęp do kont użytkownika w serwisach
sieciowych.

%package devel
Summary:	Development files for gnome-online-accounts libraries
Summary(pl.UTF-8):	Pliki programistyczne bibliotek gnome-online-accounts
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.32.0
Requires:	gtk+3-devel >= 3.5.1

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

%description apidocs
GOA API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API GOA.

%prep
%setup -q
%patch0 -p1

%build
%{__gnome_doc_prepare}
%{__gnome_doc_common}
%{__glib_gettextize}
%{__intltoolize}
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-static \
	--disable-silent-rules \
	--enable-gtk-doc \
	%{?with_kerberos5:--enable-kerberos} \
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la

%find_lang gnome-online-accounts

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
%update_icon_cache hicolor

%postun
/sbin/ldconfig
%update_icon_cache hicolor

%files -f gnome-online-accounts.lang
%defattr(644,root,root,755)
%doc NEWS
%attr(755,root,root) %{_libexecdir}/goa-daemon
%attr(755,root,root) %{_libdir}/libgoa-1.0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgoa-1.0.so.0
%attr(755,root,root) %{_libdir}/libgoa-backend-1.0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgoa-backend-1.0.so.0
%{_datadir}/dbus-1/services/org.gnome.OnlineAccounts.service
%{_iconsdir}/hicolor/*/apps/goa-*.png
%{_mandir}/man8/goa-daemon.8*
%{_libdir}/girepository-1.0/Goa-1.0.typelib
%{_datadir}/gnome-online-accounts

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgoa-1.0.so
%attr(755,root,root) %{_libdir}/libgoa-backend-1.0.so
%{_includedir}/goa-1.0
%{_datadir}/gir-1.0/Goa-1.0.gir
%{_pkgconfigdir}/goa-1.0.pc
%{_pkgconfigdir}/goa-backend-1.0.pc

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/goa
