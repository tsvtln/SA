import sys, os, gzip, cPickle, types

def fix_dates(d):
  for k in d.keys():
    v = d[k]
    if ( getattr(type(v), "__name__") == "xmlrpcdateTime" ):
      d[k] = str(v)

def emit_obj(f, ind, obj):
  cPickle.dump((ind, obj), f, 1)

def rend_Unit(unit):
  return "Unit:%(unit_id)d: %(unit_display_name)s(%(unit_file_name)s/%(unit_name)s/%(unit_loc)s) ut:%(unit_type)s, eow:%(exists_on_word)d, st:%(status)s, ct:%(create_dt)s, mt:%(modified_dt)s, mb:%(modified_by)s" % unit
  
def rend__UnitRelationship(rel):
  return "_UnitRelationship:%(unit_relation_id)d: o:%(relationship_order)s, rt:%(relation_type)s, uid:%(unit_id)d, urid:%(related_unit_id)d" % rel

def rend_None(d):
  return str(d)

def print_obj(ind, obj):
  if ( type(obj) == types.DictType ):
    obj_rend = globals().get("rend_%s" % obj.get("obj_class", "None"), rend_None)(obj)
  else:
    obj_rend = str(obj)
  sys.stdout.write("%so %s\n" % ("  " * ind, obj_rend))

def load_file(fn):
  f = gzip.open(fn)
  while 1:
    try:
      t = cPickle.load(f)
    except:
      break
    apply( print_obj, t )

def dump_unit_rels(unit_id, f = None, ind=0, units_seen=[], rels_seen=[]):
  unit_id = long(unit_id)
  b_close = 0
  if ( f is None ):
    f = gzip.open("Unit%s.pkl.gz" % unit_id, "w")
    b_close = 1
  from coglib import spinwrapper
  spin = spinwrapper.SpinWrapper()
  if ( unit_id in units_seen ):
    obj = "Unit:%d" % unit_id
  else:
    units_seen.append(unit_id)
    obj = spin.Unit.get(unit_id).data
    fix_dates(obj)
  emit_obj(f, ind, obj)
  print_obj(ind, obj)
  ind = ind + 1
  rels = spin._UnitRelationship.getAll(restrict={"related_unit_id":unit_id})
  for rel in rels:
    rel = rel.data
    urid = rel["unit_relation_id"]
    b_recurse = 0
    if ( rel["unit_relation_id"] in rels_seen ):
      rel_obj = "_UnitRelationship:%d" % urid
    else:
      rel_obj = rel
      fix_dates(rel)
      rels_seen.append(urid)
      b_recurse = 1
    emit_obj(f, ind, rel_obj)
    print_obj(ind, rel_obj)
    if ( b_recurse ):
      dump_unit_rels(rel["unit_id"], f, ind + 1, units_seen, rels_seen)
  if ( b_close ):
    f.close()

for item in sys.argv[1:]:
  if ( item[-7:] == ".pkl.gz" and os.path.exists(item) ):
    load_file(item)
  else:
    dump_unit_rels(item)