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
x��Y{O�H�{�(����z�lk����H2I������8���X�w��n��[��t:� �����ճ��������l/�f�;�s���r������_�oX�X����_��mg���?��ƛEa�	��
>����m���M�����`ԧ7X�L)7>-肖Fq8#N8��!I9F^���(���И�l�i,)�,�s=��Oz�w�6*P����e/���R	��FQ�م�k��o(Σ��~���Y����j�򣢗����N���0�t�O6{F5eeo�!W�d`�x	{L^vlӉ9�)�tD�p���� v<f�NP�^"�M,��W�^'@������	`KcXU�X��1m�B4D�t����$3��,�T�Mǋ�3"\�<h�d�(0(WI�A�/���٠;@(�W�1�|���'�0��SAK�����k�/����3p	��L��p��U�q�.���j���E��B/ 4���h$sDs�3�[t�Ј{a`0��`j:��N֓�_(�(J�� dP����ջG.�ל��.��k�4޼{,�� �3.�G��_Yw׷�[�׾m5Ϻ G�Rr� �x��| R.�m�WJ�'�fD�)[�� �`:�ȅF�����q(cF�X�ő������c4ք֑A\@$�3q}�X��9�j���P� ����
`��P'�t����p,�\��Dot�ܘQ���*�f��
��m��=�_w��
j��w`T�~�8� ���hm�ؙ��9��/@}F��b�`�Aa����=���5^=�^�
�(�F�K�%d8���7���j��P�
�eb���l�y���,X�^���1�A$�#�i0���X�*�.�d��"�"w�o�w�/���徵�W��ʇ�Q@S�ђY�u�i��t�{}zau{�������뮟IJ3���-$��T��2-M�7@�Q=Y���2�����^w:��I<��{����Y�	>��o�we���
��G$���I\�7V���Q�hL�G��Gc ��F`��O-�u�TR4�y"���k�9K�Z����Z1��JH��V��S���b�BxM�� �r5��ǻ("�d9O��	
�ԓ7Uvr���B���_1�2���z�O&�4�yy�-|�TLR[?dTDt1�#����Gy��hgO�䲚x>%� �:�)ŒCfFa�m!t�t��	�� �b����y�6%��b��r��v��/@\��JD��<�\pҧ�g�3��C��B�G�[�j�@�V ]��X�K$i���uAda1�y�C4�]_P��U
�!���v��E3�I��7J�k*T�3���ZD��i�y¾�"��e�X�`�닂�S��)yjHK
Цۡ*ļo�_���(�x�t@�D
���I�@K3��W�T*���S��V��H��\���;�t~v	
��������;��O�͓˖j�aİ�Qg���}��4?����t�����hJ�pR��C2p��q͗m:�&��a�R?&��J����j��$��y����`	O!b;���&�Z�s5u��m����Ӌ�����W�ǫ�Z�bwRlX�{0��˨�&�2^
�E<x|�q�,��ȧ���;b�e�)�	8�R.O�A�J4H^12����n__�n�e��j���{�!�lY��;L�E�}������D�Aױ� �{�M���=Z8;�ޜ��|57����'�Va<���,�/_X�������1�($����_9�TA"��h�@2��k������-��}����\��Da��h��ɞ�Ց�Q8��7^���L�� >q�DA?~@��S��;��BM�SHo�TdNxV�oL(�*�wy�gP@M|m�X�m,,�4�ο���m��i�!3�ϙ�Ԙ�1�ؾ��C�z^ơb�G��5<:$U�q��Ӵu�zj~�9Ǔ��/���;�����h��L���J�k�n{��i�㉻3{>x{�<��߬F�7��I�u?����ו~x2]���������u��G�8�~/
�・������.�7O:'���:�_?5?�����h�c��p�<M����DO��r�ܟ�^�n}�+���~��>y޼�W7��W��6��?��mo�������+O���x��4:�>�4[����wGg��+
ul-�Z���f���'�hT�
7L����$�Xq�s��높�V�������{�J<^��;�m�a�A���zc�t��~B�SG�/�
O(��bv_QPHL��2�%��p����=6��31��־�6����7�-� �{���62�Qg��?�k�׶�CP1��I�[:Y�C�-m>�t�8�vo�#���mBAM�g]a��=b��?,Ղ��$,�8̉ͬ)�@�uo���/Ϭ�m��>;����O��v���uf�Y3?:��#X�Ԫ
��k�hС�������V���!�P�euq�_q��J	�����}�}ݹi����˯��QBm�6��L�F5u�����r)BH(1Xj��d�5S��ڎ�G���������x�J �~����o̒�~���
J��<�ߜ�j�BW���z��@�m�
X����S��KDv6g��>&y��t@��
8~@W��"a�@���`�t-�?�,�����? =�$Vj;"嘥����%=�0���!
�2�07a�i9j)
8�6��-3 ���$K;�F6����bQL�3��7�R�/��s.��Ζ��83vq�7�_��UB�
  