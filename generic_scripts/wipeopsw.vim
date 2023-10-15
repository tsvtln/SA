#!/bin/sh
########################################################################
#
# Remove all HP SA / SAR / BSAE / Oracle bits and data quickly (bypasses installer) 
#
#
# Works on both Linux and Solaris cores.  Relatively quick and especially useful
# if the Opsware Installer is in a bad state.  After running this tool you can 
# freshly install SAS and BSAE.  /var/tmp and /root are untouched, so you can
# easily reuse repsonse files.
#
# General idea:
#    Stop opsware services
#    Remove all OPSW* rpms using rpm -e to clean up the bulk of the bits
#    Remove all bsae-* rpms using rpm -e to clean up the bulk of the bits
#    rm -rf opsware and oracle directories
#    Remove users, groups, ogfs mounts, other random stuff possibly left behind.
#
#
########################################################################

[ "$UID" -ne 0 ] && { echo "You must run this script as root.  Aborting."; exit 1; }

case `uname -s` in
     'SunOS') RPM=/opt/opsware/bin/rpm;;
     'Linux') RPM=/bin/rpm;;
     **) echo "ERROR: Unsupported platform"; exit 1;;
esac

for i in 10 9 8 7 6 5 4 3 2 1 ; do echo ""; done 
echo "****************************************************"
echo "*                                                  *"
echo "*      REMOVING ALL SA, SAR, BSAE, AND ORACLE      *"

if [ "$1" != "" ] && [ "$1" = "--nowait" ]; then
   echo "*    immediately! (--nowait option was used)       *"
else
   echo "*       from this machine in 30 seconds!           *"
fi
echo "*                                                  *"
echo "*                                                  *"
echo "*  This is a completely destructive removal that   *"
echo "*  does not use the Opsware Installer and cannot   *"
echo "*  be undone once started.  After a few minutes,   *"
echo "*  all existing Opsware software will be gone.     *"
echo "*                                                  *"
echo "*  Neither /root nor /var/tmp will be affected,    *"
echo "*  so your response files can be easily reused.    *"
echo "*                                                  *"
if [ "$1" != "" ] && [ "$1" = "--nowait" ]; then
   echo "*                                                  *"
else
   echo "*  Abort this script with Ctrl-C within 30 seconds *"
   echo "*  if you have any doubts about what you are doing *"
   echo "*                                                  *"
   echo "*  Bypass this delay by using the --nowait option  *"
   echo "*                                                  *"
fi
echo "****************************************************"
echo ""

if [ "$1" != "" ] && [ "$1" = "--nowait" ]; then
    echo "Skipping wait period since the --nowait option was used."
else
    sleep 19
    for i in 10 9 8 7 6 5 4 3 2 1 *BOOM* ; do sleep 1; echo $i; done 
fi

echo ""

# Stop all opsware services
echo "Making sure SA is stopped"
/etc/init.d/opsware-sas stop 2>/dev/null >/dev/null
echo "Making sure Standalone AAA is stopped"
/opt/opsware/twist-sar/twist.sh stop 2>/dev/null >/dev/null
echo "Making sure OMDB/SAR/BSAE is stopped"
/etc/init.d/opsware-omdb stop 2>/dev/null >/dev/null
echo "Making sure Oracle is stopped"
/etc/init.d/opsware-oracle stop 2>/dev/null >/dev/null

echo "Removing opsware services from system startup config"
if [ `uname` = Linux ]; then
   # Deregister opsware services from startup (linux)
   cd /etc/init.d; for i in `ls opsware* 2>/dev/null`; do chkconfig --del $i; done
else
   # Deregister opsware services from startup (solaris)
   cd /etc
   for i in /etc/rc*; do for j in `find . $i -name opsware\*`; do echo Removing $i\/$j; rm -f $i\/$j; done ; done
fi

# Remove OGFS mounts from /etc/fstab (Linux) or /etc/mnttab (SunOS)
if [ `uname` = Linux ]; then
   echo "Removing OGFS mounts from /etc/fstab"
   umount /var/opt/opsware/ogfs/export/store 2> /dev/null
   umount /var/opt/opsware/ogfs/export/audit 2> /dev/null

   perl -pi -e "s/#.*Opsware Global Filesystem mounts.*//" /etc/fstab 
   perl -pi -e "s/\/var\/opt\/opsware\/ogfs\/export.*//" /etc/fstab 
fi

if [ `uname` = SunOS ]; then
   echo "Removing OGFS mounts from /etc/mnttab"
   umount /var/opt/opsware/ogfs/mnt/audit 2> /dev/null
   umount /var/opt/opsware/ogfs/mnt/store 2> /dev/null

   #perl -pi -e "s/\/var\/opt\/opsware\/ogfs\/export.*//" /etc/mnttab
   #/var/opt/opsware/ogfs/export/store      /var/opt/opsware/ogfs/mnt/store lofs    rw,suid,dev=800010      1173799113
   #/var/opt/opsware/ogfs/export/audit      /var/opt/opsware/ogfs/mnt/audit lofs    rw,suid,dev=800010      1173799113
fi

# Uninstall all Opsware rpms twice, because dependencies stopped some the first time
if [ `uname` = SunOS ] && [ ! -f ${RPM} ] ; then
   echo "Opsware's rpm does not exist on this Solaris box!"
else
   for i in `$RPM -qa | grep "^OPSW" | grep -v OPSWrpm | awk -F "-3" '{print $1}' `; do echo "Removing $i"; $RPM -e $i; done 
   for i in `$RPM -qa | grep "^bsae-" | grep -v OPSWrpm | awk -F "-3" '{print $1}' `; do echo "Removing $i"; $RPM -e $i; done 
   for i in `$RPM -qa | grep "^OPSW" | grep -v OPSWrpm | awk -F "-3" '{print $1}' `; do echo "Trying to remove $i again since dependencies blocked removal the first time."; $RPM -e --nodeps $i; done 
   for i in `$RPM -qa | grep "^bsae-" | grep -v OPSWrpm`; do echo "Removing $i again, this time ignoring the rpm scripts, and supplying the full version info in case of duplicate packages"; $RPM --noscripts -e $i; done
   for i in `$RPM -qa | grep "^bsae-" | grep -v OPSWrpm | awk -F "-3" '{print $1}' `; do echo "One final attempt to remove $i, before giving up"; $RPM --noscripts -e $i; done

   # fyi, uses the -3 from version (e.g. -32.f) as field separator since there are dashes in some names.

   # One more time, just updating the rpm db.  Anything else will be removed by rm -rf
   for i in `$RPM -qa | grep "^OPSW" | grep -v OPSWrpm | awk -F "-3" '{print $1}' `; do $RPM --justdb -e $i; done 

   # OK to remove RPM now that the rpm operations are done
   echo "Removing OPSWrpm (this had to be last to allow the other RPMs to be removed)"
   $RPM -e OPSWrpm 2>/dev/null

fi

# Brute force remove everything left behind from opsware-owned directories
echo "Removing everything still left in opsware-owned directories: "
echo "   /etc/opt/opsware /opt/opsware /var/log/opsware /var/opt/opsware"
rm -rf /etc/opt/opsware /opt/opsware /var/log/opsware /var/opt/opsware

#Starting in omdb version 7.1, an incomplete (i.e. failed) upgrade will leave a file behind in /var/tmp
# in order to be able to resume if the upgrade is run again.  Since we're bypassing the installer
# here, we need to ensure that the flag file is gone.
rm -f /var/tmp/incomplete_omdb_upgrade

# Remove oracle dirs
echo "Removing everything left in oracle directories: /u01 /u02 /u03 /u04"
rm -rf /u01 /u02 /u03 /u04 

# Removes opsware startup scripts
echo "Removing opsware-startup scripts"
rm -f /etc/init.d/opsware-*
rm -f /etc/init.d/bsae-*

# tftp gets left behind, and during next install tftp.conf thinks it doesn't belong to opsware
# and blocks the install.  Since opsware won't install OS Provisioning Boot Server without 
# owning this file, we know it's ours and is safe to delete
if [ `uname` = Linux ]; then rm -f /etc/xinetd.d/tftp 2>/dev/null; fi

# Clean up other things that would normally be removed by rpm, just in case "rpm -e"
# failed due to corrupt rpm database, etc.
echo "Cleaning up the last few things"
rm -f /etc/oratab
rm -f /var/opt/oracle/oratab
rm -f /var/opt/oracle/OPSWoracle_install_status

userdel oracle 2>/dev/null
userdel omdb 2>/dev/null
groupdel dba 2>/dev/null
groupdel oinstall 2>/dev/null
echo ""

# Sometimes processes get left behind, particularly by BO.  We'll kill anything leftover here.
# RedHat users are created starting at id 500, solaris starting at 0000100
echo "Killing all leftover processes owned by user id 500, 501, 502, 503, 504, 0000100, 0000101"
pkill -9 -U 500,501,502,503,504,0000100,0000101

# Reboot the machine
#echo "Rebooting the machine in 10 seconds..."
#for i in 9 8 7 6 5 4 3 2 1 *BOOM* ; do sleep 1; echo $i; done 
#
#if [ `uname` = SunOS ]; then
#   reboot
#else
#   shutdown -r -y now
#fi

echo "Complete.  You may wish to reboot, but shouldn't have any problems if you don't"
echo ""
