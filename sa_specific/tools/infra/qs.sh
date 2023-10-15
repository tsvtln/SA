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
x��Y�S�F����/��N9�#�$��wd�W	Ix�#�0�����$������~���ʒ$��eH���{W���ɺ�~���E��o/������^&������/���U-������͓�Q�⿜�D4{~،����ʓ'��Yn�m�Z��}>����f�B����.�,o�%�����QO$���k(*����ҏ�Ώ�u��ѐ���M	���$�0�#�~,��/&������f�A4�l%�>�����RO0��d~��~�]hP��iB��CƓ��&<�2m����)� ��cd�#�̍�T<��5�D"�1O|��1~1C틁������QL�t���1�:5�K�<�Q����� ��ծ�nĆ"U��8�G�E�/i�Q�v�^�*��r*m�iի9�
Eb�-	E��O�׈��|O��
��}�Z� ����5�(�pZ���w���G݃�o�g�(K�M؈�Sl����$�����&a�D�KR(x�`/��4�k�(
x�
e�ܯ�/�*J��x�,�d֣	8W���.� O#l��(���7�l��L���h���X�YPS4^� �t���Ɛ��(X���8JRw5��`������4� �(��7��q��a"�BN�y��^aߪΥ|<
����W�n����x?� d�D#X}��T��,	"P[�<L�*8��!��Sa��-�>���$�;�U��]�{��^�|r�X:d�7�Hn�*x�z/n>�UVG�`���'pg�r�������D$8%���p����)���:S�S��P�%Y�A	I�L���=�D��+u��J/�<Pz%"͒�]�Tr��y0���Gz��!GjC

+2�c5vE���(ޣ��z۬j39
�J�΋о8;���X�ayiw��T��g�pܶ�c�mb/�f��z�(�~�L{��e�no�gk	�z˝���n�^L��G�����F9xD�fUG�+�*{�ȗ���v�v&��RWMj�唏�ZP�։z�
9%Y�6�l�4g"�Vy�"	Yk^�zC(�ԡ����l5(O��*�Ku�/	���(��dE�@�"�J,�o���UZ���3���ƪcg�QL�}2� -�<5���J�s�xJ�)�gTXQɩ�d���n!�;	d���׳,h��۪��
�?�(��S��'{�W��n��7?U��m����g� h��`-)93��cՍ}t�,��Z�� Cyݾ�n�tV�77��?`�tF���6�ʆ��A��>O�I�"�-���IU��X�ꘗjrvQ�
�u�G�o�ޙno��dR���RCte$(���]j��zy�̇�R�3v^���LZd��t5� ��Z���z���:����Ӈ �f3C���������r�:^��&�C���:�\`��)oLSB(&s��J�s�{����OP�|U���.V�&� 2�݅�	��)�:�2�z@���(�J26V�#H�E/�/��ƜE�p��o�
��9�a�[F��V�w;�y�؋��Zi��
ʩDi�25�N؍R�P ����0a�ch1:S�~�5M���ҳ�%�SCt=]��W� �q�x�[�,�����v��;HL��iR'#4Yy�Kj��k��&o:p9��@k-Rڮ�Iךӵn����eׄ�H.��� Ȥg�*�tE�����2�
�/-=e��J�����~s��찈�`���+��+ۜt�=�R��iPO�0DČ�u� H�(i2���X�jԢפj�Ez�̚*����`��~�q��,m���-����lIx���
���<�"N;KtX��(C��*��q\ǉ�A��*.�5Yc|������Oa)��+� T�6����aq�1��x�h�p�k(�����Ad�A���Yg�����������/���$y��i~�x2�{�	�����U���(���&�'��x{�b�M�5=��<I���pW��[6G:2�>��f���r���`-ט���A=�I�#M��j���E(�:{�Zy~û	KT�`���]��EU0��RcjHg鿌<(!V�3�l�u���Y-W
�:� '6�����z}΂�	�'Ğ4P/�
Lč�n������t&��9)��:����2�&Ci6����H���?ơ*��rDs��|�:��u 2Gö��֣�ؙ[ۦ��wzs@Q�����`�_~��y��sE���׷�m�,�7s���E�.�����<A�W�m}��3����dNuk���OBZ�G��Bj��N��F��O͕�.=t]��]����IT�l$�8f�@��Yo��O�]�M�a|ql��;��m[-{äJ��G��f4�b�o��L�T��bRx|�a��}D�j.�*��q�V�q�x�q�'�������[�W�E%�:4���}�]�����t%��F$��Dz<h|�^��Ab�Qh9�5b���m>G��������
�-���ߧ;�K�O?�����ë��;��{��غ�x��o��>?{�v�yy5�|��;y�o����A����O�[���Xn~�}x��z��9<<;�܋�nF[�.ë��:}�rg����!?ؼz��y}$?���������w����{+���co������e�z������|����}{z��m��b�������h����M^������ۣ��ۚNO��Ov���?�\n���ڮ-X�%��*�������Ɯ�N�6쾠W�3j��Q+}�
nad�b���Q�i��j
��#��T�$K�~ۮ�a��n���i�l@���=O��V)E0�m�@��	d���~�N�%L���o_��ݽ���p�`K�H/�^�A2�l�y庳��F��G�cU�L��`�*`Q�:�jHx��#����/�諰�%���A�c?�B��ҹS�zr��^�;ݳ������v��ў�wx���`��_D��_C��`i׀����S#v�[�f]uކ��Ұ�Q˫�<���S�k��N����ߝ�tk$��d���ׇ��i�6�d�QpQL"m��UR�����j�n�1�+�
]���Q����!D��Ұϓ�]q�/������u5_���9���[�U]�؆'�5L7vB�ݪ�f��b�1�by����L�S�ոҚ�4@!">�_�e��Ӄސ��y�T,ڎ2���`t��B���]�?e+s6�w`Cj��<#�3��X�Va��m6O7���n `� um�ܭ> hY�'@Z4�Q�1bӮ��x�)�řc[�@0��v�}f��CK��  