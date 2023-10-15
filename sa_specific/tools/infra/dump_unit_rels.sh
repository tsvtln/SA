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
x��WYs�H�=����
��p ��2�nO�
��M���}�`�q(�T�@��7���?�̒J��)++�/��*����:|�[n`�������ڏ�u�r3�[�e��Ŷ鹌�������J��_�|���Ga�	K�NB��^�H'��k/=��D��j����3�S�:Z�F�4�ɒ�q�%M�*��lH�8��xq�D%3�-�cm�M'�i�OMS�H�M���ő���O�Y"��c�y��QP�'u��o��,�~��Y�j��Plf�c8�P�-�|DAi�@�M�ќ�^�E����5�fҩ��Lt���o^hkL#��(f��4܂��0�s��N�$A� �5C5_�(��Q���N]�H٤,�$S�A�Z�����zwÀ��HT��!Î3YJ�fB�4�Pb^Zʳ]�NU�B"!�|�a�N�ÀfTˢD8Y)��
R"TX '��d�`�q��| O�[�j�`��'��5���"|A)����Y�)@^�K^�Aj�������c��:4�������]NU倅���7U!D!��Y-hY�^h9�t�4H�#�^5(�v
�����D�]�hH�jb��lq�5�-ųE^�� Y�"��pє�.8�LFi�?#X^�&��v�6/f9C`eP���JCtJ\&���U��{��h���".e���V��^��g�;!rFn��!uc��
�W�{x�Ϫ&#�i�v�q�d`#-N)�
W�}�2�b�!AH�`�̴R@��,���9	��
�"����,���j4`σnC_���쵳��~Ѳ�#��f��6�9�hHece�(�Ycj��Y��Ez�E�6��|e�u�E��e*��A��
�q��{�e5�)4S����;�
VY��s�ڥ<��8�R���Ԥ9�e�ȶ3�+п�E��#�8׬x�7[������Z���{��!����Fz���IŠ�J�쥕*���ְ%&�qs�f0��r��G�6�N�[1�[��ͯ#��Y�63s
/N�srv
5�ӏ�����vѹ�������O����u�K�?]�'��������
�����]���99��9=&ۧ���͵s�
�������Kcv�v���?��Ͽ4;��]on��(�OF����w����;�����;{�-:?��`4]��<�ڋ�ɽ�,����7G��6G�o��'�GC���}IW����'�4�\�NOV����N�W��3}��X|x���Ir;=������Ż�����Ѯ�!c# ����������T;�#,.�WLMu�ġ)�x�)��+�mEW�� �C~����|�L`�4�.>
#?��bz�3�(�2@K���M.��^`7�sKI@�����E�@.����ķf.��̷�=7��ڿ���X�6ܸl�H0/C�	�c/��5�&��O���8����� m��m��b?S
USM� aS�j�_m"�W[8����U
B��h�q�00�3���*7�fw���Ksp7�/���Շ�߻��]BY�-��o^���:l
�cA'�P���{�m>c���U{�CT�eh�@�7�����7�A��}O ���pS���N�Q\f��鸾w���99.�'a��F-���q��ֆ]�}�YC�����)�V"�Mh�L�y��N�"�p��N�������jzvq6�nw�\(k%�K��|oa.�z<G�xcPŻ	P>�[�e�\B�M�X�`
���� B�`�& 'N_�\��ë�뿀
���^DJ[6�L-{N�X``�t��\��(E8�1��0�01H���T�V
f��
N2����"��Q��@��XR��QD��wHԦ��"���� /�M�q  