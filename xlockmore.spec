#
# Conditional build:
# _with_sound
#
Summary:	An X terminal locking program
Summary(de):	Terminal-Sperrprogramm für X mit vielen Bildschirmschonern
Summary(fr):	Verrouillage de terminaux X
Summary(pl):	Program do blokowania X terminali
Summary(tr):	X terminal kilitleme programý
Name:		xlockmore
Version:	5.00
Release:	6
License:	MIT
Group:		X11/Amusements
Source0:	ftp://ftp.tux.org/pub/tux/bagleyd/xlockmore/%{name}-%{version}.tar.gz
Source1:	xlock.pamd
Source2:	%{name}.desktop
Patch0:		%{name}-Mesa.patch
Patch1:		%{name}-sounds_path.patch
Patch2:		%{name}-vtlock.patch
URL:		http://www.tux.org/~bagleyd/xlockmore.html
BuildRequires:	OpenGL-devel
BuildRequires:	XFree86-devel
BuildRequires:	autoconf
%{?_with_sound:BuildRequires:	esound-devel}
#BuildRequires:	freetype1-devel
BuildRequires:	libstdc++-devel
BuildRequires:	pam-devel
BuildRequires:	rpm-build >= 4.0.2-79
Requires:	pam >= 0.67
Requires:	fortune-mod
Requires:	OpenGL
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define 	_noautoreqdep	libGL.so.1 libGLU.so.1
%define		_prefix		/usr/X11R6
%define		_mandir		%{_prefix}/man

%description
The xlockmore utility is an enhanced version of the standard xlock
program, which allows you to lock an X session so that other users
can't access it. Xlockmore runs a provided screensaver until you type
in your password.

%description -l de
Eine erweiterte Version des Standardprogramms xlock, mit dem Sie eine
X-Sitzung für andere Benutzer sperren können, wenn Sie sich nicht an
Ihrem Rechner befinden. Es führt einen von vielen Bildschirmschonern
aus und wartet auf die Eingabe eines Paßworts, bevor es die Sitzung
freigibt und Sie an Ihre X-Programme läßt.

%description -l fr
Version améliorée du programme xlock standard et qui permet d'empêcher
les autres utilisateurs d'aller dans une session X pendant que vous
êtes éloigné de la machine. Il lance l'un des nombreux économiseurs
d'écran et attend que vous tapiez votre mot de passe, débloquant la
session et vous redonnant accès à vos programmes X.

%description -l pl
xlockmore to rozszerzona wersja standardowego programu xlock,
pozwalaj±cego zablokowaæ sesjê X tak, by by³a niedostêpna dla innych
u¿ytkowników. Xlockmore uruchamia dostarczony wygaszacz ekranu do
czasu wpisania has³a.

%description -l tr
Standart xlock programýnýn bir miktar geliþtirilmiþ sürümü. xlockmore
ile makinanýn baþýndan ayrýlmanýz gerektiði zaman ekraný
kilitleyebilir, böylece istenmeyen misafirlerin sistemi
kurcalamalarýný önleyebilirsiniz.

%prep
%setup -q
%patch0 -p0
%patch1 -p1
%patch2 -p1

%build
CXXFLAGS="%{rpmcflags} -fno-rtti -fno-exceptions -fno-implicit-templates"
%configure2_13 \
	--without-motif \
	--without-gtk \
	--without-nas \
	--disable-setuid \
	%{!?_with_sound:--without-rplay} \
	%{!?_with_sound:--without-esound} \
	%{?_with_sound:--with-esound} \
	--enable-vtlock \
	--enable-pam
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/pam.d,%{_applnkdir}/Amusements/} \
	   $RPM_BUILD_ROOT{%{_mandir}/man1,%{_libdir}/X11/app-defaults/}
%{?_with_sound:install -d $RPM_BUILD_ROOT%{_datadir}/sounds/%{name}}

%{__make} install \
	prefix=$RPM_BUILD_ROOT%{_prefix} \
	bindir=$RPM_BUILD_ROOT%{_bindir} \
	mandir=$RPM_BUILD_ROOT%{_mandir}/man1 \
	xapploaddir=$RPM_BUILD_ROOT%{_libdir}/X11/app-defaults/

install %{SOURCE1} $RPM_BUILD_ROOT/etc/pam.d/xlock

install %{SOURCE2} $RPM_BUILD_ROOT%{_applnkdir}/Amusements/

%{?_with_sound:install sounds/* $RPM_BUILD_ROOT%{_datadir}/sounds/%{name}}

install xlock/xlock.man $RPM_BUILD_ROOT%{_mandir}/man1/
install xlock/XLock.ad $RPM_BUILD_ROOT%{_libdir}/X11/app-defaults/XLock

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README docs/TODO docs/Revisions
%attr(644,root,root) %config(noreplace) %verify(not size mtime md5) /etc/pam.d/xlock
%attr(755,root,root) %{_bindir}/xlock
%{_mandir}/man1/*
%{_libdir}/X11/app-defaults/XLock
%{_applnkdir}/Amusements/xlockmore.desktop
%{?_with_sound:%{_datadir}/sounds/%{name}}
