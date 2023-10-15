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
x��Xms���}��f����d7� ����b��`�cs�"- #i�v˝���̞�� �qz;{���s�}����,~c^�퀻������l/�,�o&��C���������\�~��������?���%�1uؘ:sS$�2�©�Mb�O}oL��"��uL��Ś�_Hcw̺�����(k���ILǄ��M�B}�PGz+�cF\*�:��Nخc{�Ȕ[mX�R+�)����Ɉ�td��:%��0���EＭ�D�ʥ��f����)U[��M������	ɩ#9u��Ov̜
��t
�=ƶ��S���˄��
���<����'�,15�k~xࡁ��@M~��7�~�C�k�L<滢1����HG�����h�3�D1���38Hd�(�aԙ�`��n���F�O��K����é!�auT&/I�Z��e��e�3/�d#�@L<N����hR��w�N�k8�ܱ���)��
�lB|*���r���\�!I#ź�^h�z?1��dMx�
2�$�����+��e���L=�������p�y�C
� 8��	�Zp�x��(���I�  C��rG��淃�-�v/�ReE�
�$|�ܠ��I$y}[��D�*���Lc��?>_ೱ��Fi&e$�Jm�g�
��z�Z�{��ȱ��d"�|Lے7���g�Ξ�[�S�)Y
�#_���q)z�g!]pk{�����{����f�"�N��x���ړ3B�c�)#�2��N��C:� O��$	��LP&��L@�	�p)�3(�38x�ف
���
�,B���&�^�0Xs<�T�"��O�9f>_�d��B`x�R�J�
a`t���f|	A�� ��lJ;E_� �GO¿u��
q��ciߛtMǀQ^.����8��j	g�ܥϬ�A�Y��;�poDP0
�T���t��%�q�1pU�%|)t�R������=���P�&#�t3.�k���T��|\ۜ��ܦ�X�o5�~�� �K�3�f���:�A��U�*G&��n��-�	�{^�.
e�[o��Ges��ry�20�m��j�&9UY&+n�'=\�<��
�����9o��Ŏ��V��T��m����P��^G�/����׷F޿��f�Dex6�as�����h�ɢ�vS�"ȣ1����(c.�:9�}=�p	���X�`���I#`��8o���J�Xa?d�P�����E5]r�
Ҷ2����cN�l���6AZ:j�-<��/� `:�kN�^�a�ICF֘����cਫ਼6�)0�^��n���A�=Ge3A�б)1lI�{���n��ʃ��\a��Y��	]$�
j�BnB��7�9ܬ���JL�FC�5$��fҦ��Ϋ>�Gú���2L	���<�����=j��N�w�)h'pQ�d���Զ~���
%4��a�>*8�S���~��;��y�N�7�,9�
���:F-N�^���e��O�&�"�eس��xW�������Z^�������y;���x��rH�i�k�%hQb���,�-^���\����&�s�9s���Ō������h��xS�>����{w��n�y��k^�&������es}�y�ٝ,�����ՠz�u�����|�ݱ[��_}\^�$������{�rzW�'���ޛ���W���&�|tt^kv�����Qȏ��Û�won.߿m��ui�������T|�'�;���n�E��;�r��٪�^���ZV�g�� xK��W�Zrs�Q�������OO��x}������ջ�[:;J������E��޽i^�??T�G�8HHF��oL;<��ba`����	�e���0�5j�e)��B�l�[ݺ��{��h	����4/��ôcO�B5+4�3�VA;���f6c��`c�b� }�H�^�]�<�_w$�+�z��:gf��{qՄ�-s�	L� 	��*�!��hk$�lX��a1�b�������6VD����9�vZƥ�J8���
 ܖ���c󱈪�������Xb�ʋ�^>����/n���釶��
������yrڲ[�N�}�
ǒ��Vt��D�*T��@(�̇:VoEJ�pQ��_��um�;,��4XԷ��.�26s����~�������,��B���ϭ4I)J��Ei�W*v�����֊2�SV���L2,|+�v@��#� 	��*�.ز��*J�[�������9��A=�N�Z|�f��i�L�O���|L};���B���JW�6�[uY�c��
��1,���![#�e��˛�=��|� ��_0hي��"8DI�v�xp�zEN[5"}MGC��BY�f)H��Ie�@t>Dcτk����`�u�|� }}���/.�,*�c��j0e��u�ZZ�Y�{������+b�LlZZ������	  