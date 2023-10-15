import sys, string, types

if ( len(sys.argv) < 2 ):
  sys.stderr.write("""Usage:
	%s -ls				(list all Software Policies)
	%s <SoftwarePolicyId1>, ...	(dump a Software Policy by id)
""" % (sys.argv[0], sys.argv[0]))
  sys.exit(1)

import pytwist

ts = pytwist.twistserver.TwistServer()

sps = ts.swmgmt.SoftwarePolicyService

LOWER_CASE_CHARS = reduce(lambda a,b:a+b, map(lambda c:chr(c), range(ord('a'), ord('z'))))
def obj_to_map(obj, seen_obj_ids):
  if ( type(obj) != types.InstanceType):
    return obj
#    return (repr(obj), type(obj))
  else:
    obj_id = id(obj)
    obj_map = {'_id':id(obj)}
    if (seen_obj_ids != None):
      if (obj_id in seen_obj_ids):
        return obj_map
      seen_obj_ids.append(obj_id)
    obj_map['_str'] = str(obj)
    _obj = {}
    for key in filter(lambda k:k[0] in LOWER_CASE_CHARS, dir(obj)):
      child_obj = getattr(obj, key)
      if ( type(child_obj) == types.MethodType ): continue
      if ( type(child_obj) == types.TupleType or type(child_obj) == types.ListType ):
        _obj[key] = map(lambda co,otm=obj_to_map,soi=seen_obj_ids:otm(co,soi), child_obj)
      else:
        _obj[key] = obj_to_map(child_obj, seen_obj_ids)
    obj_map['_obj'] = _obj
    return obj_map

if ( sys.argv[1] == '-ls' ):
  from pytwist.com.opsware.search import Filter

  f = Filter()

  lst_sp_refs = sps.findSoftwarePolicyRefs(f)

  for sp_ref in lst_sp_refs:
    sys.stdout.write("%s: %s\n" % (sp_ref.id, sp_ref.name))
else:
  from pytwist.com.opsware.swmgmt import SoftwarePolicyRef

  for sp_id in sys.argv[1:]:
    sp_ref = SoftwarePolicyRef(sp_id)

    sp_vo = sps.getSoftwarePolicyVO(sp_ref)

#    import pprint
#    pprint.pprint(obj_to_map(sp_vo, []))

    sys.stdout.write(repr(obj_to_map(sp_vo, [])))
