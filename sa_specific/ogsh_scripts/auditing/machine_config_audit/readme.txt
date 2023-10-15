
This zipfile contains a batch file which calls a Python script which
will find the machine.config file on a system and parse it looks 
for important attributes.

The script contains a dict variable 'attribute_dict' which lists the 
config attributes in machine.config which are of interest.

The script creates a directory tree at 'machine_config_dir_root', 
which is c:\temp\audit\machine_config by default, and creates a file 
there for each subattribute of the attribute. Each file is set to contain
the subattribute name and it's value.
