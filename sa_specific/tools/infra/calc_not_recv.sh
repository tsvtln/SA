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
x��Xks�6��v���?��hDNZ�w�F��d�r�8~H�C�p a�E�������|������$��:8�₿M��^�������?Zس̀	3"�l���+Y�M-1����?��������w�Y$_p~F��k�0$��V�X(���8"[<�AES� y$P�r�g���v�v� ����&Qd�#*�Z�T���r�މ�oږI��`٣�t���Âp$\��%b�!����̈�D����IU�
+�4�����{�f�1C�P����Z�9y�Bm@�K���@M��s#�s�0�<G�cئ��0��4�x1wUM�w �X��j,\{�#<�>�D�(��A*>3�KU+�J+x����9�`�_9xZ�e��hy�a��etTI�ii�V=�;lo��Qfi���>]�}�jH�o�8�,R�?�9�/)�6�]�^���[��	K�(PcF�%�7� ^>~4Wd+9M��=N<b����	==+"�Qb.Gs�D��ȣ�5m�(OxĞ�p`_C�Z`�t�q�vSKFs�4@�&K%��{Z"T��I�BX��C�Um
�@B�E�sK������d�b@4�@���?� �8�Q���f�uT5�@V�?�{�=��c#��'br���%1u�_��"�4"������Ƿ�f�^�+�*'�M�Ł _�M́t��r�`��l�뒪�����0�R��K���"$3Cz�a�@}UV(�q�a���B]��+��\y}���H�X�-A,K��̫xAD�ǡ�adcDh���=A��T����;
��d���%��Z�$k��;�"$���,虆j�pR�|a�w�#T/��6=�l��1��f��@	�
�^,�6ԕ�܂��*����"Ϋ����uH�����*w�`�g6.˓/��s s@3��H�P]5�g�¨��[S�.�j�IW�5#�J������2�d��ʡ����(����i�:ɞ2M�B2_1*Nʞ��+�Қ�|^WR���9/x�����r8���¾|MSⅤH�SM���3b�j��:3OS�����q&�/߯;)eWR���o���1�
�
���jQ1�U.]{6
��!�3����@�)q�f��pa�ΉD����P�ux�׭3jM<��8�P��'��tH=Hzy"�l��O�ho�X#�}�tO�����w�.=oͯ(O��_.&�G���)��/�����Om{���y�e�wu���:'��{���kgt��~��>`�Ɍ����׏��_�^��Z�A?���Up��������V�����ݽ�Ǉ֧c~\9�����]�a�s���ұ{3w��۴q�x%�;�hk���śicq����N��;�s6>����h�Z������-v��sg�����]�=�k]�^?՛�5d,	Hm��s����Ak1?���	�&��v��k����C���K�+K��"n�%'����6%m`�2Y�cyv��ʛX�y�:.�&�݁��sD����[i�1��%I(c
)�1��Q{g�-h6�6��T� �qZz�J���#��w�:���\�eP d����]����W�#M��t%쀑T5頚\�\�����WwK����`�3��p17'd�V�n�����ٿ�{�m�K��cvz��I��%-K����K�4j @%�
q˱o`Q˫��o�2��v-�^���oo�2%C3w�vv��}==k�{5�T�AC���"�V�.�˼V<m�Vk�_hd{i%1�Rfj)<
W�jo-�Z��{�`y�=�w���3�&�	��_�����P���x,���a%�ܧ��T.?N��3���闲z��oֵ�3)��F�X^ 
٥�,���(��k�2,��t ~@�җ8S$�C�N'�0��;���0h�	�)��#h�d%�rQj�P��6�����aQb�L*/07` �,P�� �W�f �l,ԗ�����vK5���K�k���Cড�|��-QGY,��b�<d�_]��b�7C��  