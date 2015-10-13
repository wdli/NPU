#
# My Experimental Makefile to create SElinux policy RPM
# 



RPM_TOP ?= $(shell rpm -E "`sed -n 's/^%_topdir[ ]*\(.*\)/\1/p' ~/.rpmmacros 2>/dev/null`")
ifeq ($(strip $(RPM_TOP)),)
RPM_TOP=${PWD}/rpmbuild
endif

POLICY_WORK_DIR ?= $(shell pwd)
POLICY_ROOT_DIR ?= $(shell pwd) 

RPMBUILD_RPMS_DIR ?= $(RPM_TOP)/RPMS/noarch
RPMBUILD_SRPMS_DIR ?= $(RPM_TOP)/SRPMS
RPMBUILD_SOURCES_DIR ?= $(RPM_TOP)/SOURCES
RPMBUILD_BUILD_DIR ?= $(RPM_TOP)/BUILD
SPEC_RPMS_DIR ?= $(RPM_TOP)/SPECS

TRESYS_REFPOL ?= $(POLICY_WORK_DIR)/serefpolicy-3.7.19.tgz

MODS_CONF_6=$(POLICY_WORK_DIR)/modules-targeted.conf
MODS_CONF_6_ORG=$(POLICY_WORK_DIR)/modules-targeted.conf.org.david
#
# target: all
#
all: rpm
	

#
# target chk_rpmtop
#
chk_rpmtop: 
	if [ ! -d $(RPM_TOP) ] ; then \
                CMD="mkdir -p $(RPM_TOP)/{RPMS,SRPMS,SOURCES,SPECS,BUILD}";\
                echo "$${CMD}";eval $${CMD};\
        fi



#
# target: get_modules_conf
#


get_modules_conf:
	printf "\n#### David's test policy\n#" >> $(MODS_CONF_6); \
	cp -v $(MODS_CONF_6){.org.david,};\
	[ $$? -ne 0 ] && exit 10 || true;\
	for ff in `find policy -name *.te`; do \
                echo $$ff|\
                sed -e 's|^policy/modules/services/\(.*\).te|\n# David \n#\n\1 = module|'\
                >> $(MODS_CONF_6); \
        done
	CMD="cp $(MODS_CONF_6) $(RPMBUILD_SOURCES_DIR)";\
	echo "$${CMD}";eval $${CMD}



	
#
# target: getpol
#         Install ref policy to rpmbuild/SOURCES
#
getrefpol: chk_rpmtop
	if ! [ -e $(RPMBUILD_SOURCES_DIR)/$(TRESYS_REFPOL) ] ; then \
                CMD="cp $(TRESYS_REFPOL) $(RPMBUILD_SOURCES_DIR)";\
                echo "$${CMD}";eval $${CMD};\
        fi
 
#
# target: getmypol
#         Install my own policy
#
CS_POL_OUTFILE = $(RPM_TOP)/SOURCES/mypolicy.tar.bz2

getmypol: 
	CMD="find policy -regex \".*\.\(if\|te\|fc\)\" |\
         xargs tar -jc --atime-preserve -f $(CS_POL_OUTFILE)";\
        echo "$${CMD}";eval $${CMD}


#
# target prep_rpmsource
#        Install config files and patches to rpmbuild/SOURCES
#
RSYNC=/usr/bin/rsync
prep_rpmsource: 
	rsync -a -v $(POLICY_WORK_DIR)/config.tgz $(POLICY_WORK_DIR)/users-* $(POLICY_WORK_DIR)/customizable_types $(POLICY_WORK_DIR)/policygentool $(POLICY_WORK_DIR)/config/ $(POLICY_WORK_DIR)/securetty_types* $(POLICY_WORK_DIR)/*.conf $(POLICY_WORK_DIR)/*.patch $(RPMBUILD_SOURCES_DIR)

#
# Target: rpm
#
MYSPEC=$(POLICY_WORK_DIR)/selinux-policy.spec
MAKEFILE_DEVEL=$(POLICY_WORK_DIR)/Makefile.devel

rpm: getrefpol get_modules_conf getmypol prep_rpmsource
	CMD="cp $(MYSPEC) $(SPEC_RPMS_DIR)";\
        echo "$${CMD}";eval $${CMD};\
	CMD="cp $(MAKEFILE_DEVEL) $(RPMBUILD_SOURCES_DIR)";\
        echo "$${CMD}";eval $${CMD};\
        CMD="rpmbuild -v --define '_topdir $(RPM_TOP)' -bb $(MYSPEC)";\
        echo "$${CMD}";eval $${CMD};\
#$(call selnk)


               
clean:
	@echo "cleaning up rpmbuild/{source, build}"
	CMD="rm -rf $(RPMBUILD_SOURCES_DIR)/* $(RPMBUILD_BUILD_DIR)/*";\
	echo "$${CMD}"; eval $${CMD};
	
 
 
