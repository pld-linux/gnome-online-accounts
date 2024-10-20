#
# Conditional build:
%bcond_with	fedora		# Kerberos 5 with Fedora realm
%bcond_with	kerberos5	# Kerberos 5 support [TODO: heimdal support; needs MIT currently]

Summary:	Provide online accounts information
Summary(pl.UTF-8):	Dostarczanie informacji o kontach w serwisach sieciowych
Name:		gnome-online-accounts
Version:	3.52.1
Release:	1
License:	LGPL v2+
Group:		Libraries
Source0:	https://download.gnome.org/sources/gnome-online-accounts/3.52/%{name}-%{version}.tar.xz
# Source0-md5:	7565f47b3d630d13921f15df82bd3413
Patch0:		no-gnome-post-install.patch
URL:		https://wiki.gnome.org/Projects/GnomeOnlineAccounts
BuildRequires:	dbus-devel
BuildRequires:	gettext-tools >= 0.19.8
BuildRequires:	gi-docgen
BuildRequires:	glib2-devel >= 1:2.67.4
BuildRequires:	gobject-introspection-devel >= 0.6.2
BuildRequires:	gtk4-devel >= 4.15.2
BuildRequires:	json-glib-devel
BuildRequires:	libadwaita-devel >= 1.6
BuildRequires:	libsecret-devel >= 0.5
BuildRequires:	libsoup3-devel >= 3.0
BuildRequires:	libxml2-devel >= 2
BuildRequires:	libxslt-progs
BuildRequires:	meson >= 0.63.0
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig >= 1:0.16
BuildRequires:	rest1-devel >= 0.9.0
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 2.029
BuildRequires:	tar >= 1:1.22
BuildRequires:	vala
BuildRequires:	xz
%if %{with fedora} || %{with kerberos5}
BuildRequires:	gcr4-devel >= 4.1.0
BuildRequires:	keyutils-devel >= 1.6.2
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
Requires:	glib2 >= 1:2.67.4
Requires:	gtk4 >= 4.15.2
Requires:	libadwaita >= 1.6
Requires:	libsecret >= 0.5
Requires:	libsoup3 >= 3.0
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
Requires:	glib2-devel >= 1:2.67.4
Requires:	gtk4-devel >= 4.15.2
Requires:	libadwaita-devel >= 1.6

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
%patch0 -p1

%build
%meson build \
	-Ddocumentation=true \
	%{?with_fedora:-Dfedora=true} \
	%{!?with_kerberos:-Dkerberos=false} \
	-Dman=true

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

install -d $RPM_BUILD_ROOT%{_gidocdir}
%{__mv} $RPM_BUILD_ROOT%{_docdir}/gnome-online-accounts $RPM_BUILD_ROOT%{_gidocdir}

# not supported by glibc (as of 2.37)
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/ie

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
%doc NEWS README.md
%attr(755,root,root) %{_libexecdir}/goa-daemon
%attr(755,root,root) %{_libexecdir}/goa-oauth2-handler
%if %{with fedora} || %{with kerberos5}
%attr(755,root,root) %{_libexecdir}/goa-identity-service
%endif
%dir %{_libdir}/goa-1.0
%{_datadir}/dbus-1/services/org.gnome.OnlineAccounts.service
%{_datadir}/glib-2.0/schemas/org.gnome.online-accounts.gschema.xml
%{_desktopdir}/org.gnome.OnlineAccounts.OAuth2.desktop
%{_iconsdir}/hicolor/scalable/apps/goa-account*.svg
%{_iconsdir}/hicolor/symbolic/apps/goa-account*-symbolic.svg
%{_mandir}/man8/goa-daemon.8*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgoa-1.0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgoa-1.0.so.0
%attr(755,root,root) %{_libdir}/libgoa-backend-1.0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgoa-backend-1.0.so.2
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
%{_gidocdir}/gnome-online-accounts

%files -n vala-gnome-online-accounts
%defattr(644,root,root,755)
%{_datadir}/vala/vapi/goa-1.0.deps
%{_datadir}/vala/vapi/goa-1.0.vapi
