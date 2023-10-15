#!/opt/opsware/bin/python

import sys,string
sys.path.append("/opt/opsware/pylibs")
from coglib import spinwrapper

spin = spinwrapper.SpinWrapper()

sys.stderr.write("%s: Calculating dependancy order list of spin classes.\n" % sys.argv[0])

# Get a list of all canonical and replicated classes.
lstClasses = filter(lambda c:c['canonical']==1 and c['replicated']==1 and c['is_view']==0, spin.sys.getClasses())

# Get a dictionary of all canonical classes to their table and vice-versa
mapClsTbl = {}
mapTblCls = {}
for cls in lstClasses:
  cls['table_name'] = string.upper(cls['table_name'])
  mapClsTbl[cls['name']] = cls['table_name']
  mapTblCls[cls['table_name']] = cls['name']

# Get a list of all Classes and Tables.
lstTbls = mapClsTbl.values()
lstClss = mapClsTbl.keys()

# Will return a table name that matches the table name used by the spin or returns <None>.
def getTableName(owner, table_name):
  sTableName = "%s.%s" % (owner,table_name)
  if ( sTableName in lstTbls):
    return sTableName
  if ( table_name in lstTbls):
    return table_name
  return None

# Create a dictionary of classes to a dictionary that parent/child relationships.
mapClsRels = {}
for cls in lstClss:
  mapClsRels[cls] = {'parents':[], 'ancestors':[], 'children':[], 'descendants':[], 'unique_fields':[]}

# Grab all the PK Constraints via the spin.
lstPKs = map(lambda x:x.data, spin._PKConstraint.getAll())

# Filter PKs we don't care about.
lstPKs = filter(lambda pk: getTableName(pk['owner'], pk['table_name']) in lstTbls, lstPKs)

# Grab all the FK Constraints that refer to our PKs.
lstFKs = map(lambda fk:fk.data, spin._FKConstraint.getAll(restrict={'r_constraint_name':map(lambda pk:pk['constraint_name'], lstPKs)}))

# Filter FKs that we don't care about.
lstFKs = filter(lambda fk: getTableName(fk['owner'], fk['table_name']) in lstTbls, lstFKs)

# Create a dictionary of PKs with the 'constraint_name' as the key.
mapPKs = {}
for pk in lstPKs:
  mapPKs[pk['constraint_name']] = pk

# Itterate through every FK and map with PKs to break out parent child relationships.
for fk in lstFKs:
  # Get the target PK for the current FK.
  pk = mapPKs[fk['r_constraint_name']]

  # Get the child and parent class names.
  sChildClsName = mapTblCls[getTableName( fk['owner'], fk['table_name'] )]
  sParentClsName = mapTblCls[getTableName( pk['owner'], pk['table_name'] )]

  # Note the child and parent relationships.
  mapClsRels[sChildClsName]['parents'].append(sParentClsName)
  mapClsRels[sParentClsName]['children'].append(sChildClsName)

def calDescendantsAndAncestors(cls, children):
  # Start with no new generateion children.
  lstNextGenChildren = []

  # Itterate through all the children.
  for child in children:
    # Current generation children are always assumed new descendants.
    mapClsRels[cls]['descendants'].append(child)

    if (not (cls in mapClsRels[child]['ancestors'])):
      mapClsRels[child]['ancestors'].append(cls)

    # Itterate through this child's children.
    for nextgen_child in mapClsRels[child]['children']:
      # If this child has not been added to the list of descendants.
      if (not (nextgen_child in mapClsRels[cls]['descendants'])):
        # Add this child as a new child.
        lstNextGenChildren.append(nextgen_child)

  # If we have any next generation children.
  if (lstNextGenChildren):
    # then recurse.
    calDescendantsAndAncestors(cls, lstNextGenChildren)

# Itterate through every class and calculate full ancestor and descendant sets.
for cls in mapClsRels.keys():
  calDescendantsAndAncestors(cls, mapClsRels[cls]['children'])

# Returns:
#   -1: if <clsA> is an ancestor of <clsB>
#    0: if <clsA> is an ancestor and descendant of <clsB>
#    1: if <clsA> is a descendant of <clsB>
def cmpClassRel(clsA, clsB):
  return (clsA in mapClsRels[clsB]['descendants']) - (clsA in mapClsRels[clsB]['ancestors'])

# Sort the classes in dependency order.
lstClss.sort(cmpClassRel)

for cls in lstClss:
  sys.stdout.write("%s\n" % cls)

sys.stderr.write("%s: Done.\n" % sys.argv[0])

