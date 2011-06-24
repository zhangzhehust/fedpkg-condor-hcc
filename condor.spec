%define tarball_version 7.6.0

# Things for F15 or later
%if 0%{?fedora} >= 15
# NOTE: Condor+gsoap doesn't work yet on F15; ticket not yet upstream AFAIK.  BB
%define gsoap 0
%define deltacloud 1
%define aviary 1
%define systemd 1
%define cgroups 1
%else
%define gsoap 1
%define deltacloud 0
%define aviary 0
%define systemd 0
%define cgroups 0
%endif

# Things not turned on, or don't have Fedora packages yet
%define blahp 0
%define qmf 0

# These flags are meant for developers; it allows one to build Condor
# based upon a git-derived tarball, instead of an upstream release tarball
%define git_build 0
# If building with git tarball, Fedora requests us to record the rev.  Use:
# git log -1 --pretty=format:'%h'
%define git_rev 8b70570
%define git_build_man 0

# Determine whether man pages will be included.
%if !%git_build || (%git_build && %git_build_man)
%define include_man 1
%else
%define include_man 0
%endif

Summary: Condor: High Throughput Computing
Name: condor
Version: 7.7.0

# Only edit the %condor_base_release to bump the rev number
%define condor_base_release 0.5
%if %git_build
%define condor_release %condor_base_release.%{git_rev}git
%else
%define condor_release %condor_base_release
%endif
Release: %condor_release%{?dist}

License: ASL 2.0
Group: Applications/System
URL: http://www.cs.wisc.edu/condor/

# This allows developers to test the RPM with a non-release, git tarball
%if %git_build
# git clone http://condor-git.cs.wisc.edu/repos/condor.git
# cd condor
# git-archive master | gzip -7 > ~/rpmbuild/SOURCES/condor.tar.gz
Source0: condor.tar.gz

# Also potentially allow a git-based doc tarball
%if %git_build_man
# git clone http://condor-git.cs.wisc.edu/repos/condor_docs.git
# cd condor
# git-archive V7_6_0 | gzip -7 > ~/rpmbuild/SOURCES/condor_docs.tar.gz
Source1: condor_docs.tar.gz
%endif

%else
# The upstream Condor source tarball contains some source that cannot
# be shipped as well as extraneous copies of packages the source
# depends on. Additionally, the upstream Condor source requires a
# click-through license. Once you have downloaded the source from:
#   http://parrot.cs.wisc.edu/v7.0.license.html
# you should process it with generate-tarball.sh:
#   ./generate-tarball.sh 7.0.4
# MD5Sum of upstream source:
#   06eec3ae274b66d233ad050a047f3c91  condor_src-7.0.0-all-all.tar.gz
#   b08743cfa2e87adbcda042896e8ef537  condor_src-7.0.2-all-all.tar.gz
#   5f326ad522b63eacf34c6c563cf46910  condor_src-7.0.4-all-all.tar.gz
#   73323100c5b2259f3b9c042fa05451e0  condor_src-7.0.5-all-all.tar.gz
#   a2dd96ea537b2c6d105b6c8dad563ddc  condor_src-7.2.0-all-all.tar.gz
#   edbac8267130ac0a0e016d0f113b4616  condor_src-7.2.1-all-all.tar.gz
#   6d9b0ef74d575623af11e396fa274174  condor_src-7.2.4-all-all.tar.gz
#   ee72b65fad02d21af0dc8f1aa5872110  condor_src-7.4.0-all-all.tar.gz
#   d4deeabbbce65980c085d8bea4c1018a  condor_src-7.4.1-all-all.tar.gz
#   4714086f58942b78cf03fef9ccb1117c  condor_src-7.4.2-all-all.tar.gz
#   2b7e7687cba85d0cf0774f9126b51779  condor_src-7.4.3-all-all.tar.gz
#   108a4b91cd10deca1554ca1088be6c8c  condor_src-7.4.4-all-all.tar.gz
#   b482c4bfa350164427a1952113d53d03  condor_src-7.5.5-all-all.tar.gz
#   2a1355cb24a56a71978d229ddc490bc5  condor_src-7.6.0-all-all.tar.gz
# Note: The md5sum of each generated tarball may be different
Source0: condor-7.6.0-327697-RH.tar.gz
Source1: generate-tarball.sh
%endif

%if %systemd
Source2: %{name}-tmpfiles.conf
Source3: condor.service
%endif
Patch0: condor_config.generic.patch
Patch3: chkconfig_off.patch
%if !%git_build
Patch4: 7.7.0-catch-up.patch
%endif
Patch5: condor_shared_libs.patch

BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

# Explicitly request cmake >= 2.8.0, as this is not generally available on RHEL5 platforms
BuildRequires: cmake >= 2.8.0
BuildRequires: %_bindir/flex
BuildRequires: %_bindir/byacc
BuildRequires: pcre-devel
#BuildRequires: postgresql-devel
BuildRequires: openssl-devel
BuildRequires: krb5-devel
%if %gsoap
BuildRequires: gsoap-devel >= 2.7.12-1
%endif
BuildRequires: libvirt-devel
BuildRequires: bind-utils
BuildRequires: m4
#BuildRequires: autoconf
BuildRequires: libX11-devel
%if %aviary
BuildRequires: wso2-wsf-cpp-devel
BuildRequires: wso2-axis2-devel
%endif
BuildRequires: /usr/include/curl/curl.h
BuildRequires: /usr/include/expat.h
%if %qmf
BuildRequires: qpid-qmf-devel
%endif
%if %deltacloud
BuildRequires: %_includedir/libdeltacloud/libdeltacloud.h
%endif
BuildRequires: openldap-devel

# Globus GSI build requirements
BuildRequires: globus-gssapi-gsi-devel
BuildRequires: globus-gass-server-ez-devel
BuildRequires: globus-gass-transfer-devel
BuildRequires: globus-gram-client-devel
BuildRequires: globus-rsl-devel
BuildRequires: globus-gram-protocol
BuildRequires: globus-io-devel
BuildRequires: globus-xio-devel
BuildRequires: globus-gssapi-error-devel
BuildRequires: globus-gss-assist-devel
BuildRequires: globus-gsi-proxy-core-devel
BuildRequires: globus-gsi-credential-devel
BuildRequires: globus-gsi-callback-devel
BuildRequires: globus-gsi-sysconfig-devel
BuildRequires: globus-gsi-cert-utils-devel
BuildRequires: globus-openssl-module-devel
BuildRequires: globus-gsi-openssl-error-devel
BuildRequires: globus-gsi-proxy-ssl-devel
BuildRequires: globus-callout-devel
BuildRequires: globus-common-devel
BuildRequires: globus-ftp-client-devel
BuildRequires: globus-ftp-control-devel
BuildRequires: libtool-ltdl-devel
BuildRequires: voms-devel

%if %cgroups
BuildRequires: libcgroup-devel >= 0.37
%endif

%if %blahp
BuildRequires: blahp
%endif

%if %qmf
BuildRequires: qpid-qmf-devel
%endif

%if %systemd
BuildRequires: systemd-units
%endif

%if %git_build_man
BuildRequires: transfig
BuildRequires: latex2html
%endif

%if %gsoap
Requires: gsoap >= 2.7.12
%endif
Requires: mailx
Requires: python >= 2.2
Requires: condor-classads = %{version}-%{release}
%if %blahp
Requires: blahp >= 1.16.1
%endif
# libcgroup < 0.37 has a bug that invalidates our accounting.
Requires: libcgroup >= 0.37

Requires: initscripts

Requires(pre): shadow-utils

%if %systemd
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units
Requires(post): systemd-sysv
%else
Requires(post):/sbin/chkconfig
Requires(preun):/sbin/chkconfig
Requires(preun):/sbin/service
Requires(postun):/sbin/service
%endif

#Provides: user(condor) = 43
#Provides: group(condor) = 43

Obsoletes: condor-static < 7.2.0


%description
Condor is a specialized workload management system for
compute-intensive jobs. Like other full-featured batch systems, Condor
provides a job queueing mechanism, scheduling policy, priority scheme,
resource monitoring, and resource management. Users submit their
serial or parallel jobs to Condor, Condor places them into a queue,
chooses when and where to run the jobs based upon a policy, carefully
monitors their progress, and ultimately informs the user upon
completion.


%if %qmf
%package qmf
Summary: Condor QMF components
Group: Applications/System
Requires: %name = %version-%release
#Requires: qmf >= %{qmf_version}
Requires: python-qmf >= 0.7.946106
Requires: condor-classads = %{version}-%{release}
Obsoletes: condor-qmf-plugins

%description qmf
Components to connect Condor to the QMF management bus.
%endif

%if %aviary
%package aviary
Summary: Condor Aviary components
Group: Applications/System
Requires: %name = %version-%release
Requires: condor-classads = %{version}-%{release}

%description aviary
Components to provide simplified WS interface to Condor.
%endif

%package kbdd
Summary: Condor Keyboard Daemon
Group: Applications/System
Requires: %name = %version-%release
Requires: condor-classads = %{version}-%{release}

%description kbdd
The condor_kbdd monitors logged in X users for activity. It is only
useful on systems where no device (e.g. /dev/*) can be used to
determine console idle time.


%package vm-gahp
Summary: Condor's VM Gahp
Group: Applications/System
Requires: %name = %version-%release
Requires: libvirt
Requires: condor-classads = %{version}-%{release}

%description vm-gahp
The condor_vm-gahp enables the Virtual Machine Universe feature of
Condor. The VM Universe uses libvirt to start and control VMs under
Condor's Startd.

%if %deltacloud
%package deltacloud-gahp
Summary: Condor's Deltacloud Gahp
Group: Applications/System
Requires: %name = %version-%release

%description deltacloud-gahp
The deltacloud_gahp enables Condor's ability to manage jobs run on
resources exposed by the deltacloud API.
%endif

%package classads
Summary: Condor's classified advertisement language
Group: Development/Libraries
Obsoletes: classads <= 1.0.8
Obsoletes: classads-static <= 1.0.8

%description classads
Classified Advertisements (classads) are the lingua franca of
Condor. They are used for describing jobs, workstations, and other
resources. They are exchanged by Condor processes to schedule
jobs. They are logged to files for statistical and debugging
purposes. They are used to enquire about current state of the system.

A classad is a mapping from attribute names to expressions. In the
simplest cases, the expressions are simple constants (integer,
floating point, or string). A classad is thus a form of property
list. Attribute expressions can also be more complicated. There is a
protocol for evaluating an attribute expression of a classad vis a vis
another ad. For example, the expression "other.size > 3" in one ad
evaluates to true if the other ad has an attribute named size and the
value of that attribute is (or evaluates to) an integer greater than
three. Two classads match if each ad has an attribute requirements
that evaluates to true in the context of the other ad. Classad
matching is used by the Condor central manager to determine the
compatibility of jobs and workstations where they may be run.


%package classads-devel
Summary: Headers for Condor's classified advertisement language
Group: Development/System
Requires: %name-classads = %version-%release
Requires: pcre-devel
Obsoletes: classads-devel <= 1.0.8

%description classads-devel
Header files for Condor's ClassAd Library, a powerful and flexible,
semi-structured representation of data.


%pre
getent group condor >/dev/null || groupadd -r condor
getent passwd condor >/dev/null || \
  useradd -r -g condor -d %_var/lib/condor -s /sbin/nologin \
    -c "Owner of Condor Daemons" condor
exit 0


%prep
%if %git_build
%if %git_build_man
%setup -q -c -n %{name}-%{tarball_version} -a 1
%else
%setup -q -c -n %{name}-%{tarball_version}
%endif
%else
# For release tarballs
%setup -q -n %{name}-%{tarball_version}
%endif

%patch3 -p1
# Catch-up patch for release tarballs
%if !%git_build
%patch4 -p1
%endif
%patch0 -p1
%patch5 -p1

# fix errant execute permissions
find src -perm /a+x -type f -name "*.[Cch]" -exec chmod a-x {} \;


%build

# Possibly build man files
%if %git_build_man
pushd doc
make just-man-pages
popd
%endif

%cmake -DNO_PHONE_HOME:BOOL=TRUE \
       -DHAVE_BACKFILL:BOOL=FALSE \
       -DHAVE_BOINC:BOOL=FALSE \
%if %gsoap
       -DWITH_GSOAP:BOOL=TRUE \
%else
       -DWITH_GSOAP:BOOL=FALSE \
%endif
       -DWITH_POSTGRESQL:BOOL=FALSE \
       -DHAVE_KBDD:BOOL=TRUE \
       -DHAVE_HIBERNATION:BOOL=TRUE \
       -DWANT_LEASE_MANAGER:BOOL=FALSE \
       -DWANT_HDFS:BOOL=FALSE \
       -DWANT_QUILL:BOOL=FALSE \
       -DWITH_ZLIB:BOOL=FALSE \
       -DWITH_POSTGRESQL:BOOL=FALSE \
       -DWANT_CONTRIB:BOOL=ON \
%if %aviary
       -DWITH_AVIARY:BOOL=TRUE \
%else
       -DWITH_AVIARY:BOOL=FALSE \
%endif
%if %qmf
       -DWITH_TRIGGERD:BOOL=TRUE \
       -DWITH_MANAGEMENT:BOOL=TRUE \
%else
       -DWITH_TRIGGERD:BOOL=FALSE \
       -DWITH_MANAGEMENT:BOOL=FALSE \
%endif
       -DWANT_FULL_DEPLOYMENT:BOOL=FALSE \
       -DWANT_GLEXEC:BOOL=FALSE \
%if %deltacloud
       -DWITH_LIBDELTACLOUD:BOOL=TRUE \
%else
       -DWITH_LIBDELTACLOUD:BOOL=FALSE \
%endif
       -DWITH_GLOBUS:BOOL=TRUE \
       -DLIBCGROUP_FOUND_SEARCH_cgroup=/%{_lib}/libcgroup.so.1

# NOTE: I used to have these.  Check to see if they are still needed
#       -DHAVE_BACKFILL:BOOL=TRUE \
#       -DBUILD_TESTS=OFF \
#       -DCONDOR_STRIP_PACKAGES=OFF \

make %{?_smp_mflags}


%install
# installation happens into a temporary location, this function is
# useful in moving files into their final locations
function populate {
  _dest="$1"; shift; _src="$*"
  mkdir -p "%{buildroot}/$_dest"
  mv $_src "%{buildroot}/$_dest"
}

rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

# The install target puts etc/ under usr/, let's fix that.
mv %{buildroot}/usr/etc %{buildroot}/%{_sysconfdir}

populate %_sysconfdir/condor %{buildroot}/%{_usr}/lib/condor_ssh_to_job_sshd_config_template

# Things in /usr/lib really belong in /usr/share/condor
populate %{_datadir}/condor %{buildroot}/%{_usr}/lib/*
# Except for the shared libs
populate %{_libdir}/ %{buildroot}/%{_datadir}/condor/libclassad.so*
rm -f %{buildroot}/%{_datadir}/condor/libclassads.a
mv %{buildroot}%{_datadir}/condor/lib*.so %{buildroot}%{_libdir}/

%if %aviary || %qmf
populate %{_libdir}/condor/plugins %{buildroot}/%{_usr}/libexec/*-plugin.so
%endif

# It is proper to put Condor specific libexec binaries under libexec/condor/
populate %_libexecdir/condor %{buildroot}/usr/libexec/*

# man pages go under %{_mandir}
%if %include_man
mkdir -p %{buildroot}/%{_mandir}
mv %{buildroot}/usr/man/man1 %{buildroot}/%{_mandir}
%if %git_build_man
pushd %{buildroot}/%{_mandir}/man1
for i in `ls`; do
  gzip $i
done
popd
%endif
%endif

# Things in /usr/lib really belong in /usr/share/condor
#mv %{buildroot}/usr/lib %{buildroot}/%{_datarootdir}/condor

mkdir -p %{buildroot}/%{_sysconfdir}/condor
# the default condor_config file is not architecture aware and thus
# sets the LIB directory to always be /usr/lib, we want to do better
# than that. this is, so far, the best place to do this
# specialization. we strip the "lib" or "lib64" part from _libdir and
# stick it in the LIB variable in the config.
LIB=$(echo %{?_libdir} | sed -e 's:/usr/\(.*\):\1:')
if [ "$LIB" = "%_libdir" ]; then
  echo "_libdir does not contain /usr, sed expression needs attention"
  exit 1
fi
sed -e "s:^LIB\s*=.*:LIB = \$(RELEASE_DIR)/$LIB/condor:" \
  %{buildroot}/etc/examples/condor_config.generic \
  > %{buildroot}/%{_sysconfdir}/condor/condor_config

# Install the basic configuration, a Personal Condor config. Allows for
# yum install condor + service condor start and go.
mkdir -m0755 %{buildroot}/%{_sysconfdir}/condor/config.d
cp %{buildroot}/etc/examples/condor_config.local %{buildroot}/%{_sysconfdir}/condor/config.d/00personal_condor.config

%if %qmf
# Install condor-qmf's base plugin configuration
populate %_sysconfdir/condor/config.d %{buildroot}/etc/examples/60condor-qmf.config
%endif
%if %aviary
# Install condor-aviary's base plugin configuration
populate %_sysconfdir/condor/config.d %{buildroot}/etc/examples/61aviary.config

mkdir -p %{buildroot}/%{_var}/lib/condor/aviary
populate %{_var}/lib/condor/aviary %{buildroot}/usr/axis2.xml
populate %{_var}/lib/condor/aviary %{buildroot}/usr/services/
%endif

mkdir -p -m0755 %{buildroot}/%{_var}/run/condor
mkdir -p -m0755 %{buildroot}/%{_var}/log/condor
mkdir -p -m0755 %{buildroot}/%{_var}/lock/condor
mkdir -p -m1777 %{buildroot}/%{_var}/lock/condor/local
# Note we use %{_var}/lib instead of %{_sharedstatedir} for RHEL5 compatibility
mkdir -p -m0755 %{buildroot}/%{_var}/lib/condor/spool
mkdir -p -m1777 %{buildroot}/%{_var}/lib/condor/execute

cat >> %{buildroot}/%{_sharedstatedir}/condor/condor_config.local << EOF
CONDOR_DEVELOPERS = NONE
CONDOR_HOST = \$(FULL_HOSTNAME)
COLLECTOR_NAME = Personal Condor
START = TRUE
SUSPEND = FALSE
PREEMPT = FALSE
KILL = FALSE
DAEMON_LIST = COLLECTOR, MASTER, NEGOTIATOR, SCHEDD, STARTD
NEGOTIATOR_INTERVAL = 20
EOF

# this gets around a bug whose fix is not yet merged
echo "TRUST_UID_DOMAIN = TRUE" >> %{buildroot}/%{_sharedstatedir}/condor/condor_config.local

# no master shutdown program for now
rm %{buildroot}/%{_sbindir}/condor_set_shutdown
%if %include_man
rm %{buildroot}/%{_mandir}/man1/condor_set_shutdown.1.gz
%endif

# not packaging deployment tools
%if %include_man
rm %{buildroot}/%{_mandir}/man1/condor_config_bind.1.gz
rm %{buildroot}/%{_mandir}/man1/condor_cold_start.1.gz
rm %{buildroot}/%{_mandir}/man1/condor_cold_stop.1.gz
rm %{buildroot}/%{_mandir}/man1/uniq_pid_midwife.1.gz
rm %{buildroot}/%{_mandir}/man1/uniq_pid_undertaker.1.gz
rm %{buildroot}/%{_mandir}/man1/filelock_midwife.1.gz
rm %{buildroot}/%{_mandir}/man1/filelock_undertaker.1.gz
rm %{buildroot}/%{_mandir}/man1/install_release.1.gz
rm %{buildroot}/%{_mandir}/man1/cleanup_release.1.gz

# not packaging standard universe
rm %{buildroot}/%{_mandir}/man1/condor_compile.1.gz
rm %{buildroot}/%{_mandir}/man1/condor_checkpoint.1.gz

# not packaging configure/install scripts
rm %{buildroot}/%{_mandir}/man1/condor_configure.1.gz

# not packaging legacy cruft
rm %{buildroot}/%{_mandir}/man1/condor_master_off.1.gz
rm %{buildroot}/%{_mandir}/man1/condor_reconfig_schedd.1.gz
rm %{buildroot}/%{_mandir}/man1/condor_convert_history.1.gz

# not packaging gidd_alloc or procd_ctl
rm %{buildroot}/%{_mandir}/man1/gidd_alloc.1.gz
rm %{buildroot}/%{_mandir}/man1/procd_ctl.1.gz

# not packaging quill bits
rm %{buildroot}/%{_mandir}/man1/condor_load_history.1.gz
%endif

# Remove junk
rm -r %{buildroot}/%{_sysconfdir}/sysconfig
rm -r %{buildroot}/%{_sysconfdir}/init.d

%if %systemd
# install tmpfiles.d/condor.conf
mkdir -p %{buildroot}%{_sysconfdir}/tmpfiles.d
install -m 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/tmpfiles.d/%{name}.conf

mkdir -p %{buildroot}%{_unitdir}
cp %{SOURCE3} %{buildroot}%{_unitdir}/condor.service
%else
# install the lsb init script
install -Dp -m0755 %{buildroot}/etc/examples/condor.init %buildroot/%_initrddir/condor
%endif

# we must place the config examples in builddir so %doc can find them
mv %{buildroot}/etc/examples %_builddir/%name-%tarball_version


%clean
rm -rf %{buildroot}


%check
# This currently takes hours and can kill your machine...
#cd condor_tests
#make check-seralized


%files
%defattr(-,root,root,-)
%doc LICENSE-2.0.txt examples
%dir %_sysconfdir/condor/
%config(noreplace) %_sysconfdir/condor/condor_config
%if %systemd
%config(noreplace) %_sysconfdir/tmpfiles.d/%{name}.conf
%{_unitdir}/condor.service
%else
%_initrddir/condor
%endif
%dir %_datadir/condor/
%_datadir/condor/Chirp.jar
%_datadir/condor/CondorJavaInfo.class
%_datadir/condor/CondorJavaWrapper.class
%_datadir/condor/Condor.pm
%_datadir/condor/scimark2lib.jar
%_datadir/condor/gt4-gahp.jar
%_datadir/condor/gt42-gahp.jar
%dir %_sysconfdir/condor/config.d/
%_sysconfdir/condor/config.d/00personal_condor.config
%_sysconfdir/condor/condor_ssh_to_job_sshd_config_template
%if %gsoap
%dir %_datadir/condor/webservice/
%_datadir/condor/webservice/condorCollector.wsdl
%_datadir/condor/webservice/condorSchedd.wsdl
%endif
%dir %_libexecdir/condor/
%_libexecdir/condor/condor_chirp
%_libexecdir/condor/condor_ssh
%_libexecdir/condor/sshd.sh
%_libexecdir/condor/condor_job_router
%_libexecdir/condor/gridftp_wrapper.sh
#%_libexecdir/condor/condor_glexec_update_proxy
%_libexecdir/condor/condor_limits_wrapper.sh
%_libexecdir/condor/condor_rooster
%_libexecdir/condor/condor_ssh_to_job_shell_setup
%_libexecdir/condor/condor_ssh_to_job_sshd_setup
%_libexecdir/condor/condor_power_state
%_libexecdir/condor/condor_kflops
%_libexecdir/condor/condor_mips
%_libexecdir/condor/data_plugin
%_libexecdir/condor/curl_plugin
%_libexecdir/condor/condor_shared_port
%_libexecdir/condor/condor_glexec_wrapper
%_libexecdir/condor/glexec_starter_setup.sh
%if %include_man
%_mandir/man1/condor_advertise.1.gz
%_mandir/man1/condor_check_userlogs.1.gz
%_mandir/man1/condor_chirp.1.gz
%_mandir/man1/condor_cod.1.gz
%_mandir/man1/condor_config_val.1.gz
%_mandir/man1/condor_dagman.1.gz
%_mandir/man1/condor_fetchlog.1.gz
%_mandir/man1/condor_findhost.1.gz
%_mandir/man1/condor_history.1.gz
%_mandir/man1/condor_hold.1.gz
%_mandir/man1/condor_master.1.gz
%_mandir/man1/condor_off.1.gz
%_mandir/man1/condor_on.1.gz
%_mandir/man1/condor_preen.1.gz
%_mandir/man1/condor_prio.1.gz
%_mandir/man1/condor_procd.1.gz
%_mandir/man1/condor_q.1.gz
%_mandir/man1/condor_qedit.1.gz
%_mandir/man1/condor_reconfig.1.gz
%_mandir/man1/condor_release.1.gz
%_mandir/man1/condor_reschedule.1.gz
%_mandir/man1/condor_restart.1.gz
%_mandir/man1/condor_rm.1.gz
%_mandir/man1/condor_run.1.gz
%_mandir/man1/condor_stats.1.gz
%_mandir/man1/condor_status.1.gz
%_mandir/man1/condor_store_cred.1.gz
%_mandir/man1/condor_submit.1.gz
%_mandir/man1/condor_submit_dag.1.gz
%_mandir/man1/condor_transfer_data.1.gz
%_mandir/man1/condor_updates_stats.1.gz
%_mandir/man1/condor_userlog.1.gz
%_mandir/man1/condor_userprio.1.gz
%_mandir/man1/condor_vacate.1.gz
%_mandir/man1/condor_vacate_job.1.gz
%_mandir/man1/condor_version.1.gz
%_mandir/man1/condor_wait.1.gz
%_mandir/man1/condor_router_history.1.gz
%_mandir/man1/condor_router_q.1.gz
%_mandir/man1/condor_ssh_to_job.1.gz
%_mandir/man1/condor_power.1.gz
%_mandir/man1/condor_glidein.1.gz
%endif
# bin/condor is a link for checkpoint, reschedule, vacate
%_bindir/condor
%_bindir/condor_submit_dag
%_bindir/condor_prio
%_bindir/condor_transfer_data
%_bindir/condor_check_userlogs
%_bindir/condor_q
%_libexecdir/condor/condor_transferer
%_bindir/condor_cod
%_bindir/condor_qedit
%_bindir/condor_userlog
%_bindir/condor_release
%_bindir/condor_userlog_job_counter
%_bindir/condor_config_val
%_bindir/condor_reschedule
%_bindir/condor_userprio
%_bindir/condor_dagman
%_bindir/condor_rm
%_bindir/condor_vacate
%_bindir/condor_run
%_bindir/condor_router_history
%_bindir/condor_router_q
%_bindir/condor_router_rm
%_bindir/condor_vacate_job
%_bindir/condor_findhost
%_bindir/condor_stats
%_bindir/condor_version
%_bindir/condor_history
%_bindir/condor_status
%_bindir/condor_wait
%_bindir/condor_hold
%_bindir/condor_submit
%_bindir/condor_ssh_to_job
%_bindir/condor_power
%_bindir/condor_gather_info
%_bindir/condor_test_match
%_bindir/condor_glidein
# sbin/condor is a link for master_off, off, on, reconfig,
# reconfig_schedd, restart
%_sbindir/condor_advertise
%_sbindir/condor_c-gahp
%_sbindir/condor_c-gahp_worker_thread
%_sbindir/condor_collector
%_sbindir/condor_fetchlog
%_sbindir/condor_had
%_sbindir/condor_init
%_sbindir/condor_master
%_sbindir/condor_negotiator
%_sbindir/condor_off
%_sbindir/condor_on
%_sbindir/condor_preen
%_sbindir/condor_procd
%_sbindir/condor_reconfig
%_sbindir/condor_replication
%_sbindir/condor_restart
%_sbindir/condor_root_switchboard
%_sbindir/condor_schedd
%_sbindir/condor_shadow
%_sbindir/condor_startd
%_sbindir/condor_starter
%_sbindir/condor_store_cred
%_sbindir/condor_transferd
%_sbindir/condor_updates_stats
%_sbindir/ec2_gahp
%_sbindir/condor_gridmanager
%_sbindir/condor_gridshell
%_sbindir/gahp_server
%_sbindir/grid_monitor.sh
%_sbindir/nordugrid_gahp
%_sbindir/gt4_gahp
%_sbindir/gt42_gahp
%_libdir/lib*.so
#%_sbindir/condor_credd
%config(noreplace) %_var/lib/condor/condor_config.local
%defattr(-,condor,condor,-)
%dir %_var/lib/condor/
%dir %_var/lib/condor/execute/
%dir %_var/log/condor/
%dir %_var/lib/condor/spool/
%dir %_var/lock/condor/
%dir %_var/run/condor/


#%files static
#%defattr(-,root,root,-)
#%doc LICENSE-2.0.txt
#%_libdir/libcondorapi.a
#%dir %_includedir/condor/
#%_includedir/condor/condor_constants.h
#%_includedir/condor/condor_event.h
#%_includedir/condor/condor_holdcodes.h
#%_includedir/condor/file_lock.h
#%_includedir/condor/user_log.c++.h
#%doc %_includedir/condor/user_log.README
#%dir %_usrsrc/chirp/
#%_usrsrc/chirp/chirp_client.c
#%_usrsrc/chirp/chirp_client.h
#%_usrsrc/chirp/chirp_protocol.h

%if %qmf
%files qmf
%defattr(-,root,root,-)
%doc LICENSE-2.0.txt NOTICE.txt
%_sysconfdir/condor/config.d/60condor-qmf.config
%dir %_libdir/condor/plugins
%_libdir/condor/plugins/MgmtCollectorPlugin-plugin.so
%_libdir/condor/plugins/MgmtMasterPlugin-plugin.so
%_libdir/condor/plugins/MgmtNegotiatorPlugin-plugin.so
%_libdir/condor/plugins/MgmtScheddPlugin-plugin.so
%_libdir/condor/plugins/MgmtStartdPlugin-plugin.so
%_bindir/get_trigger_data
%_sbindir/condor_trigger_config
%_sbindir/condor_triggerd
%_sbindir/condor_job_server
%endif

%if %aviary
%files aviary
%defattr(-,root,root,-)
%doc LICENSE-2.0.txt NOTICE.txt
%_sysconfdir/condor/config.d/61aviary.config
%dir %_libdir/condor/plugins
%_libdir/condor/plugins/AviaryScheddPlugin-plugin.so
%_sbindir/aviary_query_server
%dir %_var/lib/condor/aviary
%_var/lib/condor/aviary/axis2.xml
%dir %_var/lib/condor/aviary/services
%dir %_var/lib/condor/aviary/services/job
%_var/lib/condor/aviary/services/job/libaviary_job_axis.so
%_var/lib/condor/aviary/services/job/services.xml
%_var/lib/condor/aviary/services/job/aviary-common.xsd
%_var/lib/condor/aviary/services/job/aviary-job.xsd
%_var/lib/condor/aviary/services/job/aviary-job.wsdl
%dir %_var/lib/condor/aviary/services/query
%_var/lib/condor/aviary/services/query/libaviary_query_axis.so
%_var/lib/condor/aviary/services/query/services.xml
%_var/lib/condor/aviary/services/query/aviary-common.xsd
%_var/lib/condor/aviary/services/query/aviary-query.xsd
%_var/lib/condor/aviary/services/query/aviary-query.wsdl
%endif

%files kbdd
%defattr(-,root,root,-)
%doc LICENSE-2.0.txt NOTICE.txt
%_sbindir/condor_kbdd


%files vm-gahp
%defattr(-,root,root,-)
%doc LICENSE-2.0.txt NOTICE.txt
%_sbindir/condor_vm-gahp
#%_sbindir/condor_vm_vmware.pl
#%_sbindir/condor_vm_xen.sh
%_libexecdir/condor/libvirt_simple_script.awk

%if %deltacloud
%files deltacloud-gahp
%defattr(-,root,root,-)
%doc LICENSE-2.0.txt NOTICE.txt
%_sbindir/deltacloud_gahp
%endif

%files classads
%defattr(-,root,root,-)
%doc LICENSE-2.0.txt NOTICE.txt
%_libdir/libclassad.so.1
%_libdir/libclassad.so.1.1.0
%_libdir/libclassads.so

%files classads-devel
%defattr(-,root,root,-)
%doc LICENSE-2.0.txt NOTICE.txt
%_bindir/classad_functional_tester
%_bindir/classad_version
%_libdir/libclassad.so
%dir %_includedir/classad/
%_includedir/classad/attrrefs.h
%_includedir/classad/cclassad.h
%_includedir/classad/classad_distribution.h
%_includedir/classad/classadErrno.h
%_includedir/classad/classad.h
%_includedir/classad/classadItor.h
%_includedir/classad/classad_stl.h
%_includedir/classad/collectionBase.h
%_includedir/classad/collection.h
%_includedir/classad/common.h
%_includedir/classad/debug.h
%_includedir/classad/exprList.h
%_includedir/classad/exprTree.h
%_includedir/classad/fnCall.h
%_includedir/classad/indexfile.h
%_includedir/classad/lexer.h
%_includedir/classad/lexerSource.h
%_includedir/classad/literals.h
%_includedir/classad/matchClassad.h
%_includedir/classad/operators.h
%_includedir/classad/query.h
%_includedir/classad/sink.h
%_includedir/classad/source.h
%_includedir/classad/transaction.h
%_includedir/classad/util.h
%_includedir/classad/value.h
%_includedir/classad/view.h
%_includedir/classad/xmlLexer.h
%_includedir/classad/xmlSink.h
%_includedir/classad/xmlSource.h

%if %systemd
%post
if [ $1 -eq 1 ] ; then
    # Initial installation 
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi

%preun
if [ $1 -eq 0 ] ; then
    # Package removal, not upgrade
    /bin/systemctl --no-reload disable condor.service > /dev/null 2>&1 || :
    /bin/systemctl stop condor.service > /dev/null 2>&1 || :
fi

%postun
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    /bin/systemctl try-restart condor.service >/dev/null 2>&1 || :
fi

%triggerun -- condor < 7.7.0-0.5

/usr/bin/systemd-sysv-convert --save condor >/dev/null 2>&1 ||:

/sbin/chkconfig --del condor >/dev/null 2>&1 || :
/bin/systemctl try-restart condor.service >/dev/null 2>&1 || :

%else
%post -n condor
/sbin/chkconfig --add condor
/sbin/ldconfig
#test -x /usr/sbin/selinuxenabled && /usr/sbin/selinuxenabled
#if [ $? = 0 ]; then
#   semanage fcontext -a -t unconfined_execmem_exec_t %_sbindir/condor_startd
#   restorecon  %_sbindir/condor_startd
#fi


%preun -n condor
if [ $1 = 0 ]; then
  /sbin/service condor stop >/dev/null 2>&1 || :
  /sbin/chkconfig --del condor
fi


%postun -n condor
if [ "$1" -ge "1" ]; then
  /sbin/service condor condrestart >/dev/null 2>&1 || :
fi
/sbin/ldconfig
%endif

%changelog
* Tue Jun  8 2011 <bbockelm@cse.unl.edu> - 7.7.0-0.5
- Start to break build products into conditionals for future EPEL5 support.
- Begun integration of a systemd service file.

* Tue Jun  7 2011 <matt@redhat> - 7.7.0-0.4
- Added tmpfiles.d/condor.conf (BZ711456)

* Tue Jun  7 2011 <matt@redhat> - 7.7.0-0.3
- Fast forward to 7.7.0 pre-release at 1babb324
- Catch libdeltacloud 0.8 update

* Fri May 20 2011 <matt@redhat> - 7.7.0-0.2
- Added GSI support, dependency on Globus

* Fri May 13 2011 <matt@redhat> - 7.7.0-0.1
- Fast forward to 7.7.0 pre-release at 79952d6b
- Introduced ec2_gahp
- 79952d6b brings schema expectations inline with Cumin

* Tue May 10 2011 <matt@redhat> - 7.6.1-0.1
- Upgrade to 7.6.0 release, pre-release of 7.6.1 at 5617a464
- Upstreamed patch: log_lock_run.patch
- Introduced condor-classads to obsolete classads
- Introduced condor-aviary, package of the aviary contrib
- Introduced condor-deltacloud-gahp
- Introduced condor-qmf, package of the mgmt/qmf contrib
- Transitioned from LOCAL_CONFIG_FILE to LOCAL_CONFIG_DIR
- Stopped building against gSOAP,
-  use aviary over birdbath and ec2_gahp (7.7.0) over amazon_gahp

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.5.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 27 2011 <matt@redhat> - 7.5.5-1
- Rebase to 7.5.5 release
-  configure+imake -> cmake
-  Removed patches:
-   only_dynamic_unstripped.patch
-   gsoap-2.7.16-wsseapi.patch
-   gsoap-2.7.16-dom.patch
-  man pages are now built with source
-  quill is no longer present
-  condor_shared_port added
-  condor_power added
-  condor_credd added
-  classads now built from source

* Thu Jan 13 2011 <matt@redhat> - 7.4.4-1
- Upgrade to 7.4.4 release
- Upstreamed: stdsoap2.h.patch.patch

* Mon Aug 23 2010  <matt@redhat> - 7.4.3-1
- Upgrade to 7.4.3 release
- Upstreamed: dso_link_change

* Fri Jun 11 2010  <matt@redhat> - 7.4.2-2
- Rebuild for classads DSO version change (1:0:0)
- Updated stdsoap2.h.patch.patch for gsoap 2.7.16
- Added gsoap-2.7.16-wsseapi/dom.patch for gsoap 2.7.16

* Wed Apr 21 2010  <matt@redhat> - 7.4.2-1
- Upgrade to 7.4.2 release

* Tue Jan  5 2010  <matt@redhat> - 7.4.1-1
- Upgrade to 7.4.1 release
- Upstreamed: guess_version_from_release_dir, fix_platform_check
- Security update (BZ549577)

* Fri Dec  4 2009  <matt@redhat> - 7.4.0-1
- Upgrade to 7.4.0 release
- Fixed POSTIN error (BZ540439)
- Removed NOTICE.txt source, now provided by upstream
- Removed no_rpmdb_query.patch, applied upstream
- Removed no_basename.patch, applied upstream
- Added only_dynamic_unstripped.patch to reduce build time
- Added guess_version_from_release_dir.patch, for previous
- Added fix_platform_check.patch
- Use new --with-platform, to avoid modification of make_final_tarballs
- Introduced vm-gahp package to hold libvirt deps

* Fri Aug 28 2009  <matt@redhat> - 7.2.4-1
- Upgrade to 7.2.4 release
- Removed gcc44_const.patch, accepted upstream
- New log, lock, run locations (BZ502175)
- Filtered innocuous semanage message

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 7.2.1-3
- rebuilt with new openssl

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Feb 25 2009  <matt@redhat> - 7.2.1-1
- Upgraded to 7.2.1 release
- Pruned changes accepted upstream from condor_config.generic.patch
- Removed Requires in favor of automatic dependencies on SONAMEs
- Added no_rmpdb_query.patch to avoid rpm -q during a build

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.2.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jan 15 2009 Tomas Mraz <tmraz@redhat.com> - 7.2.0-4
- rebuild with new openssl

* Mon Jan 14 2009  <matt@redhat> - 7.2.0-3
- Fixed regression: initscript was on by default, now off again

* Thu Jan  8 2009  <matt@redhat> - 7.2.0-2
- (Re)added CONDOR_DEVELOPERS=NONE to the default condor_config.local
- Added missing Obsoletes for condor-static (thanks Michael Schwendt)

* Wed Jan  7 2009  <matt@redhat> - 7.2.0-1
- Upgraded to 7.2.0 release
- Removed -static package
- Added Fedora specific buildid
- Enabled KBDD, daemon to monitor X usage on systems with only USB devs
- Updated install process

* Wed Oct  8 2008  <matt@redhat> - 7.0.5-1
- Rebased on 7.0.5, security update

* Wed Aug  6 2008  <mfarrellee@redhat> - 7.0.4-1
- Updated to 7.0.4 source
- Stopped using condor_configure in install step

* Tue Jun 10 2008  <mfarrellee@redhat> - 7.0.2-1
- Updated to 7.0.2 source
- Updated config, specifically HOSTALLOW_WRITE, for Personal Condor setup
- Added condor_config.generic

* Mon Apr  7 2008  <mfarrellee@redhat> - 7.0.0-8
- Modified init script to be off by default, resolves bz441279

* Fri Apr  4 2008  <mfarrellee@redhat> - 7.0.0-7
- Updated to handle changes in gsoap dependency

* Mon Feb 11 2008  <mfarrellee@redhat> - 7.0.0-6
- Added note about how to download the source
- Added generate-tarball.sh script

* Sun Feb 10 2008  <mfarrellee@redhat> - 7.0.0-5
- The gsoap package is compiled with --disable-namespaces, which means
  soap_set_namespaces is required after each soap_init. The
  gsoap_nonamespaces.patch handles this.

* Fri Feb  8 2008  <mfarrellee@redhat> - 7.0.0-4
- Added patch to detect GCC 4.3.0 on F9
- Added patch to detect GLIBC 2.7.90 on F9
- Added BuildRequires: autoconf to allow for regeneration of configure
  script after GCC 4.3.0 detection and GLIBC 2.7.90 patches are
  applied
- Condor + GCC 4.3.0 + -O2 results in an internal compiler error
  (BZ 432090), so -O2 is removed from optflags for the time
  being. Thanks to Mike Bonnet for the suggestion on how to filter
  -O2.

* Tue Jan 22 2008  <mfarrellee@redhat> - 7.0.0-3
- Update to UW's really-final source for Condor 7.0.0 stable series
  release. It is based on the 72173 build with minor changes to the
  configure.ac related to the SRB external version.
- In addition to removing externals from the UW tarball, the NTconfig
  directory was removed because it had not gone through IP audit.

* Tue Jan 22 2008  <mfarrellee@redhat> - 7.0.0-2
- Update to UW's final source for Condor 7.0.0 stable series release

* Thu Jan 10 2008  <mfarrellee@redhat> - 7.0.0-1
- Initial package of Condor's stable series under ASL 2.0
- is_clipped.patch replaced with --without-full-port option to configure
- zlib_is_soft.patch removed, outdated by configure.ac changes
- removed autoconf dependency needed for zlib_is_soft.patch

* Tue Dec  4 2007  <mfarrellee@redhat> - 6.9.5-2
- SELinux was stopping useradd in pre because files specified root as
  the group owner for /var/lib/condor, fixed, much thanks to Phil Knirsch

* Fri Nov 30 2007  <mfarrellee@redhat> - 6.9.5-1
- Fixed release tag
- Added gSOAP support and packaged WSDL files

* Thu Nov 29 2007  <mfarrellee@redhat> - 6.9.5-0.2
- Packaged LSB init script
- Changed pre to not create the condor user's home directory, it is
  now a directory owned by the package

* Thu Nov 29 2007  <mfarrellee@redhat> - 6.9.5-0.1
- Condor 6.9.5 release, the 7.0.0 stable series candidate
- Removed x86_64_no_multilib-200711091700cvs.patch, merged upstream
- Added patch to make zlib a soft requirement, which it should be
- Disabled use of smp_mflags because of make dependency issues
- Explicitly not packaging WSDL files until the SOAP APIs are available

* Tue Nov 20 2007  <mfarrellee@redhat> - 6.9.5-0.3.200711091700cvs
- Rebuild for repo inheritance update: dependencies are now pulled
  from RHEL 5 U1 before RH Application Stack

* Thu Nov 15 2007 <mfarrellee@redhat> - 6.9.5-0.2.200711091700cvs
- Added support for building on x86_64 without multilib packages
- Made the install section more flexible, reduced need for
  make_final_tarballs to be updated

* Fri Nov 9 2007 <mfarrellee@redhat> - 6.9.5-0.1.200711091700cvs
- Working source with new ASL 2.0 license

* Fri Nov 9 2007 <mfarrellee@redhat> - 6.9.5-0.1.200711091330cvs
- Source is now stamped ASL 2.0, as of Nov 9 2007 1:30PM Central
- Changed license to ASL 2.0
- Fixed find in prep to work if no files have bad permissions
- Changed the name of the LICENSE file to match was is now release in
  the source tarball

* Tue Nov 6 2007  <mfarrellee@redhat> - 6.9.5-0.1.rc
- Added m4 dependency not in RHEL 5.1's base
- Changed chmod a-x script to use find as more files appear to have
  improper execute bits set
- Added ?dist to Release:
- condor_privsep became condor_root_switchboard

* Tue Sep 11 2007  <mfarrellee@redhat> - 6.9.5-0.3.20070907cvs
- Instead of releasing libcondorapi.so, which is improperly created
  and poorly versioned, we release libcondorapi.a, which is apparently
  more widely used, in a -static package
- Instead of installing the stripped tarball, the unstripped is now
  installed, which gives a nice debuginfo package
- Found and fixed permissions problems on a number of src files,
  issue raised by rpmlint on the debuginfo package

* Mon Sep 10 2007  <mfarrellee@redhat> - 6.9.5-0.2.20070907cvs
- Updated pre section to create condor's home directory with adduser, and
  removed _var/lib/condor from files section
- Added doc LICENSE.TXT to all files sections
- Shortened lines longer than 80 characters in this spec (except the sed line)
- Changed install section so untar'ing a release can handle fedora7 or fedora8
- Simplified the site.def and config file updates (sed + mv over mv + sed + rm)
- Added a patch (fedora_rawhide_7.91-20070907cvs.patch) to support building on
  a fedora 7.91 (current Rawhide) release
- Moved the examples from /usr/share/doc/condor... into builddir and just
  marked them as documentation
- Added a number of dir directives to force all files to be listed, no implicit
  inclusion

* Fri Sep  7 2007  <mfarrellee@redhat> - 6.9.5-0.1.20070907cvs
- Initial release
