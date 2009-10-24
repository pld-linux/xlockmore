#
# Conditional build:
%bcond_with	sound	# with sound support
%bcond_without	freetype	# without TrueType Font mode(s)
%bcond_without	opengl	# without OpenGL mode(s)
#
Summary:	An X terminal locking program
Summary(de.UTF-8):	Terminal-Sperrprogramm für X mit vielen Bildschirmschonern
Summary(es.UTF-8):	Programa para bloquear el terminal X con varios protectores de pantalla
Summary(fr.UTF-8):	Verrouillage de terminaux X
Summary(pl.UTF-8):	Program do blokowania X terminali
Summary(pt_BR.UTF-8):	Programa para bloquear o terminal X com vários salvadores de tela
Summary(ru.UTF-8):	Программа локирования X терминала с множеством хранителей экрана
Summary(tr.UTF-8):	X terminal kilitleme programı
Summary(uk.UTF-8):	Програма локування X терміналу з великою кількістю зберігачів екрану
Name:		xlockmore
Version:	5.29.1
Release:	2
License:	MIT
Group:		X11/Amusements
Source0:	http://www.tux.org/~bagleyd/latest/xlockmore-%{version}/%{name}-%{version}.tar.bz2
# Source0-md5:	5492e1dd0eb2c1e2350c777f0e94d112
Source1:	xlock.pamd
Source2:	%{name}.desktop
Patch0:		%{name}-sounds_path.patch
Patch1:		%{name}-vtlock.patch
Patch2:		%{name}-makefile.patch
Patch3:		%{name}-ftgl.patch
URL:		http://www.tux.org/~bagleyd/xlockmore.html
%{?with_opengl:BuildRequires:	OpenGL-devel}
BuildRequires:	autoconf
%{?with_sound:BuildRequires:	esound-devel}
%{?with_freetype:BuildRequires:	freetype-devel}
%{?with_opengl:BuildRequires:	ftgl-devel}
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
BuildRequires:	pam-devel
BuildRequires:	rpm-build >= 4.0.2-79
BuildRequires:	xorg-lib-libSM-devel
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	xorg-lib-libXmu-devel
BuildRequires:	xorg-lib-libXpm-devel
%{?with_opengl:Requires:	OpenGL}
Requires:	pam >= 0.77.3
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define 	_noautoreqdep	libGL.so.1 libGLU.so.1

%define		_soundsdir	/usr/share/sounds
%define		_appdefsdir	%{_datadir}/X11/app-defaults
%define		__cxx		%{__cc}

%description
The xlockmore utility is an enhanced version of the standard xlock
program, which allows you to lock an X session so that other users
can't access it. Xlockmore runs a provided screensaver until you type
in your password.

%description -l de.UTF-8
Eine erweiterte Version des Standardprogramms xlock, mit dem Sie eine
X-Sitzung für andere Benutzer sperren können, wenn Sie sich nicht an
Ihrem Rechner befinden. Es führt einen von vielen Bildschirmschonern
aus und wartet auf die Eingabe eines Paßworts, bevor es die Sitzung
freigibt und Sie an Ihre X-Programme läßt.

%description -l es.UTF-8
Una versión mejorada del xlock que te permite mantener otros usuarios
lejos de tu sesión X mientras estás alejado de la máquina. Se ejecuta
en uno de los varios protectores de pantalla mientras aguarda que
entres con tu contraseña, desbloqueando la sesión y volviendo al X.

%description -l fr.UTF-8
Version améliorée du programme xlock standard et qui permet d'empêcher
les autres utilisateurs d'aller dans une session X pendant que vous
êtes éloigné de la machine. Il lance l'un des nombreux économiseurs
d'écran et attend que vous tapiez votre mot de passe, débloquant la
session et vous redonnant accès à vos programmes X.

%description -l pl.UTF-8
xlockmore to rozszerzona wersja standardowego programu xlock,
pozwalającego zablokować sesję X tak, by była niedostępna dla innych
użytkowników. Xlockmore uruchamia dostarczony wygaszacz ekranu do
czasu wpisania hasła.

%description -l pt_BR.UTF-8
Uma versão melhorada do xlock que permite a você manter outros
usuários longe de sua sessão X enquanto você está afastado da máquina.
Ele roda um dos vários protetores de tela enquanto aguarda você entrar
com a sua senha, desbloqueando a sessão e voltando ao X.

%description -l ru.UTF-8
Улучшенная версия стандартной программы xlock, позволяющей закрыть
X-сессию от других пользователей когда вы вдали от своей машины. Она
запускает один из множества входящих в ее комплект скринсейверов и
ждет пока не будет введен правильный пароль, по которому X-сессия
опять открывается и пускает вас к вашим X-программам.

%description -l tr.UTF-8
Standart xlock programının bir miktar geliştirilmiş sürümü. xlockmore
ile makinanın başından ayrılmanız gerektiği zaman ekranı
kilitleyebilir, böylece istenmeyen misafirlerin sistemi
kurcalamalarını önleyebilirsiniz.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2
%patch3

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
	datadir=$RPM_BUILD_ROOT%{_datadir} \
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
%config(noreplace) %verify(not md5 mtime size) /etc/pam.d/xlock
%attr(755,root,root) %{_bindir}/x*lock
%{_datadir}/xlock
%{_desktopdir}/xlockmore.desktop
%{_mandir}/man1/xlock.1*
%{_appdefsdir}/XLock
%{?with_sound:%{_soundsdir}/%{name}}
