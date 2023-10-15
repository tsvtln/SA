#!/bin/sh

echo "Creating ogsh_demo_scripts.tgz"
cd ..
find ogsh_demo_scripts | grep ".svn" > exclude_files
find ogsh_demo_scripts | grep ".pyc" >> exclude_files
echo "ogsh_demo_scripts/build_tgz_distro.sh" >> exclude_files
echo "ogsh_demo_scripts/ogsh_demo_scripts.tgz" >> exclude_files
tar cfz ogsh_demo_scripts/ogsh_demo_scripts.tgz ogsh_demo_scripts -X exclude_files
/bin/rm -f exclude_files
echo "Done"

