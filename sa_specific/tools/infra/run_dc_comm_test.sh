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
x��Vms�FN����S�UmF҄�;�����fc;���`L<�C:@ ���	�3�ܿ�=I��:��L��v�v��}v���wz﵏]j������3���ؖ��%���לٖ��b�����gL~������&����Y�#;�x�er�0�c.{N�C��CP�b����	��
���_b�B��m�"�Kɗ��R5������=�ل��t�m������e�r�Q���J������uCY��[>�aKPiS!B^�狥f���b��{Ȝ�X�!�	t������!|CQ t�ɲ1g	L�~wh�tc���v�̂�|�����m�B���!f�	��b�SӞ{�����\��A¹@�	��㺏i�=U#�XՁum,���.���e���p�AIҩψF�OR��kl��4�R@����",%S� �^�a��+�;(I�!f���+R�h\���m�����"\j{VD�;gRt�<�p�H�+�
���l�Y�����LtiD�Dz���*/�d�⎑�h �����ATG/X���@FEA�gL�v�^0�K��:F'�4hd��5�u��QxO	c��CXq����vk�`�x�n���#93>�^���スt�(��C���?��F�}@X#��ϳy�l5�^^��i�����껮����Q'���;�¹��^uK��i�ɷ�������� ^݌���3'_�n�z<�i��_zAm��囁�>8�(V[�������!
��t��~pyvT���J-�,ֳ��	�����C�{�o��{���H�i-�˼����/
{��A����]�vQ���M�1_��-.��q����Au|t]�����A_�˝�v��g��r���p�=AƖ�d�&��0'��?�{:L����.�C�A��&� O�u:�0r�o5�JҁT�Z��"X$��Զ5�h��v�c23+9��(����y�kN����$���q���:�|<q�����08���jw�0���A�&��̌�)�e���G������G�b�i ���A��p3�b*ۂ�?��!MSK���V��n�_Q��#i��o�ewB$B�.�s��5'���V�w�au�z�V�f}��ԭz�Y?k6�,i�>��9����(<�dAGɓE���9�o�
���������4S247�j�A�uqޮv[�L*� `z�&��,sHc�2�V%� ����)=FI�)K}�z94��i�l8�ۡ�����rX��P�~-S����|��يYl*��E2�n��z&To�	L�	��ےK>�rH���{�{凅�:I���%-�g�e�/�Y��"
���$>%+�K�9���D�:U��F#+���M+���$~ :� �lV�EiSټG&.v0�h C�~ m�Ϥ��M�=P�� �w�f �s�����I���,W�,�S����C঩l�"i�E�1�v:;a�@�"�_��̿�B���  