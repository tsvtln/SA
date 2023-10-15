#!/bin/sh

echo "Creating create_sw_policy_from_patch_cluster.tgz"
cd ..
find create_sw_policy_from_patch_cluster | grep ".svn" > exclude_files
find create_sw_policy_from_patch_cluster | grep ".pyc" >> exclude_files
echo "create_sw_policy_from_patch_cluster/build_tgz_distro.sh" >> exclude_files
echo "create_sw_policy_from_patch_cluster/README.txt" >> exclude_files
echo "create_sw_policy_from_patch_cluster/create_sw_policy_from_patch_cluster.tgz" >> exclude_files
tar cfz create_sw_policy_from_patch_cluster/create_sw_policy_from_patch_cluster.tgz create_sw_policy_from_patch_cluster -X exclude_files
/bin/rm -f exclude_files
echo "Done"

