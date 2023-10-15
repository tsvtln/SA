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
x��Z�S�H߻ۻ����xf��I��H�-|K�8@@��K#,,KB#��\���ɒ1	�#W���<z����>�����<�~h�"���ݿ��(��Yh_%Q�I0~���<ql�wқ?����a����~�Gq���ϸ�D�̼biL97�8�����}�O9�|f����4��SgX�hD��
Ɛ�N쇓��1Kj�)�������<�qzŌz�FpI��n���$�Sfh����y�Io%#�g�%�/I�wɷ�?'�e]�`��G=�9�	#q�}��&I,$4�MG�C�HN&>���H�q�\kN
�#>)��{�S��\�b�VL�7�|g@܈q�F)�1#�A�$�`LS��CF ��
H]�Ր8ad�E!��&Q���5�\��ud����:�|�0�G��}�9Y#mѮF��m��d��!�L �K̔���xTVc�OC���#����+��(��)��R���X�/06f����x�q�P}Bw<���g.q�rQ�#K�R&N�՛�(��{�B2��
\���j��|��Ѭ&���؀_A?����3<{QB�lF��Z��
%��0
Z{�*�M�7	-M�Āa�n�Ul݄W,�LB�A$^DAM�O�T\����h0'&�,L锤	c��(%�lD��.��W�R��b� �<�@
D�s�l�����w��c�k���v~��\������u��l���/�~��B'�O]a�%���jW�	����>�
�[��Ѕ&2GYN
�Η�re�s��枞ե�uZ���n'g�	�i�]x
g��ǧ�W �� ��Ⲉ+z
	����)���&�rY�9�k)}#�TPA��\=":d$�<�|0t��8"�`c0;�bCL�S������l������T�j(�)�Q�8��WfN�1U�F�Qߥd� ��Ӟ&Fi�uS-Q�Iʀ�5�wb<��wnr����hn��X#�b�(�7��{H��0�_"==�8G�C�]�|�h����)�tak�+��+X��p���B��T;lt�v�m=��z���<����D/��W��A��JȪ0����y]#��̰���
��c�C#R_����BQ[���=�����}�k~�@�`"~Ĕ�����+N0߄�ʗ伃($�끞i2��!�g	f��\�R|���9:<�t�O4z��,"��o-��<B�t��c�.җ��)��S��!� ����/�X�} ���&.��J�S�ૠ���?pT��Y����8o����м��*Ls�~Y��HVV�7��|K�R-���D!�7���!	A>#�R��:�z:�8y�Wq�Wfʱ� ��� E�pF�:,F�s��ohZ��^�Y?��{Bޖdq�;B>������f`]E�?�e#�����"ⲱ�0Y^!��Ku U��8�� ,	YB
B>!��KG�|o���d��9�|$��6�����]�^��p��Ӫg�	>���3��(��5�#���v
(;��'�U|أ��Q0���jn�j���cs��A莵V�ǞP�����&;&���I0)��=����2�Z�m�h��Ǳ6�k�@�>f�����b�»ҁ��D,4�L|��Џ-��$3�sA��c���VTP�f��+�u��7r�L�B�}�t��c0w�����������n�����T7��$B��<>i�5O[�Ь�")k��Ji�H�1�B,DR��G��5�ǼA�A�P�i^�<�*g�:)4l
�ct�!x��\�2�;�2a�*��{��)D�s�?����h��|���d��'����i�(wc�ф�$
����9;�ddN��w� �.��T�K�Q��Qu\Z�FL����2?�[/ۮ{ec#�6Ve�*�i[v�тf^�t���|9���W�K�O����]��a�9�!c��s��*2@E��W��0*�N$c�Eɺ^	:���)��eAp�e�2G�0�Gd/���f���	K�!lqVClJS�n�|G��������!Dy��%t�@�����a	C��X,ģ��3�j�B��!l�z�2u`�����a�g������sw�|A
���O��p9ނl!�( Q`����Ia~v�N�v:�n3�h��`;е$�W�ʰ�K�]��{:ndR7��B0�!ۅ���������*��p�*7˂����=���;�G���dZ '�k&Z�\ۼKL���ihP�*n�{j�Q�ԫ^��V@y��l��,Y�����ʽ <�7���фh ��-�jWvAa���ǫ�v�F �r��z�z5�n�=����Y�������ӏ�/kφ��vw��ouN;[Í�;������'oƛg�Ʌ�j�䕻����^��`���n�3�͋�������z���5p��NF[O���g/=��Es�hg〶6ϧ�͗��}x�
ku.�9�çm:�\�]�`<��\�lz��=��V��t���������Mz���<{z�6��?����q��^�_�>�����쭷پ8i�f�׿6�6��\���0m�j�_lL}ه�"�e�k+�ǖ��1��oksښ��)s�U�������$Kn�ۃՀ!m5��U�������Q�Ұ��;`�/4y�̅��ؒ�\�����LHO�|��+M���R:8i7��U"��.�}��3'K�2���x*ʌU�����h�J�*����t���rcQ�:�#A=l��Q'�l��`��Xx+f<+M5�4+�p�'QhA�b���N�����=�s�����o������Ak�Uk�"�����צ��T_�*jȦ)*�/�"�;����pÕ�K�P�(.\���oOpXM��3���w��N��qJ^؜�	�2��-s�x���\�٘�"�$c�$�Iz�7}ŁYU����z�R�/��|�Ap�JY����8F2����F�R��a:�ˆ���b�'�Q�vȷ���E#)
?�by�(���)��#��ˍ*�0XD��y��yΌR���{P���<@c�"~ zB$tVF���X���Y�|q�a��Ǩ���5�@-����t�5�@sN���ԍd��6��`R�
�Zn/����Nm�`��ʲ�0f,z���Y�JokR  