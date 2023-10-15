import sys,string

sys.path.append("/opt/opsware")

from waybot.base import signor
from coglib import spinwrapper
from coglib import certmaster

spin = spinwrapper.SpinWrapper(ctx = certmaster.getContextByName("spin", "spin.srv", "opsware-ca.crt"))

sign_classes = ['SecurityUser', 
  'SecurityRole', 
  'SecurityPermission', 
  'SecurityPrivilege', 
  'SecurityRoleUser', 
  'SecurityRolePermission', 
  'WayScript', 
  'WayScriptVersion', 
  'SessionCommand',
  'Session',
  'Schedule']

sDefAnswer = "x"
nStartArg = 1
if ( len(sys.argv) > 1 and sys.argv[1][0] == "-" ):
  sDefAnswer = sys.argv[1][1]
  nStartArg = 2

_wsv_parent_names = {}
def getWSVParentName(wsv):
  if (_wsv_parent_names.has_key(wsv['id'])):
    return _wsv_parent_names[wsv['id']]
  wsv_parent_name = wsv.getParent(parent_class="WayScript")['script_name']
  _wsv_parent_names[wsv['id']] = wsv_parent_name
  return wsv_parent_name

def checkWayObjSig(sClassName, sWO_ID):
  wo = getattr(spin,sClassName).get(id=sWO_ID)

  wo_name = str(sWO_ID)
  if ( wo['obj_class'] == "WayScript" ):
    wo_name = "%s (%s)" % (wo['script_name'], sWO_ID)
  elif ( wo['obj_class'] == "SecurityRole" ):
    wo_name = "%s (%s)" % (wo['role_name'], sWO_ID)
  elif ( wo['obj_class'] == "SecurityUser" ):
    wo_name = "%s (%s)" % (wo['username'], sWO_ID)
  elif ( wo['obj_class'] == "SecurityPrivilege" ):
    wo_name = "%s (%s)" % (wo['privilege_name'], sWO_ID)
  elif ( wo['obj_class'] == "WayScriptVersion" ):
    wo_name = "%s (%s) (%s)" % (getWSVParentName(wo), wo['version'], sWO_ID)

  if ( signor.verify(wo) ):
     sys.stdout.write( "%s '%s' has a valid signature.\n" % (wo['obj_class'], wo_name) )
  else:
      sys.stdout.write( "%s '%s' DOES NOT HAVE a valid signature.\n\n" % (wo['obj_class'], wo_name) )
      sys.stdout.write( "Current signature is:\n\n%s\n\n" % wo['signature'] )
      sNewSig = signor.make_sig_by_type(wo.data,wo["obj_class"])
      sys.stdout.write( "Expected signature is:\n\n%s\n\n" % sNewSig )

      sAnswer = sDefAnswer
      while ( not( sAnswer[0] in "ynYN" ) ):
        sys.stdout.write( "Would you like to resign this %s? [yn]" % wo['obj_class'] )
        sAnswer = sys.stdin.read(1)

      sys.stdout.write( "\n" )
      if ( len(sAnswer) > 0 and sAnswer[0] in "yY" ):
        wo.update( signature=sNewSig )
        sys.stdout.write( "%s '%s' resigned.\n" % (wo['obj_class'], wo_name) )
      else:
        sys.stdout.write( "%s '%s' not modified.\n" % (wo['obj_class'], wo_name) )

def checkAllWayObjSigs( sClassName ):
  for wo_id in getattr(spin,sClassName).getIDList():
    checkWayObjSig(sClassName, wo_id)

if (nStartArg < len(sys.argv)):
  sClassName = "WayScript"

  for sWO_ID in sys.argv[nStartArg:]:
    if (sWO_ID in sign_classes):
      sClassName = sWO_ID
      continue
    if ( string.lower(sWO_ID) == "all" ):
      checkAllWayObjSigs( sClassName )
    else:
      checkWayObjSig(sClassName, sWO_ID)
else:
  for sCurClass in sign_classes:
    checkAllWayObjSigs(sCurClass)