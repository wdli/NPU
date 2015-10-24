%define distro redhat
%define polyinstatiate n
%define monolithic n
%if %{?BUILD_DOC:0}%{!?BUILD_DOC:1}
%define BUILD_DOC 1
%endif
%if %{?BUILD_TARGETED:0}%{!?BUILD_TARGETED:1}
%define BUILD_TARGETED 1
%endif
%if %{?BUILD_MINIMUM:0}%{!?BUILD_MINIMUM:1}
%define BUILD_MINIMUM 0 
%endif
%if %{?BUILD_MLS:0}%{!?BUILD_MLS:1}
%define BUILD_MLS 0
%endif
%define POLICYVER 29
%define POLICYCOREUTILSVER 2.1.14-74
%define CHECKPOLICYVER 2.1.12-3
Summary: SELinux policy configuration
Name: selinux-policy
Version: 3.13.1
Release: 23%{?dist}
License: GPLv2+
Group: System Environment/Base
Source: serefpolicy-%{version}.tgz
patch: policy-rhel-7.1-base.patch
patch1: policy-rhel-7.1-contrib.patch
patch2: policy-RHEL-7.1-flask.patch
Source1: modules-targeted-base.conf 
Source31: modules-targeted-contrib.conf
Source2: booleans-targeted.conf
Source3: Makefile.devel
Source4: setrans-targeted.conf
Source5: modules-mls-base.conf
Source32: modules-mls-contrib.conf
Source6: booleans-mls.conf
Source8: setrans-mls.conf
Source14: securetty_types-targeted
Source15: securetty_types-mls
#Source16: modules-minimum.conf
Source17: booleans-minimum.conf
Source18: setrans-minimum.conf
Source19: securetty_types-minimum
Source20: customizable_types
Source21: config.tgz
Source22: users-mls
Source23: users-targeted
Source25: users-minimum
Source26: file_contexts.subs_dist
Source27: selinux-policy.conf
Source28: permissivedomains.pp
Source29: serefpolicy-contrib-%{version}.tgz
Source30: booleans.subs_dist
Source33: mypolicy.tar.bz2

Url: http://oss.tresys.com/repos/refpolicy/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
BuildRequires: python gawk checkpolicy >= %{CHECKPOLICYVER} m4 policycoreutils-devel >= %{POLICYCOREUTILSVER} bzip2 
Requires(pre): policycoreutils >= %{POLICYCOREUTILSVER}
Requires(post): /bin/awk /usr/bin/sha512sum

%description 
SELinux Base package

%files 
%defattr(-,root,root,-)
%dir %{_usr}/share/selinux
%dir %{_usr}/share/selinux/packages
%dir %{_sysconfdir}/selinux
%ghost %config(noreplace) %{_sysconfdir}/selinux/config
%ghost %{_sysconfdir}/sysconfig/selinux
%{_usr}/lib/tmpfiles.d/selinux-policy.conf
%attr(0755, root, root) %dir %{_rpmconfigdir}
%attr(0755, root, root) %dir %{_rpmconfigdir}/macros.d
%{_rpmconfigdir}/macros.d/macros.selinux-policy

%package sandbox
Summary: SELinux policy sandbox
Group: System Environment/Base
Requires(pre): selinux-policy-base = %{version}-%{release}

%description sandbox
SELinux sandbox policy used for the policycoreutils-sandbox package

%files sandbox
%defattr(-,root,root,-)
%verify(not md5 size mtime) /usr/share/selinux/packages/sandbox.pp

%post sandbox
rm -f /etc/selinux/*/modules/active/modules/sandbox.pp.disabled 2>/dev/null
semodule -n -i /usr/share/selinux/packages/sandbox.pp
if /usr/sbin/selinuxenabled ; then
    /usr/sbin/load_policy
fi;
exit 0

%preun sandbox
semodule -n -d sandbox 2>/dev/null
if /usr/sbin/selinuxenabled ; then
    /usr/sbin/load_policy
fi;exit 0

%package devel
Summary: SELinux policy devel
Group: System Environment/Base
Requires(pre): selinux-policy = %{version}-%{release}
Requires: m4 checkpolicy >= %{CHECKPOLICYVER}
Requires: /usr/bin/make
Requires(post): policycoreutils-devel >= %{POLICYCOREUTILSVER}

%description devel
SELinux policy development and man page package

%files devel
%defattr(-,root,root,-)
%{_mandir}/man*/*
%{_mandir}/ru/*/*
%dir %{_usr}/share/selinux/devel
%dir %{_usr}/share/selinux/devel/include
%{_usr}/share/selinux/devel/include/*
%dir %{_usr}/share/selinux/devel/html
%{_usr}/share/selinux/devel/html/*html
%{_usr}/share/selinux/devel/html/*css
%{_usr}/share/selinux/devel/Makefile
%{_usr}/share/selinux/devel/example.*
%{_usr}/share/selinux/devel/policy.*

%post devel
selinuxenabled && /usr/bin/sepolgen-ifgen 2>/dev/null 
exit 0

%package doc
Summary: SELinux policy documentation
Group: System Environment/Base
Requires(pre): selinux-policy = %{version}-%{release}
Requires: /usr/bin/xdg-open

%description doc
SELinux policy documentation package

%files doc
%defattr(-,root,root,-)
%doc %{_usr}/share/doc/%{name}
%attr(755,root,root) %{_usr}/share/selinux/devel/policyhelp

%define makeCmds() \
make UNK_PERMS=%4 NAME=%1 TYPE=%2 DISTRO=%{distro} UBAC=n DIRECT_INITRC=%3 MONOLITHIC=%{monolithic} MLS_CATS=1024 MCS_CATS=1024 bare \
make UNK_PERMS=%4 NAME=%1 TYPE=%2 DISTRO=%{distro} UBAC=n DIRECT_INITRC=%3 MONOLITHIC=%{monolithic} MLS_CATS=1024 MCS_CATS=1024  conf \
cp -f selinux_config/booleans-%1.conf ./policy/booleans.conf \
cp -f selinux_config/users-%1 ./policy/users \
#cp -f selinux_config/modules-%1-base.conf  ./policy/modules.conf \

%define makeModulesConf() \
cp -f selinux_config/modules-%1-%2.conf  ./policy/modules-base.conf \
cp -f selinux_config/modules-%1-%2.conf  ./policy/modules.conf \
if [ %3 == "contrib" ];then \
	cp selinux_config/modules-%1-%3.conf ./policy/modules-contrib.conf; \
	cat selinux_config/modules-%1-%3.conf >> ./policy/modules.conf; \
fi; \

%define installCmds() \
make UNK_PERMS=%4 NAME=%1 TYPE=%2 DISTRO=%{distro} UBAC=n DIRECT_INITRC=%3 MONOLITHIC=%{monolithic} MLS_CATS=1024 MCS_CATS=1024 SEMOD_EXP="/usr/bin/semodule_expand -a" base.pp \
make validate UNK_PERMS=%4 NAME=%1 TYPE=%2 DISTRO=%{distro} UBAC=n DIRECT_INITRC=%3 MONOLITHIC=%{monolithic} MLS_CATS=1024 MCS_CATS=1024 SEMOD_EXP="/usr/bin/semodule_expand -a" modules \
make UNK_PERMS=%4 NAME=%1 TYPE=%2 DISTRO=%{distro} UBAC=n DIRECT_INITRC=%3 MONOLITHIC=%{monolithic} DESTDIR=%{buildroot} MLS_CATS=1024 MCS_CATS=1024 install \
make UNK_PERMS=%4 NAME=%1 TYPE=%2 DISTRO=%{distro} UBAC=n DIRECT_INITRC=%3 MONOLITHIC=%{monolithic} DESTDIR=%{buildroot} MLS_CATS=1024 MCS_CATS=1024 install-appconfig \
%{__mkdir} -p %{buildroot}/%{_sysconfdir}/selinux/%1/logins \
%{__mkdir} -p %{buildroot}/%{_sysconfdir}/selinux/%1/policy \
%{__mkdir} -p %{buildroot}/%{_sysconfdir}/selinux/%1/modules/active/modules \
%{__mkdir} -p %{buildroot}/%{_sysconfdir}/selinux/%1/contexts/files \
touch %{buildroot}/%{_sysconfdir}/selinux/%1/modules/semanage.read.LOCK \
touch %{buildroot}/%{_sysconfdir}/selinux/%1/modules/semanage.trans.LOCK \
rm -rf %{buildroot}%{_sysconfdir}/selinux/%1/booleans \
touch %{buildroot}%{_sysconfdir}/selinux/%1/policy/policy.%{POLICYVER} \
touch %{buildroot}%{_sysconfdir}/selinux/%1/contexts/files/file_contexts.subs \
install -m0644 selinux_config/securetty_types-%1 %{buildroot}%{_sysconfdir}/selinux/%1/contexts/securetty_types \
install -m0644 selinux_config/file_contexts.subs_dist %{buildroot}%{_sysconfdir}/selinux/%1/contexts/files \
install -m0644 selinux_config/setrans-%1.conf %{buildroot}%{_sysconfdir}/selinux/%1/setrans.conf \
install -m0644 selinux_config/customizable_types %{buildroot}%{_sysconfdir}/selinux/%1/contexts/customizable_types \
touch %{buildroot}%{_sysconfdir}/selinux/%1/modules/active/seusers \
touch %{buildroot}%{_sysconfdir}/selinux/%1/modules/active/file_contexts.local \
touch %{buildroot}%{_sysconfdir}/selinux/%1/modules/active/nodes.local \
touch %{buildroot}%{_sysconfdir}/selinux/%1/modules/active/users_extra.local \
touch %{buildroot}%{_sysconfdir}/selinux/%1/modules/active/users.local \
touch %{buildroot}%{_sysconfdir}/selinux/%1/modules/active/file_contexts.homedirs.bin \
touch %{buildroot}%{_sysconfdir}/selinux/%1/modules/active/file_contexts.bin \
cp %{SOURCE30} %{buildroot}%{_sysconfdir}/selinux/%1 \
bzip2 -c %{buildroot}/%{_usr}/share/selinux/%1/base.pp  > %{buildroot}/%{_sysconfdir}/selinux/%1/modules/active/base.pp \
rm -f %{buildroot}/%{_usr}/share/selinux/%1/base.pp  \
for i in %{buildroot}/%{_usr}/share/selinux/%1/*.pp; do bzip2 -c $i > %{buildroot}/%{_sysconfdir}/selinux/%1/modules/active/modules/`basename $i`; done \
rm -f %{buildroot}/%{_usr}/share/selinux/%1/*pp*  \
mkdir -p %{buildroot}%{_usr}/share/selinux/packages \
/usr/sbin/semodule -s %1 -n -B -p %{buildroot}; \
/usr/bin/sha512sum %{buildroot}%{_sysconfdir}/selinux/%1/policy/policy.%{POLICYVER} | cut -d' ' -f 1 > %{buildroot}%{_sysconfdir}/selinux/%1/.policy.sha512; \
rm -rf %{buildroot}%{_sysconfdir}/selinux/%1/contexts/netfilter_contexts  \
rm -rf %{buildroot}%{_sysconfdir}/selinux/%1/modules/active/policy.kern \
ln -sf /etc/selinux/%1/policy/policy.%{POLICYVER}  %{buildroot}%{_sysconfdir}/selinux/%1/modules/active/policy.kern \
%nil

%define fileList() \
%defattr(-,root,root) \
%dir %{_usr}/share/selinux/%1 \
%dir %{_sysconfdir}/selinux/%1 \
%config(noreplace) %{_sysconfdir}/selinux/%1/setrans.conf \
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/selinux/%1/seusers \
%dir %{_sysconfdir}/selinux/%1/logins \
%dir %{_sysconfdir}/selinux/%1/modules \
%verify(not md5 size mtime) %{_sysconfdir}/selinux/%1/modules/semanage.read.LOCK \
%verify(not md5 size mtime) %{_sysconfdir}/selinux/%1/modules/semanage.trans.LOCK \
%dir %attr(700,root,root) %dir %{_sysconfdir}/selinux/%1/modules/active \
%dir %{_sysconfdir}/selinux/%1/modules/active/modules \
%verify(not md5 size mtime) %{_sysconfdir}/selinux/%1/modules/active/commit_num \
%verify(not md5 size mtime) %{_sysconfdir}/selinux/%1/modules/active/base.pp \
%verify(not md5 size mtime) %{_sysconfdir}/selinux/%1/modules/active/file_contexts \
%verify(not md5 size mtime) %{_sysconfdir}/selinux/%1/modules/active/file_contexts.homedirs \
%verify(not md5 size mtime) %{_sysconfdir}/selinux/%1/modules/active/file_contexts.template \
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/selinux/%1/modules/active/seusers.final \
%verify(not md5 size mtime) %{_sysconfdir}/selinux/%1/modules/active/netfilter_contexts \
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/selinux/%1/modules/active/users_extra \
%verify(not md5 size mtime) %{_sysconfdir}/selinux/%1/modules/active/homedir_template \
%verify(not md5 size mtime) %{_sysconfdir}/selinux/%1/modules/active/policy.kern \
%ghost %{_sysconfdir}/selinux/%1/modules/active/*.local \
%ghost %{_sysconfdir}/selinux/%1/modules/active/*.bin \
%ghost %{_sysconfdir}/selinux/%1/modules/active/seusers \
%dir %{_sysconfdir}/selinux/%1/policy/ \
%verify(not md5 size mtime) %{_sysconfdir}/selinux/%1/policy/policy.%{POLICYVER} \
%{_sysconfdir}/selinux/%1/.policy.sha512 \
%dir %{_sysconfdir}/selinux/%1/contexts \
%config %{_sysconfdir}/selinux/%1/contexts/customizable_types \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/securetty_types \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/dbus_contexts \
%config %{_sysconfdir}/selinux/%1/contexts/x_contexts \
%config %{_sysconfdir}/selinux/%1/contexts/default_contexts \
%config %{_sysconfdir}/selinux/%1/contexts/virtual_domain_context \
%config %{_sysconfdir}/selinux/%1/contexts/virtual_image_context \
%config %{_sysconfdir}/selinux/%1/contexts/lxc_contexts \
%config %{_sysconfdir}/selinux/%1/contexts/systemd_contexts \
%config %{_sysconfdir}/selinux/%1/contexts/sepgsql_contexts \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/default_type \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/failsafe_context \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/initrc_context \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/removable_context \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/userhelper_context \
%dir %{_sysconfdir}/selinux/%1/contexts/files \
%verify(not md5 size mtime) %{_sysconfdir}/selinux/%1/contexts/files/file_contexts \
%verify(not md5 size mtime) %{_sysconfdir}/selinux/%1/contexts/files/file_contexts.homedirs \
%ghost %{_sysconfdir}/selinux/%1/contexts/files/*.bin \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/files/file_contexts.local \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/files/file_contexts.subs \
%{_sysconfdir}/selinux/%1/contexts/files/file_contexts.subs_dist \
%{_sysconfdir}/selinux/%1/booleans.subs_dist \
%config %{_sysconfdir}/selinux/%1/contexts/files/media \
%dir %{_sysconfdir}/selinux/%1/contexts/users \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/users/root \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/users/guest_u \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/users/xguest_u \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/users/user_u \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/users/staff_u

%define relabel() \
. %{_sysconfdir}/selinux/config; \
FILE_CONTEXT=%{_sysconfdir}/selinux/%1/contexts/files/file_contexts; \
/usr/sbin/selinuxenabled; \
if [ $? = 0  -a "${SELINUXTYPE}" = %1 -a -f ${FILE_CONTEXT}.pre ]; then \
     /sbin/fixfiles -C ${FILE_CONTEXT}.pre restore 2> /dev/null; \
     rm -f ${FILE_CONTEXT}.pre; \
fi; \
if /sbin/restorecon -e /run/media -R /root /var/log /var/run /etc/passwd* /etc/group* /etc/*shadow* 2> /dev/null;then \
    continue; \
fi; \
if /sbin/restorecon -R /home/*/.config 2> /dev/null;then \
    continue; \
fi;

%define preInstall() \
if [ $1 -ne 1 ] && [ -s /etc/selinux/config ]; then \
     . %{_sysconfdir}/selinux/config; \
     FILE_CONTEXT=%{_sysconfdir}/selinux/%1/contexts/files/file_contexts; \
     if [ "${SELINUXTYPE}" = %1 -a -f ${FILE_CONTEXT} ]; then \
        [ -f ${FILE_CONTEXT}.pre ] || cp -f ${FILE_CONTEXT} ${FILE_CONTEXT}.pre; \
     fi; \
     touch /etc/selinux/%1/.rebuild; \
     if [ -e /etc/selinux/%1/.policy.sha512 ]; then \
        POLICY_FILE=`ls /etc/selinux/%1/policy/policy.* | sort | head -1` \
        sha512=`sha512sum $POLICY_FILE | cut -d ' ' -f 1`; \
	checksha512=`cat /etc/selinux/%1/.policy.sha512`; \
	if [ "$sha512" == "$checksha512" ] ; then \
		rm /etc/selinux/%1/.rebuild; \
	fi; \
   fi; \
fi;

%define postInstall() \
. %{_sysconfdir}/selinux/config; \
(cd /etc/selinux/%2/modules/active/modules; rm -f vbetool.pp l2tpd.pp shutdown.pp amavis.pp clamav.pp gnomeclock.pp nsplugin.pp matahari.pp xfs.pp kudzu.pp kerneloops.pp execmem.pp openoffice.pp ada.pp tzdata.pp hal.pp hotplug.pp howl.pp java.pp mono.pp moilscanner.pp gamin.pp audio_entropy.pp audioentropy.pp iscsid.pp polkit_auth.pp polkit.pp rtkit_daemon.pp ModemManager.pp telepathysofiasip.pp ethereal.pp passanger.pp qemu.pp qpidd.pp pyzor.pp razor.pp pki-selinux.pp phpfpm.pp consoletype.pp ctdbd.pp fcoemon.pp isnsd.pp rgmanager.pp corosync.pp aisexec.pp pacemaker.pp pkcsslotd.pp smstools.pp ) \
if [ -e /etc/selinux/%2/.rebuild ]; then \
   rm /etc/selinux/%2/.rebuild; \
   /usr/sbin/semodule -B -n -s %2; \
fi; \
[ "${SELINUXTYPE}" == "%2" ] && selinuxenabled && load_policy; \
if [ %1 -eq 1 ]; then \
   /sbin/restorecon -R /root /var/log /run 2> /dev/null; \
else \
%relabel %2 \
fi;

%define modulesList() \
awk '$1 !~ "/^#/" && $2 == "=" && $3 == "module" { printf "%%s.pp ", $1 }' ./policy/modules-base.conf > %{buildroot}/%{_usr}/share/selinux/%1/modules-base.lst \
awk '$1 !~ "/^#/" && $2 == "=" && $3 == "base" { printf "%%s.pp ", $1 }' ./policy/modules-base.conf > %{buildroot}/%{_usr}/share/selinux/%1/base.lst \
if [ -e ./policy/modules-contrib.conf ];then \
	awk '$1 !~ "/^#/" && $2 == "=" && $3 == "module" { printf "%%s.pp ", $1 }' ./policy/modules-contrib.conf > %{buildroot}/%{_usr}/share/selinux/%1/modules-contrib.lst; \
fi;

%define nonBaseModulesList() \
contrib_modules=`cat %{buildroot}/%{_usr}/share/selinux/%1/modules-contrib.lst` \
base_modules=`cat %{buildroot}/%{_usr}/share/selinux/%1/modules-base.lst` \
for i in $contrib_modules $base_modules; do \
    if [ $i != "sandbox.pp" ];then \
        echo "%verify(not md5 size mtime) /etc/selinux/%1/modules/active/modules/$i" >> %{buildroot}/%{_usr}/share/selinux/%1/nonbasemodules.lst \
    fi; \
done

%description
SELinux Reference Policy - modular.
Based off of reference policy: Checked out revision  2.20091117

%build

%prep 
%setup -n serefpolicy-contrib-%{version} -q -b 29
%patch1 -p1
contrib_path=`pwd`
%setup -n serefpolicy-%{version} -q
cd $RPM_BUILD_DIR/serefpolicy-%{version};tar -xjf %{SOURCE33}
exec 1>/dev/null 2>&1
%patch -p1
refpolicy_path=`pwd`
cp $contrib_path/* $refpolicy_path/policy/modules/contrib
rm -rf $refpolicy_path/policy/modules/contrib/kubernetes.*

%install
mkdir selinux_config
for i in %{SOURCE1} %{SOURCE2} %{SOURCE3} %{SOURCE4} %{SOURCE5} %{SOURCE6} %{SOURCE8} %{SOURCE14} %{SOURCE15} %{SOURCE17} %{SOURCE18} %{SOURCE19} %{SOURCE20} %{SOURCE21} %{SOURCE22} %{SOURCE23} %{SOURCE25} %{SOURCE26} %{SOURCE31} %{SOURCE32};do
 cp $i selinux_config
done
tar zxvf selinux_config/config.tgz
# Build targeted policy
%{__rm} -fR %{buildroot}
mkdir -p %{buildroot}%{_sysconfdir}/selinux
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
touch %{buildroot}%{_sysconfdir}/selinux/config
touch %{buildroot}%{_sysconfdir}/sysconfig/selinux
mkdir -p %{buildroot}%{_usr}/lib/tmpfiles.d/
cp %{SOURCE27} %{buildroot}%{_usr}/lib/tmpfiles.d/

# Always create policy module package directories
mkdir -p %{buildroot}%{_usr}/share/selinux/{targeted,mls,minimum,modules}/

# Install devel
make clean
%if %{BUILD_TARGETED}
# Build targeted policy
# Commented out because only targeted ref policy currently builds
mkdir -p %{buildroot}%{_usr}/share/selinux/targeted
cp %{SOURCE28} %{buildroot}/%{_usr}/share/selinux/targeted
%makeCmds targeted mcs n allow
%makeModulesConf targeted base contrib
%installCmds targeted mcs n allow
mv %{buildroot}/%{_sysconfdir}/selinux/targeted/modules/active/modules/sandbox.pp %{buildroot}/usr/share/selinux/packages
%modulesList targeted 
%nonBaseModulesList targeted
%endif

%if %{BUILD_MINIMUM}
# Build minimum policy
# Commented out because only minimum ref policy currently builds
mkdir -p %{buildroot}%{_usr}/share/selinux/minimum
cp %{SOURCE28} %{buildroot}/%{_usr}/share/selinux/minimum
%makeCmds minimum mcs n allow
%makeModulesConf targeted base contrib
%installCmds minimum mcs n allow
rm -f %{buildroot}/%{_sysconfdir}/selinux/minimum/modules/active/modules/sandbox.pp
%modulesList minimum
%nonBaseModulesList minimum
%endif

%if %{BUILD_MLS}
# Build mls policy
%makeCmds mls mls n deny
%makeModulesConf mls base contrib
%installCmds mls mls n deny
%modulesList mls
%nonBaseModulesList mls
%endif

mkdir -p %{buildroot}%{_mandir}
cp -R  man/* %{buildroot}%{_mandir}
make UNK_PERMS=allow NAME=targeted TYPE=mcs DISTRO=%{distro} UBAC=n DIRECT_INITRC=n MONOLITHIC=%{monolithic} DESTDIR=%{buildroot} PKGNAME=%{name} MLS_CATS=1024 MCS_CATS=1024 install-docs
make UNK_PERMS=allow NAME=targeted TYPE=mcs DISTRO=%{distro} UBAC=n DIRECT_INITRC=n MONOLITHIC=%{monolithic} DESTDIR=%{buildroot} PKGNAME=%{name} MLS_CATS=1024 MCS_CATS=1024 install-headers
mkdir %{buildroot}%{_usr}/share/selinux/devel/
mv %{buildroot}%{_usr}/share/selinux/targeted/include %{buildroot}%{_usr}/share/selinux/devel/include
install -m 644 selinux_config/Makefile.devel %{buildroot}%{_usr}/share/selinux/devel/Makefile
install -m 644 doc/example.* %{buildroot}%{_usr}/share/selinux/devel/
install -m 644 doc/policy.* %{buildroot}%{_usr}/share/selinux/devel/
echo  "xdg-open file:///usr/share/doc/selinux-policy/html/index.html"> %{buildroot}%{_usr}/share/selinux/devel/policyhelp
chmod +x %{buildroot}%{_usr}/share/selinux/devel/policyhelp
/usr/bin/sepolicy manpage -a -p %{buildroot}/usr/share/man/man8/ -w -r %{buildroot}
mkdir %{buildroot}%{_usr}/share/selinux/devel/html
htmldir=`compgen -d %{buildroot}%{_usr}/share/man/man8/`
mv ${htmldir}/* %{buildroot}%{_usr}/share/selinux/devel/html
mv %{buildroot}%{_usr}/share/man/man8/index.html %{buildroot}%{_usr}/share/selinux/devel/html
mv %{buildroot}%{_usr}/share/man/man8/style.css %{buildroot}%{_usr}/share/selinux/devel/html
rm -rf ${htmldir}

mkdir -p %{buildroot}%{_rpmconfigdir}/macros.d
echo '%%_selinux_policy_version %{version}-%{release}' > %{buildroot}%{_rpmconfigdir}/macros.d/macros.selinux-policy

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
# SELINUXTYPE= can take one of three two values:
#     targeted - Targeted processes are protected,
#     minimum - Modification of targeted policy. Only selected processes are protected. 
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
Conflicts:  389-ds-base < 1.2.7, 389-admin < 1.1.12
Conflicts:	pki-selinux < 10.0.0-0.45.b1
Conflicts:  freeipa-server-selinux < 3.2.2-1

%description targeted
SELinux Reference policy targeted base module.

%pre targeted
%preInstall targeted

%post targeted
%postInstall $1 targeted
exit 0

%triggerin -- pcre
selinuxenabled && semodule -nB
exit 0

%triggerpostun -- selinux-policy-targeted < 3.12.1-74
rm -f /etc/selinux/*/modules/active/modules/sandbox.pp.disabled 2>/dev/null
exit 0

%triggerpostun targeted -- selinux-policy-targeted < 3.12.1-75
restorecon -R -p /home
exit 0

%files targeted -f %{buildroot}/%{_usr}/share/selinux/targeted/nonbasemodules.lst
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/selinux/targeted/contexts/users/unconfined_u
%config(noreplace) %{_sysconfdir}/selinux/targeted/contexts/users/sysadm_u 
%fileList targeted
%verify(not md5 size mtime) %{_sysconfdir}/selinux/targeted/modules/active/modules/permissivedomains.pp
%{_usr}/share/selinux/targeted/base.lst
%{_usr}/share/selinux/targeted/modules-base.lst
%{_usr}/share/selinux/targeted/modules-contrib.lst
%{_usr}/share/selinux/targeted/nonbasemodules.lst
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
%preInstall minimum
if [ $1 -ne 1 ]; then
   /usr/sbin/semodule -s minimum -l 2>/dev/null | awk '{ if ($3 != "Disabled") print $1; }' > /usr/share/selinux/minimum/instmodules.lst
fi

%post minimum
contribpackages=`cat /usr/share/selinux/minimum/modules-contrib.lst`
basepackages=`cat /usr/share/selinux/minimum/modules-base.lst`
(cd /etc/selinux/minimum/modules/active/modules; rm -f pkcsslotd.pp)
if [ $1 -eq 1 ]; then
for p in $contribpackages; do
	touch /etc/selinux/minimum/modules/active/modules/$p.disabled
done
for p in $basepackages apache.pp dbus.pp inetd.pp kerberos.pp mta.pp nis.pp; do
	rm -f /etc/selinux/minimum/modules/active/modules/$p.disabled
done
/usr/sbin/semanage import -S minimum -f - << __eof
login -m  -s unconfined_u -r s0-s0:c0.c1023 __default__
login -m  -s unconfined_u -r s0-s0:c0.c1023 root
__eof
/sbin/restorecon -R /root /var/log /var/run 2> /dev/null
/usr/sbin/semodule -B -s minimum
else
instpackages=`cat /usr/share/selinux/minimum/instmodules.lst`
for p in $contribpackages; do
    touch /etc/selinux/minimum/modules/active/modules/$p.disabled
done
for p in $instpackages apache dbus inetd kerberos mta nis; do
    rm -f /etc/selinux/minimum/modules/active/modules/$p.pp.disabled
done
/usr/sbin/semodule -B -s minimum
%relabel minimum
fi
exit 0

%files minimum -f %{buildroot}/%{_usr}/share/selinux/minimum/nonbasemodules.lst
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/selinux/minimum/contexts/users/unconfined_u
%config(noreplace) %{_sysconfdir}/selinux/minimum/contexts/users/sysadm_u
%fileList minimum
%verify(not md5 size mtime) %{_sysconfdir}/selinux/minimum/modules/active/modules/permissivedomains.pp
%{_usr}/share/selinux/minimum/base.lst
%{_usr}/share/selinux/minimum/modules-base.lst
%{_usr}/share/selinux/minimum/modules-contrib.lst
%{_usr}/share/selinux/minimum/nonbasemodules.lst
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
%preInstall mls

%post mls 
%postInstall $1 mls

%files mls -f %{buildroot}/%{_usr}/share/selinux/mls/nonbasemodules.lst
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/selinux/mls/contexts/users/unconfined_u
%fileList mls
%{_usr}/share/selinux/mls/base.lst
%{_usr}/share/selinux/mls/modules-base.lst
%{_usr}/share/selinux/mls/modules-contrib.lst
%{_usr}/share/selinux/mls/nonbasemodules.lst
%endif

%changelog
* Wed Jan 30 2015 Miroslav Grepl <mgrepl@redhat.com> 3.13.1-23
- Update seutil_manage_config() interface.
Resolves:#1185962
- Allow pki-tomcat relabel pki_tomcat_etc_rw_t.
- Turn on docker_transition_unconfined by default

* Wed Jan 28 2015 Miroslav Grepl <mgrepl@redhat.com> 3.13.1-22
- Allow virtd to list all mountpoints.
Resolves:#1180713

* Wed Jan 28 2015 Miroslav Grepl <mgrepl@redhat.com> 3.13.1-21
- pkcsslotd_lock_t should be an alias for pkcs_slotd_lock_t.
- Allow fowner capability for sssd because of selinux_child handling.
- ALlow bind to read/write inherited ipsec pipes
- Allow hypervkvp to read /dev/urandom and read  addition states/config files.
- Allow gluster rpm scripletto create glusterd socket with correct labeling. This is a workaround until we get fix in glusterd.
- Add glusterd_filetrans_named_pid() interface
- Allow radiusd to connect to radsec ports.
- Allow setuid/setgid for selinux_child
- Allow lsmd plugin to connect to tcp/5988 by default.
- Allow lsmd plugin to connect to tcp/5989 by default.
- Update ipsec_manage_pid() interface.
Resolves:#1184978

* Wed Jan 23 2015 Miroslav Grepl <mgrepl@redhat.com> 3.13.1-20
- Update ipsec_manage_pid() interface.
Resolves:#1184978

* Wed Jan 21 2015 Miroslav Grepl <mgrepl@redhat.com> 3.13.1-19
- Allow ntlm_auth running in winbind_helper_t to access /dev/urandom.

* Wed Jan 21 2015 Miroslav Grepl <mgrepl@redhat.com> 3.13.1-18
- Add auditing support for ipsec.
Resolves:#1182524
- Label /ostree/deploy/rhel-atomic-host/deploy directory as system_conf_t
- Allow netutils chown capability to make tcpdump working with -w

* Tue Jan 20 2015 Miroslav Grepl <mgrepl@redhat.com> 3.13.1-17
- Allow ipsec to execute _updown.netkey script to run unbound-control.
- Allow neutron to read rpm DB.
- Add additional fixes for hyperkvp
 * creates new ifcfg-{name} file
 * Runs hv_set_ifconfig.sh, which does the following
 * Copies ifcfg-{name} to /etc/sysconfig/network-scripts
- Allow svirt to read symbolic links in /sys/fs/cgroups labeled as tmpfs_t
- Add labeling for pacemaker.log.
- Allow radius to connect/bind radsec ports.
- Allow pm-suspend running as virt_qemu_ga to read /var/log/pm-suspend.log
- Allow  virt_qemu_ga to dbus chat with rpm.
- Update virt_read_content() interface to allow read also char devices.
- Allow glance-registry to connect to keystone port.
Resolves:#1181818

* Mon Jan 12 2015 Miroslav Grepl <mgrepl@redhat.com> 3.13.1-16
- Allow sssd to send dbus all user domains.
Resolves:#1172291
- Allow lsm plugin to read certificates.
- Fix labeling for keystone CGI scripts.
- Make snapperd back as unconfined domain.

* Fri Jan 9 2015 Miroslav Grepl <mgrepl@redhat.com> 3.13.1-15
- Fix bugs in interfaces discovered by sepolicy.
- Allow slapd to read /usr/share/cracklib/pw_dict.hwm.
- Allow lsm plugins to connect to tcp/18700 by default.
- Allow brltty mknod capability to allow create /var/run/brltty/vcsa.
- Fix pcp_domain_template() interface.
- Fix conman.te.
- Allow mon_fsstatd to read /proc/sys/fs/binfmt_misc
- Allow glance-scrubber to connect tcp/9191.
- Add missing setuid capability for sblim-sfcbd.
- Allow pegasus ioctl() on providers.
- Add conman_can_network.
- Allow chronyd to read chrony conf files located in /run/timemaster/.
- Allow radius to bind on tcp/1813 port.
- dontaudit block suspend access for openvpn_t 
- Allow conman to create files/dirs in /tmp.
- Update xserver_rw_xdm_keys() interface to have 'setattr'.
Resolves:#1172291 
- Allow sulogin to read /dev/urandom and /dev/random.
- Update radius port definition to have also tcp/18121
- Label prandom as random_device_t.
- Allow charon to manage files in /etc/strongimcv labeled as ipsec_conf_t.

* Fri Dec 12 2014 Miroslav Grepl <mgrepl@redhat.com> 3.13.1-14
- Allow virt_qemu_ga_t to execute kmod.
- Add missing files_dontaudit_list_security_dirs() for smbd_t in samba_export_all_ro boolean.
- Add additionnal MLS attribute for oddjob_mkhomedir to create homedirs.
Resolves:#1113725
- Enable OpenStack cinder policy
- Add support for /usr/share/vdsm/daemonAdapter
- Add support for /var/run/gluster

* Tue Dec 2 2014 Miroslav Grepl <mgrepl@redhat.com> 3.13.1-13
- Remove old pkcsslotd.pp from minimum package
- Allow rlogind to use also rlogin ports.
- Add support for /usr/libexec/ntpdate-wrapper. Label it as ntpdate_exec_t.
- Allow bacula to connect also to postgresql.
- Label /usr/libexec/tomcat/server as tomcat_exec_t
- Add support for /usr/sbin/ctdbd_wrapper
- Add support for /usr/libexec/ppc64-diag/rtas_errd
- Allow rpm_script_roles to access system_mail_t
- Allow brltty to create /var/run/brltty
- Allow lsmd plugin to access netlink_route_socket
- Allow smbcontrol to read passwd
- Add support for /usr/libexec/sssd/selinux_child and create sssd_selinux_manager_t domain for it
Resolves:#1140106
- Allow osad to execute rhn_check
- Allow load_policy to rw inherited sssd pipes because of selinux_child
- Allow admin SELinux users mounting / as private within a new mount namespace as root in MLS
- Add additional fixes for su_restricted_domain_template to make moving to sysadm_r and trying to su working correctly
- Add additional booleans substitions

* Tue Nov 25 2014 Miroslav Grepl <mgrepl@redhat.com> 3.13.1-12
- Add seutil_dontaudit_access_check_semanage_module_store() interface
Resolves:#1140106
- Update to have all _systemctl() interface also init_reload_services().
- Dontaudit access check on SELinux module store for sssd.
- Add labeling for /sbin/iw.
- Allow named_filetrans_domain to create ibus directory with correct labeling.

* Mon Nov 24 2014 Miroslav Grepl <mgrepl@redhat.com> 3.13.1-11
- Allow radius to bind tcp/1812 radius port.
- Dontaudit list user_tmp files for system_mail_t.
- Label virt-who as virtd_exec_t.
- Allow rhsmcertd to send a null signal to virt-who running as virtd_t.
- Add missing alias for _content_rw_t.
Resolves:#1089177
- Allow spamd to access razor-agent.log.
- Add fixes for sfcb from libvirt-cim TestOnly bug.
- Allow NetworkManager stream connect on openvpn.
- Make /usr/bin/vncserver running as unconfined_service_t.
- getty_t should be ranged in MLS. Then also local_login_t runs as ranged domain.
- Label /etc/docker/certs.d as cert_t.

* Tue Nov 18 2014 Miroslav Grepl <mgrepl@redhat.com> 3.13.1-10
- Label /etc/strongimcv as ipsec_conf_file_t.
- Add support for /usr/bin/start-puppet-ca helper script
Resolves:#1160727
- Allow rpm scripts to enable/disable transient systemd units.
Resolves:#1154613 
- Make kpropdas nsswitch domain
Resolves:#1153561
- Make all glance domain as nsswitch domains
Resolves:#1113281
- Allow selinux_child running as sssd access check on /etc/selinux/targeted/modules/active
- Allow access checks on setfiles/load_policy/semanage_lock for selinux_child running as sssd_t
Resolves:#1140106   

* Mon Nov 10 2014 Miroslav Grepl <mgrepl@redhat.com> 3.13.1-9
- Dontaudit access check on setfiles/load_policy for sssd_t.
Resolves:#1140106
- Add kdump_rw_inherited_kdumpctl_tmp_pipes()
Resolves:#1156442
- Make linuxptp services as unconfined.
- Added new policy linuxptp.
Resolves:#1149693
- Label keystone cgi files as keystone_cgi_script_exec_t.
Resolves:#1138424
- Make tuned as unconfined domain

* Thu Nov 6 2014 Miroslav Grepl <mgrepl@redhat.com> 3.13.1-8
- Allow guest to connect to libvirt using unix_stream_socket.
- Allow all bus client domains to dbus chat with unconfined_service_t.
- Allow inetd service without own policy to run in inetd_child_t which is unconfined domain.
- Make opensm as nsswitch domain to make it working with sssd.
- Allow brctl to read meminfo.
- Allow winbind-helper to execute ntlm_auth in the caller domain.
Resolves:#1160339
- Make plymouthd as nsswitch domain to make it working with sssd.
Resolves:#1160196
- Make drbd as nsswitch domain to make it working with sssd.
- Make conman as nsswitch domain to make ipmitool.exp runing as conman_t working.
- Add support for /var/lib/sntp directory.
- Add fixes to allow docker to create more content in tmpfs ,and donaudit reading /proc
- Allow winbind to read usermodehelper
- Allow telepathy domains to execute shells and bin_t
- Allow gpgdomains to create netlink_kobject_uevent_sockets
- Allow mongodb to bind to the mongo port and mongos to run as mongod_t
- Allow abrt to read software raid state.
- Allow nslcd to execute netstat.
- Allow dovecot to create user's home directory when they log into IMAP.
- Allow login domains to create kernel keyring with different level.

* Mon Nov 3 2014 Miroslav Grepl <mgrepl@redhat.com> 3.13.1-7
- Allow modemmanger to connectto itself
Resolves:#1120152 
- Allow pki_tomcat to create link files in /var/lib/pki-ca.
Resolves:#1121744 
- varnishd needs to have fsetid capability
Resolves:#1125165
- Allow snapperd to dbus chat with system cron jobs.
Resolves:#1152447
- Allow dovecot to create user's home directory when they log into IMAP 
Resolves:#1152773   
- Add labeling for /usr/sbin/haproxy-systemd-wrapper wrapper to make haproxy running haproxy_t.
- ALlow listen and accept on tcp socket for init_t in MLS. Previously it was for xinetd_t. 
- Allow nslcd to execute netstat.
- Add suppor for keepalived unconfined scripts and allow keepalived to read all domain state and kill capability.
- Allow nslcd to read /dev/urandom.

* Thu Oct 16 2014 Miroslav Grepl <mgrepl@redhat.com> 3.13.1-6
- Add back kill permisiion for system class
Resolves:#1150011

* Wed Oct 15 2014 Miroslav Grepl <mgrepl@redhat.com> 3.13.1-5
- Add back kill permisiion for service class
Resolves:#1150011
- Make rhsmcertd_t also as dbus domain.
- Allow named to create DNS_25 with correct labeling.
- Add cloudform_dontaudit_write_cloud_log()
- Call auth_use_nsswitch to apache to read/write cloud-init keys.
- Allow cloud-init to dbus chat with certmonger.
- Fix path to mon_statd_initrc_t script.
- Allow all RHCS services to read system state.
- Allow dnssec_trigger_t to execute unbound-control in own domain.
- kernel_read_system_state needs to be called with type. Moved it to antivirus.if.
- Added policy for mon_statd and mon_procd services. BZ (1077821)
- Allow opensm_t to read/write /dev/infiniband/umad1.
- Allow mongodb to manage own log files.
- Allow neutron connections to system dbus.
- Add support for /var/lib/swiftdirectory.
- Allow nova-scheduler to read certs.
- Allow openvpn to access /sys/fs/cgroup dir.
- Allow openvpn to execute  systemd-passwd-agent in  systemd_passwd_agent_t to make openvpn working with systemd.
- Fix samba_export_all_ro/samba_export_all_rw booleans to dontaudit search/read security files.
- Add auth_use_nsswitch for portreserve to make it working with sssd.
- automount policy is non-base module so it needs to be called in optional block.
- ALlow sensord to getattr on sysfs.
- Label /usr/share/corosync/corosync as cluster_exec_t.
- Allow lmsd_plugin to read passwd file. BZ(1093733)
- Allow read antivirus domain all kernel sysctls.
- Allow mandb to getattr on file systems
- Allow nova-console to connect to mem_cache port.
- Make sosreport as unconfined domain.
- Allow mondogdb to  'accept' accesses on the tcp_socket port.
- ALlow sanlock to send a signal to virtd_t.

* Thu Oct 9 2014 Miroslav Grepl <mgrepl@redhat.com> 3.13.1-4
- Build also MLS policy
Resolves:#1138424

* Thu Oct 9 2014 Miroslav Grepl <mgrepl@redhat.com> 3.13.1-3
- Add back kill permisiion for system class
- Allow iptables read fail2ban logs.
- Fix radius labeled ports
- Add userdom_manage_user_tmpfs_files interface
- Allow libreswan to connect to VPN via NM-libreswan.
- Label 4101 tcp port as brlp port
- fix dev_getattr_generic_usb_dev interface
- Allow all domains to read fonts
- Make sure /run/systemd/generator and system is labeled correctly on creation.
- Dontaudit aicuu to search home config dir. 
- Make keystone_cgi_script_t domain. 
Resolves:#1138424
- Fix bug in drbd policy, 
- Added support for cpuplug. 
- ALlow sanlock_t to read sysfs_t.
- Added sendmail_domtrans_unconfined interface
- Fix broken interfaces
- radiusd wants to write own log files.
- Label /usr/libexec/rhsmd as rhsmcertd_exec_t
- Allow rhsmcertd send signull to setroubleshoot. 
- Allow rhsmcertd manage rpm db. 
- Added policy for blrtty. 
- Fix keepalived policy
- Allow rhev-agentd dbus chat with systemd-logind.
- Allow keepalived manage snmp var lib sock files.
- Add support for /var/lib/graphite-web
- Allow NetworkManager to create Bluetooth SDP sockets
- It's going to do the the discovery for DUN service for modems with Bluez 5.
- Allow swift to connect to all ephemeral ports by default.
- Allow sssd to read selinux config to add SELinux user mapping.
- Allow lsmd to search own plguins.
- Allow abrt to read /dev/memto generate an unique machine_id and uses  sosuploader's algorithm based off dmidecode[1] fields.
- ALlow zebra for user/group look-ups.
- Allow nova domains to getattr on all filesystems.
- Allow collectd sys_ptrace and dac_override caps because of reading of /proc/%i/io for several processes.
- Allow pppd to connect to /run/sstpc/sstpc-nm-sstp-service-28025 over unix stream socket.
- Allow rhnsd_t to manage also rhnsd config symlinks.
- ALlow user mail domains to create dead.letter.
- Allow rabbitmq_t read rabbitmq_var_lib_t lnk files. 
- Allow pki-tomcat to change SELinux object identity.
- Allow radious to connect to apache ports to do OCSP check
- Allow git cgi scripts to create content in /tmp
- Allow cockpit-session to do GSSAPI logins.
- Allow sensord read in /proc 
- Additional access required by usbmuxd

* Thu Sep 18 2014 Miroslav Grepl <mgrepl@redhat.com> 3.13.1-2
- Allow locate to look at files/directories without labels, and chr_file and blk_file on non dev file systems
- Label /usr/lib/erlang/erts.*/bin files as bin_t
- Add files_dontaudit_access_check_home_dir() inteface.
- Allow udev_t mounton udev_var_run_t dirs #(1128618)
- Add systemd_networkd_var_run_t labeling for /var/run/systemd/netif and allow systemd-networkd to manage it.
- Add init_dontaudit_read_state() interface.
- Add label for ~/.local/share/fonts
- Allow unconfined_r to access unconfined_service_t.
- Allow init to read all config files
- Add new interface to allow creation of file with lib_t type
- Assign rabbitmq port.
- Allow unconfined_service_t to dbus chat with all dbus domains
- Add new interfaces to access users keys.
- Allow domains to are allowed to mounton proc to mount on files as well as dirs
- Fix labeling for HOME_DIR/tmp and HOME_DIR/.tmp directories.
- Add a port definition for shellinaboxd
- Label ~/tmp and ~/.tmp directories in user tmp dirs as user_tmp_t
- Allow userdomains to stream connect to pcscd for smart cards
- Allow programs to use pam to search through user_tmp_t dires (/tmp/.X11-unix)
- Update to rawhide-contrib changes
Resolves:#1123844

* Thu Aug 21 2014 Miroslav Grepl <mgrepl@redhat.com> 3.13.1-1
- Rebase to 3.13.1 which we have in Fedora21
Resolves:#1128284

* Fri Jun 13 2014 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-156
- Back port fixes from Fedora. Mainly OpenStack and Docker fixes

* Wed Jun 11 2014 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-155
- Add policy-rhel-7.1-{base,contrib} patches

* Mon May 5 2014 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-154
- Add support for us_cli ports
- Fix labeling for /var/run/user/<UID>/gvfs
- add support for tcp/9697
- Additional rules required by openstack,  needs backport to F20 and RHEL7
- Additional access required by docker
- ALlow motion to use tcp/8082 port
- Allow init_t to setattr/relabelfrom dhcp state files
- Dontaudit antivirus domains read access on all security files by default
- Add missing alias for old amavis_etc_t type
- Allow block_suspend cap for haproxy
- Additional fixes for  instack overcloud
- Allow OpenStack to read mysqld_db links and connect to MySQL
- Remove dup filename rules in gnome.te
- Allow sys_chroot cap for httpd_t and setattr on httpd_log_t
- Allow iscsid to handle own unit files
- Add iscsi_systemctl()
- Allow mongod to create also sock_files in /run with correct labeling
- Allow httpd to send signull to apache script domains and don't audit leaks
- Allow rabbitmq_beam to connect to httpd port
- Allow aiccu stream connect to pcscd
- Allow dmesg to read hwdata and memory dev
- Allow all freeipmi domains to read/write ipmi devices
- Allow sblim_sfcbd to use also pegasus-https port
- Allow rabbitmq_epmd to manage rabbit_var_log_t files
- Allow chronyd to read /sys/class/hwmon/hwmon1/device/temp2_input
- Allow docker to status any unit file and allow it to start generic unit files

* Mon Apr 7 2014 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-153
- Change hsperfdata_root to have as user_tmp_t
Resolves:#1076523

* Fri Apr 4 2014 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-152
- Fix Multiple same specifications for /var/named/chroot/dev/zero
- Add labels for /var/named/chroot_sdb/dev devices
- Add support for strongimcv
- Use kerberos_keytab_domains in auth_use_nsswitch
- Update auth_use_nsswitch to make all these types as kerberos_keytab_domain to
- Allow net_raw cap for neutron_t and send sigkill to dnsmasq
- Fix ntp_filetrans_named_content for sntp-kod file
- Add httpd_dbus_sssd boolean
- Dontaudit exec insmod in boinc policy
- Rename kerberos_keytab_domain to kerberos_keytab_domains
- Add kerberos_keytab_domain()
- Fix kerberos_keytab_template()
- Make all domains which use kerberos as kerberos_keytab_domain
Resolves:#1083670
- Allow kill capability to winbind_t

* Wed Apr 2 2014 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-151
- varnishd wants chown capability
- update ntp_filetrans_named_content() interface
- Add additional fixes for neutron_t. #1083335
- Dontaudit getattr on proc_kcore_t
- Allow pki_tomcat_t to read ipa lib files
- Allow named_filetrans_domain to create /var/cache/ibus with correct labelign
- Allow init_t run /sbin/augenrules
- Add dev_unmount_sysfs_fs and sysnet_manage_ifconfig_run interfaces
- Allow unpriv SELinux user to use sandbox
- Add default label for /tmp/hsperfdata_root

* Tue Apr 1 2014 Miroslav Grepl<mgrepl@redhat.com> 3.12.1-149
- Add file subs also for /var/home

* Mon Mar 31 2014 Miroslav Grepl<mgrepl@redhat.com> 3.12.1-149
- Allow xauth_t to read user_home_dir_t lnk_file
- Add labeling for lightdm-data
- Allow certmonger to manage ipa lib files
- Add support for /var/lib/ipa
- Allow pegasus to getattr virt_content
- Added some new rules to pcp policy
- Allow chrome_sandbox to execute config_home_t
- Add support for ABRT FAF

* Fri Mar 28 2014 Miroslav Grepl<mgrepl@redhat.com> 3.12.1-148
- Allow kdm to send signull to remote_login_t process
- Add gear policy
- Turn on gear_port_t
- Allow cgit to read gitosis lib files by default
- Allow vdagent to read xdm state
- Allow NM and fcoeadm to talk together over unix_dgram_socket

* Thu Mar 27 2014 Miroslav Grepl<mgrepl@redhat.com> 3.12.1-147
- Back port fixes for pegasus_openlmi_admin_t from rawhide
Resolves:#1080973
- Add labels for ostree
- Add SELinux awareness for NM
- Label /usr/sbin/pwhistory_helper as updpwd_exec_t

* Wed Mar 26 2014 Miroslav Grepl<mgrepl@redhat.com> 3.12.1-146
- add gnome_append_home_config()
- Allow thumb to append GNOME config home files
- Allow rasdaemon to rw /dev/cpu//msr
- fix /var/log/pki file spec
- make bacula_t as auth_nsswitch domain
- Identify pki_tomcat_cert_t as a cert_type
- Define speech-dispater_exec_t as an application executable
- Add a new file context for /var/named/chroot/run directory
- update storage_filetrans_all_named_dev for sg* devices
- Allow auditctl_t  to getattr on all removeable devices
- Allow nsswitch_domains to stream connect to nmbd
- Allow unprivusers to connect to memcached
- label /var/lib/dirsrv/scripts-INSTANCE as bin_t

* Mon Mar 24 2014 Miroslav Grepl<mgrepl@redhat.com> 3.12.1-145
- Allow also unpriv user to run vmtools
- Allow secadm to read /dev/urandom and meminfo
Resolves:#1079250
- Add booleans to allow docker processes to use nfs and samba
- Add mdadm_tmpfs support
- Dontaudit net_amdin for /usr/lib/jvm/java-1.7.0-openjdk-1.7.0.51-2.4.5.1.el7.x86_64/jre-abrt/bin/java running as pki_tomcat_t
- Allow vmware-user-sui to use user ttys
- Allow talk 2 users logged via console too
- Allow ftp services to manage xferlog_t
- Make all pcp domanis as unconfined for RHEL7.0 beucause of new policies
- allow anaconda to dbus chat with systemd-localed

* Fri Mar 21 2014 Miroslav Grepl<mgrepl@redhat.com> 3.12.1-144
- allow anaconda to dbus chat with systemd-localed
- Add fixes for haproxy based on bperkins@redhat.com
- Allow cmirrord to make dmsetup working
- Allow NM to execute arping
- Allow users to send messages through talk
- Add userdom_tmp_role for secadm_t

* Thu Mar 20 2014 Lukas Vrabec <lvrabec@redhat.com> 3.12.1-143
- Add additional fixes for rtas_errd
- Fix transitions for tmp/tmpfs in rtas.te
- Allow rtas_errd to readl all sysctls


* Wed Mar 19 2014 Miroslav Grepl<mgrepl@redhat.com> 3.12.1-142
- Add support for /var/spool/rhsm/debug
- Make virt_sandbox_use_audit as True by default
- Allow svirt_sandbox_domains to ptrace themselves

* Wed Mar 19 2014 Miroslav Grepl<mgrepl@redhat.com> 3.12.1-141
- Allow docker containers to manage /var/lib/docker content

* Mon Mar 17 2014 Miroslav Grepl<mgrepl@redhat.com> 3.12.1-140
- Allow docker to read tmpfs_t symlinks
- Allow sandbox svirt_lxc_net_t to talk to syslog and to sssd over stream sockets

* Mon Mar 17 2014 Miroslav Grepl<mgrepl@redhat.com> 3.12.1-139
- Allow collectd to talk to libvirt
- Allow chrome_sandbox to use leaked unix_stream_sockets
- Dontaudit leaks of sockets into chrome_sandbox_t
- If you create a cups directory in /var/cache then it should be labeled cups_rw_etc_t
- Run vmtools as unconfined domains
- Allow snort to manage its log files
- Allow systemd_cronjob_t to be entered via bin_t
- Allow procman to list doveconf_etc_t
- allow keyring daemon to create content in tmpfs directories
- Add proper labelling for icedtea-web
- vpnc is creating content in networkmanager var run directory
- Label sddm as xdm_exec_t to make KDE working again
- Allow postgresql to read network state
- Allow java running as pki_tomcat to read network sysctls
- Fix cgroup.te to allow cgred to read cgconfig_etc_t
- Allow beam.smp to use ephemeral ports
- Allow winbind to use the nis to authenticate passwords

* Fri Mar 14 2014 Lukas Vrabec <lvrabec@redhat.com> 3.12.1-138
- Make rtas_errd_t as unconfined domain for F20.It needs additional fixes. It runs rpm at least.
- Allow net_admin cap for fence_virtd running as fenced_t
- Make  abrt-java-connector working
- Make cimtest script 03_defineVS.py of ComputerSystem group working
- Fix git_system_enable_homedirs boolean
- Allow munin mail plugins to read network systcl

* Thu Mar 13 2014 Miroslav Grepl<mgrepl@redhat.com> 3.12.1-137
- Allow vmtools_helper_t to execute bin_t
- Add support for /usr/share/joomla
- /var/lib/containers should be labeled as openshift content for now
- Allow docker domains to talk to the login programs, to allow a process to login into the container
- Allow install_t do dbus chat with NM
- Fix interface names in anaconda.if
- Add install_t for anaconda. A new type is a part of anaconda policy
- sshd to read network sysctls

* Wed Mar 12 2014 Miroslav Grepl<mgrepl@redhat.com> 3.12.1-136
- Allow zabbix to send system log msgs
- Allow init_t to stream connect to ipsec
Resolves:#1060775

* Tue Mar 11 2014 Miroslav Grepl<mgrepl@redhat.com> 3.12.1-135
- Add docker_connect_any boolean

* Tue Mar 11 2014 Miroslav Grepl<mgrepl@redhat.com> 3.12.1-134
- Allow unpriv SELinux users to dbus chat with firewalld
- Add lvm_write_metadata()
- Label /etc/yum.reposd dir as system_conf_t. Should be safe because system_conf_t is base_ro_file_type
- Allow pegasus_openlmi_storage_t to write lvm metadata
- Add hide_broken_symptoms for kdumpgui because of systemd bug
- Make kdumpgui_t as unconfined domain
Resolves:#1044299
- Allow docker to connect to tcp/5000

* Mon Mar 10 2014 Miroslav Grepl<mgrepl@redhat.com> 3.12.1-133
- Allow numad to write scan_sleep_millisecs
- Turn on entropyd_use_audio boolean by default
- Allow cgred to read /etc/cgconfig.conf because it contains templates used together with rules from /etc/cgrules.conf.
- Allow lscpu running as rhsmcertd_t to read /proc/sysinfo
- Fix label on irclogs in the homedir
- Allow kerberos_keytab_domain domains to manage keys until we get sssd fix
- Allow postgresql to use ldap
- Add missing syslog-conn port
- Add support for /dev/vmcp and /dev/sclp
Resolves:#1069310

* Fri Mar 7 2014 Miroslav Grepl<mgrepl@redhat.com> 3.12.1-132
- Modify xdm_write_home to allow create files/links in /root with xdm_home_
- Allow virt domains to read network state
Resolves:#1072019

* Thu Mar 6 2014 Miroslav Grepl<mgrepl@redhat.com> 3.12.1-131
- Added pcp rules
- dontaudit openshift_cron_t searching random directories, should be back ported to RHEL6
- clean up ctdb.te
- Allow ctdbd to connect own ports
- Fix samba_export_all_rw booleanto cover also non security dirs
- Allow swift to exec rpm in swift_t and allow to create tmp files/dirs
- Allow neutron to create /run/netns with correct labeling
- Allow certmonger to list home dirs

* Wed Mar 5 2014 Miroslav Grepl<mgrepl@redhat.com> 3.12.1-130
- Change userdom_use_user_inherited_ttys to userdom_use_user_ttys for systemd-tty-ask
- Add sysnet_filetrans_named_content_ifconfig() interface
- Allow ctdbd to connect own ports
- Fix samba_export_all_rw booleanto cover also non security dirs
- Allow swift to exec rpm in swift_t and allow to create tmp files/dirs
- Allow neutron to create /run/netns with correct labeling
- Allow kerberos keytab domains to manage sssd/userdomain keys"
- Allow to run ip cmd in neutron_t domain

* Mon Mar 3 2014 Miroslav Grepl<mgrepl@redhat.com> 3.12.1-129
- Allow block_suspend cap2 for systemd-logind and rw dri device
- Add labeling for /usr/libexec/nm-libreswan-service
- Allow locallogin to rw xdm key to make Virtual Terminal login providing smartcard pin working
- Add xserver_rw_xdm_keys()
- Allow rpm_script_t to dbus chat also with systemd-located
- Fix ipa_stream_connect_otpd()
- update lpd_manage_spool() interface
- Allow krb5kdc to stream connect to ipa-otpd
- Add ipa_stream_connect_otpd() interface
- Allow vpnc to unlink NM pids
- Add networkmanager_delete_pid_files()
- Allow munin plugins to access unconfined plugins
- update abrt_filetrans_named_content to cover /var/spool/debug
- Label /var/spool/debug as abrt_var_cache_t
- Allow rhsmcertd to connect to squid port
- Make docker_transition_unconfined as optional boolean
- Allow certmonger to list home dirs

* Wed Feb 26 2014 Miroslav Grepl<mgrepl@redhat.com> 3.12.1-128
- Make snapperd as unconfined domain and add additional fixes for it
- Remove nsplugin.pp module on upgrade

* Tue Feb 25 2014 Miroslav Grepl<mgrepl@redhat.com> 3.12.1-127
- Add snapperd_home_t for HOME_DIR/.snapshots directory
- Make sosreport as unconfined domain
- Allow sosreport to execute grub2-probe
- Allow NM to manage hostname config file
- Allow systemd_timedated_t to dbus chat with rpm_script_t
- Allow lsmd plugins to connect to http/ssh/http_cache ports by default
- Add lsmd_plugin_connect_any boolean
- Allow mozilla_plugin to attempt to set capabilities
- Allow lsdm_plugins to use tcp_socket
- Dontaudit mozilla plugin from getattr on /proc or /sys
- Dontaudit use of the keyring by the services in a sandbox
- Dontaudit attempts to sys_ptrace caused by running ps for mysqld_safe_t
- Allow rabbitmq_beam to connect to jabber_interserver_port
- Allow logwatch_mail_t to transition to qmail_inject and queueu
- Added new rules to pcp policy
- Allow vmtools_helper_t to change role to system_r
- Allow NM to dbus chat with vmtools
- Fix couchdb_manage_files() to allow manage couchdb conf files
- Add support for /var/run/redis.sock
- dontaudit gpg trying to use audit
- Allow consolekit to create log directories and files
- Fix vmtools policy to allow user roles to access vmtools_helper_t
- Allow block_suspend cap2 for ipa-otpd
- Allow pkcsslotd to read users state
- Add ioctl to init_dontaudit_rw_stream_socket
- Add systemd_hostnamed_manage_config() interface
- Remove transition for temp dirs created by init_t
- gdm-simple-slave uses use setsockopt
- sddm-greater is a xdm type program

* Tue Feb 18 2014 Miroslav Grepl<mgrepl@redhat.com> 3.12.1-126
- Add lvm_read_metadata()
- Allow auditadm to search /var/log/audit dir
- Add lvm_read_metadata() interface
- Allow confined users to run vmtools helpers
- Fix userdom_common_user_template()
- Generic systemd unit scripts do write check on /
- Allow init_t to create init_tmp_t in /tmp.This is for temporary content created by generic unit files
- Add additional fixes needed for init_t and setup script running in generic unit files
- Allow general users to create packet_sockets
- added connlcli port
- Add init_manage_transient_unit() interface
- Allow init_t (generic unit files) to manage rpc state date as we had it for initrc_t
- Fix userdomain.te to require passwd class
- devicekit_power sends out a signal to all processes on the message bus when power is going down
- Dontaudit rendom domains listing /proc and hittping system_map_t
- Dontauit leaks of var_t into ifconfig_t
- Allow domains that transition to ssh_t to manipulate its keyring
- Define oracleasm_t as a device node
- Change to handle /root as a symbolic link for os-tree
- Allow sysadm_t to create packet_socket, also move some rules to attributes
- Add label for openvswitch port
- Remove general transition for files/dirs created in /etc/mail which got etc_aliases_t label.
- Allow postfix_local to read .forward in pcp lib files
- Allow pegasus_openlmi_storage_t to read lvm metadata
- Add additional fixes for pegasus_openlmi_storage_t
- Allow bumblebee to manage debugfs
- Make bumblebee as unconfined domain
- Allow snmp to read etc_aliases_t
- Allow lscpu running in pegasus_openlmi_storage_t to read /dev/mem
- Allow pegasus_openlmi_storage_t to read /proc/1/environ
- Dontaudit read gconf files for cupsd_config_t
- make vmtools as unconfined domain
- Add vmtools_helper_t for helper scripts. Allow vmtools shutdonw a host and run ifconfig.
- Allow collectd_t to use a mysql database
- Allow ipa-otpd to perform DNS name resolution
- Added new policy for keepalived
- Allow openlmi-service provider to manage transitient units and allow stream connect to sssd
- Add additional fixes new pscs-lite+polkit support
- Add labeling for /run/krb5kdc
- Change w3c_validator_tmp_t to httpd_w3c_validator_tmp_t in F20
- Allow pcscd to read users proc info
- Dontaudit smbd_t sending out random signuls
- Add boolean to allow openshift domains to use nfs
- Allow w3c_validator to create content in /tmp
- zabbix_agent uses nsswitch
- Allow procmail and dovecot to work together to deliver mail
- Allow spamd to execute files in homedir if boolean turned on
- Allow openvswitch to listen on port 6634
- Add net_admin capability in collectd policy
- Fixed snapperd policy
- Fixed bugsfor pcp policy
- Allow dbus_system_domains to be started by init
- Fixed some interfaces
- Add kerberos_keytab_domain attribute
- Fix snapperd_conf_t def

* Tue Feb 11 2014 Miroslav Grepl<mgrepl@redhat.com> 3.12.1-125
- Addopt corenet rules for unbound-anchor to rpm_script_t
- Allow runuser to send send audit messages.
- Allow postfix-local to search .forward in munin lib dirs
- Allow udisks to connect to D-Bus
- Allow spamd to connect to spamd port
- Fix syntax error in snapper.te
- Dontaudit osad to search gconf home files
- Allow rhsmcertd to manage /etc/sysconf/rhn director
- Fix pcp labeling to accept /usr/bin for all daemon binaries
- Fix mcelog_read_log() interface
- Allow iscsid to manage iscsi lib files
- Allow snapper domtrans to lvm_t. Add support for /etc/snapper and allow snapperd to manage it.
- Make tuned_t as unconfined domain for RHEL7.0
- Allow ABRT to read puppet certs
- Add sys_time capability for virt-ga
- Allow gemu-ga to domtrans to hwclock_t
- Allow additional access for virt_qemu_ga_t processes to read system clock and send audit messages
- Fix some AVCs in pcp policy
- Add to bacula capability setgid and setuid and allow to bind to bacula ports
- Changed label from rhnsd_rw_conf_t to rhnsd_conf_t
- Add access rhnsd and osad to /etc/sysconfig/rhn
- drbdadm executes drbdmeta
- Fixes needed for docker
- Allow epmd to manage /var/log/rabbitmq/startup_err file
- Allow beam.smp connect to amqp port
- Modify xdm_write_home to allow create also links as xdm_home_t if the boolean is on true
- Allow init_t to manage pluto.ctl because of init_t instead of initrc_t
- Allow systemd_tmpfiles_t to manage all non security files on the system
- Added labels for bacula ports
- Fix label on /dev/vfio/vfio
- Add kernel_mounton_messages() interface
- init wants to manage lock files for iscsi

* Mon Feb 3 2014 Miroslav Grepl<mgrepl@redhat.com> 3.12.1-124
- Added osad policy
- Allow postfix to deliver to procmail
- Allow bumblebee to seng kill signal to xserver
- Allow vmtools to execute /usr/bin/lsb_release
- Allow docker to write system net ctrls
- Add support for rhnsd unit file
- Add dbus_chat_session_bus() interface
- Add dbus_stream_connect_session_bus() interface
- Fix pcp.te
- Fix logrotate_use_nfs boolean
- Add lot of pcp fixes found in RHEL7
- fix labeling for pmie for pcp pkg
- Change thumb_t to be allowed to chat/connect with session bus type
- Allow call renice in mlocate
- Add logrotate_use_nfs boolean
- Allow setroubleshootd to read rpc sysctl

* Fri Jan 31 2014 Miroslav Grepl<mgrepl@redhat.com> 3.12.1-123
- Turn on bacula, rhnsd policy
- Add support for rhnsd unit file
- Add dbus_chat_session_bus() interface
- Add dbus_stream_connect_session_bus() interface
- Fix logrotate_use_nfs boolean
- Add lot of pcp fixes found in RHEL7
- fix labeling for pmie for pcp pkg
- Change thumb_t to be allowed to chat/connect with session bus type
- Allow call renice in mlocate
- Add logrotate_use_nfs boolean
- Allow setroubleshootd to read rpc sysctl
- Fixes for *_admin interfaces
- Add pegasus_openlmi_storage_var_run_t type def
- Add support for /var/run/openlmi-storage
- Allow tuned to create syslog.conf with correct labeling
- Add httpd_dontaudit_search_dirs boolean
- Add support for winbind.service
- ALlow also fail2ban-client to read apache logs
- Allow vmtools to getattr on all fs
- Add support for dey_sapi port
- Add logging_filetrans_named_conf()
- Allow passwd_t to use ipc_lock, so that it can change the password in gnome-keyring

* Tue Jan 28 2014 Miroslav Grepl<mgrepl@redhat.com> 3.12.1-122
- Update snapper policy
- Allow domains to append rkhunter lib files
- Allow snapperd to getattr on all fs
- Allow xdm to create /var/gdm with correct labeling
- Add label for snapper.log
- Allow fail2ban-client to read apache log files
- Allow thumb_t to execute dbus-daemon in thumb_t

* Mon Jan 27 2014 Miroslav Grepl<mgrepl@redhat.com> 3.12.1-121
- Allow gdm to create /var/gdm with correct labeling
- Allow domains to append rkhunterl lib files. #1057982
- Allow systemd_tmpfiles_t net_admin to communicate with journald
- Add interface to getattr on an isid_type for any type of file
- Update libs_filetrans_named_content() to have support for /usr/lib/debug directory
- Allow initrc_t domtrans to authconfig if unconfined is enabled
- Allow docker and mount on devpts chr_file
- Allow docker to transition to unconfined_t if boolean set
- init calling needs to be optional in domain.te
- Allow uncofined domain types to handle transient unit files
- Fix labeling for vfio devices
- Allow net_admin capability and send system log msgs
- Allow lldpad send dgram to NM
- Add networkmanager_dgram_send()
- rkhunter_var_lib_t is correct type
- Back port pcp policy from rawhide
- Allow openlmi-storage to read removable devices
- Allow system cron jobs to manage rkhunter lib files
- Add rkhunter_manage_lib_files()
- Fix ftpd_use_fusefs boolean to allow manage also symlinks
- Allow smbcontrob block_suspend cap2
- Allow slpd to read network and system state info
- Allow NM domtrans to iscsid_t if iscsiadm is executed
- Allow slapd to send a signal itself
- Allow sslget running as pki_ra_t to contact port 8443, the secure port of the CA.
- Fix plymouthd_create_log() interface
- Add rkhunter policy with files type definition for /var/lib/rkhunter until it is fixed in rkhunter package
- Add mozilla_plugin_exec_t for /usr/lib/firefox/plugin-container
- Allow postfix and cyrus-imapd to work out of box
- Allow fcoemon to talk with unpriv user domain using unix_stream_socket
- Dontaudit domains that are calling into journald to net_admin
- Add rules to allow vmtools to do what it does
- snapperd is D-Bus service
- Allow OpenLMI PowerManagement to call 'systemctl --force reboot'
- Add haproxy_connect_any boolean
- Allow haproxy also to use http cache port by default
Resolves:#1058248

* Tue Jan 21 2014 Miroslav Grepl<mgrepl@redhat.com> 3.12.1-120
- Allow apache to write to the owncloud data directory in /var/www/html...
- Allow consolekit to create log dir
- Add support for icinga CGI scripts
- Add support for icinga
- Allow kdumpctl_t to create kdump lock file
Resolves:#1055634
- Allow kdump to create lnk lock file
- Allow nscd_t block_suspen capability
- Allow unconfined domain types to manage own transient unit file
- Allow systemd domains to handle transient init unit files
- Add interfaces to handle transient

* Mon Jan 20 2014 Miroslav Grepl<mgrepl@redhat.com> 3.12.1-119
- Add cron unconfined role support for uncofined SELinux user
- Call corenet_udp_bind_all_ports() in milter.te
- Allow fence_virtd to connect to zented port
- Fix header for mirrormanager_admin()
- Allow dkim-milter to bind udp ports
- Allow milter domains to send signull itself
- Allow block_suspend for yum running as mock_t
- Allow beam.smp to manage couchdb files
- Add couchdb_manage_files()
- Add labeling for /var/log/php_errors.log
- Allow bumblebee to stream connect to xserver
- Allow bumblebee to send a signal to xserver
- gnome-thumbnail to stream connect to bumblebee
- Allow xkbcomp running as bumblebee_t to execute  bin_t
- Allow logrotate to read squid.conf
- Additional rules to get docker and lxc to play well with SELinux
- Allow bumbleed to connect to xserver port
- Allow pegasus_openlmi_storage_t to read hwdata

* Thu Jan 16 2014 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-118
- Allow init_t to work on transitient and snapshot unit files
- Add logging_manage_syslog_config()
- Update sysnet_dns_name_resolve() to allow connect to dnssec por
- Allow pegasus_openlmi_storage_t to read hwdata
Resolves:#1031721
- Fix rhcs_rw_cluster_tmpfs()
- Allow fenced_t to bind on zented udp port
- Added policy for vmtools
- Fix mirrormanager_read_lib_files()
- Allow mirromanager scripts running as httpd_t to manage mirrormanager pid files
- Allow ctdb to create sock files in /var/run/ctdb
- Add sblim_filetrans_named_content() interface
- Allow rpm scritplets to create /run/gather with correct labeling
- Allow gnome keyring domains to create gnome config dirs
- Dontaudit read/write to init stream socket for lsmd_plugin_t
- Allow automount to read nfs link files
- Allow lsm plugins to read/write lsmd stream socket
- Allow certmonger to connect ldap port to make IPA CA certificate renewal working.
- Add also labeling for /var/run/ctdb
- Add missing labeling for /var/lib/ctdb
- ALlow tuned to manage syslog.conf. Should be fixed in tuned. #1030446
- Dontaudit hypervkvp to search homedirs
- Dontaudit hypervkvp to search admin homedirs
- Allow hypervkvp to execute bin_t and ifconfig in the caller domain
- Dontaudit xguest_t to read ABRT conf files
- Add abrt_dontaudit_read_config()
- Allow namespace-init to getattr on fs
- Add thumb_role() also for xguest
- Add filename transitions to create .spamassassin with correct labeling
- Allow apache domain to read mirrormanager pid files
- Allow domains to read/write shm and sem owned by mozilla_plugin_t
- Allow alsactl to send a generic signal to kernel_t

* Tue Jan 14 2014 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-117
- Add back rpm_run() for unconfined user

* Tue Jan 14 2014 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-116
- Add missing files_create_var_lib_dirs()
- Fix typo in ipsec.te
- Allow passwd to create directory in /var/lib
- Add filename trans also for event21
- Allow iptables command to read /dev/rand
- Add sigkill capabilityfor ipsec_t
- Add filename transitions for bcache devices
- Add additional rules to create /var/log/cron by syslogd_t with correct labeling
- Add give everyone full access to all key rings
- Add default lvm_var_run_t label for /var/run/multipathd
- Fix log labeling to have correct default label for them after logrotate
- Labeled ~/.nv/GLCache as being gstreamer output
- Allow nagios_system_plugin to read mrtg lib files
- Add mrtg_read_lib_files()
- Call rhcs_rw_cluster_tmpfs for dlm_controld
- Make authconfing as named_filetrans domain
- Allow virsh to connect to user process using stream socket
- Allow rtas_errd to read rand/urand devices and add chown capability
- Fix labeling from /var/run/net-snmpd to correct /var/run/net-snmp
Resolves:#1051497
- Add also chown cap for abrt_upload_watch_t. It already has dac_override
- Allow sosreport to manage rhsmcertd pid files
- Add rhsmcertd_manage_pid_files()
- Allow also setgid cap for rpc.gssd
- Dontaudit access check for abrt on cert_t
- Allow pegasus_openlmi_system providers to dbus chat with systemd-logind

* Fri Jan 10 2014 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-115
- Fix semanage import handling in spec file

* Fri Jan 10 2014 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-114
- Add default lvm_var_run_t label for /var/run/multipathd
Resolves:#1051430
- Fix log labeling to have correct default label for them after logrotate
- Add files_write_root_dirs
- Add new openflow port label for 6653/tcp and 6633/tcp
- Add xserver_manage_xkb_libs()
- Label tcp/8891 as milter por
- Allow gnome_manage_generic_cache_files also create cache_home_t files
- Fix aide.log labeling
- Fix log labeling to have correct default label for them after logrotate
- Allow mysqld-safe write access on /root to make mysqld working
- Allow sosreport domtrans to prelikn
- Allow OpenvSwitch to connec to openflow ports
- Allow NM send dgram to lldpad
- Allow hyperv domains to execute shell
- Allow lsmd plugins stream connect to lsmd/init
- Allow sblim domains to create /run/gather with correct labeling
- Allow httpd to read ldap certs
- Allow cupsd to send dbus msgs to process with different MLS level
- Allow bumblebee to stream connect to apmd
- Allow bumblebee to run xkbcomp
- Additional allow rules to get libvirt-lxc containers working with docker
- Additional allow rules to get libvirt-lxc containers working with docker
- Allow docker to getattr on itself
- Additional rules needed for sandbox apps
- Allow mozilla_plugin to set attributes on usb device if use_spice boolean enabled
- httpd should be able to send signal/signull to httpd_suexec_t
- Add more fixes for neturon. Domtrans to dnsmasq, iptables. Make neutron as filenamtrans domain. 

* Wed Jan 8 2014 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-113
- Add neutron fixes

* Mon Jan 6 2014 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-112
- Allow sshd to write to all process levels in order to change passwd when running at a level
- Allow updpwd_t to downgrade /etc/passwd file to s0, if it is not running with this range
- Allow apcuspd_t to status and start the power unit file
- Allow udev to manage kdump unit file
- Added new interface modutils_dontaudit_exec_insmod
- Allow cobbler to search dhcp_etc_t directory
- systemd_systemctl needs sys_admin capability
- Allow sytemd_tmpfiles_t to delete all directories
- passwd to create gnome-keyring passwd socket
- Add missing zabbix_var_lib_t type
- Fix filename trans for zabbixsrv in zabbix.te
- Allow fprintd_t to send syslog messages
- Add  zabbix_var_lib_t for /var/lib/zabbixsrv, also allow zabix to connect to smtp port
- Allow mozilla plugin to chat with policykit, needed for spice
- Allow gssprozy to change user and gid, as well as read user keyrings
- Label upgrades directory under /var/www as httpd_sys_rw_content_t, add other filetrans rules to label content correctly
- Allow polipo to connect to http_cache_ports
- Allow cron jobs to manage apache var lib content
- Allow yppassword to manage the passwd_file_t
- Allow showall_t to send itself signals
- Allow cobbler to restart dhcpc, dnsmasq and bind services
- Allow certmonger to manage home cert files
- Add userdom filename trans for user mail domains
- Allow apcuspd_t to status and start the power unit file
- Allow cgroupdrulesengd to create content in cgoups directories
- Allow smbd_t to signull cluster
- Allow gluster daemon to create fifo files in glusterd_brick_t and sock_file in glusterd_var_lib_t
- Add label for /var/spool/cron.aquota.user
- Allow sandbox_x domains to use work with the mozilla plugin semaphore
- Added new policy for speech-dispatcher
- Added dontaudit rule for insmod_exec_t  in rasdaemon policy
- Updated rasdaemon policy
- Allow system_mail_t to transition to postfix_postdrop_t
- Clean up mirrormanager policy
- Allow virt_domains to read cert files, needs backport to RHEL7
- Allow sssd to read systemd_login_var_run_t
- Allow irc_t to execute shell and bin-t files:
- Add new access for mythtv
- Allow rsync_t to manage all non auth files
- allow modemmanger to read /dev/urand
- Allow sandbox apps to attempt to set and get capabilties

* Thu Dec 19 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-111
- Add labeling for /var/lib/servicelog/servicelog.db-journal
- Add support for freeipmi port
- Add sysadm_u_default_contexts
- Make new type to texlive files in homedir
- Allow subscription-manager running as sosreport_t to manage rhsmcertd
- Additional fixes for docker.te
- Remove ability to do mount/sys_admin by default in virt_sandbox domains
- New rules required to run docker images within libivrt
- Add label for ~/.cvsignore
- Change mirrormanager to be run by cron
- Add mirrormanager policy
- Fixed bumblebee_admin() and mip6d_admin()
- Add log support for sensord
- Fix typo in docker.te
- Allow amanda to do backups over UDP
- Allow bumblebee to read /etc/group and clean up bumblebee.te
- type transitions with a filename not allowed inside conditionals
- Don't allow virt-sandbox tools to use netlink out of the box, needs back port to RHEL7
- Make new type to texlive files in homedir

* Thu Dec 12 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-110
- Allow freeipmi_ipmidetectd_t to use freeipmi port
- Update freeipmi_domain_template()
- Allow journalctl running as ABRT to read /run/log/journal
- Allow NM to read dispatcher.d directory
- Update freeipmi policy
- Type transitions with a filename not allowed inside conditionals
- Allow tor to bind to hplip port
- Make new type to texlive files in homedir
- Allow zabbix_agent to transition to dmidecode
- Add rules for docker
- Allow sosreport to send signull to unconfined_t
- Add virt_noatsecure and virt_rlimitinh interfaces
- Fix labeling in thumb.fc to add support for /usr/lib64/tumbler-1/tumblerddd support for freeipmi port
- Add sysadm_u_default_contexts
- Add logging_read_syslog_pid()
- Fix userdom_manage_home_texlive() interface
- Make new type to texlive files in homedir
- Add filename transitions for /run and /lock links
- Allow virtd to inherit rlimit information
Resolves:#975358

* Tue Dec 10 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-109
- Change labeling for /usr/libexec/nm-dispatcher.action to NetworkManager_exec_t
Resolves:#1039879
- Add labeling for /usr/lib/systemd/system/mariadb.service
- Allow hyperv_domain to read sysfs
- Fix ldap_read_certs() interface to allow acess also link files
- Add support for /usr/libexec/pegasus/cmpiLMI_Journald-cimprovagt
- Allow tuned to run modprobe
- Allow portreserve to search /var/lib/sss dir
- Add SELinux support for the teamd package contains team network device control daemon.
- Dontaudit access check on /proc for bumblebee
- Bumblebee wants to load nvidia modules
- Fix rpm_named_filetrans_log_files and wine.te
- Add conman policy for rawhide
- DRM master and input event devices are used by  the TakeDevice API
- Clean up bumblebee policy
- Update pegasus_openlmi_storage_t policy
- Add freeipmi_stream_connect() interface
- Allow logwatch read madm.conf to support RAID setup
- Add raid_read_conf_files() interface
- Allow up2date running as rpm_t create up2date log file with rpm_log_t labeling
- add rpm_named_filetrans_log_files() interface
- Allow dkim-milter to create files/dirs in /tmp
- update freeipmi policy
- Add policy for freeipmi services
- Added rdisc_admin and rdisc_systemctl interfaces
- opensm policy clean up
- openwsman policy clean up
- ninfod policy clean up
- Added new policy for ninfod
- Added new policy for openwsman
- Added rdisc_admin and rdisc_systemctl interfaces
- Fix kernel_dontaudit_access_check_proc()
- Add support for /dev/uhid
- Allow sulogin to get the attributes of initctl and sys_admin cap
- Add kernel_dontaudit_access_check_proc()
- Fix dev_rw_ipmi_dev()
- Fix new interface in devices.if
- DRM master and input event devices are used by  the TakeDevice API
- add dev_rw_inherited_dri() and dev_rw_inherited_input_dev()
- Added support for default conman port
- Add interfaces for ipmi devices

* Wed Dec 4 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-108
- Allow sosreport to send a signal to ABRT
- Add proper aliases for pegasus_openlmi_service_exec_t and pegasus_openlmi_service_t
- Label /usr/sbin/htcacheclean as httpd_exec_t
Resolves:#1037529
- Added support for rdisc unit file
- Add antivirus_db_t labeling for /var/lib/clamav-unofficial-sigs
- Allow runuser running as logrotate connections to system DBUS
- Label bcache devices as fixed_disk_device_t
- Allow systemctl running in ipsec_mgmt_t to access /usr/lib/systemd/system/ipsec.service
- Label /usr/lib/systemd/system/ipsec.service as ipsec_mgmt_unit_file_t

* Mon Dec 2 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-107
- Add back setpgid/setsched for sosreport_t

* Mon Dec 2 2013 Dan Walsh <dwalsh@redhat.com> 3.12.1-106
- Added fix for clout_init to transition to rpm_script_t (dwalsh@redhat.com)

* Tue Nov 26 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-105
- Dontaudit openshift domains trying to use rawip_sockets, this is caused by a bad check in the kernel.
- Allow git_system_t to read git_user_content if the git_system_enable_homedirs boolean is turned on
- Add lsmd_plugin_t for lsm plugins
- Allow dovecot-deliver to search mountpoints
- Add labeling for /etc/mdadm.conf
- Allow opelmi admin providers to dbus chat with init_t
- Allow sblim domain to read /dev/urandom and /dev/random
- Allow apmd to request the kernel load modules
- Add glusterd_brick_t type
- label mate-keyring-daemon with gkeyringd_exec_t
- Add plymouthd_create_log()
- Dontaudit leaks from openshift domains into mail domains, needs back port to RHEL6
- Allow sssd to request the kernel loads modules
- Allow gpg_agent to use ssh-add
- Allow gpg_agent to use ssh-add
- Dontaudit access check on /root for myslqd_safe_t
- Allow ctdb to getattr on al filesystems
- Allow abrt to stream connect to syslog
- Allow dnsmasq to list dnsmasq.d directory
- Watchdog opens the raw socket
- Allow watchdog to read network state info
- Dontaudit access check on lvm lock dir
- Allow sosreport to send signull to setroubleshootd
- Add setroubleshoot_signull() interface
- Fix ldap_read_certs() interface
- Allow sosreport all signal perms
- Allow sosreport to run systemctl
- Allow sosreport to dbus chat with rpm
- Add glusterd_brick_t files type
- Allow zabbix_agentd to read all domain state
- Clean up rtas.if
- Allow smoltclient to execute ldconfig
- Allow sosreport to request the kernel to load a module
- Fix userdom_confined_admin_template()
- Add back exec_content boolean for secadm, logadm, auditadm
- Fix files_filetrans_system_db_named_files() interface
- Allow sulogin to getattr on /proc/kcore
- Add filename transition also for servicelog.db-journal
- Add files_dontaudit_access_check_root()
- Add lvm_dontaudit_access_check_lock() interface

* Thu Nov 21 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-104
- Allow watchdog to read /etc/passwd
- Allow browser plugins to connect to bumblebee
- New policy for bumblebee and freqset
- Add new policy for mip6d daemon
- Add new policy for opensm daemon
- Allow condor domains to read/write condor_master udp_socket
- Allow openshift_cron_t to append to openshift log files, label /var/log/openshift
- Add back file_pid_filetrans for /var/run/dlm_controld
- Allow smbd_t to use inherited tmpfs content
- Allow mcelog to use the /dev/cpu device
- sosreport runs rpcinfo
- sosreport runs subscription-manager
- Allow staff_t to run frequency command
- Allow systemd_tmpfiles to relabel log directories
- Allow staff_t to read xserver_log file
- Label hsperfdata_root as tmp_t

* Wed Nov 20 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-103
- More sosreport fixes to make ABRT working

* Fri Nov 15 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-102
- Fix files_dontaudit_unmount_all_mountpoints()
- Add support for 2608-2609 tcp/udp ports
- Should allow domains to lock the terminal device
- More fixes for user config files to make crond_t running in userdomain
- Add back disable/reload/enable permissions for system class
- Fix manage_service_perms macro
- We need to require passwd rootok
- Fix zebra.fc
- Fix dnsmasq_filetrans_named_content() interface
- Allow all sandbox domains create content in svirt_home_t
- Allow zebra domains also create zebra_tmp_t files in /tmp
- Add support for new zebra services:isisd,babeld. Add systemd support for zebra services.
- Fix labeling on neutron and remove transition to iconfig_t
- abrt needs to read mcelog log file
- Fix labeling on dnsmasq content
- Fix labeling on /etc/dnsmasq.d
- Allow glusterd to relabel own lib files
- Allow sandbox domains to use pam_rootok, and dontaudit attempts to unmount file systems, this is caused by a bug in systemd
- Allow ipc_lock for abrt to run journalctl

* Thu Nov 14 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-101
- Fix config.tgz

* Tue Nov 12 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-100
- Fix passenger_stream_connect interface
- setroubleshoot_fixit wants to read network state
- Allow procmail_t to connect to dovecot stream sockets
- Allow cimprovagt service providers to read network states
- Add labeling for /var/run/mariadb
- pwauth uses lastlog() to update system's lastlog
- Allow account provider to read login records
- Add support for texlive2013
- More fixes for user config files to make crond_t running in userdomain
- Add back disable/reload/enable permissions for system class
- Fix manage_service_perms macro
- Allow passwd_t to connect to gnome keyring to change password
- Update mls config files to have cronjobs in the user domains
- Remove access checks that systemd does not actually do

* Fri Nov 8 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-99
- Add support for yubikey in homedir
- Add support for upd/3052 port
- Allow apcupsd to use PowerChute Network Shutdown
- Allow lsmd to execute various lsmplugins
- Add labeling also for /etc/watchdog\.d where are watchdog scripts located too
- Update gluster_export_all_rw boolean to allow relabel all base file types
- Allow x86_energy_perf  tool to modify the MSR
- Fix /var/lib/dspam/data labeling

* Wed Nov 6 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-98
- Add files_relabel_base_file_types() interface
- Allow netlabel-config to read passwd
- update gluster_export_all_rw boolean to allow relabel all base file types caused by lsetxattr()
- Allow x86_energy_perf  tool to modify the MSR
- Fix /var/lib/dspam/data labeling
- Allow pegasus to domtrans to mount_t
- Add labeling for unconfined scripts in /usr/libexec/watchdog/scripts
- Add support for unconfined watchdog scripts
- Allow watchdog to manage own log files

* Wed Nov 6 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-97
- Add label only for redhat.repo instead of /etc/yum.repos.d. But probably we will need to switch for the directory.
- Label /etc/yum.repos.d as system_conf_t
- Use sysnet_filetrans_named_content in udev.te instead of generic transition for net_conf_t
- Allow dac_override for sysadm_screen_t
- Allow init_t to read ipsec_conf_t as we had it for initrc_t. Needed by ipsec unit file.
- Allow netlabel-config to read meminfo
- Add interface to allow docker to mounton file_t
- Add new interface to exec unlabeled files
- Allow lvm to use docker semaphores
- Setup transitons for .xsessions-errors.old
- Change labels of files in /var/lib/*/.ssh to transition properly
- Allow staff_t and user_t to look at logs using journalctl
- pluto wants to manage own log file
- Allow pluto running as ipsec_t to create pluto.log
- Fix alias decl in corenetwork.te.in
- Add support for fuse.glusterfs
- Allow dmidecode to read/write /run/lock/subsys/rhsmcertd
- Allow rhsmcertd to manage redhat.repo which is now labeled as system.conf. Allow rhsmcertd to manage all log files.
- Additional access for docker
- Added more rules to sblim policy
- Fix kdumpgui_run_bootloader boolean
- Allow dspam to connect to lmtp port
- Included sfcbd service into sblim policy
- rhsmcertd wants to manaage /etc/pki/consumer dir
- Add kdumpgui_run_bootloader boolean
- Add support for /var/cache/watchdog
- Remove virt_domain attribute for virt_qemu_ga_unconfined_t
- Fixes for handling libvirt containes
- Dontaudit attempts by mysql_safe to write content into /
- Dontaudit attempts by system_mail to modify network config
- Allow dspam to bind to lmtp ports
- Add new policy to allow staff_t and user_t to look at logs using journalctl
- Allow apache cgi scripts to list sysfs
- Dontaudit attempts to write/delete user_tmp_t files
- Allow all antivirus domains to manage also own log dirs
- Allow pegasus_openlmi_services_t to stream connect to sssd_t

* Fri Nov 1 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-96
- Add missing permission checks for nscd

* Wed Oct 30 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-95
- Fix alias decl in corenetwork.te.in
- Add support for fuse.glusterfs
- Add file transition rules for content created by f5link
- Rename quantum_port information to neutron
- Allow all antivirus domains to manage also own log dirs
- Rename quantum_port information to neutron
- Allow pegasus_openlmi_services_t to stream connect to sssd_t

* Mon Oct 28 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-94
- Allow sysadm_t to read login information
- Allow systemd_tmpfiles to setattr on var_log_t directories
- Udpdate Makefile to include systemd_contexts
- Add systemd_contexts
- Add fs_exec_hugetlbfs_files() interface
- Add daemons_enable_cluster_mode boolean
- Fix rsync_filetrans_named_content()
- Add rhcs_read_cluster_pid_files() interface
- Update rhcs.if with additional interfaces from RHEL6
- Fix rhcs_domain_template() to not create run dirs with cluster_var_run_t
- Allow glusterd_t to mounton glusterd_tmp_t
- Allow glusterd to unmout al filesystems
- Allow xenstored to read virt config
- Add label for swift_server.lock and make add filetrans_named_content to make sure content gets created with the correct label
- Allow mozilla_plugin_t to mmap hugepages as an executable

* Thu Oct 24 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-94
- Add back userdom_security_admin_template() interface and use it for sysadm_t if sysadm_secadm.pp

* Tue Oct 22 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-93
- Allow sshd_t to read openshift content, needs backport to RHEL6.5
- Label /usr/lib64/sasl2/libsasldb.so.3.0.0 as textrel_shlib_t
- Make sur kdump lock is created with correct label if kdumpctl is executed
- gnome interface calls should always be made within an optional_block
- Allow syslogd_t to connect to the syslog_tls port
- Add labeling for /var/run/charon.ctl socket
- Add kdump_filetrans_named_content()
- Allo setpgid for fenced_t
- Allow setpgid and r/w cluster tmpfs for fenced_t
- gnome calls should always be within optional blocks
- wicd.pid should be labeled as networkmanager_var_run_t
- Allow sys_resource for lldpad

* Thu Oct 17 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-92
- Add rtas policy

* Thu Oct 17 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-91
- Allow mailserver_domains to manage and transition to mailman data
- Dontaudit attempts by mozilla plugin to relabel content, caused by using mv and cp commands
- Allow mailserver_domains to manage and transition to mailman data
- Allow svirt_domains to read sysctl_net_t
- Allow thumb_t to use tmpfs inherited from the user
- Allow mozilla_plugin to bind to the vnc port if running with spice
- Add new attribute to discover confined_admins and assign confined admin to it
- Fix zabbix to handle attributes in interfaces
- Fix zabbix to read system states for all zabbix domains
- Fix piranha_domain_template()
- Allow ctdbd to create udp_socket. Allow ndmbd to access ctdbd var files.
- Allow lldpad sys_rouserce cap due to #986870
- Allow dovecot-auth to read nologin
- Allow openlmi-networking to read /proc/net/dev
- Allow smsd_t to execute scripts created on the fly labeled as smsd_spool_t
- Add zabbix_domain attribute for zabbix domains to treat them together
- Add labels for zabbix-poxy-* (#1018221)
- Update openlmi-storage policy to reflect #1015067
- Back port piranha tmpfs fixes from RHEL6
- Update httpd_can_sendmail boolean to allow read/write postfix spool maildrop
- Add postfix_rw_spool_maildrop_files interface
- Call new userdom_admin_user_templat() also for sysadm_secadm.pp
- Fix typo in userdom_admin_user_template()
- Allow SELinux users to create coolkeypk11sE-Gate in /var/cache/coolkey
- Add new attribute to discover confined_admins
- Fix labeling for /etc/strongswan/ipsec.d
- systemd_logind seems to pass fd to anyone who dbus communicates with it
- Dontaudit leaked write descriptor to dmesg 

* Mon Oct 14 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-90
- Activate motion policy

* Mon Oct 14 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-89
- Fix gnome_read_generic_data_home_files()
- allow openshift_cgroup_t to read/write inherited openshift file types
- Remove httpd_cobbler_content * from cobbler_admin interface
- Allow svirt sandbox domains to setattr on chr_file and blk_file svirt_sandbox_file_t, so sshd will work within a container
- Allow httpd_t to read also git sys content symlinks
- Allow init_t to read gnome home data
- Dontaudit setroubleshoot_fixit_t execmem, since it does not seem to really need it.
- Allow virsh to execute systemctl
- Fix for nagios_services plugins
- add type defintion for ctdbd_var_t
- Add support for /var/ctdb. Allow ctdb block_suspend and read /etc/passwd file
- Allow net_admin/netlink_socket all hyperv_domain domains
- Add labeling for zarafa-search.log and zarafa-search.pid
- Fix hypervkvp.te
- Fix nscd_shm_use()
- Add initial policy for /usr/sbin/hypervvssd in hypervkvp policy which should be renamed to hyperv. Also add hyperv_domain attribute to treat these HyperV services.
- Add hypervkvp_unit_file_t type
- Fix logging policy
- Allow syslog to bind to tls ports
- Update labeling for /dev/cdc-wdm
- Allow to su_domain to read init states
- Allow init_t to read gnome home data
- Make sure if systemd_logind creates nologin file with the correct label
- Clean up ipsec.te

* Tue Oct 8 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-88
- Add auth_exec_chkpwd interface
- Fix port definition for ctdb ports
- Allow systemd domains to read /dev/urand
- Dontaudit attempts for mozilla_plugin to append to /dev/random
- Add label for /var/run/charon.*
- Add labeling for /usr/lib/systemd/system/lvm2.*dd policy for motion service
- Fix for nagios_services plugins
- Fix some bugs in zoneminder policy
- add type defintion for ctdbd_var_t
- Add support for /var/ctdb. Allow ctdb block_suspend and read /etc/passwd file
- Allow net_admin/netlink_socket all hyperv_domain domains
- Add labeling for zarafa-search.log and zarafa-search.pid
- glusterd binds to random unreserved ports
- Additional allow rules found by testing glusterfs
- apcupsd needs to send a message to all users on the system so needs to look them up
- Fix the label on ~/.juniper_networks
- Dontaudit attempts for mozilla_plugin to append to /dev/random
- Allow polipo_daemon to connect to flash ports
- Allow gssproxy_t to create replay caches
- Fix nscd_shm_use()
- Add initial policy for /usr/sbin/hypervvssd in hypervkvp policy which should be renamed to hyperv. Also add hyperv_domain attribute to treat these HyperV services.
- Add hypervkvp_unit_file_t type

* Fri Oct 4 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-87
- init reload  from systemd_localed_t
- Allow domains that communicate with systemd_logind_sessions to use systemd_logind_t fd
- Allow systemd_localed_t to ask systemd to reload the locale.
- Add systemd_runtime_unit_file_t type for unit files that systemd creates in memory
- Allow readahead to read /dev/urand
- Fix lots of avcs about tuned
- Any file names xenstored in /var/log should be treated as xenstored_var_log_t
- Allow tuned to inderact with hugepages
- Allow condor domains to list etc rw dirs

* Fri Oct 4 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-86
- Fix nscd_shm_use()
- Add initial policy for /usr/sbin/hypervvssd in hypervkvp policy which should be renamed to hyperv. Also add hyperv_domain attribute to treat these HyperV services.
- Add hypervkvp_unit_file_t type
- Add additional fixes forpegasus_openlmi_account_t
- Allow mdadm to read /dev/urand
- Allow pegasus_openlmi_storage_t to create mdadm.conf and write it
- Add label/rules for /etc/mdadm.conf
- Allow pegasus_openlmi_storage_t to transition to fsadm_t
- Fixes for interface definition problems
- Dontaudit dovecot-deliver to gettatr on all fs dirs
- Allow domains to search data_home_t directories
- Allow cobblerd to connect to mysql
- Allow mdadm to r/w kdump lock files
- Add support for kdump lock files
- Label zarafa-search as zarafa-indexer
- Openshift cgroup wants to read /etc/passwd
- Add new sandbox domains for kvm
- Allow mpd to interact with pulseaudio if mpd_enable_homedirs is turned on
- Fix labeling for /usr/lib/systemd/system/lvm2.*
- Add labeling for /usr/lib/systemd/system/lvm2.*
- Fix typos to get a new build. We should not cover filename trans rules to prevent duplicate rules
- Add sshd_keygen_t policy for sshd-keygen
- Fix alsa_home_filetrans interface name and definition
- Allow chown for ssh_keygen_t
- Add fs_dontaudit_getattr_all_dirs()
- Allow init_t to manage etc_aliases_t and read xserver_var_lib_t and chrony keys
- Fix up patch to allow systemd to manage home content
- Allow domains to send/recv unlabeled traffic if unlabelednet.pp is enabled
- Allow getty to exec hostname to get info
- Add systemd_home_t for ~/.local/share/systemd directory

* Wed Oct 2 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-85
- Fix lxc labels in config.tgz

* Mon Sep 30 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-84
- Fix labeling for /usr/libexec/kde4/kcmdatetimehelper
- Allow tuned to search all file system directories
- Allow alsa_t to sys_nice, to get top performance for sound management
- Add support for MySQL/PostgreSQL for amavis
- Allow openvpn_t to manage openvpn_var_log_t files.
- Allow dirsrv_t to create tmpfs_t directories
- Allow dirsrv to create dirs in /dev/shm with dirsrv_tmpfs label
- Dontaudit leaked unix_stream_sockets into gnome keyring
- Allow telepathy domains to inhibit pipes on telepathy domains
- Allow cloud-init to domtrans to rpm
- Allow abrt daemon to manage abrt-watch tmp files
- Allow abrt-upload-watcher to search /var/spool directory
- Allow nsswitch domains to manage own process key
- Fix labeling for mgetty.* logs
- Allow systemd to dbus chat with upower
- Allow ipsec to send signull to itself
- Allow setgid cap for ipsec_t
- Match upstream labeling

* Wed Sep 25 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-83
- Do not build sanbox pkg on MLS 

* Wed Sep 25 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-82
- wine_tmp is no longer needed
- Allow setroubleshoot to look at /proc
- Allow telepathy domains to dbus with systemd logind
- Fix handling of fifo files of rpm
- Allow mozilla_plugin to transition to itself
- Allow certwatch to write to cert_t directories
- New abrt application
- Allow NetworkManager to set the kernel scheduler
- Make wine_domain shared by all wine domains
- Allow mdadm_t to read images labeled svirt_image_t
- Allow amanda to read /dev/urand
- ALlow my_print_default to read /dev/urand
- Allow mdadm to write to kdumpctl fifo files
- Allow nslcd to send signull to itself
- Allow yppasswd to read /dev/urandom
- Fix zarafa_setrlimit
- Add support for /var/lib/php/wsdlcache
- Add zarafa_setrlimit boolean
- Allow fetchmail to send mails
- Add additional alias for user_tmp_t because wine_tmp_t is no longer used
- More handling of ther kernel keyring required by kerberos
- New privs needed for init_t when running without transition to initrc_t over bin_t, and without unconfined domain installed

* Thu Sep 19 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-81
- Dontaudit attempts by sosreport to read shadow_t
- Allow browser sandbox plugins to connect to cups to print
- Add new label mpd_home_t
- Label /srv/www/logs as httpd_log_t
- Add support for /var/lib/php/wsdlcache
- Add zarafa_setrlimit boolean
- Allow fetchmail to send mails
- Add labels for apache logs under miq package
- Allow irc_t to use tcp sockets
- fix labels in puppet.if
- Allow tcsd to read utmp file
- Allow openshift_cron_t to run ssh-keygen in ssh_keygen_t to access host keys
- Define svirt_socket_t as a domain_type
- Take away transition from init_t to initrc_t when executing bin_t, allow init_t to run chk_passwd_t
- Fix label on pam_krb5 helper apps

* Thu Sep 12 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-80
- Allow ldconfig to write to kdumpctl fifo files
- allow neutron to connect to amqp ports
- Allow kdump_manage_crash to list the kdump_crash_t directory
- Allow glance-api to connect to amqp port
- Allow virt_qemu_ga_t to read meminfo
- Add antivirus_home_t type for antivirus date in HOMEDIRS
- Allow mpd setcap which is needed by pulseaudio
- Allow smbcontrol to create content in /var/lib/samba
- Allow mozilla_exec_t to be used as a entrypoint to mozilla_domtrans_spec
- Add additional labeling for qemu-ga/fsfreeze-hook.d scripts
- amanda_exec_t needs to be executable file
- Allow block_suspend cap for samba-net
- Allow apps that read ipsec_mgmt_var_run_t to search ipsec_var_run_t
- Allow init_t to run crash utility
- Treat usr_t just like bin_t for transitions and executions
- Add port definition of pka_ca to port 829 for openshift
- Allow selinux_store to use symlinks

* Mon Sep 9 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-79
- Allow block_suspend cap for samba-net
- Allow t-mission-control to manage gabble cache files
- Allow nslcd to read /sys/devices/system/cpu
- Allow selinux_store to use symlinks

* Mon Sep 9 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-78
- Allow xdm_t to transition to itself
- Call neutron interfaces instead of quantum
- Allow init to change targed role to make uncofined services (xrdp which now has own systemd unit file) working. We want them to have in unconfined_t
- Make sure directories in /run get created with the correct label
- Make sure /root/.pki gets created with the right label
- try to remove labeling for motion from zoneminder_exec_t to bin_t
- Allow inetd_t to execute shell scripts
- Allow cloud-init to read all domainstate
- Fix to use quantum port
- Add interface netowrkmanager_initrc_domtrans
- Fix boinc_execmem
- Allow t-mission-control to read gabble cache home
- Add labeling for ~/.cache/telepathy/avatars/gabble
- Allow memcache to read sysfs data
- Cleanup antivirus policy and add additional fixes
- Add boolean boinc_enable_execstack
- Add support for couchdb in rabbitmq policy
- Add interface couchdb_search_pid_dirs
- Allow firewalld to read NM state
- Allow systemd running as git_systemd to bind git port
- Fix mozilla_plugin_rw_tmpfs_files()

* Thu Sep 5 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-77
- Split out rlogin ports from inetd
- Treat files labeld as usr_t like bin_t when it comes to transitions
- Allow staff_t to read login config
- Allow ipsec_t to read .google authenticator data
- Allow systemd running as git_systemd to bind git port
- Fix mozilla_plugin_rw_tmpfs_files()
- Call the correct interface - corenet_udp_bind_ktalkd_port()
- Allow all domains that can read gnome_config to read kde config
- Allow sandbox domain to read/write mozilla_plugin_tmpfs_t so pulseaudio will work
- Allow mdadm to getattr any file system
- Allow a confined domain to executes mozilla_exec_t via dbus
- Allow cupsd_lpd_t to bind to the printer port
- Dontaudit attempts to bind to ports < 1024 when nis is turned on
- Allow apache domain to connect to gssproxy socket
- Allow rlogind to bind to the rlogin_port
- Allow telnetd to bind to the telnetd_port
- Allow ktalkd to bind to the ktalkd_port
- Allow cvs to bind to the cvs_port

* Wed Sep 4 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-76
- Cleanup related to init_domain()+inetd_domain fixes
- Use just init_domain instead of init_daemon_domain in inetd_core_service_domain
- svirt domains neeed to create kobject_uevint_sockets
- Lots of new access required for sosreport
- Allow tgtd_t to connect to isns ports
- Allow init_t to transition to all inetd domains:
- openct needs to be able to create netlink_object_uevent_sockets
- Dontaudit leaks into ldconfig_t
- Dontaudit su domains getattr on /dev devices, move su domains to attribute based calls
- Move kernel_stream_connect into all Xwindow using users
- Dontaudit inherited lock files in ifconfig o dhcpc_t

* Tue Sep 3 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-75
- Also sock_file trans rule is needed in lsm
- Fix labeling for fetchmail pid files/dirs
- Add additional fixes for abrt-upload-watch
- Fix polipo.te
- Fix transition rules in asterisk policy
- Add fowner capability to networkmanager policy
- Allow polipo to connect to tor ports
- Cleanup lsmd.if
- Cleanup openhpid policy
- Fix kdump_read_crash() interface
- Make more domains as init domain
- Fix cupsd.te
- Fix requires in rpm_rw_script_inherited_pipes
- Fix interfaces in lsm.if
- Allow munin service plugins to manage own tmpfs files/dirs
- Allow virtd_t also relabel unix stream sockets for virt_image_type
- Make ktalk as init domain
- Fix to define ktalkd_unit_file_t correctly
- Fix ktalk.fc
- Add systemd support for talk-server
- Allow glusterd to create sock_file in /run
- Allow xdm_t to delete gkeyringd_tmp_t files on logout
- Add fixes for hypervkvp policy
- Add logwatch_can_sendmail boolean
- Allow mysqld_safe_t to handle also symlinks in /var/log/mariadb
- Allow xdm_t to delete gkeyringd_tmp_t files on logout

* Thu Aug 29 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-74
- Add selinux-policy-sandbox pkg

* Tue Aug 27 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-73
0 
- Allow rhsmcertd to read init state
- Allow fsetid for pkcsslotd
- Fix labeling for /usr/lib/systemd/system/pkcsslotd.service
- Allow fetchmail to create own pid with correct labeling
- Fix rhcs_domain_template()
- Allow roles which can run mock to read mock lib files to view results
- Allow rpcbind to use nsswitch
- Fix lsm.if summary
- Fix collectd_t can read /etc/passwd file
- Label systemd unit files under dracut correctly
- Add support for pam_mount to mount user's encrypted home When a user logs in and logs out using ssh
- Add support for .Xauthority-n
- Label umount.crypt as lvm_exec_t
- Allow syslogd to search psad lib files
- Allow ssh_t to use /dev/ptmx
- Make sure /run/pluto dir is created with correct labeling
- Allow syslog to run shell and bin_t commands
- Allow ip to relabel tun_sockets
- Allow mount to create directories in files under /run
- Allow processes to use inherited fifo files

* Fri Aug 23 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-72
- Add policy for lsmd
- Add support for /var/log/mariadb dir and allow mysqld_safe to list this directory
- Update condor_master rules to allow read system state info and allow logging
- Add labeling for /etc/condor and allow condor domain to write it (bug)
- Allow condor domains to manage own logs
- Allow glusterd to read domains state
- Fix initial hypervkvp policy
- Add policy for hypervkvpd
- Fix redis.if summary

* Wed Aug 21 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-71
- Allow boinc to connect to  @/tmp/.X11-unix/X0
- Allow beam.smp to connect to tcp/5984
- Allow named to manage own log files
- Add label for /usr/libexec/dcc/start-dccifd  and domtrans to dccifd_t
- Add virt_transition_userdomain boolean decl
- Allow httpd_t to sendto unix_dgram sockets on its children
- Allow nova domains to execute ifconfig
- bluetooth wants to create fifo_files in /tmp
- exim needs to be able to manage mailman data
- Allow sysstat to getattr on all file systems
- Looks like bluetoothd has moved
- Allow collectd to send ping packets
- Allow svirt_lxc domains to getpgid
- Remove virt-sandbox-service labeling as virsh_exec_t, since it no longer does virsh_t stuff
- Allow frpintd_t to read /dev/urandom
- Allow asterisk_t to create sock_file in /var/run
- Allow usbmuxd to use netlink_kobject
- sosreport needs to getattr on lots of devices, and needs access to netlink_kobject_uevent_socket
- More cleanup of svirt_lxc policy
- virtd_lxc_t now talks to dbus
- Dontaudit leaked ptmx_t
- Allow processes to use inherited fifo files
- Allow openvpn_t to connect to squid ports
- Allow prelink_cron_system_t to ask systemd to reloaddd miscfiles_dontaudit_access_check_cert()
- Allow ssh_t to use /dev/ptmx
- Make sure /run/pluto dir is created with correct labeling
- Allow syslog to run shell and bin_t commands
- Allow ip to relabel tun_sockets
- Allow mount to create directories in files under /run
- Allow processes to use inherited fifo files
- Allow user roles to connect to the journal socket

* Thu Aug 8 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-70
- selinux_set_enforce_mode needs to be used with type
- Add append to the dontaudit for unix_stream_socket of xdm_t leak
- Allow xdm_t to create symlinks in log direcotries
- Allow login programs to read afs config
- Label 10933 as a pop port, for dovecot
- New policy to allow selinux_server.py to run as semanage_t as a dbus service
- Add fixes to make netlabelctl working on MLS
- AVCs required for running sepolicy gui as staff_t
- Dontaudit attempts to read symlinks, sepolicy gui is likely to cause this type of AVC
- New dbus server to be used with new gui
- After modifying some files in /etc/mail, I saw this needed on the next boot
- Loading a vm from /usr/tmp with virt-manager
- Clean up oracleasm policy for Fedora
- Add oracleasm policy written by rlopez@redhat.com
- Make postfix_postdrop_t as mta_agent to allow domtrans to system mail if it is executed by apache
- Add label for /var/crash
- Allow fenced to domtrans to sanclok_t
- Allow nagios to manage nagios spool files
- Make tfptd as home_manager
- Allow kdump to read kcore on MLS system
- Allow mysqld-safe sys_nice/sys_resource caps
- Allow apache to search automount tmp dirs if http_use_nfs is enabled
- Allow crond to transition to named_t, for use with unbound
- Allow crond to look at named_conf_t, for unbound
- Allow mozilla_plugin_t to transition its home content
- Allow dovecot_domain to read all system and network state
- Allow httpd_user_script_t to call getpw
- Allow semanage to read pid files
- Dontaudit leaked file descriptors from user domain into thumb
- Make PAM authentication working if it is enabled in ejabberd
- Add fixes for rabbit to fix ##992920,#992931
- Allow glusterd to mount filesystems
- Loading a vm from /usr/tmp with virt-manager
- Trying to load a VM I got an AVC from devicekit_disk for loopcontrol device
- Add fix for pand service
- shorewall touches own log
- Allow nrpe to list /var
- Mozilla_plugin_roles can not be passed into lpd_run_lpr
- Allow afs domains to read afs_config files
- Allow login programs to read afs config
- Allow virt_domain to read virt_var_run_t symlinks
- Allow smokeping to send its process signals
- Allow fetchmail to setuid
- Add kdump_manage_crash() interface
- Allow abrt domain to write abrt.socket

* Wed Jul 31 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-69
- Add more aliases in pegasus.te
- Add more fixes for *_admin interfaces
- Add interface fixes
- Allow nscd to stream connect to nmbd
- Allow gnupg apps to write to pcscd socket
- Add more fixes for openlmi provides. Fix naming and support for additionals
- Allow fetchmail to resolve host names
- Allow firewalld to interact also with lnk files labeled as firewalld_etc_rw_t
- Add labeling for cmpiLMI_Fan-cimprovagt
- Allow net_admin for glusterd
- Allow telepathy domain to create dconf with correct labeling in /home/userX/.cache/
- Add pegasus_openlmi_system_t
- Fix puppet_domtrans_master() to make all puppet calling working in passenger.te
- Fix corecmd_exec_chroot()
- Fix logging_relabel_syslog_pid_socket interface
- Fix typo in unconfineduser.te
- Allow system_r to access unconfined_dbusd_t to run hp_chec

* Tue Jul 30 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-68
- Allow xdm_t to act as a dbus client to itsel
- Allow fetchmail to resolve host names
- Allow gnupg apps to write to pcscd socket
- Add labeling for cmpiLMI_Fan-cimprovagt
- Allow net_admin for glusterd
- Allow telepathy domain to create dconf with correct labeling in /home/userX/.cache/
- Add pegasus_openlmi_system_t
- Fix puppet_domtrans_master() to make all puppet calling working in passenger.te
-httpd_t does access_check on certs

* Fri Jul 26 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-67
- Add support for cmpiLMI_Service-cimprovagt
- Allow pegasus domtrans to rpm_t to make pycmpiLMI_Software-cimprovagt running as rpm_t
- Label pycmpiLMI_Software-cimprovagt as rpm_exec_t
- Add support for pycmpiLMI_Storage-cimprovagt
- Add support for cmpiLMI_Networking-cimprovagt
- Allow system_cronjob_t to create user_tmpfs_t to make pulseaudio working
- Allow virtual machines and containers to run as user doains, needed for virt-sandbox
- Allow buglist.cgi to read cpu info

* Mon Jul 22 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-66
- Allow systemd-tmpfile to handle tmp content in print spool dir
- Allow systemd-sysctl to send system log messages
- Add support for RTP media ports and fmpro-internal
- Make auditd working if audit is configured to perform SINGLE action on disk error
- Add interfaces to handle systemd units
- Make systemd-notify working if pcsd is used
- Add support for netlabel and label /usr/sbin/netlabelctl as iptables_exec_t
- Instead of having all unconfined domains get all of the named transition rules,
- Only allow unconfined_t, init_t, initrc_t and rpm_script_t by default.
- Add definition for the salt ports
- Allow xdm_t to create link files in xdm_var_run_t
- Dontaudit reads of blk files or chr files leaked into ldconfig_t
- Allow sys_chroot for useradd_t
- Allow net_raw cap for ipsec_t
- Allow sysadm_t to reload services
- Add additional fixes to make strongswan working with a simple conf
- Allow sysadm_t to enable/disable init_t services
- Add additional glusterd perms
- Allow apache to read lnk files in the /mnt directory
- Allow glusterd to ask the kernel to load a module
- Fix description of ftpd_use_fusefs boolean
- Allow svirt_lxc_net_t to sys_chroot, modify policy to tighten up svirt_lxc_domain capabilties and process controls, but add them to svirt_lxc_net_t
- Allow glusterds to request load a kernel module
- Allow boinc to stream connect to xserver_t
- Allow sblim domains to read /etc/passwd
- Allow mdadm to read usb devices
- Allow collectd to use ping plugin
- Make foghorn working with SNMP
- Allow sssd to read ldap certs
- Allow haproxy to connect to RTP media ports
- Add additional trans rules for aide_db
- Add labeling for /usr/lib/pcsd/pcsd
- Add labeling for /var/log/pcsd
- Add support for pcs which is a corosync and pacemaker configuration tool

* Wed Jul 17 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-65
- Label /var/lib/ipa/pki-ca/publish as pki_tomcat_cert_t
- Add labeling for /usr/libexec/kde4/polkit-kde-authentication-agent-1
- Allow all domains that can domtrans to shutdown, to start the power services script to shutdown
- consolekit needs to be able to shut down system
- Move around interfaces
- Remove nfsd_rw_t and nfsd_ro_t, they don't do anything
- Add additional fixes for rabbitmq_beam to allow getattr on mountpoints
- Allow gconf-defaults-m to read /etc/passwd
- Fix pki_rw_tomcat_cert() interface to support lnk_files

* Fri Jul 12 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-64
- Add support for gluster ports
- Make sure that all keys located in /etc/ssh/ are labeled correctly
- Make sure apcuspd lock files get created with the correct label
- Use getcap in gluster.te
- Fix gluster policy
- add additional fixes to allow beam.smp to interact with couchdb files
- Additional fix for #974149
- Allow gluster to user gluster ports
- Allow glusterd to transition to rpcd_t and add additional fixes for #980683
- Allow tgtd working when accessing to the passthrough device
- Fix labeling for mdadm unit files

* Thu Jul 11 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-63
- Add mdadm fixes

* Tue Jul 9 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-62
- Fix definition of sandbox.disabled to sandbox.pp.disabled

* Mon Jul 8 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-61
- Allow mdamd to execute systemctl
- Allow mdadm to read /dev/kvm
- Allow ipsec_mgmt_t to read l2tpd pid content

* Mon Jul 8 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-60
- Allow nsd_t to read /dev/urand
- Allow mdadm_t to read framebuffer
- Allow rabbitmq_beam_t to read process info on rabbitmq_epmd_t
- Allow mozilla_plugin_config_t to create tmp files
- Cleanup openvswitch policy
- Allow mozilla plugin to getattr on all executables
- Allow l2tpd_t to create fifo_files in /var/run
- Allow samba to touch/manage fifo_files or sock_files in a samba_share_t directory
- Allow mdadm to connecto its own unix_stream_socket
- FIXME: nagios changed locations to /log/nagios which is wrong. But we need to have this workaround for now.
- Allow apache to access smokeping pid files
- Allow rabbitmq_beam_t to getattr on all filesystems
- Add systemd support for iodined
- Allow nup_upsdrvctl_t to execute its entrypoint
- Allow fail2ban_client to write to fail2ban_var_run_t, Also allow it to use nsswitch
- add labeling for ~/.cache/libvirt-sandbox
- Add interface to allow domains transitioned to by confined users to send sigchld to screen program
- Allow sysadm_t to check the system status of files labeled etc_t, /etc/fstab
- Allow systemd_localed to start /usr/lib/systemd/system/systemd-vconsole-setup.service
- Allow an domain that has an entrypoint from a type to be allowed to execute the entrypoint without a transition,  I can see no case where this is  a bad thing, and elminiates a whole class of AVCs.
- Allow staff to getsched all domains, required to run htop
- Add port definition for redis port
- fix selinuxuser_use_ssh_chroot boolean

* Wed Jul 3 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-59
- Add prosody policy written by Michael Scherer
- Allow nagios plugins to read /sys info
- ntpd needs to manage own log files
- Add support for HOME_DIR/.IBMERS
- Allow iptables commands to read firewalld config
- Allow consolekit_t to read utmp
- Fix filename transitions on .razor directory
- Add additional fixes to make DSPAM with LDA working
- Allow snort to read /etc/passwd
- Allow fail2ban to communicate with firewalld over dbus
- Dontaudit openshift_cgreoup_file_t read/write leaked dev
- Allow nfsd to use mountd port
- Call th proper interface
- Allow openvswitch to read sys and execute plymouth
- Allow tmpwatch to read /var/spool/cups/tmp
- Add support for /usr/libexec/telepathy-rakia
- Add systemd support for zoneminder
- Allow mysql to create files/directories under /var/log/mysql
- Allow zoneminder apache scripts to rw zoneminder tmpfs
- Allow httpd to manage zoneminder lib files
- Add zoneminder_run_sudo boolean to allow to start zoneminder
- Allow zoneminder to send mails
- gssproxy_t sock_file can be under /var/lib
- Allow web domains to connect to whois port.
- Allow sandbox_web_type to connect to the same ports as mozilla_plugin_t.
- We really need to add an interface to corenet to define what a web_client_domain is and
- then define chrome_sandbox_t, mozilla_plugin_t and sandbox_web_type to that domain.
- Add labeling for cmpiLMI_LogicalFile-cimprovagt
- Also make pegasus_openlmi_logicalfile_t as unconfined to have unconfined_domain attribute for filename trans rules
- Update policy rules for pegasus_openlmi_logicalfile_t
- Add initial types for logicalfile/unconfined OpenLMI providers
- mailmanctl needs to read own log
- Allow logwatch manage own lock files
- Allow nrpe to read meminfo
- Allow httpd to read certs located in pki-ca
- Add pki_read_tomcat_cert() interface
- Add support for nagios openshift plugins
- Add port definition for redis port
- fix selinuxuser_use_ssh_chroot boolean

* Fri Jun 28 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-58
- Shrink the size of policy by moving to attributes, also add dridomain so that mozilla_plugin can follow selinuxuse_dri boolean. 
- Allow bootloader to manage generic log files 
- Allow ftp to bind to port 989 
- Fix label of new gear directory 
- Add support for new directory /var/lib/openshift/gears/ 
- Add openshift_manage_lib_dirs() 
- allow virtd domains to manage setrans_var_run_t 
- Allow useradd to manage all openshift content 
- Add support so that mozilla_plugin_t can use dri devices 
- Allow chronyd to change the scheduler 
- Allow apmd to shut downthe system 
- Devicekit_disk_t needs to manage /etc/fstab

* Wed Jun 26 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-57
- Make DSPAM to act as a LDA working
- Allow ntop to create netlink socket
- Allow policykit to send a signal to policykit-auth
- Allow stapserver to dbus chat with avahi/systemd-logind
- Fix labeling on haproxy unit file
- Clean up haproxy policy
- A new policy for haproxy and placed it to rhcs.te
- Add support for ldirectord and treat it with cluster_t
- Make sure anaconda log dir is created with var_log_t

* Mon Jun 24 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-56
- Allow lvm_t to create default targets for filesystem handling
- Fix labeling for razor-lightdm binaries
- Allow insmod_t to read any file labeled var_lib_t
- Add policy for pesign
- Activate policy for cmpiLMI_Account-cimprovagt
- Allow isnsd syscall=listen
- /usr/libexec/pegasus/cimprovagt needs setsched caused by sched_setscheduler
- Allow ctdbd to use udp/4379
- gatherd wants sys_nice and setsched
- Add support for texlive2012
- Allow NM to read file_t (usb stick with no labels used to transfer keys for example)
- Allow cobbler to execute apache with domain transition

* Fri Jun 21 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-55
- condor_collector uses tcp/9000
- Label /usr/sbin/virtlockd as virtd_exec_t for now
- Allow cobbler to execute ldconfig
- Allow NM to execute ssh
- Allow mdadm to read /dev/crash
- Allow antivirus domains to connect to snmp port
- Make amavisd-snmp working correctly
- Allow nfsd_t to mounton nfsd_fs_t
- Add initial snapper policy
- We still need to have consolekit policy
- Dontaudit firefox attempting to connect to the xserver_port_t if run within sandbox_web_t
- Dontaudit sandbox apps attempting to open user_devpts_t
- Allow dirsrv to read network state
- Fix pki_read_tomcat_lib_files
- Add labeling for /usr/libexec/nm-ssh-service
- Add label cert_t for /var/lib/ipa/pki-ca/publish
- Lets label /sys/fs/cgroup as cgroup_t for now, to keep labels consistant
- Allow nfsd_t to mounton nfsd_fs_t
- Dontaudit sandbox apps attempting to open user_devpts_t
- Allow passwd_t to change role to system_r from unconfined_r

* Wed Jun 19 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-54
- Don't audit access checks by sandbox xserver on xdb var_lib
- Allow ntop to read usbmon devices
- Add labeling for new polcykit authorizor
- Dontaudit access checks from fail2ban_client
- Don't audit access checks by sandbox xserver on xdb var_lib
- Allow apps that connect to xdm stream to conenct to xdm_dbusd_t stream
- Fix labeling for all /usr/bim/razor-lightdm-* binaries
- Add filename trans for /dev/md126p1

* Tue Jun 18 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-53
- Make vdagent able to request loading kernel module
- Add support for cloud-init make it as unconfined domain
- Allow snmpd to run smartctl in fsadm_t domain
- remove duplicate openshift_search_lib() interface
- Allow mysqld to search openshift lib files
- Allow openshift cgroup to interact with passedin file descriptors
- Allow colord to list directories inthe users homedir
- aide executes prelink to check files
- Make sure cupsd_t creates content in /etc/cups with the correct label
- Lest dontaudit apache read all domains, so passenger will not cause this avc
- Allow gssd to connect to gssproxy
- systemd-tmpfiles needs to be able to raise the level to fix labeling on /run/setrans in MLS
- Allow systemd-tmpfiles to relabel also lock files
- Allow useradd to add homdir in /var/lib/openshift
- Allow setfiles and semanage to write output to /run/files

* Fri Jun 14 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-52
- Add labeling for /dev/tgt
- Dontaudit leak fd from firewalld for modprobe
- Allow runuser running as rpm_script_t to create netlink_audit socket
- Allow mdadm to read BIOS non-volatile RAM

* Thu Jun 13 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-51
- accountservice watches when accounts come and go in wtmp
- /usr/java/jre1.7.0_21/bin/java needs to create netlink socket
- Add httpd_use_sasl boolean
- Allow net_admin for tuned_t
- iscsid needs sys_module to auto-load kernel modules
- Allow blueman to read bluetooth conf
- Add nova_manage_lib_files() interface
- Fix mplayer_filetrans_home_content()
- Add mplayer_filetrans_home_content()
- mozilla_plugin_config_roles need to be able to access mozilla_plugin_config_t
- Revert "Allow thumb_t to append inherited xdm stream socket"
- Add iscsi_filetrans_named_content() interface
- Allow to create .mplayer with the correct labeling for unconfined
- Allow iscsiadmin to create lock file with the correct labeling

* Tue Jun 11 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-50
- Allow wine to manage wine home content
- Make amanda working with socket actiovation
- Add labeling for /usr/sbin/iscsiadm
- Add support for /var/run/gssproxy.sock
- dnsmasq_t needs to read sysctl_net_t

* Fri Jun 7 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-49
- Fix courier_domain_template() interface
- Allow blueman to write ip_forward
- Allow mongodb to connect to mongodb port
- Allow mongodb to connect to mongodb port
- Allow java to bind jobss_debug port
- Fixes for *_admin interfaces
- Allow iscsid auto-load kernel modules needed for proper iSCSI functionality
- Need to assign attribute for courier_domain to all courier_domains
- Fail2ban reads /etc/passwd
- postfix_virtual will create new files in postfix_spool_t
- abrt triggers sys_ptrace by running pidof
- Label ~/abc as mozilla_home_t, since java apps as plugin want to create it
- Add passenger fixes needed by foreman
- Remove dup interfaces
- Add additional interfaces for quantum
- Add new interfaces for dnsmasq
- Allow  passenger to read localization and send signull to itself
- Allow dnsmasq to stream connect to quantum
- Add quantum_stream_connect()
- Make sure that mcollective starts the service with the correct labeling
- Add labels for ~/.manpath
- Dontaudit attempts by svirt_t to getpw* calls
- sandbox domains are trying to look at parent process data
- Allow courior auth to create its pid file in /var/spool/courier subdir
- Add fixes for beam to have it working with couchdb
- Add labeling for /run/nm-xl2tpd.con
- Allow apache to stream connect to thin
- Add systemd support for amand
- Make public types usable for fs mount points
- Call correct mandb interface in domain.te
- Allow iptables to r/w quantum inherited pipes and send sigchld
- Allow ifconfig domtrans to iptables and execute ldconfig
- Add labels for ~/.manpath
- Allow systemd to read iscsi lib files
- seunshare is trying to look at parent process data

* Mon Jun 3 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-48
- Fix openshift_search_lib
- Add support for abrt-uefioops-oops
- Allow colord to getattr any file system
- Allow chrome processes to look at each other
- Allow sys_ptrace for abrt_t
- Add new policy for gssproxy
- Dontaudit leaked file descriptor writes from firewalld
- openshift_net_type is interface not template
- Dontaudit pppd to search gnome config
- Update openshift_search_lib() interface
- Add fs_list_pstorefs()
- Fix label on libbcm_host.so since it is built incorrectly on raspberry pi, needs back port to F18
- Better labels for raspberry pi devices
- Allow init to create devpts_t directory
- Temporarily label rasbery pi devices as memory_device_t, needs back port to f18
- Allow sysadm_t to build kernels
- Make sure mount creates /var/run/blkid with the correct label, needs back port to F18
- Allow userdomains to stream connect to gssproxy
- Dontaudit leaked file descriptor writes from firewalld
- Allow xserver to read /dev/urandom
- Add additional fixes for ipsec-mgmt
- Make SSHing into an Openshift Enterprise Node working

* Wed May 29 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-47
- Add transition rules to unconfined domains and to sysadm_t to create /etc/adjtime
- with the proper label.
- Update files_filetrans_named_content() interface to get right labeling for pam.d conf files
- Allow systemd-timedated to create adjtime
- Add clock_create_adjtime()
- Additional fix ifconfing for #966106
- Allow kernel_t to create boot.log with correct labeling
- Remove unconfined_mplayer for which we don't have rules
- Rename interfaces
- Add userdom_manage_user_home_files/dirs interfaces
- Fix files_dontaudit_read_all_non_security_files
- Fix ipsec_manage_key_file()
- Fix ipsec_filetrans_key_file()
- Label /usr/bin/razor-lightdm-greeter as xdm_exec_t instead of spamc_exec_t
- Fix labeling for ipse.secrets
- Add interfaces for ipsec and labeling for ipsec.info and ipsec_setup.pid
- Add files_dontaudit_read_all_non_security_files() interface
- /var/log/syslog-ng should be labeled var_log_t
- Make ifconfig_var_run_t a mountpoint
- Add transition from ifconfig to dnsmasq
- Allow ifconfig to execute bin_t/shell_exec_t
- We want to have hwdb.bin labeled as etc_t
- update logging_filetrans_named_content() interface
- Allow systemd_timedate_t to manage /etc/adjtime
- Allow NM to send signals to l2tpd
- Update antivirus_can_scan_system boolean
- Allow devicekit_disk_t to sys_config_tty
- Run abrt-harvest programs as abrt_t, and allow abrt_t to list all filesystem directories
- Make printing from vmware working
- Allow php-cgi from php54 collection to access /var/lib/net-snmp/mib_indexes
- Add virt_qemu_ga_data_t for qemu-ga
- Make chrome and mozilla able to connect to same ports, add jboss_management_port_t to both
- Fix typo in virt.te
- Add virt_qemu_ga_unconfined_t for hook scripts
- Make sure NetworkManager files get created with the correct label
- Add mozilla_plugin_use_gps boolean
- Fix cyrus to have support for net-snmp
- Additional fixes for dnsmasq and quantum for #966106
- Add plymouthd_create_log()
- remove httpd_use_oddjob for which we don't have rules
- Add missing rules for httpd_can_network_connect_cobbler
- Add missing cluster_use_execmem boolean
- Call userdom_manage_all_user_home_type_files/dirs
- Additional fix for ftp_home_dir
- Fix ftp_home_dir boolean
- Allow squit to recv/send client squid packet
- Fix nut.te to have nut_domain attribute
- Add support for ejabberd; TODO: revisit jabberd and rabbit policy
- Fix amanda policy
- Add more fixes for domains which use libusb
- Make domains which use libusb working correctly
- Allow l2tpd to create ipsec key files with correct labeling and manage them
- Fix cobbler_manage_lib_files/cobbler_read_lib_files to cover also lnk files
- Allow rabbitmq-beam to bind generic node
- Allow l2tpd to read ipse-mgmt pid files
- more fixes for l2tpd, NM and pppd from #967072

* Wed May 22 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-46
- Dontaudit to getattr on dirs for dovecot-deliver
- Allow raiudusd server connect to postgresql socket
- Add kerberos support for radiusd
- Allow saslauthd to connect to ldap port
- Allow postfix to manage postfix_private_t files
- Add chronyd support for #965457
- Fix labeling for HOME_DIR/\.icedtea
- CHange squid and snmpd to be allowed also write own logs
- Fix labeling for /usr/libexec/qemu-ga
- Allow virtd_t to use virt_lock_t
- Allow also sealert to read the policy from the kernel
- qemu-ga needs to execute scripts in /usr/libexec/qemu-ga and to use /tmp content
- Dontaudit listing of users homedir by sendmail Seems like a leak
- Allow passenger to transition to puppet master
- Allow apache to connect to mythtv
- Add definition for mythtv ports

* Fri May 17 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-45
- Add additional fixes for #948073 bug
- Allow sge_execd_t to also connect to sge ports
- Allow openshift_cron_t to manage openshift_var_lib_t sym links
- Allow openshift_cron_t to manage openshift_var_lib_t sym links
- Allow sge_execd to bind sge ports. Allow kill capability and reads cgroup files
- Remove pulseaudio filetrans pulseaudio_manage_home_dirs which is a part of pulseaudio_manage_home_files
- Add networkmanager_stream_connect()
- Make gnome-abrt wokring with staff_t
- Fix openshift_manage_lib_files() interface
- mdadm runs ps command which seems to getattr on random log files
- Allow mozilla_plugin_t to create pulseaudit_home_t directories
- Allow qemu-ga to shutdown virtual hosts
- Add labelling for cupsd-browsed
- Add web browser plugins to connect to aol ports
- Allow nm-dhcp-helper to stream connect to NM
- Add port definition for sge ports

* Mon May 13 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-44
- Make sure users and unconfined domains create .hushlogin with the correct label
- Allow pegaus to chat with realmd over DBus
- Allow cobblerd to read network state
- Allow boicn-client to stat on /dev/input/mice
- Allow certwatch to read net_config_t when it executes apache
- Allow readahead to create /run/systemd and then create its own directory with the correct label

* Mon May 13 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-43
- Transition directories and files when in a user_tmp_t directory
- Change certwatch to domtrans to apache instead of just execute
- Allow virsh_t to read xen lib files
- update policy rules for pegasus_openlmi_account_t
- Add support for svnserve_tmp_t
- Activate account openlmi policy
- pegasus_openlmi_domain_template needs also require pegasus_t
- One more fix for policykit.te
- Call fs_list_cgroups_dirs() in policykit.te
- Allow nagios service plugin to read mysql config files
- Add labeling for /var/svn
- Fix chrome.te
- Fix pegasus_openlmi_domain_template() interfaces
- Fix dev_rw_vfio_dev definiton, allow virtd_t to read tmpfs_t symlinks
- Fix location of google-chrome data
- Add support for chome_sandbox to store content in the homedir
- Allow policykit to watch for changes in cgroups file system
- Add boolean to allow  mozilla_plugin_t to use spice
- Allow collectd to bind to udp port
- Allow collected_t to read all of /proc
- Should use netlink socket_perms
- Should use netlink socket_perms
- Allow glance domains to connect to apache ports
- Allow apcupsd_t to manage its log files
- Allow chrome objects to rw_inherited unix_stream_socket from callers
- Allow staff_t to execute virtd_exec_t for running vms
- nfsd_t needs to bind mountd port to make nfs-mountd.service working
- Allow unbound net_admin capability because of setsockopt syscall
- Fix fs_list_cgroup_dirs()
- Label /usr/lib/nagios/plugins/utils.pm as bin_t
- Remove uplicate definition of fs_read_cgroup_files()
- Remove duplicate definition of fs_read_cgroup_files()
- Add files_mountpoint_filetrans interface to be used by quotadb_t and snapperd
- Additional interfaces needed to list and read cgroups config
- Add port definition for collectd port
- Add labels for /dev/ptp*
- Allow staff_t to execute virtd_exec_t for running vms

* Mon May 6 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-42
- Allow samba-net to also read realmd tmp files
- Allow NUT to use serial ports
- realmd can be started by systemctl now

* Mon May 6 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-41
- Remove userdom_home_manager for xdm_t and move all rules to xserver.te directly
- Add new xdm_write_home boolean to allow xdm_t to create files in HOME dirs with xdm_home_t
- Allow postfix-showq to read/write unix.showq in /var/spool/postfix/pid
- Allow virsh to read xen lock file
- Allow qemu-ga to create files in /run with proper labeling
- Allow glusterd to connect to own socket in /tmp
- Allow glance-api to connect to http port to make glance image-create working
- Allow keystonte_t to execute rpm

* Fri May 3 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-40
- Fix realmd cache interfaces

* Fri May 3 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-39
- Allow tcpd to execute leafnode
- Allow samba-net to read realmd cache files
- Dontaudit sys_tty_config for alsactl
- Fix allow rules for postfix_var_run
- Allow cobblerd to read /etc/passwd
- Allow pegasus to read exports
- Allow systemd-timedate to read xdm state
- Allow mout to stream connect to rpcbind
- Add labeling just for /usr/share/pki/ca-trust-source instead of /usr/share/pki

* Tue Apr 30 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-38
- Allow thumbnails to share memory with apps which run thumbnails
- Allow postfix-postqueue block_suspend
- Add lib interfaces for smsd
- Add support for nginx
- Allow s2s running as jabberd_t to connect to jabber_interserver_port_t
- Allow pki apache domain to create own tmp files and execute httpd_suexec
- Allow procmail to manger user tmp files/dirs/lnk_files
- Add virt_stream_connect_svirt() interface
- Allow dovecot-auth to execute bin_t
- Allow iscsid to request that kernel load a kernel module
- Add labeling support for /var/lib/mod_security
- Allow iw running as tuned_t to create netlink socket
- Dontaudit sys_tty_config for thumb_t
- Add labeling for nm-l2tp-service
- Allow httpd running as certwatch_t to open tcp socket
- Allow useradd to manager smsd lib files
- Allow useradd_t to add homedirs in /var/lib
- Fix typo in userdomain.te
- Cleanup userdom_read_home_certs
- Implement userdom_home_reader_certs_type to allow read certs also on encrypt /home with ecryptfs_t
- Allow staff to stream connect to svirt_t to make gnome-boxes working

* Fri Apr 26 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-37
- Allow lvm to create its own unit files
- Label /var/lib/sepolgen as selinux_config_t
- Add filetrans rules for tw devices
- Add transition from cupsd_config_t to cupsd_t

* Wed Apr 24 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-36
- Add filetrans rules for tw devices
- Cleanup bad transition lines

* Tue Apr 23 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-35
- Fix lockdev_manage_files()
- Allow setroubleshootd to read var_lib_t to make email_alert working
- Add lockdev_manage_files()
- Call proper interface in virt.te
- Allow gkeyring_domain to create /var/run/UID/config/dbus file
- system dbus seems to be blocking suspend
- Dontaudit attemps to sys_ptrace, which I believe gpsd does not need
- When you enter a container from root, you generate avcs with a leaked file descriptor
- Allow mpd getattr on file system directories
- Make sure realmd creates content with the correct label
- Allow systemd-tty-ask to write kmsg
- Allow mgetty to use lockdev library for device locking
- Fix selinuxuser_user_share_music boolean name to selinuxuser_share_music
- When you enter a container from root, you generate avcs with a leaked file descriptor
- Make sure init.fc files are labeled correctly at creation
- File name trans vconsole.conf
- Fix labeling for nagios plugins
- label shared libraries in /opt/google/chrome as testrel_shlib_t

* Thu Apr 18 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-34
- Allow certmonger to dbus communicate with realmd 
- Make realmd working

* Thu Apr 18 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-33
- Fix mozilla specification of homedir content
- Allow certmonger to read network state
- Allow tmpwatch to read tmp in /var/spool/{cups,lpd}
- Label all nagios plugin as unconfined by default
- Add httpd_serve_cobbler_files()
- Allow mdadm to read /dev/sr0 and create tmp files
- Allow certwatch to send mails
- Fix labeling for nagios plugins
- label shared libraries in /opt/google/chrome as testrel_shlib_t

* Wed Apr 17 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-32
- Allow realmd to run ipa, really needs to be an unconfined_domain
- Allow sandbox domains to use inherted terminals
- Allow pscd to use devices labeled svirt_image_t in order to use cat cards.
- Add label for new alsa pid
- Alsa now uses a pid file and needs to setsched 
- Fix oracleasmfs_t definition
- Add support for sshd_unit_file_t
- Add oracleasmfs_t
- Allow unlabeled_t files to be stored on unlabeled_t filesystems

* Tue Apr 16 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-31
- Fix description of deny_ptrace boolean
- Remove allow for execmod lib_t for now
- Allow quantum to connect to keystone port
- Allow nova-console to talk with mysql over unix stream socket
- Allow dirsrv to stream connect to uuidd
- thumb_t needs to be able to create ~/.cache if it does not exist
- virtd needs to be able to sys_ptrace when starting and stoping containers

* Mon Apr 15 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-30
- Allow alsa_t signal_perms, we probaly should search for any app that can execute something without transition and give it signal_perms...
- Add dontaudit for mozilla_plugin_t looking at the xdm_t sockets
- Fix deny_ptrace boolean, certain ptrace leaked into the system
- Allow winbind to manage kerberos_rcache_host
- Allow spamd to create spamd_var_lib_t directories
- Remove transition to mozilla_tmp_t by mozilla_t, to allow it to manage the users tmp dirs
- Add mising nslcd_dontaudit_write_sock_file() interface
- one more fix
- Fix pki_read_tomcat_lib_files() interface
- Allow certmonger to read pki-tomcat lib files
- Allow certwatch to execute bin_t
- Allow snmp to manage /var/lib/net-snmp files
- Call snmp_manage_var_lib_files(fogorn_t) instead of snmp_manage_var_dirs
- Fix vmware_role() interface
- Fix cobbler_manage_lib_files() interface
- Allow nagios check disk plugins to execute bin_t
- Allow quantum to transition to openvswitch_t
- Allow postdrop to stream connect to postfix-master
- Allow quantum to stream connect to openvswitch
- Add xserver_dontaudit_xdm_rw_stream_sockets() interface
- Allow daemon to send dgrams to initrc_t
- Allow kdm to start the power service to initiate a reboot or poweroff

* Thu Apr 11 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-29
- Add mising nslcd_dontaudit_write_sock_file() interface
- one more fix
- Fix pki_read_tomcat_lib_files() interface
- Allow certmonger to read pki-tomcat lib files
- Allow certwatch to execute bin_t
- Allow snmp to manage /var/lib/net-snmp files
- Don't audit attempts to write to stream socket of nscld by thumbnailers
- Allow git_system_t to read network state
- Allow pegasas to execute mount command
- Fix desc for drdb_admin
- Fix condor_amin()
- Interface fixes for uptime, vdagent, vnstatd
- Fix labeling for moodle in /var/www/moodle/data
- Add interface fixes
- Allow bugzilla to read certs
- /var/www/moodle needs to be writable by apache
- Add interface to dontaudit attempts to send dbus messages to systemd domains, for xguest
- Fix namespace_init_t to create content with proper labels, and allow it to manage all user content
- Allow httpd_t to connect to osapi_compute port using httpd_use_openstack bolean
- Fixes for dlm_controld
- Fix apache_read_sys_content_rw_dirs() interface
- Allow logrotate to read /var/log/z-push dir
- Fix sys_nice for cups_domain
- Allow postfix_postdrop to acces postfix_public socket
- Allow sched_setscheduler for cupsd_t
- Add missing context for /usr/sbin/snmpd
- Kernel_t needs mac_admin in order to support labeled NFS
- Fix systemd_dontaudit_dbus_chat() interface
- Add interface to dontaudit attempts to send dbus messages to systemd domains, for xguest
- Allow consolehelper domain to write Xauth files in /root
- Add port definition for osapi_compute port
- Allow unconfined to create /etc/hostname with correct labeling
- Add systemd_filetrans_named_hostname() interface

* Mon Apr 8 2013 Dan Walsh <dwalsh@redhat.com> 3.12.1-28
- Allow httpd_t to connect to osapi_compute port using httpd_use_openstack bolean
- Fixes for dlm_controld
- Fix apache_read_sys_content_rw_dirs() interface
- Allow logrotate to read /var/log/z-push dir
- Allow postfix_postdrop to acces postfix_public socket
- Allow sched_setscheduler for cupsd_t
- Add missing context for /usr/sbin/snmpd
- Allow consolehelper more access discovered by Tom London
- Allow fsdaemon to send signull to all domain
- Add port definition for osapi_compute port
- Allow unconfined to create /etc/hostname with correct labeling
- Add systemd_filetrans_named_hostname() interface

* Sat Apr 6 2013 Dan Walsh <dwalsh@redhat.com> 3.12.1-27
- Fix file_contexts.subs to label /run/lock correctly

* Fri Apr 5 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-26
- Try to label on controlC devices up to 30 correctly
- Add mount_rw_pid_files() interface
- Add additional mount/umount interfaces needed by mock
- fsadm_t sends audit messages in reads kernel_ipc_info when doing livecd-iso-to-disk
- Fix tabs
- Allow initrc_domain to search rgmanager lib files
- Add more fixes which make mock working together with confined users
  * Allow mock_t to manage rpm files
  * Allow mock_t to read rpm log files
  * Allow mock to setattr on tmpfs, devpts
  * Allow mount/umount filesystems
- Add rpm_read_log() interface
- yum-cron runs rpm from within it.
- Allow tuned to transition to dmidecode
- Allow firewalld to do net_admin
- Allow mock to unmont tmpfs_t
- Fix virt_sigkill() interface
- Add additional fixes for mock. Mainly caused by mount running in mock_t
- Allow mock to write sysfs_t and mount pid files
- Add mailman_domain to mailman_template()
- Allow openvswitch to execute shell
- Allow qpidd to use kerberos
- Allow mailman to use fusefs, needs back port to RHEL6
- Allow apache and its scripts to use anon_inodefs
- Add alias for git_user_content_t and git_sys_content_t so that RHEL6 will update to RHEL7
- Realmd needs to connect to samba ports, needs back port to F18 also
- Allow colord to read /run/initial-setup-
- Allow sanlock-helper to send sigkill to virtd which is registred to sanlock
- Add virt_kill() interface
- Add rgmanager_search_lib() interface
- Allow wdmd to getattr on all filesystems. Back ported from RHEL6

* Tue Apr 2 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-25
- Allow realmd to create tmp files
- FIx ircssi_home_t type to irssi_home_t
- Allow adcli running as realmd_t to connect to ldap port
- Allow NetworkManager to transition to ipsec_t, for running strongswan
- Make openshift_initrc_t an lxc_domain
- Allow gssd to manage user_tmp_t files
- Fix handling of irclogs in users homedir
- Fix labeling for drupal an wp-content in subdirs of /var/www/html
- Allow abrt to read utmp_t file
- Fix openshift policy to transition lnk_file, sock-file an fifo_file when created in a tmpfs_t, needs back port to RHEL6
- fix labeling for (oo|rhc)-restorer-wrapper.sh
- firewalld needs to be able to write to network sysctls
- Fix mozilla_plugin_dontaudit_rw_sem() interface
- Dontaudit generic ipc read/write to a mozilla_plugin for sandbox_x domains
- Add mozilla_plugin_dontaudit_rw_sem() interface
- Allow svirt_lxc_t to transition to openshift domains
- Allow condor domains block_suspend and dac_override caps
- Allow condor_master to read passd
- Allow condor_master to read system state
- Allow NetworkManager to transition to ipsec_t, for running strongswan
- Lots of access required by lvm_t to created encrypted usb device
- Allow xdm_t to dbus communicate with systemd_localed_t
- Label strongswan content as ipsec_exec_mgmt_t for now
- Allow users to dbus chat with systemd_localed
- Fix handling of .xsession-errors in xserver.if, so kde will work
- Might be a bug but we are seeing avc's about people status on init_t:service
- Make sure we label content under /var/run/lock as <<none>>
- Allow daemon and systemprocesses to search init_var_run_t directory
- Add boolean to allow xdm to write xauth data to the home directory
- Allow mount to write keys for the unconfined domain
- Add unconfined_write_keys() interface

* Tue Mar 26 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-24
- Add labeling for /usr/share/pki
- Allow programs that read var_run_t symlinks also read var_t symlinks
- Add additional ports as mongod_port_t for  27018, 27019, 28017, 28018 and 28019 ports
- Fix labeling for /etc/dhcp directory
- add missing systemd_stub_unit_file() interface
- Add files_stub_var() interface
- Add lables for cert_t directories
- Make localectl set-x11-keymap working at all
- Allow abrt to manage mock build environments to catch build problems.
- Allow virt_domains to setsched for running gdb on itself
- Allow thumb_t to execute user home content
- Allow pulseaudio running as mozilla_plugin_t to read /run/systemd/users/1000
- Allow certwatch to execut /usr/bin/httpd
- Allow cgred to send signal perms to itself, needs back port to RHEL6
- Allow openshift_cron_t to look at quota
- Allow cups_t to read inhered tmpfs_t from the kernel
- Allow yppasswdd to use NIS
- Tuned wants sys_rawio capability
- Add ftpd_use_fusefs boolean
- Allow dirsrvadmin_t to signal itself

* Wed Mar 20 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-23
- Allow localectl to read /etc/X11/xorg.conf.d directory
- Revert "Revert "Fix filetrans rules for kdm creates .xsession-errors""
- Allow mount to transition to systemd_passwd_agent
- Make sure abrt directories are labeled correctly
- Allow commands that are going to read mount pid files to search mount_var_run_t
- label /usr/bin/repoquery as rpm_exec_t
- Allow automount to block suspend
- Add abrt_filetrans_named_content so that abrt directories get labeled correctly
- Allow virt domains to setrlimit and read file_context

* Mon Mar 18 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-22
- Allow nagios to manage nagios spool files
- /var/spool/snmptt is a directory which snmdp needs to write to, needs back port to RHEL6
- Add swift_alias.* policy files which contain typealiases for swift types
- Add support for /run/lock/opencryptoki
- Allow pkcsslotd chown capability
- Allow pkcsslotd to read passwd
- Add rsync_stub() interface
- Allow systemd_timedate also manage gnome config homedirs
- Label /usr/lib64/security/pam_krb5/pam_krb5_cchelper as bin_t
- Fix filetrans rules for kdm creates .xsession-errors
- Allow sytemd_tmpfiles to create wtmp file
- Really should not label content  under /var/lock, since it could have labels on it different from var_lock_t
- Allow systemd to list all file system directories
- Add some basic stub interfaces which will be used in PRODUCT policies

* Wed Mar 13 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-21
- Fix log transition rule for cluster domains
- Start to group all cluster log together
- Dont use filename transition for POkemon Advanced Adventure until a new checkpolicy update
- cups uses usbtty_device_t devices
- These fixes were all required to build a MLS virtual Machine with single level desktops
- Allow domains to transiton using httpd_exec_t
- Allow svirt domains to manage kernel key rings
- Allow setroubleshoot to execute ldconfig
- Allow firewalld to read generate gnome data
- Allow bluetooth to read machine-info
- Allow boinc domain to send signal to itself
- Fix gnome_filetrans_home_content() interface
- Allow mozilla_plugins to list apache modules, for use with gxine
- Fix labels for POkemon in the users homedir
- Allow xguest to read mdstat
- Dontaudit virt_domains getattr on /dev/*
- These fixes were all required to build a MLS virtual Machine with single level desktops
- Need to back port this to RHEL6 for openshift
- Add tcp/8891 as milter port
- Allow nsswitch domains to read sssd_var_lib_t files
- Allow ping to read network state.
- Fix typo
- Add labels to /etc/X11/xorg.d and allow systemd-timestampd_t to manage them

* Fri Mar 8 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-20
- Adopt swift changes from lhh@redhat.com
- Add rhcs_manage_cluster_pid_files() interface
- Allow screen domains to configure tty and setup sock_file in ~/.screen directory
- ALlow setroubleshoot to read default_context_t, needed to backport to F18
- Label /etc/owncloud as being an apache writable directory
- Allow sshd to stream connect to an lxc domain

* Thu Mar 7 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-19
- Allow postgresql to manage rgmanager pid files
- Allow postgresql to read ccs data
- Allow systemd_domain to send dbus messages to policykit
- Add labels for /etc/hostname and /etc/machine-info and allow systemd-hostnamed to create them
- All systemd domains that create content are reading the file_context file and setfscreate
- Systemd domains need to search through init_var_run_t
- Allow sshd to communicate with libvirt to set containers labels
- Add interface to manage pid files
- Allow NetworkManger_t to read /etc/hostname
- Dontaudit leaked locked files into openshift_domains
- Add fixes for oo-cgroup-read - it nows creates tmp files
- Allow gluster to manage all directories as well as files
- Dontaudit chrome_sandbox_nacl_t using user terminals
- Allow sysstat to manage its own log files
- Allow virtual machines to setrlimit and send itself signals.
- Add labeling for /var/run/hplip

* Mon Mar 4 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-18
- Fix POSTIN scriptlet

* Fri Mar 1 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-17
- Merge rgmanger, corosync,pacemaker,aisexec policies to cluster_t in rhcs.pp

* Wed Feb 27 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-16
- Fix authconfig.py labeling
- Make any domains that write homedir content do it correctly
- Allow glusterd to read/write anyhwere on the file system by default
- Be a little more liberal with the rsync log files
- Fix iscsi_admin interface
- Allow iscsid_t to read /dev/urand
- Fix up iscsi domain for use with unit files
- Add filename transition support for spamassassin policy
- Allow web plugins to use badly formated libraries
- Allow nmbd_t to create samba_var_t directories
- Add filename transition support for spamassassin policy
- Add filename transition support for tvtime
- Fix alsa_home_filetrans_alsa_home() interface
- Move all userdom_filetrans_home_content() calling out of booleans
- Allow logrotote to getattr on all file sytems
- Remove duplicate userdom_filetrans_home_content() calling
- Allow kadmind to read /etc/passwd
- Dontaudit append .xsession-errors file on ecryptfs for  policykit-auth
- Allow antivirus domain to manage antivirus db links
- Allow logrotate to read /sys
- Allow mandb to setattr on man dirs
- Remove mozilla_plugin_enable_homedirs boolean
- Fix ftp_home_dir boolean
- homedir mozilla filetrans has been moved to userdom_home_manager
- homedir telepathy filetrans has been moved to userdom_home_manager
- Remove gnome_home_dir_filetrans() from gnome_role_gkeyringd()
- Might want to eventually write a daemon on fusefsd.
- Add policy fixes for sshd [net] child from plautrba@redhat.com
- Tor uses a new port
- Remove bin_t for authconfig.py
- Fix so only one call to userdom_home_file_trans
- Allow home_manager_types to create content with the correctl label
- Fix all domains that write data into the homedir to do it with the correct label
- Change the postgresql to use proper boolean names, which is causing httpd_t to
- not get access to postgresql_var_run_t
- Hostname needs to send syslog messages
- Localectl needs to be able to send dbus signals to users
- Make sure userdom_filetrans_type will create files/dirs with user_home_t labeling by default
- Allow user_home_manger domains to create spam* homedir content with correct labeling
- Allow user_home_manger domains to create HOMEDIR/.tvtime with correct labeling
- Add missing miscfiles_setattr_man_pages() interface and for now comment some rules for userdom_filetrans_type to make build process working
- Declare userdom_filetrans_type attribute
- userdom_manage_home_role() needs to be called withoout usertype attribute because of userdom_filetrans_type attribute
- fusefsd is mounding a fuse file system on /run/user/UID/gvfs

* Thu Feb 21 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-15
- Man pages are now generated in the build process
- Allow cgred to list inotifyfs filesystem

* Wed Feb 20 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-14
- Allow gluster to get attrs on all fs
- New access required for virt-sandbox
- Allow dnsmasq to execute bin_t
- Allow dnsmasq to create content in /var/run/NetworkManager
- Fix openshift_initrc_signal() interface
- Dontaudit openshift domains doing getattr on other domains
- Allow consolehelper domain to communicate with session bus
- Mock should not be transitioning to any other domains,  we should keep mock_t as mock_t
- Update virt_qemu_ga_t policy
- Allow authconfig running from realmd to restart oddjob service
- Add systemd support for oddjob
- Add initial policy for realmd_consolehelper_t which if for authconfig executed by realmd
- Add labeling for gnashpluginrc
- Allow chrome_nacl to execute /dev/zero
- Allow condor domains to read /proc
- mozilla_plugin_t will getattr on /core if firefox crashes
- Allow condor domains to read /etc/passwd
- Allow dnsmasq to execute shell scripts, openstack requires this access
- Fix glusterd labeling
- Allow virtd_t to interact with the socket type
- Allow nmbd_t to override dac if you turned on sharing all files
- Allow tuned to created kobject_uevent socket
- Allow guest user to run fusermount
- Allow openshift to read /proc and locale
- Allow realmd to dbus chat with rpm
- Add new interface for virt
- Remove depracated interfaces
- Allow systemd_domains read access on etc, etc_runtime and usr files, also allow them to connect stream to syslog socket
- /usr/share/munin/plugins/plugin.sh should be labeled as bin_t
- Remove some more unconfined_t process transitions, that I don't believe are necessary
- Stop transitioning uncofnined_t to checkpc
- dmraid creates /var/lock/dmraid
- Allow systemd_localed to creatre unix_dgram_sockets
- Allow systemd_localed to write kernel messages.
- Also cleanup systemd definition a little.
- Fix userdom_restricted_xwindows_user_template() interface
- Label any block devices or char devices under /dev/infiniband as fixed_disk_device_t
- User accounts need to dbus chat with accountsd daemon
- Gnome requires all users to be able to read /proc/1/

* Thu Feb 14 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-13
- virsh now does a setexeccon call
- Additional rules required by openshift domains
- Allow svirt_lxc_domains to use inherited terminals, needed to make virt-sandbox-service execute work
- Allow spamd_update_t to search spamc_home_t
- Avcs discovered by mounting an isci device under /mnt
- Allow lspci running as logrotate to read pci.ids
- Additional fix for networkmanager_read_pid_files()
- Fix networkmanager_read_pid_files() interface
- Allow all svirt domains to connect to svirt_socket_t
- Allow virsh to set SELinux context for a process.
- Allow tuned to create netlink_kobject_uevent_socket
- Allow systemd-timestamp to set SELinux context
- Add support for /var/lib/systemd/linger
- Fix ssh_sysadm_login to be working on MLS as expected

* Mon Feb 11 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-12
- Rename files_rw_inherited_tmp_files to files_rw_inherited_tmp_file
- Add missing files_rw_inherited_tmp_files interface
- Add additional interface for ecryptfs
- ALlow nova-cert to connect to postgresql
- Allow keystone to connect to postgresql
- Allow all cups domains to getattr on filesystems
- Allow pppd to send signull
- Allow tuned to execute ldconfig
- Allow gpg to read fips_enabled
- Add additional fixes for ecryptfs
- Allow httpd to work with posgresql
- Allow keystone getsched and setsched

* Fri Feb 8 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-11
- Allow gpg to read fips_enabled
- Add support for /var/cache/realmd
- Add support for /usr/sbin/blazer_usb and systemd support for nut
- Add labeling for fenced_sanlock and allow sanclok transition to fenced_t
- bitlbee wants to read own log file
- Allow glance domain to send a signal itself
- Allow xend_t to request that the kernel load a kernel module
- Allow pacemaker to execute heartbeat lib files
- cleanup new swift policy

* Tue Feb 5 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-10
- Fix smartmontools
- Fix userdom_restricted_xwindows_user_template() interface
- Add xserver_xdm_ioctl_log() interface
- Allow Xusers to ioctl lxdm.log to make lxdm working
- Add MLS fixes to make MLS boot/log-in working
- Add mls_socket_write_all_levels() also for syslogd
- fsck.xfs needs to read passwd
- Fix ntp_filetrans_named_content calling in init.te
- Allow postgresql to create pg_log dir
- Allow sshd to read rsync_data_t to make rsync <backuphost> working
- Change ntp.conf to be labeled net_conf_t
- Allow useradd to create homedirs in /run.  ircd-ratbox does this and we should just allow it
- Allow xdm_t to execute gstreamer home content
- Allod initrc_t and unconfined domains, and sysadm_t to manage ntp
- New policy for openstack swift domains
- More access required for openshift_cron_t
- Use cupsd_log_t instead of cupsd_var_log_t
- rpm_script_roles should be used in rpm_run
- Fix rpm_run() interface
- Fix openshift_initrc_run()
- Fix sssd_dontaudit_stream_connect() interface
- Fix sssd_dontaudit_stream_connect() interface
- Allow LDA's job to deliver mail to the mailbox
- dontaudit block_suspend for mozilla_plugin_t
- Allow l2tpd_t to all signal perms
- Allow uuidgen to read /dev/random
- Allow mozilla-plugin-config to read power_supply info
- Implement cups_domain attribute for cups domains
- We now need access to user terminals since we start by executing a command outside the tty
- We now need access to user terminals since we start by executing a command outside the tty
- svirt lxc containers want to execute userhelper apps, need these changes to allow this to happen
- Add containment of openshift cron jobs
- Allow system cron jobs to create tmp directories
- Make userhelp_conf_t a config file
- Change rpm to use rpm_script_roles
- More fixes for rsync to make rsync <backuphost> wokring
- Allow logwatch to domtrans to mdadm
- Allow pacemaker to domtrans to ifconfig
- Allow pacemaker to setattr on corosync.log
- Add pacemaker_use_execmem for memcheck-amd64 command
- Allow block_suspend capability
- Allow create fifo_file in /tmp with pacemaker_tmp_t
- Allow systat to getattr on fixed disk
- Relabel /etc/ntp.conf to be net_conf_t
- ntp_admin should create files in /etc with the correct label
- Add interface to create ntp_conf_t files in /etc
- Add additional labeling for quantum
- Allow quantum to execute dnsmasq with transition

* Wed Jan 30 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-9
- boinc_cliean wants also execmem as boinc projecs have
- Allow sa-update to search admin home for /root/.spamassassin
- Allow sa-update to search admin home for /root/.spamassassin
- Allow antivirus domain to read net sysctl
- Dontaudit attempts from thumb_t to connect to ssd
- Dontaudit attempts by readahead to read sock_files
- Dontaudit attempts by readahead to read sock_files
- Create tmpfs file while running as wine as user_tmpfs_t
- Dontaudit attempts by readahead to read sock_files
- libmpg ships badly created librarie

* Mon Jan 28 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-8
- Change ssh_use_pts to use macro and only inherited sshd_devpts_t
- Allow confined users to read systemd_logind seat information
- libmpg ships badly created libraries
- Add support for strongswan.service
- Add labeling for strongswan
- Allow l2tpd_t to read network manager content in /run directory
- Allow rsync to getattr any file in rsync_data_t
- Add labeling and filename transition for .grl-podcasts

* Fri Jan 25 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-7
- mount.glusterfs executes glusterfsd binary
- Allow systemd_hostnamed_t to stream connect to systemd
- Dontaudit any user doing a access check
- Allow obex-data-server to request the kernel to load a module
- Allow gpg-agent to manage gnome content (~/.cache/gpg-agent-info)
- Allow gpg-agent to read /proc/sys/crypto/fips_enabled
- Add new types for antivirus.pp policy module
- Allow gnomesystemmm_t caps because of ioprio_set
- Make sure if mozilla_plugin creates files while in permissive mode, they get created with the correct label, user_home_t
- Allow gnomesystemmm_t caps because of ioprio_set
- Allow NM rawip socket
- files_relabel_non_security_files can not be used with boolean
- Add interface to thumb_t dbus_chat to allow it to read remote process state
- ALlow logrotate to domtrans to mdadm_t
- kde gnomeclock wants to write content to /tmp

* Wed Jan 23 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-6
- kde gnomeclock wants to write content to /tmp
- /usr/libexec/kde4/kcmdatetimehelper attempts to create /root/.kde
- Allow blueman_t to rwx zero_device_t, for some kind of jre
- Allow mozilla_plugin_t to rwx zero_device_t, for some kind of jre
- Ftp full access should be allowed to create directories as well as files
- Add boolean to allow rsync_full_acces, so that an rsync server can write all
- over the local machine
- logrotate needs to rotate logs in openshift directories, needs back port to RHEL6
- Add missing vpnc_roles type line
- Allow stapserver to write content in /tmp
- Allow gnome keyring to create keyrings dir in ~/.local/share
- Dontaudit thumb drives trying to bind to udp sockets if nis_enabled is turned on
- Add interface to colord_t dbus_chat to allow it to read remote process state
- Allow colord_t to read cupsd_t state
- Add mate-thumbnail-font as thumnailer
- Allow sectoolm to sys_ptrace since it is looking at other proceses /proc data.
- Allow qpidd to list /tmp. Needed by ssl
- Only allow init_t to transition to rsync_t domain, not initrc_t.  This should be back ported to F17, F18
- - Added systemd support for ksmtuned
- Added booleans
 	ksmtuned_use_nfs
 	ksmtuned_use_cifs
- firewalld seems to be creating mmap files which it needs to execute in /run /tmp and /dev/shm.  Would like to clean this up but for now we will allow
- Looks like qpidd_t needs to read /dev/random
- Lots of probing avc's caused by execugting gpg from staff_t
- Dontaudit senmail triggering a net_admin avc
- Change thumb_role to use thumb_run, not sure why we have a thumb_role, needs back port
- Logwatch does access check on mdadm binary
- Add raid_access_check_mdadm() iterface

* Wed Jan 16 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-5
- Fix systemd_manage_unit_symlinks() interface
- Call systemd_manage_unit_symlinks(() which is correct interface
- Add filename transition for opasswd
- Switch gnomeclock_dbus_chat to systemd_dbus_chat_timedated since we have switched the name of gnomeclock
- Allow sytstemd-timedated to get status of init_t
- Add new systemd policies for hostnamed and rename gnomeclock_t to systemd_timedate_t
- colord needs to communicate with systemd and systemd_logind, also remove duplicate rules
- Switch gnomeclock_dbus_chat to systemd_dbus_chat_timedated since we have switched the name of gnomeclock
- Allow gpg_t to manage all gnome files
- Stop using pcscd_read_pub_files
- New rules for xguest, dontaudit attempts to dbus chat
- Allow firewalld to create its mmap files in tmpfs and tmp directories
- Allow firewalld to create its mmap files in tmpfs and tmp directories
- run unbound-chkconf as named_t, so it can read dnssec
- Colord is reading xdm process state, probably reads state of any apps that sends dbus message
- Allow mdadm_t to change the kernel scheduler
- mythtv policy
- Update mandb_admin() interface
- Allow dsspam to listen on own tpc_socket
- seutil_filetrans_named_content needs to be optional
- Allow sysadm_t to execute content in his homedir
- Add attach_queue to tun_socket, new patch from Paul Moore
- Change most of selinux configuration types to security_file_type.
- Add filename transition rules for selinux configuration
- ssh into a box with -X -Y requires ssh_use_ptys
- Dontaudit thumb drives trying to bind to udp sockets if nis_enabled is turned on
- Allow all unpriv userdomains to send dbus messages to hostnamed and timedated
- New allow rules found by Tom London for systemd_hostnamed

* Mon Jan 14 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-4
- Allow systemd-tmpfiles to relabel lpd spool files
- Ad labeling for texlive bash scripts
- Add xserver_filetrans_fonts_cache_home_content() interface
- Remove duplicate rules from *.te
- Add support for /var/lock/man-db.lock
- Add support for /var/tmp/abrt(/.*)?
- Add additional labeling for munin cgi scripts
- Allow httpd_t to read munin conf files
- Allow certwatch to read meminfo
- Fix nscd_dontaudit_write_sock_file() interfac
- Fix gnome_filetrans_home_content() to include also "fontconfig" dir as cache_home_t
- llow mozilla_plugin_t to create HOMEDIR/.fontconfig with the proper labeling 

* Fri Jan 11 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-3
- Allow gnomeclock to talk to puppet over dbus
- Allow numad access discovered by Dominic
- Add support for HOME_DIR/.maildir
- Fix attribute_role for mozilla_plugin_t domain to allow staff_r to access this domain
- Allow udev to relabel udev_var_run_t lnk_files
- New bin_t file in mcelog

* Thu Jan 10 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-2
- Remove all mcs overrides and replace with t1 != mcs_constrained_types
- Add attribute_role for iptables
- mcs_process_set_categories needs to be called for type
- Implement additional role_attribute statements
- Sodo domain is attempting to get the additributes of proc_kcore_t
- Unbound uses port 8953
- Allow svirt_t images to compromise_kernel when using pci-passthrough
- Add label for dns lib files
- Bluetooth aquires a dbus name
- Remove redundant files_read_usr_file calling
- Remove redundant files_read_etc_file calling
- Fix mozilla_run_plugin()
- Add role_attribute support for more domains

* Wed Jan 9 2013 Miroslav Grepl <mgrepl@redhat.com> 3.12.1-1
- Mass merge with upstream

* Sat Jan 5 2013 Dan Walsh <dwalsh@redhat.com> 3.11.1-69.1
- Bump the policy version to 28 to match selinux userspace
- Rebuild versus latest libsepol

* Wed Jan 2 2013 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-69
- Add systemd_status_all_unit_files() interface
- Add support for nshadow
- Allow sysadm_t to administrate the postfix domains
- Add interface to setattr on isid directories for use by tmpreaper
- Allow sshd_t sys_admin for use with afs logins
- Allow systemd to read/write all sysctls
- Allow sshd_t sys_admin for use with afs logins
- Allow systemd to read/write all sysctls
- Add systemd_status_all_unit_files() interface
- Add support for nshadow
- Allow sysadm_t to administrate the postfix domains
- Add interface to setattr on isid directories for use by tmpreaper
- Allow sshd_t sys_admin for use with afs logins
- Allow systemd to read/write all sysctls
- Allow sshd_t sys_admin for use with afs logins
- Add labeling for /var/named/chroot/etc/localtim

* Thu Dec 27 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-68
- Allow setroubleshoot_fixit to execute rpm
- zoneminder needs to connect to httpd ports where remote cameras are listening
- Allow firewalld to execute content created in /run directory
- Allow svirt_t to read generic certs
- Dontaudit leaked ps content to mozilla plugin
- Allow sshd_t sys_admin for use with afs logins
- Allow systemd to read/write all sysctls
- init scripts are creating systemd_unit_file_t directories

* Fri Dec 21 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-67
- systemd_logind_t is looking at all files under /run/user/apache
- Allow systemd to manage all user tmp files
- Add labeling for /var/named/chroot/etc/localtime
- Allow netlabel_peer_t type to flow over netif_t and node_t, and only be hindered by MLS, need back port to RHEL6
- Keystone is now using a differnt port
- Allow xdm_t to use usbmuxd daemon to control sound
- Allow passwd daemon to execute gnome_exec_keyringd
- Fix chrome_sandbox policy
- Add labeling for /var/run/checkquorum-timer
- More fixes for the dspam domain, needs back port to RHEL6
- More fixes for the dspam domain, needs back port to RHEL6
- sssd needs to connect to kerberos password port if a user changes his password
- Lots of fixes from RHEL testing of dspam web
- Allow chrome and mozilla_plugin to create msgq and semaphores
- Fixes for dspam cgi scripts
- Fixes for dspam cgi scripts
- Allow confine users to ptrace screen
- Backport virt_qemu_ga_t changes from RHEL
- Fix labeling for dspam.cgi needed for RHEL6
- We need to back port this policy to RHEL6, for lxc domains
- Dontaudit attempts to set sys_resource of logrotate
- Allow corosync to read/write wdmd's tmpfs files
- I see a ptrace of mozilla_plugin_t by staff_t, will allow without deny_ptrace being set
- Allow cron jobs to read bind config for unbound
- libvirt needs to inhibit systemd
- kdumpctl needs to delete boot_t files
- Fix duplicate gnome_config_filetrans
- virtd_lxc_t is using /dev/fuse
- Passenger needs to create a directory in /var/log, needs a backport to RHEL6 for openshift
- apcupsd can be setup to listen to snmp trafic
- Allow transition from kdumpgui to kdumpctl
- Add fixes for munin CGI scripts
- Allow deltacloud to connect to openstack at the keystone port
- Allow domains that transition to svirt domains to be able to signal them
- Fix file context of gstreamer in .cache directory
- libvirt is communicating with logind
- NetworkManager writes to the systemd inhibit pipe

* Mon Dec 17 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-66
- Allow munin disk plugins to get attributes of all directories
- Allow munin disk plugins to get attributes of all directorie
- Allow logwatch to get attributes of all directories
- Fix networkmanager_manage_lib() interface
- Fix gnome_manage_config() to allow to manage sock_file
- Fix virtual_domain_context
- Add support for dynamic DNS for DHCPv6

* Sat Dec 15 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-65
- Allow svirt to use netlink_route_socket which was a part of auth_use_nsswitch
- Add additional labeling for /var/www/openshift/broker
- Fix rhev policy
- Allow openshift_initrc domain to dbus chat with systemd_logind
- Allow httpd to getattr passenger log file if run_stickshift
- Allow consolehelper-gtk to connect to xserver
- Add labeling for the tmp-inst directory defined in pam_namespace.conf
- Add lvm_metadata_t labeling for /etc/multipath

* Fri Dec 14 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-64
- consoletype is no longer used

* Wed Dec 12 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-63
- Add label for efivarfs
- Allow certmonger to send signal to itself
- Allow plugin-config to read own process status
- Add more fixes for pacemaker
- apache/drupal can run clamscan on uploaded content
- Allow chrome_sandbox_nacl_t to read pid 1 content

* Tue Dec 11 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-62
- Fix MCS Constraints to control ingres and egres controls on the network.
- Change name of svirt_nokvm_t to svirt_tcg_t
- Allow tuned to request the kernel to load kernel modules

* Mon Dec 10 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-61
- Label /var/lib/pgsql/.ssh as ssh_home_t
- Add labeling for /usr/bin/pg_ctl
- Allow systemd-logind to manage keyring user tmp dirs
- Add support for 7389/tcp port
- gems seems to be placed in lots of places
- Since xdm is running a full session, it seems to be trying to execute lots of executables via dbus
- Add back tcp/8123 port as http_cache port
- Add ovirt-guest-agent\.pid labeling
- Allow xend to run scsi_id
- Allow rhsmcertd-worker to read "physical_package_id"
- Allow pki_tomcat to connect to ldap port
- Allow lpr to read /usr/share/fonts
- Allow open file from CD/DVD drive on domU
- Allow munin services plugins to talk to SSSD
- Allow all samba domains to create samba directory in var_t directories
- Take away svirt_t ability to use nsswitch
- Dontaudit attempts by openshift to read apache logs
- Allow apache to create as well as append _ra_content_t
- Dontaudit sendmail_t reading a leaked file descriptor
- Add interface to have admin transition /etc/prelink.cache to the proper label
- Add sntp support to ntp policy
- Allow firewalld to dbus chat with devicekit_power
- Allow tuned to call lsblk
- Allow tor to read /proc/sys/kernel/random/uuid
- Add tor_can_network_relay boolean  

* Wed Dec 5 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-60
- Add openshift_initrc_signal() interface
- Fix typos
- dspam port is treat as spamd_port_t
- Allow setroubleshoot to getattr on all executables
- Allow tuned to execute profiles scripts in /etc/tuned
- Allow apache to create directories to store its log files
- Allow all directories/files in /var/log starting with passenger to be labeled passenger_log_t
- Looks like apache is sending sinal to openshift_initrc_t now,needs back port to RHEL6
- Allow Postfix to be configured to listen on TCP port 10026 for email from DSPAM
- Add filename transition for /etc/tuned/active_profile
- Allow condor_master to send mails
- Allow condor_master to read submit.cf
- Allow condor_master to create /tmp files/dirs
- Allow condor_mater to send sigkill to other condor domains
- Allow condor_procd sigkill capability
- tuned-adm wants to talk with tuned daemon
- Allow kadmind and krb5kdc to also list sssd_public_t
- Allow accountsd to dbus chat with init
- Fix git_read_generic_system_content_files() interface
- pppd wants sys_nice by nmcli because of "syscall=sched_setscheduler"
- Fix mozilla_plugin_can_network_connect to allow to connect to all ports
- Label all munin plugins which are not covered by munin plugins policy  as unconfined_munin_plugin_exec_t
- dspam wants to search /var/spool for opendkim data
- Revert "Add support for tcp/10026 port as dspam_port_t"
- Turning on labeled networking requires additional access for netlabel_peer_t; these allow rules need to be back ported to RHEL6
- Allow all application domains to use fifo_files passed in from userdomains, also allow them to write to tmp_files inherited from userdomain
- Allow systemd_tmpfiles_t to setattr on mandb_cache_t

* Sat Dec 1 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-59
- consolekit.pp was not removed from the postinstall script

* Fri Nov 30 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-58
- Add back consolekit policy
- Silence bootloader trying to use inherited tty
- Silence xdm_dbusd_t trying to execute telepathy apps
- Fix shutdown avcs when machine has unconfined.pp disabled
- The host and a virtual machine can share the same printer on a usb device
- Change oddjob to transition to a ranged openshift_initr_exec_t when run from oddjob
- Allow abrt_watch_log_t to execute bin_t
- Allow chrome sandbox to write content in ~/.config/chromium
- Dontaudit setattr on fontconfig dir for thumb_t
- Allow lircd to request the kernel to load module
- Make rsync as userdom_home_manager
- Allow rsync to search automount filesystem
- Add fixes for pacemaker

* Wed Nov 28 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-57
- Add support for 4567/tcp port
- Random fixes from Tuomo Soini
- xdm wants to get init status
- Allow programs to run in fips_mode
- Add interface to allow the reading of all blk device nodes
- Allow init to relabel rpcbind sock_file
- Fix labeling for lastlog and faillog related to logrotate
- ALlow aeolus_configserver to use TRAM port
- Add fixes for aeolus_configserver
- Allow snmpd to connect to snmp port
- Allow spamd_update to create spamd_var_lib_t directories
- Allow domains that can read sssd_public_t files to also list the directory
- Remove miscfiles_read_localization, this is defined for all domains

* Mon Nov 26 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-56
- Allow syslogd to request the kernel to load a module
- Allow syslogd_t to read the network state information
- Allow xdm_dbusd_t connect to the system DBUS
- Add support for 7389/tcp port
- Allow domains to read/write all inherited sockets
- Allow staff_t to read kmsg
- Add awstats_purge_apache_log boolean
- Allow ksysguardproces to read /.config/Trolltech.conf
- Allow passenger to create and append puppet log files
- Add puppet_append_log and puppet_create_log interfaces
- Add puppet_manage_log() interface
- Allow tomcat domain to search tomcat_var_lib_t
- Allow pki_tomcat_t to connect to pki_ca ports
- Allow pegasus_t to have net_admin capability
- Allow pegasus_t to write /sys/class/net/<interface>/flags
- Allow mailserver_delivery to manage mail_home_rw_t lnk_files
- Allow fetchmail to create log files
- Allow gnomeclock to manage home config in .kde
- Allow bittlebee to read kernel sysctls
- Allow logrotate to list /root

* Mon Nov 19 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-55
- Fix userhelper_console_role_template()
- Allow enabling Network Access Point service using blueman
- Make vmware_host_t as unconfined domain
- Allow authenticate users in webaccess via squid, using mysql as backend
- Allow gathers to get various metrics on mounted file systems
- Allow firewalld to read /etc/hosts
- Fix cron_admin_role() to make sysadm cronjobs running in the sysadm_t instead of cronjob_t
- Allow kdumpgui to read/write to zipl.conf
- Commands needed to get mock to build from staff_t in enforcing mode
- Allow mdadm_t to manage cgroup files
- Allow all daemons and systemprocesses to use inherited initrc_tmp_t files
- dontaudit ifconfig_t looking at fifo_files that are leaked to it
- Add lableing for Quest Authentication System

* Thu Nov 15 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-54
- Fix filetrans interface definitions
- Dontaudit xdm_t to getattr on BOINC lib files
- Add systemd_reload_all_services() interface
- Dontaudit write access on /var/lib/net-snmp/mib_indexes 
- Only stop mcsuntrustedproc from relableing files
- Allow accountsd to dbus chat with gdm
- Allow realmd to getattr on all fs
- Allow logrotate to reload all services
- Add systemd unit file for radiusd
- Allow winbind to create samba pid dir
- Add labeling for /var/nmbd/unexpected
- Allow chrome and mozilla plugin to connect to msnp ports

* Mon Nov 12 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-53
- Fix storage_rw_inherited_fixed_disk_dev() to cover also blk_file
- Dontaudit setfiles reading /dev/random
- On initial boot gnomeclock is going to need to be set buy gdm
- Fix tftp_read_content() interface
- Random apps looking at kernel file systems
- Testing virt with lxc requiers additional access for virsh_t
- New allow rules requied for latest libvirt, libvirt talks directly to journald,lxc setup tool needs compromize_kernel,and we need ipc_lock in the container
- Allow MPD to read /dev/radnom
- Allow sandbox_web_type to read logind files which needs to read pulseaudio
- Allow mozilla plugins to read /dev/hpet
- Add labeling for /var/lib/zarafa-webap
- Allow BOINC client to use an HTTP proxy for all connections
- Allow rhsmertd to domain transition to dmidecod
-  Allow setroubleshootd to send D-Bus msg to ABRT

* Thu Nov 8 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-52
- Define usbtty_device_t as a term_tty
- Allow svnserve to accept a connection
- Allow xend manage default virt_image_t type
- Allow prelink_cron_system_t to overide user componant when executing cp
- Add labeling for z-push
- Gnomeclock sets the realtime clock
- Openshift seems to be storing apache logs in /var/lib/openshift/.log/httpd
- Allow lxc domains to use /dev/random and /dev/urandom

* Wed Nov 7 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-51
- Add port defintion for tcp/9000
- Fix labeling for /usr/share/cluster/checkquorum to label also checkquorum.wdmd
- Add rules and labeling for $HOME/cache/\.gstreamer-.* directory
- Add support for CIM provider openlmi-networking which uses NetworkManager dbus API
- Allow shorewall_t to create netlink_socket
- Allow krb5admind to block suspend
- Fix labels on /var/run/dlm_controld /var/log/dlm_controld
- Allow krb5kdc to block suspend
- gnomessytemmm_t needs to read /etc/passwd
- Allow cgred to read all sysctls

* Tue Nov 6 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-50
- Allow all domains to read /proc/sys/vm/overcommit_memory
- Make proc_numa_t an MLS Trusted Object
- Add /proc/numactl support for confined users
- Allow ssh_t to connect to any port > 1023
- Add openvswitch domain
- Pulseaudio tries to create directories in gnome_home_t directories
- New ypbind pkg wants to search /var/run which is caused by sd_notify
- Allow NM to read certs on NFS/CIFS using use_nfs_*, use_samba_* booleans
- Allow sanlock to read /dev/random
- Treat php-fpm with httpd_t
- Allow domains that can read named_conf_t to be able to list the directories
- Allow winbind to create sock files in /var/run/samba

* Thu Nov 1 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-49
- Add smsd policy
- Add support for OpenShift sbin labelin
- Add boolean to allow virt to use rawip
- Allow mozilla_plugin to read all file systems with noxattrs support
- Allow kerberos to write on anon_inodefs fs
- Additional access required by fenced
- Add filename transitions for passwd.lock/group.lock
- UPdate man pages
- Create coolkey directory in /var/cache with the correct label

* Tue Oct 30 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-48
- Fix label on /etc/group.lock
- Allow gnomeclock to create lnk_file in /etc
- label /root/.pki as a home_cert_t
- Add interface to make sure rpcbind.sock is created with the correct label
- Add definition for new directory /var/lib/os-probe and bootloader wants to read udev rules
- opendkim should be a part of milter
- Allow libvirt to set the kernel sched algorythm
- Allow mongod to read sysfs_t
- Add authconfig policy
- Remove calls to miscfiles_read_localization all domains get this
- Allow virsh_t to read /root/.pki/ content
- Add label for log directory under /var/www/stickshift

* Mon Oct 29 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-47
- Allow getty to setattr on usb ttys
- Allow sshd to search all directories for sshd_home_t content
- Allow staff domains to send dbus messages to kdumpgui
- Fix labels on /etc/.pwd.lock and friends to be passwd_file_t
- Dontaudit setfiles reading urand
- Add files_dontaudit_list_tmp() for domains to which we added sys_nice/setsched
- Allow staff_gkeyringd_t to read /home/$USER/.local/share/keyrings dir
- Allow systemd-timedated to read /dev/urandom
- Allow entropyd_t to read proc_t (meminfo)
- Add unconfined munin plugin
- Fix networkmanager_read_conf() interface
- Allow blueman to list /tmp which is needed by sys_nic/setsched
- Fix label of /etc/mail/aliasesdb-stamp
- numad is searching cgroups
- realmd is communicating with networkmanager using dbus
- Lots of fixes to try to get kdump to work

* Fri Oct 26 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-46
- Allow loging programs to dbus chat with realmd
- Make apache_content_template calling as optional
- realmd is using policy kit

* Fri Oct 26 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-45
- Add new selinuxuser_use_ssh_chroot boolean
- dbus needs to be able to read/write inherited fixed disk device_t passed through it
- Cleanup netutils process allow rule
- Dontaudit leaked fifo files from openshift to ping
- sanlock needs to read mnt_t lnk files
- Fail2ban needs to setsched and sys_nice

* Wed Oct 24 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-44
- Change default label of all files in /var/run/rpcbind
- Allow sandbox domains (java) to read hugetlbfs_t
- Allow awstats cgi content to create tmp files and read apache log files
- Allow setuid/setgid for cupsd-config
- Allow setsched/sys_nice pro cupsd-config
-  Fix /etc/localtime sym link to be labeled locale_t
- Allow sshd to search postgresql db t since this is a homedir
- Allow xwindows users to chat with realmd
- Allow unconfined domains to configure all files and null_device_t service

* Tue Oct 23 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-43
- Adopt pki-selinux policy

* Mon Oct 22 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-42
- pki is leaking which we dontaudit until a pki code fix
- Allow setcap for arping
- Update man pages
- Add labeling for /usr/sbin/mcollectived
- pki fixes
- Allow smokeping to execute fping in the netutils_t domain

* Fri Oct 19 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-41
- Allow mount to relabelfrom unlabeled file systems
- systemd_logind wants to send and receive messages from devicekit disk over dbus to make connected mouse working
- Add label to get bin files under libreoffice labeled correctly
- Fix interface to allow executing of base_ro_file_type
- Add fixes for realmd
- Update pki policy
- Add tftp_homedir boolean
- Allow blueman sched_setscheduler
- openshift user domains wants to r/w ssh tcp sockets

* Wed Oct 17 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-40
- Additional requirements for disable unconfined module when booting
- Fix label of systemd script files
- semanage can use -F /dev/stdin to get input
- syslog now uses kerberos keytabs
- Allow xserver to compromise_kernel access
-  Allow nfsd to write to mount_var_run_t when running the mount command
- Add filename transition rule for bin_t directories
- Allow files to read usr_t lnk_files
- dhcpc wants chown
- Add support for new openshift labeling
- Clean up for tunable+optional statements
- Add labeling for /usr/sbin/mkhomedir_helper
- Allow antivirus domain to managa amavis spool files
- Allow rpcbind_t to read passwd 
- Allow pyzor running as spamc to manage amavis spool


* Tue Oct 16 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-39
- Add interfaces to read kernel_t proc info
- Missed this version of exec_all
- Allow anyone who can load a kernel module to compromise kernel
- Add oddjob_dbus_chat to openshift apache policy
- Allow chrome_sandbox_nacl_t to send signals to itself
- Add unit file support to usbmuxd_t
- Allow all openshift domains to read sysfs info
- Allow openshift domains to getattr on all domains

* Fri Oct 12 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-38
- MLS fixes from Dan
- Fix name of capability2 secure_firmware->compromise_kerne

* Thu Oct 11 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-37
- Allow xdm to search all file systems
- Add interface to allow the config of all files
- Add rngd policy
- Remove kgpg as a gpg_exec_t type
- Allow plymouthd to block suspend
- Allow systemd_dbus to config any file
- Allow system_dbus_t to configure all services
- Allow freshclam_t to read usr_files
- varnishd requires execmem to load modules

* Thu Oct 11 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-36
- Allow semanage to verify types
- Allow sudo domain to execute user home files
- Allow session_bus_type to transition to user_tmpfs_t
- Add dontaudit caused by yum updates
- Implement pki policy but not activated

* Wed Oct 10 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-35
- tuned wants to getattr on all filesystems
- tuned needs also setsched. The build is needed for test day

* Wed Oct 10 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-34
- Add policy for qemu-qa
- Allow razor to write own config files
-  Add an initial antivirus policy to collect all antivirus program
- Allow qdisk to read usr_t
- Add additional caps for vmware_host
- Allow tmpfiles_t to setattr on mandb_cache_t
- Dontaudit leaked files into mozilla_plugin_config_t
- Allow wdmd to getattr on tmpfs
- Allow realmd to use /dev/random
- allow containers to send audit messages
- Allow root mount any file via loop device with enforcing mls policy
- Allow tmpfiles_t to setattr on mandb_cache_t
- Allow tmpfiles_t to setattr on mandb_cache_t
- Make userdom_dontaudit_write_all_ not allow open
- Allow init scripts to read all unit files
- Add support for saphostctrl ports

* Mon Oct 8 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-33
- Add kernel_read_system_state to sandbox_client_t
- Add some of the missing access to kdumpgui
- Allow systemd_dbusd_t to status the init system
- Allow vmnet-natd to request the kernel to load a module
- Allow gsf-office-thum to append .cache/gdm/session.log
- realmd wants to read .config/dconf/user
- Firewalld wants sys_nice/setsched
- Allow tmpreaper to delete mandb cache files
- Firewalld wants sys_nice/setsched
- Allow firewalld to perform  a DNS name resolution
- Allown winbind to read /usr/share/samba/codepages/lowcase.dat
- Add support for HTTPProxy* in /etc/freshclam.conf
- Fix authlogin_yubike boolean
- Extend smbd_selinux man page to include samba booleans
- Allow dhcpc to execute consoletype
- Allow ping to use inherited tmp files created in init scripts
- On full relabel with unconfined domain disabled, initrc was running some chcon's
- Allow people who delete man pages to delete mandb cache files

* Thu Oct 4 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-32
- Add missing permissive domains

* Thu Oct 4 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-31
- Add new mandb policy
- ALlow systemd-tmpfiles_t to relabel mandb_cache_t
- Allow logrotate to start all unit files

* Thu Oct 4 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-30
- Add fixes for ctbd
- Allow nmbd to stream connect to ctbd
- Make cglear_t as nsswitch_domain
- Fix bogus in interfaces
- Allow openshift to read/write postfix public pipe
- Add postfix_manage_spool_maildrop_files() interface
- stickshift paths have been renamed to openshift
- gnome-settings-daemon wants to write to /run/systemd/inhibit/ pipes
- Update man pages, adding ENTRYPOINTS

* Tue Oct 2 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-29
-  Add mei_device_t
- Make sure gpg content in homedir created with correct label
- Allow dmesg to write to abrt cache files
- automount wants to search  virtual memory sysctls
- Add support for hplip logs stored in /var/log/hp/tmp
- Add labeling for /etc/owncloud/config.php
- Allow setroubleshoot to send analysys to syslogd-journal
- Allow virsh_t to interact with new fenced daemon
- Allow gpg to write to /etc/mail/spamassassiin directories
- Make dovecot_deliver_t a mail server delivery type
- Add label for /var/tmp/DNS25

* Thu Sep 27 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-28
- Fixes for tomcat_domain template interface

* Thu Sep 27 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-27
- Remove init_systemd and init_upstart boolean, Move init_daemon_domain and init_system_domain to use attributes
- Add attribute to all base os types.  Allow all domains to read all ro base OS types

* Wed Sep 26 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-26
- Additional unit files to be defined as power unit files
- Fix more boolean names

* Tue Sep 25 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-25
- Fix boolean name so subs will continue to work

* Tue Sep 25 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-24
- dbus needs to start getty unit files
- Add interface to allow system_dbusd_t to start the poweroff service
- xdm wants to exec telepathy apps
- Allow users to send messages to systemdlogind
- Additional rules needed for systemd and other boot apps
- systemd wants to list /home and /boot
- Allow gkeyringd to write dbus/conf file
- realmd needs to read /dev/urand
- Allow readahead to delete /.readahead if labeled root_t, might get created before policy is loaded

* Thu Sep 20 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-23
- Fixes to safe more rules
- Re-write tomcat_domain_template()
- Fix passenger labeling
- Allow all domains to read man pages
- Add ephemeral_port_t to the 'generic' port interfaces
- Fix the names of postgresql booleans

* Tue Sep 18 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-22
- Stop using attributes form netlabel_peer and syslog, auth_use_nsswitch setsup netlabel_peer
- Move netlable_peer check out of booleans
- Remove call to recvfrom_netlabel for kerberos call
- Remove use of attributes when calling syslog call 
- Move -miscfiles_read_localization to domain.te to save hundreds of allow rules
- Allow all domains to read locale files.  This eliminates around 1500 allow rules- Cleanup nis_use_ypbind_uncond interface
- Allow rndc to block suspend
- tuned needs to modify the schedule of the kernel
- Allow svirt_t domains to read alsa configuration files
- ighten security on irc domains and make sure they label content in homedir correctly
- Add filetrans_home_content for irc files
- Dontaudit all getattr access for devices and filesystems for sandbox domains
- Allow stapserver to search cgroups directories
- Allow all postfix domains to talk to spamd

* Mon Sep 17 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-21
- Add interfaces to ignore setattr until kernel fixes this to be checked after the DAC check
- Change pam_t to pam_timestamp_t
- Add dovecot_domain attribute and allow this attribute block_suspend capability2
- Add sanlock_use_fusefs boolean
- numad wants send/recieve msg
- Allow rhnsd to send syslog msgs
- Make piranha-pulse as initrc domain
- Update openshift instances to dontaudit setattr until the kernel is fixed.

* Fri Sep 14 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-20
-  Fix auth_login_pgm_domain() interface to allow domains also managed user tmp dirs because of #856880 related to pam_systemd
- Remove pam_selinux.8 which conflicts with man page owned by the pam package
- Allow glance-api to talk to mysql
- ABRT wants to read Xorg.0.log if if it detects problem with Xorg
- Fix gstreamer filename trans. interface

* Thu Sep 13 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-19
- Man page fixes by Dan Walsh

* Tue Sep 11 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-18
- Allow postalias to read postfix config files
- Allow man2html to read man pages
- Allow rhev-agentd to search all mountpoints
- Allow rhsmcertd to read /dev/random
- Add tgtd_stream_connect() interface
- Add cyrus_write_data() interface
- Dontaudit attempts by sandboxX clients connectiing to the xserver_port_t
- Add port definition for tcp/81 as http_port_t
- Fix /dev/twa labeling
- Allow systemd to read modules config

* Mon Sep 10 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-17
- Merge openshift policy
- Allow xauth to read /dev/urandom
- systemd needs to relabel content in /run/systemd directories
- Files unconfined should be able to perform all services on all files
- Puppet tmp file can be leaked to all domains
- Dontaudit rhsmcertd-worker to search /root/.local
- Allow chown capability for zarafa domains
-  Allow system cronjobs to runcon into openshift domains
- Allow virt_bridgehelper_t to manage content in the svirt_home_t labeled directories

* Fri Sep 7 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-16
- nmbd wants to create /var/nmbd
-  Stop transitioning out of anaconda and firstboot, just causes AVC messages
- Allow clamscan to read /etc files
- Allow bcfg2 to bind cyphesis port
- heartbeat should be run as rgmanager_t instead of corosync_t
- Add labeling for /etc/openldap/certs
- Add labeling for /opt/sartest directory
- Make crontab_t as userdom home reader
- Allow tmpreaper to list admin_home dir
- Add defition for imap_0 replay cache file
- Add support for gitolite3
- Allow virsh_t to send syslog messages
- allow domains that can read samba content to be able to list the directories also
- Add realmd_dbus_chat to allow all apps that use nsswitch to talk to realmd
- Separate out sandbox from sandboxX policy so we can disable it by default
- Run dmeventd as lvm_t
- Mounting on any directory requires setattr and write permissions
- Fix use_nfs_home_dirs() boolean
- New labels for pam_krb5
- Allow init and initrc domains to sys_ptrace since this is needed to look at processes not owned by uid 0
- Add realmd_dbus_chat to allow all apps that use nsswitch to talk to realmd

* Fri Aug 31 2012 Dan Walsh <dwalsh@redhat.com> 3.11.1-15
- Separate sandbox policy into sandbox and sandboxX, and disable sandbox by default on fresh installs
- Allow domains that can read etc_t to read etc_runtime_t 
- Allow all domains to use inherited tmpfiles

* Wed Aug 29 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-14
- Allow realmd to read resolv.conf
- Add pegasus_cache_t type
- Label /usr/sbin/fence_virtd as virsh_exec_t
- Add policy for pkcsslotd
- Add support for cpglockd
- Allow polkit-agent-helper to read system-auth-ac
- telepathy-idle wants to read gschemas.compiled
- Allow plymouthd to getattr on fs_t
- Add slpd policy
- Allow ksysguardproces to read/write config_usr_t

* Sat Aug 25 2012 Dan Walsh <dwalsh@redhat.com> 3.11.1-13
- Fix labeling substitution so rpm will label /lib/systemd content correctly

* Fri Aug 24 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-12
- Add file name transitions for ttyACM0
- spice-vdagent(d)'s are going to log over to syslog
- Add sensord policy
- Add more fixes for passenger policy related to puppet
- Allow wdmd to create wdmd_tmpfs_t
- Fix labeling for /var/run/cachefilesd\.pid
- Add thumb_tmpfs_t files type

* Mon Aug 20 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-11
- Allow svirt domains to manage the network since this is containerized
- Allow svirt_lxc_net_t to send audit messages

* Mon Aug 20 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-10
- Make "snmpwalk -mREDHAT-CLUSTER-MIB ...." working
- Allow dlm_controld to execute dlm_stonith labeled as bin_t
- Allow GFS2 working on F17
- Abrt needs to execute dmesg
- Allow jockey to list the contents of modeprobe.d
- Add policy for lightsquid as squid_cron_t
- Mailscanner is creating files and directories in /tmp
- dmesg is now reading /dev/kmsg
- Allow xserver to communicate with secure_firmware
- Allow fsadm tools (fsck) to read /run/mount contnet
- Allow sysadm types to read /dev/kmsg
- 

* Thu Aug 16 2012 Dan Walsh <dwalsh@redhat.com> 3.11.1-9
- Allow postfix, sssd, rpcd to block_suspend
- udev seems to need secure_firmware capability
- Allow virtd to send dbus messages to firewalld so it can configure the firewall

* Thu Aug 16 2012 Dan Walsh <dwalsh@redhat.com> 3.11.1-8
- Fix labeling of content in /run created by virsh_t
- Allow condor domains to read kernel sysctls
- Allow condor_master to connect to amqp
- Allow thumb drives to create shared memory and semaphores
- Allow abrt to read mozilla_plugin config files
- Add labels for lightsquid
- Default files in /opt and /usr that end in .cgi as httpd_sys_script_t, allow
- dovecot_auth_t uses ldap for user auth
- Allow domains that can read dhcp_etc_t to read lnk_files
- Add more then one watchdog device
- Allow useradd_t to manage etc_t files so it can rename it and edit them
- Fix invalid class dir should be fifo_file
- Move /run/blkid to fsadm and make sure labeling is correct

* Tue Aug 14 2012 Dan Walsh <dwalsh@redhat.com> 3.11.1-7
- Fix bogus regex found by eparis
- Fix manage run interface since lvm needs more access
- syslogd is searching cgroups directory
- Fixes to allow virt-sandbox-service to manage lxc var run content

* Mon Aug 13 2012 Dan Walsh <dwalsh@redhat.com> 3.11.1-6
- Fix Boolean settings
- Add new libjavascriptcoregtk as textrel_shlib_t
- Allow xdm_t to create xdm_home_t directories
- Additional access required for systemd
- Dontaudit mozilla_plugin attempts to ipc_lock
- Allow tmpreaper to delete unlabeled files
- Eliminate screen_tmp_t and allow it to manage user_tmp_t
- Dontaudit mozilla_plugin_config_t to append to leaked file descriptors
- Allow web plugins to connect to the asterisk ports
- Condor will recreate the lock directory if it does not exist
- Oddjob mkhomedir needs to connectto user processes
- Make oddjob_mkhomedir_t a userdom home manager

* Thu Aug 9 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-5
- Put placeholder back in place for proper numbering of capabilities
- Systemd also configures init scripts

* Thu Aug 9 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-4
- Fix ecryptfs interfaces
- Bootloader seems to be trolling around /dev/shm and /dev
- init wants to create /etc/systemd/system-update.target.wants
- Fix systemd_filetrans call to move it out of tunable
- Fix up policy to work with systemd userspace manager
- Add secure_firmware capability and remove bogus epolwakeup
- Call seutil_*_login_config interfaces where should be needed
- Allow rhsmcertd to send signal to itself
- Allow thin domains to send signal to itself
- Allow Chrome_ChildIO to read dosfs_t

* Tue Aug 7 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-3
- Add role rules for realmd, sambagui

* Tue Aug 7 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-2
- Add new type selinux_login_config_t for /etc/selinux/<type>/logins/
- Additional fixes for seutil_manage_module_store()
- dbus_system_domain() should be used with optional_policy
- Fix svirt to be allowed to use fusefs file system
- Allow login programs to read /run/ data created by systemd_login
- sssd wants to write /etc/selinux/<policy>/logins/ for SELinux PAM module
- Fix svirt to be allowed to use fusefs file system
- Allow piranha domain to use nsswitch
- Sanlock needs to send Kill Signals to non root processes
- Pulseaudio wants to execute /run/user/PID/.orc

* Fri Aug 3 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-1
- Fix saslauthd when it tries to read /etc/shadow
- Label gnome-boxes as a virt homedir
- Need to allow svirt_t ability to getattr on nfs_t file systems
- Update sanlock policy to solve all AVC's
- Change confined users can optionally manage virt content
- Handle new directories under ~/.cache
- Add block suspend to appropriate domains
- More rules required for containers
- Allow login programs to read /run/ data created by systemd_logind
- Allow staff users to run svirt_t processes

* Thu Aug 2 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.1-0
- Update to upstream

* Mon Jul 30 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.0-15
- More fixes for systemd to make rawhide booting from Dan Walsh

* Mon Jul 30 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.0-14
- Add systemd fixes to make rawhide booting

* Fri Jul 27 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.0-13
- Add systemd_logind_inhibit_var_run_t attribute
- Remove corenet_all_recvfrom_unlabeled() for non-contrib policies because we moved it to domain.if for all domain_type
- Add interface for mysqld to dontaudit signull to all processes
- Label new /var/run/journal directory correctly
- Allow users to inhibit suspend via systemd
- Add new type for the /var/run/inhibit directory
- Add interface to send signull to systemd_login so avahi can send them
- Allow systemd_passwd to send syslog messages
- Remove corenet_all_recvfrom_unlabeled() calling fro policy files
- Allow       editparams.cgi running as httpd_bugzilla_script_t to read /etc/group
- Allow smbd to read cluster config
- Add additional labeling for passenger
- Allow dbus to inhibit suspend via systemd
- Allow avahi to send signull to systemd_login

* Mon Jul 23 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.0-12
- Add interface to dontaudit getattr access on sysctls
- Allow sshd to execute /bin/login
- Looks like xdm is recreating the xdm directory in ~/.cache/ on login
- Allow syslog to use the leaked kernel_t unix_dgram_socket from system-jounald
-  Fix semanage to work with unconfined domain disabled on F18
- Dontaudit attempts by mozilla plugins to getattr on all kernel sysctls
- Virt seems to be using lock files
- Dovecot seems to be searching directories of every mountpoint
- Allow jockey to read random/urandom, execute shell and install third-party drivers
- Add aditional params to allow cachedfiles to manage its content
- gpg agent needs to read /dev/random
- The kernel hands an svirt domains /SYSxxxxx which is a tmpfs that httpd wants to read and write
- Add a bunch of dontaudit rules to quiet svirt_lxc domains
- Additional perms needed to run svirt_lxc domains
- Allow cgclear to read cgconfig
- Allow sys_ptrace capability for snmp
- Allow freshclam to read /proc
- Allow procmail to manage /home/user/Maildir content
- Allow NM to execute wpa_cli
- Allow amavis to read clamd system state
- Regenerate man pages

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.11.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 16 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.0-10
- Add realmd and stapserver policies
- Allow useradd to manage stap-server lib files
- Tighten up capabilities for confined users
- Label /etc/security/opasswd as shadow_t
- Add label for /dev/ecryptfs
- Allow condor_startd_t to start sshd with the ranged
- Allow lpstat.cups to read fips_enabled file
- Allow pyzor running as spamc_t to create /root/.pyzor directory
- Add labelinf for amavisd-snmp init script
- Add support for amavisd-snmp
- Allow fprintd sigkill self
- Allow xend (w/o libvirt) to start virtual machines
- Allow aiccu to read /etc/passwd
- Allow condor_startd to Make specified domain MCS trusted for setting any category set for the processes it executes
- Add condor_startd_ranged_domtrans_to() interface
- Add ssd_conf_t for /etc/sssd
- accountsd needs to fchown some files/directories
- Add ICACLient and zibrauserdata as mozilla_filetrans_home_content
- SELinux reports afs_t needs dac_override to read /etc/mtab, even though everything works, adding dontaudit
- Allow xend_t to read the /etc/passwd file

* Wed Jul 11 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.0-9
- Until we figure out how to fix systemd issues, allow all apps that send syslog messages to send them to kernel_t
- Add init_access_check() interface
- Fix label on /usr/bin/pingus to not be labeled as ping_exec_t
- Allow tcpdump to create a netlink_socket
- Label newusers like useradd
- Change xdm log files to be labeled xdm_log_t
- Allow sshd_t with privsep to work in MLS
- Allow freshclam to update databases thru HTTP proxy
- Allow s-m-config to access check on systemd
- Allow abrt to read public files by default
- Fix amavis_create_pid_files() interface
- Add labeling and filename transition for dbomatic.log
- Allow system_dbusd_t to stream connect to bluetooth, and use its socket
- Allow amavisd to execute fsav
- Allow tuned to use sys_admin and sys_nice capabilities
- Add php-fpm policy from Bryan
- Add labeling for aeolus-configserver-thinwrapper
- Allow thin domains to execute shell
- Fix gnome_role_gkeyringd() interface description
- Lot of interface fixes
- Allow OpenMPI job running as condor_startd_ssh_t to manage condor lib files
- Allow OpenMPI job to use kerberos
- Make deltacloudd_t as nsswitch_domain
- Allow xend_t to run lsscsi
- Allow qemu-dm running as xend_t to create tun_socket
- Add labeling for /opt/brother/Printers(.*/)?inf
- Allow jockey-backend to read pyconfig-64.h labeled as usr_t
- Fix clamscan_can_scan_system boolean
- Allow lpr to connectto to /run/user/$USER/keyring-22uREb/pkcs11

* Tue Jul 3 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.0-8
- initrc is calling exportfs which is not confined so it attempts to read nfsd_files
- Fixes for passenger running within openshift.
- Add labeling for all tomcat6 dirs
- Add support for tomcat6
- Allow cobblerd to read /etc/passwd
- Allow jockey to read sysfs and and execute binaries with bin_t
- Allow thum to use user terminals
- Allow cgclear to read cgconfig config files
- Fix bcf2g.fc
- Remove sysnet_dns_name_resolve() from policies where auth_use_nsswitch() is used for other domains
- Allow dbomatic to execute ruby
- abrt_watch_log should be abrt_domain
- Allow mozilla_plugin to connect to gatekeeper port

* Wed Jun 27 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.0-7
- add ptrace_child access to process
- remove files_read_etc_files() calling from all policies which have auth_use_nsswith()
- Allow boinc domains to manage boinc_lib_t lnk_files
- Add support for boinc-client.service unit file
- Add support for boinc.log
- Allow mozilla_plugin execmod on mozilla home files if allow_ex
- Allow dovecot_deliver_t to read dovecot_var_run_t
- Allow ldconfig and insmod to manage kdumpctl tmp files
- Move thin policy out from cloudform.pp and add a new thin poli
- pacemaker needs to communicate with corosync streams
- abrt is now started on demand by dbus
- Allow certmonger to talk directly to Dogtag servers
- Change labeling for /var/lib/cobbler/webui_sessions to httpd_c
- Allow mozila_plugin to execute gstreamer home files
- Allow useradd to delete all file types stored in the users hom
- rhsmcertd reads the rpm database
- Add support for lightdm


* Mon Jun 25 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.0-6
- Add tomcat policy
- Remove pyzor/razor policy
- rhsmcertd reads the rpm database
- Dontaudit  thumb to setattr on xdm_tmp dir
- Allow wicd to execute ldconfig in the networkmanager_t domain
- Add /var/run/cherokee\.pid labeling
- Allow mozilla_plugin to create mozilla_plugin_tmp_t lnk files too
- Allow postfix-master to r/w pipes other postfix domains
- Allow snort to create netlink_socket
- Add kdumpctl policy
- Allow firstboot to create tmp_t files/directories
- /usr/bin/paster should not be labeled as piranha_exec_t
- remove initrc_domain from tomcat
- Allow ddclient to read /etc/passwd
- Allow useradd to delete all file types stored in the users homedir
- Allow ldconfig and insmod to manage kdumpctl tmp files
- Firstboot should be just creating tmp_t dirs and xauth should be allowed to write to those
- Transition xauth files within firstboot_tmp_t
- Fix labeling of /run/media to match /media
- Label all lxdm.log as xserver_log_t
- Add port definition for mxi port
- Allow local_login_t to execute tmux

* Tue Jun 19 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.0-5
- apcupsd needs to read /etc/passwd
- Sanlock allso sends sigkill
- Allow glance_registry to connect to the mysqld port
- Dontaudit mozilla_plugin trying to getattr on /dev/gpmctl
- Allow firefox plugins/flash to connect to port 1234
- Allow mozilla plugins to delete user_tmp_t files
- Add transition name rule for printers.conf.O
- Allow virt_lxc_t to read urand
- Allow systemd_loigind to list gstreamer_home_dirs
- Fix labeling for /usr/bin
- Fixes for cloudform services
  * support FIPS
- Allow polipo to work as web caching
- Allow chfn to execute tmux

* Fri Jun 15 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.0-4
- Add support for ecryptfs
  * ecryptfs does not support xattr
  * we need labeling for HOMEDIR
- Add policy for (u)mount.ecryptfs*
- Fix labeling of kerbero host cache files, allow rpc.svcgssd to manage host cache
- Allow dovecot to manage Maildir content, fix transitions to Maildir
- Allow postfix_local to transition to dovecot_deliver
- Dontaudit attempts to setattr on xdm_tmp_t, looks like bogus code
- Cleanup interface definitions
- Allow apmd to change with the logind daemon
- Changes required for sanlock in rhel6
- Label /run/user/apache as httpd_tmp_t
- Allow thumb to use lib_t as execmod if boolean turned on
- Allow squid to create the squid directory in /var with the correct labe
- Add a new policy for glusterd from Bryan Bickford (bbickfor@redhat.com)
- Allow virtd to exec xend_exec_t without transition
- Allow virtd_lxc_t to unmount all file systems

* Tue Jun 12 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.0-3
- PolicyKit path has changed
- Allow httpd connect to dirsrv socket
- Allow tuned to write generic kernel sysctls
- Dontaudit logwatch to gettr on /dev/dm-2
- Allow policykit-auth to manage kerberos files
- Make condor_startd and rgmanager as initrc domain
- Allow virsh to read /etc/passwd
- Allow mount to mount on user_tmp_t for /run/user/dwalsh/gvfs
- xdm now needs to execute xsession_exec_t
- Need labels for /var/lib/gdm
- Fix files_filetrans_named_content() interface
- Add new attribute - initrc_domain
- Allow systemd_logind_t to signal, signull, sigkill all processes
- Add filetrans rules for etc_runtime files

* Sat Jun 9 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.0-2
- Rename boolean names to remove allow_

* Thu Jun 7 2012 Miroslav Grepl <mgrepl@redhat.com> 3.11.0-1
- Mass merge with upstream
  * new policy topology to include contrib policy modules
  * we have now two base policy patches

* Wed May 30 2012 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-128
- Fix description of authlogin_nsswitch_use_ldap
- Fix transition rule for rhsmcertd_t needed for RHEL7
- Allow useradd to list nfs state data
- Allow openvpn to manage its log file and directory
- We want vdsm to transition to mount_t when executing mount command to make sure /etc/mtab remains labeled correctly
- Allow thumb to use nvidia devices
-  Allow local_login to create user_tmp_t files for kerberos
- Pulseaudio needs to read systemd_login /var/run content
- virt should only transition named system_conf_t config files
- Allow  munin to execute its plugins
- Allow nagios system plugin to read /etc/passwd
- Allow plugin to connect to soundd port
- Fix httpd_passwd to be able to ask passwords
- Radius servers can use ldap for backing store
- Seems to need to mount on /var/lib for xguest polyinstatiation to work.
- Allow systemd_logind to list the contents of gnome keyring
- VirtualGL need xdm to be able to manage content in /etc/opt/VirtualGL
- Add policy for isns-utils

* Mon May 28 2012 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-127
- Add policy for subversion daemon
- Allow boinc to read passwd
- Allow pads to read kernel network state
- Fix man2html interface for sepolgen-ifgen
- Remove extra /usr/lib/systemd/system/smb
- Remove all /lib/systemd and replace with /usr/lib/systemd
- Add policy for man2html
- Fix the label of kerberos_home_t to krb5_home_t
- Allow mozilla plugins to use Citrix
- Allow tuned to read /proc/sys/kernel/nmi_watchdog
- Allow tune /sys options via systemd's tmpfiles.d "w" type

* Wed May 23 2012 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-126
- Dontaudit lpr_t to read/write leaked mozilla tmp files
- Add file name transition for .grl-podcasts directory
- Allow corosync to read user tmp files
- Allow fenced to create snmp lib dirs/files
- More fixes for sge policy
- Allow mozilla_plugin_t to execute any application
- Allow dbus to read/write any open file descriptors to any non security file on the system that it inherits to that it can pass them to another domain
- Allow mongod to read system state information
-  Fix wrong type, we should dontaudit sys_admin for xdm_t not xserver_t
- Allow polipo to manage polipo_cache dirs
- Add jabbar_client port to mozilla_plugin_t
- Cleanup procmail policy
- system bus will pass around open file descriptors on files that do not have labels on them
- Allow l2tpd_t to read system state
- Allow tuned to run ls /dev
- Allow sudo domains to read usr_t files
- Add label to machine-id 
- Fix corecmd_read_bin_symlinks cut and paste error

* Wed May 16 2012 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-125
- Fix pulseaudio port definition
- Add labeling for condor_starter
- Allow chfn_t to creat user_tmp_files
- Allow chfn_t to execute bin_t
- Allow prelink_cron_system_t to getpw calls
- Allow sudo domains to manage kerberos rcache files
- Allow user_mail_domains to work with courie
- Port definitions necessary for running jboss apps within openshift
-  Add support for openstack-nova-metadata-api
- Add support for nova-console*
- Add support for openstack-nova-xvpvncproxy
- Fixes to make privsep+SELinux working if we try to use chage to change passwd
- Fix auth_role() interface
- Allow numad to read sysfs
- Allow matahari-rpcd to execute shell
- Add label for ~/.spicec
- xdm is executing lspci as root which is requesting a sys_admin priv but seems to succeed without it
- Devicekit_disk wants to read the logind sessions file when writing a cd
- Add fixes for condor to make condor jobs working correctly
- Change label of /var/log/rpmpkgs to cron_log_t
- Access requires to allow systemd-tmpfiles --create to work.
- Fix obex to be a user application started by the session bus.
- Add additional filename trans rules for kerberos
- Fix /var/run/heartbeat labeling
- Allow apps that are managing rcache to file trans correctly
- Allow openvpn to authenticate against ldap server
- Containers need to listen to network starting and stopping events

* Wed May 9 2012 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-124
- Make systemd unit files less specific

* Tue May 8 2012 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-123
- Fix zarafa labeling
- Allow guest_t to fix labeling
- corenet_tcp_bind_all_unreserved_ports(ssh_t) should be called with the user_tcp_server boolean
- add lxc_contexts
- Allow accountsd to read /proc
- Allow restorecond to getattr on all file sytems
- tmpwatch now calls getpw
- Allow apache daemon to transition to pwauth domain
- Label content under /var/run/user/NAME/keyring* as gkeyringd_tmp_t
- The obex socket seems to be a stream socket
- dd label for /var/run/nologin

* Mon May 7 2012 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-122
- Allow jetty running as httpd_t to read hugetlbfs files
- Allow sys_nice and setsched for rhsmcertd
- Dontaudit attempts by mozilla_plugin_t to bind to ssdp ports
- Allow setfiles to append to xdm_tmp_t
- Add labeling for /export as a usr_t directory
- Add labels for .grl files created by gstreamer

* Fri May 4 2012 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-121
- Add labeling for /usr/share/jetty/bin/jetty.sh
- Add jetty policy which contains file type definitios
- Allow jockey to use its own fifo_file and make this the default for all domains
- Allow mozilla_plugins to use spice (vnc_port/couchdb)
- asterisk wants to read the network state
- Blueman now uses /var/lib/blueman- Add label for nodejs_debug
- Allow mozilla_plugin_t to create ~/.pki directory and content

* Wed May 2 2012 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-120
- Add clamscan_can_scan_system boolean
- Allow mysqld to read kernel network state
- Allow sshd to read/write condor lib files
- Allow sshd to read/write condor-startd tcp socket
- Fix description on httpd_graceful_shutdown
- Allow glance_registry to communicate with mysql
- dbus_system_domain is using systemd to lauch applications
- add interfaces to allow domains to send kill signals to user mail agents
- Remove unnessary access for svirt_lxc domains, add privs for virtd_lxc_t
- Lots of new access required for secure containers
- Corosync needs sys_admin capability
- ALlow colord to create shm
- .orc should be allowed to be created by any app that can create gstream home content, thumb_t to be specific
- Add boolean to control whether or not mozilla plugins can create random content in the users homedir
-  Add new interface to allow domains to list msyql_db directories, needed for libra
- shutdown has to be allowed to delete etc_runtime_t
- Fail2ban needs to read /etc/passwd
-  Allow ldconfig to create /var/cache/ldconfig
- Allow tgtd to read hardware state information
- Allow collectd to create packet socket
- Allow chronyd to send signal to itself
- Allow collectd to read /dev/random
- Allow collectd to send signal to itself
- firewalld needs to execute restorecon
- Allow restorecon and other login domains to execute restorecon

* Tue Apr 24 2012 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-119
- Allow logrotate to getattr on systemd unit files
- Add support for tor systemd unit file
- Allow apmd to create /var/run/pm-utils with the correct label
- Allow l2tpd to send sigkill to pppd
- Allow pppd to stream connect to l2tpd
- Add label for scripts in /etc/gdm/
- Allow systemd_logind_t to ignore mcs constraints on sigkill
- Fix files_filetrans_system_conf_named_files() interface
- Add labels for /usr/share/wordpress/wp-includes/*.php
- Allow cobbler to get SELinux mode and booleans

* Mon Apr 23 2012 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-118
- Add unconfined_execmem_exec_t as an alias to bin_t
- Allow fenced to read snmp var lib files, also allow it to read usr_t
- ontaudit access checks on all executables from mozilla_plugin
- Allow all user domains to setexec, so that sshd will work properly if it call setexec(NULL) while running withing a user mode
- Allow systemd_tmpfiles_t to getattr all pipes and sockets
- Allow glance-registry to send system log messages
- semanage needs to manage mock lib files/dirs

* Sun Apr 22 2012 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-117
- Add policy for abrt-watch-log
- Add definitions for jboss_messaging ports
- Allow systemd_tmpfiles to manage printer devices
- Allow oddjob to use nsswitch
- Fix labeling of log files for postgresql
- Allow mozilla_plugin_t to execmem and execstack by default
- Allow firewalld to execute shell
- Fix /etc/wicd content files to get created with the correct label
- Allow mcelog to exec shell
- Add ~/.orc as a gstreamer_home_t
- /var/spool/postfix/lib64 should be labeled lib_t
- mpreaper should be able to list all file system labeled directories
- Add support for apache to use openstack
- Add labeling for /etc/zipl.conf and zipl binary
- Turn on allow_execstack and turn off telepathy transition for final release

* Mon Apr 16 2012 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-116
- More access required for virt_qmf_t
- Additional assess required for systemd-logind to support multi-seat
- Allow mozilla_plugin to setrlimit
- Revert changes to fuse file system to stop deadlock

* Mon Apr 16 2012 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-115
- Allow condor domains to connect to ephemeral ports
- More fixes for condor policy
- Allow keystone to stream connect to mysqld
- Allow mozilla_plugin_t to read generic USB device to support GPS devices
- Allow thum to file name transition gstreamer home content
- Allow thum to read all non security files
- Allow glance_api_t to connect to ephemeral ports
- Allow nagios plugins to read /dev/urandom
- Allow syslogd to search postfix spool to support postfix chroot env
- Fix labeling for /var/spool/postfix/dev
- Allow wdmd chown
- Label .esd_auth as pulseaudio_home_t
- Have no idea why keyring tries to write to /run/user/dwalsh/dconf/user, but we can dontaudit for now

* Fri Apr 13 2012 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-114
- Add support for clamd+systemd
- Allow fresclam to execute systemctl to handle clamd
- Change labeling for /usr/sbin/rpc.ypasswd.env
	- Allow yppaswd_t to execute yppaswd_exec_t
	- Allow yppaswd_t to read /etc/passwd
- Gnomekeyring socket has been moved to /run/user/USER/
- Allow samba-net to connect to ldap port
- Allow signal for vhostmd
- allow mozilla_plugin_t to read user_home_t socket
- New access required for secure Linux Containers
- zfs now supports xattrs
- Allow quantum to execute sudo and list sysfs
- Allow init to dbus chat with the firewalld
- Allow zebra to read /etc/passwd

* Tue Apr 10 2012 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-113
- Allow svirt_t to create content in the users homedir under ~/.libvirt
- Fix label on /var/lib/heartbeat
- Allow systemd_logind_t to send kill signals to all processes started by a user
- Fuse now supports Xattr Support

* Tue Apr 10 2012 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-112
- upowered needs to setsched on the kernel
- Allow mpd_t to manage log files
- Allow xdm_t to create /var/run/systemd/multi-session-x
- Add rules for missedfont.log to be used by thumb.fc
- Additional access required for virt_qmf_t
- Allow dhclient to dbus chat with the firewalld
- Add label for lvmetad
- Allow systemd_logind_t to remove userdomain sock_files
- Allow cups to execute usr_t files
- Fix labeling on nvidia shared libraries
- wdmd_t needs access to sssd and /etc/passwd
- Add boolean to allow ftp servers to run in passive mode
- Allow namepspace_init_t to relabelto/from a different user system_u from the user the namespace_init running with
- Fix using httpd_use_fusefs
- Allow chrome_sandbox_nacl to write inherited user tmp files as we allow it for chrome_sandbox

* Fri Apr 6 2012 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-111
- Rename rdate port to time port, and allow gnomeclock to connect to it
- We no longer need to transition to ldconfig from rpm, rpm_script, or anaconda
- /etc/auto.* should be labeled bin_t
- Add httpd_use_fusefs boolean
- Add fixes for heartbeat
- Allow sshd_t to signal processes that it transitions to
- Add condor policy
- Allow svirt to create monitors in ~/.libvirt
- Allow dovecot to domtrans sendmail to handle sieve scripts
- Lot of fixes for cfengine

* Tue Apr 3 2012 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-110
- /var/run/postmaster.* labeling is no longer needed
- Alllow drbdadmin to read /dev/urandom
- l2tpd_t seems to use ptmx
- group+ and passwd+ should be labeled as /etc/passwd
- Zarafa-indexer is a socket

* Fri Mar 30 2012 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-109
- Ensure lastlog is labeled correctly
- Allow accountsd to read /proc data about gdm
- Add fixes for tuned
- Add bcfg2 fixes which were discovered during RHEL6 testing
- More fixes for gnome-keyring socket being moved
- Run semanage as a unconfined domain, and allow initrc_t to create tmpfs_t sym links on shutdown
- Fix description for files_dontaudit_read_security_files() interface

* Wed Mar 28 2012 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-108
- Add new policy and man page for bcfg2
- cgconfig needs to use getpw calls
- Allow domains that communicate with the keyring to use cache_home_t instead of gkeyringd_tmpt
- gnome-keyring wants to create a directory in cache_home_t
- sanlock calls getpw

* Wed Mar 28 2012 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-107
- Add numad policy and numad man page
- Add fixes for interface bugs discovered by SEWatch
- Add /tmp support for squid
- Add fix for #799102
     * change default labeling for /var/run/slapd.* sockets
- Make thumb_t as userdom_home_reader
- label /var/lib/sss/mc same as pubconf, so getpw domains can read it
- Allow smbspool running as cups_t to stream connect to nmbd
- accounts needs to be able to execute passwd on behalf of users
- Allow systemd_tmpfiles_t to delete boot flags
- Allow dnssec_trigger to connect to apache ports
- Allow gnome keyring to create sock_files in ~/.cache
- google_authenticator is using .google_authenticator
- sandbox running from within firefox is exposing more leaks
- Dontaudit thumb to read/write /dev/card0
- Dontaudit getattr on init_exec_t for gnomeclock_t
- Allow certmonger to do a transition to certmonger_unconfined_t
- Allow dhcpc setsched which is caused by nmcli
- Add rpm_exec_t for /usr/sbin/bcfg2
- system cronjobs are sending dbus messages to systemd_logind
- Thumnailers read /dev/urand

* Thu Mar 22 2012 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-106
- Allow auditctl getcap
- Allow vdagent to use libsystemd-login
- Allow abrt-dump-oops to search /etc/abrt
- Got these avc's while trying to print a boarding pass from firefox
- Devicekit is now putting the media directory under /run/media
- Allow thumbnailers to create content in ~/.thumbails directory
- Add support for proL2TPd by Dominick Grift
- Allow all domains to call getcap
- wdmd seems to get a random chown capability check that it does not need
- Allow vhostmd to read kernel sysctls

* Wed Mar 21 2012 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-105
- Allow chronyd to read unix
- Allow hpfax to read /etc/passwd
- Add support matahari vios-proxy-* apps and add virtd_exec_t label for them
- Allow rpcd to read quota_db_t
- Update to man pages to match latest policy
- Fix bug in jockey interface for sepolgen-ifgen
- Add initial svirt_prot_exec_t policy

* Mon Mar 19 2012 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-104
- More fixes for systemd from Dan Walsh

* Mon Mar 19 2012 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-103
- Add a new type for /etc/firewalld and allow firewalld to write to this directory
- Add definition for ~/Maildir, and allow mail deliver domains to write there
- Allow polipo to run from a cron job
- Allow rtkit to schedule wine processes
- Allow mozilla_plugin_t to acquire a bug, and allow it to transition gnome content in the home dir to the proper label
- Allow users domains to send signals to consolehelper domains

* Fri Mar 16 2012 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-102
- More fixes for boinc policy
- Allow polipo domain to create its own cache dir and pid file
- Add systemctl support to httpd domain
- Add systemctl support to polipo, allow NetworkManager to manage the service
- Add policy for jockey-backend
- Add support for motion daemon which is now covered by zoneminder policy
- Allow colord to read/write motion tmpfs
- Allow vnstat to search through var_lib_t directories
- Stop transitioning to quota_t, from init an sysadm_t

* Wed Mar 14 2012 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-101
- Add svirt_lxc_file_t as a customizable type

* Wed Mar 14 2012 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-100
- Add additional fixes for icmp nagios plugin
- Allow cron jobs to open fifo_files from cron, since service script opens /dev/stdin
- Add certmonger_unconfined_exec_t
- Make sure tap22 device is created with the correct label
- Allow staff users to read systemd unit files
- Merge in previously built policy
- Arpwatch needs to be able to start netlink sockets in order to start
- Allow cgred_t to sys_ptrace to look at other DAC Processes

* Mon Mar 12 2012 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-99
- Back port some of the access that was allowed in nsplugin_t
- Add definitiona for couchdb ports
- Allow nagios to use inherited users ttys
- Add git support for mock
- Allow inetd to use rdate port
- Add own type for rdate port
- Allow samba to act as a portmapper
- Dontaudit chrome_sandbox attempts to getattr on chr_files in /dev
- New fixes needed for samba4
- Allow apps that use lib_t to read lib_t symlinks

* Fri Mar 9 2012 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-98
- Add policy for nove-cert
- Add labeling for nova-openstack  systemd unit files
- Add policy for keystoke 

* Thu Mar 8 2012 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-97
- Fix man pages fro domains
- Add man pages for SELinux users and roles
- Add storage_dev_filetrans_named_fixed_disk() and use it for smartmon
- Add policy for matahari-rpcd
- nfsd executes mount command on restart
- Matahari domains execute renice and setsched
- Dontaudit leaked tty in mozilla_plugin_config
- mailman is changing to a per instance naming
- Add 7600 and 4447 as jboss_management ports
- Add fixes for nagios event handlers
- Label httpd.event as httpd_exec_t, it is an apache daemon

* Mon Mar 5 2012 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-96
- Add labeling for /var/spool/postfix/dev/log
- NM reads sysctl.conf
- Iscsi log file context specification fix
-  Allow mozilla plugins to send dbus messages to user domains that transition to it
- Allow mysql to read the passwd file
- Allow mozilla_plugin_t to create mozilla home dirs in user homedir
- Allow deltacloud to read kernel sysctl
- Allow postgresql_t to connectto itselfAllow postgresql_t to connectto itself
- Allow postgresql_t to connectto itself
- Add login_userdomain attribute for users which can log in using terminal

* Tue Feb 28 2012 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-95
- Allow sysadm_u to reach system_r by default #784011
- Allow nagios plugins to use inherited user terminals
- Razor labeling is not used no longer
- Add systemd support for matahari
- Add port_types to man page, move booleans to the top, fix some english
- Add support for matahari-sysconfig-console
- Clean up matahari.fc
- Fix matahari_admin() interfac
- Add labels for/etc/ssh/ssh_host_*.pub keys

* Mon Feb 27 2012 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-94
- Allow ksysguardproces to send system log msgs
- Allow  boinc setpgid and signull
- Allow xdm_t to sys_ptrace to run pidof command
- Allow smtpd_t to manage spool files/directories and symbolic links
- Add labeling for jetty
- Needed changes to get unbound/dnssec to work with openswan

* Thu Feb 23 2012 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-93
- Add user_fonts_t alias xfs_tmp_t
- Since depmod now runs as insmod_t we need to write to kernel_object_t
- Allow firewalld to dbus chat with networkmanager
- Allow qpidd to connect to matahari ports
- policykit needs to read /proc for uses not owned by it
- Allow systemctl apps to connecto the init stream

* Wed Feb 22 2012 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-92
- Turn on deny_ptrace boolean

* Tue Feb 21 2012 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-91
- Remove pam_selinux.8 man page. There was a conflict.

* Tue Feb 21 2012 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-90
- Add proxy class and read access for gssd_proxy
- Separate out the sharing public content booleans
- Allow certmonger to execute a script and send signals to  apache and dirsrv to reload the certificate
-  Add label transition for gstream-0.10 and 12
- Add booleans to allow rsync to share nfs and cifs file sytems
- chrome_sandbox wants to read the /proc/PID/exe file of the program that executed it
- Fix filename transitions for cups files
- Allow denyhosts to read "unix"
- Add file name transition for locale.conf.new
- Allow boinc projects to gconf config files
- sssd needs to be able to increase the socket limit under certain loads
- sge_execd needs to read /etc/passwd
- Allow denyhost to check network state
- NetworkManager needs to read sessions data
- Allow denyhost to check network state
- Allow xen to search virt images directories
- Add label for /dev/megaraid_sas_ioctl_node
- Add autogenerated man pages

* Thu Feb 16 2012 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-89
- Allow boinc project to getattr on fs
- Allow init to execute initrc_state_t
- rhev-agent package was rename to ovirt-guest-agent
- If initrc_t creates /etc/local.conf then we need to make sure it is labeled correctly
- sytemd writes content to /run/initramfs and executes it on shutdown
- kdump_t needs to read /etc/mtab, should be back ported to F16
- udev needs to load kernel modules in early system boot

* Tue Feb 14 2012 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-88
- Need to add sys_ptrace back in since reading any content in /proc can cause these accesses
- Add additional systemd interfaces which are needed fro *_admin interfaces
- Fix bind_admin() interface

* Mon Feb 13 2012 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-87
- Allow firewalld to read urand
- Alias java, execmem_mono to bin_t to allow third parties
- Add label for kmod
- /etc/redhat-lsb contains binaries
- Add boolean to allow gitosis to send mail
- Add filename transition also for "event20"
- Allow systemd_tmpfiles_t to delete all file types
- Allow collectd to ipc_lock

* Fri Feb 10 2012 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-86
- make consoletype_exec optional, so we can remove consoletype policy
- remove unconfined_permisive.patch
- Allow openvpn_t to inherit user home content and tmp content
- Fix dnssec-trigger labeling
- Turn on obex policy for staff_t
- Pem files should not be secret
- Add lots of rules to fix AVC's when playing with containers
- Fix policy for dnssec
- Label ask-passwd directories correctly for systemd

* Thu Feb 9 2012 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-85
- sshd fixes seem to be causing unconfined domains to dyntrans to themselves
- fuse file system is now being mounted in /run/user
- systemd_logind is sending signals to processes that are dbus messaging with it
- Add support for winshadow port and allow iscsid to connect to this port
- httpd should be allowed to bind to the http_port_t udp socket
- zarafa_var_lib_t can be a lnk_file
- A couple of new .xsession-errors files
- Seems like user space and login programs need to read logind_sessions_files
- Devicekit disk seems to be being launched by systemd
- Cleanup handling of setfiles so most of rules in te file
- Correct port number for dnssec
- logcheck has the home dir set to its cache

* Tue Feb 7 2012 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-84
- Add policy for grindengine MPI jobs

* Mon Feb 6 2012 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-83
- Add new sysadm_secadm.pp module
	* contains secadm definition for sysadm_t
- Move user_mail_domain access out of the interface into the te file
- Allow httpd_t to create httpd_var_lib_t directories as well as files
- Allow snmpd to connect to the ricci_modcluster stream
- Allow firewalld to read /etc/passwd
- Add auth_use_nsswitch for colord
- Allow smartd to read network state
- smartdnotify needs to read /etc/group

* Fri Feb 3 2012 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-82
- Allow gpg and gpg_agent to store sock_file in gpg_secret_t directory
- lxdm startup scripts should be labeled bin_t, so confined users will work
- mcstransd now creates a pid, needs back port to F16
- qpidd should be allowed to connect to the amqp port
- Label devices 010-029 as usb devices
- ypserv packager says ypserv does not use tmp_t so removing selinux policy types
- Remove all ptrace commands that I believe are caused by the kernel/ps avcs
- Add initial Obex policy
- Add logging_syslogd_use_tty boolean
- Add polipo_connect_all_unreserved bolean
- Allow zabbix to connect to ftp port
- Allow systemd-logind to be able to switch VTs
- Allow apache to communicate with memcached through a sock_file

* Tue Jan 31 2012 Dan Walsh <dwalsh@redhat.com> 3.10.0-81.2
- Fix file_context.subs_dist for now to work with pre usrmove

* Mon Jan 30 2012 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-81
- More /usr move fixes

* Thu Jan 26 2012 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-80
- Add zabbix_can_network boolean
- Add httpd_can_connect_zabbix boolean
- Prepare file context labeling for usrmove functions
- Allow system cronjobs to read kernel network state
- Add support for selinux_avcstat munin plugin
- Treat hearbeat with corosync policy
- Allow corosync to read and write to qpidd shared mem
-  mozilla_plugin is trying to run pulseaudio 
- Fixes for new sshd patch for running priv sep domains as the users context
- Turn off dontaudit rules when turning on allow_ypbind
- udev now reads /etc/modules.d directory

* Tue Jan 24 2012 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-79
- Turn on deny_ptrace boolean for the Rawhide run, so we can test this out
- Cups exchanges dbus messages with init
- udisk2 needs to send syslog messages
- certwatch needs to read /etc/passwd

* Mon Jan 23 2012 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-78
- Add labeling for udisks2
- Allow fsadmin to communicate with the systemd process

* Mon Jan 23 2012 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-77
- Treat Bip with bitlbee policy
      * Bip is an IRC proxy
- Add port definition for interwise port
- Add support for ipa_memcached socket
- systemd_jounald needs to getattr on all processes
- mdadmin fixes
     * uses getpw
- amavisd calls getpwnam()
- denyhosts calls getpwall()

* Fri Jan 20 2012 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-76
- Setup labeling of /var/rsa and /var/lib/rsa to allow login programs to write there
- bluetooth says they do not use /tmp and want to remove the type
- Allow init to transition to colord
- Mongod needs to read /proc/sys/vm/zone_reclaim_mode
- Allow postfix_smtpd_t to connect to spamd
- Add boolean to allow ftp to connect to all ports > 1023
- Allow sendmain to write to inherited dovecot tmp files
- setroubleshoot needs to be able to execute rpm to see what version of packages
* Mon Jan 16 2012 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-75
- Merge systemd patch
- systemd-tmpfiles wants to relabel /sys/devices/system/cpu/online
- Allow deltacloudd dac_override, setuid, setgid  caps
- Allow aisexec to execute shell
- Add use_nfs_home_dirs boolean for ssh-keygen

* Fri Jan 13 2012 Dan Walsh <dwalsh@redhat.com> 3.10.0-74.2
- Fixes to make rawhide boot in enforcing mode with latest systemd changes

* Wed Jan 11 2012 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-74
- Add labeling for /var/run/systemd/journal/syslog
- libvirt sends signals to ifconfig
- Allow domains that read logind session files to list them

* Wed Jan 11 2012 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-73
- Fixed destined form libvirt-sandbox
- Allow apps that list sysfs to also read sympolicy links in this filesystem
- Add ubac_constrained rules for chrome_sandbox
- Need interface to allow domains to use tmpfs_t files created by the kernel, used by libra
- Allow postgresql to be executed by the caller
- Standardize interfaces of daemons 
- Add new labeling for mm-handler
- Allow all matahari domains to read network state and etc_runtime_t files

* Wed Jan 4 2012 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-72
- New fix for seunshare, requires seunshare_domains to be able to mounton /
- Allow systemctl running as logrotate_t to connect to private systemd socket
- Allow tmpwatch to read meminfo
- Allow rpc.svcgssd to read supported_krb5_enctype
- Allow zarafa domains to read /dev/random and /dev/urandom
- Allow snmpd to read dev_snmp6
- Allow procmail to talk with cyrus
- Add fixes for check_disk and check_nagios plugins

* Tue Dec 20 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-71
- default trans rules for Rawhide policy
-  Make sure sound_devices controlC* are labeled correctly on creation
- sssd now needs sys_admin
- Allow snmp to read all proc_type
- Allow to setup users homedir with quota.group

* Mon Dec 19 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-70
- Add httpd_can_connect_ldap() interface
- apcupsd_t needs to use seriel ports connected to usb devices
- Kde puts procmail mail directory under ~/.local/share
- nfsd_t can trigger sys_rawio on tests that involve too many mountpoints, dontaudit for now
- Add labeling for /sbin/iscsiuio

* Wed Dec 14 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-69
- Add label for /var/lib/iscan/interpreter
- Dont audit writes to leaked file descriptors or redirected output for nacl
- NetworkManager needs to write to /sys/class/net/ib*/mode

* Tue Dec 13 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-68
- Allow abrt  to request the kernel to load a module
- Make sure mozilla content is labeled correctly
- Allow tgtd to read system state
- More fixes for boinc
  * allow to resolve dns name
  * re-write boinc policy to use boinc_domain attribute
- Allow munin services plugins to use NSCD services

* Thu Dec 8 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-67
- Allow mozilla_plugin_t to manage mozilla_home_t
- Allow ssh derived domain to execute ssh-keygen in the ssh_keygen_t domain
- Add label for tumblerd

* Wed Dec 7 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-66
- Fixes for xguest package

* Tue Dec 6 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-65
- Fixes related to  /bin, /sbin
- Allow abrt to getattr on blk files
- Add type for rhev-agent log file
- Fix labeling for /dev/dmfm
- Dontaudit wicd leaking
- Allow systemd_logind_t to look at process info of apps that exchange dbus messages with it
- Label /etc/locale.conf correctly
- Allow user_mail_t to read /dev/random
- Allow postfix-smtpd to read MIMEDefang
- Add label for /var/log/suphp.log
- Allow swat_t to connect and read/write nmbd_t sock_file
- Allow systemd-tmpfiles to setattr for /run/user/gdm/dconf
- Allow systemd-tmpfiles to change user identity in object contexts
- More fixes for rhev_agentd_t consolehelper policy

* Thu Dec 1 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-64
- Use fs_use_xattr for squashf
-  Fix procs_type interface
- Dovecot has a new fifo_file /var/run/dovecot/stats-mail
- Dovecot has a new fifo_file /var/run/stats-mail
- Colord does not need to connect to network
- Allow system_cronjob to dbus chat with NetworkManager
- Puppet manages content, want to make sure it labels everything correctly

* Tue Nov 29 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-63
- Change port 9050 to tor_socks_port_t and then allow openvpn to connect to it
- Allow all postfix domains to use the fifo_file
- Allow sshd_t to getattr on all file systems in order to generate avc on nfs_t
- Allow apmd_t to read grub.cfg
- Let firewallgui read the selinux config
- Allow systemd-tmpfiles to delete content in /root that has been moved to /tmp
- Fix devicekit_manage_pid_files() interface
- Allow squid to check the network state
- Dontaudit colord getattr on file systems
- Allow ping domains to read zabbix_tmp_t files

* Wed Nov 23 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-59
- Allow mcelog_t to create dir and file in /var/run and label it correctly
- Allow dbus to manage fusefs
- Mount needs to read process state when mounting gluster file systems
- Allow collectd-web to read collectd lib files
- Allow daemons and system processes started by init to read/write the unix_stream_socket passed in from as stdin/stdout/stderr
- Allow colord to get the attributes of tmpfs filesystem
- Add sanlock_use_nfs and sanlock_use_samba booleans
- Add bin_t label for /usr/lib/virtualbox/VBoxManage

* Wed Nov 16 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-58
- Add ssh_dontaudit_search_home_dir
- Changes to allow namespace_init_t to work
- Add interface to allow exec of mongod, add port definition for mongod port, 27017
- Label .kde/share/apps/networkmanagement/certificates/ as home_cert_t
- Allow spamd and clamd to steam connect to each other
- Add policy label for passwd.OLD
- More fixes for postfix and postfix maildro
- Add ftp support for mozilla plugins
- Useradd now needs to manage policy since it calls libsemanage
- Fix devicekit_manage_log_files() interface
- Allow colord to execute ifconfig
- Allow accountsd to read /sys
- Allow mysqld-safe to execute shell
- Allow openct to stream connect to pcscd
- Add label for /var/run/nm-dns-dnsmasq\.conf
- Allow networkmanager to chat with virtd_t

* Fri Nov 11 2011 Dan Walsh <dwalsh@redhat.com> 3.10.0-57
- Pulseaudio changes
- Merge patches 

* Thu Nov 10 2011 Dan Walsh <dwalsh@redhat.com> 3.10.0-56
- Merge patches back into git repository.

* Tue Nov 8 2011 Dan Walsh <dwalsh@redhat.com> 3.10.0-55.2
- Remove allow_execmem boolean and replace with deny_execmem boolean

* Tue Nov 8 2011 Dan Walsh <dwalsh@redhat.com> 3.10.0-55.1
- Turn back on allow_execmem boolean

* Mon Nov 7 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-55
- Add more MCS fixes to make sandbox working
- Make faillog MLS trusted to make sudo_$1_t working
- Allow sandbox_web_client_t to read passwd_file_t
- Add .mailrc file context
- Remove execheap from openoffice domain
- Allow chrome_sandbox_nacl_t to read cpu_info
- Allow virtd to relabel generic usb which is need if USB device
- Fixes for virt.if interfaces to consider chr_file as image file type

* Fri Nov 4 2011 Dan Walsh <dwalsh@redhat.com> 3.10.0-54.1
- Remove Open Office policy
- Remove execmem policy

* Fri Nov 4 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-54
- MCS fixes
- quota fixes

* Thu Nov 3 2011 Dan Walsh <dwalsh@redhat.com> 3.10.0-53.1
- Remove transitions to consoletype

* Tue Nov 1 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-53
- Make nvidia* to be labeled correctly
- Fix abrt_manage_cache() interface
- Make filetrans rules optional so base policy will build
- Dontaudit chkpwd_t access to inherited TTYS
- Make sure postfix content gets created with the correct label
- Allow gnomeclock to read cgroup
- Fixes for cloudform policy

* Thu Oct 27 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-52
- Check in fixed for Chrome nacl support

* Thu Oct 27 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-51
-  Begin removing qemu_t domain, we really no longer need this domain.  
- systemd_passwd needs dac_overide to communicate with users TTY's
- Allow svirt_lxc domains to send kill signals within their container

* Thu Oct 27 2011 Dan Walsh <dwalsh@redhat.com> 3.10.0-50.2
- Remove qemu.pp again without causing a crash

* Wed Oct 26 2011 Dan Walsh <dwalsh@redhat.com> 3.10.0-50.1
- Remove qemu.pp, everything should use svirt_t or stay in its current domain	

* Wed Oct 26 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-50
- Allow policykit to talk to the systemd via dbus
- Move chrome_sandbox_nacl_t to permissive domains
- Additional rules for chrome_sandbox_nacl

* Tue Oct 25 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-49
- Change bootstrap name to nacl
- Chrome still needs execmem
- Missing role for chrome_sandbox_bootstrap
- Add boolean to remove execmem and execstack from virtual machines
- Dontaudit xdm_t doing an access_check on etc_t directories

* Mon Oct 24 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-48
- Allow named to connect to dirsrv by default
- add ldapmap1_0 as a krb5_host_rcache_t file
- Google chrome developers asked me to add bootstrap policy for nacl stuff
- Allow rhev_agentd_t to getattr on mountpoints
- Postfix_smtpd_t needs access to milters and cleanup seems to read/write postfix_smtpd_t unix_stream_sockets

* Mon Oct 24 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-47
- Fixes for cloudform policies which need to connect to random ports
- Make sure if an admin creates modules content it creates them with the correct label
- Add port 8953 as a dns port used by unbound
- Fix file name transition for alsa and confined users

* Fri Oct 21 2011 Dan Walsh <dwalsh@redhat.com> 3.10.0-46.1
- Turn on mock_t and thumb_t for unconfined domains

* Fri Oct 21 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-46
- Policy update should not modify local contexts

* Thu Oct 20 2011 Dan Walsh <dwalsh@redhat.com> 3.10.0-45.1
- Remove ada policy

* Thu Oct 20 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-45
- Remove tzdata policy
- Add labeling for udev
- Add cloudform policy
- Fixes for bootloader policy

* Wed Oct 19 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-43
- Add policies for nova openstack

* Tue Oct 18 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-42
- Add fixes for nova-stack policy

* Tue Oct 18 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-41
- Allow svirt_lxc_domain to chr_file and blk_file devices if they are in the domain
- Allow init process to setrlimit on itself
- Take away transition rules for users executing ssh-keygen
- Allow setroubleshoot_fixit_t to read /dev/urand
- Allow sshd to relbale tunnel sockets
- Allow fail2ban domtrans to shorewall in the same way as with iptables
- Add support for lnk files in the /var/lib/sssd directory
- Allow system mail to connect to courier-authdaemon over an unix stream socket

* Mon Oct 17 2011 Dan Walsh <dwalsh@redhat.com> 3.10.0-40.2
- Add passwd_file_t for /etc/ptmptmp

* Fri Oct 14 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-40
- Dontaudit access checks for all executables, gnome-shell is doing access(EXEC, X_OK)
- Make corosync to be able to relabelto cluster lib fies
- Allow samba domains to search /var/run/nmbd
- Allow dirsrv to use pam
- Allow thumb to call getuid
- chrome less likely to get mmap_zero bug so removing dontaudit
- gimp help-browser has built in javascript
- Best guess is that devices named /dev/bsr4096 should be labeled as cpu_device_t
- Re-write glance policy

* Thu Oct 13 2011 Dan Walsh <dwalsh@redhat.com> 3.10.0-39.3
- Move dontaudit sys_ptrace line from permissive.te to domain.te
- Remove policy for hal, it no longer exists

* Wed Oct 12 2011 Dan Walsh <dwalsh@redhat.com> 3.10.0-39.2
- Don't check md5 size or mtime on certain config files

* Tue Oct 11 2011 Dan Walsh <dwalsh@redhat.com> 3.10.0-39.1
- Remove allow_ptrace and replace it with deny_ptrace, which will remove all 
ptrace from the system
- Remove 2000 dontaudit rules between confined domains on transition
and replace with single
dontaudit domain domain:process { noatsecure siginh rlimitinh } ;

* Mon Oct 10 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-39
- Fixes for bootloader policy
- $1_gkeyringd_t needs to read $HOME/%USER/.local/share/keystore
- Allow nsplugin to read /usr/share/config
- Allow sa-update to update rules
- Add use_fusefs_home_dirs for chroot ssh option
- Fixes for grub2
- Update systemd_exec_systemctl() interface
- Allow gpg to read the mail spool
- More fixes for sa-update running out of cron job
- Allow ipsec_mgmt_t to read hardware state information
- Allow pptp_t to connect to unreserved_port_t
- Dontaudit getattr on initctl in /dev from chfn
- Dontaudit getattr on kernel_core from chfn
- Add systemd_list_unit_dirs to systemd_exec_systemctl call
- Fixes for collectd policy
- CHange sysadm_t to create content as user_tmp_t under /tmp

* Thu Oct 6 2011 Dan Walsh <dwalsh@redhat.com> 3.10.0-38.1
- Shrink size of policy through use of attributes for userdomain and apache

* Wed Oct 5 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-38
- Allow virsh to read xenstored pid file
- Backport corenetwork fixes from upstream
- Do not audit attempts by thumb to search config_home_t dirs (~/.config)
- label ~/.cache/telepathy/logger telepathy_logger_cache_home_t
- allow thumb to read generic data home files (mime.type)

* Wed Oct 5 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-37
- Allow nmbd to manage sock file in /var/run/nmbd
- ricci_modservice send syslog msgs
- Stop transitioning from unconfined_t to ldconfig_t, but make sure /etc/ld.so.cache is labeled correctly
- Allow systemd_logind_t to manage /run/USER/dconf/user

* Tue Oct 4 2011 Dan Walsh <dwalsh@redhat.com> 3.10.0-36.1
- Fix missing patch from F16

* Mon Oct 3 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-36
- Allow logrotate setuid and setgid since logrotate is supposed to do it
- Fixes for thumb policy by grift
- Add new nfsd ports
- Added fix to allow confined apps to execmod on chrome
- Add labeling for additional vdsm directories
- Allow Exim and Dovecot SASL
- Add label for /var/run/nmbd
- Add fixes to make virsh and xen working together
- Colord executes ls
- /var/spool/cron  is now labeled as user_cron_spool_t

* Mon Oct 3 2011 Dan Walsh <dwalsh@redhat.com> 3.10.0-35
- Stop complaining about leaked file descriptors during install

* Fri Sep 30 2011 Dan Walsh <dwalsh@redhat.com> 3.10.0-34.7
- Remove java and mono module and merge into execmem

* Fri Sep 30 2011 Dan Walsh <dwalsh@redhat.com> 3.10.0-34.6
- Fixes for thumb policy and passwd_file_t

* Fri Sep 30 2011 Dan Walsh <dwalsh@redhat.com> 3.10.0-34.4
- Fixes caused by the labeling of /etc/passwd
- Add thumb.patch to transition unconfined_t to thumb_t for Rawhide

* Thu Sep 29 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-34.3
- Add support for Clustered Samba commands
- Allow ricci_modrpm_t to send log msgs
- move permissive virt_qmf_t from virt.te to permissivedomains.te
- Allow ssh_t to use kernel keyrings
- Add policy for libvirt-qmf and more fixes for linux containers
- Initial Polipo
- Sanlock needs to run ranged in order to kill svirt processes
- Allow smbcontrol to stream connect to ctdbd

* Mon Sep 26 2011 Dan Walsh <dwalsh@redhat.com> 3.10.0-34.2
- Add label for /etc/passwd

* Mon Sep 26 2011 Dan Walsh <dwalsh@redhat.com> 3.10.0-34.1
- Change unconfined_domains to permissive for Rawhide
- Add definition for the ephemeral_ports

* Mon Sep 26 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-34
- Make mta_role() active
- Allow asterisk to connect to jabber client port
- Allow procmail to read utmp
- Add NIS support for systemd_logind_t
- Allow systemd_logind_t to manage /run/user/$USER/dconf dir which is labeled as config_home_t
- Fix systemd_manage_unit_dirs() interface
- Allow ssh_t to manage directories passed into it
- init needs to be able to create and delete unit file directories
- Fix typo in apache_exec_sys_script
- Add ability for logrotate to transition to awstat domain

* Fri Sep 23 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-33
- Change screen to use screen_domain attribute and allow screen_domains to read all process domain state
- Add SELinux support for ssh pre-auth net process in F17
- Add logging_syslogd_can_sendmail boolean

* Wed Sep 21 2011 Dan Walsh <dwalsh@redhat.com> 3.10.0-31.1
- Add definition for ephemeral ports
- Define user_tty_device_t as a customizable_type

* Tue Sep 20 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-31
- Needs to require a new version of checkpolicy
- Interface fixes

* Fri Sep 16 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-29
- Allow sanlock to manage virt lib files
- Add virt_use_sanlock booelan
- ksmtuned is trying to resolve uids
- Make sure .gvfs is labeled user_home_t in the users home directory
- Sanlock sends kill signals and needs the kill capability
- Allow mockbuild to work on nfs homedirs
- Fix kerberos_manage_host_rcache() interface
- Allow exim to read system state

* Tue Sep 13 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-28
- Allow systemd-tmpfiles to set the correct labels on /var/run, /tmp and other files
- We want any file type that is created in /tmp by a process running as initrc_t to be labeled initrc_tmp_t

* Tue Sep 13 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-27
-  Allow collectd to read hardware state information
- Add loop_control_device_t
- Allow mdadm to request kernel to load module
- Allow domains that start other domains via systemctl to search unit dir
- systemd_tmpfiles, needs to list any file systems mounted on /tmp
- No one can explain why radius is listing the contents of /tmp, so we will dontaudit
- If I can manage etc_runtime files, I should be able to read the links
- Dontaudit hostname writing to mock library chr_files
- Have gdm_t setup labeling correctly in users home dir
- Label content unde /var/run/user/NAME/dconf as config_home_t
- Allow sa-update to execute shell
- Make ssh-keygen working with fips_enabled
- Make mock work for staff_t user
- Tighten security on mock_t

* Fri Sep 9 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-26
- removing unconfined_notrans_t no longer necessary
- Clean up handling of secure_mode_insmod and secure_mode_policyload
- Remove unconfined_mount_t

* Tue Sep 6 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-25
- Add exim_exec_t label for /usr/sbin/exim_tidydb
- Call init_dontaudit_rw_stream_socket() interface in mta policy
- sssd need to search /var/cache/krb5rcache directory
- Allow corosync to relabel own tmp files
- Allow zarafa domains to send system log messages
- Allow ssh to do tunneling
- Allow initrc scripts to sendto init_t unix_stream_socket
- Changes to make sure dmsmasq and virt directories are labeled correctly
- Changes needed to allow sysadm_t to manage systemd unit files
- init is passing file descriptors to dbus and on to system daemons
- Allow sulogin additional access Reported by dgrift and Jeremy Miller
- Steve Grubb believes that wireshark does not need this access
- Fix /var/run/initramfs to stop restorecon from looking at
- pki needs another port
- Add more labels for cluster scripts
- Allow apps that manage cgroup_files to manage cgroup link files
- Fix label on nfs-utils scripts directories
- Allow gatherd to read /dev/rand and /dev/urand

* Wed Aug 31 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-24
- pki needs another port
- Add more labels for cluster scripts
- Fix label on nfs-utils scripts directories
- Fixes for cluster
- Allow gatherd to read /dev/rand and /dev/urand
- abrt leaks fifo files

* Tue Aug 30 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-23
- Add glance policy
- Allow mdadm setsched
- /var/run/initramfs should not be relabeled with a restorecon run
- memcache can be setup to override sys_resource
- Allow httpd_t to read tetex data
- Allow systemd_tmpfiles to delete kernel modules left in /tmp directory.

* Mon Aug 29 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-22
- Allow Postfix to deliver to Dovecot LMTP socket
- Ignore bogus sys_module for lldpad
- Allow chrony and gpsd to send dgrams, gpsd needs to write to the real time clock
- systemd_logind_t sets the attributes on usb devices
- Allow hddtemp_t to read etc_t files
- Add permissivedomains module
- Move all permissive domains calls to permissivedomain.te
- Allow pegasis to send kill signals to other UIDs

* Wed Aug 24 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-21
- Allow insmod_t to use fds leaked from devicekit
- dontaudit getattr between insmod_t and init_t unix_stream_sockets
- Change sysctl unit file interfaces to use systemctl
- Add support for chronyd unit file
- Allow mozilla_plugin to read gnome_usr_config
- Add policy for new gpsd
- Allow cups to create kerberos rhost cache files
- Add authlogin_filetrans_named_content, to unconfined_t to make sure shadow and other log files get labeled correctly

* Tue Aug 23 2011 Dan Walsh <dwalsh@redhat.com> 3.10.0-20
- Make users_extra and seusers.final into config(noreplace) so semanage users and login does not get overwritten

* Tue Aug 23 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-19
- Add policy for sa-update being run out of cron jobs
- Add create perms to postgresql_manage_db
- ntpd using a gps has to be able to read/write generic tty_device_t
- If you disable unconfined and unconfineduser, rpm needs more privs to manage /dev
- fix spec file
- Remove qemu_domtrans_unconfined() interface
- Make passenger working together with puppet
- Add init_dontaudit_rw_stream_socket interface
- Fixes for wordpress

* Thu Aug 11 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-18
- Turn on allow_domain_fd_use boolean on F16
- Allow syslog to manage all log files
- Add use_fusefs_home_dirs boolean for chrome
- Make vdagent working with confined users
- Add abrt_handle_event_t domain for ABRT event scripts
- Labeled /usr/sbin/rhnreg_ks as rpm_exec_t and added changes related to this change
- Allow httpd_git_script_t to read passwd data
- Allow openvpn to set its process priority when the nice parameter is used

* Wed Aug 10 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-17
- livecd fixes
- spec file fixes 

* Thu Aug 4 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-16
- fetchmail can use kerberos
- ksmtuned reads in shell programs
- gnome_systemctl_t reads the process state of ntp
- dnsmasq_t asks the kernel to load multiple kernel modules
- Add rules for domains executing systemctl
- Bogus text within fc file

* Wed Aug 3 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-14
- Add cfengine policy

* Tue Aug 2 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-13
- Add abrt_domain attribute
- Allow corosync to manage cluster lib files
- Allow corosync to connect to the system DBUS

* Mon Aug 1 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-12
- Add sblim, uuidd policies
- Allow kernel_t dyntrasition to init_t

* Fri Jul 29 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-11
- init_t need setexec
- More fixes of rules which cause an explosion in rules by Dan Walsh

* Tue Jul 26 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-10
- Allow rcsmcertd to perform DNS name resolution
- Add dirsrvadmin_unconfined_script_t domain type for 389-ds admin scripts
- Allow tmux to run as screen
- New policy for collectd
- Allow gkeyring_t to interact with all user apps
- Add rules to allow firstboot to run on machines with the unconfined.pp module removed

* Sat Jul 23 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-9
- Allow systemd_logind to send dbus messages with users
- allow accountsd to read wtmp file
- Allow dhcpd to get and set capabilities

* Fri Jul 22 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-8
- Fix oracledb_port definition
- Allow mount to mounton the selinux file system
- Allow users to list /var directories

* Thu Jul 21 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-7
- systemd fixes

* Tue Jul 19 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-6
- Add initial policy for abrt_dump_oops_t
- xtables-multi wants to getattr of the proc fs
- Smoltclient is connecting to abrt
- Dontaudit leaked file descriptors to postdrop
- Allow abrt_dump_oops to look at kernel sysctls
- Abrt_dump_oops_t reads kernel ring buffer
- Allow mysqld to request the kernel to load modules
- systemd-login needs fowner
- Allow postfix_cleanup_t to searh maildrop

* Mon Jul 18 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-5
- Initial systemd_logind policy
- Add policy for systemd_logger and additional proivs for systemd_logind
- More fixes for systemd policies

* Thu Jul 14 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-4
- Allow setsched for virsh
- Systemd needs to impersonate cups, which means it needs to create tcp_sockets in cups_t domain, as well as manage spool directories
- iptables: the various /sbin/ip6?tables.* are now symlinks for
/sbin/xtables-multi

* Tue Jul 12 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-3
- A lot of users are running yum -y update while in /root which is causing ldconfig to list the contents, adding dontaudit
- Allow colord to interact with the users through the tmpfs file system
- Since we changed the label on deferred, we need to allow postfix_qmgr_t to be able to create maildrop_t files
- Add label for /var/log/mcelog
- Allow asterisk to read /dev/random if it uses TLS
- Allow colord to read ini files which are labeled as bin_t
- Allow dirsrvadmin sys_resource and setrlimit to use ulimit
- Systemd needs to be able to create sock_files for every label in /var/run directory, cupsd being the first.  
- Also lists /var and /var/spool directories
- Add openl2tpd to l2tpd policy
- qpidd is reading the sysfs file

* Thu Jun 30 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-2
- Change usbmuxd_t to dontaudit attempts to read chr_file
- Add mysld_safe_exec_t for libra domains to be able to start private mysql domains
- Allow pppd to search /var/lock dir
- Add rhsmcertd policy

* Mon Jun 27 2011 Miroslav Grepl <mgrepl@redhat.com> 3.10.0-1
- Update to upstream

* Mon Jun 27 2011 Miroslav Grepl <mgrepl@redhat.com> 3.9.16-30
- More fixes
  * http://git.fedorahosted.org/git/?p=selinux-policy.git

* Thu Jun 16 2011 Dan Walsh <dwalsh@redhat.com> 3.9.16-29.1
- Fix spec file to not report Verify errors

* Thu Jun 16 2011 Miroslav Grepl <mgrepl@redhat.com> 3.9.16-29
- Add dspam policy
- Add lldpad policy
- dovecot auth wants to search statfs #713555
- Allow systemd passwd apps to read init fifo_file
- Allow prelink to use inherited terminals
- Run cherokee in the httpd_t domain
- Allow mcs constraints on node connections
- Implement pyicqt policy
- Fixes for zarafa policy
- Allow cobblerd to send syslog messages

* Wed Jun 8 2011 Dan Walsh <dwalsh@redhat.com> 3.9.16-28.1
- Add policy.26 to the payload
- Remove olpc stuff
- Remove policygentool

* Wed Jun 8 2011 Miroslav Grepl <mgrepl@redhat.com> 3.9.16-27
- Fixes for zabbix
- init script needs to be able to manage sanlock_var_run_...
- Allow sandlock and wdmd to create /var/run directories... 
- mixclip.so has been compiled correctly
- Fix passenger policy module name

* Tue Jun 7 2011 Miroslav Grepl <mgrepl@redhat.com> 3.9.16-26
- Add mailscanner policy from dgrift
- Allow chrome to optionally be transitioned to
- Zabbix needs these rules when starting the zabbix_server_mysql
- Implement a type for freedesktop openicc standard (~/.local/share/icc)
- Allow system_dbusd_t to read inherited icc_data_home_t files.
- Allow colord_t to read icc_data_home_t content. #706975
- Label stuff under /usr/lib/debug as if it was labeled under /

* Thu Jun 2 2011 Miroslav Grepl <mgrepl@redhat.com> 3.9.16-25
- Fixes for sanlock policy
- Fixes for colord policy
- Other fixes
	* http://git.fedorahosted.org/git/?p=selinux-policy.git;a=log

* Thu May 26 2011 Miroslav Grepl <mgrepl@redhat.com> 3.9.16-24
- Add rhev policy module to modules-targeted.conf

* Tue May 24 2011 Miroslav Grepl <mgrepl@redhat.com> 3.9.16-23
- Lot of fixes
	* http://git.fedorahosted.org/git/?p=selinux-policy.git;a=log

* Thu May 19 2011 Miroslav Grepl <mgrepl@redhat.com> 3.9.16-22
- Allow logrotate to execute systemctl
- Allow nsplugin_t to getattr on gpmctl
- Fix dev_getattr_all_chr_files() interface
- Allow shorewall to use inherited terms
- Allow userhelper to getattr all chr_file devices
- sandbox domains should be able to getattr and dontaudit search of sysctl_kernel_t
- Fix labeling for ABRT Retrace Server

* Mon May 9 2011 Miroslav Grepl <mgrepl@redhat.com> 3.9.16-21
- Dontaudit sys_module for ifconfig
- Make telepathy and gkeyringd daemon working with confined users
- colord wants to read files in users homedir
- Remote login should be creating user_tmp_t not its own tmp files

* Thu May 5 2011 Miroslav Grepl <mgrepl@redhat.com> 3.9.16-20
- Fix label for /usr/share/munin/plugins/munin_* plugins
- Add support for zarafa-indexer
- Fix boolean description
- Allow colord to getattr on /proc/scsi/scsi
- Add label for /lib/upstart/init
- Colord needs to list /mnt

* Tue May 3 2011 Miroslav Grepl <mgrepl@redhat.com> 3.9.16-19
- Forard port changes from F15 for telepathy
- NetworkManager should be allowed to use /dev/rfkill
- Fix dontaudit messages to say Domain to not audit
- Allow telepathy domains to read/write gnome_cache files
- Allow telepathy domains to call getpw
- Fixes for colord and vnstatd policy

* Wed Apr 27 2011 Miroslav Grepl <mgrepl@redhat.com> 3.9.16-18
- Allow init_t getcap and setcap
- Allow namespace_init_t to use nsswitch
- aisexec will execute corosync
- colord tries to read files off noxattr file systems
- Allow init_t getcap and setcap

* Thu Apr 21 2011 Miroslav Grepl <mgrepl@redhat.com> 3.9.16-17
- Add support for ABRT retrace server
- Allow user_t and staff_t access to generic scsi to handle locally plugged in scanners
- Allow telepath_msn_t to read /proc/PARENT/cmdline
- ftpd needs kill capability
- Allow telepath_msn_t to connect to sip port
- keyring daemon does not work on nfs homedirs
- Allow $1_sudo_t to read default SELinux context
- Add label for tgtd sock file in /var/run/
- Add apache_exec_rotatelogs interface
- allow all zaraha domains to signal themselves, server writes to /tmp
- Allow syslog to read the process state
- Add label for /usr/lib/chromium-browser/chrome
- Remove the telepathy transition from unconfined_t
- Dontaudit sandbox domains trying to mounton sandbox_file_t, this is caused by fuse mounts
- Allow initrc_t domain to manage abrt pid files
- Add support for AEOLUS project
- Virt_admin should be allowed to manage images and processes
- Allow plymountd to send signals to init
- Change labeling of fping6

* Tue Apr 19 2011 Dan Walsh <dwalsh@redhat.com> 3.9.16-16.1
- Add filename transitions

* Tue Apr 19 2011 Miroslav Grepl <mgrepl@redhat.com> 3.9.16-16
- Fixes for zarafa policy
- Add support for AEOLUS project
- Change labeling of fping6
- Allow plymountd to send signals to init
- Allow initrc_t domain to manage abrt pid files
- Virt_admin should be allowed to manage images and processes

* Fri Apr 15 2011 Miroslav Grepl <mgrepl@redhat.com> 3.9.16-15
- xdm_t needs getsession for switch user 
- Every app that used to exec init is now execing systemdctl 
- Allow squid to manage krb5_host_rcache_t files 
- Allow foghorn to connect to agentx port - Fixes for colord policy

* Mon Apr 11 2011 Miroslav Grepl <mgrepl@redhat.com> 3.9.16-14
- Add Dan's patch to remove 64 bit variants
- Allow colord to use unix_dgram_socket 
- Allow apps that search pids to read /var/run if it is a lnk_file 
- iscsid_t creates its own directory 
- Allow init to list var_lock_t dir 
- apm needs to verify user accounts auth_use_nsswitch
- Add labeling for systemd unit files
- Allow gnomeclok to enable ntpd service using systemctl - systemd_systemctl_t domain was added
- Add label for matahari-broker.pid file
- We want to remove untrustedmcsprocess from ability to read /proc/pid
- Fixes for matahari policy
- Allow system_tmpfiles_t to delete user_home_t files in the /tmp dir
- Allow sshd to transition to sysadm_t if ssh_sysadm_login is turned on

* Tue Apr 5 2011 Miroslav Grepl <mgrepl@redhat.com> 3.9.16-13
- Fix typo

* Mon Apr 4 2011 Miroslav Grepl <mgrepl@redhat.com> 3.9.16-12
- Add /var/run/lock /var/lock definition to file_contexts.subs
- nslcd_t is looking for kerberos cc files
- SSH_USE_STRONG_RNG is 1 which requires /dev/random
- Fix auth_rw_faillog definition
- Allow sysadm_t to set attributes on fixed disks
- allow user domains to execute lsof and look at application sockets
- prelink_cron job calls telinit -u if init is rewritten
- Fixes to run qemu_t from staff_t

* Mon Apr 4 2011 Miroslav Grepl <mgrepl@redhat.com> 3.9.16-11
- Fix label for /var/run/udev to udev_var_run_t
- Mock needs to be able to read network state

* Fri Apr 1 2011 Miroslav Grepl <mgrepl@redhat.com> 3.9.16-10
- Add file_contexts.subs to handle /run and /run/lock
- Add other fixes relating to /run changes from F15 policy

* Fri Mar 25 2011 Miroslav Grepl <mgrepl@redhat.com> 3.9.16-7
- Allow $1_sudo_t and $1_su_t open access to user terminals
- Allow initrc_t to use generic terminals
- Make Makefile/Rules.modular run sepolgen-ifgen during build to check if files for bugs
-systemd is going to be useing /run and /run/lock for early bootup files.
- Fix some comments in rlogin.if
- Add policy for KDE backlighthelper
- sssd needs to read ~/.k5login in nfs, cifs or fusefs file systems
- sssd wants to read .k5login file in users homedir
- setroubleshoot reads executables to see if they have TEXTREL
- Add /var/spool/audit support for new version of audit
- Remove kerberos_connect_524() interface calling
- Combine kerberos_master_port_t and kerberos_port_t
- systemd has setup /dev/kmsg as stderr for apps it executes
- Need these access so that init can impersonate sockets on unix_dgram_socket

* Wed Mar 23 2011 Miroslav Grepl <mgrepl@redhat.com> 3.9.16-6
- Remove some unconfined domains
- Remove permissive domains
- Add policy-term.patch from Dan 

* Thu Mar 17 2011 Miroslav Grepl <mgrepl@redhat.com> 3.9.16-5
- Fix multiple specification for boot.log
- devicekit leaks file descriptors to setfiles_t
- Change all all_nodes to generic_node and all_if to generic_if
- Should not use deprecated interface
- Switch from using all_nodes to generic_node and from all_if to generic_if
- Add support for xfce4-notifyd
- Fix file context to show several labels as SystemHigh
- seunshare needs to be able to mounton nfs/cifs/fusefs homedirs
- Add etc_runtime_t label for /etc/securetty
- Fixes to allow xdm_t to start gkeyringd_USERTYPE_t directly
- login.krb needs to be able to write user_tmp_t
- dirsrv needs to bind to port 7390 for dogtag
- Fix a bug in gpg policy
- gpg sends audit messages
- Allow qpid to manage matahari files

* Tue Mar 15 2011 Miroslav Grepl <mgrepl@redhat.com> 3.9.16-4
- Initial policy for matahari
- Add dev_read_watchdog
- Allow clamd to connect clamd port
- Add support for kcmdatetimehelper
- Allow shutdown to setrlimit and sys_nice
- Allow systemd_passwd to talk to /dev/log before udev or syslog is running
- Purge chr_file and blk files on /tmp
- Fixes for pads
- Fixes for piranha-pulse
- gpg_t needs to be able to encyprt anything owned by the user

* Thu Mar 10 2011 Miroslav Grepl <mgrepl@redhat.com> 3.9.16-3
- mozilla_plugin_tmp_t needs to be treated as user tmp files
- More dontaudits of writes from readahead
- Dontaudit readahead_t file_type:dir write, to cover up kernel bug
- systemd_tmpfiles needs to relabel faillog directory as well as the file
- Allow hostname and consoletype to r/w inherited initrc_tmp_t files handline hostname >> /tmp/myhost

* Thu Mar 10 2011 Miroslav Grepl <mgrepl@redhat.com> 3.9.16-2
- Add policykit fixes from Tim Waugh
- dontaudit sandbox domains sandbox_file_t:dir mounton
- Add new dontaudit rules for sysadm_dbusd_t
- Change label for /var/run/faillock
	* other fixes which relate with this change

* Tue Mar 8 2011 Miroslav Grepl <mgrepl@redhat.com> 3.9.16-1
- Update to upstream
- Fixes for telepathy
- Add port defition for ssdp port
- add policy for /bin/systemd-notify from Dan
- Mount command requires users read mount_var_run_t
- colord needs to read konject_uevent_socket
- User domains connect to the gkeyring socket
- Add colord policy and allow user_t and staff_t to dbus chat with it
- Add lvm_exec_t label for kpartx
- Dontaudit reading the mail_spool_t link from sandbox -X
- systemd is creating sockets in avahi_var_run and system_dbusd_var_run

* Tue Mar 1 2011 Miroslav Grepl <mgrepl@redhat.com> 3.9.15-5
- gpg_t needs to talk to gnome-keyring
- nscd wants to read /usr/tmp->/var/tmp to generate randomziation in unixchkpwd
- enforce MCS labeling on nodes
- Allow arpwatch to read meminfo
- Allow gnomeclock to send itself signals
- init relabels /dev/.udev files on boot
- gkeyringd has to transition back to staff_t when it runs commands in bin_t or shell_exec_t
- nautilus checks access on /media directory before mounting usb sticks, dontaudit access_check on mnt_t
- dnsmasq can run as a dbus service, needs acquire service
- mysql_admin should  be allowed to connect to mysql service
- virt creates monitor sockets in the users home dir

* Mon Feb 21 2011 Miroslav Grepl <mgrepl@redhat.com> 3.9.15-2
- Allow usbhid-ups to read hardware state information
- systemd-tmpfiles has moved
- Allo cgroup to sys_tty_config
- For some reason prelink is attempting to read gconf settings
- Add allow_daemons_use_tcp_wrapper boolean
- Add label for ~/.cache/wocky to make telepathy work in enforcing mode
- Add label for char devices /dev/dasd*
- Fix for apache_role
- Allow amavis to talk to nslcd
- allow all sandbox to read selinux poilcy config files
- Allow cluster domains to use the system bus and send each other dbus messages

* Wed Feb 16 2011 Miroslav Grepl <mgrepl@redhat.com> 3.9.15-1
- Update to upstream

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.9.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Feb 8 2011 Dan Walsh <dwalsh@redhat.com> 3.9.14-1
- Update to ref policy
- cgred needs chown capability
- Add /dev/crash crash_dev_t
- systemd-readahead wants to use fanotify which means readahead_t needs sys_admin capability

* Tue Feb 8 2011 Miroslav Grepl <mgrepl@redhat.com> 3.9.13-10
- New labeling for postfmulti #675654
- dontaudit xdm_t listing noxattr file systems
- dovecot-auth needs to be able to connect to mysqld via the network as well as locally
- shutdown is passed stdout to a xdm_log_t file
- smartd creates a fixed disk device
- dovecot_etc_t contains a lnk_file that domains need to read
- mount needs to be able to read etc_runtim_t:lnk_file since in rawhide this is a link created at boot

* Thu Feb 3 2011 Miroslav Grepl <mgrepl@redhat.com> 3.9.13-9
- syslog_t needs syslog capability
- dirsrv needs to be able to create /var/lib/snmp
- Fix labeling for dirsrv
- Fix for dirsrv policy missing manage_dirs_pattern
- corosync needs to delete clvm_tmpfs_t files
- qdiskd needs to list hugetlbfs
- Move setsched to sandbox_x_domain, so firefox can run without network access
- Allow hddtemp to read removable devices
- Adding syslog and read_policy permissions to policy
	* syslog
		Allow unconfined, sysadm_t, secadm_t, logadm_t
	* read_policy
		allow unconfined, sysadm_t, secadm_t, staff_t on Targeted
		allow sysadm_t (optionally), secadm_t on MLS
- mdadm application will write into /sys/.../uevent whenever arrays are
assembled or disassembled.

* Tue Feb 1 2011 Dan Walsh <dwalsh@redhat.com> 3.9.13-8
- Add tcsd policy

* Tue Feb 1 2011 Miroslav Grepl <mgrepl@redhat.com> 3.9.13-7
- ricci_modclusterd_t needs to bind to rpc ports 500-1023
- Allow dbus to use setrlimit to increase resoueces
- Mozilla_plugin is leaking to sandbox
- Allow confined users  to connect to lircd over unix domain stream socket which allow to use remote control
- Allow awstats to read squid logs
- seunshare needs to manage tmp_t
- apcupsd cgi scripts have a new directory

* Thu Jan 27 2011 Miroslav Grepl <mgrepl@redhat.com> 3.9.13-6
- Fix xserver_dontaudit_read_xdm_pid
- Change oracle_port_t to oracledb_port_t to prevent conflict with satellite
- Allow dovecot_deliver_t to read/write postfix_master_t:fifo_file. 
	* These fifo_file is passed from postfix_master_t to postfix_local_t to dovecot_deliver_t
- Allow readahead to manage readahead pid dirs
- Allow readahead to read all mcs levels
- Allow mozilla_plugin_t to use nfs or samba homedirs

* Tue Jan 25 2011 Miroslav Grepl <mgrepl@redhat.com> 3.9.13-5
- Allow nagios plugin to read /proc/meminfo
- Fix for mozilla_plugin
- Allow samba_net_t to create /etc/keytab
- pppd_t setting up vpns needs to run unix_chkpwd, setsched its process and write wtmp_t
- nslcd can read user credentials
- Allow nsplugin to delete mozilla_plugin_tmpfs_t
- abrt tries to create dir in rpm_var_lib_t
- virt relabels fifo_files
- sshd needs to manage content in fusefs homedir
- mock manages link files in cache dir

* Fri Jan 21 2011 Miroslav Grepl <mgrepl@redhat.com> 3.9.13-4
- nslcd needs setsched and to read /usr/tmp
- Invalid call in likewise policy ends up creating a bogus role
- Cannon puts content into /var/lib/bjlib that cups needs to be able to write
- Allow screen to create screen_home_t in /root
- dirsrv sends syslog messages
- pinentry reads stuff in .kde directory
- Add labels for .kde directory in homedir
- Treat irpinit, iprupdate, iprdump services with raid policy

* Wed Jan 19 2011 Miroslav Grepl <mgrepl@redhat.com> 3.9.13-3
- NetworkManager wants to read consolekit_var_run_t
- Allow readahead to create /dev/.systemd/readahead
- Remove permissive domains
- Allow newrole to run namespace_init

* Tue Jan 18 2011 Miroslav Grepl <mgrepl@redhat.com> 3.9.13-2
- Add sepgsql_contexts file

* Mon Jan 17 2011 Miroslav Grepl <mgrepl@redhat.com> 3.9.13-1
- Update to upstream

* Mon Jan 17 2011 Miroslav Grepl <mgrepl@redhat.com> 3.9.12-8
- Add oracle ports and allow apache to connect to them if the connect_db boolean is turned on
- Add puppetmaster_use_db boolean
- Fixes for zarafa policy
- Fixes for gnomeclock poliy
- Fix systemd-tmpfiles to use auth_use_nsswitch

* Fri Jan 14 2011 Miroslav Grepl <mgrepl@redhat.com> 3.9.12-7
- gnomeclock executes a shell
- Update for screen policy to handle pipe in homedir
- Fixes for polyinstatiated homedir
- Fixes for namespace policy and other fixes related to polyinstantiation
- Add namespace policy
- Allow dovecot-deliver transition to sendmail which is needed by sieve scripts
- Fixes for init, psad policy which relate with confined users
- Do not audit bootloader attempts to read devicekit pid files
- Allow nagios service plugins to read /proc

* Tue Jan 11 2011 Miroslav Grepl <mgrepl@redhat.com> 3.9.12-6
- Add firewalld policy
- Allow vmware_host to read samba config
- Kernel wants to read /proc Fix duplicate grub def in cobbler
- Chrony sends mail, executes shell, uses fifo_file and reads /proc
- devicekitdisk getattr all file systems
- sambd daemon writes wtmp file
- libvirt transitions to dmidecode

* Wed Jan 5 2011 Miroslav Grepl <mgrepl@redhat.com> 3.9.12-5
- Add initial policy for system-setup-keyboard which is now daemon
- Label /var/lock/subsys/shorewall as shorewall_lock_t
- Allow users to communicate with the gpg_agent_t
- Dontaudit mozilla_plugin_t using the inherited terminal
- Allow sambagui to read files in /usr
- webalizer manages squid log files
- Allow unconfined domains to bind ports to raw_ip_sockets
- Allow abrt to manage rpm logs when running yum
- Need labels for /var/run/bittlebee
- Label .ssh under amanda
- Remove unused genrequires for virt_domain_template
- Allow virt_domain to use fd inherited from virtd_t
- Allow iptables to read shorewall config

* Tue Dec 28 2010 Dan Walsh <dwalsh@redhat.com> 3.9.12-4
- Gnome apps list config_home_t
- mpd creates lnk files in homedir
- apache leaks write to mail apps on tmp files
- /var/stockmaniac/templates_cache contains log files
- Abrt list the connects of mount_tmp_t dirs
- passwd agent reads files under /dev and reads utmp file
- squid apache script connects to the squid port
- fix name of plymouth log file
- teamviewer is a wine app
- allow dmesg to read system state
- Stop labeling files under /var/lib/mock so restorecon will not go into this 
- nsplugin needs to read network state for google talk

* Thu Dec 23 2010 Dan Walsh <dwalsh@redhat.com> 3.9.12-3
- Allow xdm and syslog to use /var/log/boot.log
- Allow users to communicate with mozilla_plugin and kill it
- Add labeling for ipv6 and dhcp

* Tue Dec 21 2010 Dan Walsh <dwalsh@redhat.com> 3.9.12-2
- New labels for ghc http content
- nsplugin_config needs to read urand, lvm now calls setfscreate to create dev
- pm-suspend now creates log file for append access so we remove devicekit_wri
- Change authlogin_use_sssd to authlogin_nsswitch_use_ldap
- Fixes for greylist_milter policy

* Tue Dec 21 2010 Miroslav Grepl <mgrepl@redhat.com> 3.9.12-1
- Update to upstream
- Fixes for systemd policy
- Fixes for passenger policy
- Allow staff users to run mysqld in the staff_t domain, akonadi needs this
- Add bin_t label for /usr/share/kde4/apps/kajongg/kajongg.py
- auth_use_nsswitch does not need avahi to read passwords,needed for resolving data
- Dontaudit (xdm_t) gok attempting to list contents of /var/account
- Telepathy domains need to read urand
- Need interface to getattr all file classes in a mock library for setroubleshoot

* Wed Dec 15 2010 Dan Walsh <dwalsh@redhat.com> 3.9.11-2
- Update selinux policy to handle new /usr/share/sandbox/start script

* Wed Dec 15 2010 Miroslav Grepl <mgrepl@redhat.com> 3.9.11-1
- Update to upstream
- Fix version of policy in spec file

* Tue Dec 14 2010 Miroslav Grepl <mgrepl@redhat.com> 3.9.10-13
- Allow sandbox to run on nfs partitions, fixes for systemd_tmpfs
- remove per sandbox domains devpts types
- Allow dkim-milter sending signal to itself

* Mon Dec 13 2010 Dan Walsh <dwalsh@redhat.com> 3.9.10-12
- Allow domains that transition to ping or traceroute, kill them
- Allow user_t to conditionally transition to ping_t and traceroute_t
- Add fixes to systemd- tools, including new labeling for systemd-fsck, systemd-cryptsetup

* Mon Dec 13 2010 Miroslav Grepl <mgrepl@redhat.com> 3.9.10-11
- Turn on systemd policy
- mozilla_plugin needs to read certs in the homedir.
- Dontaudit leaked file descriptors from devicekit
- Fix ircssi to use auth_use_nsswitch
- Change to use interface without param in corenet to disable unlabelednet packets
- Allow init to relabel sockets and fifo files in /dev
- certmonger needs dac* capabilities to manage cert files not owned by root
- dovecot needs fsetid to change group membership on mail
- plymouthd removes /var/log/boot.log
- systemd is creating symlinks in /dev
- Change label on /etc/httpd/alias to be all cert_t

* Fri Dec 10 2010 Miroslav Grepl <mgrepl@redhat.com> 3.9.10-10
- Fixes for clamscan and boinc policy
- Add boinc_project_t setpgid
- Allow alsa to create tmp files in /tmp

* Tue Dec 7 2010 Miroslav Grepl <mgrepl@redhat.com> 3.9.10-9
- Push fixes to allow disabling of unlabeled_t packet access
- Enable unlabelednet policy

* Tue Dec 7 2010 Miroslav Grepl <mgrepl@redhat.com> 3.9.10-8
- Fixes for lvm to work with systemd

* Mon Dec 6 2010 Miroslav Grepl <mgrepl@redhat.com> 3.9.10-7
- Fix the label for wicd log
- plymouthd creates force-display-on-active-vt file
- Allow avahi to request the kernel to load a module
- Dontaudit hal leaks
- Fix gnome_manage_data interface
- Add new interface corenet_packet to define a type as being an packet_type.
- Removed general access to packet_type from icecast and squid.
- Allow mpd to read alsa config
- Fix the label for wicd log
- Add systemd policy

* Fri Dec 3 2010 Miroslav Grepl <mgrepl@redhat.com> 3.9.10-6
- Fix gnome_manage_data interface
- Dontaudit sys_ptrace capability for iscsid
- Fixes for nagios plugin policy

* Thu Dec 2 2010 Miroslav Grepl <mgrepl@redhat.com> 3.9.10-5
- Fix cron to run ranged when started by init
- Fix devicekit to use log files
- Dontaudit use of devicekit_var_run_t for fstools
- Allow init to setattr on logfile directories
- Allow hald to manage files in /var/run/pm-utils/ dir which is now labeled as devicekit_var_run_t

* Tue Nov 30 2010 Dan Walsh <dwalsh@redhat.com> 3.9.10-4
- Fix up handling of dnsmasq_t creating /var/run/libvirt/network
- Turn on sshd_forward_ports boolean by default
- Allow sysadmin to dbus chat with rpm
- Add interface for rw_tpm_dev
- Allow cron to execute bin
- fsadm needs to write sysfs
- Dontaudit consoletype reading /var/run/pm-utils
- Lots of new privs fro mozilla_plugin_t running java app, make mozilla_plugin
- certmonger needs to manage dirsrv data
- /var/run/pm-utils should be labeled as devicekit_var_run_t

* Tue Nov 30 2010 Miroslav Grepl <mgrepl@redhat.com> 3.9.10-3
- fixes to allow /var/run and /var/lock as tmpfs
- Allow chrome sandbox to connect to web ports
- Allow dovecot to listem on lmtp and sieve ports
- Allov ddclient to search sysctl_net_t
- Transition back to original domain if you execute the shell

* Thu Nov 25 2010 Miroslav Grepl <mgrepl@redhat.com> 3.9.10-2
- Remove duplicate declaration

* Thu Nov 25 2010 Miroslav Grepl <mgrepl@redhat.com> 3.9.10-1
- Update to upstream
- Cleanup for sandbox
- Add attribute to be able to select sandbox types

* Mon Nov 22 2010 Miroslav Grepl <mgrepl@redhat.com> 3.9.9-4
- Allow ddclient to fix file mode bits of ddclient conf file
- init leaks file descriptors to daemons
- Add labels for /etc/lirc/ and
- Allow amavis_t to exec shell
- Add label for gssd_tmp_t for /var/tmp/nfs_0

* Thu Nov 18 2010 Dan Walsh <dwalsh@redhat.com> 3.9.9-3
- Put back in lircd_etc_t so policy will install

* Thu Nov 18 2010 Miroslav Grepl <mgrepl@redhat.com> 3.9.9-2
- Turn on allow_postfix_local_write_mail_spool
- Allow initrc_t to transition to shutdown_t
- Allow logwatch and cron to mls_read_to_clearance for MLS boxes
- Allow wm to send signull to all applications and receive them from users
- lircd patch from field
- Login programs have to read /etc/samba
- New programs under /lib/systemd
- Abrt needs to read config files

* Tue Nov 16 2010 Miroslav Grepl <mgrepl@redhat.com> 3.9.9-1
- Update to upstream
- Dontaudit leaked sockets from userdomains to user domains
- Fixes for mcelog to handle scripts
- Apply patch from Ruben Kerkhof
- Allow syslog to search spool dirs

* Mon Nov 15 2010 Miroslav Grepl <mgrepl@redhat.com> 3.9.8-7
- Allow nagios plugins to read usr files
- Allow mysqld-safe to send system log messages
- Fixes fpr ddclient policy
- Fix sasl_admin interface
- Allow apache to search zarafa config
- Allow munin plugins to search /var/lib directory
- Allow gpsd to read sysfs_t
- Fix labels on /etc/mcelog/triggers to bin_t

* Fri Nov 12 2010 Dan Walsh <dwalsh@redhat.com> 3.9.8-6
- Remove saslauthd_tmp_t and transition tmp files to krb5_host_rcache_t
- Allow saslauthd_t to create krb5_host_rcache_t files in /tmp
- Fix xserver interface
- Fix definition of /var/run/lxdm

* Fri Nov 12 2010 Miroslav Grepl <mgrepl@redhat.com> 3.9.8-5
- Turn on mediawiki policy
- kdump leaks kdump_etc_t to ifconfig, add dontaudit
- uux needs to transition to uucpd_t
- More init fixes relabels man,faillog
- Remove maxima defs in libraries.fc
- insmod needs to be able to create tmpfs_t files
- ping needs setcap

* Wed Nov 10 2010 Miroslav Grepl <mgrepl@redhat.com> 3.9.8-4
- Allow groupd transition to fenced domain when executes fence_node
- Fixes for rchs policy
- Allow mpd to be able to read samba/nfs files

* Tue Nov 9 2010 Dan Walsh <dwalsh@redhat.com> 3.9.8-3
- Fix up corecommands.fc to match upstream
- Make sure /lib/systemd/* is labeled init_exec_t
- mount wants to setattr on all mountpoints
- dovecot auth wants to read dovecot etc files
- nscd daemon looks at the exe file of the comunicating daemon
- openvpn wants to read utmp file
- postfix apps now set sys_nice and lower limits
- remote_login (telnetd/login) wants to use telnetd_devpts_t and user_devpts_t to work correctly
- Also resolves nsswitch
- Fix labels on /etc/hosts.*
- Cleanup to make upsteam patch work
- allow abrt to read etc_runtime_t

* Fri Nov 5 2010 Dan Walsh <dwalsh@redhat.com> 3.9.8-2
- Add conflicts for dirsrv package

* Fri Nov 5 2010 Dan Walsh <dwalsh@redhat.com> 3.9.8-1
- Update to upstream
- Add vlock policy

* Wed Nov 3 2010 Dan Walsh <dwalsh@redhat.com> 3.9.7-10
- Fix sandbox to work on nfs homedirs
- Allow cdrecord to setrlimit
- Allow mozilla_plugin to read xauth
- Change label on systemd-logger to syslogd_exec_t
- Install dirsrv policy from dirsrv package

* Tue Nov 2 2010 Dan Walsh <dwalsh@redhat.com> 3.9.7-9
- Add virt_home_t, allow init to setattr on xserver_tmp_t and relabel it
- Udev needs to stream connect to init and kernel
- Add xdm_exec_bootloader boolean, which allows xdm to execute /sbin/grub and read files in /boot directory

* Mon Nov 1 2010 Dan Walsh <dwalsh@redhat.com> 3.9.7-8
- Allow NetworkManager to read openvpn_etc_t
- Dontaudit hplip to write of /usr dirs
- Allow system_mail_t to create /root/dead.letter as mail_home_t
- Add vdagent policy for spice agent daemon

* Thu Oct 28 2010 Dan Walsh <dwalsh@redhat.com> 3.9.7-7
- Dontaudit sandbox sending sigkill to all user domains
- Add policy for rssh_chroot_helper
- Add missing flask definitions
- Allow udev to relabelto removable_t
- Fix label on /var/log/wicd.log
- Transition to initrc_t from init when executing bin_t
- Add audit_access permissions to file
- Make removable_t a device_node 
- Fix label on /lib/systemd/*

* Fri Oct 22 2010 Dan Walsh <dwalsh@redhat.com> 3.9.7-6
- Fixes for systemd to manage /var/run
- Dontaudit leaks by firstboot

* Tue Oct 19 2010 Dan Walsh <dwalsh@redhat.com> 3.9.7-5
- Allow chome to create netlink_route_socket
- Add additional MATHLAB file context
- Define nsplugin as an application_domain
- Dontaudit sending signals from sandboxed domains to other domains
- systemd requires init to build /tmp /var/auth and /var/lock dirs
- mount wants to read devicekit_power /proc/ entries
- mpd wants to connect to soundd port
- Openoffice causes a setattr on a lib_t file for normal users, add dontaudit
- Treat lib_t and textrel_shlib_t directories the same
- Allow mount read access on virtual images

* Fri Oct 15 2010 Dan Walsh <dwalsh@redhat.com> 3.9.7-4
- Allow sandbox_x_domains to work with nfs/cifs/fusefs home dirs.
- Allow devicekit_power to domtrans to mount
- Allow dhcp to bind to udp ports > 1024 to do named stuff
- Allow ssh_t to exec ssh_exec_t
- Remove telepathy_butterfly_rw_tmp_files(), dev_read_printk() interfaces which are nolonger used
- Fix clamav_append_log() intefaces
- Fix 'psad_rw_fifo_file' interface

* Fri Oct 15 2010 Dan Walsh <dwalsh@redhat.com> 3.9.7-3
- Allow cobblerd to list cobler appache content

* Fri Oct 15 2010 Dan Walsh <dwalsh@redhat.com> 3.9.7-2
- Fixup for the latest version of upowed
- Dontaudit sandbox sending SIGNULL to desktop apps

* Wed Oct 13 2010 Dan Walsh <dwalsh@redhat.com> 3.9.7-1
- Update to upstream

* Tue Oct 12 2010 Dan Walsh <dwalsh@redhat.com> 3.9.6-3
-Mount command from a confined user generates setattr on /etc/mtab file, need to dontaudit this access
- dovecot-auth_t needs ipc_lock
- gpm needs to use the user terminal
- Allow system_mail_t to append ~/dead.letter
- Allow NetworkManager to edit /etc/NetworkManager/NetworkManager.conf
- Add pid file to vnstatd
- Allow mount to communicate with gfs_controld
- Dontaudit hal leaks in setfiles

* Fri Oct 8 2010 Dan Walsh <dwalsh@redhat.com> 3.9.6-2
- Lots of fixes for systemd
- systemd now executes readahead and tmpwatch type scripts
- Needs to manage random seed

* Thu Oct 7 2010 Dan Walsh <dwalsh@redhat.com> 3.9.6-1
- Allow smbd to use sys_admin
- Remove duplicate file context for tcfmgr
- Update to upstream

* Wed Oct 6 2010 Dan Walsh <dwalsh@redhat.com> 3.9.5-11
- Fix fusefs handling
- Do not allow sandbox to manage nsplugin_rw_t
- Allow mozilla_plugin_t to connecto its parent
- Allow init_t to connect to plymouthd running as kernel_t
- Add mediawiki policy
- dontaudit sandbox sending signals to itself.  This can happen when they are running at different mcs.
- Disable transition from dbus_session_domain to telepathy for F14
- Allow boinc_project to use shm
- Allow certmonger to search through directories that contain certs
- Allow fail2ban the DAC Override so it can read log files owned by non root users

* Mon Oct 4 2010 Dan Walsh <dwalsh@redhat.com> 3.9.5-10
- Start adding support for use_fusefs_home_dirs
- Add /var/lib/syslog directory file context
- Add /etc/localtime as locale file context

* Thu Sep 30 2010 Dan Walsh <dwalsh@redhat.com> 3.9.5-9
- Turn off default transition to mozilla_plugin and telepathy domains from unconfined user 
- Turn off iptables from unconfined user 
- Allow sudo to send signals to any domains the user could have transitioned to.
- Passwd in single user mode needs to talk to console_device_t
- Mozilla_plugin_t needs to connect to web ports, needs to write to video device, and read alsa_home_t alsa setsup pulseaudio
- locate tried to read a symbolic link, will dontaudit
- New labels for telepathy-sunshine content in homedir
- Google is storing other binaries under /opt/google/talkplugin
- bluetooth/kernel is creating unlabeled_t socket that I will allow it to use until kernel fixes bug
- Add boolean for unconfined_t transition to mozilla_plugin_t and telepathy domains, turned off in F14 on in F15
- modemmanger and bluetooth send dbus messages to devicekit_power
- Samba needs to getquota on filesystems labeld samba_share_t

* Wed Sep 29 2010 Dan Walsh <dwalsh@redhat.com> 3.9.5-8
- Dontaudit attempts by xdm_t to write to bin_t for kdm
- Allow initrc_t to manage system_conf_t

* Mon Sep 27 2010 Dan Walsh <dwalsh@redhat.com> 3.9.5-7
- Fixes to allow mozilla_plugin_t to create nsplugin_home_t directory.
- Allow mozilla_plugin_t to create tcp/udp/netlink_route sockets
- Allow confined users to read xdm_etc_t files
- Allow xdm_t to transition to xauth_t for lxdm program

* Sun Sep 26 2010 Dan Walsh <dwalsh@redhat.com> 3.9.5-6
- Rearrange firewallgui policy to be more easily updated to upstream, dontaudit search of /home
- Allow clamd to send signals to itself
- Allow mozilla_plugin_t to read user home content.  And unlink pulseaudio shm.
- Allow haze to connect to yahoo chat and messenger port tcp:5050.
Bz #637339
- Allow guest to run ps command on its processes by allowing it to read /proc
- Allow firewallgui to sys_rawio which seems to be required to setup masqerading
- Allow all domains to search through default_t directories, in order to find differnet labels.  For example people serring up /foo/bar to be share via samba.
- Add label for /var/log/slim.log

* Fri Sep 24 2010 Dan Walsh <dwalsh@redhat.com> 3.9.5-5
- Pull in cleanups from dgrift
- Allow mozilla_plugin_t to execute mozilla_home_t
- Allow rpc.quota to do quotamod

* Thu Sep 23 2010 Dan Walsh <dwalsh@redhat.com> 3.9.5-4
- Cleanup policy via dgrift
- Allow dovecot_deliver to append to inherited log files
- Lots of fixes for consolehelper

* Wed Sep 22 2010 Dan Walsh <dwalsh@redhat.com> 3.9.5-3
- Fix up Xguest policy

* Thu Sep 16 2010 Dan Walsh <dwalsh@redhat.com> 3.9.5-2
- Add vnstat policy
- allow libvirt to send audit messages
- Allow chrome-sandbox to search nfs_t

* Thu Sep 16 2010 Dan Walsh <dwalsh@redhat.com> 3.9.5-1
- Update to upstream

* Wed Sep 15 2010 Dan Walsh <dwalsh@redhat.com> 3.9.4-3
- Add the ability to send audit messages to confined admin policies
- Remove permissive domain from cmirrord and dontaudit sys_tty_config
- Split out unconfined_domain() calls from other unconfined_ calls so we can d
- virt needs to be able to read processes to clearance for MLS

* Tue Sep 14 2010 Dan Walsh <dwalsh@redhat.com> 3.9.4-2
- Allow all domains that can use cgroups to search tmpfs_t directory
- Allow init to send audit messages

* Thu Sep 9 2010 Dan Walsh <dwalsh@redhat.com> 3.9.4-1
- Update to upstream

* Thu Sep 9 2010 Dan Walsh <dwalsh@redhat.com> 3.9.3-4
- Allow mdadm_t to create files and sock files in /dev/md/

* Thu Sep 9 2010 Dan Walsh <dwalsh@redhat.com> 3.9.3-3
- Add policy for ajaxterm

* Wed Sep 8 2010 Dan Walsh <dwalsh@redhat.com> 3.9.3-2
- Handle /var/db/sudo
- Allow pulseaudio to read alsa config
- Allow init to send initrc_t dbus messages

* Tue Sep 7 2010 Dan Walsh <dwalsh@redhat.com> 3.9.3-1
Allow iptables to read shorewall tmp files
Change chfn and passwd to use auth_use_pam so they can send dbus messages to fpr
intd
label vlc as an execmem_exec_t 
Lots of fixes for mozilla_plugin to run google vidio chat
Allow telepath_msn to execute ldconfig and its own tmp files
Fix labels on hugepages
Allow mdadm to read files on /dev
Remove permissive domains and change back to unconfined
Allow freshclam to execute shell and bin_t
Allow devicekit_power to transition to dhcpc
Add boolean to allow icecast to connect to any port

* Tue Aug 31 2010 Dan Walsh <dwalsh@redhat.com> 3.9.2-1
- Merge upstream fix of mmap_zero
- Allow mount to write files in debugfs_t
- Allow corosync to communicate with clvmd via tmpfs
- Allow certmaster to read usr_t files
- Allow dbus system services to search cgroup_t
- Define rlogind_t as a login pgm

* Tue Aug 31 2010 Dan Walsh <dwalsh@redhat.com> 3.9.1-3
- Allow mdadm_t to read/write hugetlbfs

* Tue Aug 31 2010 Dan Walsh <dwalsh@redhat.com> 3.9.1-2
- Dominic Grift Cleanup
- Miroslav Grepl policy for jabberd
- Various fixes for mount/livecd and prelink

* Mon Aug 30 2010 Dan Walsh <dwalsh@redhat.com> 3.9.1-1
- Merge with upstream

* Thu Aug 26 2010 Dan Walsh <dwalsh@redhat.com> 3.9.0-2
- More access needed for devicekit
- Add dbadm policy

* Thu Aug 26 2010 Dan Walsh <dwalsh@redhat.com> 3.9.0-1
- Merge with upstream

* Tue Aug 24 2010 Dan Walsh <dwalsh@redhat.com> 3.8.8-21
- Allow seunshare to fowner

* Tue Aug 24 2010 Dan Walsh <dwalsh@redhat.com> 3.8.8-20
- Allow cron to look at user_cron_spool links
- Lots of fixes for mozilla_plugin_t
- Add sysv file system
- Turn unconfined domains to permissive to find additional avcs

* Mon Aug 23 2010 Dan Walsh <dwalsh@redhat.com> 3.8.8-19
- Update policy for mozilla_plugin_t

* Mon Aug 23 2010 Dan Walsh <dwalsh@redhat.com> 3.8.8-18
- Allow clamscan to read proc_t
- Allow mount_t to write to debufs_t dir
- Dontaudit mount_t trying to write to security_t dir

* Thu Aug 19 2010 Dan Walsh <dwalsh@redhat.com> 3.8.8-17
- Allow clamscan_t execmem if clamd_use_jit set
- Add policy for firefox plugin-container

* Wed Aug 18 2010 Dan Walsh <dwalsh@redhat.com> 3.8.8-16
- Fix /root/.forward definition

* Tue Aug 17 2010 Dan Walsh <dwalsh@redhat.com> 3.8.8-15
- label dead.letter as mail_home_t

* Fri Aug 13 2010 Dan Walsh <dwalsh@redhat.com> 3.8.8-14
- Allow login programs to search /cgroups

* Thu Aug 12 2010 Dan Walsh <dwalsh@redhat.com> 3.8.8-13
- Fix cert handling

* Tue Aug 10 2010 Dan Walsh <dwalsh@redhat.com> 3.8.8-12
- Fix devicekit_power bug
- Allow policykit_auth_t more access.

* Thu Aug 5 2010 Dan Walsh <dwalsh@redhat.com> 3.8.8-11
- Fix nis calls to allow bind to ports 512-1024
- Fix smartmon

* Wed Aug 4 2010 Dan Walsh <dwalsh@redhat.com> 3.8.8-10
- Allow pcscd to read sysfs
- systemd fixes 
- Fix wine_mmap_zero_ignore boolean

* Tue Aug 3 2010 Dan Walsh <dwalsh@redhat.com> 3.8.8-9
- Apply Miroslav munin patch
- Turn back on allow_execmem and allow_execmod booleans

* Tue Jul 27 2010 Dan Walsh <dwalsh@redhat.com> 3.8.8-8
- Merge in fixes from dgrift repository

* Tue Jul 27 2010 Dan Walsh <dwalsh@redhat.com> 3.8.8-7
- Update boinc policy
- Fix sysstat policy to allow sys_admin
- Change failsafe_context to unconfined_r:unconfined_t:s0

* Mon Jul 26 2010 Dan Walsh <dwalsh@redhat.com> 3.8.8-6
- New paths for upstart

* Mon Jul 26 2010 Dan Walsh <dwalsh@redhat.com> 3.8.8-5
- New permissions for syslog
- New labels for /lib/upstart

* Fri Jul 23 2010 Dan Walsh <dwalsh@redhat.com> 3.8.8-4
- Add mojomojo policy

* Thu Jul 22 2010 Dan Walsh <dwalsh@redhat.com> 3.8.8-3
- Allow systemd to setsockcon on sockets to immitate other services

* Wed Jul 21 2010 Dan Walsh <dwalsh@redhat.com> 3.8.8-2
- Remove debugfs label

* Tue Jul 20 2010 Dan Walsh <dwalsh@redhat.com> 3.8.8-1
- Update to latest policy

* Wed Jul 14 2010 Dan Walsh <dwalsh@redhat.com> 3.8.7-3
- Fix eclipse labeling from IBMSupportAssasstant packageing

* Wed Jul 14 2010 Dan Walsh <dwalsh@redhat.com> 3.8.7-2
- Make boot with systemd in enforcing mode

* Wed Jul 14 2010 Dan Walsh <dwalsh@redhat.com> 3.8.7-1
- Update to upstream

* Mon Jul 12 2010 Dan Walsh <dwalsh@redhat.com> 3.8.6-3
- Add boolean to turn off port forwarding in sshd.

* Fri Jul 9 2010 Miroslav Grepl <mgrepl@redhat.com> 3.8.6-2
- Add support for ebtables
- Fixes for rhcs and corosync policy

* Tue Jun 22 2010 Dan Walsh <dwalsh@redhat.com> 3.8.6-1
-Update to upstream

* Mon Jun 21 2010 Dan Walsh <dwalsh@redhat.com> 3.8.5-1
-Update to upstream

* Thu Jun 17 2010 Dan Walsh <dwalsh@redhat.com> 3.8.4-1
-Update to upstream

* Wed Jun 16 2010 Dan Walsh <dwalsh@redhat.com> 3.8.3-4
- Add Zarafa policy

* Wed Jun 9 2010 Dan Walsh <dwalsh@redhat.com> 3.8.3-3
- Cleanup of aiccu policy
- initial mock policy

* Wed Jun 9 2010 Dan Walsh <dwalsh@redhat.com> 3.8.3-2
- Lots of random fixes

* Tue Jun 8 2010 Dan Walsh <dwalsh@redhat.com> 3.8.3-1
- Update to upstream

* Fri Jun 4 2010 Dan Walsh <dwalsh@redhat.com> 3.8.2-1
- Update to upstream
- Allow prelink script to signal itself
- Cobbler fixes

* Wed Jun 2 2010 Dan Walsh <dwalsh@redhat.com> 3.8.1-5
- Add xdm_var_run_t to xserver_stream_connect_xdm
- Add cmorrord and mpd policy from Miroslav Grepl

* Tue Jun 1 2010 Dan Walsh <dwalsh@redhat.com> 3.8.1-4
- Fix sshd creation of krb cc files for users to be user_tmp_t

* Thu May 27 2010 Dan Walsh <dwalsh@redhat.com> 3.8.1-3
- Fixes for accountsdialog
- Fixes for boinc

* Thu May 27 2010 Dan Walsh <dwalsh@redhat.com> 3.8.1-2
- Fix label on /var/lib/dokwiki
- Change permissive domains to enforcing
- Fix libvirt policy to allow it to run on mls

* Tue May 25 2010 Dan Walsh <dwalsh@redhat.com> 3.8.1-1
- Update to upstream

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

* Fri May 7 2010 Dan Walsh <dwalsh@redhat.com> 3.7.19-14
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

* Wed Feb 24 2010 Dan Walsh <dwalsh@redhat.com> 3.7.10-4
- Change allow_execstack and allow_execmem booleans to on
- dontaudit acct using console
- Add label for fping
- Allow tmpreaper to delete sandbox_file_t
- Fix wine dontaudit mmap_zero
- Allow abrt to read var_t symlinks

* Tue Feb 23 2010 Dan Walsh <dwalsh@redhat.com> 3.7.10-3
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

* Thu Jan 28 2010 Dan Walsh <dwalsh@redhat.com> 3.7.8-5
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

* Thu Jan 7 2010 Dan Walsh <dwalsh@redhat.com> 3.7.7-1
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

* Tue Sep 22 2009 Dan Walsh <dwalsh@redhat.com> 3.6.32-10
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

* Wed Sep 16 2009 Dan Walsh <dwalsh@redhat.com> 3.6.32-1
- Update to upstream
- Dontaudit nsplugin search /root
- Dontaudit nsplugin sys_nice

* Tue Sep 15 2009 Dan Walsh <dwalsh@redhat.com> 3.6.31-5
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

* Thu Jul 23 2009 Dan Walsh <dwalsh@redhat.com> 3.6.23-1
- Update to upstream

* Tue Jul 21 2009 Dan Walsh <dwalsh@redhat.com> 3.6.22-3
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

* Fri May 8 2009 Dan Walsh <dwalsh@redhat.com> 3.6.12-33
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

* Wed Apr 8 2009 Dan Walsh <dwalsh@redhat.com> 3.6.12-2
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

* Thu Mar 5 2009 Dan Walsh <dwalsh@redhat.com> 3.6.8-1
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

* Fri Nov 7 2008 Dan Walsh <dwalsh@redhat.com> 3.5.13-19
- Fix labeling on /var/spool/rsyslog

* Thu Nov 6 2008 Dan Walsh <dwalsh@redhat.com> 3.5.13-18
- Allow postgresl to bind to udp nodes

* Wed Nov 5 2008 Dan Walsh <dwalsh@redhat.com> 3.5.13-17
- Allow lvm to dbus chat with hal
- Allow rlogind to read nfs_t 

* Wed Nov 5 2008 Dan Walsh <dwalsh@redhat.com> 3.5.13-16
- Fix cyphesis file context

* Tue Nov 4 2008 Dan Walsh <dwalsh@redhat.com> 3.5.13-15
- Allow hal/pm-utils to look at /var/run/video.rom
- Add ulogd policy

* Tue Nov 4 2008 Dan Walsh <dwalsh@redhat.com> 3.5.13-14
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

* Sat Aug 2 2008 Dan Walsh <dwalsh@redhat.com> 3.5.2-2
- Allow system-config-selinux to work with policykit

* Fri Jul 25 2008 Dan Walsh <dwalsh@redhat.com> 3.5.1-5
- Fix novel labeling

* Fri Jul 25 2008 Dan Walsh <dwalsh@redhat.com> 3.5.1-4
- Consolodate pyzor,spamassassin, razor into one security domain
- Fix xdm requiring additional perms.

* Fri Jul 25 2008 Dan Walsh <dwalsh@redhat.com> 3.5.1-3
- Fixes for logrotate, alsa

* Thu Jul 24 2008 Dan Walsh <dwalsh@redhat.com> 3.5.1-2
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

* Fri Jun 13 2008 Dan Walsh <dwalsh@redhat.com> 3.4.2-4
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

* Fri Apr 18 2008 Dan Walsh <dwalsh@redhat.com> 3.3.1-37
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

* Sat Mar 29 2008 Dan Walsh <dwalsh@redhat.com> 3.3.1-26
- Allow initrc_t to dbus chat with consolekit.

* Thu Mar 27 2008 Dan Walsh <dwalsh@redhat.com> 3.3.1-25
- Additional access for nsplugin
- Allow xdm setcap/getcap until pulseaudio is fixed

* Tue Mar 25 2008 Dan Walsh <dwalsh@redhat.com> 3.3.1-24
- Allow mount to mkdir on tmpfs
- Allow ifconfig to search debugfs

* Fri Mar 21 2008 Dan Walsh <dwalsh@redhat.com> 3.3.1-23
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

* Thu Feb 7 2008 Dan Walsh <dwalsh@redhat.com> 3.2.7-6
- Allow udev to send audit messages

* Thu Feb 7 2008 Dan Walsh <dwalsh@redhat.com> 3.2.7-5
- Add additional login users interfaces
  -     userdom_admin_login_user_template(staff)

* Thu Feb 7 2008 Dan Walsh <dwalsh@redhat.com> 3.2.7-3
- More fixes for polkit

* Thu Feb 7 2008 Dan Walsh <dwalsh@redhat.com> 3.2.7-2
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

* Sat Dec 22 2007 Dan Walsh <dwalsh@redhat.com> 3.2.5-5
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

* Fri Oct 19 2007 Dan Walsh <dwalsh@redhat.com> 3.0.8-28
- Fixes for hald_mac 
- Treat unconfined_home_dir_t as a home dir
- dontaudit rhgb writes to fonts and root

* Fri Oct 19 2007 Dan Walsh <dwalsh@redhat.com> 3.0.8-27
- Fix dnsmasq
- Allow rshd full login privs

* Thu Oct 18 2007 Dan Walsh <dwalsh@redhat.com> 3.0.8-26
- Allow rshd to connect to ports > 1023

* Thu Oct 18 2007 Dan Walsh <dwalsh@redhat.com> 3.0.8-25
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

* Thu Sep 27 2007 Dan Walsh <dwalsh@redhat.com> 3.0.8-15
- Allow tmpreadper to read man_t
- Allow racoon to bind to all nodes
- Fixes for finger print reader

* Tue Sep 25 2007 Dan Walsh <dwalsh@redhat.com> 3.0.8-14
- Allow xdm to talk to input device (fingerprint reader)
- Allow octave to run as java

* Tue Sep 25 2007 Dan Walsh <dwalsh@redhat.com> 3.0.8-13
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

* Tue Jul 24 2007 Dan Walsh <dwalsh@redhat.com> 3.0.4-2
- Add context for dbus machine id

* Tue Jul 24 2007 Dan Walsh <dwalsh@redhat.com> 3.0.4-1
- Update with latest changes from upstream

* Tue Jul 24 2007 Dan Walsh <dwalsh@redhat.com> 3.0.3-6
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

* Tue Jun 26 2007 Dan Walsh <dwalsh@redhat.com> 3.0.1-3
- Fix syslog declaration

* Tue Jun 26 2007 Dan Walsh <dwalsh@redhat.com> 3.0.1-2
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

* Fri Apr 13 2007 Dan Walsh <dwalsh@redhat.com> 2.5.12-3
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

* Fri Jan 26 2007 Dan Walsh <dwalsh@redhat.com> 2.5.2-3
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

* Thu Nov 30 2006 Dan Walsh <dwalsh@redhat.com> 2.4.6-3
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

* Tue Nov 21 2006 Dan Walsh <dwalsh@redhat.com> 2.4.5-4
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

* Fri Sep 29 2006 Dan Walsh <dwalsh@redhat.com> 2.3.17-1
- Update to upstream

* Fri Sep 29 2006 Dan Walsh <dwalsh@redhat.com> 2.3.16-9
- Remove bluetooth-helper transition
- Add selinux_validate for semanage
- Require new version of libsemanage

* Fri Sep 29 2006 Dan Walsh <dwalsh@redhat.com> 2.3.16-8
- Fix prelink

* Fri Sep 29 2006 Dan Walsh <dwalsh@redhat.com> 2.3.16-7
- Fix rhgb

* Thu Sep 28 2006 Dan Walsh <dwalsh@redhat.com> 2.3.16-6
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

* Tue Aug 22 2006 Dan Walsh <dwalsh@redhat.com> 2.3.8-2
- Fixes for stunnel and postgresql
- Update from upstream

* Sat Aug 12 2006 Dan Walsh <dwalsh@redhat.com> 2.3.7-1
- Update from upstream
- More java fixes

* Fri Aug 11 2006 Dan Walsh <dwalsh@redhat.com> 2.3.6-4
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

* Fri Mar 31 2006 Dan Walsh <dwalsh@redhat.com> 2.2.29-1
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

* Thu Feb 23 2006 Dan Walsh <dwalsh@redhat.com> 2.2.21-4
- Turn on polyinstatiation

* Thu Feb 23 2006 Dan Walsh <dwalsh@redhat.com> 2.2.21-3
- Don't transition from unconfined_t to fsadm_t

* Thu Feb 23 2006 Dan Walsh <dwalsh@redhat.com> 2.2.21-2
- Fix policy update model.

* Thu Feb 23 2006 Dan Walsh <dwalsh@redhat.com> 2.2.21-1
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
* Fri Jan 6 2006 Dan Walsh <dwalsh@redhat.com> 2.1.7-4
- Add wine and fix hal problems

* Thu Jan 5 2006 Dan Walsh <dwalsh@redhat.com> 2.1.7-3
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

* Sun Dec  11 2005 Dan Walsh <dwalsh@redhat.com> 2.1.2-2
- Allow unconfined_t to execmod texrel_shlib_t

* Sat Dec  10 2005 Dan Walsh <dwalsh@redhat.com> 2.1.2-1
- Update to upstream 
- Turn off allow_execmem and allow_execmod booleans
- Add tcpd and automount policies

* Fri Dec  9 2005 Dan Walsh <dwalsh@redhat.com> 2.1.1-3
- Add two new httpd booleans, turned off by default
     * httpd_can_network_relay
     * httpd_can_network_connect_db

* Fri Dec  9 2005 Dan Walsh <dwalsh@redhat.com> 2.1.1-2
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

* Tue Nov 22 2005 Dan Walsh <dwalsh@redhat.com> 2.0.5-1
-Update to latest from upstream

* Tue Nov 22 2005 Dan Walsh <dwalsh@redhat.com> 2.0.4-1
- Add rules for pegasus and avahi

* Mon Nov 21 2005 Dan Walsh <dwalsh@redhat.com> 2.0.2-2
- Start building MLS Policy

* Fri Nov 18 2005 Dan Walsh <dwalsh@redhat.com> 2.0.2-1
- Update to upstream

* Wed Nov 9 2005 Dan Walsh <dwalsh@redhat.com> 2.0.1-2
- Turn on bash

* Wed Nov 9 2005 Dan Walsh <dwalsh@redhat.com> 2.0.1-1
- Initial version
