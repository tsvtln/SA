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
x��V�o�Hn�����{>E��GRN������mH�K�"k��x�/���9��Y�Z�N�HX��3��|3����q�c�~h�0~��'7y8#��G�ŖiS���:����/�����Ga�K�$Q)�#�;Ǔe�먌�*�v���*��(H�e��	�@�
��~+h���h4�@�-ذ4B�
YS����2s%|E�$�P}�S�/#�Ī.��t����|!���#h$�uęj�xF���١vX$�q��h
�����\@�]{��(����/�1������R��^Hqy�N���>�XBV�:Ԛy��㘹�+<{t\`<��D�&�B�5�<���9$�#����Y�n5�������U�R����E7����F�m�z�6��6�b�>;������j��5;wv���3�+��KFؘ-Yu���ֵ�}Yk�[�ez���^�?�}������6nU��v{Þ��3���έ�쬋W��4���]}��{�/���Z��p�99�����G>0.g���C8�n���zj��Siz3�n-I�jw��ZIu�^�U/��K��+f,AȆڔ�1f�z�'YbO�B?�Qā
�m�V2�Tb��pE>fr>_�w�rA&kb�4��N=�;�w�1[��  �F~l�cRd
�-�dI�5]b͠[#���
��$&��/�Dl�,��'����[�
8J�����E8�D"/5��n6Z�Zp<���r6|�B�	sC�b���B�F��b2a�י�j�	P'��i�J�VGa��?LԘ`[9�3U��O$X�8T3sFE��͆q����
�}�0?j�7M��n5�Z�P��ڙ��d$�������((�-d��Bh~����Hd���^���N���ash������:��Ή��n"[D��f�z��^V�����������:	3��^zp-�r�XN�8ؿ���?�)�.A0JH<Gp��8Q%s�>A�F,��V(�$�&N���S�g�'$V�޽p�=3`�RZ���/�m���^/�;����$�e�!Ӡ
!���JĲ� 	�|�"���p{"*��U3��4@z��$1�[.������O!8ܞ ��:0g��s��k[h�C�
�e ��j��*����
���`$�Y��J�~m��:���~8n����?��7���  