# seems that this is loaded as a plugin, symbols come from libgoa
%define		skip_post_check_so	libgoa-backend-1.0.so.0.0.0
Summary:	Provide online accounts information
Name:		gnome-online-accounts
Version:	3.1.1
Release:	1
License:	LGPL v2+
Group:		Libraries
Source0:	http://ftp.gnome.org/pub/GNOME/sources/gnome-online-accounts/3.1/%{name}-%{version}.tar.bz2
# Source0-md5:	1149d66985b513dd34c32abf9b237b4f
URL:		http://www.gnome.org/
BuildRequires:	autoconf
BuildRequires:	automake >= 1:1.10
BuildRequires:	glib2-devel
BuildRequires:	gobject-introspection-devel
BuildRequires:	gtk-doc
BuildRequires:	gtk+3-devel
BuildRequires:	intltool >= 0.40.1
BuildRequires:	json-glib-devel
BuildRequires:	gettext-devel >= 0.17
BuildRequires:	gnome-doc-utils >= 0.12.1
BuildRequires:	gnome-keyring-devel
BuildRequires:	libnotify-devel
BuildRequires:	rest-devel
BuildRequires:	gtk-webkit3-devel
Requires(post,postun):	gtk-update-icon-cache

%description
gnome-online-accounts provides interfaces so applications and
libraries in GNOME can access the user's online accounts.

%package devel
Summary:	Development files for %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	gobject-introspection-devel
Requires:	pkgconfig

%description devel
The gnome-online-accounts-devel package contains libraries and header
files for developing applications that use gnome-online-accounts.

%package apidocs
Summary:	GOA API documentation
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
GOA API documentation.

%prep
%setup -q

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
	--enable-gtk-doc \
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT
%{__rm} $RPM_BUILD_ROOT/%{_libdir}/*.la

%post
/sbin/ldconfig
%update_icon_cache hicolor

%postun
/sbin/ldconfig
%update_icon_cache hicolor

%files
%defattr(644,root,root,755)
%doc NEWS COPYING
%attr(755,root,root) %{_libexecdir}/goa-daemon
%attr(755,root,root) %{_libdir}/libgoa-1.0.so.0
%attr(755,root,root) %{_libdir}/libgoa-1.0.so.0.0.0
%attr(755,root,root) %{_libdir}/libgoa-backend-1.0.so.0
%attr(755,root,root) %{_libdir}/libgoa-backend-1.0.so.0.0.0
%{_datadir}/dbus-1/services/org.gnome.OnlineAccounts.service
%{_iconsdir}/hicolor/*/apps/goa-*.png
%{_mandir}/man8/goa-daemon.8*
%{_libdir}/girepository-1.0/Goa-1.0.typelib

%files devel
%defattr(644,root,root,755)
%{_includedir}/goa-1.0/
%{_libdir}/libgoa-1.0.so
%{_libdir}/libgoa-backend-1.0.so
%{_datadir}/gir-1.0/Goa-1.0.gir
%{_pkgconfigdir}/goa-1.0.pc
%{_pkgconfigdir}/goa-backend-1.0.pc

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/goa
