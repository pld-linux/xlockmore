Summary:	An X terminal locking program.
Name:		xlockmore
Version:	4.15
Release:	1
Copyright:	MIT
Group:		X11/Utilities
Source0:	ftp://ftp.tux.org/pub/tux/bagleyd/xlockmore/xlockmore-%{version}.tar.gz
Source1:	xlock.pamd
Patch:		xlockmore-3.13-fortune.patch
Requires:	pam >= 0.67 /usr/games/fortune
Buildroot:	/tmp/%{name}-%{version}-root

%define		_prefix	/usr/X11R6
%define		_mandir	/usr/X11R6/man

%description
The xlockmore utility is an enhanced version of the standard xlock
program, which allows you to lock an X session so that other users
can't access it.  Xlockmore runs a provided screensaver until you type
in your password.

Install the xlockmore package if you need a locking program to secure
X sessions.

%prep
%setup -q
#%patch -p1

%build
%configure \
	--without-motif \
	--without-gtk \
	--without-nas \
	--disable-setuid \
	--enable-pam
make

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/pam.d

make install \
	prefix=$RPM_BUILD_ROOT%{_prefix} \
	bindir=$RPM_BUILD_ROOT%{_bindir} \
	mandir=$RPM_BUILD_ROOT%{_mandir}/man1 \
	xapploaddir=$RPM_BUILD_ROOT%{_libdir}/X11/app-defaults/

install %{SOURCE1} $RPM_BUILD_ROOT/etc/pam.d/xlock

install -d $RPM_BUILD_ROOT/etc/X11/wmconfig
cat > $RPM_BUILD_ROOT/etc/X11/wmconfig/xlock <<EOF
xlock name "xlock"
xlock description "Screen Saver"
xlock group "Amusements/Screen Savers"
xlock exec "xlock -mode random &"
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%config /etc/pam.d/xlock
%attr(755,root,root) /usr/X11R6/bin/xlock
/usr/X11R6/man/man1/*
%config /usr/X11R6/lib/X11/app-defaults/XLock
%config /etc/X11/wmconfig/xlock
