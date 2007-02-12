Summary:	POP3 server
Summary(pl.UTF-8):   Serwer POP3
Name:		popa3d
Version:	0.6.4.1
Release:	6
License:	distributable (see LICENSE for details)
Group:		Networking/Daemons
Source0:	http://www.openwall.com/popa3d/%{name}-%{version}.tar.gz
# Source0-md5:	5e352b7eebe59f184ce0b0c4c9731c89
Source1:	%{name}.pamd
Source2:	%{name}.inetd
Patch0:		%{name}-params.patch
Patch1:		%{name}-user.patch
URL:		http://www.openwall.com/popa3d/
BuildRequires:	pam-devel
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/sbin/useradd
Requires:	filesystem >= 3.0-11
Requires:	pam >= 0.79.0
Requires:	rc-inetd
Provides:	pop3daemon
Provides:	user(pop3)
Obsoletes:	imap-pop
Obsoletes:	imap-pop3
Obsoletes:	pop3daemon
Obsoletes:	qpopper
Obsoletes:	qpopper6
Conflicts:	courier-imap-pop3
Conflicts:	cyrus-imapd
Conflicts:	solid-pop3d
Conflicts:	solid-pop3d-ssl
Conflicts:	tpop3d
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
popa3d is a Post Office Protocol version 3 (POP3) server written by
Solar Designer. It supports only mailbox spool format.

%description -l pl.UTF-8
popa3d to serwer protokołu Post Office Protocol w wersji 3
(powszechnie znanego jako POP3), napisany przez Solar Designera.
Obsługuje tylko skrzynki w formacie mailbox.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__make} \
	CC="%{__cc}" LD="%{__cc}" \
	CFLAGS="%{rpmcflags} -c" \
	LDFLAGS="%{rpmldflags}" \
	LIBS="-lpam -lcrypt"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{pam.d,sysconfig/rc-inetd,security} \
	$RPM_BUILD_ROOT/var/lib/popa3d-empty

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	SBINDIR="%{_sbindir}" \
	MANDIR="%{_mandir}"

install %{SOURCE1} $RPM_BUILD_ROOT/etc/pam.d/popa3d
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/popa3d

> $RPM_BUILD_ROOT/etc/security/blacklist.popa3d

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%useradd -u 60 -r -d /usr/share/empty -s /bin/false -c "pop3 user" -g nobody pop3

%post
%service -q rc-inetd reload

%postun
if [ "$1" = "0" ]; then
	%service -q rc-inetd reload
	%userremove pop3
fi

%triggerpostun -- popa3d < 0.6.3-2
if [ "$1" != "0" ]; then
	%userremove popa3d
fi

%files
%defattr(644,root,root,755)
%doc DESIGN LICENSE VIRTUAL
%attr(755,root,root) %{_sbindir}/*
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/pam.d/popa3d
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/security/blacklist.popa3d
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/rc-inetd/popa3d
%{_mandir}/man8/*
