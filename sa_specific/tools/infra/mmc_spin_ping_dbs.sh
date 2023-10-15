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
x��V�o�V�n������+md[�5G�T��slȱ		��P�>����?s8��!�쮪JE2z�{~3�Ɵ��I�������u�g�7u�;<�2�����M�r�d�����_������W�\?
��+$��'1($ZY�ċı��nhL�/���)OX,����
���݄I-I�%`�$!1� `f�G�dqJ�u�$q�wTU�3(Ȃ৖AN���f]₳��:aI�Z��r<�I�G����	-��Hh<Y"Q���[&�N���y^���\K!�A�0&�����QUg,�|"�E���kC٪�2;�\�����Ā�X�<��
Yekf.8�<Dʠ�XL�8���7���a@V�ٖ�3F���U�{{u(�T�L��m��N��×�9�D:��	9�'`��P rH�M}�&Mh����EQ���h]73�@b�8�)�o� ��
���T�Bj��<����^��Q��3;�9��Ә;�S=�P�V���d��c[Ou�z���b�i:k]����m֜A�ӭ��n��E7��Ϻ�ҵ����*�Y�n;���ۏ��`����F��*��{o����R?�ϖ��0��׵�MYk��Z����� �
���������~]��i�:\O��s~����ñ9�u�7e
��t�E�r˃� )9F���?��c�v^N�7��~s6?>�߆���k�Ζ�f�/M��SK�[��}�h��:}�
����ҩ�,���6�Ϡ�U��`K�If�G��$d��טq.�2�b9��YV
϶J{�"��7�!������
*�(���h̊�`�퀃TA~%
��3�8cĵɊ��1)1{�~��`���I|:q���>�^W����t5�������$��*`W�&!�5jxltR9�ӗ1b��\�L��"0A��;'���.O��2SEsI� ���(��SF,�RE����U)�Ă����P��$:C��?�j꽻~�ݬ�����h���&��d�Գ���T��,e��N���7Ҿ�J~
�w�1f(V�<���v�ޢ��As����7���1���ȣ&��%�1J����t��x�1�����I��K�$�1XJ;�)d��&�3AkBǀ�Ӓ*��e��+�f�F��Ɔ˞Ʃ*���<�
[bv�����C@�'��a=�	�����~Zʪ�U����X6b��I���f�q3�\�G�϶/6~�V�bc��L��|��`%��_c ��g�:���@�ae�tH�G��H��=��?�����'�w���V�}��Ľ2���lj�!�(7���
��zb0A�<��T�m��~�@��w��s�ˀf.����B�h�f�H  