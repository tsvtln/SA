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
x��WyS�F�T�b�cy"�mhɌ
&$�`;�G#K+kmy%kW>��7��{�l���t���w�޹�?g�j��S�qs8��z/��s&g��^��6}&����GmM���׏�|æaI��x���%�.VB��eӡeOt!#�G�bE#AN
8���ぢ8�%�c����BH~�2��C��QG�D�qkJ��c����A��߉�XX#�%�К�NKc1I5UU{H>&;��wc�G��� ���ɜ���ϵ7�0���dg��2(+
s�F|�5��LNNH�$f3 �dR������)AY���Ȅ3�(	H��#񄨻��ZA;E8�������R9�m|(&hƓA5�0���2M�Ӆa&���g�����������N�tƍ�Z��8���V��"�[f7� +A#���9-�H}V�F�l�idt��IΚ��,=���ݰb�Q.�m�;9R�0	:�"�3��� �~���d6M3_����у����A�G�0^?)�(�m<'T4\Ɲ�����આ*?]�%0�2�k�I'�\��"���ZV/�-�7y�f&�2m����g�mK�޳�C������m 9P��J�תmG��%����1>�
(�q;���*_��:
�0���}BP<�!��� n��L-í�V
�A�PE�gPwz���NP&-��i(3M�Ĉ'��k��_i�����Ԓf*��g=m����V&e��������ͳ�|G$�
Ԁ���^H���+�,�F�����E1�q��Q�n��=�>�"�Y���a1�Gf��b�c2z4���T��[~O���q��Ƶ���Χ���1�Xo�qg5Y�wz���ٽ�֎&�w
g�=}��a~x{�Z<����Kg��Y��>�j��*��1��Ç������Zo�n����uC�����w��/�����<�_���.��u'�5��x�߱�1=uZso�7uX�vy++���h�7}k5W�f������;���g���ņ��yPw��U��w�Z]����v��:�����=VNJO"�s���6������w:�|��!<��gDa��<ɍCӀc�岮�u��J�Ԇ�$��|�d�`�9C ۦ���{A(�G���!�{�\���JN=jO�����tA	������]��?7$��1���g�z�V�S'"�6s��$�QN'Z�0��5�i���?H^�-�C�����-�t�0p-��3�^{�iYSN� �f:�����H�<i�$Z�|΢��%�	]ij��l�.ޟ�ݛ^�u�0?��/N��V���yiI��Z��o",�j	�8]JL(��w�Ģ���'1�g=,�J�D�ַ��
ٔ,�9�R��ۺ�خw[��zN���a8i�q����E�8�J����h����	�̵
�t���*�� �ݡ����Z��T�V"�'���̀8̖}5�T���⺭����x6��C�7���8�]q��*i�|4��: �B��0���ǵ"�!��X�@���t���L!�Y?)A�s
���
3	�iB$CH�$�Y��;�UM'I�l@!d�6�^=��6���O1� ��{1�=r����%y" �D%&�"}Z���9�v�Qaf��d��4�����P�Ry��Sk؎��V�a�Pf?�����`�t  