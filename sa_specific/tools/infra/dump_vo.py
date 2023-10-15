# TODO:
#
# [ ] Add a "-u <username>:[password]" option.
#
# [ ] Add queries for "XXXService.getYYY(XXXRef ref)" to vo dump.
#     (actually, I'm not sure how practicle this is.)
#

import sys, string, types, traceback, gzip, cPickle, pprint

def usage():
  sys.stderr.write("""Usage:
  %s [-lt | [-s] -ls <obj_type> | [-f <attrs>] [-b] <ref_spec1> ...]

  -lt
    List all object types.

  -ls <obj_type>
    List all instances of the given object type.

  -s
    Causes "-ls" to only output reference specifications.

  <ref_spec1> ...
    Dumps a gzip'ed pickle of the VO for the given reference specification to
    stdout.  Prints an error message if stdout is detected as being a tty.

  -f <attrs>
    While a VO is being dumped, if any VO references are found under one of the
    attributes given by  <attrs>, then the corresponding VO  will be loaded and
    dumped.  <attrs> is a coma delimited list of attributes.

  -b
    Dump VOs as a binary gzip'ed pickle blob to stdout.

  -h
    Print usage
""" % sys.argv[0])

if ( len(sys.argv) < 2 ):
  usage()
  sys.exit(1)

import pytwist

ts = pytwist.twistserver.TwistServer()

ss = ts.search.SearchService

LOWER_CASE_CHARS = reduce(lambda a,b:a+b, map(lambda c:chr(c), range(ord('a'), ord('z'))))
# If <obj> is a VO, then dumps it and returns a ref spec.
# If <obj> is not a VO then returns a representation of the object.
def dump_obj(obj, seen_ref_specs=None, follow_keys=[], follow=0, pp=0, fo=sys.stdout, dump_vo=1):
  if ( type(obj) != types.InstanceType ):
    return obj
  else:
    obj_map = {}
    # Test to see if this objects if a ref.
    _spec = spec_from_ref(obj)
    if (_spec):
      if ( follow ):
        if ( (not _spec in seen_ref_specs) ):
          seen_ref_specs.append(_spec)
          dump_obj(vo_from_spec(_spec), seen_ref_specs, follow_keys, 0, pp)
        return _spec
      else:
        return "%s (%s)" % (_spec, obj.name)
    for key in filter(lambda k:k[0] in LOWER_CASE_CHARS, dir(obj)):
      follow = 0
      if ( key in follow_keys ): follow = 1
      child_obj = getattr(obj, key)
      if ( type(child_obj) == types.TupleType or type(child_obj) == types.ListType ):
        obj_map[key] = map(lambda i,seen_ref_specs=seen_ref_specs,
          follow_keys=follow_keys,follow=follow,pp=pp,fo=fo: 
          dump_obj(i, seen_ref_specs, follow_keys, follow, pp, fo, 0), child_obj)
      else:
        if ( key == 'ref' ):
          obj_map[key] = dump_obj(child_obj, seen_ref_specs, follow_keys, 1, pp, fo, 0)
        else:
          obj_map[key] = dump_obj(child_obj, seen_ref_specs, follow_keys, follow, pp, fo, 0)
    if ( dump_vo ):
      # Emit this VO.
      if ( pp ):
        fo.write("%s\n" % pprint.pformat(obj_map))
      else:
        cPickle.dump(obj_map, fo)
        sys.stderr.write('.')
        sys.stderr.flush()
      return "(this should never show up.) VO Ref: %s" % spec_from_ref(obj.ref)
    else:
      return obj_map

def spec_from_ref(ref):
#  if (hasattr(ref, "secureResourceTypeName") and hasattr(ref, "id")):
  if (ref.__class__.__name__[-3:] == 'Ref' and hasattr(ref, "id")):
    return "%s:%s:%d" % (ref.__class__.__module__[len("pytwist.com.opsware."):], ref.__class__.__name__[:-3], ref.id)
  else:
    return None

def vo_from_spec(spec):
  # Attempt to load the VO for the given spec.
  try:
    # Parse the reference specification string.
    (obj_mod, obj_type, obj_id) = string.split(spec, ':')

    # Import the relevent reference module.
    exec("from pytwist.com.opsware.%s import %sRef" % (obj_mod, obj_type))

    # Instantiate the reference out of the local namespace.
    obj_ref = locals()["%sRef" % obj_type](obj_id)

    # Get a reference to the relevent service module.
    obj_s = getattr(getattr(ts, obj_mod), "%sService" % obj_type)

    # Invoke the "getXXXVO()" method of the relevent service.
    obj_vo = getattr(obj_s, "get%sVO" % obj_type)(obj_ref)

    # Return the VO.
    return obj_vo
  except:
    sys.stderr.write("%s: Failed to load the VO for '%s'.\n%s" % (sys.argv[0], spec, string.join(apply(traceback.format_exception, sys.exc_info()),'')))
    return None

def shift(lst):
  if lst:
    ret = lst[0]
    del lst[0]
    return ret
  else:
    return None

def main(argv):
  simple_output = 0
  follow_keys = []
  pp = 1
  while argv[0] in ['-s', '-b', '-f', '-h']:
    if ( argv[0] == '-s' ):
      simple_output = 1
      shift(argv)
    elif ( argv[0] == '-b' ):
      pp = 0
      shift(argv)
    elif ( argv[0] == '-f' ):
      shift(argv)
      follow_keys = string.split(string.replace(shift(argv),' ',''), ',')
    elif ( argv[0] == '-h' ):
      usage()
      sys.exit(1)
    else:
      sys.stderr.write("%s: WARNING: '%s' is an unrecognized argument.  skipping\n" % (sys.argv[0], shift(argv)))

  if ( argv[0] == '-lt' ):
    obj_types = ss.getSearchableTypes()
    sys.stdout.write(reduce(lambda a,b:a+b, map(lambda t:"%s\n" % t, obj_types)))
  elif ( argv[0] == '-ls' ):
    obj_types = string.split(argv[1], ',')
    from pytwist.com.opsware.search import Filter

    for obj_type in obj_types:
      f = Filter()
      f.objectType = argv[1]

      obj_refs = ss.findObjRefs(f)

      fn_fmt = lambda ref: "%s\t%s\n" % (spec_from_ref(ref), ref.name)
      if ( simple_output ):
        fn_fmt = lambda ref: "%s\n" % spec_from_ref(ref)

      if (obj_refs):
        sys.stdout.write(reduce(lambda a,b:a+b, map(fn_fmt, obj_refs)))
  else:
    if ( pp ):
      fo = sys.stdout
    else:
      if ( sys.stdout.isatty() ):
        sys.stderr.write("%s: ERROR: stdout is a tty.  Redirect stdout to file.\n" % sys.argv[0])
        sys.exit(1)
      else:
        fo = gzip.GzipFile(fileobj=sys.stdout, mode='wb')

    m = {}
    for obj_spec in argv:
      obj_vo = vo_from_spec(obj_spec)

      dump_obj(obj_vo, seen_ref_specs=[obj_spec], follow_keys=follow_keys, pp=pp, fo=fo)

if ( __name__ == "__main__" ):
  main(sys.argv[1:])
