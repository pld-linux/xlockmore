#
# Conditional build:
%bcond_with	sound	# with sound support
%bcond_without	freetype	# without True Type Font mode(s)
%bcond_without	opengl	# without OpenGL mode(s)
#
Summary:	An X terminal locking program
Summary(de):	Terminal-Sperrprogramm fЭr X mit vielen Bildschirmschonern
Summary(es):	Programa para bloquear el terminal X con varios protectores de pantalla
Summary(fr):	Verrouillage de terminaux X
Summary(pl):	Program do blokowania X terminali
Summary(pt_BR):	Programa para bloquear o terminal X com vАrios salvadores de tela
Summary(ru):	Программа локирования X терминала с множеством хранителей экрана
Summary(tr):	X terminal kilitleme programЩ
Summary(uk):	Програма локування X терм╕налу з великою к╕льк╕стю збер╕гач╕в екрану
Name:		xlockmore
Version:	5.12
Release:	3
License:	MIT
Group:		X11/Amusements
Source0:	ftp://ftp.tux.org/pub/tux/bagleyd/xlockmore/%{name}-%{version}.tar.bz2
# Source0-md5:	f58758fa3757984edee42e141c7a80dc
Source1:	xlock.pamd
Source2:	%{name}.desktop
Patch0:		%{name}-sounds_path.patch
Patch1:		%{name}-vtlock.patch
URL:		http://www.tux.org/~bagleyd/xlockmore.html
%{?with_opengl:BuildRequires:	OpenGL-devel}
BuildRequires:	XFree86-devel
BuildRequires:	autoconf
%{?with_sound:BuildRequires:	esound-devel}
%{?with_freetype:BuildRequires:	freetype1-devel}
BuildRequires:	gcc-c++
BuildRequires:	libtool
BuildRequires:	pam-devel
BuildRequires:	rpm-build >= 4.0.2-79
%{?_with_opengl:Requires:	OpenGL}
Requires:	pam >= 0.77.3
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define 	_noautoreqdep	libGL.so.1 libGLU.so.1
%define		_prefix		/usr/X11R6
%define		_mandir		%{_prefix}/man
%define		_soundsdir	/usr/share/sounds
%define		_appdefsdir	/usr/X11R6/lib/X11/app-defaults
%define		__cxx		%{__cc}

%description
The xlockmore utility is an enhanced version of the standard xlock
program, which allows you to lock an X session so that other users
can't access it. Xlockmore runs a provided screensaver until you type
in your password.

%description -l de
Eine erweiterte Version des Standardprogramms xlock, mit dem Sie eine
X-Sitzung fЭr andere Benutzer sperren kЖnnen, wenn Sie sich nicht an
Ihrem Rechner befinden. Es fЭhrt einen von vielen Bildschirmschonern
aus und wartet auf die Eingabe eines Paъworts, bevor es die Sitzung
freigibt und Sie an Ihre X-Programme lДъt.

%description -l es
Una versiСn mejorada del xlock que te permite mantener otros usuarios
lejos de tu sesiСn X mientras estАs alejado de la mАquina. Se ejecuta
en uno de los varios protectores de pantalla mientras aguarda que
entres con tu contraseЯa, desbloqueando la sesiСn y volviendo al X.

%description -l fr
Version amИliorИe du programme xlock standard et qui permet d'empЙcher
les autres utilisateurs d'aller dans une session X pendant que vous
Йtes ИloignИ de la machine. Il lance l'un des nombreux Иconomiseurs
d'Иcran et attend que vous tapiez votre mot de passe, dИbloquant la
session et vous redonnant accХs Ю vos programmes X.

%description -l pl
xlockmore to rozszerzona wersja standardowego programu xlock,
pozwalaj╠cego zablokowaФ sesjЙ X tak, by byЁa niedostЙpna dla innych
u©ytkownikСw. Xlockmore uruchamia dostarczony wygaszacz ekranu do
czasu wpisania hasЁa.

%description -l pt_BR
Uma versЦo melhorada do xlock que permite a vocЙ manter outros
usuАrios longe de sua sessЦo X enquanto vocЙ estА afastado da mАquina.
Ele roda um dos vАrios protetores de tela enquanto aguarda vocЙ entrar
com a sua senha, desbloqueando a sessЦo e voltando ao X.

%description -l ru
Улучшенная версия стандартной программы xlock, позволяющей закрыть
X-сессию от других пользователей когда вы вдали от своей машины. Она
запускает один из множества входящих в ее комплект скринсейверов и
ждет пока не будет введен правильный пароль, по которому X-сессия
опять открывается и пускает вас к вашим X-программам.

%description -l tr
Standart xlock programЩnЩn bir miktar geliЧtirilmiЧ sЭrЭmЭ. xlockmore
ile makinanЩn baЧЩndan ayrЩlmanЩz gerektiПi zaman ekranЩ
kilitleyebilir, bЖylece istenmeyen misafirlerin sistemi
kurcalamalarЩnЩ Жnleyebilirsiniz.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
CXXFLAGS="%{rpmcflags} -fno-rtti -fno-exceptions -fno-implicit-templates"
%{__libtoolize}
%{__autoconf}
%configure \
	--without-motif \
	--without-gtk \
	--without-nas \
	--disable-setuid \
	%{!?with_sound:--without-rplay} \
	%{!?with_sound:--without-esound} \
	%{?with_sound:--with-esound} \
	%{!?with_freetype:--without-ttf} \
	%{!?with_opengl:--without-opengl --without-mesa} \
	--enable-vtlock \
	--enable-pam
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/pam.d,%{_desktopdir}} \
	$RPM_BUILD_ROOT{%{_mandir}/man1,%{_appdefsdir}}
%{?with_sound:install -d $RPM_BUILD_ROOT%{_soundsdir}/%{name}}

%{__make} install \
	prefix=$RPM_BUILD_ROOT%{_prefix} \
	bindir=$RPM_BUILD_ROOT%{_bindir} \
	mandir=$RPM_BUILD_ROOT%{_mandir}/man1 \
	xapploaddir=$RPM_BUILD_ROOT%{_appdefsdir} \
	INSTPGMFLAGS="-m 755"

install %{SOURCE1} $RPM_BUILD_ROOT/etc/pam.d/xlock

install %{SOURCE2} $RPM_BUILD_ROOT%{_desktopdir}

%{?with_sound:install sounds/* $RPM_BUILD_ROOT%{_soundsdir}/%{name}}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README docs/TODO docs/Revisions
%attr(644,root,root) %config(noreplace) %verify(not size mtime md5) /etc/pam.d/xlock
%attr(755,root,root) %{_bindir}/xlock
%{_mandir}/man1/*
%{_appdefsdir}/XLock
%{_desktopdir}/xlockmore.desktop
%{?with_sound:%{_soundsdir}/%{name}}
