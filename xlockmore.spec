#
# Conditional build:
%bcond_with	sound	# with sound support
%bcond_without	freetype	# without True Type Font mode(s)
%bcond_without	opengl	# without OpenGL mode(s)
#
Summary:	An X terminal locking program
Summary(de):	Terminal-Sperrprogramm f�r X mit vielen Bildschirmschonern
Summary(es):	Programa para bloquear el terminal X con varios protectores de pantalla
Summary(fr):	Verrouillage de terminaux X
Summary(pl):	Program do blokowania X terminali
Summary(pt_BR):	Programa para bloquear o terminal X com v�rios salvadores de tela
Summary(ru):	��������� ����������� X ��������� � ���������� ���������� ������
Summary(tr):	X terminal kilitleme program�
Summary(uk):	�������� ��������� X ���ͦ���� � ������� ˦��˦��� ���Ҧ��ަ� ������
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
X-Sitzung f�r andere Benutzer sperren k�nnen, wenn Sie sich nicht an
Ihrem Rechner befinden. Es f�hrt einen von vielen Bildschirmschonern
aus und wartet auf die Eingabe eines Pa�worts, bevor es die Sitzung
freigibt und Sie an Ihre X-Programme l��t.

%description -l es
Una versi�n mejorada del xlock que te permite mantener otros usuarios
lejos de tu sesi�n X mientras est�s alejado de la m�quina. Se ejecuta
en uno de los varios protectores de pantalla mientras aguarda que
entres con tu contrase�a, desbloqueando la sesi�n y volviendo al X.

%description -l fr
Version am�lior�e du programme xlock standard et qui permet d'emp�cher
les autres utilisateurs d'aller dans une session X pendant que vous
�tes �loign� de la machine. Il lance l'un des nombreux �conomiseurs
d'�cran et attend que vous tapiez votre mot de passe, d�bloquant la
session et vous redonnant acc�s � vos programmes X.

%description -l pl
xlockmore to rozszerzona wersja standardowego programu xlock,
pozwalaj�cego zablokowa� sesj� X tak, by by�a niedost�pna dla innych
u�ytkownik�w. Xlockmore uruchamia dostarczony wygaszacz ekranu do
czasu wpisania has�a.

%description -l pt_BR
Uma vers�o melhorada do xlock que permite a voc� manter outros
usu�rios longe de sua sess�o X enquanto voc� est� afastado da m�quina.
Ele roda um dos v�rios protetores de tela enquanto aguarda voc� entrar
com a sua senha, desbloqueando a sess�o e voltando ao X.

%description -l ru
���������� ������ ����������� ��������� xlock, ����������� �������
X-������ �� ������ ������������� ����� �� ����� �� ����� ������. ���
��������� ���� �� ��������� �������� � �� �������� ������������� �
���� ���� �� ����� ������ ���������� ������, �� �������� X-������
����� ����������� � ������� ��� � ����� X-����������.

%description -l tr
Standart xlock program�n�n bir miktar geli�tirilmi� s�r�m�. xlockmore
ile makinan�n ba��ndan ayr�lman�z gerekti�i zaman ekran�
kilitleyebilir, b�ylece istenmeyen misafirlerin sistemi
kurcalamalar�n� �nleyebilirsiniz.

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
