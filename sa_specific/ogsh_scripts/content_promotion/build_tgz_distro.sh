#!/bin/sh

echo "Creating content_promotion.tgz"
cd ..
find content_promotion | grep ".svn" > exclude_files
find content_promotion | grep ".pyc" >> exclude_files
echo "content_promotion/build_tgz_distro.sh" >> exclude_files
echo "content_promotion/README.txt" >> exclude_files
echo "content_promotion/content_promotion.tgz" >> exclude_files
tar cfz content_promotion/content_promotion.tgz content_promotion -X exclude_files
/bin/rm -f exclude_files
echo "Done"

