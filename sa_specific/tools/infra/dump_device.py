#!/opt/opsware/bin/python

import sys
sys.path.append("/opt/opsware/pylibs")
from coglib import spinwrapper

spin = spinwrapper.SpinWrapper()

g_mapClassTree = { "class":"Device",
  "child_classes":[
    {"class":"Account"}
    {"class":"AppPolicy"}
  ]
}
    

lsSeenSpinObjs = []
def DumpSpinObj( mapClassTree, obj, nDepth=0 ):
  global lsSeenSpinObjs
  mapChildren = {}
  for sCurChildClass in mapClassTree['child_classes']:
    lsChildren = obj.getChildren(child_class=sCurChildClass)
    print "%s%s(%d Children)" % ( "  "*nDepth, sCurChildClass, len(lsChildren) )
    for oCurChild in lsChildren:
      sCurChildID = "%s:%s" % (sCurChildClass, oCurChild['id'])
      if ( sCurChildID in lsSeenSpinObjs ):
        mapChildren[sCurChildID] = sCurChildID
      else:
        lsSeenSpinObjs.append( sCurChildID )
        mapChildren[sCurChildID] = DumpSpinObj( oCurChild, lsSeenClasses + [sCurChildClass], nDepth+1 )
  return [obj, mapChildren]

for dvc_id in sys.argv[1:]:
  dvc = spin.Device.get(dvc_id)

  DumpSpinObj( dvc )

