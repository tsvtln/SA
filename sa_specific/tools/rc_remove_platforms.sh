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
x��V�o�Hn�՞�`ϧ�Fq�+��+��А�mH�%�!k���������߬���N']"���<��ff�/����F�n:[��e����"�k��.fVyt�S�x���A���`E���`�:S��C��D8I$�5�����Z^En]�k�|��V-��V,ފ9Ap,$#��2Rq4[��;TF���xl�23X1u9�ȢF���+��r�<C�2ܰ+����t�TU���C���:L.B�Ě��E'�)=�j!IP�\�r1�jJX7�Kv�z�NA��&wQ�|儯���N	��g�	a��6IT\�����!�
,��*F�1.Q<Q��B�,r�� ��G�Ww��O+���D������f޸����=�}�ml��kՋۋ�V���w�RuQ�j����P>�����fd]���f��;�{k:������X��h��o�՛b�ӹkۆ��C?����������}���Y��ve��7�.�?�o��ѩ1_�{xӟ���Y��g:��v�
e{Z�k�{�|�O��xx󑍴��򴼼
fg��X
��}a~9�v5�o�Jo�m����McP9�(ԥ'����	SLI��O�Ʈl^�D��I�6"�ʩN"1IJ�,��b.��{ߢ"�-1@*�W�;���mN���-���|2��
�H��Y~����(��M�b�� �
A>!&�D�5�����K����03l�ȝn�3Jǂ� �y��t�� Ɗ�KƵRy��O1Nb3;�E�}�\�_@�3��eT~�i����PuF�� �s��:
B���L`ʰ)���~�x$⯝(�US}AbY���v��\��i��yS�ظ�l�N�u�>������t�o&�,E	�|�e���䊓���������T�RO��N���c3*u���ͧn�ߑ8����_"OSARC/S�qU��H\Jj�w��>J$H9X��)h|��^`u<��`�&9���1� %�.'�q����d����˱�	E��Mb%}�{�)�G��G�W���`�]ݧ�BR����¬bɈeģ���n��0���1Ӡ
y��dñ�v��}.Q�Y�t���J���b ��'�:�H�0�ć�`�FiU��뙋#���$�w�ȹ
��L����ģ2���w5މ�����a���zaJ0�i��
Y�=��f��9
{x ��,_h/3�����R����  