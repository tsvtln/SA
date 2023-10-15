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
x���v�Ʊw���z j"%ۉQS
Eɖ�C�(E�><X��@ �h?�^��3{� ��i�&������3�Ϸ�7.��za�N����YxK7������n���>������ſ���߅�4�r�'�R�FY2��q��`i/2/MivߴO�|�\;��f�4O�|���m�,JRkZ@GdƼ15LG#�-��� ���"sj4�+oI^%^@�ȋ}�ɓ$"�$#�.��,��N�H�h�w?�G�x�yy�Ķft`&Da4�ӌ��xK�M�,�/�����0���i�Hs4�n��/!��iJ�	%,
}J� <',I��Oc`��� *I��p��@Hl6�(��̒$'�	c�kJ��&�8O"���񒃘��vPfBI��g(��<>y�n�۳`�O���z��'�m��^��"/����Q�rN#N��9�I@��[������bq��$�' F�� �\a�0+ǐPz)����ph8���"�����I6�r�����g~�\T���I�����$a�~�y��?P�*�����qcƄ�e�*l���!eMH2��ӘN2:�t@iV@()nOYg��9����(&��<�1�/��́e�}�4�e��(1X�Y&Y�MSnf�|��W��<#m����KS�Y�Lq�9����S(�9戫xq�B��K��x��Ͽ���͒3���F.�i['�E�g,wGq;���#��o�%]1(n�@2�,����d<�� ���9\�k��zw�2/'���,��?���X,N^��� ��ːf��崃��F����iZ�V8��4��n��06�����5���
n���|�F�(�������[�{�C �Ƕ@�㆏�չa~	���ܙ5jq�6g����u�<�5`�9�����O�����<ry��B��ńN�|)�p�A_�B42����w����RH
��QbM��i�L��_6:�s�FK�:r�E��vFY^@��)�.(k� 0	���� �!���(�:��;��C�����H��-0D�|��Nu()�Q�����OVL�Wv����."�ˍc�|w�a�y[@��-'�a:�����h�wm�>|����q�9<�mw�{�X�1Ј�*%eZb�i.i:X���O0^4,��f���-��n���gy�Nd�7N<�10�"{Ņ�"d���+�C7S�)�)�/�-��W�D	� ����v	]Q!�6A|0�fI���i��%k� �<h�~g7���MZ��#M������Z���U̙��`i���- É�ѽa�#�r��ە���^2���I<��0y ��A��l�u�	˼��J��0~���%9���@�
hDjÅ}���hF��,�%U3�O �V7�S�XBUګ`~	���l�������kc��ف���G|��2�B�`L��U�^ Y�+j���r���Sib4�w>��Ѕt]wxr�����3x�� �8���g��'���>k�Y��i  �%d7y �yGx���8$�B���s@.>��a[W$~��NE+���'��^>"�N���#�ct�y2����O��*߀�0d!�B�IA"�|Ds๖7t��]���w��t���pAx^�����Q2�'��y0�al&�l~_�)W�qn�ku8􁌔"��j�t�J�:5�r��oA�8
#���nƁ\��ݲ�I� w4͍ܸ��!j�?R/c��qg�<v83�%�
�,��\�~��`�5.@�Zt��F�bP�l�\�IeE�����~�^��K�@9���k�)��W�`�N�����:8W5�2�
J,y����2����S6���eB��
4HJ���	�l�7��ȼ����*����E�ϫn����%$b�=�HE�TO�����w�*�R��Ef�
��]U5K�+���܃�/@e��5J��C�kz\�lT����*#I�����j�d���2re�DQ��1�ϱ�s/��D�̟�-V�N�7�> Ϲq���E��x��?�.��� �`�@ ��}=d�t����lFuK����a(�F`å0)���P���=k������:_	�=,M]����n��8	����㻴Ϛ
��'y��8��2���⨶��^`l�ê�4�� �ƭ_PZ��/@�`��-^�p��\	����J�k*���5'����3�H�2*K�g\	 %aR���W{�jc�"i
�_P�*��y��df�Y�U0RN�$��uH�R��'�Y}]Po�O�-�sp�������T(1���Ku,nC�i58
K�MG������t�.'�����U\�o,�Re0�'s!�1*FR*&����/2]q��`(#��v�q�4D>kb��l�*rgɩ7	)�=0^?���-\<ں��煯*�~�w��1.;1N���ڤ��ܒ$cۺp�'9�'r�,��'��E��A*<�-�4��@�hU7'�3.�3����p�'��Gub�L��؛k����S����Z*�Z���0ӑ}�H%�Yq�j��P�Q
|����$�u�N��7�{�J̤�]�]�*����j넮���n4��)`� Wȥ�\Y���#�v�鰙]��Jp�(LM.Ts��S
S,@�����k�d�!�j�n����Zmb��Ĩ֩x?��⢄�Rx���wzFEDԓ��.�e})�i�kK�]w��ϵ����t 񎢨�l!]��}�`� 1)4��
����+��W�/i�����w�� �# ���b"���=�g�Uu�0E$��]!4�Z��R�Ă�u���w���_Lj�Ox�9��-	LCظ�8u
|�}��
h�0��2Wd���:�������y�B�V������D�x��[2P�|�R��=}qpz�-�UK:P�ʅ��a�쾬����$�{d�r����FA82�(!X��ʹ`�N���N��;��ƛl<qw�6f6��F#H��žxE� K,9fgړ���c'8jZH�d/xS��!ҥ�?|NX�7e<Qs%p����}X����PV?|'�>$-��[���l1��`%�x�!�;������W �Q�-pH|0ŮA�� Z���J���ڙ�KȖ3���M�p��)f���l�FJax��iZa�0߲��Ԕ�)C֩ئp�x���"���qy"=8Sq��tҽ�^��j?�R�7eQ��f��%]�Ng���p�H�u⫹t=�JX"��t�P*��&���V��W
�X���uu}P����^B����w-��u
@)7� x���sj��H�bW�RW�\Y�waL��%�k�����1��ɀ2�ԌwKm�@xD2���s���@���:Ŷ�v$��M�,��ph���Q�p���I�	�����
C��^�Յz��/�l�ˤ�����i��/ڦ�.��&����_/>����	�h���0�?���ZS(R'^d}�e4Ѵ�[@h������;|�;��ǻ��o�^.�;o�G���U立��U�;ǣYoys��w�|]�_�>���� �9�~�{�z����r�a��{�2�9��޻��������erp3gO>����{����9>>?����i�<ݻ��?�����/�w��{GO��]w~<a����wG��7{=oqqM���|2ߙa���*o�M�Ow.�Ͻ��ˇ���������Û�G{�o���p�x1O:����'�������I��Y�h���q���ỏͶ��Lut�Z�?�-O���a�d��/2p�(�b�2�>P�p�����(a7��
F1� M˳Y>�J%]��=��j��J�#W���
4���7h����!�T��2��x���Fe'��|�4dP����Y�S�	A �s�q��:�8�?˱)�wv����4��t�O�aXG��Ƞ~���X=��K�J� ���	4L�m����[ķ �*[���Vm��,��&I��{py��н8��8><p_w^�t���Q���!�E��rk�K[��A�DC�r�{=}/t�
��p�5��E��ë�=�e��"T?{q|��sq�/3Vz^�VBޗ.A���$�v����o�d��$�s�r<��ko����: �$'�Ƅ_Jf~�@�5W}
#|�7�`cP��a���	)>�2�%C�1k7˒�,�7�Ĕ�(����c�(��ʨ�4,�?��e&��JQ�	�W3���$��4���r�.���y�$����	xlM}r�����jx��0�;C�ϋΉj\�5�b(�L��Z%��Z7����W��x�3�_}��Ë.�/����J�Urjh���x�s����7 �W��  