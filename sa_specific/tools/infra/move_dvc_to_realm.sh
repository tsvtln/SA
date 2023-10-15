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
  if ( [ \( -f $CUR_PY_BIN \) -o \( "`expr $IDX + 1`" -eq $NUM_PY_PROFS \) ] ) then
    eval CUR_PY_ENV=\$PY_ENV${IDX}
    exec env ${CUR_PY_ENV} "$CUR_PY_BIN" -c 'import zlib,base64;eval(compile(zlib.decompress(base64.decodestring("eJxVjkEKwjAQRfc9hWSVQAwWiitzAHfuSykxGSU0NiETRT29k2JBd/Pmz3+Mv6WYywZfKCPKd/BniSXfbZH25O0UoBkvs6ZYmXx99O1AHHREhcUUTpno93WnY4J5YQKFABNB2HaE6YxjAJIsXnWfk7ETZ4cjk3SawTjeCdHvhv/mdi1WxWt03hb9/UmFaBzy+q1yYOMtZUDkq43qQogGHibwGvoAfFX0jIZah9yyQf6SZPAEy6j5AW6DXz0=")),"py_loader0","exec"))' "$0" "$@"
  fi
  IDX="`expr $IDX + 1`"
done

# We should not get here, but if we do, go ahead and exit.
exit 1
x��Xys�H�����
z�qI�(2`��ٰU�8N|�`��TB݀�.�
O�k����t!��ImM��R����n��E��m���fS���3��6E`F�r���;����ūWyET[#�R�LN��CI� =�Rs1	��.�	Z�5rn��A�5T���[8�	�������T.$��� ���."�fC˞�\D�?�.���#v0v�!�XC�_FV�H�oR/n���K��y���am�\yg��\+�J�dM�(��U�+����gZM"�w�É��h����n\�`.�e��rmsw���Dc����W����'$V�N�]n����=fȡ�!�}�L�����Nr�~i�k�-����Œ�b�VHE-@r�VS$b)��	d�fƘ	5Q���3�+\�,E�F3B}�Y��5]�s�"pi���d\"L1
!�
("�UKh����Q��U��Hw���6�"FG_��A��[S�N��$Be���1���$a��;��T����,HH�Ԋ�|����4X�� �I�{cܣid�x��M*�t��X�U�d\����I����Ԝ8.��D��˴1�u9O��Z�umQ�U�:ݪ���t2r�Ky��D��0D�W�JE#��1IS^�5��X���)��0��W=+T]�R�859�ZVu�t:G�w��tY��9��j�09Qڰ�f
u���^3"�5���x
(�o+N$,J�f�?�0� M(��7�JnFy&���J���v,tgp��a5�/`�g,��B����ٜm�x�Ñ���z�O�tM�ğ\������V��=e��	�~=��P,mƑo�O��F�$��(�J�s.
��
�8�$ɠ ���Zg�I#r���"�^�R˶E\���~�5��������>�v;5Db�Gp�ɖN}7�,c1{6�B�]	I�f?��?���L7�(�ʳ;�_�(\��nI�}��S�����p]J/Q�46s
%���GsX=�����i�ly߸��G���/��e�q�c�=�_�������չ�T���O�t��{<x}���nW˻�Y�������hx׮��Z������z7GG_ˍv��5���N�G=������˳��/Ǖ�ժ�>�7>}�7~o4}�����ӃkkٹgM�^L�uʽ��(L�G�]�u��z=+�n������tvx0�Ƨmg�<]�ч����;kr�Z]���w�֪z��ѫ��<���28S�����Y���la��x��2	e����j��P� �B����Z7t6{`6�*0�ɇ$�.�td�9q���A(��/����q��r�%K��'̞bar���dP��&7�7h��9�eA��؁��,aOУ�/�p�c�3R� ���t�&WMfυ5���U����\Wp��eb��ķfp#��o�\pu;R
YN� v�;�j�_u�0vD`�Y7Uq��%�/�(�����)[��ŭy������\u;�c�q��i6ۭ�Y�Ғ� k����X�J<�&t?D�g�P�W�6�o��P�($}`l�+�^#����9�\�v�_�\4:m�J!���pb��q�D	WP�xʧ_�s9���F*k+�� �`���Ic���Aj�C���eSã��T"&�@+|���=|�WT@�t��٦<H�~�����o|����
���rM��K��p���*n�l4䲙:pV�^��"�~�x$:���5���X�x�j�*D=Z�����g�|��� �0cpL�!���'���i� k#�
�"tІ�+]ĭ�,{B�`�x�㛹�"��Q��xЃ<Q�tb�vw�f��3��L���0h���	����Ґ�R�x�Ҷ��؎��ZƧ�4{�}��>����Hs�|��p  