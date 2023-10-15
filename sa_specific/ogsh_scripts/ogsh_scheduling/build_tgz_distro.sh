#!/bin/sh

echo "Creating ogsh_scheduling.tgz"
cd ..
find ogsh_scheduling | grep ".svn" > exclude_files
find ogsh_scheduling | grep ".pyc" >> exclude_files
echo "ogsh_scheduling/build_tgz_distro.sh" >> exclude_files
echo "ogsh_scheduling/README.txt" >> exclude_files
echo "ogsh_scheduling/ogsh_scheduling.tgz" >> exclude_files
tar cfz ogsh_scheduling/ogsh_scheduling.tgz ogsh_scheduling -X exclude_files
/bin/rm -f exclude_files
echo "Done"

