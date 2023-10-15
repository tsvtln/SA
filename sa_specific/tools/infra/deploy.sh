#!/bin/sh

TARGET_DIR="/shared/support/tools/dwest"
cp -p dump_session dump_session.py I_T.tgz get_external_users py_build DumpNguiCache.jar DumpFolders dump_trans sql obj_dump oash dump_occ_perms dump_occ_perms.py surl "${TARGET_DIR}/."
find "$TARGET_DIR" -type f | xargs chmod a+r

cp -r get_external_users_dev "${TARGET_DIR}"
