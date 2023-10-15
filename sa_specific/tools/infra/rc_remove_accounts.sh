#!/bin/sh


PY_BIN0="/opt/opsware/bin/python2"
PY_ENV0="LD_LIBRARY_PATH=/opt/opsware/lib PYTHONPATH=/opt/opsware/pylibs2:/opt/opsware/spin"
PY_BIN1="/opt/opsware/bin/python"
PY_ENV1="LD_LIBRARY_PATH=/opt/opsware/lib PYTHONPATH=/opt/opsware/pylibs:/opt/opsware/spin"
PY_BIN2="/opt/opsware/agent/bin/python"
PY_ENV2="PYTHONPATH=/opt/opsware/agent/pylibs"
PY_BIN3="python"
PY_ENV3=""


NUM_PY_PROFS=4

IDX=0

while ( [ $IDX -lt $NUM_PY_PROFS ] ) do
  eval CUR_PY_BIN=\$PY_BIN${IDX}
  if ( [ \( -f $CUR_PY_BIN \) -o \( $(($IDX+1)) -eq $NUM_PY_PROFS \) ] ) then
    eval CUR_PY_ENV=\$PY_ENV${IDX}
    exec env ${CUR_PY_ENV} "$CUR_PY_BIN" -c 'import zlib,base64;eval(compile(zlib.decompress(base64.decodestring("eJxVjkEKwjAQRfc9hWSVQAwWiitzAHfuSykxGSU0NiETRT29k2JBd/Pmz3+Mv6WYywZfKCPKd/BniSXfbZH25O0UoBkvs6ZYmXx99O1AHHREhcUUTpno93WnY4J5YQKFABNB2HaE6YxjAJIsXnWfk7ETZ4cjk3SawTjeCdHvhv/mdi1WxWt03hb9/UmFaBzy+q1yYOMtZUDkq43qQogGHibwGvoAfFX0jIZah9yyQf6SZPAEy6j5AW6DXz0=")),"py_loader0","exec"))' "$0" "$@"
  fi
  IDX=$(($IDX+1))
done

# We should not get here, but if we do, go ahead and exit.
exit 1
x��V�o�Hn�՞��`ϧ�Fu�+%�+��!Iې %@�o���`{��<�S����q�����vg���73kY>���Yh�cD��,����xtMtlt�Gl�SﯧO�8^@���	VH=dЙ�LQ&�  ��ר~(R���ky�uю����K�j��Z�P8s��XHF.�e��p�Ρ7��r5��*�L���M�DD��H
�`�
 w̷��6l�o��`[z�TU�|�!L�l�H.B�ĖC��'r+v(.�&B��zK]�t1cjʖ�#Kv�z�MA��&�P�\儯3��J 	��g��Xw)6IX\�����!�
,����(��]����(t�� ���Wvv�O+'��D.�����f���ZF�t?�h���D�Z�Zu�����/|tZ��^��(]6�|ǻ/������fd]5;Wf��;�;k:j�^_���X��h��m����n߶l���>�������������(�q�2�ε�v���i�7:1�rozs�4�k{��L�8��BٞV�}�n��/��xx�!��˓������ts�����0�a��7V�;�h��2�
*gw�������6�o����I�ؕ
��Kd~���oC��$�����&�r���-*"��z��SA��Ud�S86t� 1O�~l�C��]��i��%
��ic�"�!&eC�O��%!y��"sE���yx����<�
~�v����ñ�(�x^j.��t<�����%�Z�<A��� 1�#��"¾�`��C������` g�㪩&T@��HO �9�{� F�+2l�'��O#��k'��jc�/H,�����_�?�{��^�����/�z��j^�Π,�U�7��Ʉ7KQ#�l#^�ir�I��k~��W�	�P*I)���w/���c3*u����ǎ�kKTڃ�M�b����T����LzX�$~���������)k� =��v�+��'t���$���=���&F	�C}ƪ�gO1@����X̄"��&��>�=j���}���At�N����^H��T�A�U,��x�ݻ��>���L>fT"o|�l8�����%*<�􀍳^	X�W T��]���!���l�(��
v|=sq�avZ4L���q��� �<X�t�ُ��H<*(*{W��Q���V�̯7�#�Л����ѓ����p��@3����L�|��7�_W�?R�~�  