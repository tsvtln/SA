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
x��<iw�F��s��*^v�5G�<]���Gd)>=<h��@�B��������>� II�����E��U�uw7>]��s��8L�`�Ǘ�|�eF��_่�8����t�o֫?��_}���a+̉\����������
%�٩�Q^��_�<,y�g?U�m>� ������_%"ɳ���s��G�[�:�v�r���wV����{^p&���)g]9��Y��.K��'����]�lu�Ey�� ��
�$ee� ���I�r߀�I�|ʆ0��E��,MD)|ƜߒP��,�`Wg
��daU��L�05�$e�E'ٹ`S@��,�W�1�c_��YV"��<,�9j��*� P,<8 +�8/94�dS�'T�I��w($i�c5�@��t=g�@���%�IV
&�1g#�NXɯKƯ')L�����s$P��M�9K�sbi�W�0`E��
[���.��5c:+�_��N'O�dU����%Pz�Ѵ�0���Lx��t�E>a9�N��Ox�E�(ǡ(y�Һ���c��Ϝ�A(x ��xL>�y��s��Ip����q>���m�G9��$��a=�����������:����X_�H�u=���c�?1
���eד���-���_k�am��Y"n����fG>/��}`�:��x  ��@$��K n��F�Mf�Tb
��`�u���_��=`{��<��gqPp1)��:�S��x�����Y	�W�ل#�P�H��{�[8��p�t��d�=P �P��g MʌDdNY^R1X�
�W�
6P�|�.�s^:]��}�g�퀕t�5f�ڙ��ؠ #?��@��!!'�2�yI�:�hD�
�� y�
�.꿍$�ڭJ�,G�+���O�y�F,���*���g��FY@N-�� s�EѲ!v7?�� ͣ�o���w�����k�[6~��DI�?!����2 � ��.^t�[��'(l�
dh�nRO��A8,i�~T��e�|~�~�܄R;[����S���&�Pd�R�_�X-�l%��R�'G�@x�z�k��AMc>�/A�:!�p���b�\�#NW7�P����?�� ،p9��T�{���	م�c�G�W>ғ�zLઓʘ���ƴ��atY%'9WX��{fF��")�#�v�0��H���P��H�%��BA������۽�W��^��E���ErLʞs!�."�D���!O2'�Lҙc��X@���Ѭ�3H�aN,^{�u�e�&��I(D�e�9g�S��m�-%Y�bX��&4?J�A���A��W �i��*�� ��������흁]GY��|
�C�P�*2��s��	���䙺V���#9��%mHo�4)q�sR&iRB��Ѥ ˍXR4Yx.flXe���P�dF!du>[�&W�u�*�8Є3��"ClyE�? �O��>̎����U1`[3����!���˶0p���3e�2�gF���-��_%�M�'��aN��\��k�I��ѣ���,:�0)C��UE�8jQM��C�j�w����y���D?����t9�W��5�k�(�×zL�d�ĄG�0�� d6C�}>��D-㪵r<Y����uٕ�6S�=L� <��
�
�&d���d�V��8GDY�/����|�gô�=,��,GB�;�%�,���'��Z�ፖ�J`�E6a-Y��B\�U�:��!c%�g��AR k�c	*I��c�7 ���A��K�Q=�I��!�/`��	�85&PՄ�/`��jjJߦ�b*X�bS~M���%O��Da�r�'.�CЋT ��PG	v��C��0��,�0��
#��*L�L��4�G,�h��9/�$>��Jf.��0ŀj Ȫhφ�*���9�$"��c
�=�(6HՊ ��BjB�(]�h�I&�`g	{�*����g��Pޕ�7�^�s�"cZTF�H�a�ϘT°q"WZ��ɉ?�֊��]�'�`ؚ_q�IH.�稔�
�"�,	�	d������/�33��p@��cqb7'���FN"=�������*���㜅c�	�?r������gN;�u���ö���l���S�h1h
��X�����gAg_�+p�p<�Cz�~4�8!�<�?&��X���ĂaE�s(���e(�Y3簠@���������~�k�S�5G츪�$vHq�w����}!oI$6����*����t���*���K�:�7���*�G��;&�����G���1o'�A�����{~�.�"���G�^�I�ydd��I�"=
x���2��Ϳ�3u
,���Dv�88B�d
X�FZ�`vC ���d:�]L[
��
�T͈��ۤ@M�z�`�נ�ɑ�n$�(_�}�m��1����$
D=�뼊"��3�y��:�a��Xg�b�_�5ҏ�Tw�NRF�$]
H����]=���p�������a��a�hح1�J)��6)�d��f��F�%�
B����\Ȩ�@n�c��i�AQ�1�+&gB��ӧܒ�����1d�E���ЊAN�tkB%}F��ܴ7�R/K��`ɐ.�f��ɇ+a��e�#�erw�bن�Ixʝ�3
�I��
w�q�������*�lɔ�Ic�Ka��ƜP�\[.m�*ㄐPcb��y��JK0mz����@Va�h�%����c:q��.\!�?f���n��B������M
��0�x{c�����q��#�&�J�0��-U7(.���P�nZS�T��~��a Q�E�c+�˶ئ����]���5:�@6C���0B�����xO8�5�ݿ��]�b�.4�檳�����16��ؼ��P[��̮��Y�X���3G����{:X0�~�w�KT��c���bhkh��͕�6名O1���eo �C�^���H
��VbV�<Z{٨��VM��E���a��G!j���BV@
*z �%e8h)=FU��ť��7fX�p+���m�I$	��`ҳP?k��hMA
z����[��Q�~����F�(�ĺ��Jؓ�qu�dA�@�F�2q�a
`S,��*R������;ͩD
�rLY�jA*x�1�Ä�(�M,Ib����W˩VA�AW���Ҁ6�0�x]���j"%ܱ9L�U�@n䘝3��g��^�-Ǘ�v
��R,�C�ڹ*-�@_Yf��\�lH��5�R���
��r%�^��Ўx>Jx�s��ً�j�c��P��1$��$�f)�	ěH�=(�Ql��+�3I^8��J�Lv)�rk͕{��"yz�G(���X+�$�z��},%Z����*˵5+����ET$��u�XO��@ [eTUwT���<~�Ǆj�0z)B�|%��x��T�wq뼁5!ёzM��P��i@I#�@2gڷ,	5���z��Iʚ� )[!c_�	�\-�_�y��b�&6|Xg�ې^`�p�������o_�ޡجS%[�-��8$�� LxHm�
���Q�PP�����?�� �Zg;�'��"�����:�X�k5����ŭv�����M���jB���H61���c�9�Y3i.C��fkR-En6Q6�lԺ�����q��.�7S&c�R��Mڝ�x��ޘ�����Z��<b ���m�l��ވ�F�[^j���לSl:"7�����-�q����"�gv1$B�&N��8}6���������:��|Y�C�,��zL�u��a���0�D.��H��UdcD��`� j�3��D�eՆ��apQEd�.��]$ã�R�܀�b�qA�0��g$��N�o�|m(�A����i��=#�+��m8}G�3kƅ��9�l���F]DbC�5��2�|����Ei>(C�JI������N��)m0�e$]�AK�(}
�GO��=̀�gJ��͵j�w7`�̳�Ĵ'�{�d4����.uҶu�	�e~O�P���oOj�� w�X��1�����d�d�٫mVZ��R��� �M���r�0q/�:��8��v��;����Z��T[��>'_�V�N��ћ9J;�`㜀�n5*�������{��F�B/m��Ѩ�����
��ݎ
�^�	�դ���T��	�U�uo��-��2�ʱ4O�
6��BE�T�N�,�u�ޞX�J4/��Q+��r�X"��Rq�#��e#�P\�g J��f�0�
t��$:Ĉ��ި�]�T��G��.��9�	��[�|C1Gӳu�>�֦YO�s�2���]9S�����C�FI%��x�Y Ch
��Y�P�j�P|��Y�wmѺ�p<���'c�h��h�d�R�ds]��Oi
��ڲ�S��hR�����!VE�v����圸D]:p��̶/V���u+rڛkL��oaa�>mO~�U�͚����"ˇb�W)^�;�	����ٵ!�Y��$�[H@�A^��T.^דo_��EH�C��j�&��Mw�x_<q8��I��(b�?��
��q<�e���RKB���׌�����$�Qw�i�Ҭ��M��%���U�zr�a@:�'|���c�ݣ>� k&�O�']��� ��7��8�c�slc�LgS�fefy�Y?��Ո���A�� � Lk�hTثh��K�e����$s��o��>ߌ�/�Pr]uGrɪ�oX���И�6j�ü�	���k(1�eX��-�m.A�,����-e��y��T4�X?�

��(8�+�����^��r���5�������j���&���)�w��u�ڞ�g:��U{���&�w2�R o
�Nח�
���
:5�G�.q���,O��faZuC;��M�fv{G�Q��
���L����M�Rд��u^���<
ԗ�z��l���!����</뉭��ʍ9�#�{�>�<�\l�Oŗu�Հ`m�ا͈6�`��v�UPC�RA�������=�{���*p�ނ�*��r�u"�v6��]̓W*1h��kf���ku-�wd��]���E�/����w�b����X��\��r�l�o$�*R��N,r�&����%q�2�ʒ�����P��D�f?mx�9�&8\�i�U|k�Gwu�H�4�(CG�B5�YYo��E�Ո�%{�a�K��j��t��	]�����g�H����k�]�
ԑ��_�uKjP1��o�S����>^�?)R��pA'��_��r]���������p����_����h\���٤�է��/��.�ȳb� ��B��h��*���V�jp�ܱK�x	4���S��m��#�%/Er��`H��t��c��40�V���}~UWW�Kn�$Kaȏ�y:����yJpz�?��C8�J\�I;�w^��F�=�̽m��<������
s<|�M{_a��;P�#���r��*�j,~u@?~��P���!�A�ꔨv�d������S��7�������?���d�9rr����?���W։O�TC.��U]������X��2a ��b��������t�ۇ����v~=F�Go^�����M��w��������O�_$�GǛ�/6ڍ�^�?>���գ7�f��ß�^���f��������_���W���w�׏���9<<:E''Ǔ,��M���O߿���;�/v7ÃG�?���L���/~88~�0�p��u8=����ë���8N6�\�)����N�O�ݏ��.7f�^>/ߟ�_\>|p�k~��a2��x����]���}8z<��:|������٣��y�����v��<s�S�%���z��ϴ���|��b
ב}�%��hX��wk�]OE�n�����EU�������_TQ���G]�[�7��]���Wd\�_��EF��	�v���D��2�~��W�w��DP^UR��/�b)贿�@F
���t�%# �	��$�M)�3�'~�#/BС����H�{h
u0|��xv�K�bE�ջ`���/��������n�|��g{�������]I�COo�no��2p��@7�-�E���&���6{:�i³}��:���ޫwǇ/_��9>�-���XO~��g�6{���_p��z�$�<�r,�<v���[�z^SW�3��1�d!W�/�V�֐��Oe��[4�[bx����iW7v���J���<v�?��t��)o
2���;b�Q�X�:`��ଌ_%­oL�^�o��������3s�p�F�3+0񒔕�t�Z~�G�Mǝ5���n�ƨg�K��*6\�}��fM����e��^
�T5�����$���d��3�m-/����YOh�Ә�~¼��?*� ���w�  