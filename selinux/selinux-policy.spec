%define distro redhat
%define polyinstatiate n
%define monolithic n
%if %{?BUILD_TARGETED:0}%{!?BUILD_TARGETED:1}
%define BUILD_TARGETED 1
%endif
%if %{?BUILD_MINIMUM:0}%{!?BUILD_MINIMUM:1}
%define BUILD_MINIMUM 0
%endif
%if %{?BUILD_OLPC:0}%{!?BUILD_OLPC:1}
%define BUILD_OLPC 0
%endif
%if %{?BUILD_MLS:0}%{!?BUILD_MLS:1}
%define BUILD_MLS 0 
%endif
%define POLICYVER 24
%define libsepolver 2.0.41-1
%define POLICYCOREUTILSVER 2.0.78-1
%define CHECKPOLICYVER 2.0.21-1
Summary: SELinux policy configuration
Name: selinux-policy
Version: 3.7.19
Release: 279%{?dist}.4
License: GPLv2+
Group: System Environment/Base
Source: serefpolicy-%{version}.tgz
patch: policy-F13.patch
patch1: policy-RHEL6_4.patch
patch2: policy-RHEL6.5.patch
patch3: policy-RHEL6.6.patch
patch4: policy-RHEL6.6-20140414.patch
patch5: policy-RHEL6.7-e2506.patch
patch6: policy-RHEL6.7.z-58ad9.patch
Source1: modules-targeted.conf
Source2: booleans-targeted.conf
Source3: Makefile.devel
Source4: setrans-targeted.conf
Source5: modules-mls.conf
Source6: booleans-mls.conf
Source8: setrans-mls.conf
Source9: modules-olpc.conf
Source10: booleans-olpc.conf
Source11: setrans-olpc.conf
Source12: securetty_types-olpc
Source13: policygentool
Source14: securetty_types-targeted
Source15: securetty_types-mls
Source16: modules-minimum.conf
Source17: booleans-minimum.conf
Source18: setrans-minimum.conf
Source19: securetty_types-minimum
Source20: customizable_types
Source21: config.tgz
Source22: users-mls
Source23: users-targeted
Source24: users-olpc
Source25: users-minimum
Source26: mypolicy.tar.bz2

Url: http://oss.tresys.com/repos/refpolicy/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
BuildRequires: python gawk checkpolicy >= %{CHECKPOLICYVER} m4 policycoreutils-python >= %{POLICYCOREUTILSVER} bzip2 
Requires(pre): policycoreutils >= %{POLICYCOREUTILSVER} libsemanage >= 2.0.14-3
Requires(post): /usr/bin/bunzip2 /bin/mktemp /bin/awk
Requires: checkpolicy >= %{CHECKPOLICYVER} m4 
Obsoletes: selinux-policy-devel <= %{version}-%{release}
Provides: selinux-policy-devel = %{version}-%{release}

%description 
SELinux Base package

%files 
%defattr(-,root,root,-)
#%{_mandir}/man*/*
# policycoreutils owns these manpage directories, we only own the files within them
#%{_mandir}/ru/*/*
%dir %{_usr}/share/selinux
%dir %{_usr}/share/selinux/devel
%dir %{_usr}/share/selinux/devel/include
%dir %{_usr}/share/selinux/packages
%dir %{_sysconfdir}/selinux
%ghost %config(noreplace) %{_sysconfdir}/selinux/config
%ghost %{_sysconfdir}/sysconfig/selinux
%{_usr}/share/selinux/devel/include/*
%{_usr}/share/selinux/devel/Makefile
%{_usr}/share/selinux/devel/policygentool
%{_usr}/share/selinux/devel/example.*
%{_usr}/share/selinux/devel/policy.*

%package doc
Summary: SELinux policy documentation
Group: System Environment/Base
Requires(pre): selinux-policy = %{version}-%{release}
Requires: /usr/bin/xdg-open

%description doc
SELinux policy documentation package

%files doc
%defattr(-,root,root,-)
%doc %{_usr}/share/doc/%{name}-%{version}
%attr(755,root,root) %{_usr}/share/selinux/devel/policyhelp
%{_mandir}/man*/*
%{_mandir}/ru/*/*

%check
if /usr/sbin/selinuxenabled; then
/usr/bin/sepolgen-ifgen -i %{buildroot}%{_usr}/share/selinux/devel/include -o /dev/null 
fi

%define makeCmds() \
make UNK_PERMS=%5 NAME=%1 TYPE=%2 DISTRO=%{distro} UBAC=n DIRECT_INITRC=%3 MONOLITHIC=%{monolithic} POLY=%4 MLS_CATS=1024 MCS_CATS=1024 bare \
make UNK_PERMS=%5 NAME=%1 TYPE=%2 DISTRO=%{distro} UBAC=n DIRECT_INITRC=%3 MONOLITHIC=%{monolithic} POLY=%4 MLS_CATS=1024 MCS_CATS=1024  conf \
cp -f selinux_config/modules-%1.conf  ./policy/modules.conf \
cp -f selinux_config/booleans-%1.conf ./policy/booleans.conf \
cp -f selinux_config/users-%1 ./policy/users \

%define installCmds() \
make UNK_PERMS=%5 NAME=%1 TYPE=%2 DISTRO=%{distro} UBAC=n DIRECT_INITRC=%3 MONOLITHIC=%{monolithic} POLY=%4 MLS_CATS=1024 MCS_CATS=1024 base.pp \
make validate UNK_PERMS=%5 NAME=%1 TYPE=%2 DISTRO=%{distro} UBAC=n DIRECT_INITRC=%3 MONOLITHIC=%{monolithic} POLY=%4 MLS_CATS=1024 MCS_CATS=1024 modules \
make UNK_PERMS=%5 NAME=%1 TYPE=%2 DISTRO=%{distro} UBAC=n DIRECT_INITRC=%3 MONOLITHIC=%{monolithic} DESTDIR=%{buildroot} POLY=%4 MLS_CATS=1024 MCS_CATS=1024 install \
make UNK_PERMS=%5 NAME=%1 TYPE=%2 DISTRO=%{distro} UBAC=n DIRECT_INITRC=%3 MONOLITHIC=%{monolithic} DESTDIR=%{buildroot} POLY=%4 MLS_CATS=1024 MCS_CATS=1024 install-appconfig \
#%{__cp} *.pp %{buildroot}/%{_usr}/share/selinux/%1/ \
%{__mkdir} -p %{buildroot}/%{_sysconfdir}/selinux/%1/logins \
%{__mkdir} -p %{buildroot}/%{_sysconfdir}/selinux/%1/policy \
%{__mkdir} -p %{buildroot}/%{_sysconfdir}/selinux/%1/modules/active \
%{__mkdir} -p %{buildroot}/%{_sysconfdir}/selinux/%1/contexts/files \
touch %{buildroot}/%{_sysconfdir}/selinux/%1/modules/semanage.read.LOCK \
touch %{buildroot}/%{_sysconfdir}/selinux/%1/modules/semanage.trans.LOCK \
rm -rf %{buildroot}%{_sysconfdir}/selinux/%1/booleans \
touch %{buildroot}%{_sysconfdir}/selinux/%1/seusers \
touch %{buildroot}%{_sysconfdir}/selinux/%1/policy/policy.%{POLICYVER} \
touch %{buildroot}%{_sysconfdir}/selinux/%1/contexts/files/file_contexts \
touch %{buildroot}%{_sysconfdir}/selinux/%1/contexts/files/file_contexts.homedirs \
install -m0644 selinux_config/securetty_types-%1 %{buildroot}%{_sysconfdir}/selinux/%1/contexts/securetty_types \
install -m0644 selinux_config/setrans-%1.conf %{buildroot}%{_sysconfdir}/selinux/%1/setrans.conf \
install -m0644 selinux_config/customizable_types %{buildroot}%{_sysconfdir}/selinux/%1/contexts/customizable_types \
bzip2 %{buildroot}/%{_usr}/share/selinux/%1/*.pp \
awk '$1 !~ "/^#/" && $2 == "=" && $3 == "module" { printf "%%s.pp.bz2 ", $1 }' ./policy/modules.conf > %{buildroot}/%{_usr}/share/selinux/%1/modules.lst
%nil

%define fileList() \
%defattr(-,root,root) \
%dir %{_usr}/share/selinux/%1 \
%{_usr}/share/selinux/%1/*.pp.bz2 \
%{_usr}/share/selinux/%1/modules.lst \
%dir %{_sysconfdir}/selinux/%1 \
%config(noreplace) %{_sysconfdir}/selinux/%1/setrans.conf \
%ghost %{_sysconfdir}/selinux/%1/seusers \
%dir %{_sysconfdir}/selinux/%1/logins \
%dir %{_sysconfdir}/selinux/%1/modules \
%verify(not mtime) %{_sysconfdir}/selinux/%1/modules/semanage.read.LOCK \
%verify(not mtime) %{_sysconfdir}/selinux/%1/modules/semanage.trans.LOCK \
%attr(700,root,root) %dir %{_sysconfdir}/selinux/%1/modules/active \
#%verify(not md5 size mtime) %attr(600,root,root) %config(noreplace) %{_sysconfdir}/selinux/%1/modules/active/seusers \
%dir %{_sysconfdir}/selinux/%1/policy/ \
%ghost %{_sysconfdir}/selinux/%1/policy/policy.* \
%dir %{_sysconfdir}/selinux/%1/contexts \
%config %{_sysconfdir}/selinux/%1/contexts/customizable_types \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/securetty_types \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/dbus_contexts \
%config %{_sysconfdir}/selinux/%1/contexts/x_contexts \
%config %{_sysconfdir}/selinux/%1/contexts/default_contexts \
%config %{_sysconfdir}/selinux/%1/contexts/virtual_domain_context \
%config %{_sysconfdir}/selinux/%1/contexts/virtual_image_context \
%config %{_sysconfdir}/selinux/%1/contexts/sepgsql_contexts \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/default_type \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/failsafe_context \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/initrc_context \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/removable_context \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/userhelper_context \
%dir %{_sysconfdir}/selinux/%1/contexts/files \
%ghost %{_sysconfdir}/selinux/%1/contexts/files/file_contexts \
%ghost %{_sysconfdir}/selinux/%1/contexts/files/file_contexts.homedirs \
%config %{_sysconfdir}/selinux/%1/contexts/files/media \
%dir %{_sysconfdir}/selinux/%1/contexts/users \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/users/root \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/users/guest_u \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/users/xguest_u \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/users/user_u \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/users/staff_u 

%define saveFileContext() \
if [ -s /etc/selinux/config ]; then \
     . %{_sysconfdir}/selinux/config; \
     FILE_CONTEXT=%{_sysconfdir}/selinux/%1/contexts/files/file_contexts; \
     if [ "${SELINUXTYPE}" = %1 -a -f ${FILE_CONTEXT} ]; then \
        [ -f ${FILE_CONTEXT}.pre ] || cp -f ${FILE_CONTEXT} ${FILE_CONTEXT}.pre; \
     fi \
fi

%define loadpolicy() \
. %{_sysconfdir}/selinux/config; \
( cd /usr/share/selinux/%1; \
semodule -n -r oracle-port -b base.pp.bz2 -i %2 -s %1 2>&1 | grep -v "oracle-port"; \
[ "${SELINUXTYPE}" == "%1" ] && selinuxenabled && load_policy; \
); \

%define relabel() \
. %{_sysconfdir}/selinux/config; \
FILE_CONTEXT=%{_sysconfdir}/selinux/%1/contexts/files/file_contexts; \
selinuxenabled; \
if [ $? = 0  -a "${SELINUXTYPE}" = %1 -a -f ${FILE_CONTEXT}.pre ]; then \
     fixfiles -C ${FILE_CONTEXT}.pre restore 2> /dev/null; \
     restorecon -R /root /var/log /var/run 2> /dev/null; \
     rm -f ${FILE_CONTEXT}.pre; \
fi; 

%description
SELinux Reference Policy - modular.
Based off of reference policy: Checked out revision  2.20091117

%build

%prep 
%setup -n serefpolicy-%{version} -q
cd $RPM_BUILD_DIR/serefpolicy-%{version};tar -xjf %{SOURCE26}
exec 1>/dev/null 2>&1
%patch -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%install
mkdir selinux_config
for i in %{SOURCE1} %{SOURCE2} %{SOURCE3} %{SOURCE4} %{SOURCE5} %{SOURCE6} %{SOURCE8} %{SOURCE9} %{SOURCE10} %{SOURCE11} %{SOURCE12} %{SOURCE13} %{SOURCE14} %{SOURCE15} %{SOURCE16} %{SOURCE17} %{SOURCE18} %{SOURCE19} %{SOURCE20} %{SOURCE21} %{SOURCE22} %{SOURCE23} %{SOURCE24} %{SOURCE25};do
 cp $i selinux_config
done
tar zxvf selinux_config/config.tgz
# Build targeted policy
%{__rm} -fR %{buildroot}
mkdir -p %{buildroot}%{_mandir}
cp -R  man/* %{buildroot}%{_mandir}
mkdir -p %{buildroot}%{_sysconfdir}/selinux
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
touch %{buildroot}%{_sysconfdir}/selinux/config
touch %{buildroot}%{_sysconfdir}/sysconfig/selinux

# Always create policy module package directories
mkdir -p %{buildroot}%{_usr}/share/selinux/{targeted,mls,minimum,modules}/

# Install devel
make clean
%if %{BUILD_TARGETED}
# Build targeted policy
# Commented out because only targeted ref policy currently builds
%makeCmds targeted mcs n y allow
%installCmds targeted mcs n y allow
%endif

%if %{BUILD_MINIMUM}
# Build minimum policy
# Commented out because only minimum ref policy currently builds
%makeCmds minimum mcs n y allow
%installCmds minimum mcs n y allow
%endif

%if %{BUILD_MLS}
# Build mls policy
%makeCmds mls mls n y deny
%installCmds mls mls n y deny
%endif

%if %{BUILD_OLPC}
# Build olpc policy
# Commented out because only olpc ref policy currently builds
%makeCmds olpc mcs n y allow
%installCmds olpc mcs n y allow
%endif

make UNK_PERMS=allow NAME=targeted TYPE=mcs DISTRO=%{distro} UBAC=n DIRECT_INITRC=n MONOLITHIC=%{monolithic} DESTDIR=%{buildroot} PKGNAME=%{name}-%{version} POLY=y MLS_CATS=1024 MCS_CATS=1024 install-headers install-docs
mkdir %{buildroot}%{_usr}/share/selinux/devel/
mkdir %{buildroot}%{_usr}/share/selinux/packages/
mv %{buildroot}%{_usr}/share/selinux/targeted/include %{buildroot}%{_usr}/share/selinux/devel/include
install -m 755 selinux_config/policygentool %{buildroot}%{_usr}/share/selinux/devel/
install -m 644 selinux_config/Makefile.devel %{buildroot}%{_usr}/share/selinux/devel/Makefile
install -m 644 doc/example.* %{buildroot}%{_usr}/share/selinux/devel/
install -m 644 doc/policy.* %{buildroot}%{_usr}/share/selinux/devel/
echo  "xdg-open file:///usr/share/doc/selinux-policy-%{version}/html/index.html"> %{buildroot}%{_usr}/share/selinux/devel/policyhelp
chmod +x %{buildroot}%{_usr}/share/selinux/devel/policyhelp
rm -rf selinux_config
%clean
%{__rm} -fR %{buildroot}

%post
if [ ! -s /etc/selinux/config ]; then
#
#     New install so we will default to targeted policy
#
echo "
# This file controls the state of SELinux on the system.
# SELINUX= can take one of these three values:
#     enforcing - SELinux security policy is enforced.
#     permissive - SELinux prints warnings instead of enforcing.
#     disabled - No SELinux policy is loaded.
SELINUX=enforcing
# SELINUXTYPE= can take one of these two values:
#     targeted - Targeted processes are protected,
#     mls - Multi Level Security protection.
SELINUXTYPE=targeted 

" > /etc/selinux/config

     ln -sf ../selinux/config /etc/sysconfig/selinux 
     restorecon /etc/selinux/config 2> /dev/null || :
else
     . /etc/selinux/config
     # if first time update booleans.local needs to be copied to sandbox
     [ -f /etc/selinux/${SELINUXTYPE}/booleans.local ] && mv /etc/selinux/${SELINUXTYPE}/booleans.local /etc/selinux/targeted/modules/active/
     [ -f /etc/selinux/${SELINUXTYPE}/seusers ] && cp -f /etc/selinux/${SELINUXTYPE}/seusers /etc/selinux/${SELINUXTYPE}/modules/active/seusers
fi
exit 0

%postun
if [ $1 = 0 ]; then
     setenforce 0 2> /dev/null
     if [ ! -s /etc/selinux/config ]; then
          echo "SELINUX=disabled" > /etc/selinux/config
     else
          sed -i 's/^SELINUX=.*/SELINUX=disabled/g' /etc/selinux/config
     fi
fi
exit 0

%if %{BUILD_TARGETED}
%package targeted
Summary: SELinux targeted base policy
Provides: selinux-policy-base = %{version}-%{release}
Group: System Environment/Base
Obsoletes: selinux-policy-targeted-sources < 2
Requires(pre): policycoreutils >= %{POLICYCOREUTILSVER}
Requires(pre): coreutils
Requires(pre): selinux-policy = %{version}-%{release}
Requires: selinux-policy = %{version}-%{release}
Conflicts:  audispd-plugins <= 1.7.7-1
Obsoletes: mod_fcgid-selinux <= %{version}-%{release}
Obsoletes: cachefilesd-selinux <= 0.10-1
Conflicts:  seedit

%description targeted
SELinux Reference policy targeted base module.

%pre targeted
%saveFileContext targeted

%post targeted
packages=`cat /usr/share/selinux/targeted/modules.lst`
if [ $1 -eq 1 ]; then
   %loadpolicy targeted $packages
   restorecon -R /root /var/log /var/run 2> /dev/null
else
   semodule -n -s targeted -r moilscanner -r mailscanner -r gamin -r audio_entropy -r iscsid -r polkit_auth -r polkit -r rtkit_daemon -r ModemManager -r telepathysofiasip -r passanger -r rgmanager -r aisexec -r corosync -r pacemaker -r amavis -r clamav -r glusterfs 2>/dev/null
   %loadpolicy targeted $packages
   %relabel targeted
fi
exit 0

%triggerpostun targeted -- selinux-policy-targeted < 3.2.5-9.fc9
. /etc/selinux/config
[ "${SELINUXTYPE}" != "targeted" ] && exit 0
setsebool -P use_nfs_home_dirs=1
semanage user -l | grep -s unconfined_u > /dev/null
if [ $? -eq 0 ]; then
   semanage user -m -R "unconfined_r system_r" -r s0-s0:c0.c1023 unconfined_u
else
   semanage user -a -P user -R "unconfined_r system_r" -r s0-s0:c0.c1023 unconfined_u
fi
seuser=`semanage login -l | grep __default__ | awk '{ print $2 }'`
[ "$seuser" != "unconfined_u" ]  && semanage login -m -s "unconfined_u"  -r s0-s0:c0.c1023 __default__
seuser=`semanage login -l | grep root | awk '{ print $2 }'`
[ "$seuser" = "system_u" ] && semanage login -m -s "unconfined_u"  -r s0-s0:c0.c1023 root
restorecon -R /root /etc/selinux/targeted 2> /dev/null
semodule -r qmail 2> /dev/null
exit 0

%files targeted
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/selinux/targeted/contexts/users/unconfined_u
%fileList targeted
%endif

%if %{BUILD_MINIMUM}
%package minimum
Summary: SELinux minimum base policy
Provides: selinux-policy-base = %{version}-%{release}
Group: System Environment/Base
Requires(post): policycoreutils-python >= %{POLICYCOREUTILSVER}
Requires(pre): coreutils
Requires(pre): selinux-policy = %{version}-%{release}
Requires: selinux-policy = %{version}-%{release}
Conflicts:  seedit

%description minimum
SELinux Reference policy minimum base module.

%pre minimum
%saveFileContext minimum

%post minimum
packages="execmem.pp.bz2 unconfined.pp.bz2 unconfineduser.pp.bz2"
%loadpolicy minimum $packages
if [ $1 -eq 1 ]; then
#semanage -S minimum -i - << __eof
#login -m  -s unconfined_u -r s0-s0:c0.c1023 __default__
#login -m  -s unconfined_u -r s0-s0:c0.c1023 root
#__eof
echo "# This file is auto-generated by libsemanage
# Do not edit directly.
system_u:system_u:s0-s0:c0.c1023
root:unconfined_u:s0-s0:c0.c1023
__default__:unconfined_u:s0-s0:c0.c1023
" > /etc/selinux/minimum/seusers
[ -f /etc/selinux/minimum/seusers ] && cp -f /etc/selinux/minimum/seusers /etc/selinux/minimum/modules/active/seusers.final
restorecon -R /root /var/log /var/run 2> /dev/null
else
%relabel minimum
fi
exit 0

%files minimum
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/selinux/minimum/contexts/users/unconfined_u
%fileList minimum
%endif

%if %{BUILD_OLPC}
%package olpc 
Summary: SELinux olpc base policy
Group: System Environment/Base
Provides: selinux-policy-base = %{version}-%{release}
Requires(pre): policycoreutils >= %{POLICYCOREUTILSVER}
Requires(pre): coreutils
Requires(pre): selinux-policy = %{version}-%{release}
Requires: selinux-policy = %{version}-%{release}
Conflicts:  seedit

%description olpc 
SELinux Reference policy olpc base module.

%pre olpc 
%saveFileContext olpc

%post olpc 
packages=`cat /usr/share/selinux/olpc/modules.lst`
%loadpolicy olpc $packages

if [ $1 -ne 1 ]; then
%relabel olpc
fi
exit 0

%files olpc
%defattr(-,root,root,-)
%fileList olpc

%endif

%if %{BUILD_MLS}
%package mls 
Summary: SELinux mls base policy
Group: System Environment/Base
Provides: selinux-policy-base = %{version}-%{release}
Obsoletes: selinux-policy-mls-sources < 2
Requires: policycoreutils-newrole >= %{POLICYCOREUTILSVER} setransd
Requires(pre): policycoreutils >= %{POLICYCOREUTILSVER}
Requires(pre): coreutils
Requires(pre): selinux-policy = %{version}-%{release}
Requires: selinux-policy = %{version}-%{release}
Conflicts:  seedit

%description mls 
SELinux Reference policy mls base module.

%pre mls 
%saveFileContext mls

%post mls 
semodule -n -s mls -r mailscanner -r polkit -r ModemManager -r telepathysofiasip  -r rgmanager -r aisexec -r corosync -r pacemaker -r amavis -r clamav 2>/dev/null
packages=`cat /usr/share/selinux/mls/modules.lst`
%loadpolicy mls $packages

if [ $1 -eq 1 ]; then
   restorecon -R /root /var/log /var/run 2> /dev/null
else
%relabel mls
fi
exit 0

%files mls
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/selinux/mls/contexts/users/unconfined_u
%fileList mls

%endif

%changelog
* Mon Aug 4 2015 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-279.el6_7.4
- Allow nsswitch domain to search samba pid dirs to allow to connect to nmbd_t
Resolves:#1248520

* Mon Aug 3 2015 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-279.el6_7.3
- Add default labeling for /var/run/samba/nmbd
Resolves:#1248520

* Thu Jul 30 2015 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-279.el6_7.2
- Allow nmbd to create pids files/dirs under /var/run/samba with correct labeling.
Resolves:#1248520

* Thu Jul 30 2015 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-279.el6_7.1
- Backport gluster fixes from RHEL7
 - execute showmount in own domain
Resolves:#1248520
 - execute nsfd in own domain
 - allow gluster to connect to all ports
 - Add support for /usr/sbin/ctdbd_wrapper.
 - nrpe needs kill capability to make gluster moniterd nodes working.

* Tue Jun 23 2015 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-278
- Allow logrotate get attributes of all unallocated tty device nodes.
- Add logging_syslogd_run_nagios_plugins boolean for rsyslog to allow transition to nagios unconfined plugins.
- Allow glusterd to connect to init.
Resolves:#1230371
- Allow gluster do dbus chat with domain running as initrc_t.

* Wed Jun 17 2015 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-277
- Allow glusterd to interact with gluster tools running in a user domain
Resolves:#1229605

* Wed Jun 17 2015 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-276
- Allow gluster to manage own log files.
- S30samba-start gluster hooks wants to search audit logs. Dontaudit it.
- Label gluster python hooks also as bin_t.
- Allow samba_t net_admin capability to make CIFS mount working.
Resolves:#1229605
- Allow ssh_keygen_t to manage keys located in /var/lib/gluster.

* Fri Jun 12 2015 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-275
- Allow glusterd to have transition to insmod.
- Allow glusterd to use geo-replication gluster tool.
- Remove gluster from permissive domains.
Resolves:#1229605

* Mon Jun 8 2015 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-275
 - Allow glusterd to have mknod capability. It creates a special file using mknod in a brick.
 - Update rules related to glusterd_brick_t.
 - Allow glusterd to execute lvm tools in the lvm_t target domain.
 - Allow glusterd to execute xfs_growfs in the target domain.
 - Add support for /usr/sbin/xfs_growfs.
 - Allow glusterd to create samba config files if it is started by service script and running with unconfined_u.
Resolves:#1228109
- Fix description for ftpd_use_passive_mode boolean.

* Sat Jun 6 2015 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-274
- Don't ship pam_selinux to avoin a conflict with pam package
Resolves:#1220691

* Thu Jun 4 2015 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-273
- Fix redis_stream_connect interface.
Resolves:#1220691
- Allow kadmind to bind to kprop port.
- Add new man pages for bacula

* Wed Jun 3 2015 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-272
- Allow hypervkvp to read default SELinux contexts.
- Allow hypervkvp to write to /etc directories.
- Update all man pages for RHEL6.7 SELinux domains/roles using the latest sepolicy-manpage from RHEL7.
- Fix labeling for /var/lib/graphite-web
- ALlow kpropd to connect to tcp/754 port.
Resolves:#1220691
- Allow php-fpm write access to /var/run/redis/redis.sock
- Update fs_rw_inherited_nfs_files() to allow search auto mountpoints.
- Dontaudit rpm leaks for prelink_mask_t.
- Allow sysctl to have running under hypervkvp_t domain.

* Wed May 27 2015 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-271
- Remove ctdbd_manage_var_files() interface which is not used and is declared for the wrong type.
Resolves:#1221929

* Tue May 26 2015 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-270
- Update policy rules for afs_fserver_t to allow connectto on unix_stream_socket instead of afs_t.
- Allow smbd to access /var/lib/ctdb/persistent/secrets.tdb.0.
- Allow glusterd to execute consoletype.
- Glusterd wants to manage samba config files if they are setup together.
Resolves:#1221929

* Mon May 25 2015 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-269
- Fix labeling for /var/tmp/kiprop_0 to kadmind_tmp_t.
- Allow postdrop runinng as postfix_postdrop_t to access /var/spool/postfix/public/pickup socket.
- Allow gluster hooks scripts to transition to ctdbd_t.
- Update policy rules for afs_fserver_t to allow connectto on unix_stream_socket.
- Allow gluster transition to smbd_t also using samba init script.
Resolves:#1221929

* Wed May 20 2015 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-268
- Add labeling for /var/run/ctdb and allow samba domains to connect to ctdbd.
Resolves:#1221929
- Allow glusterd to read/write samba config files.
- Update mysqld rules related to mysqld log files.
- Add fixes for hypervkvp realed to ifdown/ifup scripts.
- Update netlink_route_socket for ptp4l.
- Allow sosreport to dbus chat with NM.
- Allow glusterd to connect to /var/run/dbus/system_bus_socket.
- ALlow glusterd to have sys_ptrace capability. Needed by gluster+samba configuration.
- Add new boolean samba_load_libgfapi to allow smbd load libgfapi from gluster. Allow smbd to read gluster config files by default.
- Allow gluster to transition to smbd. It is needed for smbd+gluster configuration.
- Allow glusterd to read /dev/random.
- Label all gluster hooks in /var/lib/gluster as bin_t. Thy are not created on the fly.
- Update nagios_run_sudo boolean to allow run chkpwd.
- Add labeling for /usr/sbin/kpropd.
- Add nagios_run_sudo boolean
- Allow ctdb to create rawip socket.

* Wed May 13 2015 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-267
- Allow ctdb to create rawip socket.
- ALlow nmbd_t to crate nmbd_var_run_t dir under smbd_var_run_t.
- Make ctdbd as userdom_home_reader.
- Allow ctdbd to bind  smbd port.
Resolves:#1219317

* Tue May 12 2015 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-266
- Add audit_access permissions
- Allow cupsd_t access to files in /etc dir
- Allow hplip to dbus chat with all users.
- Allow sblim-gathered sys_ptrace capability.
- Allow sys_admin capability for gfs_controld
- Add more cobbler labels to /var/lib/tftpboot/
- Add new smbd_tmpfs_t type.
- Add more fixes related to timemaster+ntp+ptp4l.
- Fix cgdcbxd_admin() interface.
- Add labeling for /var/tmp/kadmin_0 and /var/tmp/kiprop_0.
- Dontaudit read access on admin_home_t for load_policy. 

* Tue Apr 14 2015 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-265
- Allow redis to create /var/run/redis/redis.sock
- Allow fence_mpathpersist to run mpathpersist which requires sys_admin capability.
Resolves:#1206244
- Allow rhn_check running as rpm to domtrans to shutdown domain
- openshift_cache_t does exist

* Fri Apr 10 2015 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-264
- Allow qpidd to read own init script file.
- Allow passenger to accept connection
- Back port hypervkvp fixes from RHEL7
- ALlow load_policy to list inotifyfs filesystem
- Allow cluster domain to execute ldconfig and update lvm_read_config() interface
-  Allow sssd_t to connect to samba TCP port
- Allow NetworkManager to run arping
Resolves:#1209854
- Backport RHEL7 redis policy
- Add apache log and lib labels for roundcubemail

* Fri Apr 3 2015 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-263
- Allow userdomain to manage pcscd pid fifo files.
- Allow prelink domain access to /dev/console 
Resolves:#1145662
- Allow httpd search access on tomcat6 directory
- Allow apcupsd to get attributes of filesystems with xattrs
- Allow qemu-ga getattr access of all filesystems
- Allow abrt to read network state information
- Make collectd_t as unconfined domain.
- Make rpcbind as nsswitch domain.
- Back port labeling for /etc/my.cnf.d dir.
- Allow dhcpd kill capability.
- Allow cachefilesd to create cachefilesd_var_t
- cvs_home backport from RHEL7.
- Add support for new fence agent fence_mpath which is executed by fence_node
- Allow lsmd plugin to run with configured SSSD.
- Allow bacula access to tape devices
- Allow sblim-sfcb setuid.
- Allow sblim domain to read sysctls.
- Allow ntp to read localtime and allow timemaster send a signal to ntpd.
- Add cobblerd_t fixes
- Allow mysqld_t to use pam
- Dontaudit xguest_t communication with avahi_t via dbus
- Allow cobblerd_t to communicate with sssd
- Allow pmwebd to send and receive messages from avahi over dbus
- Allow conman_t to commmunicate with sssd
- Allow mysqld_t to send audit messages
- Allow load_policy rw access to inherited sssd pipes
- Update label for /etc/mcelog/.* files
- Allow bacula_t to connect to psql via tcp/unix socket
- Remove type to only match directories on /boot
- Add more labels for ownCloud
- Dontaudit net_admin capability for munin

* Wed Mar 4 2015 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-262
- Allow lsmd_t getattr all exec.
Resolves:#1141719
- Update afs policy
Resolves:#1136396
- Add support for /usr/sbin/named-sdb.
- Add support for mongos service.
- Allow cyrus to use tcp/2005 port.
- More service wants to auth_use_nsswitch.
- Allow apps that need to read sysctl_vm_overcommit_t be able to read it.
- Update passenger rules from RHEL7.
- Allow smartd to manage generich devices if they are created with wrong label.
- Allow sblim-sfcb to execute itself.

* Tue Mar 3 2015 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-261
- Allow sys_ptrace and dac_override caps for collectd.
- Add labeling for /etc/rc\.d/init\.d/htcacheclean.
- Allow /usr/sbin/sfcbd to send audit msgs.
- Allow postdrop to connect to master process over unix stream socket.
- Allow ssh_t to connect to all unreserved ports.
- Allow setfiles domain to access files with admin_home_t. semanage -i /root/testfile.
- Don't relabel files under /dev/shm/
- Allow munin_disk_plugin_t getattr access on blk_file 
- Allow xauth_t and sshd_t to search automount_tmp_t if use_nfs_home_dirs boolean.
- Add suppor for keepalived unconfined scripts and allow keepalived to read all domain state and kill capability.
- Allow antivirus domains to read all dirs/files regardless of their MCS category set.
- Add labeling for mariadb log/pid files/dirs.
- Allow rsyslogd to read /proc/sys/vm/overcommit_memory file.
- Allow slapd to read /usr/share/cracklib/pw_dict.hwm.
- Remove ftpd_use_passive_mode boolean. It does not make sense due to ephemeral port handling.
- Add support for /usr/libexec/sssd/selinux_child and create sssd_selinux_manager_t domain for it.
- Allow qpidd to read network state and sysctls dirs
Resolves:#1171275
- Add labeling for /var/bacula directory.
- mcelog runs as a daemon domain 
- Allow shutdown to r/w iherited rhev-agetnd pipes.
- Allow sshd to seind signull itself.
- Add the 'base_ro_file_type' and 'base_file_type' attributes to RHEL6.
- Allow prelink_mask_t getattr on filesystems that support xattrs
- Allow radious to connect to apache ports to do OCSP check.
- remove transition from unconfined user to auditctl.
- Backport RHEL7 sblim-sfcb fixes.
- Add bacula fixes related to unconfined scripts based on ssekidde@redhat.com patch.
- Allow zebra to communicate with sssd 
- Add interfaces fixes.
- Added some optional blogs from timemaster policy to chronyd.
- Added linuxptp policy
- Add interface to read mysql db link files
- Added cinder policy
- Make munin yum plugin as unconfined by default.
- Allow bitlbee connections to the system DBUS.
- Allow hv_vss_daemon to call ioctl(FIFREEZE) on /boot.
- Add rsync_server boolean to don't have a transition from initrc by default.
- Dontaudit to r/w inherited pipes from httpd because of certmonger unconfined scripts.
- Backport all capabilities for cvs from RHEL7.
- Allow dccproc to execute bash.
- Fix labeling for /usr/libexec/nm-dispatcher.action.
- Allow logrotate to manage virt_cache.
- Allow osad to execute rhn_check.
- Make osad_t as unconfined domain.
- Allow osad connect to jabber client port.
- Allow rhev-agentd to access /dev/.udev/db/block:sr0.

* Wed Sep 17 2014 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-260
- Add virt_getattr_images and call it for sblim_sfcbd_t.
- We also need to call virt_search_images for sblim.
Resolves:#1140614

* Wed Sep 17 2014 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-259
- Add missing nagios_var_lib_t definition
Resolves:#1103674

* Wed Sep 17 2014 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-258
- Allow unlink lib_t located in /tmp for prelink_mask_t.
Resolves:#1103674
- Add support for pnp4nagios
- Allow mysql to read all domain state
- Allow sblim_sfcbd_t to search virt images
- Revert "Remove shadow_t label from /etc/security/opasswd "

* Tue Sep 16 2014 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-257
- Add fixes for sblim_sfcbd to make libvirt-cim working.
- Allow keepalived stream connect to snmpd
- Allow local_login_t and xdm_t to manage etc_t if authlogin_can_shadow boolean.
- Allow prelink_transition_domain to send signal to prelink_mask_t.
Resolves:#1103674

* Fri Sep 12 2014 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-256
- Allow sosreport to domtrans to prelink_t instead of prelink_mask_t.
Resolves:#1103674

* Thu Sep 11 2014 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-255
- Allow couriertcpd to read /var/spool/courier dir.
- Allow prelink domain to rea /dev/mem.
- ALlow transition to prelink_t instead of prelink_mask_t to ABRT domains/rpm.
Resolves:#1103674

* Fri Sep 5 2014 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-254
- Dontaudit to read/write all dev nodes for prelink_mask_t.
- Add label for path /var/lib/ctdb
- Allow escd access to /var/run/pcscd.events directory
Resolves:#1103674

* Tue Sep 2 2014 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-253
- Add additional dontaudits for prelink_mask_t
Resolves:#1103674
- Allow local_login_t and xdm_t to manage shadow_t because of PAM

* Tue Aug 26 2014 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-252
- Allow aide_t to read /dev/random and /dev/urandom.
- Allow sysadm to talk with lldpad over unix dgram socket.
- Allow sysadm to send/recv with unix dgram socket.
- Allow crond_t to read lastlog.
- Allow xdm_t to read plymouthd_spool_t files
Resolves:#1131195
- Allow hald to rpm dbus chat
- Additional dontaudits for prelink_mask_t.
- Add samba_domain attribute also for smbcontrol_t and winbind_helper_t.

* Wed Aug 20 2014 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-251
- Allow tgtd service to read kernel network state
Resolves: 1130040
- Allow mail-servers policies to read pcp libs
Resolves: 1130934
- Allow passwd_t to read/write stream sockets
Resolves: #1129296
- Add support for zabbix external scripts for which zabbix_script_t domain has been created. This domain is unconfined by default and user needs to run 'semodule -d unconfined' to make system running without unconfined domains. 
- Dontaudit zebra to read getattr for all files and dirs
Resolves: 1122031
- Allow zebra to read /dev/urandom
Resolves: #1122031
- Label /var/lib/asterisk/agi-bin as bin_t
- Added to lldpad policy sys_resource cap. and allow read localization 
Resolves:1021984
- Fix path to luci(/usr/sbin/luci) 
Resolves:1023202
- Add auth_can_read_shadow_passwords for rlogind.
- Add authlogin_shadow boolean for all login domains.
- Dontaudit rw all non security leaks.

* Fri Aug 8 2014 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-250
- Dontaudit read/write/setattr all pipes for prelink domains on all domains
Resolves:#1103674
- Allow chroot_user_t to change the role.
- Add sys_time caps for virt_qemu_ga_t
- Add label for /usr/sbin/luci

* Thu Aug 7 2014 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-249
- Add support for luci.
- Add support for rhsmd and treat it with rhsmcertd_t.
- Make zabbix_agent_t as unconfined domain for rhel6.6.
- Allow chroot_user_t to change process identity.
Resolves:#1082183
- Revert "Remove shadow_t label from /etc/security/opasswd
- Dontaudit relabel lib_t files for prelink_mask_t.

* Tue Aug 5 2014 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-248
- Allow openshift_cron_t to append to openshift log files, label /var/log/openshift 
Resolves: #1034206
- Do not send/receive packets when ftpd_use_passive_mode is disabled 
Resolves: #1105544
- Allow qemu-ga domtrans to hwclock 
Resolves: #1062384
- Allow sshd read access to files on ftp directory 
Resolves: #1097387
- dontaudit r/w inherited certs for prelink_mask_t.
- Allow sblim_gatherd_t to search all mountpoints. This is caused by ps. Should not be needed in Fedora.
- Fix labeling in dhcpc.fc.
- Add labels also for glusterd sockets.

* Tue Jul 29 2014 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-247
- Add all login domain auth_can_read_shadow_passwords attribute.
- Added support for dhcrelay service
Resolves: #1123338
- We need to call auth_tunable_read_shadow in auth_shadow boolean.
- Move authlogin_shadow to authlogin.if.
- Add filetrans also for bacula log files.
- Dontaudit kdumpgui to read openshift_initrc_exec_t
Resolves: #1023336
- Allow squid to manage squid_var_run_t sock_file
Resolves: #1102346
- Alloe bacula manage bacula_log_t dirs
Resolves: #1122545
- Added sys_ptrace cap. to stapserver_t
Resolves: #811366
- Label also /var/run/glusterd.socket file as glusterd_var_run_t
Resolves: #1052206
- Added support for collectd daemon
Resolves: #1024715
- Label conmans pid file as conman_var_run_t, Resolves: #1122106
- Fix authlogin_shadow boolean to have it for all login_pgm domains
- Dontaudit r/w inherited all log files for prelink_mask_t
- Label zabbix_var_lib_t directories
Resolves: #1053205
- Allow all sblim domain to read localization data
Resolves:##1122022

* Mon Jul 21 2014 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-246
- Add boolean to allow user login programs access to /etc/shadow
- Use old icecast_connect_any boolean name and dontaudit list /tmp with tmp_t labeling
- Remove unused interface rtas_errd_systemctl 
Resolves:#1121169
- Allow prelink_mask to use user terminals and dontaudit relabel tmpfiles.
- Dontaudit r/w inherited lockfiles/tmpfiles for prelink_mask_t.
- Allow prelink_mask to append all log files.

* Fri Jul 18 2014 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-245
- Allow setpgid for all sandbox domains.
- Allow sandbox domains read all mountpoint symlinks to make symlinked homedirs working with sandbox.
- One more fix for osad.te
- Back port osad changes from RHEL7.
- Rename svirt_lxc_file_t to svirt_sandbox_file_t.
- Label nginx init script as httpd_initrc_exec_t 
Resolves:#1045041
- Allow postfix_smtpd to stream connect to antivirus 
Resolves:#1105889
- Label init thttpd file as httpd_initrc_exec_t 
Resolves:#1069843
- Allow httpd to setattr on httpd_log files
Resolves:#1111581
- Add tomcat
- Allow zabbix to read system network state
- Allow ndc to read random and urandom device 
Resolves:#1110397
- Add kerberos support for radiusd.
- Allow procmail to ioctl on zarafa-deliver executable.

* Mon Jul 14 2014 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-244
- Add support for vdsm 
Resolves:#1064270
- Allow userdomain role to access prelink_mask_t
- Rename module glusterfs to glusterd 
Resolves:#1052206
- Allow gfs_controld_t to getattr on all file systems 
Resolves:#1110886
- Allow apache to manage pid sock files 
Resolves:#1042864
- Bind TCP/UDP sockets to the nfs port
- The /var/run/tuned directory is not a regular file 
Resolves:#1117685
- Allow utilize winbind for authentication to AD. 
Resolves:#1084177
- Dont audit access on /etc/init.d/mcollective for kdump_t
- FIx labeling in networkmanager.fc
- Allow passenger to connect to MySQL
- ALlow passenger to read locales
- Dontaudit relabelfrom/relabelto for all variablefiles for prelink_map_t
- Change all var_lib_t types to have also variablestatefile attribute
- Implement new prelink_mask_t domain to which transition all domain by default (using fips_mode boolean) except prelink_transition domains. 

* Thu Jul 10 2014 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-243
- Implement new prelink_mask_t domain to which transition all domain by default (using fips_mode boolean) except prelink_transition domains.

* Tue Jul 8 2014 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-242
- Added support for glance-scrubber
Resolves:#1113271
- Fix labeling for /var/lib/dokuwiki

* Tue Jul 8 2014 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-241
- Remove deny_ptrace from interfaces
- Add setpgid procces to mip6d_t
- Added support for hv_vss_daemon
- Allow keepalived also managed snmp lib dirs
- Allow chroot_user_t unconfined shell domtrans
Resolves:#1082183
- Label swift-object-expirer as swift_exec_t
- Allow keepalived manage snmp files, dontaudit list tmp files
Resolves:#1053450
- Additional fix for calling postfix interfaces in sysadm.te to make postfix_admin() working

* Fri Jul 4 2014 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-240
- Allow nagios to stream connect to postgresqlBZ #1015708
Resolves:#1015708
- Allow hypervkvp read localization
- Fix postfix_admin()
- Add lldpad policy for MLS

* Fri Jul 4 2014 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-239
- Fixed lsmd_plugin_t
Resolves:#1111619
- Added glusterd_conf_t alias glusterd_etc_t
- Allow samba to touch/manage fifo_files or sock_files in a samba_share_t directory 
Resolves:#982160
- Label zabbix-proxy files
Resolves:#1018211
- allow sshd to write to all process levels in order to change passwd when running at a level
Resolves:#837616
- Allow updpwd_t to downgrade /etc/passwd file to s0, if it is not running with this range 
Resolves:#837616
- Rename quantum port to neutron 
Resolves:#1024927
- Added zarafa_read_lib_files interface
- Added dont audit list non security files in xdm_t 
Resolves:#1030760
- Added more fixes relates to 
Resolves:#1060656
- Added dontaudit rules to xdm_t 
Resolves:#1030760
- Allow procmail to run zarafa-degent 
Resolves:#1060656
- Add userdom_user_application_domain in xauth 
Resolves:#1013832
- Allow dmesg read raw memory 
Resolves:#1030762
- Allow communication between postfix and cyrus 
Resolves:#1057307

* Wed Jul 2 2014 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-238
- Allow domain to read an append inherited tmp files
- Dontauit leaks of var_t into ifconfig_t
- Allow fsdaemon_t to read/write device_t char files 
Resolves:#1035363
- Remove sblim_filetrans_named_content in RHEL6
- We don't have systemd in RHEL6.
- one more fix for bacula_admin()
- fix bacula_run_admin()
- Remove shadow_t label from /etc/security/opasswd 
- Fix logrotate_use_nfs boolean
- Allow userdom to read inherited users files in /tmp 
- Allow certmonger_t read puppet libs
- Allow in logging_inherit_append_all_logs also ioctl and append
- Label pacemaker_remoted as cluster_exec_t
- Tag some conman exec files
- Allow conman to read localization
- Should use rw_socket_perms rather then sock_file on a unix_stream_socket
- Added conman fixes
- Allow apache to manage passenger sock_files
- Allow bacula to bind on 9103 tcp port
- Allow postfix stream connect to antivirus
- Allow osad to read localization

* Tue Jun 24 2014 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-237
- Fixes for mirrormanager
- Fix swift interface
- Allow lsmd_plugin_t to read localization
- Allow keepalived read snmp libs, Allow keepalived connect to agentx port
- Allow keepalived read localization
- Added setuid capability to lsm service
- Added some swift rules to rsync policy
- Remove duplicate line entry in .fc
- Do not send/receive packets when ftpd_use_passive_mode is disabled
- Add mirrormanager policy to RHEL6 Fixes Bug 1042864
- Update permissivedomains by mirrormanager
- Add mirrormanager policy
- Added support for openwsmand
- Added policy for swift
- Added support for sblim
- label also 64bit heartbeat libs
- Allow kill capability on varnish
- Added haveged policy
- Add missing kernel_rw_stream_socket_perms
- Label tcp/udp port no. 3052 as apc, Allow apcups to bind on apc port
- Allow logwatch stream connect to courier service
- Fix mcelog policy
- Back port rsyslog fixes from RHEL7 for rsyslog7
- Fix whitespace
- Add support for osad
- Fix automount policy
- Added policy for bacula
- add radvd_read_pid_files inteface
- Add missing syslog-conn port
- Allow httpd_t write to kernel keyring
- Allow httpd_sys_script_t domain to send system log messages 
- Allow passwd_t to write to ipa trusted user files in /tmp 
- Boolean to allow mcelog use all the user ttys 
- Allow icecast to use any tcp ports 
- Define oracleasm_t as a device node 
- Allow sudomain to getattr of kernel interface
- Add squid directory in /var/run
- Allow automount read nfs symlinks
- Allow asterisk to connect to the apache ports
- allow abrt to read mcelog log file 
- allow udev to search radvd files under the /run dir 
- allow auditctl getattr access on blk_file 
Resolves:#1080555
- Allow ssh to manage nfs links

* Wed Apr 23 2014 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-236
- Added conman policy
- Added label for conman port
- Added support for mip6d policy
- Added support for isns
- Added rtas_errd policy
- Added support for keepalived policy
- Add label samba_spool_t for /var/spool/samba
- Allow httpd_t to bind preupgrade port if httpd_run_preupgrade boolean is enabled
- Allow openshift_cron_t to append to openshift log files
- dontaudit sudo domains listing /dev
- Allow read/write to login records
- Allow auditctl getattr access on blk_file
- Allow nova-scheduler to read utmp
- Added stapserver policy
- Added support for freeipmi services
- Added lsm policy
- Added support for pcp service
- Added chown capability to dhcpd_t domain
- Add boolean to allow openshift domains nfs access
- Allow abrt to read man pages and getcap
- Allow cgroupdrulesengd to create content in cgoups directories
- Dontaudit smbd_t sending out random signuls
- Backport all zabbix changes
- Allow mcelog write access to nscd socket

* Thu Apr 17 2014 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-235
- Add support for nginx
Resolves:#1045041
- Change shutdown_t to also read wtmp
- Added support for hypervkvpd
- Add preupgrade policy

* Mon Mar 31 2014 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-234
- Add httpd_dbus_sssd boolean to make mod_lookup_identit working
- Add support for ABRT FAF

* Fri Mar 21 2014 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-233
- Add support for OpenShift syslog plugin
- Allow snmpd to getattr on removeable and fixed disks
- Add shmemnetgrp and getnetgrp to access_vectors
Resolves:#1025758

* Fri Dec 13 2013 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-232
- Add more fixes for zabbix-agent
- Fix neutron labeling
- Allow all domains to read sysfs_t due to glibc change
- Allow ping to read inherited zabbix tmp files
Resolves:#1039851
- Allow hostname to read/write inherited rpm script files

* Tue Oct 29 2013 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-231
- Add named_cache_t label for /var/lib/unbound
- Fix puppet_domtrans_master() interface to make passenger working correctly if it wants to read puppet config files
- Allow anitvirus domains to manage own log dirs

* Tue Oct 29 2013 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-230
- Add missing transition from dovecot-auth to oddjob_mkhomedir

* Thu Oct 24 2013 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-229
- Add bootloader_exec_t labeling for /sbin/grubby
Resolves:#915729
- Add etc_runtime_t label for zipl.conf
- Allow daemons to manage cluster lib files if daemons_enable_cluster_mode is enabled

* Wed Oct 23 2013 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-228
- Add daemons_enable_cluster_mode boolean and turn on it by default until RHEL6.6
Resolves:#915151
- Add tcp/8893 as milter port
- Allow antivirus domain to read localization without the boolean

* Tue Oct 22 2013 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-227
- Resource agents needs to manage /etc/cluster to place own config files
Resolves:#915151
- tgtd needs ipc_lock

* Mon Oct 21 2013 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-226
- Label /usr/sbin/fence_scsi as fenced_exec_t
- Fix cluster domains to create dirs in /var/run/cluster as var_run_t to make resource scripts working
Resolves:#915151

* Tue Oct 15 2013 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-225
- Re-write rules to create tmpfs for all piranha tmpfs files/dirs
- Allow piranha-lvs to manage piranha_tmpfs_t
Resolves:#1018306

* Tue Oct 15 2013 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-224
- Allow piranha_pulse_t to create tmpfs and send sigkill to piranha domains

* Tue Oct 15 2013 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-223
- Fix dovecot_rw_pipes() interface
- Allow piranha_pulse_t to search tmpfs
- Allow sysadm to stream connect to postfix-master process
- Label /usr/sbin/fence_sanlockd as fenced_exec_t

* Wed Oct 9 2013 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-222
- Add  kdumpgui_run_bootloader to allow execute zipl correctly

* Wed Oct 9 2013 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-221
- Fix /var/run/charon labeling
- More fix for strongswant and ipsec.secretes
- Allow sandbox domain to use inherited user terminals

* Tue Oct 8 2013 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-220
- Allow cobblerd to stream connect to MySQL
- Allow cobblerd to execute ldconfig
- Allow openstack-glance to access to amqp
- Add labeling for /var/run/charon.*
- Make munin "df" plugins working
Resolves:#908095

* Wed Oct 2 2013 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-219
- Update httpd_can_sendmail boolean to allow read/write postfix spool maildrop
- Allow tzdate to unlink etc_t lnk files
- Allow jabberd to connect to jabber_interserver port
- Fix description for logging_syslog_can_read_tmp boolean
- Update ipsec rules and labels
Resolves:#986883
- Allow pegasus transition to mount_t

* Fri Sep 27 2013 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-218
- Add support for /var/log/qemu-ga directory
- Regenerate man pages for domains
Resolves:#880728
- Allow setgid capability for ipsec_t
- Allow ipsec to send signull to itself
- Add tcp/9000 as http_port_t
- Allow dirsrv_t to create tmpfs_t directories
- Fix git_role() interface

* Fri Sep 20 2013 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-217
- Fix virtd_lxc_t to be able to communicate with hal
- Allow NM and wireless working together
Resolves:#1009661
- Allow my_print_default to read /dev/urand

* Fri Sep 13 2013 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-216
- Remove transition from virtd_t to qemu_t to stay in virtd_t if selinux_driver is None in qemu.conf
- Allow openshift_cron_t to run ssh-keygen in ssh_keygen_t to access host keys

* Wed Sep 11 2013 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-215
- Add port definition of pka_ca to port 829 for openshift
- Rename quantum to neutron
- Allow rpcd to request the kernel to load a module
- Allow ovsdb-server to create dirs/files in /tmp directory

* Fri Sep 6 2013 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-214
- Allow git daemons to read localization
- Allow tgtd_t to connect to isns ports
Resolves:#1003571
- Cleanup antivirus policy and add additional fixes
- Fix labeling for munin CGI scripts
- Allow virtd_t also relabel unix stream sockets for virt_image_type
- Fix fs_search_auto_mountpoints to allow search automount tmp dirs
Resolves:#990661

* Tue Aug 27 2013 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-213
- Add openhpid policy
Resolves:#1000521
- Fix rhcs_domain_template to allow cluster_t to create socket in /var/run with correct labeling

* Fri Aug 23 2013 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-212
- Update rules for antivirus domains
Resolves:#999471
- Allow virt_domain to read virt_var_run_t symlinks
- Allow chroot_user_t to read/write inherited user domain pty
- Allow to start guest while the libvirtd is started with valgrind
- Allow lldpad to talk with fcoemon
- Allow chronyd sched_setscheduler

* Thu Aug 8 2013 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-211
- Fix spec file
- Fix zabbix labeling

* Tue Aug 6 2013 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-210
- Allow nrpe to list /var
- Allow apache to search automount tmp dirs if http_use_nfs is enabled
- Add support for strongswan
- Fix description of ftpd_use_fusefs boolean
- Allow kdumpgui to write dos files for /boot/efi/EFI/fedora/grub.cfg
- Back port tgtd fixes from Fedora to allow sys_rawio cap
- Add support for OpenDMARCD
Resolves:#983551
- Allow openvpn to run unconfined scripts
- Allow amavis to execute shell
Resolves:#979421
- man pages should be owned only by selinux-policy-doc package
- Fix fs_manage_nfs_files and fs_manage_nfs_dirs boolean to allow to search autofs
- Allow mysqld-safe sys_nice/sys_resource caps
Resolves:#975921
- Add labeling for /boot/etc/yaboot.conf
Resolves:#973156
- /var/log/syslog-ng should be labeled var_log_t
- Back port munin-cgi fixes
- Fix ftp_home_dir boolean 
- Allow kdump to read kcore on MLS system
- Add support for svn ports
- Add labels for /dev/ptp*
- Add labels for /etc/security/opasswd
- Fix labeling for /etc/localtime lnk file
- Add  tftp booleans for NFS/CIFS access
- Merge amavis,clamd,clamscan,freshclam policies to antivirus policy
- Label all nagios plugins as nagios_unconfined_plugin_exec_t by default
- Add additional ports as mongod_port_t
- Allow sandbox domains to use inherted terminals
- Allow pegasus to execute mount in pegasus_t domain
- Fix *_admin interfaces  and interface descriptions
- Allow yppasswdd to use NIS
- Allow nagios to manage nagios spool files
- Allow ABRT to domtrans to prelink
Resolves:#921234
- Fix labeling for /var/lib/dspam/
Resolves:#919456
- Label postfix-policyd-spf-perl as bin_t
- Allow nrpe to run sudo
- Label /usr/bin/yum-builddep as rpm_exec_t
- Label /usr/local/bin/x11vnc as xserver_exec_t
- Allow logwatch to domtrans to mdadm
- Allow postfix-master to list /tmp dir
- Add lldpad policy and make it as unconfined domain
- Allow sysadm to admin postfix
- ALlow postfix_virtual to stream connect to mysql
- Update zabbix policy
- Activate watchod policy and make it as unconfined
- Add httpd_serve_cobbler_files boolean
- Make postfix_postdrop_t as mta_agent to allow domtrans to system mail if it is executed by apache
- Add oracleasm policy
- Add support for pand
- Add awstats_purge_apache_log_files boolean
- Back port smstools policy

* Fri Jul 19 2013 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-209
- Remove old cluster policies also for MLS
Resolves:#915151

* Wed Jul 17 2013 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-208
- Merge cluster administrative domains to cluster_t. Back ported from Fedora
Resolves:#915151
- Aadd additinal rules for disk plugins
- Allow setuid/setgid caps for syslogd_t
- Dontaudit sendmail to  write dovecote-deliver tmp files
- Add suppport for /var/lib/openvpn
- /var/spool/snmptt is a directory which snmdp needs to write to

* Mon Jul 9 2013 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-207
- Make tcp/81 as http port
- Add cert_t labeling for pki stuff
Resolves:#959554

* Tue Jun 25 2013 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-206
- Update openvswitch policy
Resolves:#977415
- Add support for zfs

* Wed Jun 12 2013 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-205
- Remove domtrans for quantum which needs to stay in the same domain
- Allow qemu to manage nova lib files
- Allow hald to read svirt images
Resolves:#966106

* Thu Jun 6 2013 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-204
- Allow iptables to read and write quantum inherited pipes
- Allow iptables to send sigchld to quantum
Resolves:#966106

* Wed Jun 5 2013 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-203
- Allow dnsmasq to stream connect to quantum
- Allow ifconfig domtrans to iptables and execute ldconfig
Resolves:#966106
- Make openshift_initrc_t as initrc domain

* Thu May 30 2013 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-202
- Make Quantum 2013.1.1 working with netns
- Make SSHing into an Openshift Enterprise Node working

* Thu May 23 2013 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-201
- Add virt_qemu_ga_unconfined_t for hook scripts

* Tue May 21 2013 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-200
- Add virt_kill interface and use it for sanlock

* Tue Apr 21 2013 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-199
- qemu-ga needs to execute scripts in /usr/libexec/qemu-ga
- Allow openshift_cron_t to manage openshift_var_lib_t sym links
- Allow dovecot-auth to execute bin_t
- Allow mysqld-safe to execute bin_t
- Allow procmail to manage user tmp files
- Allow sanlock to kill svirt_t
Resolves:#913673

* Tue Apr 16 2013 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-198
- Allow dirsrv-admin script to exec apache modules
- Add labeling for dirsrv-admin lock file
- Add labeling for /var/lib/owncloud
- Add labeling for /var/www/moodle
Resolves:#913673

* Tue Apr 4 2013 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-197
- Fix /etc/dhcp labeling
- Back port openshift fixes
- Make dirsrv-admin server restarted from console working
- Add ftpd_use_fusefs boolean
Resolves:#913673
- openshift_cron_t needs dac_override

* Thu Mar 21 2013 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-196
- Backport openshfit fixes
- Allow cgred to use notify 
Resolves:#913673
- Allow mount to transition to gluster 
- Fix tuned policy to make it working with the lastet tuned package

* Tue Jan 22 2013 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-195
- Make matahari domains as unconfined
- Allow nscd to connect to nmbd
Resolves:#901565
- Allow setcap/getcap for syslogd

* Wed Jan 16 2013 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-194
- qdiskd needs to read usr_t/bin_t files
- Allow dpsam to connect/bind to spamd ports
- Allow munin services plugins to bind to generic node
Resolves:#865759

* Tue Jan 15 2013 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-193
- Fix ssh_sysadm_login boolean for MLS
Resolves:#865759
- Allow rpm_script_t to dbus communicate with certmonger_t
- More fixes for qemu-ga to make "guest-fsfreeze-freeze" working 
* Wed Jan 9 2013 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-192
- Label /usr/lib/yaboot/addnote as bin_t
- Allow postfix_local to read/write /var/spool/postfix/active
- Allow postfix domains to list /tmp
- Allow wdmd to transition to kdump
Resolves:#887793
- Add labeling for /var/named/chroot/etc/localtime

* Fri Jan 4 2013 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-191
- Remove pam_selinux due to conflict
- Add labeling for /etc/multipath - lvm_metadata_t
Resolves:#880407
- Add additional gitolite3 labeling

* Fri Jan 4 2013 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-190
- Allow virtd to settattr on virt image dirs in MLS
Resolves:#885045
- Allow all postfix domains to connect to mysql stream
- Call init_daemon_domain for rsync_t
- Add labeling for /var/lib/pgsql/ssh 
- Allow certmonger to send signal to itself
- Allow rsyslog to read user tmp files using logging_syslog_can_read_tmp boolean
- Add support for 1228/tcp and 1228/udp ports and allow corosync touse them
- Allow corosync to read wdmd tmpfs
- Allow wdmd to execute consoletype
- Update man pages using sepolicy from Fedora
- Fix admin interfaces  

* Tue Dec 18 2012 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-189
- Allow virt_qemu_ga to execute shutdown
- sssd needs to connect to kerberos password port if a user changes his password
- More fixes for the dspam domain
- Allow dovecot to execute bash
- Additional fixes for passenger
Resolves:#886619
- Add labeling for /var/run/checkquorum-timer

* Tue Dec 18 2012 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-188
- Allow rpcd_t to read /var/run/utmp
- Make glance domains as permissive instead of just glance_t
- Allow kill capability for ftpd
- Add labeling for prespawn helper script
Resolves:#886619
- Allow winbind to stream connect to nmbd
- Allow transition from virt domains to bridgehelper domain
- Add support for watchdog script from sanlock
- Add labeling for tmp-inst
- Fix rhev policy
- Update virt_qemu_ga policy
- Backport wm_domain policy
- Backport virtd_lxc_t and make it as unconfined domain

* Wed Dec 12 2012 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-187
- Add missing labeling for /usr/share/ovirt-guest-agent/ovirt-guest-agent.py
Resolves:#885432
- Add labeling for /var/nmbd
- apache/drupal can run clamscan on uploaded content

* Mon Dec 10 2012 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-186
- Allow virtd to manage dnsmasq pid files
- Allow all samba domains to create samba directory in var_t directory
- Dontaudit attempts by openshift to read apache logs
- Add labeling for /usr/share/ovirt-guest-agent/ovirt-guest-agent.py
Resolves:#885432

* Wed Dec 5 2012 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-185
- Apache is sending sinal to openshift_initrc_t now
-  Allow all directories/files in /var/log starting with passenger to be labeled passenger_log_t
- Allow winbind to manage samba_var_t sock files
- Allow git-daemon and httpd to serve the same dir
Resolves:#883143
- Allow dac_override for nrpe

* Mon Dec 3 2012 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-184
- Add support for tcp/10026 port as dspam_port_t
- Allow dspam to connect/bind to dspam_port_t
- Add uconfined_munin_plugin_exec_t for all plugins which are not covered by munin plugins policy
- Allow domains that can read sssd_public_t files to also list the directory
Resolves:#881413
- Allow programs to run in fips_mode using fips_mode boolean
- Change oddjob to transition to a ranged openshift_initr_exec_t when run from oddjob
- Allow sshd to look into the mysql home directory for authorized_keys
- Make rsync as homemanager which allows to manage CIFS/NFS	  
- 

* Tue Nov 27 2012 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-183
- Allow quota to manage openshift_var_lib_t directories
Resolves:#843732

* Tue Nov 27 2012 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-182
- Fix labeling for /var/named/chroot/usr/lib
Resolves:#843732
- Allow amavis to stream connect to snmpd
Resolves:#839250
- Additional fixes for log files related to logrotate
- Allow all domains to read base etc_t file type
- Allow logrotate to list root home directory
- Fix labeling for /var/log/z-push
- Allow cyrus init scriptu to manage cyrus data files
- Dontaudit leaks of locks or generic log files to systemprocesses
- Allow ricci-modrpm to send syslog msgs
- Allow munin to have kill capability

* Mon Nov 19 2012 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-181
- Allow kdumpgui to read/write to zipl.conf
Resolves:#877108
- Add /proc/numactl support for confined users
- Make proc_numa_t an MLS Trusted Object
- Make ccs_tool and cman_tool labeled as rgmanager_exec_t
- Fix cron_admin_role interface
- Add support for opendkim

* Wed Nov 14 2012 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-180
- Allow openshift domains to execute tmux
- Allow wdmd to getattr on tmpfs_t
Resolves:#831908
- Add labeling for /var/nmbd/unexpected
- Allow winbind to create samba pid dir
- Dontaudit write access on /var/lib/net-snmp/mib_indexes for syslogd
- Fenced communicates with libvirt
- Fix labeling for libflashplayer.so
- Add labeling for /var/lib/zarafa-webapp
- Allow dspam to read localization
- Add labeling for Z-Push
- Allow rpc.svcgssd to search nfsd_fs_t dirs
- Allo cgred to read all sysctl

* Mon Nov 5 2012 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-179
- Fix labeling for /var/lib/sss/mc
Resolves:#871816

* Thu Nov 1 2012 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-178
- Fix labeling for OpenShift binaries
- Add samba_portmapper boolean and labeling for /var/run/samba
Resolves:#871816
- Backport dspam policy

* Wed Oct 31 2012 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-177
- Allow dnsmasq to manage virt run files
Resolves:#843543
- Allow setroubleshootd to read /proc/irq
- Backport fixes for virt_use_* booleans
- Allow qemu-ga to use ttyS0
- Allow dhcpc to manage dhclient-eth0.pid labeled as virt_var_run_t 

* Tue Oct 30 2012 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-176
- Add unconfined munin plugin
Resolves:#871106
- Add new httpd_verify_dns boolean

* Tue Oct 23 2012 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-175
- Add initial openswitch policy. Domains are unconfined
Resolves:#845417
- Add labeling for /usr/sbin/mcollectived
- Allow openshift domains to read /dev/urandom

* Fri Oct 19 2012 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-174
- openshift user domains wants to r/w ssh tcp sockets
- Allow mount to relabelfrom unlabeled file systems
- Additional fix for syslog/kerberos
Resolves:#867001

* Thu Oct 18 2012 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-173
- syslogd_t now support kerberos
Resolves:#867001
- Fix openshift labeling for binaries
- Allow passwd to read usr_t links/files
- Add labeling for /var/lib/sss/mc

* Mon Oct 15 2012 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-172
- Update httpd_runstickshift boolean
- Remove transition from sysadm_t to fsadm_t
Resolves:#852763
- Make vmware-host as unconfined domain
- Allow all domains to read usr_t
- Fix labeling for all log files

* Sat Oct 13 2012 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-171
- Add labeling for /usr/bin/oo-admin-ctl-gears
Resolves:#839831

* Fri Oct 12 2012 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-170
- Fix passenger labeling to support lib64 paths. Needed by openshift
Resolves:#839831

* Thu Oct 11 2012 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-169
- Fix spec file to silent restorecon errors on files which do not exist
- Fix passenger backport
Resolves:#839831

* Tue Oct 9 2012 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-168
- Add support for HTTPProxy* in /etc/freshclam.conf
- pppd wants to read /usr/share/radiusclient-ng/dictionary
- Add ssh_chroot_manage_apache_content and ssh_chroot_full_access booleans
- snmp wants to also manage snmp dirs for amavisd-snmp support
- Add labeling for virsh_fenced
- Allow nmbd_t to crate dirs with samba_var_t labeling
- Add clamscan_can_scan_system boolean
- Allow all domains to getattr on prelink_exec_t
- Add postgresql_can_rsync boolean
- Allow pulse to domain transition to iptables
- Allow nslcd sys_nice capability
- Allow corosync to connect to saphostctrl ports
- Allow passwd to read generic /tmp dirs
- Add policy for qemu-qa
- Add new antivirus policy module for antivirus programs
Resolves:#838260

* Fri Oct 5 2012 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-167
- Allow postfix_locat to search stickshift lib files
- Dontaudit sys_ptrace cap for httpd if httpd_stickshift is on
- Allow openshift domains change process identity
- SELinux is reporting that openshift domains are trying to write into their proc directories
Resolves:#855889

* Wed Oct 3 2012 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-166
- More fixes for openshift and add support for opeshift labeling instead of stickshift
- /etc/selinux/<type>/logins should be owned by the policy package
Resolves:#855889
- Add labeling for /var/tmp/DNS_25      
- Allow postfix_local_t to execute files on nfs_t
- Add fixes for kadmind
- Add rhnsd policy

* Tue Oct 2 2012 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-165
- Add httpd_run_stickshift boolean
- Add labeling for /var/lib/stickshift/.httpd.d
Resolves:#836241

* Tue Oct 2 2012 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-164
- Add additional part of openshift patch
Resolves:#836241

* Mon Oct 1 2012 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-163
- Backport openshift policy
- Allow dovecot_deliver_t to search /root/mail
Resolves:#836241

* Tue Sep 10 2012 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-162
- Add pkcslotd policy
Resolves:#851483
- Allow cyrus-imapd init script to write cyrus data
- Fix labeling for /dev/twa 

* Mon Sep 10 2012 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-161
- Fix labeling for /var/run/cachefilesd.pid
Resolves:#851113

* Fri Sep 7 2012 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-160
- Add named_bind_http_port boolean
- Add port definition for 8953/tcp
- spice-vdagent(d)'s are going to log over to syslog
- Fix labeling for /usr/sbin/rpc.* binaries to label them as rpcd_exec_t
- Add sensord policy
- Allow oddjob_mkhomedir to write on nfs share
- Add virt_bridgehelper policy
- Allow clamd to write/delete own pid file with clamd_var_run_t label
- Add support for wdmd tmpfs
- Add initrc_domain attribute 
- Add bcfg2 policy
- Modify ssh_chroot_rw_homedirs boolean to allow manage apache system r/w content if for /var/www as home
- Add pacemaker policy
- Allow snmpd to connect to corosync over unix stream socket
- Allow crontab to read NFS
- Add new type selinux_login_config_t for /etc/selinux/TYPE/logins directory and allow sssd to manage files in this directory
Resolves:#843814
- Add labeling for /opt/sartest directory
- Add initrc_domain attribute to allow domains to work as initrc_t domain
- heartbeat should be running as rgmanager_t instead of corosync_t
- Add glusterd policy
- Add l2tpd policy
- Add numad policy
Resolves:#801493

* Wed Aug 8 2012 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-159
- Allow munin_stats to read munin logs
- Allow updpwd to write all MLS levels
- Make piranha_web_t as nsswitch domain
- Allow munin mail plugins to read exim log files
- Backport sanlock policy from Fedora
Resolves:#831908
- Allos dac_override, sys_nice for sasl
- Add labeling for /var/named/chroot/usr/lib64
- Add support for gitolite3
- Allow confined users to send mail

* Thu Jul 26 2012 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-158
- Add amavis_use_jit boolean

* Thu Jul 26 2012 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-157
- Allow procmail to manage mail home data
- We should only block MCS node_bind on mcsuntrustedproc
- Fixes for amavis
Resolves:#837815

* Tue Jul 17 2012 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-156
- Allow user to login using ssh with random MLS range
Resolves:#837815
- Allow virtd_t to create mtab with the proper labeling
- Add support for check_icmp nagios plugin
- Make chkconfig working on MLS for sysadm_t
- Allow dovecot to manage mail_home_rw_t
- Add support for fsav
- Allow clamscan to use amavisd-new
- Add support for rhnsd

* Mon Jun 18 2012 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-155
- Allow setroubleshootd to execute rpm
Resolves:#833053
- Add labeling for /usr/lib/flash-plugin/libflashplayer.so

* Thu May 24 2012 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-154
- distcvs to distgit corruption fix
Resolves:#823991

* Wed May 23 2012 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-154
- Allow fenced to manage snmpd lib files
- Allow certmonger to get attributes on init script files
Resolves:#790967
- Fix labeling for Firefox plugins
Resolves:#747993
- Add mta_signal_user_agent() interface

* Wed May 16 2012 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-153
- user_tcp_server boolean should be also for sysadm_t
Resolves:#798534

* Wed May 16 2012 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-152
- Add label for condor_starter
Resolves:#807682
- Dontaudit sys_module for brctl
- Allow winbind to send signull to smbd
- Add jacorb port definition

* Tue May 15 2012 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-151
- Add openstack-nova, openstack-keystone, openstack-glance, openstack-quantum policies
- Allow sysadm_t to create other crontabs
- Allow nfsd_t to read defaul_t link files
- Fix labeling for /var/run/heartbeat
- Fixes for admin_template() interface to make sysadm_secadm.pp module working correctly
- More fixes for condor policy
- Allow chfn_t to creat user_tmp_files
- Allow chfn_t to execute bin_t
- Fix auth_role() interface
- Fixes to make privsep+SELinux working if we try to use chage to change passwd

* Wed May 9 2012 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-150
- Allow condor-startd to dbus chat with hal
#Resolves:#807682
- Allow rpc.mountd to read all files/dirs

* Tue May 8 2012 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-149
- Add labeling for /usr/sbin/matahari-dbus-sysconfigd
- Add additional labeling for zarafa
- Allow guest_t to fix labeling
- Corenet_tcp_bind_all_unreserved_ports(ssh_t) should be called with the user_tcp_server boolean
- squashfs does not support xattr in RHEL6
Resolves:#815898
- Remove pyzor labeling and move it to spamassassin.fc
- Fix config.tgz

* Wed May 2 2012 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-148
- Add mysql_list_db() interface
- Allow sshd to read/write condor-startd tcp socket

* Tue Apr 24 2012 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-147
- Fix man pages for SELinux users
- Allow all user domains to setexec
- Allow cobblerd to get SELinux status and booleans
- Add labeling for /etc/zipl.conf
Resolves:#813803
- Allow fenced to read SNMP lib files

* Tue Apr 17 2012 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-146
- Add sysadm_secadm policy module to separate in secadm_r, sysadm_r
Resolves:#787413
- Fixes for libvirt-qmf
- Add label for package-cleanup 
- Add support for zfs
- Make cfengine domains as unconfined
Resolves:#753184
- Allow sshd_t to dyntransition to sysadm_t

* Thu Apr 4 2012 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-145
- Fix labeling for /var/run/slapd.* sockets
Resolves:#799102
- Add condor policy

* Tue Apr 3 2012 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-144
- Fixes for cfengine policy
  * changed labeling for /var/cfengine/outputs from var_log to cfengine_var_log_t
  * re-arranged policy to use template and cfengine_domain 
- Allow dovecot to domtrans sendmail to handle sieve scripts
- Bacport libvirt-qmf policy for Fedora
- Remove labeling for postmaster.pid file 
- Fix for virtual network which looses network connection
- Add man pages for SELinux users
- cgconfig needs to use getpw calls
- Allow lvm and fsadm to write sysfs_t
- Allow rpc.mounted to list user tmp files
- Fix permissivedomains declarations
Resolves:#806220
- Fix spec file to instal minimum policy properly

* Wed Mar 21 2012 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-143
- Add missing transition from certmonger to certmonger_unconfined_t
Resolves:#790967

* Tue Mar 20 2012 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-142
- Fixes for man pages
- Allow rpcd to execute sm-notify
Resolves:#802247
- Add support for matahari-qmf-rpcd
- Add support matahari vios-proxy-* apps
- Allow quota-check to create files on nonxattr filesystems
- Add support for ~/Maildir
- Allow unconfined dyntransition
- Fixes for certmonger_unconfined and certmonger
- Fixes for certmonger policy

* Wed Mar 14 2012 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-141
- Add man pages for apps, services
- Allow nagios to use user terminals
Resolves:#782325
- Add support for unconfined certmonger scripts
- Add support for matahari-qmf-rpcd service
- Allow chsh to use PAM
- Allow rpc.statd to execute sm-notify which has bin_t label
- Make sure files which are created by /usr/bin/R get proper label in home directories

* Wed Mar 7 2012 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-140
- Add additional fixes for nagios handlers
Resolves:#749311
- Add 7600 and 4447 as jboss_management ports

* Tue Mar 6 2012 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-139
- Allow nfsd_t to getattr on all fs
Resolves:#738628
- Make mailx working together with cron without unconfined module
- Allow sssd sys_resource capability

* Wed Feb 29 2012 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-138
- Add new policy for cfengine
- Add new policy for sge gridengine jobs
- Add support for nagios eventhandlers
- Make system cron jobs run in the proper domain
- Add policy to support privsep ssh process running in user domain
- Add fixes relates to nss/FIPS
- Add new rsync_use_* booleans
- Allow qpidd to connect to matahari ports
- Allow sysadm_u to read system_r in MLS
- Remove razor labeling because we treat razor with spam policy
- Add support for matahari-qmf-sysconfig-consoled, clean up matahari policy
- Fixes for interfaces
Resolves:#791294
Resolves:#796351

* Thu Feb 16 2012 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-137
- Remove nfs_* booleans because nfs runs in kernel_t domain
Resolves:#760405
- Add httpd_manage_ipa boolean
- Dontaudit sys_ptrace for matahari-netd
- Allow vhostmd to getattr on virtd
- Allow snmpd to connect to the ricci_modcluster
- qpidd should be allowed to connect to the amqp port

* Thu Jan 26 2012 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-136
- backport mozilla_plugin policy
- backport sandbox policy to support nacl
- Add support for selinux_avcstat munin plugin
- Treat hearbeat with corosync policy
- Allow system cronjobs to read kernel network state
- Allow corosync to read and write to qpidd shared memory
- More fixes for qpidd
Resolves:#769352
- Add policy for quota-nld

* Wed Jan 25 2012 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-135
- Add fixes for qpidd policy, support for tmpfs_t
Resolves:#769352
- Add fixes for mcelog policy, for new location of pid,sock files
- Make sendmail and postfix working together

* Wed Jan 11 2012 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-134
- Backport ABRT policy
- Backport matahari policy
- Add interfaces for libra
- Add jboss_dubeg port definition

* Wed Jan 4 2012 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-133
- Allow mta_user_agents to send sigchld to transitioning domain

* Tue Jan 3 2012 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-132
- Fixes for nagios policy
- Add a new interface for libra
- Fix spec file to be testing SELinux status correctly

* Mon Dec 5 2011 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-131
- Fixes for rhev policy
- Make ssh-keygen as unconfined domain
- Add sanlock_use_nfs boolean
- Add ssh_dontaudit_search_user_home_dir interface
- namespace_init and MLS fix

* Mon Nov 21 2011 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-130
- Fix cloudform_exec_mongod interface
Resolves:#753184

* Mon Nov 21 2011 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-129
- Cron and libra fixes
#Resolves:#753184

* Mon Nov 21 2011 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-128
- Add cronjob_role for sysadm
#Resolves:#753184
- Change label for /var/spool/cron
- Add interface to allow exec of mongod

* Tue Nov 15 2011 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-127
- Make cronjob working on MLS
#Resolves:#753184

* Wed Nov 9 2011 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-126
- Fix dev_rw_generic_usb_dev
#Resolves:#751388

* Wed Nov 9 2011 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-125
- Change the postinstall to load_policy separately from the semodule command
- This will put the proper files in place even if the kernel rejects the policy.
#Resolves:#751861	
- Allow login programs to connect to the pki_ca_port
- Allow vhostmd to read /dev/rand and signal

* Mon Nov 7 2011 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-124
- Add MCS fixes to make sVirt working correctly
#Resolves:#751388
- Fixes for httpd_dirsrvadmin_script_t policy

* Thu Nov 3 2011 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-123
- MLS Overrides needed for a user running at a level to be able to use sudo and talk to sssd
- Allow initrc_t to manage dirsrv pid files with disabled unconfined module
- Fixed for deltacloudd policy

* Wed Nov 2 2011 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-122
- Add label for imagefactory images directory
- Allow dovecot sys_nice
Resolves:#749690

* Mon Oct 31 2011 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-121
- Add support for dbomatic
Resolves: #745531

* Wed Oct 26 2011 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-120
- dhcpd needs dac_override

* Tue Oct 25 2011 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-119
- Add cloudform policy
#Resolves: #745531

* Tue Oct 18 2011 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-118
- Fix label for /root/.hushlogin
- Allow domain to send/recv unlabeled packet
- Allow sshd to relabel tun socket
- Allow puppetmasterd to relabel puppet config files
- Add label for lvs.conf
- Fix labeling for matahari-netd agents

* Thu Oct 13 2011 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-117
- Fix device interfaces
- Add label for /dev/bsr4096_* devices

* Wed Oct 12 2011 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-116
- Interfaces fixes
- Allow dirsrv to use PAM
- Fix matahari labeling

* Wed Oct 5 2011 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-115
- Add unlabelednet policy module
- Add chrome role for xguest
- Fix for vdagent policy
- Add fix to allow confined apps to execmod on chrome

* Thu Sep 29 2011 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-114
- Fix httpd_selinux man page
- Add corenet_packet() interface
- Add support for Clustered Samba commands

* Wed Sep 21 2011 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-113
- Fix execmem_execmod() interface
Resolves:#739618

* Tue Sep 20 2011 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-112
- Fix description of allow_* booleans
- Allow sanlock to manage libvirt lib files
- Fix bug in lsassd policy
- Add label for /var/run/luci
- move port 18001 from http_port_t to jboss_management_port_t

* Fri Sep 16 2011 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-111
- Add git_cgit_read_gitosis_content boolean
- Add support for cma port
- Add virt_use_sanlock boolean and make sanlock working together libvirt
- Make passenger and puppet working together

* Thu Sep 8 2011 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-110
- Add label for passwd.adjunct
- Allow pulse to execute  /usr/sbin/fos
- Fix labeling for passenger
- Add selinux policy support for IP-in-SSH tunnelling
- Allow sulogin to write /dev/pts/0 in single user mode

* Wed Aug 31 2011 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-109
- Add abrt man page
- Make internal-sftpd working
- Fixes for cluster 

* Wed Aug 24 2011 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-108
- Add squid man page
- Add git man page
- Make puppet working with passenger
- Allow procmail to execute hostname command

* Thu Aug 11 2011 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-107
- Make new domains as unconfined
- Add abrt_handle_event_t domain for ABRT event script
- Add selinux_mysql man page
- Fix httpd selinux man page
- Fix interfaces

* Tue Aug 2 2011 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-106
- Add ctdbd, uuidd, sblim policies

* Tue Jul 26 2011 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-105
- Add zarafa, drbd, fcoemon, lldpad policies

* Wed Jul 20 2011 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-104
- Allow puppet to Check access to the passwd executable
- Add label for /var/www/html/logs directory
- Add label for /var/lib/squeezeboxserver directory
- Allow rgmanager executes init script files in initrc_t domain which ensure proper transitions

* Thu Jul 14 2011 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-103
- Fixes in postfix policy

* Thu Jun 30 2011 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-102
- Add rhsmcertd policy

* Wed Jun 29 2011 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-101
- Add sanlock and wdmd policy
- Allow syslogd ipc_lock

* Mon Jun 20 2011 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-100
- More fixes for rhev-agentd

* Fri Jun 17 2011 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-99
- Add mta_user_agent attribute
  * Needed for libra

* Fri Jun 10 2011 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-98
- Fix for OpenShift

* Mon Jun 6 2011 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-97
- Allow postfix-pickup to write files and directories regardless of their MCS category set.
- Make xinetd trusted to write outbound packets regardless of the network's or node's MLS range
Resolves: #705772

* Thu May 26 2011 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-96
- Add rhev policy
- Make vhostd device MLS trusted

* Tue May 24 2011 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-95
- Allow secadm to manage selinux config files
- Allow apache to use jboss management port
- Add fenced_can_ssh boolean

* Thu May 12 2011 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-94
- Fixes for libra

* Fri Apr 29 2011 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-93
- Make init_t MLS trusted for reading/writing from/to sockets at any level

* Wed Apr 27 2011 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-92
- Fix virt_admin interface

* Wed Apr 27 2011 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-91
- Allow netlabel_mgmt_t to use all terms

* Wed Apr 27 2011 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-90
- Add label for /dev/hpilo directory
- Fix label for /var/cache/libvirt

* Tue Apr 26 2011 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-89
- More fixes for aide 

* Tue Apr 26 2011 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-88
- Aide policy does not handle MLS mode well
- Make netlabelctl working in MLS

* Wed Apr 20 2011 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-87
- Allow $1_sudo_t to read default SELinux context
- Allow tgtd to create a sock file
- Allow initrc_t to manage faillock

* Tue Apr 19 2011 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-86
- Allow squid to manage krb5_host_rcache_t files

* Wed Apr 13 2011 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-85
- Allow unconfined to run libvirt in virtd_t domain
- Make foghorn unconfined domain

* Mon Apr 11 2011 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-84
- Allow foghorn to read usr files

* Fri Apr 8 2011 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-83
- Add label for matahari-broker.pid file
- Allow foghor to read snmp lib files
- Make sysadm security admin
- Fix ssh_sysadm_login boolean
Resolves: #694551 

* Wed Apr 6 2011 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-82
- Allow ssh_keygen_t read and write a user TTYs and PTYs

* Tue Apr 5 2011 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-81
- Add allow_sysadm_manage_security boolean
- Add label for /dev/dlm.*
- Allow auditadm_screen_t and secadm_screen_t dac_override capability
- SSH_USE_STRONG_RNG is 1 which requires /dev/random
- Fix auth_rw_faillog definition
- Fixes for nslcd policy
Resolves: #693368
- Allow qpidd to manage pid and lib matahari files
- Allow rgmanager to send the kill signal to all users

* Fri Mar 25 2011 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-80
- Add support for a new cluster service - foghorn
- sssd needs to read ~/.k5login in nfs, cifs or fusefs file systems
- sssd wants to read .k5login file in users homedir
- Add support for vdsm
- Allow syslogd setrlimit, sys_nice
Resolves: #689431
- ipsec_mgmt_t wants to cause ipsec_t to dump core, needs to be allowed

* Thu Mar 17 2011 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-79
- Fixes for sandbox/seunshare policy 
Resolves:#684919
- Allow ssh_keygen_t dac_override
- Add matahari policy 
- Add label for /etc/securetty 
- Fixes for pirahna-pulse policy
- Fixes for radius, samba, dirsrv, kerberos policies 
- Allow console login on MLS
- Fix file context to show several labels as SystemHigh
- Add port definition for dogtag, matahari, movaz ports 

* Thu Mar 10 2011 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-78
- Change context for /var/run/faillock

* Wed Mar 9 2011 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-77
- Add spice fixes
- Add label for /dev/hpilo/*

* Tue Mar 8 2011 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-76
- Fixes for ssh_keygen policy
- Allow sysadm_t to run ssh-keygen in ssh_keygen_t domain
- Backport spice vdagent policy

* Fri Mar 4 2011 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-75
- Allow svirt to manage sock_file in ~/.libvirt directory
- Allow sysamd to run udev in udev_t domain
- Remove capability from svirt
- Add lvm_exec_t label for kpartx

* Tue Mar 1 2011 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-74
- Add virt_home_ type files located in ~/.libvirt directory
- virt creates monitor sockets in the users home dir
- Allow lvm setfscreate
Resolves: #680388
- Make lsusb and lsblk working on MLS
Resolves: #680426

* Thu Feb 24 2011 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-73
- Fix spec file
- Fix for policykit
Resolves: #678044

* Tue Feb 22 2011 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-72
- Fix for cmirrord
Resolves: #676664
- Add mcsnetwrite attribute

* Thu Feb 17 2011 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-71
- Allow cmirrord to create physical disk devices in /dev
#Resolves: #676664
- Allow cluster domains to use the system bus and send each other dbus messages
- Add label for /dev/tgt

* Tue Feb 8 2011 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-70
- Make screen working for sysadm_u
Resolves: #669439

* Mon Feb 7 2011 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-69
- Make Spacewalk to work with selinux-policy
Resolves: #673112
- Fix /root/.ssh labeling
Resolves: #637109	
- Fix for the spec file

* Mon Jan 24 2011 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-68
- Other fixes for namespace policy
#Resolves: #669439

* Thu Jan 20 2011 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-67
- Treat irpinit, iprupdate, iprdump services with raid policy
Resolves: #669402

* Wed Jan 19 2011 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-66
- Fixes for newrole related with namespace.init
#Resolves: #669439

* Tue Jan 18 2011 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-65
- Allow newrole to run namespace_init
#Resolves: #669439

* Fri Jan 14 2011 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-64
- Add namespace policy
- Allow udev to stream connect to init
Resolves: #667370
- Update for screen policy to handle pipe in homedir
- Fixes for polyinstatiated homedir

* Mon Jan 10 2011 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-63
- Make kernel_t domain MLS trusted for lowering the level of files
#Resolves: #667370

* Wed Dec 22 2010 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-62
- Allow apache to read cobbler lib files
Resolves: #658410

* Tue Dec 21 2010 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-61
- Fixes for passenger policy
- Allow user_t to conditionally transition to ping_t and traceroute_t
Resolves: #663054

* Mon Dec 20 2010 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-60
- Fixes for certmonger
- Backport passenger policy
- Allow run_init to read console_device
Resolves: #657568
- Add label for /var/lib/dkim-milter
- Fixes for munin policy

* Thu Dec 9 2010 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-59
- Allow cdrecord setrlimiit
Resolves: #615731
- Define debugfs_t as mountpoint
Resolves: #646856
- Fix fenced_can_network_connect boolean description
Resolves: #650136
- Add label for /var/run/faillock
- Add dirsrv and dirsrv-admin policy
Resolves: #655206
- Fixes for cobbler policy
#Resolves: #658410
- Allow certmonger to manage dirsrv config
Resolves: #658591

* Wed Oct 26 2010 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-58
- Fix httpd_setrlimit boolean to allow sys_resource capability
- Fix label for ip6tables.save
- Allow ssh_t to exec ssh_exec_t
- Dontaudit init leaks
Resolves: #639083

* Wed Oct 13 2010 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-57
- Allow system_mail_t to append ~/dead.letter
- Allow mount to communicate with gfs_controld
Resolves: #636683
- Dontaudit hal leaks in setfiles
- gpm needs to use the user terminal

* Wed Oct 6 2010 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-56
- Allow smartd to read usr files
- Allow devicekit-power transition to dhcpc
- Add label for /etc/timezone
- Remove transition from unconfined_t to iptables_t
- Allow domains with different mcs levels to send each other signals as long as they are not identified as mcsconstrainproc
Resolves: #634945
- Allow nrpe to send signal and sigkill to the plugins
- Fix up xguest to allow it to read hwdata and gconf_etc_t

* Thu Sep 16 2010 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-55
- Add cluster_var_lib_t type and label for /var/lib/cluster
- Add labeling for /root/.debug
- Remove permissive from cmirrord domain
- Dontaudit cmirrord_t sys_tty_config capability
- Allow virtd to read from processes up to its clearance
- Allow dovecot-deliver to create tmp files
- Allow tor to send signals to itself
- Handle /var/db/sudo
- Remove allow_corosync_rw_tmpfs boolean
Resolves: #631564


* Thu Sep 2 2010 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-54
- Allow clmvd to create tmpfs files
Resolves: #629391
Resolves: #594833

* Wed Sep 1 2010 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-53
- Fixes for jabberd policy
- Fixes for sandbox policy

* Mon Aug 30 2010 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-52
- Fix label for /bin/mountpoint 
- Allow fsadm to read virt blk image files

* Wed Aug 25 2010 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-51
- Allow seunshare fowner capability
- Allow dovecot to manage postfix privet socket

* Tue Aug 24 2010 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-50
- Fixes for boinc policy
- Fixes for shorewall policy

* Fri Aug 20 2010 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-49
- Add label for /var/cache/rpcbind directory
- Add chrome_role for xguest
- Fix amavis_read_spool_files interface

* Wed Aug 18 2010 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-48
- Fixes for shorewall policy
- Allow sssd chown capability
- Fix label for /usr/bin/mutter
- Label dead.letter as mail_home_t
- Allow pcscd to read  hardware state information 
- Fixes for ulogd policy

* Fri Aug 13 2010 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-47
- Fixes for boinc-project policy
- Allow swat to read nmbd pid file
- Allow fail2ban to read BIND log files
- Fix cert handling from Dan 
- Remove transition from unconfined to ncftool domain

* Wed Aug 11 2010 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-46
- Allow ipsec-mgmt to dbus chat with unconfined
- Fixes for boinc policy

* Tue Aug 10 2010 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-45
- Fixes for cgroup policy
- Fixes for ncftool policy
- Add ncftool_read_user_content boolean
- Fix label for boinc init script
- Fix label for fence_tool
- Allow vhostmd to write virt content
- Allow ricci domtrans ot shutdown

* Thu Aug 5 2010 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-44
- Add support for luci
- Add label for /var/spool/up2date

* Wed Aug 4 2010 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-43
- Allow ncftool to run brctl
- Fixes for ricci-modclusterd policy
- Allow uucpd to execute ssh client
- Add label for dayplanner
- Allow sandbox_xserver execstack

* Mon Aug 2 2010 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-42
- Allow kdump to read information from the debugging filesystem
- Update boinc policy
- Fixes for logwatch-mail policy

* Tue Jul 27 2010 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-41
- Allow logwatch_mail to read read the networking state information.
- Add label for /usr/bin/dosbox
- Allow systat sys_admin capability

* Fri Jul 23 2010 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-40
- Fixes for puppetmaster
- Fix label for kadmin init script
- Fixes for logwatch-mail policy
- Allow arpwatch to request the kernel to load modules
- Allow cron jobs to run with context of user that started them

* Wed Jul 21 2010 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-39
- Allow munin_system_plugin to read files in /usr
- Do not audit insmod attempts to write virt daemon unnamed pipes
- Allow corosync to read ricci lib files

* Mon Jul 19 2010 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-38
- Allow xdm_t to manage gnome homedir content
- Allow s-c-firewall to read and write virtual memory sysctls
- Fixes for logwatch policy

* Wed Jul 14 2010 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-37
- Redefine hi_reserved_port_t to include ports from 512 to 599 
- Add label for /sbin/sushell
- Fixes for munin plugin policy

* Tue Jul 13 2010 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-36
- Allow netutils to read and write USB monitor devices
- Fix label for /rhev
- Add user_setrlimit boolean
- Allow initrc to manage virt lib files
- Add support for ebtables
- Add label for /bin/mksh
- Dontaudit aiccu sys_tty_config capability
- Add httpd_setrlimit boolean

* Fri Jul 9 2010 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-35
- Add label for /bin/yash
- Fixes for rhcs and corosync policy
- Fixes for piranha-web policy

* Thu Jul 1 2010 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-34
- Fix ipsec-mgmt inteface

* Wed Jun 30 2010 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-33
- Fix label for /var/lib/git
- Fix labels for conflicted files
- Fix cgroup_admin interface

* Mon Jun 28 2010 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-32
- Allow sectool to connect to users over unix stream socket
- Add label for /var/spool/abrt-upload
- Add audio_home_t type for homedir/Music files
- Allow aiccu to read network config files
- Allow qpidd to setsched
- Allow virt domains to manage svirt_image_t fifo files
- Fixes for NM-openswan
- Fixes for admin interfaces

* Mon Jun 21 2010 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-31
- Remove daemons dontaudit to search all dirs 
- Add support for epylog
- All all domains to read lib files
- Allow denyhosts to send syslog messages
- Allow mysql-safe setrlimit
- Allow rpm to execute rpm_tmp_t
- Allow dmesg to appen abrt_var_cache files
- Fixed label for abrt.socket

* Wed Jun 16 2010 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-30
- Allow sysadm to run ncftool
- Fixes for cobbler policy
- Allow Network Manager to transition to ipsec_mgmt domain
- Add label for /usr/libexec/nm-openswan-service
- Add label for /dev

* Tue Jun 15 2010 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-29
- Allow abrt sigkill
- Add ncftool policy
- Add cluster fixes
- Fixes for audisp-remote

* Mon Jun 14 2010 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-28
- Fixes for netutils
- Cleanup of aiccu policy
- Add mpd policy

* Wed Jun 9 2010 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-27
- Allow ftpd ipc_lock capability
- Allow audisp-remote to getcap and setcap
- Allow iscsid to read and write raw memory devices
- Fixes for bitlbee policy

* Wed Jun 9 2010 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-26
- Allow krb5kdc to write krb5kdc_principal_t file
- Allow hald to send generic signal to dhcp client
- Fix dev_rw_vhost interface
- Add /var/run/abrt.socket label

* Tue Jun 8 2010 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-25
- Fixes for cmirrord policy
- Dontaudit xauth to list inotifyfs filesystem.
- Allow xserver to translate contexts.
- Allow kdumpgui domain sys_admin capability
- Allow vpnc to relabelfrom tun_socket
- Allow prelink_cron_system_t to signal
- Fixes for gitolite
- Allow virt domain to read symbolic links in device directories

* Thu Jun 3 2010 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-24
- Add support for /dev/vhost-net
- Allow psad to read files in /usr
- Allow systat to use nscd socket
- Fixes for boinc policy

* Tue Jun 1 2010 Miroslav Grepl <mgrepl@redhat.com> 3.7.19-23
- Add cmirrord policy
- Fixes for accountsd policy
- Fixes for boinc policy
- Allow cups-pdf to set attributes on fonts cache directory
- Allow radiusd to setrlimit
- Allow nscd sys_ptrace capability

* Tue May 25 2010 Dan Walsh <dwalsh@redhat.com> 3.7.19-22
- Allow procmail to execute scripts in the users home dir that are labeled home_bin_t
- Fix /var/run/abrtd.lock label

* Mon May 24 2010 Dan Walsh <dwalsh@redhat.com> 3.7.19-21
- Allow login programs to read krb5_home_t
Resolves: 594833
- Add obsoletes for cachefilesfd-selinux package
Resolves: #575084

* Thu May 20 2010 Dan Walsh <dwalsh@redhat.com> 3.7.19-20
- Allow mount to r/w abrt fifo file
- Allow svirt_t to getattr on hugetlbfs
- Allow abrt to create a directory under /var/spool

* Wed May 19 2010 Dan Walsh <dwalsh@redhat.com> 3.7.19-19
- Add labels for /sys
- Allow sshd to getattr on shutdown
- Fixes for munin
- Allow sssd to use the kernel key ring
- Allow tor to send syslog messages
- Allow iptabels to read usr files
- allow policykit to read all domains state

* Thu May 13 2010 Dan Walsh <dwalsh@redhat.com> 3.7.19-17
- Fix path for /var/spool/abrt
- Allow nfs_t as an entrypoint for http_sys_script_t
- Add policy for piranha
- Lots of fixes for sosreport

* Wed May 12 2010 Dan Walsh <dwalsh@redhat.com> 3.7.19-16
- Allow xm_t to read network state and get and set capabilities
- Allow policykit to getattr all processes
- Allow denyhosts to connect to tcp port 9911
- Allow pyranha to use raw ip sockets and ptrace itself
- Allow unconfined_execmem_t and gconfsd mechanism to dbus
- Allow staff to kill ping process
- Add additional MLS rules

* Mon May 10 2010 Dan Walsh <dwalsh@redhat.com> 3.7.19-15
- Allow gdm to edit ~/.gconf dir
Resolves: #590677
- Allow dovecot to create directories in /var/lib/dovecot
Partially resolves 590224
- Allow avahi to dbus chat with NetworkManager
- Fix cobbler labels
- Dontaudit iceauth_t leaks
- fix /var/lib/lxdm file context
- Allow aiccu to use tun tap devices
- Dontaudit shutdown using xserver.log

* Fri May 6 2010 Dan Walsh <dwalsh@redhat.com> 3.7.19-14
- Fixes for sandbox_x_net_t  to match access for sandbox_web_t ++
- Add xdm_etc_t for /etc/gdm directory, allow accountsd to manage this directory
- Add dontaudit interface for bluetooth dbus
- Add chronyd_read_keys, append_keys for initrc_t
- Add log support for ksmtuned
Resolves: #586663

* Thu May 6 2010 Dan Walsh <dwalsh@redhat.com> 3.7.19-13
- Allow boinc to send mail

* Wed May 5 2010 Dan Walsh <dwalsh@redhat.com> 3.7.19-12
- Allow initrc_t to remove dhcpc_state_t
- Fix label on sa-update.cron
- Allow dhcpc to restart chrony initrc
- Don't allow sandbox to send signals to its parent processes
- Fix transition from unconfined_t -> unconfined_mount_t -> rpcd_t
Resolves: #589136

* Mon May 3 2010 Dan Walsh <dwalsh@redhat.com> 3.7.19-11
- Fix location of oddjob_mkhomedir
Resolves: #587385
- fix labeling on /root/.shosts and ~/.shosts
- Allow ipsec_mgmt_t to manage net_conf_t
Resolves: #586760

* Fri Apr 30 2010 Dan Walsh <dwalsh@redhat.com> 3.7.19-10
- Dontaudit sandbox trying to connect to netlink sockets
Resolves: #587609
- Add policy for piranha

* Thu Apr 29 2010 Dan Walsh <dwalsh@redhat.com> 3.7.19-9
- Fixups for xguest policy
- Fixes for running sandbox firefox

* Wed Apr 28 2010 Dan Walsh <dwalsh@redhat.com> 3.7.19-8
- Allow ksmtuned to use terminals
Resolves: #586663
- Allow lircd to write to generic usb devices

* Tue Apr 27 2010 Dan Walsh <dwalsh@redhat.com> 3.7.19-7
- Allow sandbox_xserver to connectto unconfined stream
Resolves: #585171

* Mon Apr 26 2010 Dan Walsh <dwalsh@redhat.com> 3.7.19-6
- Allow initrc_t to read slapd_db_t
Resolves: #585476
- Allow ipsec_mgmt to use unallocated devpts and to create /etc/resolv.conf
Resolves: #585963

* Thu Apr 22 2010 Dan Walsh <dwalsh@redhat.com> 3.7.19-5
- Allow rlogind_t to search /root for .rhosts
Resolves: #582760
- Fix path for cached_var_t
- Fix prelink paths /var/lib/prelink	
- Allow confined users to direct_dri
- Allow mls lvm/cryptosetup to work

* Wed Apr 21 2010 Dan Walsh <dwalsh@redhat.com> 3.7.19-4
- Allow virtd_t to manage firewall/iptables config
Resolves: #573585

* Tue Apr 20 2010 Dan Walsh <dwalsh@redhat.com> 3.7.19-3
- Fix label on /root/.rhosts
Resolves: #582760
- Add labels for Picasa
- Allow openvpn to read home certs
- Allow plymouthd_t to use tty_device_t
- Run ncftool as iptables_t
- Allow mount to unmount unlabeled_t
- Dontaudit hal leaks

* Wed Apr 14 2010 Dan Walsh <dwalsh@redhat.com> 3.7.19-2
- Allow livecd to transition to mount

* Tue Apr 13 2010 Dan Walsh <dwalsh@redhat.com> 3.7.19-1
- Update to upstream
- Allow abrt to delete sosreport
Resolves: #579998
- Allow snmp to setuid and gid
Resolves: #582155
- Allow smartd to use generic scsi devices
Resolves: #582145

* Tue Apr 13 2010 Dan Walsh <dwalsh@redhat.com> 3.7.18-3
- Allow ipsec_t to create /etc/resolv.conf with the correct label
- Fix reserved port destination
- Allow autofs to transition to showmount
- Stop crashing tuned

* Mon Apr 12 2010 Dan Walsh <dwalsh@redhat.com> 3.7.18-2
- Add telepathysofiasip policy

* Mon Apr 5 2010 Dan Walsh <dwalsh@redhat.com> 3.7.18-1
- Update to upstream
- Fix label for  /opt/google/chrome/chrome-sandbox
- Allow modemmanager to dbus with policykit

* Mon Apr 5 2010 Dan Walsh <dwalsh@redhat.com> 3.7.17-6
- Fix allow_httpd_mod_auth_pam to use 	auth_use_pam(httpd_t)
- Allow accountsd to read shadow file
- Allow apache to send audit messages when using pam
- Allow asterisk to bind and connect to sip tcp ports
- Fixes for dovecot 2.0
- Allow initrc_t to setattr on milter directories
- Add procmail_home_t for .procmailrc file


* Thu Apr 1 2010 Dan Walsh <dwalsh@redhat.com> 3.7.17-5
- Fixes for labels during install from livecd

* Thu Apr 1 2010 Dan Walsh <dwalsh@redhat.com> 3.7.17-4
- Fix /cgroup file context 
- Fix broken afs use of unlabled_t
- Allow getty to use the console for s390

* Wed Mar 31 2010 Dan Walsh <dwalsh@redhat.com> 3.7.17-3
- Fix cgroup handling adding policy for /cgroup
- Allow confined users to write to generic usb devices, if user_rw_noexattrfile boolean set

* Tue Mar 30 2010 Dan Walsh <dwalsh@redhat.com> 3.7.17-2
- Merge patches from dgrift

* Mon Mar 29 2010 Dan Walsh <dwalsh@redhat.com> 3.7.17-1
- Update upstream
- Allow abrt to write to the /proc under any process

* Fri Mar 26 2010 Dan Walsh <dwalsh@redhat.com> 3.7.16-2
  - Fix ~/.fontconfig label
- Add /root/.cert label
- Allow reading of the fixed_file_disk_t:lnk_file if you can read file
- Allow qemu_exec_t as an entrypoint to svirt_t

* Tue Mar 23 2010 Dan Walsh <dwalsh@redhat.com> 3.7.16-1
- Update to upstream
- Allow tmpreaper to delete sandbox sock files
- Allow chrome-sandbox_t to use /dev/zero, and dontaudit getattr file systems
- Fixes for gitosis
- No transition on livecd to passwd or chfn
- Fixes for denyhosts

* Tue Mar 23 2010 Dan Walsh <dwalsh@redhat.com> 3.7.15-4
- Add label for /var/lib/upower
- Allow logrotate to run sssd
- dontaudit readahead on tmpfs blk files
- Allow tmpreaper to setattr on sandbox files
- Allow confined users to execute dos files
- Allow sysadm_t to kill processes running within its clearance
- Add accountsd policy
- Fixes for corosync policy
- Fixes from crontab policy
- Allow svirt to manage svirt_image_t chr files
- Fixes for qdisk policy
- Fixes for sssd policy
- Fixes for newrole policy

* Thu Mar 18 2010 Dan Walsh <dwalsh@redhat.com> 3.7.15-3
- make libvirt work on an MLS platform

* Thu Mar 18 2010 Dan Walsh <dwalsh@redhat.com> 3.7.15-2
- Add qpidd policy

* Thu Mar 18 2010 Dan Walsh <dwalsh@redhat.com> 3.7.15-1
- Update to upstream

* Tue Mar 16 2010 Dan Walsh <dwalsh@redhat.com> 3.7.14-5
- Allow boinc to read kernel sysctl
- Fix snmp port definitions
- Allow apache to read anon_inodefs

* Sun Mar 14 2010 Dan Walsh <dwalsh@redhat.com> 3.7.14-4
- Allow shutdown dac_override

* Sat Mar 13 2010 Dan Walsh <dwalsh@redhat.com> 3.7.14-3
- Add device_t as a file system
- Fix sysfs association

* Fri Mar 12 2010 Dan Walsh <dwalsh@redhat.com> 3.7.14-2
- Dontaudit ipsec_mgmt sys_ptrace
- Allow at to mail its spool files
- Allow nsplugin to search in .pulse directory

* Fri Mar 12 2010 Dan Walsh <dwalsh@redhat.com> 3.7.14-1
- Update to upstream

* Fri Mar 12 2010 Dan Walsh <dwalsh@redhat.com> 3.7.13-4
- Allow users to dbus chat with xdm
- Allow users to r/w wireless_device_t
- Dontaudit reading of process states by ipsec_mgmt

* Thu Mar 11 2010 Dan Walsh <dwalsh@redhat.com> 3.7.13-3
- Fix openoffice from unconfined_t

* Wed Mar 10 2010 Dan Walsh <dwalsh@redhat.com> 3.7.13-2
- Add shutdown policy so consolekit can shutdown system

* Tue Mar 9 2010 Dan Walsh <dwalsh@redhat.com> 3.7.13-1
- Update to upstream

* Thu Mar 4 2010 Dan Walsh <dwalsh@redhat.com> 3.7.12-1
- Update to upstream

* Thu Mar 4 2010 Dan Walsh <dwalsh@redhat.com> 3.7.11-1
- Update to upstream - These are merges of my patches
- Remove 389 labeling conflicts
- Add MLS fixes found in RHEL6 testing
- Allow pulseaudio to run as a service
- Add label for mssql and allow apache to connect to this database port if boolean set
- Dontaudit searches of debugfs mount point
- Allow policykit_auth to send signals to itself
- Allow modcluster to call getpwnam
- Allow swat to signal winbind
- Allow usbmux to run as a system role
- Allow svirt to create and use devpts

* Mon Mar 1 2010 Dan Walsh <dwalsh@redhat.com> 3.7.10-5
- Add MLS fixes found in RHEL6 testing
- Allow domains to append to rpm_tmp_t
- Add cachefilesfd policy
- Dontaudit leaks when transitioning

* Wed Feb 23 2010 Dan Walsh <dwalsh@redhat.com> 3.7.10-4
- Change allow_execstack and allow_execmem booleans to on
- dontaudit acct using console
- Add label for fping
- Allow tmpreaper to delete sandbox_file_t
- Fix wine dontaudit mmap_zero
- Allow abrt to read var_t symlinks

* Tue Feb 22 2010 Dan Walsh <dwalsh@redhat.com> 3.7.10-3
- Additional policy for rgmanager

* Mon Feb 22 2010 Dan Walsh <dwalsh@redhat.com> 3.7.10-2
- Allow sshd to setattr on pseudo terms

* Mon Feb 22 2010 Dan Walsh <dwalsh@redhat.com> 3.7.10-1
- Update to upstream

* Thu Feb 18 2010 Dan Walsh <dwalsh@redhat.com> 3.7.9-4
- Allow policykit to send itself signals

* Wed Feb 17 2010 Dan Walsh <dwalsh@redhat.com> 3.7.9-3
- Fix duplicate cobbler definition

* Wed Feb 17 2010 Dan Walsh <dwalsh@redhat.com> 3.7.9-2
- Fix file context of /var/lib/avahi-autoipd

* Fri Feb 12 2010 Dan Walsh <dwalsh@redhat.com> 3.7.9-1
- Merge with upstream

* Thu Feb 11 2010 Dan Walsh <dwalsh@redhat.com> 3.7.8-11
- Allow sandbox to work with MLS 

* Tue Feb 9 2010 Dan Walsh <dwalsh@redhat.com> 3.7.8-9
- Make Chrome work with staff user

* Thu Feb 4 2010 Dan Walsh <dwalsh@redhat.com> 3.7.8-8
- Add icecast policy
- Cleanup  spec file

* Wed Feb 3 2010 Dan Walsh <dwalsh@redhat.com> 3.7.8-7
- Add mcelog policy

* Mon Feb 1 2010 Dan Walsh <dwalsh@redhat.com> 3.7.8-6
- Lots of fixes found in F12

* Thu Jan 27 2010 Dan Walsh <dwalsh@redhat.com> 3.7.8-5
- Fix rpm_dontaudit_leaks

* Wed Jan 27 2010 Dan Walsh <dwalsh@redhat.com> 3.7.8-4
- Add getsched to hald_t
- Add file context for Fedora/Redhat Directory Server

* Mon Jan 25 2010 Dan Walsh <dwalsh@redhat.com> 3.7.8-3
- Allow abrt_helper to getattr on all filesystems
- Add label for /opt/real/RealPlayer/plugins/oggfformat\.so     

* Thu Jan 21 2010 Dan Walsh <dwalsh@redhat.com> 3.7.8-2
- Add gstreamer_home_t for ~/.gstreamer

* Mon Jan 18 2010 Dan Walsh <dwalsh@redhat.com> 3.7.8-1
- Update to upstream

* Fri Jan 15 2010 Dan Walsh <dwalsh@redhat.com> 3.7.7-3
- Fix git

* Thu Jan 7 2010 Dan Walsh <dwalsh@redhat.com> 3.7.7-2
- Turn on puppet policy
- Update to dgrift git policy

* Mon Jan 7 2010 Dan Walsh <dwalsh@redhat.com> 3.7.7-1
- Move users file to selection by spec file.
- Allow vncserver to run as unconfined_u:unconfined_r:unconfined_t

* Thu Jan 7 2010 Dan Walsh <dwalsh@redhat.com> 3.7.6-1
- Update to upstream

* Wed Jan 6 2010 Dan Walsh <dwalsh@redhat.com> 3.7.5-8
- Remove most of the permissive domains from F12.

* Tue Jan 5 2010 Dan Walsh <dwalsh@redhat.com> 3.7.5-7
- Add cobbler policy from dgrift

* Mon Jan 4 2010 Dan Walsh <dwalsh@redhat.com> 3.7.5-6
- add usbmon device
- Add allow rulse for devicekit_disk

* Wed Dec 30 2009 Dan Walsh <dwalsh@redhat.com> 3.7.5-5
- Lots of fixes found in F12, fixes from Tom London

* Wed Dec 23 2009 Dan Walsh <dwalsh@redhat.com> 3.7.5-4
- Cleanups from dgrift

* Tue Dec 22 2009 Dan Walsh <dwalsh@redhat.com> 3.7.5-3
- Add back xserver_manage_home_fonts

* Mon Dec 21 2009 Dan Walsh <dwalsh@redhat.com> 3.7.5-2
- Dontaudit sandbox trying to read nscd and sssd

* Fri Dec 18 2009 Dan Walsh <dwalsh@redhat.com> 3.7.5-1
- Update to upstream

* Thu Dec 17 2009 Dan Walsh <dwalsh@redhat.com> 3.7.4-4
- Rename udisks-daemon back to devicekit_disk_t policy

* Wed Dec 16 2009 Dan Walsh <dwalsh@redhat.com> 3.7.4-3
- Fixes for abrt calls

* Fri Dec 11 2009 Dan Walsh <dwalsh@redhat.com> 3.7.4-2
- Add tgtd policy

* Fri Dec 4 2009 Dan Walsh <dwalsh@redhat.com> 3.7.4-1
- Update to upstream release

* Mon Nov 16 2009 Dan Walsh <dwalsh@redhat.com> 3.7.3-1
- Add asterisk policy back in
- Update to upstream release 2.20091117

* Mon Nov 16 2009 Dan Walsh <dwalsh@redhat.com> 3.7.1-1
- Update to upstream release 2.20091117

* Mon Nov 16 2009 Dan Walsh <dwalsh@redhat.com> 3.6.33-2
- Fixup nut policy

* Thu Nov 12 2009 Dan Walsh <dwalsh@redhat.com> 3.6.33-1
- Update to upstream

* Thu Oct 1 2009 Dan Walsh <dwalsh@redhat.com> 3.6.32-17
- Allow vpnc request the kernel to load modules

* Wed Sep 30 2009 Dan Walsh <dwalsh@redhat.com> 3.6.32-16
- Fix minimum policy installs
- Allow udev and rpcbind to request the kernel to load modules

* Wed Sep 30 2009 Dan Walsh <dwalsh@redhat.com> 3.6.32-15
- Add plymouth policy
- Allow local_login to sys_admin

* Tue Sep 29 2009 Dan Walsh <dwalsh@redhat.com> 3.6.32-13
- Allow cupsd_config to read user tmp
- Allow snmpd_t to signal itself
- Allow sysstat_t to makedir in sysstat_log_t

* Fri Sep 25 2009 Dan Walsh <dwalsh@redhat.com> 3.6.32-12
- Update rhcs policy

* Thu Sep 24 2009 Dan Walsh <dwalsh@redhat.com> 3.6.32-11
- Allow users to exec restorecond

* Tue Sep 21 2009 Dan Walsh <dwalsh@redhat.com> 3.6.32-10
- Allow sendmail to request kernel modules load

* Mon Sep 21 2009 Dan Walsh <dwalsh@redhat.com> 3.6.32-9
- Fix all kernel_request_load_module domains

* Mon Sep 21 2009 Dan Walsh <dwalsh@redhat.com> 3.6.32-8
- Fix all kernel_request_load_module domains

* Sun Sep 20 2009 Dan Walsh <dwalsh@redhat.com> 3.6.32-7
- Remove allow_exec* booleans for confined users.  Only available for unconfined_t

* Fri Sep 18 2009 Dan Walsh <dwalsh@redhat.com> 3.6.32-6
- More fixes for sandbox_web_t

* Fri Sep 18 2009 Dan Walsh <dwalsh@redhat.com> 3.6.32-5
- Allow sshd to create .ssh directory and content

* Fri Sep 18 2009 Dan Walsh <dwalsh@redhat.com> 3.6.32-4
- Fix request_module line to module_request

* Fri Sep 18 2009 Dan Walsh <dwalsh@redhat.com> 3.6.32-3
- Fix sandbox policy to allow it to run under firefox.  
- Dont audit leaks.

* Thu Sep 17 2009 Dan Walsh <dwalsh@redhat.com> 3.6.32-2
- Fixes for sandbox

* Wed Sep 17 2009 Dan Walsh <dwalsh@redhat.com> 3.6.32-1
- Update to upstream
- Dontaudit nsplugin search /root
- Dontaudit nsplugin sys_nice

* Mon Sep 15 2009 Dan Walsh <dwalsh@redhat.com> 3.6.31-5
- Fix label on /usr/bin/notepad, /usr/sbin/vboxadd-service
- Remove policycoreutils-python requirement except for minimum

* Mon Sep 14 2009 Dan Walsh <dwalsh@redhat.com> 3.6.31-4
- Fix devicekit_disk_t to getattr on all domains sockets and fifo_files
- Conflicts seedit (You can not use selinux-policy-targeted and seedit at the same time.)


* Thu Sep 10 2009 Dan Walsh <dwalsh@redhat.com> 3.6.31-3
- Add wordpress/wp-content/uploads label
- Fixes for sandbox when run from staff_t

* Thu Sep 10 2009 Dan Walsh <dwalsh@redhat.com> 3.6.31-2
- Update to upstream
- Fixes for devicekit_disk

* Tue Sep 8 2009 Dan Walsh <dwalsh@redhat.com> 3.6.30-6
- More fixes

* Tue Sep 8 2009 Dan Walsh <dwalsh@redhat.com> 3.6.30-5
- Lots of fixes for initrc and other unconfined domains

* Fri Sep 4 2009 Dan Walsh <dwalsh@redhat.com> 3.6.30-4
- Allow xserver to use  netlink_kobject_uevent_socket

* Thu Sep 3 2009 Dan Walsh <dwalsh@redhat.com> 3.6.30-3
- Fixes for sandbox 

* Mon Aug 31 2009 Dan Walsh <dwalsh@redhat.com> 3.6.30-2
- Dontaudit setroubleshootfix looking at /root directory

* Mon Aug 31 2009 Dan Walsh <dwalsh@redhat.com> 3.6.30-1
- Update to upsteam

* Mon Aug 31 2009 Dan Walsh <dwalsh@redhat.com> 3.6.29-2
- Allow gssd to send signals to users
- Fix duplicate label for apache content

* Fri Aug 28 2009 Dan Walsh <dwalsh@redhat.com> 3.6.29-1
- Update to upstream

* Fri Aug 28 2009 Dan Walsh <dwalsh@redhat.com> 3.6.28-9
- Remove polkit_auth on upgrades

* Wed Aug 26 2009 Dan Walsh <dwalsh@redhat.com> 3.6.28-8
- Add back in unconfined.pp and unconfineduser.pp
- Add Sandbox unshare

* Tue Aug 25 2009 Dan Walsh <dwalsh@redhat.com> 3.6.28-7
- Fixes for cdrecord, mdadm, and others

* Sat Aug 22 2009 Dan Walsh <dwalsh@redhat.com> 3.6.28-6
- Add capability setting to dhcpc and gpm

* Sat Aug 22 2009 Dan Walsh <dwalsh@redhat.com> 3.6.28-5
- Allow cronjobs to read exim_spool_t

* Fri Aug 21 2009 Dan Walsh <dwalsh@redhat.com> 3.6.28-4
- Add ABRT policy

* Thu Aug 20 2009 Dan Walsh <dwalsh@redhat.com> 3.6.28-3
- Fix system-config-services policy

* Wed Aug 19 2009 Dan Walsh <dwalsh@redhat.com> 3.6.28-2
- Allow libvirt to change user componant of virt_domain

* Tue Aug 18 2009 Dan Walsh <dwalsh@redhat.com> 3.6.28-1
- Allow cupsd_config_t to be started by dbus
- Add smoltclient policy

* Fri Aug 14 2009 Dan Walsh <dwalsh@redhat.com> 3.6.27-1
- Add policycoreutils-python to pre install

* Thu Aug 13 2009 Dan Walsh <dwalsh@redhat.com> 3.6.26-11
- Make all unconfined_domains permissive so we can see what AVC's happen 

* Mon Aug 10 2009 Dan Walsh <dwalsh@redhat.com> 3.6.26-10
- Add pt_chown policy

* Mon Aug 10 2009 Dan Walsh <dwalsh@redhat.com> 3.6.26-9
- Add kdump policy for Miroslav Grepl
- Turn off execstack boolean

* Fri Aug 7 2009 Bill Nottingham <notting@redhat.com> 3.6.26-8
- Turn on execstack on a temporary basis (#512845)

* Thu Aug 6 2009 Dan Walsh <dwalsh@redhat.com> 3.6.26-7
- Allow nsplugin to connecto the session bus
- Allow samba_net to write to coolkey data

* Wed Aug 5 2009 Dan Walsh <dwalsh@redhat.com> 3.6.26-6
- Allow devicekit_disk to list inotify

* Wed Aug 5 2009 Dan Walsh <dwalsh@redhat.com> 3.6.26-5
- Allow svirt images to create sock_file in svirt_var_run_t

* Tue Aug 4 2009 Dan Walsh <dwalsh@redhat.com> 3.6.26-4
- Allow exim to getattr on mountpoints
- Fixes for pulseaudio

* Fri Jul 31 2009 Dan Walsh <dwalsh@redhat.com> 3.6.26-3
- Allow svirt_t to stream_connect to virtd_t

* Fri Jul 31 2009 Dan Walsh <dwalsh@redhat.com> 3.6.26-2
- Allod hald_dccm_t to create sock_files in /tmp

* Thu Jul 30 2009 Dan Walsh <dwalsh@redhat.com> 3.6.26-1
- More fixes from upstream

* Tue Jul 28 2009 Dan Walsh <dwalsh@redhat.com> 3.6.25-1
- Fix polkit label
- Remove hidebrokensymptoms for nss_ldap fix
- Add modemmanager policy
- Lots of merges from upstream
- Begin removing textrel_shlib_t labels, from fixed libraries

* Tue Jul 28 2009 Dan Walsh <dwalsh@redhat.com> 3.6.24-1
- Update to upstream

* Mon Jul 27 2009 Dan Walsh <dwalsh@redhat.com> 3.6.23-2
- Allow certmaster to override dac permissions

* Thu Jul 22 2009 Dan Walsh <dwalsh@redhat.com> 3.6.23-1
- Update to upstream

* Tue Jul 20 2009 Dan Walsh <dwalsh@redhat.com> 3.6.22-3
- Fix context for VirtualBox

* Tue Jul 14 2009 Dan Walsh <dwalsh@redhat.com> 3.6.22-1
- Update to upstream

* Fri Jul 10 2009 Dan Walsh <dwalsh@redhat.com> 3.6.21-4
- Allow clamscan read amavis spool files

* Wed Jul 8 2009 Dan Walsh <dwalsh@redhat.com> 3.6.21-3
- Fixes for xguest

* Tue Jul  7 2009 Tom "spot" Callaway <tcallawa@redhat.com> 3.6.21-2
- fix multiple directory ownership of mandirs

* Wed Jul 1 2009 Dan Walsh <dwalsh@redhat.com> 3.6.21-1
- Update to upstream

* Tue Jun 30 2009 Dan Walsh <dwalsh@redhat.com> 3.6.20-2
- Add rules for rtkit-daemon

* Thu Jun 25 2009 Dan Walsh <dwalsh@redhat.com> 3.6.20-1
- Update to upstream
- Fix nlscd_stream_connect

* Thu Jun 25 2009 Dan Walsh <dwalsh@redhat.com> 3.6.19-5
- Add rtkit policy

* Wed Jun 24 2009 Dan Walsh <dwalsh@redhat.com> 3.6.19-4
- Allow rpcd_t to stream connect to rpcbind

* Tue Jun 23 2009 Dan Walsh <dwalsh@redhat.com> 3.6.19-3
- Allow kpropd to create tmp files

* Tue Jun 23 2009 Dan Walsh <dwalsh@redhat.com> 3.6.19-2
- Fix last duplicate /var/log/rpmpkgs

* Mon Jun 22 2009 Dan Walsh <dwalsh@redhat.com> 3.6.19-1
- Update to upstream
  * add sssd

* Sat Jun 20 2009 Dan Walsh <dwalsh@redhat.com> 3.6.18-1
- Update to upstream
  * cleanup
* Fri Jun 19 2009 Dan Walsh <dwalsh@redhat.com> 3.6.17-1
- Update to upstream
- Additional mail ports
- Add virt_use_usb boolean for svirt

* Thu Jun 18 2009 Dan Walsh <dwalsh@redhat.com> 3.6.16-4
- Fix mcs rules to include chr_file and blk_file

* Tue Jun 16 2009 Dan Walsh <dwalsh@redhat.com> 3.6.16-3
- Add label for udev-acl

* Mon Jun 15 2009 Dan Walsh <dwalsh@redhat.com> 3.6.16-2
- Additional rules for consolekit/udev, privoxy and various other fixes

* Fri Jun 12 2009 Dan Walsh <dwalsh@redhat.com> 3.6.16-1
- New version for upstream

* Thu Jun 11 2009 Dan Walsh <dwalsh@redhat.com> 3.6.14-3
- Allow NetworkManager to read inotifyfs

* Wed Jun 10 2009 Dan Walsh <dwalsh@redhat.com> 3.6.14-2
- Allow setroubleshoot to run mlocate

* Mon Jun 8 2009 Dan Walsh <dwalsh@redhat.com> 3.6.14-1
- Update to upstream 

* Tue Jun 2 2009 Dan Walsh <dwalsh@redhat.com> 3.6.13-3
- Add fish as a shell
- Allow fprintd to list usbfs_t
- Allow consolekit to search mountpoints
- Add proper labeling for shorewall

* Tue May 26 2009 Dan Walsh <dwalsh@redhat.com> 3.6.13-2
- New log file for vmware
- Allow xdm to setattr on user_tmp_t

* Thu May 21 2009 Dan Walsh <dwalsh@redhat.com> 3.6.13-1
- Upgrade to upstream

* Wed May 20 2009 Dan Walsh <dwalsh@redhat.com> 3.6.12-39
- Allow fprintd to access sys_ptrace
- Add sandbox policy

* Mon May 18 2009 Dan Walsh <dwalsh@redhat.com> 3.6.12-38
- Add varnishd policy

* Thu May 14 2009 Dan Walsh <dwalsh@redhat.com> 3.6.12-37
- Fixes for kpropd

* Tue May 12 2009 Dan Walsh <dwalsh@redhat.com> 3.6.12-36
- Allow brctl to r/w tun_tap_device_t

* Mon May 11 2009 Dan Walsh <dwalsh@redhat.com> 3.6.12-35
- Add /usr/share/selinux/packages

* Mon May 11 2009 Dan Walsh <dwalsh@redhat.com> 3.6.12-34
- Allow rpcd_t to send signals to kernel threads

* Fri May 7 2009 Dan Walsh <dwalsh@redhat.com> 3.6.12-33
- Fix upgrade for F10 to F11

* Thu May 7 2009 Dan Walsh <dwalsh@redhat.com> 3.6.12-31
- Add policy for /var/lib/fprint

* Tue May 5 2009 Dan Walsh <dwalsh@redhat.com> 3.6.12-30
-Remove duplicate line

* Tue May 5 2009 Dan Walsh <dwalsh@redhat.com> 3.6.12-29
- Allow svirt to manage pci and other sysfs device data

* Mon May 4 2009 Dan Walsh <dwalsh@redhat.com> 3.6.12-28
- Fix package selection handling

* Fri May 1 2009 Dan Walsh <dwalsh@redhat.com> 3.6.12-27
- Fix /sbin/ip6tables-save context
- Allod udev to transition to mount
- Fix loading of mls policy file

* Thu Apr 30 2009 Dan Walsh <dwalsh@redhat.com> 3.6.12-26
- Add shorewall policy

* Wed Apr 29 2009 Dan Walsh <dwalsh@redhat.com> 3.6.12-25
- Additional rules for fprintd and sssd

* Tue Apr 28 2009 Dan Walsh <dwalsh@redhat.com> 3.6.12-24
- Allow nsplugin to unix_read unix_write sem for unconfined_java

* Tue Apr 28 2009 Dan Walsh <dwalsh@redhat.com> 3.6.12-23
- Fix uml files to be owned by users

* Tue Apr 28 2009 Dan Walsh <dwalsh@redhat.com> 3.6.12-22
- Fix Upgrade path to install unconfineduser.pp when unocnfined package is 3.0.0 or less

* Mon Apr 27 2009 Dan Walsh <dwalsh@redhat.com> 3.6.12-21
- Allow confined users to manage virt_content_t, since this is home dir content
- Allow all domains to read rpm_script_tmp_t which is what shell creates on redirection

* Mon Apr 27 2009 Dan Walsh <dwalsh@redhat.com> 3.6.12-20
- Fix labeling on /var/lib/misc/prelink*
- Allow xserver to rw_shm_perms with all x_clients
- Allow prelink to execute files in the users home directory

* Fri Apr 24 2009 Dan Walsh <dwalsh@redhat.com> 3.6.12-19
- Allow initrc_t to delete dev_null
- Allow readahead to configure auditing
- Fix milter policy
- Add /var/lib/readahead

* Fri Apr 24 2009 Dan Walsh <dwalsh@redhat.com> 3.6.12-16
- Update to latest milter code from Paul Howarth

* Thu Apr 23 2009 Dan Walsh <dwalsh@redhat.com> 3.6.12-15
- Additional perms for readahead

* Thu Apr 23 2009 Dan Walsh <dwalsh@redhat.com> 3.6.12-14
- Allow pulseaudio to acquire_svc on session bus
- Fix readahead labeling

* Thu Apr 23 2009 Dan Walsh <dwalsh@redhat.com> 3.6.12-13
- Allow sysadm_t to run rpm directly
- libvirt needs fowner

* Wed Apr 22 2009 Dan Walsh <dwalsh@redhat.com> 3.6.12-12
- Allow sshd to read var_lib symlinks for freenx

* Tue Apr 21 2009 Dan Walsh <dwalsh@redhat.com> 3.6.12-11
- Allow nsplugin unix_read and write on users shm and sem
- Allow sysadm_t to execute su

* Tue Apr 21 2009 Dan Walsh <dwalsh@redhat.com> 3.6.12-10
- Dontaudit attempts to getattr user_tmpfs_t by lvm
- Allow nfs to share removable media

* Mon Apr 20 2009 Dan Walsh <dwalsh@redhat.com> 3.6.12-9
- Add ability to run postdrop from confined users

* Sat Apr 18 2009 Dan Walsh <dwalsh@redhat.com> 3.6.12-8
- Fixes for podsleuth

* Fri Apr 17 2009 Dan Walsh <dwalsh@redhat.com> 3.6.12-7
- Turn off nsplugin transition
- Remove Konsole leaked file descriptors for release

* Fri Apr 17 2009 Dan Walsh <dwalsh@redhat.com> 3.6.12-6
- Allow cupsd_t to create link files in print_spool_t
- Fix iscsi_stream_connect typo
- Fix labeling on /etc/acpi/actions
- Don't reinstall unconfine and unconfineuser on upgrade if they are not installed

* Tue Apr 14 2009 Dan Walsh <dwalsh@redhat.com> 3.6.12-5
- Allow audioentroy to read etc files

* Mon Apr 13 2009 Dan Walsh <dwalsh@redhat.com> 3.6.12-4
- Add fail2ban_var_lib_t
- Fixes for devicekit_power_t

* Thu Apr 9 2009 Dan Walsh <dwalsh@redhat.com> 3.6.12-3
- Separate out the ucnonfined user from the unconfined.pp package

* Wed Apr 7 2009 Dan Walsh <dwalsh@redhat.com> 3.6.12-2
- Make sure unconfined_java_t and unconfined_mono_t create user_tmpfs_t.

* Tue Apr 7 2009 Dan Walsh <dwalsh@redhat.com> 3.6.12-1
- Upgrade to latest upstream
- Allow devicekit_disk sys_rawio

* Mon Apr 6 2009 Dan Walsh <dwalsh@redhat.com> 3.6.11-1
- Dontaudit binds to ports < 1024 for named
- Upgrade to latest upstream

* Fri Apr 3 2009 Dan Walsh <dwalsh@redhat.com> 3.6.10-9
- Allow podsleuth to use tmpfs files

* Fri Apr 3 2009 Dan Walsh <dwalsh@redhat.com> 3.6.10-8
- Add customizable_types for svirt

* Fri Apr 3 2009 Dan Walsh <dwalsh@redhat.com> 3.6.10-7
- Allow setroubelshoot exec* privs to prevent crash from bad libraries
- add cpufreqselector

* Thu Apr 2 2009 Dan Walsh <dwalsh@redhat.com> 3.6.10-6
- Dontaudit listing of /root directory for cron system jobs

* Mon Mar 30 2009 Dan Walsh <dwalsh@redhat.com> 3.6.10-5
- Fix missing ld.so.cache label

* Fri Mar 27 2009 Dan Walsh <dwalsh@redhat.com> 3.6.10-4
- Add label for ~/.forward and /root/.forward

* Thu Mar 26 2009 Dan Walsh <dwalsh@redhat.com> 3.6.10-3
- Fixes for svirt

* Thu Mar 19 2009 Dan Walsh <dwalsh@redhat.com> 3.6.10-2
- Fixes to allow svirt read iso files in homedir

* Thu Mar 19 2009 Dan Walsh <dwalsh@redhat.com> 3.6.10-1
- Add xenner and wine fixes from mgrepl

* Wed Mar 18 2009 Dan Walsh <dwalsh@redhat.com> 3.6.9-4
- Allow mdadm to read/write mls override

* Tue Mar 17 2009 Dan Walsh <dwalsh@redhat.com> 3.6.9-3
- Change to svirt to only access svirt_image_t

* Thu Mar 12 2009 Dan Walsh <dwalsh@redhat.com> 3.6.9-2
- Fix libvirt policy

* Thu Mar 12 2009 Dan Walsh <dwalsh@redhat.com> 3.6.9-1
- Upgrade to latest upstream

* Tue Mar 10 2009 Dan Walsh <dwalsh@redhat.com> 3.6.8-4
- Fixes for iscsid and sssd
- More cleanups for upgrade from F10 to Rawhide.

* Mon Mar 9 2009 Dan Walsh <dwalsh@redhat.com> 3.6.8-3
- Add pulseaudio, sssd policy
- Allow networkmanager to exec udevadm

* Sat Mar 7 2009 Dan Walsh <dwalsh@redhat.com> 3.6.8-2
- Add pulseaudio context

* Thu Mar 4 2009 Dan Walsh <dwalsh@redhat.com> 3.6.8-1
- Upgrade to latest patches

* Wed Mar 4 2009 Dan Walsh <dwalsh@redhat.com> 3.6.7-2
- Fixes for libvirt

* Mon Mar 2 2009 Dan Walsh <dwalsh@redhat.com> 3.6.7-1
- Update to Latest upstream

* Sat Feb 28 2009 Dan Walsh <dwalsh@redhat.com> 3.6.6-9
- Fix setrans.conf to show SystemLow for s0

* Fri Feb 27 2009 Dan Walsh <dwalsh@redhat.com> 3.6.6-8
- Further confinement of qemu images via svirt

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 19 2009 Dan Walsh <dwalsh@redhat.com> 3.6.6-6
- Allow NetworkManager to manage /etc/NetworkManager/system-connections

* Wed Feb 18 2009 Dan Walsh <dwalsh@redhat.com> 3.6.6-5
- add virtual_image_context and virtual_domain_context files

* Tue Feb 17 2009 Dan Walsh <dwalsh@redhat.com> 3.6.6-4
- Allow rpcd_t to send signal to mount_t
- Allow libvirtd to run ranged

* Tue Feb 17 2009 Dan Walsh <dwalsh@redhat.com> 3.6.6-3
- Fix sysnet/net_conf_t

* Tue Feb 17 2009 Dan Walsh <dwalsh@redhat.com> 3.6.6-2
- Fix squidGuard labeling

* Wed Feb 11 2009 Dan Walsh <dwalsh@redhat.com> 3.6.6-1
- Re-add corenet_in_generic_if(unlabeled_t)

* Wed Feb 11 2009 Dan Walsh <dwalsh@redhat.com> 3.6.5-3

* Tue Feb 10 2009 Dan Walsh <dwalsh@redhat.com> 3.6.5-2
- Add git web policy

* Mon Feb 9 2009 Dan Walsh <dwalsh@redhat.com> 3.6.5-1
- Add setrans contains from upstream 

* Mon Feb 9 2009 Dan Walsh <dwalsh@redhat.com> 3.6.4-6
- Do transitions outside of the booleans

* Sun Feb 8 2009 Dan Walsh <dwalsh@redhat.com> 3.6.4-5
- Allow xdm to create user_tmp_t sockets for switch user to work

* Thu Feb 5 2009 Dan Walsh <dwalsh@redhat.com> 3.6.4-4
- Fix staff_t domain

* Thu Feb 5 2009 Dan Walsh <dwalsh@redhat.com> 3.6.4-3
- Grab remainder of network_peer_controls patch

* Wed Feb 4 2009 Dan Walsh <dwalsh@redhat.com> 3.6.4-2
- More fixes for devicekit

* Tue Feb 3 2009 Dan Walsh <dwalsh@redhat.com> 3.6.4-1
- Upgrade to latest upstream 

* Mon Feb 2 2009 Dan Walsh <dwalsh@redhat.com> 3.6.3-13
- Add boolean to disallow unconfined_t login

* Fri Jan 30 2009 Dan Walsh <dwalsh@redhat.com> 3.6.3-12
- Add back transition from xguest to mozilla

* Fri Jan 30 2009 Dan Walsh <dwalsh@redhat.com> 3.6.3-11
- Add virt_content_ro_t and labeling for isos directory

* Tue Jan 27 2009 Dan Walsh <dwalsh@redhat.com> 3.6.3-10
- Fixes for wicd daemon

* Mon Jan 26 2009 Dan Walsh <dwalsh@redhat.com> 3.6.3-9
- More mls/rpm fixes 

* Fri Jan 23 2009 Dan Walsh <dwalsh@redhat.com> 3.6.3-8
- Add policy to make dbus/nm-applet work

* Thu Jan 22 2009 Dan Walsh <dwalsh@redhat.com> 3.6.3-7
- Remove polgen-ifgen from post and add trigger to policycoreutils-python

* Wed Jan 21 2009 Dan Walsh <dwalsh@redhat.com> 3.6.3-6
- Add wm policy
- Make mls work in graphics mode

* Tue Jan 20 2009 Dan Walsh <dwalsh@redhat.com> 3.6.3-3
- Fixed for DeviceKit

* Mon Jan 19 2009 Dan Walsh <dwalsh@redhat.com> 3.6.3-2
- Add devicekit policy

* Mon Jan 19 2009 Dan Walsh <dwalsh@redhat.com> 3.6.3-1
- Update to upstream

* Thu Jan 15 2009 Dan Walsh <dwalsh@redhat.com> 3.6.2-5
- Define openoffice as an x_domain

* Mon Jan 12 2009 Dan Walsh <dwalsh@redhat.com> 3.6.2-4
- Fixes for reading xserver_tmp_t

* Thu Jan 8 2009 Dan Walsh <dwalsh@redhat.com> 3.6.2-3
- Allow cups_pdf_t write to nfs_t

* Tue Jan 6 2009 Dan Walsh <dwalsh@redhat.com> 3.6.2-2
- Remove audio_entropy policy

* Mon Jan 5 2009 Dan Walsh <dwalsh@redhat.com> 3.6.2-1
- Update to upstream

* Sun Jan 4 2009 Dan Walsh <dwalsh@redhat.com> 3.6.1-15
- Allow hal_acl_t to getattr/setattr fixed_disk

* Sat Dec 27 2008 Dan Walsh <dwalsh@redhat.com> 3.6.1-14
- Change userdom_read_all_users_state to include reading symbolic links in /proc

* Mon Dec 22 2008 Dan Walsh <dwalsh@redhat.com> 3.6.1-13
- Fix dbus reading /proc information

* Thu Dec 18 2008 Dan Walsh <dwalsh@redhat.com> 3.6.1-12
- Add missing alias for home directory content

* Wed Dec 17 2008 Dan Walsh <dwalsh@redhat.com> 3.6.1-11
- Fixes for IBM java location

* Thu Dec 11 2008 Dan Walsh <dwalsh@redhat.com> 3.6.1-10
- Allow unconfined_r unconfined_java_t

* Tue Dec 9 2008 Dan Walsh <dwalsh@redhat.com> 3.6.1-9
- Add cron_role back to user domains

* Mon Dec 8 2008 Dan Walsh <dwalsh@redhat.com> 3.6.1-8
- Fix sudo setting of user keys

* Thu Dec 4 2008 Dan Walsh <dwalsh@redhat.com> 3.6.1-7
- Allow iptables to talk to terminals
- Fixes for policy kit
- lots of fixes for booting. 

* Wed Dec 3 2008 Dan Walsh <dwalsh@redhat.com> 3.6.1-4
- Cleanup policy

* Mon Dec 01 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 3.6.1-2
- Rebuild for Python 2.6

* Fri Nov 5 2008 Dan Walsh <dwalsh@redhat.com> 3.5.13-19
- Fix labeling on /var/spool/rsyslog

* Thu Nov 5 2008 Dan Walsh <dwalsh@redhat.com> 3.5.13-18
- Allow postgresl to bind to udp nodes

* Wed Nov 5 2008 Dan Walsh <dwalsh@redhat.com> 3.5.13-17
- Allow lvm to dbus chat with hal
- Allow rlogind to read nfs_t 

* Wed Nov 5 2008 Dan Walsh <dwalsh@redhat.com> 3.5.13-16
- Fix cyphesis file context

* Tue Nov 3 2008 Dan Walsh <dwalsh@redhat.com> 3.5.13-15
- Allow hal/pm-utils to look at /var/run/video.rom
- Add ulogd policy

* Tue Nov 3 2008 Dan Walsh <dwalsh@redhat.com> 3.5.13-14
- Additional fixes for cyphesis
- Fix certmaster file context
- Add policy for system-config-samba
- Allow hal to read /var/run/video.rom

* Mon Nov 3 2008 Dan Walsh <dwalsh@redhat.com> 3.5.13-13
- Allow dhcpc to restart ypbind
- Fixup labeling in /var/run

* Thu Oct 30 2008 Dan Walsh <dwalsh@redhat.com> 3.5.13-12
- Add certmaster policy

* Wed Oct 29 2008 Dan Walsh <dwalsh@redhat.com> 3.5.13-11
- Fix confined users 
- Allow xguest to read/write xguest_dbusd_t

* Mon Oct 27 2008 Dan Walsh <dwalsh@redhat.com> 3.5.13-9
- Allow openoffice execstack/execmem privs

* Fri Oct 24 2008 Dan Walsh <dwalsh@redhat.com> 3.5.13-8
- Allow mozilla to run with unconfined_execmem_t

* Thu Oct 23 2008 Dan Walsh <dwalsh@redhat.com> 3.5.13-7
- Dontaudit domains trying to write to .xsession-errors

* Thu Oct 23 2008 Dan Walsh <dwalsh@redhat.com> 3.5.13-6
- Allow nsplugin to look at autofs_t directory

* Wed Oct 22 2008 Dan Walsh <dwalsh@redhat.com> 3.5.13-5
- Allow kerneloops to create tmp files

* Wed Oct 22 2008 Dan Walsh <dwalsh@redhat.com> 3.5.13-4
- More alias for fastcgi

* Tue Oct 21 2008 Dan Walsh <dwalsh@redhat.com> 3.5.13-3
- Remove mod_fcgid-selinux package

* Mon Oct 20 2008 Dan Walsh <dwalsh@redhat.com> 3.5.13-2
- Fix dovecot access

* Fri Oct 17 2008 Dan Walsh <dwalsh@redhat.com> 3.5.13-1
- Policy cleanup 

* Thu Oct 16 2008 Dan Walsh <dwalsh@redhat.com> 3.5.12-3
- Remove Multiple spec
- Add include
- Fix makefile to not call per_role_expansion

* Wed Oct 15 2008 Dan Walsh <dwalsh@redhat.com> 3.5.12-2
- Fix labeling of libGL

* Fri Oct 10 2008 Dan Walsh <dwalsh@redhat.com> 3.5.12-1
- Update to upstream

* Wed Oct 8 2008 Dan Walsh <dwalsh@redhat.com> 3.5.11-1
- Update to upstream policy

* Mon Oct 6 2008 Dan Walsh <dwalsh@redhat.com> 3.5.10-3
- Fixes for confined xwindows and xdm_t 

* Fri Oct 3 2008 Dan Walsh <dwalsh@redhat.com> 3.5.10-2
- Allow confined users and xdm to exec wm
- Allow nsplugin to talk to fifo files on nfs

* Fri Oct 3 2008 Dan Walsh <dwalsh@redhat.com> 3.5.10-1
- Allow NetworkManager to transition to avahi and iptables
- Allow domains to search other domains keys, coverup kernel bug

* Wed Oct 1 2008 Dan Walsh <dwalsh@redhat.com> 3.5.9-4
- Fix labeling for oracle 

* Wed Oct 1 2008 Dan Walsh <dwalsh@redhat.com> 3.5.9-3
- Allow nsplugin to comminicate with xdm_tmp_t sock_file

* Mon Sep 29 2008 Dan Walsh <dwalsh@redhat.com> 3.5.9-2
- Change all user tmpfs_t files to be labeled user_tmpfs_t
- Allow radiusd to create sock_files

* Wed Sep 24 2008 Dan Walsh <dwalsh@redhat.com> 3.5.9-1
- Upgrade to upstream

* Tue Sep 23 2008 Dan Walsh <dwalsh@redhat.com> 3.5.8-7
- Allow confined users to login with dbus

* Mon Sep 22 2008 Dan Walsh <dwalsh@redhat.com> 3.5.8-6
- Fix transition to nsplugin

* Mon Sep 22 2008 Dan Walsh <dwalsh@redhat.com> 3.5.8-5
- Add file context for /dev/mspblk.*

* Sun Sep 21 2008 Dan Walsh <dwalsh@redhat.com> 3.5.8-4
- Fix transition to nsplugin
'
* Thu Sep 18 2008 Dan Walsh <dwalsh@redhat.com> 3.5.8-3
- Fix labeling on new pm*log
- Allow ssh to bind to all nodes

* Thu Sep 11 2008 Dan Walsh <dwalsh@redhat.com> 3.5.8-1
- Merge upstream changes
- Add Xavier Toth patches

* Wed Sep 10 2008 Dan Walsh <dwalsh@redhat.com> 3.5.7-2
- Add qemu_cache_t for /var/cache/libvirt

* Fri Sep 5 2008 Dan Walsh <dwalsh@redhat.com> 3.5.7-1
- Remove gamin policy

* Thu Sep 4 2008 Dan Walsh <dwalsh@redhat.com> 3.5.6-2
- Add tinyxs-max file system support

* Wed Sep 3 2008 Dan Walsh <dwalsh@redhat.com> 3.5.6-1
- Update to upstream
-       New handling of init scripts

* Fri Aug 29 2008 Dan Walsh <dwalsh@redhat.com> 3.5.5-4
- Allow pcsd to dbus
- Add memcache policy

* Fri Aug 29 2008 Dan Walsh <dwalsh@redhat.com> 3.5.5-3
- Allow audit dispatcher to kill his children

* Tue Aug 26 2008 Dan Walsh <dwalsh@redhat.com> 3.5.5-2
- Update to upstream
- Fix crontab use by unconfined user

* Tue Aug 12 2008 Dan Walsh <dwalsh@redhat.com> 3.5.4-2
- Allow ifconfig_t to read dhcpc_state_t

* Mon Aug 11 2008 Dan Walsh <dwalsh@redhat.com> 3.5.4-1
- Update to upstream

* Thu Aug 7 2008 Dan Walsh <dwalsh@redhat.com> 3.5.3-1
- Update to upstream 

* Wed Aug 2 2008 Dan Walsh <dwalsh@redhat.com> 3.5.2-2
- Allow system-config-selinux to work with policykit

* Fri Jul 25 2008 Dan Walsh <dwalsh@redhat.com> 3.5.1-5
- Fix novel labeling

* Fri Jul 25 2008 Dan Walsh <dwalsh@redhat.com> 3.5.1-4
- Consolodate pyzor,spamassassin, razor into one security domain
- Fix xdm requiring additional perms.

* Fri Jul 25 2008 Dan Walsh <dwalsh@redhat.com> 3.5.1-3
- Fixes for logrotate, alsa

* Thu Jul 25 2008 Dan Walsh <dwalsh@redhat.com> 3.5.1-2
- Eliminate vbetool duplicate entry

* Wed Jul 16 2008 Dan Walsh <dwalsh@redhat.com> 3.5.1-1
- Fix xguest -> xguest_mozilla_t -> xguest_openiffice_t
- Change dhclient to be able to red networkmanager_var_run

* Tue Jul 15 2008 Dan Walsh <dwalsh@redhat.com> 3.5.0-1
- Update to latest refpolicy
- Fix libsemanage initial install bug

* Wed Jul 9 2008 Dan Walsh <dwalsh@redhat.com> 3.4.2-14
- Add inotify support to nscd

* Tue Jul 8 2008 Dan Walsh <dwalsh@redhat.com> 3.4.2-13
- Allow unconfined_t to setfcap

* Mon Jul 7 2008 Dan Walsh <dwalsh@redhat.com> 3.4.2-12
- Allow amanda to read tape
- Allow prewikka cgi to use syslog, allow audisp_t to signal cgi
- Add support for netware file systems

* Thu Jul 3 2008 Dan Walsh <dwalsh@redhat.com> 3.4.2-11
- Allow ypbind apps to net_bind_service

* Wed Jul 2 2008 Dan Walsh <dwalsh@redhat.com> 3.4.2-10
- Allow all system domains and application domains to append to any log file

* Sun Jun 29 2008 Dan Walsh <dwalsh@redhat.com> 3.4.2-9
- Allow gdm to read rpm database
- Allow nsplugin to read mplayer config files

* Thu Jun 26 2008 Dan Walsh <dwalsh@redhat.com> 3.4.2-8
- Allow vpnc to run ifconfig

* Tue Jun 24 2008 Dan Walsh <dwalsh@redhat.com> 3.4.2-7
- Allow confined users to use postgres
- Allow system_mail_t to exec other mail clients
- Label mogrel_rails as an apache server

* Mon Jun 23 2008 Dan Walsh <dwalsh@redhat.com> 3.4.2-6
- Apply unconfined_execmem_exec_t to haskell programs

* Sun Jun 22 2008 Dan Walsh <dwalsh@redhat.com> 3.4.2-5
- Fix prelude file context

* Fri Jun 12 2008 Dan Walsh <dwalsh@redhat.com> 3.4.2-4
- allow hplip to talk dbus
- Fix context on ~/.local dir

* Thu Jun 12 2008 Dan Walsh <dwalsh@redhat.com> 3.4.2-3
- Prevent applications from reading x_device

* Thu Jun 12 2008 Dan Walsh <dwalsh@redhat.com> 3.4.2-2
- Add /var/lib/selinux context

* Wed Jun 11 2008 Dan Walsh <dwalsh@redhat.com> 3.4.2-1
- Update to upstream 

* Wed Jun 4 2008 Dan Walsh <dwalsh@redhat.com> 3.4.1-5
- Add livecd policy

* Wed Jun 4 2008 Dan Walsh <dwalsh@redhat.com> 3.4.1-3
- Dontaudit search of admin_home for init_system_domain
- Rewrite of xace interfaces
- Lots of new fs_list_inotify
- Allow livecd to transition to setfiles_mac

* Fri May 9 2008 Dan Walsh <dwalsh@redhat.com> 3.4.1-2
- Begin XAce integration

* Fri May 9 2008 Dan Walsh <dwalsh@redhat.com> 3.4.1-1
- Merge Upstream

* Wed May 7 2008 Dan Walsh <dwalsh@redhat.com> 3.3.1-48
- Allow amanada to create data files

* Wed May 7 2008 Dan Walsh <dwalsh@redhat.com> 3.3.1-47
- Fix initial install, semanage setup

* Tue May 6 2008 Dan Walsh <dwalsh@redhat.com> 3.3.1-46
- Allow system_r for httpd_unconfined_script_t

* Wed Apr 30 2008 Dan Walsh <dwalsh@redhat.com> 3.3.1-45
- Remove dmesg boolean
- Allow user domains to read/write game data

* Mon Apr 28 2008 Dan Walsh <dwalsh@redhat.com> 3.3.1-44
- Change unconfined_t to transition to unconfined_mono_t when running mono
- Change XXX_mono_t to transition to XXX_t when executing bin_t files, so gnome-do will work

* Mon Apr 28 2008 Dan Walsh <dwalsh@redhat.com> 3.3.1-43
- Remove old booleans from targeted-booleans.conf file

* Fri Apr 25 2008 Dan Walsh <dwalsh@redhat.com> 3.3.1-42
- Add boolean to mmap_zero
- allow tor setgid
- Allow gnomeclock to set clock

* Thu Apr 24 2008 Dan Walsh <dwalsh@redhat.com> 3.3.1-41
- Don't run crontab from unconfined_t

* Wed Apr 23 2008 Dan Walsh <dwalsh@redhat.com> 3.3.1-39
- Change etc files to config files to allow users to read them

* Fri Apr 14 2008 Dan Walsh <dwalsh@redhat.com> 3.3.1-37
- Lots of fixes for confined domains on NFS_t homedir

* Mon Apr 14 2008 Dan Walsh <dwalsh@redhat.com> 3.3.1-36
- dontaudit mrtg reading /proc
- Allow iscsi to signal itself
- Allow gnomeclock sys_ptrace

* Thu Apr 10 2008 Dan Walsh <dwalsh@redhat.com> 3.3.1-33
- Allow dhcpd to read kernel network state

* Thu Apr 10 2008 Dan Walsh <dwalsh@redhat.com> 3.3.1-32
- Label /var/run/gdm correctly
- Fix unconfined_u user creation

* Tue Apr 8 2008 Dan Walsh <dwalsh@redhat.com> 3.3.1-31
- Allow transition from initrc_t to getty_t

* Tue Apr 8 2008 Dan Walsh <dwalsh@redhat.com> 3.3.1-30
- Allow passwd to communicate with user sockets to change gnome-keyring

* Sat Apr 5 2008 Dan Walsh <dwalsh@redhat.com> 3.3.1-29
- Fix initial install

* Fri Apr 4 2008 Dan Walsh <dwalsh@redhat.com> 3.3.1-28
- Allow radvd to use fifo_file
- dontaudit setfiles reading links
- allow semanage sys_resource
- add allow_httpd_mod_auth_ntlm_winbind boolean
- Allow privhome apps including dovecot read on nfs and cifs home 
dirs if the boolean is set


* Tue Apr 1 2008 Dan Walsh <dwalsh@redhat.com> 3.3.1-27
- Allow nsplugin to read /etc/mozpluggerrc, user_fonts
- Allow syslog to manage innd logs.
- Allow procmail to ioctl spamd_exec_t

* Sat Mar 28 2008 Dan Walsh <dwalsh@redhat.com> 3.3.1-26
- Allow initrc_t to dbus chat with consolekit.

* Thu Mar 27 2008 Dan Walsh <dwalsh@redhat.com> 3.3.1-25
- Additional access for nsplugin
- Allow xdm setcap/getcap until pulseaudio is fixed

* Tue Mar 25 2008 Dan Walsh <dwalsh@redhat.com> 3.3.1-24
- Allow mount to mkdir on tmpfs
- Allow ifconfig to search debugfs

* Fri Mar 18 2008 Dan Walsh <dwalsh@redhat.com> 3.3.1-23
- Fix file context for MATLAB
- Fixes for xace

* Tue Mar 18 2008 Dan Walsh <dwalsh@redhat.com> 3.3.1-22
- Allow stunnel to transition to inetd children domains
- Make unconfined_dbusd_t an unconfined domain 

* Mon Mar 17 2008 Dan Walsh <dwalsh@redhat.com> 3.3.1-21
- Fixes for qemu/virtd

* Fri Mar 14 2008 Dan Walsh <dwalsh@redhat.com> 3.3.1-20
- Fix bug in mozilla policy to allow xguest transition
- This will fix the 

libsemanage.dbase_llist_query: could not find record value
libsemanage.dbase_llist_query: could not query record value (No such file or
directory)
 bug in xguest

* Fri Mar 14 2008 Dan Walsh <dwalsh@redhat.com> 3.3.1-19
- Allow nsplugin to run acroread

* Thu Mar 13 2008 Dan Walsh <dwalsh@redhat.com> 3.3.1-18
- Add cups_pdf policy
- Add openoffice policy to run in xguest

* Thu Mar 13 2008 Dan Walsh <dwalsh@redhat.com> 3.3.1-17
- prewika needs to contact mysql
- Allow syslog to read system_map files

* Wed Mar 12 2008 Dan Walsh <dwalsh@redhat.com> 3.3.1-16
- Change init_t to an unconfined_domain

* Tue Mar 11 2008 Dan Walsh <dwalsh@redhat.com> 3.3.1-15
- Allow init to transition to initrc_t on shell exec.
- Fix init to be able to sendto init_t.
- Allow syslog to connect to mysql
- Allow lvm to manage its own fifo_files
- Allow bugzilla to use ldap
- More mls fixes 

* Tue Mar 11 2008 Bill Nottingham <notting@redhat.com> 3.3.1-14
- fixes for init policy (#436988)
- fix build

* Mon Mar 10 2008 Dan Walsh <dwalsh@redhat.com> 3.3.1-13
- Additional changes for MLS policy

* Thu Mar 6 2008 Dan Walsh <dwalsh@redhat.com> 3.3.1-12
- Fix initrc_context generation for MLS

* Mon Mar 3 2008 Dan Walsh <dwalsh@redhat.com> 3.3.1-11
- Fixes for libvirt

* Mon Mar 3 2008 Dan Walsh <dwalsh@redhat.com> 3.3.1-10
- Allow bitlebee to read locale_t

* Fri Feb 29 2008 Dan Walsh <dwalsh@redhat.com> 3.3.1-9
- More xselinux rules

* Thu Feb 28 2008 Dan Walsh <dwalsh@redhat.com> 3.3.1-8
- Change httpd_$1_script_r*_t to httpd_$1_content_r*_t

* Wed Feb 27 2008 Dan Walsh <dwalsh@redhat.com> 3.3.1-6
- Prepare policy for beta release
- Change some of the system domains back to unconfined
- Turn on some of the booleans

* Tue Feb 26 2008 Dan Walsh <dwalsh@redhat.com> 3.3.1-5
- Allow nsplugin_config execstack/execmem
- Allow nsplugin_t to read alsa config
- Change apache to use user content 

* Tue Feb 26 2008 Dan Walsh <dwalsh@redhat.com> 3.3.1-4
- Add cyphesis policy

* Tue Feb 26 2008 Dan Walsh <dwalsh@redhat.com> 3.3.1-2
- Fix Makefile.devel to build mls modules
- Fix qemu to be more specific on labeling

* Tue Feb 26 2008 Dan Walsh <dwalsh@redhat.com> 3.3.1-1
- Update to upstream fixes

* Fri Feb 22 2008 Dan Walsh <dwalsh@redhat.com> 3.3.0-2
- Allow staff to mounton user_home_t

* Fri Feb 22 2008 Dan Walsh <dwalsh@redhat.com> 3.3.0-1
- Add xace support

* Thu Feb 21 2008 Dan Walsh <dwalsh@redhat.com> 3.2.9-2
- Add fusectl file system

* Wed Feb 20 2008 Dan Walsh <dwalsh@redhat.com> 3.2.9-1
- Fixes from yum-cron
- Update to latest upstream


* Tue Feb 19 2008 Dan Walsh <dwalsh@redhat.com> 3.2.8-2
- Fix userdom_list_user_files


* Fri Feb 15 2008 Dan Walsh <dwalsh@redhat.com> 3.2.8-1
- Merge with upstream

* Thu Feb 5 2008 Dan Walsh <dwalsh@redhat.com> 3.2.7-6
- Allow udev to send audit messages

* Thu Feb 5 2008 Dan Walsh <dwalsh@redhat.com> 3.2.7-5
- Add additional login users interfaces
  -     userdom_admin_login_user_template(staff)

* Thu Feb 5 2008 Dan Walsh <dwalsh@redhat.com> 3.2.7-3
- More fixes for polkit

* Thu Feb 5 2008 Dan Walsh <dwalsh@redhat.com> 3.2.7-2
- Eliminate transition from unconfined_t to qemu by default
- Fixes for gpg

* Tue Feb 5 2008 Dan Walsh <dwalsh@redhat.com> 3.2.7-1
- Update to upstream

* Tue Feb 5 2008 Dan Walsh <dwalsh@redhat.com> 3.2.6-7
- Fixes for staff_t

* Tue Feb 5 2008 Dan Walsh <dwalsh@redhat.com> 3.2.6-6
- Add policy for kerneloops
- Add policy for gnomeclock

* Mon Feb 4 2008 Dan Walsh <dwalsh@redhat.com> 3.2.6-5
- Fixes for libvirt

* Sun Feb 3 2008 Dan Walsh <dwalsh@redhat.com> 3.2.6-4
- Fixes for nsplugin

* Sat Feb 2 2008 Dan Walsh <dwalsh@redhat.com> 3.2.6-3
- More fixes for qemu

* Sat Feb 2 2008 Dan Walsh <dwalsh@redhat.com> 3.2.6-2
- Additional ports for vnc and allow qemu and libvirt to search all directories

* Fri Feb 1 2008 Dan Walsh <dwalsh@redhat.com> 3.2.6-1
- Update to upstream
- Add libvirt policy
- add qemu policy

* Fri Feb 1 2008 Dan Walsh <dwalsh@redhat.com> 3.2.5-25
- Allow fail2ban to create a socket in /var/run

* Wed Jan 30 2008 Dan Walsh <dwalsh@redhat.com> 3.2.5-24
- Allow allow_httpd_mod_auth_pam to work

* Wed Jan 30 2008 Dan Walsh <dwalsh@redhat.com> 3.2.5-22
- Add audisp policy and prelude

* Mon Jan 28 2008 Dan Walsh <dwalsh@redhat.com> 3.2.5-21
- Allow all user roles to executae samba net command

* Fri Jan 25 2008 Dan Walsh <dwalsh@redhat.com> 3.2.5-20
- Allow usertypes to read/write noxattr file systems

* Thu Jan 24 2008 Dan Walsh <dwalsh@redhat.com> 3.2.5-19
- Fix nsplugin to allow flashplugin to work in enforcing mode

* Wed Jan 23 2008 Dan Walsh <dwalsh@redhat.com> 3.2.5-18
- Allow pam_selinux_permit to kill all processes

* Mon Jan 21 2008 Dan Walsh <dwalsh@redhat.com> 3.2.5-17
- Allow ptrace or user processes by users of same type
- Add boolean for transition to nsplugin

* Mon Jan 21 2008 Dan Walsh <dwalsh@redhat.com> 3.2.5-16
- Allow nsplugin sys_nice, getsched, setsched

* Mon Jan 21 2008 Dan Walsh <dwalsh@redhat.com> 3.2.5-15
- Allow login programs to talk dbus to oddjob

* Thu Jan 17 2008 Dan Walsh <dwalsh@redhat.com> 3.2.5-14
- Add procmail_log support
- Lots of fixes for munin

* Tue Jan 15 2008 Dan Walsh <dwalsh@redhat.com> 3.2.5-13
- Allow setroubleshoot to read policy config and send audit messages

* Mon Jan 14 2008 Dan Walsh <dwalsh@redhat.com> 3.2.5-12
- Allow users to execute all files in homedir, if boolean set
- Allow mount to read samba config

* Sun Jan 13 2008 Dan Walsh <dwalsh@redhat.com> 3.2.5-11
- Fixes for xguest to run java plugin

* Mon Jan 7 2008 Dan Walsh <dwalsh@redhat.com> 3.2.5-10
- dontaudit pam_t and dbusd writing to user_home_t

* Mon Jan 7 2008 Dan Walsh <dwalsh@redhat.com> 3.2.5-9
- Update gpg to allow reading of inotify

* Wed Jan 2 2008 Dan Walsh <dwalsh@redhat.com> 3.2.5-8
- Change user and staff roles to work correctly with varied perms

* Mon Dec 31 2007 Dan Walsh <dwalsh@redhat.com> 3.2.5-7
- Fix munin log,
- Eliminate duplicate mozilla file context
- fix wpa_supplicant spec

* Mon Dec 24 2007 Dan Walsh <dwalsh@redhat.com> 3.2.5-6
- Fix role transition from unconfined_r to system_r when running rpm
- Allow unconfined_domains to communicate with user dbus instances

* Sat Dec 21 2007 Dan Walsh <dwalsh@redhat.com> 3.2.5-5
- Fixes for xguest

* Thu Dec 20 2007 Dan Walsh <dwalsh@redhat.com> 3.2.5-4
- Let all uncofined domains communicate with dbus unconfined

* Thu Dec 20 2007 Dan Walsh <dwalsh@redhat.com> 3.2.5-3
- Run rpm in system_r

* Wed Dec 19 2007 Dan Walsh <dwalsh@redhat.com> 3.2.5-2
- Zero out customizable types

* Wed Dec 19 2007 Dan Walsh <dwalsh@redhat.com> 3.2.5-1
- Fix definiton of admin_home_t

* Wed Dec 19 2007 Dan Walsh <dwalsh@redhat.com> 3.2.4-5
- Fix munin file context

* Tue Dec 18 2007 Dan Walsh <dwalsh@redhat.com> 3.2.4-4
- Allow cron to run unconfined apps

* Mon Dec 17 2007 Dan Walsh <dwalsh@redhat.com> 3.2.4-3
- Modify default login to unconfined_u

* Thu Dec 13 2007 Dan Walsh <dwalsh@redhat.com> 3.2.4-1
- Dontaudit dbus user client search of /root

* Wed Dec 12 2007 Dan Walsh <dwalsh@redhat.com> 3.2.4-1
- Update to upstream

* Tue Dec 11 2007 Dan Walsh <dwalsh@redhat.com> 3.2.3-2
- Fixes for polkit
- Allow xserver to ptrace

* Tue Dec 11 2007 Dan Walsh <dwalsh@redhat.com> 3.2.3-1
- Add polkit policy
- Symplify userdom context, remove automatic per_role changes

* Tue Dec 4 2007 Dan Walsh <dwalsh@redhat.com> 3.2.2-1
- Update to upstream
- Allow httpd_sys_script_t to search users homedirs

* Mon Dec 3 2007 Dan Walsh <dwalsh@redhat.com> 3.2.1-3
- Allow rpm_script to transition to unconfined_execmem_t

* Fri Nov 30 2007 Dan Walsh <dwalsh@redhat.com> 3.2.1-1
- Remove user based home directory separation

* Wed Nov 28 2007 Dan Walsh <dwalsh@redhat.com> 3.1.2-2
- Remove user specific crond_t

* Mon Nov 19 2007 Dan Walsh <dwalhh@redhat.com> 3.1.2-1
- Merge with upstream
- Allow xsever to read hwdata_t
- Allow login programs to setkeycreate

* Sat Nov 10 2007 Dan Walsh <dwalsh@redhat.com> 3.1.1-1
- Update to upstream

* Mon Oct 22 2007 Dan Walsh <dwalsh@redhat.com> 3.1.0-1
- Update to upstream

* Mon Oct 22 2007 Dan Walsh <dwalsh@redhat.com> 3.0.8-30
- Allow XServer to read /proc/self/cmdline
- Fix unconfined cron jobs
- Allow fetchmail to transition to procmail
- Fixes for hald_mac
- Allow system_mail to transition to exim
- Allow tftpd to upload files
- Allow xdm to manage unconfined_tmp
- Allow udef to read alsa config
- Fix xguest to be able to connect to sound port

* Fri Oct 17 2007 Dan Walsh <dwalsh@redhat.com> 3.0.8-28
- Fixes for hald_mac 
- Treat unconfined_home_dir_t as a home dir
- dontaudit rhgb writes to fonts and root

* Fri Oct 17 2007 Dan Walsh <dwalsh@redhat.com> 3.0.8-27
- Fix dnsmasq
- Allow rshd full login privs

* Thu Oct 16 2007 Dan Walsh <dwalsh@redhat.com> 3.0.8-26
- Allow rshd to connect to ports > 1023

* Thu Oct 16 2007 Dan Walsh <dwalsh@redhat.com> 3.0.8-25
- Fix vpn to bind to port 4500
- Allow ssh to create shm
- Add Kismet policy

* Tue Oct 16 2007 Dan Walsh <dwalsh@redhat.com> 3.0.8-24
- Allow rpm to chat with networkmanager

* Mon Oct 15 2007 Dan Walsh <dwalsh@redhat.com> 3.0.8-23
- Fixes for ipsec and exim mail
- Change default to unconfined user

* Fri Oct 12 2007 Dan Walsh <dwalsh@redhat.com> 3.0.8-22
- Pass the UNK_PERMS param to makefile
- Fix gdm location

* Wed Oct 10 2007 Dan Walsh <dwalsh@redhat.com> 3.0.8-21
- Make alsa work

* Tue Oct 9 2007 Dan Walsh <dwalsh@redhat.com> 3.0.8-20
- Fixes for consolekit and startx sessions

* Mon Oct 8 2007 Dan Walsh <dwalsh@redhat.com> 3.0.8-19
- Dontaudit consoletype talking to unconfined_t

* Thu Oct 4 2007 Dan Walsh <dwalsh@redhat.com> 3.0.8-18
- Remove homedir_template

* Tue Oct 2 2007 Dan Walsh <dwalsh@redhat.com> 3.0.8-17
- Check asound.state

* Mon Oct 1 2007 Dan Walsh <dwalsh@redhat.com> 3.0.8-16
- Fix exim policy

* Thu Sep 24 2007 Dan Walsh <dwalsh@redhat.com> 3.0.8-15
- Allow tmpreadper to read man_t
- Allow racoon to bind to all nodes
- Fixes for finger print reader

* Tue Sep 24 2007 Dan Walsh <dwalsh@redhat.com> 3.0.8-14
- Allow xdm to talk to input device (fingerprint reader)
- Allow octave to run as java

* Tue Sep 24 2007 Dan Walsh <dwalsh@redhat.com> 3.0.8-13
- Allow login programs to set ioctl on /proc

* Mon Sep 24 2007 Dan Walsh <dwalsh@redhat.com> 3.0.8-12
- Allow nsswitch apps to read samba_var_t

* Mon Sep 24 2007 Dan Walsh <dwalsh@redhat.com> 3.0.8-11
- Fix maxima

* Mon Sep 24 2007 Dan Walsh <dwalsh@redhat.com> 3.0.8-10
- Eliminate rpm_t:fifo_file avcs
- Fix dbus path for helper app

* Sat Sep 22 2007 Dan Walsh <dwalsh@redhat.com> 3.0.8-9
- Fix service start stop terminal avc's

* Fri Sep 21 2007 Dan Walsh <dwalsh@redhat.com> 3.0.8-8
- Allow also to search var_lib
- New context for dbus launcher 

* Fri Sep 21 2007 Dan Walsh <dwalsh@redhat.com> 3.0.8-7
- Allow cupsd_config_t to read/write usb_device_t
- Support for finger print reader,
- Many fixes for clvmd
- dbus starting networkmanager

* Thu Sep 20 2007 Dan Walsh <dwalsh@redhat.com> 3.0.8-5
- Fix java and mono to run in xguest account

* Wed Sep 19 2007 Dan Walsh <dwalsh@redhat.com> 3.0.8-4
- Fix to add xguest account when inititial install
- Allow mono, java, wine to run in userdomains

* Wed Sep 19 2007 Dan Walsh <dwalsh@redhat.com> 3.0.8-3
- Allow xserver to search devpts_t
- Dontaudit ldconfig output to homedir

* Tue Sep 18 2007 Dan Walsh <dwalsh@redhat.com> 3.0.8-2
- Remove hplip_etc_t change back to etc_t.


* Mon Sep 17 2007 Dan Walsh <dwalsh@redhat.com> 3.0.8-1
- Allow cron to search nfs and samba homedirs

* Tue Sep 11 2007 Dan Walsh <dwalsh@redhat.com> 3.0.7-10
- Allow NetworkManager to dbus chat with yum-updated

* Tue Sep 11 2007 Dan Walsh <dwalsh@redhat.com> 3.0.7-9
- Allow xfs to bind to port 7100

* Mon Sep 10 2007 Dan Walsh <dwalsh@redhat.com> 3.0.7-8
- Allow newalias/sendmail dac_override
- Allow bind to bind to all udp ports

* Fri Sep 7 2007 Dan Walsh <dwalsh@redhat.com> 3.0.7-7
- Turn off direct transition

* Fri Sep 7 2007 Dan Walsh <dwalsh@redhat.com> 3.0.7-6
- Allow wine to run in system role

* Thu Sep 6 2007 Dan Walsh <dwalsh@redhat.com> 3.0.7-5
- Fix java labeling 

* Thu Sep 6 2007 Dan Walsh <dwalsh@redhat.com> 3.0.7-4
- Define user_home_type as home_type

* Tue Aug 28 2007 Dan Walsh <dwalsh@redhat.com> 3.0.7-3
- Allow sendmail to create etc_aliases_t

* Tue Aug 28 2007 Dan Walsh <dwalsh@redhat.com> 3.0.7-2
- Allow login programs to read symlinks on homedirs

* Mon Aug 27 2007 Dan Walsh <dwalsh@redhat.com> 3.0.7-1
- Update an readd modules

* Fri Aug 24 2007 Dan Walsh <dwalsh@redhat.com> 3.0.6-3
- Cleanup  spec file

* Fri Aug 24 2007 Dan Walsh <dwalsh@redhat.com> 3.0.6-2
- Allow xserver to be started by unconfined process and talk to tty

* Wed Aug 22 2007 Dan Walsh <dwalsh@redhat.com> 3.0.6-1
- Upgrade to upstream to grab postgressql changes

* Tue Aug 21 2007 Dan Walsh <dwalsh@redhat.com> 3.0.5-11
- Add setransd for mls policy

* Mon Aug 20 2007 Dan Walsh <dwalsh@redhat.com> 3.0.5-10
- Add ldconfig_cache_t

* Sat Aug 18 2007 Dan Walsh <dwalsh@redhat.com> 3.0.5-9
- Allow sshd to write to proc_t for afs login

* Sat Aug 18 2007 Dan Walsh <dwalsh@redhat.com> 3.0.5-8
- Allow xserver access to urand

* Tue Aug 14 2007 Dan Walsh <dwalsh@redhat.com> 3.0.5-7
- allow dovecot to search mountpoints

* Sat Aug 11 2007 Dan Walsh <dwalsh@redhat.com> 3.0.5-6
- Fix Makefile for building policy modules

* Fri Aug 10 2007 Dan Walsh <dwalsh@redhat.com> 3.0.5-5
- Fix dhcpc startup of service 

* Fri Aug 10 2007 Dan Walsh <dwalsh@redhat.com> 3.0.5-4
- Fix dbus chat to not happen for xguest and guest users

* Mon Aug 6 2007 Dan Walsh <dwalsh@redhat.com> 3.0.5-3
- Fix nagios cgi
- allow squid to communicate with winbind

* Mon Aug 6 2007 Dan Walsh <dwalsh@redhat.com> 3.0.5-2
- Fixes for ldconfig

* Thu Aug 2 2007 Dan Walsh <dwalsh@redhat.com> 3.0.5-1
- Update from upstream

* Wed Aug 1 2007 Dan Walsh <dwalsh@redhat.com> 3.0.4-6
- Add nasd support

* Wed Aug 1 2007 Dan Walsh <dwalsh@redhat.com> 3.0.4-5
- Fix new usb devices and dmfm

* Mon Jul 30 2007 Dan Walsh <dwalsh@redhat.com> 3.0.4-4
- Eliminate mount_ntfs_t policy, merge into mount_t

* Mon Jul 30 2007 Dan Walsh <dwalsh@redhat.com> 3.0.4-3
- Allow xserver to write to ramfs mounted by rhgb

* Tue Jul 23 2007 Dan Walsh <dwalsh@redhat.com> 3.0.4-2
- Add context for dbus machine id

* Tue Jul 23 2007 Dan Walsh <dwalsh@redhat.com> 3.0.4-1
- Update with latest changes from upstream

* Tue Jul 23 2007 Dan Walsh <dwalsh@redhat.com> 3.0.3-6
- Fix prelink to handle execmod

* Mon Jul 23 2007 Dan Walsh <dwalsh@redhat.com> 3.0.3-5
- Add ntpd_key_t to handle secret data

* Fri Jul 20 2007 Dan Walsh <dwalsh@redhat.com> 3.0.3-4
- Add anon_inodefs
- Allow unpriv user exec pam_exec_t
- Fix trigger

* Fri Jul 20 2007 Dan Walsh <dwalsh@redhat.com> 3.0.3-3
- Allow cups to use generic usb
- fix inetd to be able to run random apps (git)

* Thu Jul 19 2007 Dan Walsh <dwalsh@redhat.com> 3.0.3-2
- Add proper contexts for rsyslogd

* Thu Jul 19 2007 Dan Walsh <dwalsh@redhat.com> 3.0.3-1
- Fixes for xguest policy

* Tue Jul 17 2007 Dan Walsh <dwalsh@redhat.com> 3.0.2-9
- Allow execution of gconf

* Sat Jul 14 2007 Dan Walsh <dwalsh@redhat.com> 3.0.2-8
- Fix moilscanner update problem

* Thu Jul 12 2007 Dan Walsh <dwalsh@redhat.com> 3.0.2-7
- Begin adding policy to separate setsebool from semanage
- Fix xserver.if definition to not break sepolgen.if

* Wed Jul 11 2007 Dan Walsh <dwalsh@redhat.com> 3.0.2-5
- Add new devices

* Tue Jul 10 2007 Dan Walsh <dwalsh@redhat.com> 3.0.2-4
- Add brctl policy

* Fri Jul 6 2007 Dan Walsh <dwalsh@redhat.com> 3.0.2-3
- Fix root login to include system_r

* Fri Jul 6 2007 Dan Walsh <dwalsh@redhat.com> 3.0.2-2
- Allow prelink to read kernel sysctls

* Mon Jul 2 2007 Dan Walsh <dwalsh@redhat.com> 3.0.1-5
- Default to user_u:system_r:unconfined_t 

* Sun Jul 1 2007 Dan Walsh <dwalsh@redhat.com> 3.0.1-4
- fix squid
- Fix rpm running as uid

* Wed Jun 26 2007 Dan Walsh <dwalsh@redhat.com> 3.0.1-3
- Fix syslog declaration

* Wed Jun 26 2007 Dan Walsh <dwalsh@redhat.com> 3.0.1-2
- Allow avahi to access inotify
- Remove a lot of bogus security_t:filesystem avcs

* Fri May 25 2007 Dan Walsh <dwalsh@redhat.com> 3.0.1-1
- Remove ifdef strict policy from upstream

* Fri May 18 2007 Dan Walsh <dwalsh@redhat.com> 2.6.5-3
- Remove ifdef strict to allow user_u to login 

* Fri May 18 2007 Dan Walsh <dwalsh@redhat.com> 2.6.5-2
- Fix for amands
- Allow semanage to read pp files
- Allow rhgb to read xdm_xserver_tmp

* Fri May 18 2007 Dan Walsh <dwalsh@redhat.com> 2.6.4-7
- Allow kerberos servers to use ldap for backing store

* Thu May 17 2007 Dan Walsh <dwalsh@redhat.com> 2.6.4-6
- allow alsactl to read kernel state

* Wed May 16 2007 Dan Walsh <dwalsh@redhat.com> 2.6.4-5
- More fixes for alsactl
- Transition from hal and modutils
- Fixes for suspend resume.  
     - insmod domtrans to alsactl
     - insmod writes to hal log

* Wed May 16 2007 Dan Walsh <dwalsh@redhat.com> 2.6.4-2
- Allow unconfined_t to transition to NetworkManager_t
- Fix netlabel policy

* Mon May 14 2007 Dan Walsh <dwalsh@redhat.com> 2.6.4-1
- Update to latest from upstream

* Fri May 4 2007 Dan Walsh <dwalsh@redhat.com> 2.6.3-1
- Update to latest from upstream

* Mon Apr 30 2007 Dan Walsh <dwalsh@redhat.com> 2.6.2-1
- Update to latest from upstream

* Fri Apr 27 2007 Dan Walsh <dwalsh@redhat.com> 2.6.1-4
- Allow pcscd_t to send itself signals

* Fri Apr 27 2007 Dan Walsh <dwalsh@redhat.com> 2.6.1-3
- 

* Wed Apr 25 2007 Dan Walsh <dwalsh@redhat.com> 2.6.1-2
- Fixes for unix_update
- Fix logwatch to be able to search all dirs

* Mon Apr 23 2007 Dan Walsh <dwalsh@redhat.com> 2.6.1-1
- Upstream bumped the version

* Thu Apr 19 2007 Dan Walsh <dwalsh@redhat.com> 2.5.12-12
- Allow consolekit to syslog
- Allow ntfs to work with hal

* Thu Apr 19 2007 Dan Walsh <dwalsh@redhat.com> 2.5.12-11
- Allow iptables to read etc_runtime_t

* Thu Apr 19 2007 Dan Walsh <dwalsh@redhat.com> 2.5.12-10
- MLS Fixes

* Wed Apr 18 2007 Dan Walsh <dwalsh@redhat.com> 2.5.12-8
- Fix path of /etc/lvm/cache directory
- Fixes for alsactl and pppd_t
- Fixes for consolekit

* Tue Apr 17 2007 Dan Walsh <dwalsh@redhat.com> 2.5.12-5
- Allow insmod_t to mount kvmfs_t filesystems

* Tue Apr 17 2007 Dan Walsh <dwalsh@redhat.com> 2.5.12-4
- Rwho policy
- Fixes for consolekit

* Fri Apr 12 2007 Dan Walsh <dwalsh@redhat.com> 2.5.12-3
- fixes for fusefs

* Thu Apr 12 2007 Dan Walsh <dwalsh@redhat.com> 2.5.12-2
- Fix samba_net to allow it to view samba_var_t

* Tue Apr 10 2007 Dan Walsh <dwalsh@redhat.com> 2.5.12-1
- Update to upstream

* Tue Apr 10 2007 Dan Walsh <dwalsh@redhat.com> 2.5.11-8
- Fix Sonypic backlight
- Allow snmp to look at squid_conf_t

* Mon Apr 9 2007 Dan Walsh <dwalsh@redhat.com> 2.5.11-7
- Fixes for pyzor, cyrus, consoletype on everything installs

* Mon Apr 9 2007 Dan Walsh <dwalsh@redhat.com> 2.5.11-6
- Fix hald_acl_t to be able to getattr/setattr on usb devices
- Dontaudit write to unconfined_pipes for load_policy

* Thu Apr 5 2007 Dan Walsh <dwalsh@redhat.com> 2.5.11-5
- Allow bluetooth to read inotifyfs

* Wed Apr 4 2007 Dan Walsh <dwalsh@redhat.com> 2.5.11-4
- Fixes for samba domain controller.
- Allow ConsoleKit to look at ttys

* Tue Apr 3 2007 Dan Walsh <dwalsh@redhat.com> 2.5.11-3
- Fix interface call

* Tue Apr 3 2007 Dan Walsh <dwalsh@redhat.com> 2.5.11-2
- Allow syslog-ng to read /var
- Allow locate to getattr on all filesystems
- nscd needs setcap

* Mon Mar 26 2007 Dan Walsh <dwalsh@redhat.com> 2.5.11-1
- Update to upstream

* Fri Mar 23 2007 Dan Walsh <dwalsh@redhat.com> 2.5.10-2
- Allow samba to run groupadd

* Thu Mar 22 2007 Dan Walsh <dwalsh@redhat.com> 2.5.10-1
- Update to upstream

* Thu Mar 22 2007 Dan Walsh <dwalsh@redhat.com> 2.5.9-6
- Allow mdadm to access generic scsi devices

* Wed Mar 21 2007 Dan Walsh <dwalsh@redhat.com> 2.5.9-5
- Fix labeling on udev.tbl dirs

* Tue Mar 20 2007 Dan Walsh <dwalsh@redhat.com> 2.5.9-4
- Fixes for logwatch

* Tue Mar 20 2007 Dan Walsh <dwalsh@redhat.com> 2.5.9-3
- Add fusermount and mount_ntfs policy

* Tue Mar 20 2007 Dan Walsh <dwalsh@redhat.com> 2.5.9-2
- Update to upstream
- Allow saslauthd to use kerberos keytabs

* Mon Mar 19 2007 Dan Walsh <dwalsh@redhat.com> 2.5.8-8
- Fixes for samba_var_t

* Mon Mar 19 2007 Dan Walsh <dwalsh@redhat.com> 2.5.8-7
- Allow networkmanager to setpgid
- Fixes for hal_acl_t

* Mon Mar 19 2007 Dan Walsh <dwalsh@redhat.com> 2.5.8-6
- Remove disable_trans booleans
- hald_acl_t needs to talk to nscd

* Thu Mar 15 2007 Dan Walsh <dwalsh@redhat.com> 2.5.8-5
- Fix prelink to be able to manage usr dirs.

* Tue Mar 13 2007 Dan Walsh <dwalsh@redhat.com> 2.5.8-4
- Allow insmod to launch init scripts

* Tue Mar 13 2007 Dan Walsh <dwalsh@redhat.com> 2.5.8-3
- Remove setsebool policy

* Mon Mar 12 2007 Dan Walsh <dwalsh@redhat.com> 2.5.8-2
- Fix handling of unlabled_t packets

* Thu Mar 8 2007 Dan Walsh <dwalsh@redhat.com> 2.5.8-1
- More of my patches from upstream

* Thu Mar 1 2007 Dan Walsh <dwalsh@redhat.com> 2.5.7-1
- Update to latest from upstream
- Add fail2ban policy

* Wed Feb 28 2007 Dan Walsh <dwalsh@redhat.com> 2.5.6-1
- Update to remove security_t:filesystem getattr problems

* Fri Feb 23 2007 Dan Walsh <dwalsh@redhat.com> 2.5.5-2
- Policy for consolekit

* Fri Feb 23 2007 Dan Walsh <dwalsh@redhat.com> 2.5.5-1
- Update to latest from upstream

* Wed Feb 21 2007 Dan Walsh <dwalsh@redhat.com> 2.5.4-2
- Revert Nemiver change
- Set sudo as a corecmd so prelink will work,  remove sudoedit mapping, since this will not work, it does not transition.
- Allow samba to execute useradd

* Tue Feb 20 2007 Dan Walsh <dwalsh@redhat.com> 2.5.4-1
- Upgrade to the latest from upstream

* Thu Feb 15 2007 Dan Walsh <dwalsh@redhat.com> 2.5.3-3
- Add sepolgen support
- Add bugzilla policy

* Wed Feb 14 2007 Dan Walsh <dwalsh@redhat.com> 2.5.3-2
- Fix file context for nemiver

* Sun Feb 11 2007 Dan Walsh <dwalsh@redhat.com> 2.5.3-1
- Remove include sym link

* Mon Feb 5 2007 Dan Walsh <dwalsh@redhat.com> 2.5.2-6
- Allow mozilla, evolution and thunderbird to read dev_random.
Resolves: #227002
- Allow spamd to connect to smtp port
Resolves: #227184
- Fixes to make ypxfr work
Resolves: #227237

* Sun Feb 4 2007 Dan Walsh <dwalsh@redhat.com> 2.5.2-5
- Fix ssh_agent to be marked as an executable
- Allow Hal to rw sound device 

* Thu Feb 1 2007 Dan Walsh <dwalsh@redhat.com> 2.5.2-4
- Fix spamassisin so crond can update spam files
- Fixes to allow kpasswd to work
- Fixes for bluetooth

* Fri Jan 25 2007 Dan Walsh <dwalsh@redhat.com> 2.5.2-3
- Remove some targeted diffs in file context file

* Thu Jan 25 2007 Dan Walsh <dwalsh@redhat.com> 2.5.2-2
- Fix squid cachemgr labeling

* Thu Jan 25 2007 Dan Walsh <dwalsh@redhat.com> 2.5.2-1
- Add ability to generate webadm_t policy
- Lots of new interfaces for httpd
- Allow sshd to login as unconfined_t

* Mon Jan 22 2007 Dan Walsh <dwalsh@redhat.com> 2.5.1-5
- Continue fixing, additional user domains

* Wed Jan 10 2007 Dan Walsh <dwalsh@redhat.com> 2.5.1-4
- Begin adding user confinement to targeted policy 

* Wed Jan 10 2007 Dan Walsh <dwalsh@redhat.com> 2.5.1-2
- Fixes for prelink, ktalkd, netlabel

* Mon Jan 8 2007 Dan Walsh <dwalsh@redhat.com> 2.5.1-1
- Allow prelink when run from rpm to create tmp files
Resolves: #221865
- Remove file_context for exportfs
Resolves: #221181
- Allow spamassassin to create ~/.spamassissin
Resolves: #203290
- Allow ssh access to the krb tickets
- Allow sshd to change passwd
- Stop newrole -l from working on non securetty
Resolves: #200110
- Fixes to run prelink in MLS machine
Resolves: #221233
- Allow spamassassin to read var_lib_t dir
Resolves: #219234

* Fri Dec 29 2006 Dan Walsh <dwalsh@redhat.com> 2.4.6-20
- fix mplayer to work under strict policy
- Allow iptables to use nscd
Resolves: #220794

* Thu Dec 28 2006 Dan Walsh <dwalsh@redhat.com> 2.4.6-19
- Add gconf policy and make it work with strict

* Sat Dec 23 2006 Dan Walsh <dwalsh@redhat.com> 2.4.6-18
- Many fixes for strict policy and by extension mls.

* Fri Dec 22 2006 Dan Walsh <dwalsh@redhat.com> 2.4.6-17
- Fix to allow ftp to bind to ports > 1024
Resolves: #219349

* Tue Dec 19 2006 Dan Walsh <dwalsh@redhat.com> 2.4.6-16
- Allow semanage to exec it self.  Label genhomedircon as semanage_exec_t
Resolves: #219421
- Allow sysadm_lpr_t to manage other print spool jobs
Resolves: #220080

* Mon Dec 18 2006 Dan Walsh <dwalsh@redhat.com> 2.4.6-15
- allow automount to setgid
Resolves: #219999

* Thu Dec 14 2006 Dan Walsh <dwalsh@redhat.com> 2.4.6-14
- Allow cron to polyinstatiate 
- Fix creation of boot flags
Resolves: #207433

* Thu Dec 14 2006 Dan Walsh <dwalsh@redhat.com> 2.4.6-13
- Fixes for irqbalance
Resolves: #219606

* Thu Dec 14 2006 Dan Walsh <dwalsh@redhat.com> 2.4.6-12
- Fix vixie-cron to work on mls
Resolves: #207433

* Wed Dec 13 2006 Dan Walsh <dwalsh@redhat.com> 2.4.6-11
Resolves: #218978

* Tue Dec 12 2006 Dan Walsh <dwalsh@redhat.com> 2.4.6-10
- Allow initrc to create files in /var directories
Resolves: #219227

* Fri Dec 8 2006 Dan Walsh <dwalsh@redhat.com> 2.4.6-9
- More fixes for MLS
Resolves: #181566

* Wed Dec 6 2006 Dan Walsh <dwalsh@redhat.com> 2.4.6-8
- More Fixes polyinstatiation
Resolves: #216184

* Wed Dec 6 2006 Dan Walsh <dwalsh@redhat.com> 2.4.6-7
- More Fixes polyinstatiation
- Fix handling of keyrings
Resolves: #216184

* Mon Dec 4 2006 Dan Walsh <dwalsh@redhat.com> 2.4.6-6
- Fix polyinstatiation
- Fix pcscd handling of terminal
Resolves: #218149
Resolves: #218350

* Fri Dec 1 2006 Dan Walsh <dwalsh@redhat.com> 2.4.6-5
- More fixes for quota
Resolves: #212957

* Fri Dec 1 2006 Dan Walsh <dwalsh@redhat.com> 2.4.6-4
- ncsd needs to use avahi sockets
Resolves: #217640
Resolves: #218014

* Thu Nov 28 2006 Dan Walsh <dwalsh@redhat.com> 2.4.6-3
- Allow login programs to polyinstatiate homedirs
Resolves: #216184
- Allow quotacheck to create database files
Resolves: #212957

* Tue Nov 28 2006 Dan Walsh <dwalsh@redhat.com> 2.4.6-1
- Dontaudit appending hal_var_lib files 
Resolves: #217452
Resolves: #217571
Resolves: #217611
Resolves: #217640
Resolves: #217725

* Mon Nov 21 2006 Dan Walsh <dwalsh@redhat.com> 2.4.5-4
- Fix context for helix players file_context #216942

* Mon Nov 20 2006 Dan Walsh <dwalsh@redhat.com> 2.4.5-3
- Fix load_policy to be able to mls_write_down so it can talk to the terminal

* Mon Nov 20 2006 Dan Walsh <dwalsh@redhat.com> 2.4.5-2
- Fixes for hwclock, clamav, ftp

* Wed Nov 15 2006 Dan Walsh <dwalsh@redhat.com> 2.4.5-1
- Move to upstream version which accepted my patches

* Wed Nov 15 2006 Dan Walsh <dwalsh@redhat.com> 2.4.4-2
- Fixes for nvidia driver

* Tue Nov 14 2006 Dan Walsh <dwalsh@redhat.com> 2.4.4-2
- Allow semanage to signal mcstrans

* Tue Nov 14 2006 Dan Walsh <dwalsh@redhat.com> 2.4.4-1
- Update to upstream

* Mon Nov 13 2006 Dan Walsh <dwalsh@redhat.com> 2.4.3-13
- Allow modstorage to edit /etc/fstab file

* Mon Nov 13 2006 Dan Walsh <dwalsh@redhat.com> 2.4.3-12
- Fix for qemu, /dev/

* Mon Nov 13 2006 Dan Walsh <dwalsh@redhat.com> 2.4.3-11
- Fix path to realplayer.bin

* Fri Nov 10 2006 Dan Walsh <dwalsh@redhat.com> 2.4.3-10
- Allow xen to connect to xen port

* Fri Nov 10 2006 Dan Walsh <dwalsh@redhat.com> 2.4.3-9
- Allow cups to search samba_etc_t directory
- Allow xend_t to list auto_mountpoints

* Thu Nov 9 2006 Dan Walsh <dwalsh@redhat.com> 2.4.3-8
- Allow xen to search automount

* Thu Nov 9 2006 Dan Walsh <dwalsh@redhat.com> 2.4.3-7
- Fix spec of jre files 

* Wed Nov 8 2006 Dan Walsh <dwalsh@redhat.com> 2.4.3-6
- Fix unconfined access to shadow file

* Wed Nov 8 2006 Dan Walsh <dwalsh@redhat.com> 2.4.3-5
- Allow xend to create files in xen_image_t directories

* Wed Nov 8 2006 Dan Walsh <dwalsh@redhat.com> 2.4.3-4
- Fixes for /var/lib/hal

* Tue Nov 7 2006 Dan Walsh <dwalsh@redhat.com> 2.4.3-3
- Remove ability for sysadm_t to look at audit.log

* Tue Nov 7 2006 Dan Walsh <dwalsh@redhat.com> 2.4.3-2
- Fix rpc_port_types
- Add aide policy for mls

* Mon Nov 6 2006 Dan Walsh <dwalsh@redhat.com> 2.4.3-1
- Merge with upstream

* Fri Nov 3 2006 Dan Walsh <dwalsh@redhat.com> 2.4.2-8
- Lots of fixes for ricci

* Fri Nov 3 2006 Dan Walsh <dwalsh@redhat.com> 2.4.2-7
- Allow xen to read/write fixed devices with a boolean
- Allow apache to search /var/log

* Thu Nov 2 2006 James Antill <james.antill@redhat.com> 2.4.2-6
- Fix policygentool specfile problem.
- Allow apache to send signals to it's logging helpers.
- Resolves: rhbz#212731

* Wed Nov 1 2006 Dan Walsh <dwalsh@redhat.com> 2.4.2-5
- Add perms for swat

* Tue Oct 31 2006 Dan Walsh <dwalsh@redhat.com> 2.4.2-4
- Add perms for swat

* Mon Oct 30 2006 Dan Walsh <dwalsh@redhat.com> 2.4.2-3
- Allow daemons to dump core files to /

* Fri Oct 27 2006 Dan Walsh <dwalsh@redhat.com> 2.4.2-2
- Fixes for ricci

* Fri Oct 27 2006 Dan Walsh <dwalsh@redhat.com> 2.4.2-1
- Allow mount.nfs to work

* Fri Oct 27 2006 Dan Walsh <dwalsh@redhat.com> 2.4.1-5
- Allow ricci-modstorage to look at lvm_etc_t

* Mon Oct 23 2006 Dan Walsh <dwalsh@redhat.com> 2.4.1-4
- Fixes for ricci using saslauthd

* Mon Oct 23 2006 Dan Walsh <dwalsh@redhat.com> 2.4.1-3
- Allow mountpoint on home_dir_t and home_t

* Mon Oct 23 2006 Dan Walsh <dwalsh@redhat.com> 2.4.1-2
- Update xen to read nfs files

* Mon Oct 23 2006 Dan Walsh <dwalsh@redhat.com> 2.4-4
- Allow noxattrfs to associate with other noxattrfs 

* Mon Oct 23 2006 Dan Walsh <dwalsh@redhat.com> 2.4-3
- Allow hal to use power_device_t

* Fri Oct 20 2006 Dan Walsh <dwalsh@redhat.com> 2.4-2
- Allow procemail to look at autofs_t
- Allow xen_image_t to work as a fixed device

* Thu Oct 19 2006 Dan Walsh <dwalsh@redhat.com> 2.4-1
- Refupdate from upstream

* Thu Oct 19 2006 Dan Walsh <dwalsh@redhat.com> 2.3.19-4
- Add lots of fixes for mls cups

* Wed Oct 18 2006 Dan Walsh <dwalsh@redhat.com> 2.3.19-3
- Lots of fixes for ricci

* Mon Oct 16 2006 Dan Walsh <dwalsh@redhat.com> 2.3.19-2
- Fix number of cats

* Mon Oct 16 2006 Dan Walsh <dwalsh@redhat.com> 2.3.19-1
- Update to upstream

* Thu Oct 12 2006 James Antill <jantill@redhat.com> 2.3.18-10
- More iSCSI changes for #209854

* Tue Oct 10 2006 James Antill <jantill@redhat.com> 2.3.18-9
- Test ISCSI fixes for #209854

* Sun Oct 8 2006 Dan Walsh <dwalsh@redhat.com> 2.3.18-8
- allow semodule to rmdir selinux_config_t dir

* Fri Oct 6 2006 Dan Walsh <dwalsh@redhat.com> 2.3.18-7
- Fix boot_runtime_t problem on ppc.  Should not be creating these files.

* Thu Oct 5 2006 Dan Walsh <dwalsh@redhat.com> 2.3.18-6
- Fix context mounts on reboot
- Fix ccs creation of directory in /var/log

* Thu Oct 5 2006 Dan Walsh <dwalsh@redhat.com> 2.3.18-5
- Update for tallylog

* Thu Oct 5 2006 Dan Walsh <dwalsh@redhat.com> 2.3.18-4
- Allow xend to rewrite dhcp conf files
- Allow mgetty sys_admin capability

* Wed Oct 4 2006 Dan Walsh <dwalsh@redhat.com> 2.3.18-3
- Make xentapctrl work

* Tue Oct 3 2006 Dan Walsh <dwalsh@redhat.com> 2.3.18-2
- Don't transition unconfined_t to bootloader_t
- Fix label in /dev/xen/blktap

* Tue Oct 3 2006 Dan Walsh <dwalsh@redhat.com> 2.3.18-1
- Patch for labeled networking

* Mon Oct 2 2006 Dan Walsh <dwalsh@redhat.com> 2.3.17-2
- Fix crond handling for mls

* Fri Sep 28 2006 Dan Walsh <dwalsh@redhat.com> 2.3.17-1
- Update to upstream

* Fri Sep 28 2006 Dan Walsh <dwalsh@redhat.com> 2.3.16-9
- Remove bluetooth-helper transition
- Add selinux_validate for semanage
- Require new version of libsemanage

* Fri Sep 28 2006 Dan Walsh <dwalsh@redhat.com> 2.3.16-8
- Fix prelink

* Fri Sep 28 2006 Dan Walsh <dwalsh@redhat.com> 2.3.16-7
- Fix rhgb

* Thu Sep 27 2006 Dan Walsh <dwalsh@redhat.com> 2.3.16-6
- Fix setrans handling on MLS and useradd

* Wed Sep 27 2006 Dan Walsh <dwalsh@redhat.com> 2.3.16-5
- Support for fuse
- fix vigr

* Wed Sep 27 2006 Dan Walsh <dwalsh@redhat.com> 2.3.16-4
- Fix dovecot, amanda
- Fix mls

* Mon Sep 25 2006 Dan Walsh <dwalsh@redhat.com> 2.3.16-2
- Allow java execheap for itanium

* Mon Sep 25 2006 Dan Walsh <dwalsh@redhat.com> 2.3.16-1
- Update with upstream

* Mon Sep 25 2006 Dan Walsh <dwalsh@redhat.com> 2.3.15-2
- mls fixes 

* Fri Sep 22 2006 Dan Walsh <dwalsh@redhat.com> 2.3.15-1
- Update from upstream 

* Fri Sep 22 2006 Dan Walsh <dwalsh@redhat.com> 2.3.14-8
- More fixes for mls
- Revert change on automount transition to mount

* Wed Sep 20 2006 Dan Walsh <dwalsh@redhat.com> 2.3.14-7
- Fix cron jobs to run under the correct context

* Tue Sep 19 2006 Dan Walsh <dwalsh@redhat.com> 2.3.14-6
- Fixes to make pppd work

* Mon Sep 18 2006 Dan Walsh <dwalsh@redhat.com> 2.3.14-4
- Multiple policy fixes
- Change max categories to 1023

* Sat Sep 16 2006 Dan Walsh <dwalsh@redhat.com> 2.3.14-3
- Fix transition on mcstransd

* Fri Sep 15 2006 Dan Walsh <dwalsh@redhat.com> 2.3.14-2
- Add /dev/em8300 defs

* Fri Sep 15 2006 Dan Walsh <dwalsh@redhat.com> 2.3.14-1
- Upgrade to upstream

* Thu Sep 14 2006 Dan Walsh <dwalsh@redhat.com> 2.3.13-6
- Fix ppp connections from network manager

* Wed Sep 13 2006 Dan Walsh <dwalsh@redhat.com> 2.3.13-5
- Add tty access to all domains boolean
- Fix gnome-pty-helper context for ia64

* Mon Sep 11 2006 Dan Walsh <dwalsh@redhat.com> 2.3.13-4
- Fixed typealias of firstboot_rw_t

* Thu Sep 7 2006 Dan Walsh <dwalsh@redhat.com> 2.3.13-3
- Fix location of xel log files
- Fix handling of sysadm_r -> rpm_exec_t 

* Thu Sep 7 2006 Dan Walsh <dwalsh@redhat.com> 2.3.13-2
- Fixes for autofs, lp

* Wed Sep 6 2006 Dan Walsh <dwalsh@redhat.com> 2.3.13-1
- Update from upstream

* Tue Sep 5 2006 Dan Walsh <dwalsh@redhat.com> 2.3.12-2
- Fixup for test6

* Tue Sep 5 2006 Dan Walsh <dwalsh@redhat.com> 2.3.12-1
- Update to upstream

* Fri Sep 1 2006 Dan Walsh <dwalsh@redhat.com> 2.3.11-1
- Update to upstream

* Fri Sep 1 2006 Dan Walsh <dwalsh@redhat.com> 2.3.10-7
- Fix suspend to disk problems

* Thu Aug 31 2006 Dan Walsh <dwalsh@redhat.com> 2.3.10-6
- Lots of fixes for restarting daemons at the console.

* Wed Aug 30 2006 Dan Walsh <dwalsh@redhat.com> 2.3.10-3
- Fix audit line
- Fix requires line

* Tue Aug 29 2006 Dan Walsh <dwalsh@redhat.com> 2.3.10-1
- Upgrade to upstream

* Mon Aug 28 2006 Dan Walsh <dwalsh@redhat.com> 2.3.9-6
- Fix install problems

* Fri Aug 25 2006 Dan Walsh <dwalsh@redhat.com> 2.3.9-5
- Allow setroubleshoot to getattr on all dirs to gather RPM data

* Thu Aug 24 2006 Dan Walsh <dwalsh@redhat.com> 2.3.9-4
- Set /usr/lib/ia32el/ia32x_loader to unconfined_execmem_exec_t for ia32 platform
- Fix spec for /dev/adsp

* Thu Aug 24 2006 Dan Walsh <dwalsh@redhat.com> 2.3.9-3
- Fix xen tty devices

* Thu Aug 24 2006 Dan Walsh <dwalsh@redhat.com> 2.3.9-2
- Fixes for setroubleshoot

* Wed Aug 23 2006 Dan Walsh <dwalsh@redhat.com> 2.3.9-1
- Update to upstream

* Sun Aug 20 2006 Dan Walsh <dwalsh@redhat.com> 2.3.8-2
- Fixes for stunnel and postgresql
- Update from upstream

* Sat Aug 10 2006 Dan Walsh <dwalsh@redhat.com> 2.3.7-1
- Update from upstream
- More java fixes

* Fri Aug 10 2006 Dan Walsh <dwalsh@redhat.com> 2.3.6-4
- Change allow_execstack to default to on, for RHEL5 Beta.  
  This is required because of a Java compiler problem.
  Hope to turn off for next beta

* Thu Aug 10 2006 Dan Walsh <dwalsh@redhat.com> 2.3.6-3
- Misc fixes

* Wed Aug 9 2006 Dan Walsh <dwalsh@redhat.com> 2.3.6-2
- More fixes for strict policy

* Tue Aug 8 2006 Dan Walsh <dwalsh@redhat.com> 2.3.6-1
- Quiet down anaconda audit messages

* Mon Aug 7 2006 Dan Walsh <dwalsh@redhat.com> 2.3.5-1
- Fix setroubleshootd

* Thu Aug 3 2006 Dan Walsh <dwalsh@redhat.com> 2.3.4-1
- Update to the latest from upstream

* Thu Aug 3 2006 Dan Walsh <dwalsh@redhat.com> 2.3.3-20
- More fixes for xen

* Thu Aug 3 2006 Dan Walsh <dwalsh@redhat.com> 2.3.3-19
- Fix anaconda transitions

* Wed Aug 2 2006 Dan Walsh <dwalsh@redhat.com> 2.3.3-18
- yet more xen rules
 
* Tue Aug 1 2006 Dan Walsh <dwalsh@redhat.com> 2.3.3-17
- more xen rules

* Mon Jul 31 2006 Dan Walsh <dwalsh@redhat.com> 2.3.3-16
- Fixes for Samba

* Sat Jul 29 2006 Dan Walsh <dwalsh@redhat.com> 2.3.3-15
- Fixes for xen

* Fri Jul 28 2006 Dan Walsh <dwalsh@redhat.com> 2.3.3-14
- Allow setroubleshootd to send mail

* Wed Jul 26 2006 Dan Walsh <dwalsh@redhat.com> 2.3.3-13
- Add nagios policy

* Wed Jul 26 2006 Dan Walsh <dwalsh@redhat.com> 2.3.3-12
-  fixes for setroubleshoot

* Wed Jul 26 2006 Dan Walsh <dwalsh@redhat.com> 2.3.3-11
- Added Paul Howarth patch to only load policy packages shipped 
  with this package
- Allow pidof from initrc to ptrace higher level domains
- Allow firstboot to communicate with hal via dbus

* Mon Jul 24 2006 Dan Walsh <dwalsh@redhat.com> 2.3.3-10
- Add policy for /var/run/ldapi

* Sat Jul 22 2006 Dan Walsh <dwalsh@redhat.com> 2.3.3-9
- Fix setroubleshoot policy

* Fri Jul 21 2006 Dan Walsh <dwalsh@redhat.com> 2.3.3-8
- Fixes for mls use of ssh
- named  has a new conf file

* Fri Jul 21 2006 Dan Walsh <dwalsh@redhat.com> 2.3.3-7
- Fixes to make setroubleshoot work

* Wed Jul 19 2006 Dan Walsh <dwalsh@redhat.com> 2.3.3-6
- Cups needs to be able to read domain state off of printer client

* Wed Jul 19 2006 Dan Walsh <dwalsh@redhat.com> 2.3.3-5
- add boolean to allow zebra to write config files

* Tue Jul 18 2006 Dan Walsh <dwalsh@redhat.com> 2.3.3-4
- setroubleshootd fixes

* Mon Jul 17 2006 Dan Walsh <dwalsh@redhat.com> 2.3.3-3
- Allow prelink to read bin_t symlink
- allow xfs to read random devices
- Change gfs to support xattr


* Mon Jul 17 2006 Dan Walsh <dwalsh@redhat.com> 2.3.3-2
- Remove spamassassin_can_network boolean

* Fri Jul 14 2006 Dan Walsh <dwalsh@redhat.com> 2.3.3-1
- Update to upstream
- Fix lpr domain for mls

* Fri Jul 14 2006 Dan Walsh <dwalsh@redhat.com> 2.3.2-4
- Add setroubleshoot policy

* Fri Jul 7 2006 Dan Walsh <dwalsh@redhat.com> 2.3.2-3
- Turn off auditallow on setting booleans

* Fri Jul 7 2006 Dan Walsh <dwalsh@redhat.com> 2.3.2-2
- Multiple fixes

* Fri Jul 7 2006 Dan Walsh <dwalsh@redhat.com> 2.3.2-1
- Update to upstream

* Thu Jun 22 2006 Dan Walsh <dwalsh@redhat.com> 2.3.1-1
- Update to upstream
- Add new class for kernel key ring

* Wed Jun 21 2006 Dan Walsh <dwalsh@redhat.com> 2.2.49-1
- Update to upstream

* Tue Jun 20 2006 Dan Walsh <dwalsh@redhat.com> 2.2.48-1
- Update to upstream

* Tue Jun 20 2006 Dan Walsh <dwalsh@redhat.com> 2.2.47-5
- Break out selinux-devel package

* Fri Jun 16 2006 Dan Walsh <dwalsh@redhat.com> 2.2.47-4
- Add ibmasmfs

* Thu Jun 15 2006 Dan Walsh <dwalsh@redhat.com> 2.2.47-3
- Fix policygentool gen_requires

* Tue Jun 13 2006 Dan Walsh <dwalsh@redhat.com> 2.2.47-1
- Update from Upstream

* Tue Jun 13 2006 Dan Walsh <dwalsh@redhat.com> 2.2.46-2
- Fix spec of realplay

* Tue Jun 13 2006 Dan Walsh <dwalsh@redhat.com> 2.2.46-1
- Update to upstream

* Mon Jun 12 2006 Dan Walsh <dwalsh@redhat.com> 2.2.45-3
- Fix semanage

* Mon Jun 12 2006 Dan Walsh <dwalsh@redhat.com> 2.2.45-2
- Allow useradd to create_home_dir in MLS environment

* Thu Jun 8 2006 Dan Walsh <dwalsh@redhat.com> 2.2.45-1
- Update from upstream

* Tue Jun 6 2006 Dan Walsh <dwalsh@redhat.com> 2.2.44-1
- Update from upstream

* Tue Jun 6 2006 Dan Walsh <dwalsh@redhat.com> 2.2.43-4
- Add oprofilefs

* Sun May 28 2006 Dan Walsh <dwalsh@redhat.com> 2.2.43-3
- Fix for hplip and Picasus

* Sat May 27 2006 Dan Walsh <dwalsh@redhat.com> 2.2.43-2
- Update to upstream

* Fri May 26 2006 Dan Walsh <dwalsh@redhat.com> 2.2.43-1
- Update to upstream

* Fri May 26 2006 Dan Walsh <dwalsh@redhat.com> 2.2.42-4
- fixes for spamd

* Wed May 24 2006 Dan Walsh <dwalsh@redhat.com> 2.2.42-3
- fixes for java, openldap and webalizer

* Mon May 22 2006 Dan Walsh <dwalsh@redhat.com> 2.2.42-2
- Xen fixes

* Thu May 18 2006 Dan Walsh <dwalsh@redhat.com> 2.2.42-1
- Upgrade to upstream

* Thu May 18 2006 Dan Walsh <dwalsh@redhat.com> 2.2.41-1
- allow hal to read boot_t files
- Upgrade to upstream

* Wed May 17 2006 Dan Walsh <dwalsh@redhat.com> 2.2.40-2
- allow hal to read boot_t files

* Tue May 16 2006 Dan Walsh <dwalsh@redhat.com> 2.2.40-1
- Update from upstream

* Mon May 15 2006 Dan Walsh <dwalsh@redhat.com> 2.2.39-2
- Fixes for amavis

* Mon May 15 2006 Dan Walsh <dwalsh@redhat.com> 2.2.39-1
- Update from upstream

* Fri May 12 2006 Dan Walsh <dwalsh@redhat.com> 2.2.38-6
- Allow auditctl to search all directories

* Thu May 11 2006 Dan Walsh <dwalsh@redhat.com> 2.2.38-5
- Add acquire service for mono.

* Thu May 11 2006 Dan Walsh <dwalsh@redhat.com> 2.2.38-4
- Turn off allow_execmem boolean
- Allow ftp dac_override when allowed to access users homedirs

* Wed May 10 2006 Dan Walsh <dwalsh@redhat.com> 2.2.38-3
- Clean up spec file
- Transition from unconfined_t to prelink_t

* Mon May 8 2006 Dan Walsh <dwalsh@redhat.com> 2.2.38-2
- Allow execution of cvs command

* Fri May 5 2006 Dan Walsh <dwalsh@redhat.com> 2.2.38-1
- Update to upstream

* Wed May 3 2006 Dan Walsh <dwalsh@redhat.com> 2.2.37-1
- Update to upstream

* Mon May 1 2006 Dan Walsh <dwalsh@redhat.com> 2.2.36-2
- Fix libjvm spec

* Tue Apr 25 2006 Dan Walsh <dwalsh@redhat.com> 2.2.36-1
- Update to upstream

* Tue Apr 25 2006 James Antill <jantill@redhat.com> 2.2.35-2
- Add xm policy
- Fix policygentool

* Mon Apr 24 2006 Dan Walsh <dwalsh@redhat.com> 2.2.35-1
- Update to upstream
- Fix postun to only disable selinux on full removal of the packages

* Fri Apr 21 2006 Dan Walsh <dwalsh@redhat.com> 2.2.34-3
- Allow mono to chat with unconfined

* Thu Apr 20 2006 Dan Walsh <dwalsh@redhat.com> 2.2.34-2
- Allow procmail to sendmail
- Allow nfs to share dosfs

* Thu Apr 20 2006 Dan Walsh <dwalsh@redhat.com> 2.2.34-1
- Update to latest from upstream
- Allow selinux-policy to be removed and kernel not to crash

* Tue Apr 18 2006 Dan Walsh <dwalsh@redhat.com> 2.2.33-1
- Update to latest from upstream
- Add James Antill patch for xen
- Many fixes for pegasus

* Sat Apr 15 2006 Dan Walsh <dwalsh@redhat.com> 2.2.32-2
- Add unconfined_mount_t
- Allow privoxy to connect to httpd_cache
- fix cups labeleing on /var/cache/cups

* Fri Apr 14 2006 Dan Walsh <dwalsh@redhat.com> 2.2.32-1
- Update to latest from upstream

* Fri Apr 14 2006 Dan Walsh <dwalsh@redhat.com> 2.2.31-1
- Update to latest from upstream
- Allow mono and unconfined to talk to initrc_t dbus objects

* Tue Apr 11 2006 Dan Walsh <dwalsh@redhat.com> 2.2.30-2
- Change libraries.fc to stop shlib_t form overriding texrel_shlib_t

* Tue Apr 11 2006 Dan Walsh <dwalsh@redhat.com> 2.2.30-1
- Fix samba creating dirs in homedir
- Fix NFS so its booleans would work

* Mon Apr 10 2006 Dan Walsh <dwalsh@redhat.com> 2.2.29-6
- Allow secadm_t ability to relabel all files
- Allow ftp to search xferlog_t directories
- Allow mysql to communicate with ldap
- Allow rsync to bind to rsync_port_t

* Mon Apr 10 2006 Russell Coker <rcoker@redhat.com> 2.2.29-5
- Fixed mailman with Postfix #183928
- Allowed semanage to create file_context files.
- Allowed amanda_t to access inetd_t TCP sockets and allowed amanda_recover_t
  to bind to reserved ports.  #149030
- Don't allow devpts_t to be associated with tmp_t.
- Allow hald_t to stat all mountpoints.
- Added boolean samba_share_nfs to allow smbd_t full access to NFS mounts.
  #169947
- Make mount run in mount_t domain from unconfined_t to prevent mislabeling of
  /etc/mtab.
- Changed the file_contexts to not have a regex before the first ^/[a-z]/
  whenever possible, makes restorecon slightly faster.
- Correct the label of /etc/named.caching-nameserver.conf
- Now label /usr/src/kernels/.+/lib(/.*)? as usr_t instead of
  /usr/src(/.*)?/lib(/.*)? - I don't think we need anything else under /usr/src
  hit by this.
- Granted xen access to /boot, allowed mounting on xend_var_lib_t, and allowed
  xenstored_t rw access to the xen device node.

* Tue Apr 4 2006 Dan Walsh <dwalsh@redhat.com> 2.2.29-4
- More textrel_shlib_t file path fixes
- Add ada support

* Mon Apr 3 2006 Dan Walsh <dwalsh@redhat.com> 2.2.29-3
- Get auditctl working in MLS policy

* Mon Apr 3 2006 Dan Walsh <dwalsh@redhat.com> 2.2.29-2
- Add mono dbus support
- Lots of file_context fixes for textrel_shlib_t in FC5
- Turn off execmem auditallow since they are filling log files

* Fri Mar 30 2006 Dan Walsh <dwalsh@redhat.com> 2.2.29-1
- Update to upstream

* Thu Mar 30 2006 Dan Walsh <dwalsh@redhat.com> 2.2.28-3
- Allow automount and dbus to read cert files

* Thu Mar 30 2006 Dan Walsh <dwalsh@redhat.com> 2.2.28-2
- Fix ftp policy
- Fix secadm running of auditctl

* Mon Mar 27 2006 Dan Walsh <dwalsh@redhat.com> 2.2.28-1
- Update to upstream

* Wed Mar 22 2006 Dan Walsh <dwalsh@redhat.com> 2.2.27-1
- Update to upstream

* Wed Mar 22 2006 Dan Walsh <dwalsh@redhat.com> 2.2.25-3
- Fix policyhelp

* Wed Mar 22 2006 Dan Walsh <dwalsh@redhat.com> 2.2.25-2
- Fix pam_console handling of usb_device
- dontaudit logwatch reading /mnt dir

* Fri Mar 17 2006 Dan Walsh <dwalsh@redhat.com> 2.2.24-1
- Update to upstream

* Wed Mar 15 2006 Dan Walsh <dwalsh@redhat.com> 2.2.23-19
- Get transition rules to create policy.20 at SystemHigh

* Tue Mar 14 2006 Dan Walsh <dwalsh@redhat.com> 2.2.23-18
- Allow secadmin to shutdown system
- Allow sendmail to exec newalias

* Tue Mar 14 2006 Dan Walsh <dwalsh@redhat.com> 2.2.23-17
- MLS Fixes
     dmidecode needs mls_file_read_up
- add ypxfr_t
- run init needs access to nscd
- udev needs setuid
- another xen log file
- Dontaudit mount getattr proc_kcore_t

* Tue Mar 14 2006 Karsten Hopp <karsten@redhat.de> 2.2.23-16
- fix buildroot usage (#185391)

* Thu Mar 9 2006 Dan Walsh <dwalsh@redhat.com> 2.2.23-15
- Get rid of mount/fsdisk scan of /dev messages
- Additional fixes for suspend/resume

* Thu Mar 9 2006 Dan Walsh <dwalsh@redhat.com> 2.2.23-14
- Fake make to rebuild enableaudit.pp

* Thu Mar 9 2006 Dan Walsh <dwalsh@redhat.com> 2.2.23-13
- Get xen networking running.

* Thu Mar 9 2006 Dan Walsh <dwalsh@redhat.com> 2.2.23-12
- Fixes for Xen
- enableaudit should not be the same as base.pp
- Allow ps to work for all process

* Thu Mar  9 2006 Jeremy Katz <katzj@redhat.com> - 2.2.23-11
- more xen policy fixups

* Wed Mar  8 2006 Jeremy Katz <katzj@redhat.com> - 2.2.23-10
- more xen fixage (#184393)

* Wed Mar 8 2006 Dan Walsh <dwalsh@redhat.com> 2.2.23-9
- Fix blkid specification
- Allow postfix to execute mailman_que

* Wed Mar 8 2006 Dan Walsh <dwalsh@redhat.com> 2.2.23-8
- Blkid changes
- Allow udev access to usb_device_t
- Fix post script to create targeted policy config file

* Wed Mar 8 2006 Dan Walsh <dwalsh@redhat.com> 2.2.23-7
- Allow lvm tools to create drevice dir

* Tue Mar 7 2006 Dan Walsh <dwalsh@redhat.com> 2.2.23-5
- Add Xen support

* Mon Mar 6 2006 Dan Walsh <dwalsh@redhat.com> 2.2.23-4
- Fixes for cups
- Make cryptosetup work with hal

* Sun Mar 5 2006 Dan Walsh <dwalsh@redhat.com> 2.2.23-3
- Load Policy needs translock

* Sat Mar 4 2006 Dan Walsh <dwalsh@redhat.com> 2.2.23-2
- Fix cups html interface

* Sat Mar 4 2006 Dan Walsh <dwalsh@redhat.com> 2.2.23-1
- Add hal changes suggested by Jeremy
- add policyhelp to point at policy html pages

* Mon Feb 27 2006 Dan Walsh <dwalsh@redhat.com> 2.2.22-2
- Additional fixes for nvidia and cups

* Mon Feb 27 2006 Dan Walsh <dwalsh@redhat.com> 2.2.22-1
- Update to upstream
- Merged my latest fixes
- Fix cups policy to handle unix domain sockets

* Sat Feb 25 2006 Dan Walsh <dwalsh@redhat.com> 2.2.21-9
- NSCD socket is in nscd_var_run_t needs to be able to search dir

* Fri Feb 24 2006 Dan Walsh <dwalsh@redhat.com> 2.2.21-8
- Fixes Apache interface file

* Fri Feb 24 2006 Dan Walsh <dwalsh@redhat.com> 2.2.21-7
- Fixes for new version of cups

* Fri Feb 24 2006 Dan Walsh <dwalsh@redhat.com> 2.2.21-6
- Turn off polyinstatiate util after FC5

* Fri Feb 24 2006 Dan Walsh <dwalsh@redhat.com> 2.2.21-5
- Fix problem with privoxy talking to Tor

* Thu Feb 22 2006 Dan Walsh <dwalsh@redhat.com> 2.2.21-4
- Turn on polyinstatiation

* Thu Feb 22 2006 Dan Walsh <dwalsh@redhat.com> 2.2.21-3
- Don't transition from unconfined_t to fsadm_t

* Thu Feb 22 2006 Dan Walsh <dwalsh@redhat.com> 2.2.21-2
- Fix policy update model.

* Thu Feb 22 2006 Dan Walsh <dwalsh@redhat.com> 2.2.21-1
- Update to upstream

* Wed Feb 22 2006 Dan Walsh <dwalsh@redhat.com> 2.2.20-1
- Fix load_policy to work on MLS
- Fix cron_rw_system_pipes for postfix_postdrop_t
- Allow audotmount to run showmount

* Tue Feb 21 2006 Dan Walsh <dwalsh@redhat.com> 2.2.19-2
- Fix swapon
- allow httpd_sys_script_t to be entered via a shell
- Allow httpd_sys_script_t to read eventpolfs

* Tue Feb 21 2006 Dan Walsh <dwalsh@redhat.com> 2.2.19-1
- Update from upstream

* Tue Feb 21 2006 Dan Walsh <dwalsh@redhat.com> 2.2.18-2
- allow cron to read apache files

* Tue Feb 21 2006 Dan Walsh <dwalsh@redhat.com> 2.2.18-1
- Fix vpnc policy to work from NetworkManager

* Mon Feb 20 2006 Dan Walsh <dwalsh@redhat.com> 2.2.17-2
- Update to upstream
- Fix semoudle polcy

* Thu Feb 16 2006 Dan Walsh <dwalsh@redhat.com> 2.2.16-1
- Update to upstream 
- fix sysconfig/selinux link

* Wed Feb 15 2006 Dan Walsh <dwalsh@redhat.com> 2.2.15-4
- Add router port for zebra
- Add imaze port for spamd
- Fixes for amanda and java

* Tue Feb 14 2006 Dan Walsh <dwalsh@redhat.com> 2.2.15-3
- Fix bluetooth handling of usb devices
- Fix spamd reading of ~/
- fix nvidia spec

* Tue Feb 14 2006 Dan Walsh <dwalsh@redhat.com> 2.2.15-1
- Update to upsteam

* Mon Feb 13 2006 Dan Walsh <dwalsh@redhat.com> 2.2.14-2
- Add users_extra files

* Fri Feb 10 2006 Dan Walsh <dwalsh@redhat.com> 2.2.14-1
- Update to upstream

* Fri Feb 10 2006 Dan Walsh <dwalsh@redhat.com> 2.2.13-1
- Add semodule policy

* Tue Feb 7 2006 Dan Walsh <dwalsh@redhat.com> 2.2.12-1
- Update from upstream


* Mon Feb 6 2006 Dan Walsh <dwalsh@redhat.com> 2.2.11-2
- Fix for spamd to use razor port

* Fri Feb 3 2006 Dan Walsh <dwalsh@redhat.com> 2.2.11-1
- Fixes for mcs
- Turn on mount and fsadm for unconfined_t

* Wed Feb 1 2006 Dan Walsh <dwalsh@redhat.com> 2.2.10-1
- Fixes for the -devel package

* Wed Feb 1 2006 Dan Walsh <dwalsh@redhat.com> 2.2.9-2
- Fix for spamd to use ldap

* Fri Jan 27 2006 Dan Walsh <dwalsh@redhat.com> 2.2.9-1
- Update to upstream

* Fri Jan 27 2006 Dan Walsh <dwalsh@redhat.com> 2.2.8-2
- Update to upstream
- Fix rhgb, and other Xorg startups

* Thu Jan 26 2006 Dan Walsh <dwalsh@redhat.com> 2.2.7-1
- Update to upstream

* Thu Jan 26 2006 Dan Walsh <dwalsh@redhat.com> 2.2.6-3
- Separate out role of secadm for mls

* Thu Jan 26 2006 Dan Walsh <dwalsh@redhat.com> 2.2.6-2
- Add inotifyfs handling

* Thu Jan 26 2006 Dan Walsh <dwalsh@redhat.com> 2.2.6-1
- Update to upstream
- Put back in changes for pup/zen

* Tue Jan 24 2006 Dan Walsh <dwalsh@redhat.com> 2.2.5-1
- Many changes for MLS 
- Turn on strict policy

* Mon Jan 23 2006 Dan Walsh <dwalsh@redhat.com> 2.2.4-1
- Update to upstream

* Wed Jan 18 2006 Dan Walsh <dwalsh@redhat.com> 2.2.3-1
- Update to upstream
- Fixes for booting and logging in on MLS machine

* Wed Jan 18 2006 Dan Walsh <dwalsh@redhat.com> 2.2.2-1
- Update to upstream
- Turn off execheap execstack for unconfined users
- Add mono/wine policy to allow execheap and execstack for them
- Add execheap for Xdm policy

* Wed Jan 18 2006 Dan Walsh <dwalsh@redhat.com> 2.2.1-1
- Update to upstream
- Fixes to fetchmail,

* Tue Jan 17 2006 Dan Walsh <dwalsh@redhat.com> 2.1.13-1
- Update to upstream

* Tue Jan 17 2006 Dan Walsh <dwalsh@redhat.com> 2.1.12-3
- Fix for procmail/spamassasin
- Update to upstream
- Add rules to allow rpcd to work with unlabeled_networks.

* Sat Jan 14 2006 Dan Walsh <dwalsh@redhat.com> 2.1.11-1
- Update to upstream
- Fix ftp Man page

* Fri Jan 13 2006 Dan Walsh <dwalsh@redhat.com> 2.1.10-1
- Update to upstream

* Wed Jan 11 2006 Jeremy Katz <katzj@redhat.com> - 2.1.9-2
- fix pup transitions (#177262)
- fix xen disks (#177599)

* Tue Jan 10 2006 Dan Walsh <dwalsh@redhat.com> 2.1.9-1
- Update to upstream

* Tue Jan 10 2006 Dan Walsh <dwalsh@redhat.com> 2.1.8-3
- More Fixes for hal and readahead

* Mon Jan 9 2006 Dan Walsh <dwalsh@redhat.com> 2.1.8-2
- Fixes for hal and readahead

* Mon Jan 9 2006 Dan Walsh <dwalsh@redhat.com> 2.1.8-1
- Update to upstream
- Apply 
* Fri Jan 7 2006 Dan Walsh <dwalsh@redhat.com> 2.1.7-4
- Add wine and fix hal problems

* Thu Jan 6 2006 Dan Walsh <dwalsh@redhat.com> 2.1.7-3
- Handle new location of hal scripts

* Thu Jan 5 2006 Dan Walsh <dwalsh@redhat.com> 2.1.7-2
- Allow su to read /etc/mtab

* Wed Jan 4 2006 Dan Walsh <dwalsh@redhat.com> 2.1.7-1
- Update to upstream

* Tue Jan 3 2006 Dan Walsh <dwalsh@redhat.com> 2.1.6-24
- Fix  "libsemanage.parse_module_headers: Data did not represent a module." problem

* Tue Jan 3 2006 Dan Walsh <dwalsh@redhat.com> 2.1.6-23
- Allow load_policy to read /etc/mtab

* Mon Jan 2 2006 Dan Walsh <dwalsh@redhat.com> 2.1.6-22
- Fix dovecot to allow dovecot_auth to look at /tmp

* Mon Jan 2 2006 Dan Walsh <dwalsh@redhat.com> 2.1.6-21
- Allow restorecon to read unlabeled_t directories in order to fix labeling.

* Fri Dec 30 2005 Dan Walsh <dwalsh@redhat.com> 2.1.6-20
- Add Logwatch policy

* Wed Dec 28 2005 Dan Walsh <dwalsh@redhat.com> 2.1.6-18
- Fix /dev/ub[a-z] file context

* Tue Dec 27 2005 Dan Walsh <dwalsh@redhat.com> 2.1.6-17
- Fix library specification
- Give kudzu execmem privs

* Thu Dec 22 2005 Dan Walsh <dwalsh@redhat.com> 2.1.6-16
- Fix hostname in targeted policy

* Wed Dec 21 2005 Dan Walsh <dwalsh@redhat.com> 2.1.6-15
- Fix passwd command on mls

* Wed Dec 21 2005 Dan Walsh <dwalsh@redhat.com> 2.1.6-14
- Lots of fixes to make mls policy work

* Tue Dec 20 2005 Dan Walsh <dwalsh@redhat.com> 2.1.6-13
- Add dri libs to textrel_shlib_t
- Add system_r role for java
- Add unconfined_exec_t for vncserver
- Allow slapd to use kerberos

* Mon Dec 19 2005 Dan Walsh <dwalsh@redhat.com> 2.1.6-11
- Add man pages

* Fri Dec 16 2005 Dan Walsh <dwalsh@redhat.com> 2.1.6-10
- Add enableaudit.pp

* Fri Dec 16 2005 Dan Walsh <dwalsh@redhat.com> 2.1.6-9
- Fix mls policy

* Fri Dec 16 2005 Dan Walsh <dwalsh@redhat.com> 2.1.6-8
- Update mls file from old version

* Thu Dec 15 2005 Dan Walsh <dwalsh@redhat.com> 2.1.6-5
- Add sids back in
- Rebuild with update checkpolicy

* Thu Dec 15 2005 Dan Walsh <dwalsh@redhat.com> 2.1.6-4
- Fixes to allow automount to use portmap
- Fixes to start kernel in s0-s15:c0.c255

* Wed Dec 14 2005 Dan Walsh <dwalsh@redhat.com> 2.1.6-3
- Add java unconfined/execmem policy 

* Wed Dec 14 2005 Dan Walsh <dwalsh@redhat.com> 2.1.6-2
- Add file context for /var/cvs
- Dontaudit webalizer search of homedir

* Tue Dec 13 2005 Dan Walsh <dwalsh@redhat.com> 2.1.6-1
- Update from upstream

* Tue Dec 13 2005 Dan Walsh <dwalsh@redhat.com> 2.1.4-2
- Clean up spec
- range_transition crond to SystemHigh

* Mon Dec 12 2005 Dan Walsh <dwalsh@redhat.com> 2.1.4-1
- Fixes for hal
- Update to upstream

* Mon Dec 12 2005 Dan Walsh <dwalsh@redhat.com> 2.1.3-1
- Turn back on execmem since we need it for java, firefox, ooffice
- Allow gpm to stream socket to itself

* Mon Dec 12 2005 Jeremy Katz <katzj@redhat.com> - 2.1.2-3
- fix requirements to be on the actual packages so that policy can get
  created properly at install time

* Sun Dec  10 2005 Dan Walsh <dwalsh@redhat.com> 2.1.2-2
- Allow unconfined_t to execmod texrel_shlib_t

* Sat Dec  9 2005 Dan Walsh <dwalsh@redhat.com> 2.1.2-1
- Update to upstream 
- Turn off allow_execmem and allow_execmod booleans
- Add tcpd and automount policies

* Fri Dec  8 2005 Dan Walsh <dwalsh@redhat.com> 2.1.1-3
- Add two new httpd booleans, turned off by default
     * httpd_can_network_relay
     * httpd_can_network_connect_db

* Fri Dec  8 2005 Dan Walsh <dwalsh@redhat.com> 2.1.1-2
- Add ghost for policy.20

* Thu Dec  8 2005 Dan Walsh <dwalsh@redhat.com> 2.1.1-1
- Update to upstream
- Turn off boolean allow_execstack

* Thu Dec  8 2005 Dan Walsh <dwalsh@redhat.com> 2.1.0-3
- Change setrans-mls to use new libsetrans
- Add default_context rule for xdm

* Thu Dec  8 2005 Dan Walsh <dwalsh@redhat.com> 2.1.0-2.
- Change Requires to PreReg for requiring of policycoreutils on install

* Wed Dec  7 2005 Dan Walsh <dwalsh@redhat.com> 2.1.0-1.
- New upstream release

* Wed Dec  7 2005 Dan Walsh <dwalsh@redhat.com> 2.0.11-2.
Add xdm policy

* Tue Dec  6 2005 Dan Walsh <dwalsh@redhat.com> 2.0.11-1.
Update from upstream

* Fri Dec  2 2005 Dan Walsh <dwalsh@redhat.com> 2.0.9-1.
Update from upstream

* Fri Dec  2 2005 Dan Walsh <dwalsh@redhat.com> 2.0.8-1.
Update from upstream

* Fri Dec  2 2005 Dan Walsh <dwalsh@redhat.com> 2.0.7-3
- Also trigger to rebuild policy for versions up to 2.0.7.

* Tue Nov 29 2005 Dan Walsh <dwalsh@redhat.com> 2.0.7-2
- No longer installing policy.20 file, anaconda handles the building of the app.

* Tue Nov 29 2005 Dan Walsh <dwalsh@redhat.com> 2.0.6-2
- Fixes for dovecot and saslauthd

* Wed Nov 23 2005 Dan Walsh <dwalsh@redhat.com> 2.0.5-4
- Cleanup pegasus and named 
- Fix spec file
- Fix up passwd changing applications

* Tue Nov 21 2005 Dan Walsh <dwalsh@redhat.com> 2.0.5-1
-Update to latest from upstream

* Tue Nov 21 2005 Dan Walsh <dwalsh@redhat.com> 2.0.4-1
- Add rules for pegasus and avahi

* Mon Nov 21 2005 Dan Walsh <dwalsh@redhat.com> 2.0.2-2
- Start building MLS Policy

* Fri Nov 18 2005 Dan Walsh <dwalsh@redhat.com> 2.0.2-1
- Update to upstream

* Wed Nov 9 2005 Dan Walsh <dwalsh@redhat.com> 2.0.1-2
- Turn on bash

* Wed Nov 9 2005 Dan Walsh <dwalsh@redhat.com> 2.0.1-1
- Initial version
