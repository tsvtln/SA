#!/bin/sh

##
# Program Overview:
#
# This program dumps vairous information about a device under the credentials
# of a given user.
#
# Currently, this script depends on the spin, via local spinwrapper libraries,
# to lookup the userid of the given username.  This dependency could be 
# removed by having this script accept the userid on the command line.
#

if ( [ "$2" ]; ) then {
  sUserName="$1"
  sDvcId="$2"
} elif ( [ "$1" ]; ) then {
  sUserName="detuser"
  sDvcId="$1"
} else {
  echo Usage: $0 '[<username>] <dvc_id>'
  exit 1
} fi

# Locate twist private key.
EINSTEIN_KEY_PATH="/var/opt/opsware/crypto/twist/twist-key.pem"
if ( [ -f "$EINSTEIN_KEY_PATH" ]; ) then {
  sKeyPath="$EINSTEIN_KEY_PATH"
} else {
  echo $0: 'Could not locate twist private key on this system.  (Requires SAS 6.0 or higher.)'
  exit 1
} fi

# Locate the python interpreter.
EINSTEIN_PYTHON_BIN="/opt/opsware/bin/python"
if ( [ -f "$EINSTEIN_PYTHON_BIN" ]; ) then {
  sPythonCmd="env PYTHONPATH=/opt/opsware/pylibs $EINSTEIN_PYTHON_BIN"
  sOgshEnvPath="/bin:/usr/bin:/usr/local/bin:/usr/sbin:/opt/opsware/ogfs/bin"
  sTtlgCmd="/opt/opsware/ogfs/bin/ttlg"
} else {
  echo $0: 'Could not locate the opsware python interpreter on this system.  (Requires SAS 6.0 or higher.)'
  exit 1
} fi

# Locate the java interpreter and required libraries.
if ( [ -f "/opt/opsware/twist/lib/client/twistclient.jar" ]; ) then {
  sJavaCmd="`echo /opt/opsware/j*/bin/java | head -1` -classpath $0:/opt/opsware/twist/lib/client/twistclient.jar:/opt/opsware/bea/weblogic81/server/lib/wlclient.jar:/opt/opsware/twist/lib/opsware_common-latest.jar:/opt/opsware/twist/lib/spinclient-latest.jar:/opt/opsware/twist/lib/client/twistclient.jar:/opt/opsware/twist/lib/twist.jar:/opt/opsware/twist/lib/common-latest.jar"
} else {
  echo $0: 'Could not locate dependent twist jar libraries for the token generation step.  (Requires SAS 6.0 or higher.)'
  exit 1
} fi

# Attempt to locate the user id of this user from the spin.
nUserID=`$sPythonCmd -c "from coglib import spinwrapper;import string;import sys;sys.stdout.write(string.replace(str(spinwrapper.SpinWrapper()._AAAAaaUser.getList(name='$sUserName')[0][0]),'L',''))"`

# If no user id was found.
if ( [ \! "$nUserID" ]; ) then {
  echo $0: "'"$sUserName"'": Could not locate the userid of this user from the spin.
  exit 1
} fi

# Attempt to invoke the GetDeviceInfo class using the user/userid for the given device id.
$sJavaCmd GetDeviceInfo $sDvcId $sUserName $nUserID $sKeyPath

cat <<PYTHON_CODE | /opt/opsware/bin/python -c 'import sys,string;eval(compile(string.join(sys.stdin.readlines(), ""), "foo", "exec"))'
import sys, time
sys.path.append("/opt/opsware/pylibs")
from coglib import spinwrapper
def replDates(o):
  for k in o.keys():
    if (str(type(o[k])) == "<type 'xmlrpcdateTime'>"):
      o[k] = time.asctime(o[k].date() + (0,0,0))
  return o
spin = spinwrapper.SpinWrapper()
print "Installedi Units:"
d = spin.Device.get($sDvcId)
ius = d.getChildren(child_class="InstalledUnit")
for iu in ius:
  print "  iu: %s" % (str(replDates(iu)))
print "Recommended Patches:"
rps = d.getChildren(child_class="RecommendedPatch")
for rp in rps:
  print "  rp: %s" % (str(replDates(rp)))
PYTHON_CODE

exit 0
