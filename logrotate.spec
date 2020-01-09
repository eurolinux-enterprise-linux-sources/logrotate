Summary: Rotates, compresses, removes and mails system log files
Name: logrotate
Version: 3.7.8
Release: 23%{?dist}
License: GPL+
URL: https://fedorahosted.org/logrotate/
Group: System Environment/Base
Source: https://fedorahosted.org/releases/l/o/logrotate/logrotate-%{version}.tar.gz
Patch1: logrotate-3.7.7-curdir2.patch
Patch2: logrotate-3.7.7-toolarge.patch
Patch4: logrotate-3.7.8-man5.patch
Patch5: logrotate-3.7.8-missingok.patch
Patch6: logrotate-3.7.8-configsize.patch
Patch7: logrotate-3.7.8-dont-remove-log.patch
Patch8: logrotate-3.7.8-scripts-args.patch
Patch9: logrotate-3.7.8-scripts-man.patch
Patch10: logrotate-3.7.8-handle-rename-error.patch
Patch11: logrotate-3.7.9-shred.patch
Patch12: logrotate-3.7.9-statefile.patch
Patch13: logrotate-3.7.9-atomic-create.patch
Patch14: logrotate-3.7.9-acl.patch
Patch15: logrotate-3.8.0-brace.patch
Patch16: logrotate-3.8.0-man.patch
Patch17: logrotate-3.8.0-mail-delay.patch
Patch18: logrotate-3.7.8-useless-chown.patch
Patch19: logrotate-3.7.8-umask.patch
Patch20: logrotate-3.7.8-selinux-compress.patch
Patch21: logrotate-3.7.8-unlink-temp.patch
Patch22: logrotate-3.7.8-acl-vs-chmod.patch
Patch23: logrotate-3.7.8-sortglob.patch
Patch24: logrotate-3.7.8-atomic-statefile.patch
Patch25: logrotate-3.7.8-maxsize.patch
Patch26: logrotate-3.7.8-createolddir.patch
Patch28: logrotate-3.7.8-covscan.path

Requires: coreutils >= 5.92 libsepol libselinux popt
BuildRequires: libselinux-devel popt-devel libacl-devel
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
The logrotate utility is designed to simplify the administration of
log files on a system which generates a lot of log files.  Logrotate
allows for the automatic rotation compression, removal and mailing of
log files.  Logrotate can be set to handle a log file daily, weekly,
monthly or when the log file gets to a certain size.  Normally,
logrotate runs as a daily cron job.

Install the logrotate package if you need a utility to deal with the
log files on your system.

%prep
%setup -q
%patch1 -p1 -b .curdir
%patch2 -p1 -b .toolarge
%patch4 -p1 -b .man5
%patch5 -p1 -b .missingok
%patch6 -b .configsize
%patch7 -b .dont-remove-log
%patch8 -b .scripts-args
%patch9 -b .scripts-man
%patch10 -b .handle-rename-error
%patch11 -p1 -b .shred
%patch12 -b .statefile
%patch13 -p1 -b .atomic-log-create
%patch14 -p1 -b .acl
%patch15 -p1 -b .brace
%patch16 -p1 -b .man
%patch17 -p1 -b .mail-delay
%patch18 -p1 -b .useless-chown
%patch19 -p1 -b .umask
%patch20 -p1 -b .selinuxcompress
%patch21 -p1 -b .unlinktemp
%patch22 -p1 -b .aclvschmod
%patch23 -p1 -b .sortglob
%patch24 -p1 -b .atomicstate
%patch25 -p1 -b .maxsize
%patch26 -p1 -b .createolddir
%patch28 -p1 -b .covscan

%build
make %{?_smp_mflags} RPM_OPT_FLAGS="$RPM_OPT_FLAGS" WITH_SELINUX=yes WITH_ACL=yes

%install
rm -rf $RPM_BUILD_ROOT
make PREFIX=$RPM_BUILD_ROOT MANDIR=%{_mandir} install
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/logrotate.d
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/cron.daily
mkdir -p $RPM_BUILD_ROOT/%{_localstatedir}/lib

install -p -m 644 examples/logrotate-default $RPM_BUILD_ROOT/%{_sysconfdir}/logrotate.conf
install -p -m 755 examples/logrotate.cron $RPM_BUILD_ROOT/%{_sysconfdir}/cron.daily/logrotate
touch $RPM_BUILD_ROOT/%{_localstatedir}/lib/logrotate.status

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc CHANGES COPYING
%attr(0755, root, root) %{_sbindir}/logrotate
%attr(0644, root, root) %{_mandir}/man8/logrotate.8*
%attr(0644, root, root) %{_mandir}/man5/logrotate.conf.5*
%attr(0700, root, root) %config(noreplace) %{_sysconfdir}/cron.daily/logrotate
%attr(0644, root, root) %config(noreplace) %{_sysconfdir}/logrotate.conf
%attr(0755, root, root) %dir %{_sysconfdir}/logrotate.d
%attr(0644, root, root) %verify(not size md5 mtime) %config(noreplace) %{_localstatedir}/lib/logrotate.status

%changelog
* Mon Mar 09 2015 Jan Kaluza <jkaluza@redhat.com> 3.7.8-23
- revert fix #1177970

* Tue Mar 03 2015 Jan Kaluza <jkaluza@redhat.com> 3.7.8-22
- fix #1177970 - fix the potential leaks in previous patch

* Thu Feb 26 2015 Jan Kaluza <jkaluza@redhat.com> 3.7.8-21
- fix #1177970 - do not fail if log is removed during rotation

* Tue Feb 03 2015 Jan Kaluza <jkaluza@redhat.com> 3.7.8-20
- fix #1117189 - sort logs only when dateformat is set

* Thu Jan 29 2015 Jan Kaluza <jkaluza@redhat.com> 3.7.8-19
- fix #1047899 - add support for "maxsize" directive
- fix #1125769 - add support for "createolddir" directive

* Mon Dec 15 2014 Jan Kaluza <jkaluza@redhat.com> 3.7.8-18
- fix #722209 - do not redirect output of logrotate to /dev/null, mark
  logrotate.conf as config
- fix #1117189 - sort logs according to dateformat when removing the old one
- fix #625034 - update logrotate.status atomically
- fix #984965 - fix possible overflow in "create" directive parsing
- fix #1012485 - use permissions 0700 for cron.daily script

* Tue May 28 2013 Jan Kaluza <jkaluza@redhat.com> 3.7.8-17
- fix #841520 - do not try to change owner of log if it is not needed
- fix #848131 - fix bad umask value while creating temp file
- fix #920030 - set SELinux context before compress files creation
- fix #922169 - remove temp files on error
- fix #847338 - do not overwrite create directive value by ACL setting
- fix #847339 - fix race condition between fchmod and acl_set_fd

* Mon Aug 06 2012 Jan kaluza <jkaluza@redhat.com> 3.7.8-16
- fix #827570 - fixed mailing the log file with the "mailfirst"
  and "delaycompress" options

* Thu Feb 02 2012 Jan Kaluza <jkaluza@redhat.com> 3.7.8-15
- fix #674864 - fixed grammar mistakes in man-page

* Wed Feb 01 2012 Jan Kaluza <jkaluza@redhat.com> 3.7.8-14
- fix #683622 - add support for ACLs
- fix #736053 - check for brackets order in config file
- fix #659705, #659713, #659720 - fixed mistakes in man-page

* Thu Mar 17 2011 Jan Kaluza <jkaluza@redhat.com> 3.7.8-13
- fix #688519 - fixed CVE-2011-1154, CVE-2011-1155
  and CVE-2011-1098

* Thu Jun 24 2010 Jan Kaluza <jkaluza@redhat.com> 3.7.8-12
- fix #604073 - stop rotation if there is an error when
  renaming old logs

* Thu Jun 17 2010 Jan Kaluza <jkaluza@redhat.com> 3.7.8-11
- fix #604981 - update manpage to reflect scripts changes

* Thu Jun 17 2010 Jan Kaluza <jkaluza@redhat.com> 3.7.8-10
- fix #604686 - pass currently rotated file as argument to
  postrotate/prerotate script in nosharedscripts mode

* Tue Jun 15 2010 Jan Kaluza <jkaluza@redhat.com> 3.7.8-9
- fix #604073 - do not remove log if there is an error in
  rotate process

* Fri Jun 11 2010 Jan Kaluza <jkaluza@redhat.com> 3.7.8-8
- fix #602654 - fix integer overflow in size and minsize

* Tue Apr 06 2010 Daniel Novotny <dnovotny@redhat.com> 3.7.8-7
- fix #578116 - missingok problem with globs

* Wed Feb 24 2010 Daniel Novotny <dnovotny@redhat.com> 3.7.8-6
- added upstream URL

* Thu Nov 12 2009 Daniel Novotny <dnovotny@redhat.com> 3.7.8-5
- fix #525659 (man page for logrotate.conf)

* Thu Sep 17 2009 Daniel Novotny <dnovotny@redhat.com> 3.7.8-4
- fix #517321 (logrotate blocking anacron)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.7.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.7.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 02 2009 Daniel Novotny <dnovotny@redhat.com> 3.7.8-1
- new upstream version 3.7.8

* Fri Nov 21 2008 Daniel Novotny <dnovotny@redhat.com> 3.7.7-4
- fix #468926 (segfault with very large /var/log/messages)

* Thu Nov 20 2008 Daniel Novotny <dnovotny@redhat.com> 3.7.7-3
- less aggressive approach to the fix

* Thu Nov 20 2008 Daniel Novotny <dnovotny@redhat.com> 3.7.7-2
- fix #471463 (selinux problems with logrotate)

* Mon May 19 2008 Tomas Smetana <tsmetana@redhat.com> 3.7.7-1
- new upstream version

* Wed Apr 23 2008 Tomas Smetana <tsmetana@redhat.com> 3.7.6-4
- improve patch for #432330
- fix #437748 - don't forget to close log files

* Mon Feb 11 2008 Tomas Smetana <tsmetana@redhat.com> 3.7.6-3
- fix #432330 segfault on corrupted status file

* Mon Jan 21 2008 Tomas Smetana <tsmetana@redhat.com> 3.7.6-2.2
- fix #429454 - logrotate fails due to invalid pointer

* Wed Jan 09 2008 Tomas Smetana <tsmetana@redhat.com> 3.7.6-2.1
- fix the selinux patch

* Wed Jan 09 2008 Tomas Smetana <tsmetana@redhat.com> 3.7.6-2
- fix #427274 - logrotate fails to preserve SELinux file contexts
- fix #427661 - SELinux stops vsftpd from working correctly

* Thu Sep 27 2007 Tomas Smetana <tsmetana@redhat.com> 3.7.6-1.3
- popt-devel dependency was still missing

* Thu Sep 27 2007 Tomas Smetana <tsmetana@redhat.com> 3.7.6-1.2
- add missing dependencies to spec file

* Thu Aug 23 2007 Tomas Smetana <tsmetana@redhat.com> 3.7.6-1.1
- rebuild

* Tue Aug 07 2007 Tomas Smetana <tsmetana@redhat.com> 3.7.6-1
- new upstream version
- fix #248565 logrotate never rotates /var/log/btmp
- fix compile warnings
- tabooext accepts wildcards (related #247816)
- fix minor errors and update man page (related #250059)
- fix handling of size directive (related #247410)

* Thu May 31 2007 Tomas Smetana <tsmetana@redhat.com> 3.7.5-5
- fix ignoring pre/postrotate arguments (related #241766)

* Wed May 23 2007 Tomas Smetana <tsmetana@redhat.com> 3.7.5-4
- use dateext in the default config file (#240292)
- add options to use shred for deleting files -- adapt patch sent by
  Peter Eckersley <pde@eff.org> (#239934)
- ignore .cfsaved files by default (#223476)

* Sat Mar 31 2007 Peter Vrabec <pvrabec@redhat.com> 3.7.5-3
- add error checking before running prerotate and postrotate scripts

* Thu Mar 29 2007 Peter Vrabec <pvrabec@redhat.com> 3.7.5-2
- fix error hadnling after prerotate, postrotate, firstaction 
  script failure. (http://qa.mandriva.com/show_bug.cgi?id=29979)

* Thu Mar 01 2007 Peter Vrabec <pvrabec@redhat.com> 3.7.5-1
- new upstream release.

* Fri Feb 09 2007 Peter Vrabec <pvrabec@redhat.com> 3.7.4-13
- another spec file fixes (#226104)

* Thu Feb 08 2007 Peter Vrabec <pvrabec@redhat.com> 3.7.4-12
- fix problem with compress_options_list (#227706)
- fix spec file to meet Fedora standards (#226104)

* Tue Jan 23 2007 Peter Vrabec <pvrabec@redhat.com> 3.7.4-11
- logrotate won't stop if there are some errors in configuration
  or glob failures (#166510, #182062)

* Wed Jan 10 2007 Peter Vrabec <pvrabec@redhat.com> 3.7.4-10
- fix some rpmlint issues

* Tue Jan 09 2007 Peter Vrabec <pvrabec@redhat.com> 3.7.4-9
- allow multibyte characters in readPath() (#122145)

* Fri Jan 05 2007 Peter Vrabec <pvrabec@redhat.com> 3.7.4-8
- "size" option was ignored in config files (#221341)

* Sun Oct 01 2006 Jesse Keating <jkeating@redhat.com> - 3.7.4-7
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Tue Sep 26 2006 Peter Vrabec <pvrabec@redhat.com> 3.7.4-6
- fix leaking file descriptor (#205072)

* Wed Aug 09 2006 Dan Walsh <dwalsh@redhat.com> 3.7.4-5
- Use selinux raw functions

* Mon Jul 24 2006 Peter Vrabec <pvrabec@redhat.com> 3.7.4-4
- make error message, about ignoring certain config files,
  a debug message instead (#196052)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 3.7.4-3.1
- rebuild

* Tue Jun 13 2006 Peter Vrabec <pvrabec@redhat.com> 3.7.4-3
- rename ENOSUP to ENOTSUP

* Tue Jun 13 2006 Peter Vrabec <pvrabec@redhat.com> 3.7.4-2
- clean up a couple of SELinux problems. Patch from Daniel J. Walsh.

* Wed May 17 2006 Peter Vrabec <pvrabec@redhat.com> 3.7.4-1
- add new "minsize" option (#173088)

* Tue Mar 28 2006 Peter Vrabec <pvrabec@redhat.com> 3.7.3-3
- correct man page "extension" option description  (#185318)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 3.7.3-2.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 3.7.3-2.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Sun Nov 13 2005 Peter Vrabec <pvrabec@redhat.com> 3.7.3-2
- fix_free_segfaults (#172918)

* Sat Nov 12 2005 Peter Vrabec <pvrabec@redhat.com> 3.7.3-1
- new upstream release
- indent sources

* Fri Nov 11 2005 Peter Vrabec <pvrabec@redhat.com> 3.7.2-12
- fix_free_segfaults (#172918)

* Mon Nov 07 2005 Peter Vrabec <pvrabec@redhat.com> 3.7.2-11
- man description for "nodateext" option (#171577)
- remove not working "pattern" option (#171577)

* Tue Oct 25 2005 Peter Vrabec <pvrabec@redhat.com> 3.7.2-10
- some more clean up (#171587)

* Thu Oct 20 2005 Peter Vrabec <pvrabec@redhat.com> 3.7.2-9
- fix_free_segfaults (#171093)

* Tue Oct 18 2005 Peter Vrabec <pvrabec@redhat.com> 3.7.2-8
- fix leaks of tabooExts

* Sat Oct 15 2005 Peter Vrabec <pvrabec@redhat.com> 3.7.2-7
- fix_free_segfaults (#170904)

* Wed Oct 12 2005 Peter Vrabec <pvrabec@redhat.com> 3.7.2-6
- code clean up (#169885)

* Mon Oct 10 2005 Peter Vrabec <pvrabec@redhat.com> 3.7.2-5
- fix bug introduced in logrotate 3.7.2-3(#169858)
- fix some memory leaks (#169888)

* Fri Sep 23 2005 Peter Vrabec <pvrabec@redhat.com> 3.7.2-4
- do not run compression program in debug mode (#166912)

* Wed Sep 07 2005 Peter Vrabec <pvrabec@redhat.com> 3.7.2-3
- even when sharedscript option used, do postrotate 
  script before compress (#167575)

* Wed Aug 17 2005 Peter Vrabec <pvrabec@redhat.com> 3.7.2-2
- allow yearly rotations(#134612)

* Mon Aug 01 2005 Peter Vrabec <pvrabec@redhat.com> 3.7.2-1
- new upstream release

* Tue Jul 26 2005 Peter Vrabec <pvrabec@redhat.com> 3.7.1-14
- fix some "error running script" messages

* Tue Jul 26 2005 Peter Vrabec <pvrabec@redhat.com> 3.7.1-13
- fix man page (#163458,#163366)

* Wed Jun 22 2005 Peter Vrabec <pvrabec@redhat.com> 3.7.1-12
- enhance logrotate with "dateext", "maxage"

* Thu Mar 31 2005 Dan Walsh <dwalsh@redhat.com> 3.7.1-10
- use security_getenforce() instead of selinux_getenforcemode

* Thu Mar 17 2005 Dan Walsh <dwalsh@redhat.com> 3.7.1-9
- Add selinux_getenforce() calls to work when not in enforcing mode

* Thu Mar 17 2005 Peter Vrabec <pvrabec@redhat.com> 3.7.1-8
- rebuild

* Tue Feb 22 2005 Peter Vrabec <pvrabec@redhat.com>
- do not use tmpfile to run script anymore (#149270)

* Fri Feb 18 2005 Peter Vrabec <pvrabec@redhat.com>
- remove logrotate-3.7.1-share.patch, it doesn't solve (#140353)

* Mon Dec 13 2004 Peter Vrabec <pvrabec@redhat.com> - 3.7.1-5
- Add section to logrotate.conf for "/var/log/btmp" (#117844)

* Mon Dec 13 2004 Peter Vrabec <pvrabec@redhat.com> - 3.7.1-4
- Typo and missing information in man page (#139346)

* Mon Dec 06 2004 Peter Vrabec <pvrabec@redhat.com> - 3.7.1-3
- compressed logfiles and logrotate (#140353)

* Tue Oct 19 2004 Miloslav Trmac <mitr@redhat.com> - 3.7.1-2
- Fix sending mails (#131583)
- Preserve file attributes when compressing files (#121523, original patch by
  Daniel Himler)

* Fri Jul 16 2004 Elliot Lee <sopwith@redhat.com> 3.7.1-1
- Fix #126490 typo

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Jan 26 2004 Dan Walsh <dwalsh@redhat.com> 3.6.10-4
- fix is_selinux_enabled call

* Fri Sep 5 2003 Dan Walsh <dwalsh@redhat.com> 3.6.10-3
- Turn off selinux

* Fri Sep 5 2003 Dan Walsh <dwalsh@redhat.com> 3.6.10-2.sel
- Turn on selinux

* Wed Aug 06 2003 Erik Troan <ewt@redhat.com>
- always use compressext for the extension for compressed
  files; before compresscmd and compressext had to agree
- moved all compression to one code block
- compression, scripts don't use system() anymore
- compress and maillast didn't work together properly
- delaycompress and mailfirst didn't work properly
- don't use system() for mailing (or uncompressing) logs anymore
- use "-s" for speciying the subjected of mailed logs

* Thu Jul 24 2003 Elliot Lee <sopwith@redhat.com> 3.6.10-1
- Fix #100546, change selinux port.

* Wed Jul 18 2003 Dan Walsh <dwalsh@redhat.com> 3.6.9-2
- Port to SELinux 2.5

* Wed Jul 09 2003 Elliot Lee <sopwith@redhat.com> 3.6.9-1
- Fix #90229, #90274, #89458, #91408

* Mon Jan 20 2003 Elliot Lee <sopwith@redhat.com> 3.6.8-1
- Old patch from pm@debian.org

* Tue Jan 14 2003 Elliot Lee <sopwith@redhat.com> 3.6.7-1
- Fixes from bugzilla

* Fri Nov 15 2002 Elliot Lee <sopwith@redhat.com> 3.6.6-1
- Commit patch from Fidelis Assis <fidelis@embratel.net.br>

* Thu Jun 20 2002 Elliot Lee <sopwith@redhat.com> 3.6.5-1
- Commit fix for #65299

* Mon Apr 15 2002 Elliot Lee <sopwith@redhat.com> 3.6.4-1
- Commit fix for #62560

* Wed Mar 13 2002 Elliot Lee <sopwith@redhat.com> 3.6.3-1
- Apply various bugfix patches from the openwall people

* Tue Jan 29 2002 Elliot Lee <sopwith@redhat.com> 3.6.2-1
- Fix bug #55809 (include logrotate.status in "files")
- Fix bug #58328 (incorrect error detection when reading state file)
- Allow 'G' size specifier from bug #57242

* Mon Dec 10 2001 Preston Brown <pbrown@redhat.com>
- noreplace config file

* Wed Nov 28 2001 Preston Brown <pbrown@redhat.com> 3.6-1
- patch from Alexander Kourakos <awk@awks.org> to stop the shared
  postrotate/prerotate scripts from running if none of the log(s) need
  rotating.  All log files are now checked for rotation in one batch,
  rather than sequentially.
- more fixes from Paul Martin <pm@debian.org>

* Thu Nov  8 2001 Preston Brown <pbrown@redhat.com> 3.5.10-1
- fix from paul martin <pm@debian.org> for zero-length state files

* Tue Sep  4 2001 Preston Brown <pbrown@redhat.com>
- fix segfault when logfile is in current directory.

* Tue Aug 21 2001 Preston Brown <pbrown@redhat.com>
- fix URL for source location

* Thu Aug  2 2001 Preston Brown <pbrown@redhat.com>
- man page cleanups, check for negative rotation counts

* Mon Jul  2 2001 Preston Brown <pbrown@redhat.com>
- more minor manpage updates (#45625)

* Thu Jun 21 2001 Preston Brown <pbrown@redhat.com> 3.5.6-1
- enable LFS support (debian bug #100810)
- quote filenames for running compress commands or pre/postrotate cmds (#21348)
- deprecate "errors" directive (see bug #16544 for explanation)
- update man page
- configurable compression command by Colm Buckley <colm@tuatha.org>

* Fri Jun  1 2001 Preston Brown <pbrown@redhat.com> 3.5.5-1
- be less strict about whitespace near filenames.  Patch from Paul Martin <pm@debian.org>.

* Thu Jan  4 2001 Bill Nottingham <notting@redhat.com>
- %%defattr

* Wed Jan 03 2001 Preston Brown <pbrown@redhat.com>
- see CHANGES

* Tue Aug 15 2000 Erik Troan <ewt@redhat.com>
- see CHANGES

* Sun Jul 23 2000 Erik Troan <ewt@redhat.com>
- see CHANGES

* Tue Jul 11 2000 Erik Troan <ewt@redhat.com>
- support spaces in filenames
- added sharedscripts

* Sun Jun 18 2000 Matt Wilson <msw@redhat.com>
- use %%{_mandir} for man pages

* Thu Feb 24 2000 Erik Troan <ewt@redhat.com>
- don't rotate lastlog

* Thu Feb 03 2000 Erik Troan <ewt@redhat.com>
- gzipped manpages
