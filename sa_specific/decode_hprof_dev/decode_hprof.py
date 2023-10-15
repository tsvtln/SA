import sys, copy

# Quick and dirty hprof decoder.
#
# Major features:
#
#  [ ] Auto parameter dereferencing
#
#  [ ] File based indexing - Indexes will be a simple file containing a list
#      of offsets into the hprof file for whatever kind of record that the 
#      index file is intended for.  This list of file offsets will be in 
#      ascending order for a specific field of the kind of record that the
#      index file is intended for.
#
#      o objects-id.idx - Object instance records sorted by obj_id.
#      o classes-id.idx - Class definition records sorted by cls_id.
#      o objects-cls_id.idx - Object instance records sorted by cls_id.
#      o names-id.idx - Name records sorted by name_id.
#
#      These indexes will be stored in a directory named after the hprof file
#      being decoded.  An index "bundle" will be assumed to be complete only
#      when the hidden file ".done" is present inside of the bundle directory.
#
# [ ] Kind of queries that can be done;
#     [ ] dump all instance records.
#     [ ] histogram
#     [ ] dump specific instance record by obj_id.
#         (ex: "obj:123abc32")
#     [ ] dump instance records by class glob.
#         (ex: "cls:*RBDMS)
#
# [ ] HTTP server.
#
# Being a command line utility it is important that this utility be able to
# get access to indexes as quickly as possible.  There should be a minimum
# amount of data that needs to be loaded on startup.
#------------------------------------------------------------------------------

# notes:
# 




// Caching
class Index():
  def __init__(self, idx_file_name, cache_size=0):
    self.idx = open(idx_file_name)
    pass

  def foo(self, *args, **kwargs):
    raise "HprofIndex.foo() must be overriden."


class IndexBuilder():
  def __init__(self, idx_file_name):
    self.idx = open(idx_file_name, "w")

class HprofScanner():
  pass

class HprofIndexBuilder(HprofScanner):
  pass


class hprof_decoder():
  def _usage(self):
    sys.stdout.write(
"""Usage: %s [-h] [-dr] [-a|-i|[-o <obj_id>|-oc <cls_glob>|-c <cls_glob> ...]]

  -h
     This help screen.

  -dr
     Automatic field dereferencing.

  -a
     Emit all object instance records.

  -i
     Emit a histogram of all class types and the number of instances.

  -o <obj_id>
     Emit the object referenced by instance id <obj_id>.

  -oc <cls_glob>
     Emit all objects of the class types specified by the class name glob
     <cls_glob>.

  -c <cls_glob>
     Emit the classes specified by the class name glob <cls_glob>.
""" % sys.argv[0])
    sys.exit(0)

  def load_indexes(self):
    raise "TODO: implement load_indexes"

  def main(self, argv):
    # Parse arguments.

    # Initialize member variables.
    self.indexes_loaded = 0
    self.idx_objs = None
    self.idx_clss = None
    self.idx_objs_by_cls = None
    self.idx_names = None

    # Load indexes.
    self.load_indexes()

    # Indicate success
    return 0


if __name__=='__main__':
  g_hprof_decoder = hprof_decoder()
  sys.exit(g_hprof_decoder.main(copy.copy(sys.argv)))
