Summary:	POP3 server
Summary(pl):	Serwer POP3
Name:		popa3d
Version:	0.6.4
Release:	1
License:	distributable (see LICENSE for details)
Group:		Networking/Daemons
Source0:	http://www.openwall.com/popa3d/%{name}-%{version}.tar.gz
# Source0-md5:	21d4876c4d85b92d323e46d2e8f12e11
Source1:	%{name}.pamd
Source2:	%{name}.inetd
Patch0:		%{name}-params.patch
Patch1:		%{name}-user.patch
URL:		http://www.openwall.com/popa3d/
BuildRequires:	pam-devel
BuildRequires:	rpmbuild(macros) >= 1.159
PreReq:		rc-inetd
Requires(pre):	/bin/id
Requires(pre):	/usr/sbin/useradd
Requires(postun):	/usr/sbin/userdel
Requires:	FHS >= 2.1-24
Requires:	pam >= 0.77.3
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

%description -l pl
popa3d to serwer protoko³u Post Office Protocol w wersji 3
(powszechnie znanego jako POP3), napisany przez Solar Designera.
Obs³uguje tylko skrzynki w formacie mailbox.

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
if [ -n "`id -u pop3 2>/dev/null`" ]; then
	if [ "`id -u pop3`" != "60" ]; then
		echo "Error: user pop3 doesn't have uid=60. Correct this before installing pop3." 1>&2
		exit 1
	fi
else
	/usr/sbin/useradd -u 60 -r -d /dev/null -s /bin/false -c "pop3 user" -g nobody pop3 1>&2
fi

%post
if [ -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd reload 1>&2
else
	echo "Type \"/etc/rc.d/init.d/rc-inetd start\" to start inet server" 1>&2
fi

%postun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/rc-inetd ]; then
		/etc/rc.d/init.d/rc-inetd reload 1>&2
	fi
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
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/pam.d/popa3d
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/security/blacklist.popa3d
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/sysconfig/rc-inetd/popa3d
%{_mandir}/man8/*
