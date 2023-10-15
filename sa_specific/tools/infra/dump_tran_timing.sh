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
x��W�n۸����5���E!U�%iхxk�&m�خ���@S��X�EzQ���<�=��ș��p�!�9<�wRO���7�B;�����?;� �y�C�{�N���a	����?���zA���o?����Q���ы
�2�t<2��&Q�|o���\>�AQ�d{`楶�n��V��d|M@d�'4�f�&��p��8����
�����z�������Q�������=Ƒ%(HQ�a*Ajo�U�X�q0v0�K��������8�֩-\�FC�3!psBy���m���؝aNW8mD���y "��(�"��1�!��,�!l��zC҅����	e<�DT�k�c�`�����-�P��G���vn���SA(3��
am�	b}=ԄQ;�j{D��������`�E���� ͧCeS��a$J`ı���I�:DH�R�p�� L�@�!�B�V�̊�7N�\W�K���Ï�pB�$IcZ��d�fN'@gB��hn<���K��2���1'^��*� p�X����}��������܀s�.0����S�cfePV�T:�+�Aq��oۢ��3���*�H�A�!���CM�R����E�]�EP�8�,���HGn8|��5B�T�j�3ߜ<��`!)��e;�[ )�8�Ms�x�ꪨj����1%�AP6���7��fJ�>1L�(���RW"�Y6�@��d��3�2��K�,�� >���0��B�+&܋���lCr�4譓�&U���g���toX0=�ʄ�z�`��C���i��sͭ&4�=�lן�V��@Q�	N�Cz���U�KRC%��wu=�;�:̱ ��I��m�)ƹ�]�������q.���	\B�
��5��?^����&;�va�"5 JB�%��a���	���u bQ���W���#�������vw���`iD�[Ѐ�¦�7��
��p�({��d�[v�h�O��~Z}��.V����Nݯ׵����c��.��l}�헾x��M�r:�|�;�N�x����dp���݋F��)�C�{��ەW�~T�-���]p�>=�*���֔���8�N����w�k�/�J�N���O��6��_[��c�0;��U�6��r�,�W��t4���G\L������g~�o���G��hr��ƫ�eTs?ޖ����4M�ݓ�}��JO>�'���RU{��l����1�'���K��$�:��.�C�:�陌�84\��B)�{�P!tM	P5��W�(<Y�36�]�&F��M$����h��KhJ�L7F)�Ṣpe�.��]�,���NB[L<��c�dj������~�Ns��9�D\f!ʢP���c����H�}��qʧ�"� �"�ؘO�84ӟGZ��$d@4�-�����wGL�;�~�;����K4\z	̼)f6Ll]������e����{�f��\;;o؍v�q�jBZ������?:"�b����
"�cyh�`!$_��}Y�qZE�\x�/�{'Ĕ
�[G��]�}��S�5�>�5h���(�5Iiq
�̴ݪ���E}F�����ފ4e,�\x��Nv�0�?��|�]W>���&6��L��~Q��B�X�-Q)�C]Y��D��|�H�@����vȪ%���q�1�b��;�W��}���2�iE��;R���(�RDD�1�p����_���-!�m����='���+ev��:�`�*0�r C�I2�gB���SI����E��y�� ��^�pCz�n�f�k�M ��$�Hhf1Ԧ�l����i�����;f�(�2؟�Y�����"   