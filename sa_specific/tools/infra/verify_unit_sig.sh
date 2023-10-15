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
x��Wks���<w�/�mM!��cco��0��`�m�R��!	u󐫒ߞ{�%@���&�����<���ҿ�������]�~��M|/5���M�O�c�c>�?�Ҿ�s������q�p�2��'e�Rxb<��	��'�(^͉M�&��C>���<�\�HҘG��}��(.�ȜM4�h%v~�T�+���p����'�B9��{� ���-��N|N5�w�`ɦ��9sO<?��
kΔ:3���I81B��Pۃu���DMl7y�� �S�@�rA��Dq�H��j����� s��A@υA�f�*wo,cׂ�Q���i�y�'�q%�/�p�����67��&<ɪ򟖭z��n���k�k���(�PI 	#n �J'��J���D���5�u�"�՟�H<�~"�a�e��,"|J�'���EC�"��-�Mh1�GIJ�3ܔ�6�Qe\�%��E7�Ȗ�(pMd�[|J �݌	�j]8ӈ��׎8���]1⥭���[1X�BXf�6P�"�5g4նv��pA��#1%0/ƙVHJ����`f����B�n�\Yqظ���^c����]=����C��`�GBF	q���E�X�!�֨ZK�SAl��>F&��EU+��8�V�0������u��1]�Wp������Tk�\Y��N��m�]���1]��g��t(�|�����u�r�m���	�΢�d�� =���~6pr�ؑC%l?- �!M�OM4w�lIU�X��+ra���)�����fw��5Q﯍O��:�޳_�$
}�ڹ͔�*�����K��7���]5�8����-s
df��5��)�l��n5���� ��7���Y��	a�$˘�IPl1�(��5P�����Iu�?�]�x��c.^��;3 �Zdj��g��
V����P1�J�����1��D?n�>�Z7���ݽ�M���w�����K��-{�ls�Tn�V��_;��>6���������t��������{��ރg?�k'_*��9[�ӧ������K��n߷��`Џ���h><y���j4o����:}�<7>v�C8�f?��O����g�����m���ù�W��!�M�����j���j���3\��G��hr�����*jxW��Γ5=K�;���m���������r^z����d�
�l����P`��D��.�%�iRF�T���eug[-�tC�-�{��P�,�Ե����z�~��Cc�0�2@JU����EF)6�K��N��K�%��&Pq��_��-�L
�����a1u|�d��2tE4��a����Q�v$gw!FB�S>�BU��_���L�ԑ�P�ZM����e��9���T�O4\�IS���O�>��A�ӥٿ�ۗM�s�sa^�[7�K(��E;�ѯ���,�(�tñ��7E)��_a��:�K�R>���W(�dh恖������n��.aP���MX�ޒ,�R��Yi�T+�ɴ���G'���$������dTX�>8�U��1`��V�#�?��|�L��@/C1��
���Gj�����x;��
~bt��<��
"�
̐�W���ͼV���Ѱ�ݙ˺_��.ӊ�(����/�e�B��k�<`��k ��m�i���b("'�e�9��,��lxl@�`��.�$�.Z�ZΔ�X``�ߎ�O����C�I H�`[�Q���{]�jy)ʹp��h0sVp�ᧂ@��w

%�2t�%�k�(���VW��/K�?���P  