Summary:	An X terminal locking program
Summary(de):	Terminal-Sperrprogramm f�r X mit vielen Bildschirmschonern
Summary(fr):	Verrouillage de terminaux X
Summary(tr):	X terminal kilitleme program�
Name:		xlockmore
Version:	4.17.2
Release:	1
Copyright:	MIT
Group:		X11/Amusements
Group(de):	X11/Unterhaltung
Group(pl):	X11/Rozrywka
Source0:	ftp://ftp.tux.org/pub/tux/bagleyd/xlockmore/%{name}-%{version}.tar.gz
Source1:	xlock.pamd
Source2:	%{name}.desktop
Patch0:		%{name}-fortune.patch
Patch1:		%{name}-Mesa.patch
Patch2:		%{name}-X4.patch
Patch3:		%{name}-sounds_path.patch
URL:		http://www.tux.org/~bagleyd/xlockmore.html
BuildRequires:	autoconf
%{?sound:BuildRequires:	esound-devel}
BuildRequires:	freetype-devel
BuildRequires:	libstdc++-devel
BuildRequires:	OpenGL-devel
BuildRequires:	pam-devel
BuildRequires:	XFree86-devel
Requires:	pam >= 0.67
Requires:	/usr/games/fortune
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_prefix		/usr/X11R6
%define		_mandir		%{_prefix}/man

%description
The xlockmore utility is an enhanced version of the standard xlock
program, which allows you to lock an X session so that other users
can't access it. Xlockmore runs a provided screensaver until you type
in your password.

%description -l de
Eine erweiterte Version des Standardprogramms xlock, mit dem Sie eine
X-Sitzung f�r andere Benutzer sperren k�nnen, wenn Sie sich nicht an
Ihrem Rechner befinden. Es f�hrt einen von vielen Bildschirmschonern
aus und wartet auf die Eingabe eines Pa�worts, bevor es die Sitzung
freigibt und Sie an Ihre X-Programme l��t.

%description -l fr
Version am�lior�e du programme xlock standard et qui permet d'emp�cher
les autres utilisateurs d'aller dans une session X pendant que vous
�tes �loign� de la machine. Il lance l'un des nombreux �conomiseurs
d'�cran et attend que vous tapiez votre mot de passe, d�bloquant la
session et vous redonnant acc�s � vos programmes X.

%description -l tr
Standart xlock program�n�n bir miktar geli�tirilmi� s�r�m�. xlockmore
ile makinan�n ba��ndan ayr�lman�z gerekti�i zaman ekran�
kilitleyebilir, b�ylece istenmeyen misafirlerin sistemi
kurcalamalar�n� �nleyebilirsiniz.

%prep
%setup -q
#%patch0 -p1
%patch1 -p0
%patch2 -p1
%patch3 -p1

%build
autoconf
CXXFLAGS="%{!?debug:$RPM_OPT_FLAGS -fno-rtti -fno-exceptions -fno-implicit-templates}%{?debug:-O -g}"
%configure \
	--without-motif \
	--without-gtk \
	--without-nas \
	--disable-setuid \
	%{!?sound:--without-rplay} \
	%{!?sound:--without-esound} \
	%{?sound:--with-esound} \
	--enable-pam
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/pam.d,%{_applnkdir}/Amusements/}
%{?sound:install -d $RPM_BUILD_ROOT%{_datadir}/sounds/%{name}}

%{__make} install \
	prefix=$RPM_BUILD_ROOT%{_prefix} \
	bindir=$RPM_BUILD_ROOT%{_bindir} \
	mandir=$RPM_BUILD_ROOT%{_mandir}/man1 \
	xapploaddir=$RPM_BUILD_ROOT%{_libdir}/X11/app-defaults/

install %{SOURCE1} $RPM_BUILD_ROOT/etc/pam.d/xlock

install %{SOURCE2} $RPM_BUILD_ROOT%{_applnkdir}/Amusements

%{?sound:install sounds/* $RPM_BUILD_ROOT%{_datadir}/sounds/%{name}}

gzip -9nf docs/{TODO,Revisions}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc docs/*gz
%attr(644,root,root) %config %verify(not size mtime md5) /etc/pam.d/xlock
%attr(755,root,root) %{_bindir}/xlock
%{_mandir}/man1/*
%{_libdir}/X11/app-defaults/XLock
%{_applnkdir}/Amusements/xlockmore.desktop
%{?sound:%{_datadir}/sounds/%{name}}
