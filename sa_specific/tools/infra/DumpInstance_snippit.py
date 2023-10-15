import string
import types
def DumpInstance( vo, lstObjsDumped=[] ):
  if vo in lstObjsDumped:
    print( "GOT HERE" )
    # Already dumped so just print out a string rep of the object:
    return "AD: " + str(vo)
  else:
    print( lstObjsDumped )
    lstObjsDumped = lstObjsDumped.append( vo )
  m = { }
  if ( type(vo) == types.TupleType or type(vo) == types.ListType ):
    m = map( lambda x, lstObjsDumped=lstObjsDumped: DumpInstance( x, lstObjsDumped ), vo )
  elif ( type(vo) == types.DictType ):
    for sCurKey in vo.keys():
      oAttr = vo[sCurKey]
      if ( string.find(str(type(oAttr)), "instance") == -1):
        m[sCurKey] = oAttr
      else:
        m[sCurKey] = DumpInstance( oAttr, lstObjsDumped )
  else:
    for sCurKey in dir(vo):
      if ( string.find( sCurKey, '__' ) == -1 ):
        oAttr = getattr( vo, sCurKey )
        if ( string.find(str(type(oAttr)), "instance") == -1):
          m[sCurKey] = oAttr
        else:
          m[sCurKey] = DumpInstance( oAttr, lstObjsDumped )
    m = { str(vo): m }
  return m

#------------------------------------------------------------------------------
#import pprint
#for i in nasdata:
#  progress.log( 'INFO', 'DEBUG', DumpInstance( i ), 0 )
