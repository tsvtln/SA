import sys
from coglib import spinwrapper

spin = spinwrapper.SpinWrapper()

for eo_id in sys.argv[1:]:
  eo = spin.ExtensionObject.get(eo_id)

  eot = eo.getParent(parent_class='ExtensionObjectType')

  sys.stdout.write("%s(%s):\n" % (eo['extension_object_name'], eot['display_name']))

  vcvs = eo.getChildren(child_class='_VirtualColumnValue')

  for vcv in vcvs:
    vc = vcv.getParent(parent_class='VirtualColumn')
    sys.stdout.write("  %s.%s(%s): %s\n" % (vc['namespace'], vc['virtual_column_name'], vc['data_type'], vcv.getValue()))
