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
x��V�N�Fn�mw���i*dG�l*h��@ �.�lHBdM�q<ķx������t=Ǘ\袪R�g�s��\f�̾U���]���wݟ���kF�j�������b���N�fp=�}�e�ë�;�����^��'
��G�	}*D���%�$Y���	)Is��:>n<�I��L",n���?�	`��F�4��-���D�� �F���(��Gyiiq��9X :qA�M�$'D޷d#	I�,��wA�5h� �V�[���
o�ˀ�L��r]A'��	2ܟ��3K�$	v�Y�4ʧ6؊�J�<�|��/�/X�vpݎ�J>	cc
fb��yQ��J.�;&9���yh17�:��3C���Ęh���h��Y����lK�x�:h�sT�K0U0�IK�<�'�����WM�[v�)���1O��ו��H��O퉔�JA~\�����c�'d�9c������������Y� Z�6�׳z���6��l��A��&������~*v�p�f��a)�
�k%�'r���:��%Pt��, �Ot%?�l�,(��v�|��Ͱ�;�����

�E�³��p�݉$M�����Sc򬍫���̮V������S���ԏ�^��]m��<|�5�y;��.���
ot�;��i�n[����O�j�-��i��(�]�~0ǃf��m��էQ������m��l�7,�����wt�s��W�w���M�Ҥ�j�T��nϜ������A�.;O��h.�E�1x��ꅥk|T�:��������p�=��fw����ˋ�W3�JO�jEѝYmZ�FT}�P�U��K'�ft$$�6�oL����V�1|�Z
n@7�'���`b��������v��c+��k��|�����1l�8��^sE��iK���b�R���_ȩ��)	="�B]2�2f�$`��s��[�ġh��������j׈��M�J$x.5�Yɰc�<�c�
�+#��1�!D'��L]�$%�����Y	SQyy�<B$d \������x>s�����ᖪ�
������ڔEJ�����ˏgZ��i�յO���S��8�n�AZ�ި�Me��R�A�e�
�F�+\��|z��~y�'�+��k����{�I)�Y�r��i�޴j���A%5��6ՙ��@d?�Z�zU���*�����;����
d��%�렵ۡ#�`�-u�v	\�Z���f9
"UҲD�fp9�e��(yؠq|l)�%)� �moLm�'�8;q��,cq�eb��1��>^|��Pv�(����%�2O
�~rg੓
1�v0���1�P�b
4
��
$a�2
7~�G��g����6f;�!^ꈁ>C�k�U�9׬e(�]�)�;i `acj��^�ͤ��go L&hY�P������V�H�����ހb�'���\��t�'�  