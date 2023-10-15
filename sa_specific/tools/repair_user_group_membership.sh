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
x��;is�Hv�c���*��WE0������	%ђ��a���Q�@�I�

��7������ )�35�-;+��]��]����﬋oE�9a �ۿ���˺��?������o=2�#fyM�������yೞ�>p�bO7K'q�^��K��r�
#�l�Y:i���9�"���_�u�G_p?bD
;��,��tΓy�m��@���%1�s=��Ҙ����wSw�
��D��GO~��F0��I��R�b�J�)oy�l�i��ݞ���vg3����R�7�bDf�0�Ni���g��2��6ZͶ��8��n�*�91��Țm��4K�rb��h�O0E�I L@����MGq2�ɣ$�2E����i1�#��l���cy⩷���n2�!�ah��6��.���jJ�8e��y4�8�'�pn��2'}��|tb�P�6�J�	��<E��h��p� 1�0��w���7G�z�Pi����I?�����w������/ �B���@9�'�P}`,N�F�B�?=HD�V1Q�0	P������I���,U޻sN�94�F{w��em@}�m��a�ԝ�x��q/�%l���+P$���u^D�㿦��l��^���t���g��Є�pTFs���/̶m�0�.@��~1/t��9{Y"9K�%J�4�.Z��%[$hb�&q��-YdMb���`30�`2�d�̥hI	���t�0^����q0�0��p��H�i1�y�rS���-;g#����Z�0r�ab%|��d@�E�iB�<0\\���|f{�Pd��
�8�&��� ��ҡutK�p�b�J�a��HU��*݃d�l�&����%0[ �Z`]N�Ԩ<�f�M�Ś�Pt6���S3�iʧ�����i �S�i�N�h� ��~g{�x��`�A�@y��v�p iˮ��>O�s���l�'(Q7a���]
�L�ri2�MI����C@�I��4D���#L͢����-�f��okk+'�TrB�Y�	�>xs�����ZeH5���{Y�-��ttu��R~�Z��~�w�c����7��L���͒Bأ���V�j�:'�h��)���0���p��CFY�{���?�0r���0�60�	h��H���hfL�� �����bW�4��;LzU��w����]���9���
����17����N���(���C����3���(MN���9�ꅙ��VRl�Pn-T��&����E!���<�Ѵ�9�6���4@�*���,-I����>��P�� ,(��/(% ��iR�ȝr%
25���1x�x9��=#�0!�ɒZZ�(�P�Pr��%F�!67�o@ȹ����/�=Z��l�����"N���: Ć�� �\��}�=-�UN�������a�琝x�-�W���4�A�,Hh0��]p���<�6���(�H�����I�J�I���[��24�M �a3���9+&S.:Lą�Ag�j��d-�b"n�d*�(
��a���#{�ٔ�	TJ����lGNw�J���Ho���l|9F`���B<�Ѳ�8;?�o���2��4�{��{
ɧH�˄U��ha��FV����*?W(فr��dg��]`���mս}��sE���/UY�e�r\�rY���XE�_�k�kV���50�U�温F�ؙ�aƍU1�^�%q%����'�g�{$�-� ��ĝ�!�-H�n�wB-sC��1+O@zv]f͎�J<[C)&��~Zo�%�n���Nޢ���tvh�2����_m��>�đ�M��
�f�ξYk����F�6�Q�0��mlMz0����b�EK�V�emh�k:M������q�e^  �\c~Z9M��cHh&`�iM�����d��Uu$i�h+�N���9�1�-h�k�A��Y6�uώڲփ���.\�9y#&ͣs� ��7�^���WJ:�LUe���T�C�Jm}��?�Ib�����,y��]�jy�ѾJtO&�l���H���K\u�
��3w�q=xN��+h{���+�x��v�
H�"�����+i�j>�1&�`���'
.� ��8msPNDRJ�@�uv�D��b5RܴJ��.�?<�"��L�a�dS���\O@Wr�{ 5HB��E�즫0V|'P�T�������YU(C����c�R+<Г�QN���Ȕ��E��/k�P���?�jy��$�SV~|��9���L�U<%2��]5�m�hfDŝz�\�*�����	��(�[
�}}s���Ȟލ��K�|x�.\H
K<\i.�PFb����j����9�a��r��`��q��ԥ�M��| ��7,�;3�[qB1�JH"�p*�~�[ 
�DO,�r/��␕������Z%)��(�a#l-COU��
��j��d� Q�߼/������M��[v}��8q��<���ģ�]Q���cy��~�ɍ4����}`���D�A� Q#�%}u�Y���Z���1Le��/�g�wY�Fd��%	L	���`�B��$gD1=᢬���P����W\15z�=Н�X+������v�ȭ%�,��z�#e4��4/�D[^���_=,.����Z,Y�;�.s[�6��"Y�9h+*�@&����K�*p/xͦFUX����Y�v�I��ӨVI���c�a���h]�l17Hĝqg3gʧC��&���O����?�-'�?@P���`���:�xu��u�8��l�� �Zo�&#۳%{�3�W�����F���n׆?��(mH:��r�OH����\w|�T0uÈӽ=�GsB'@��3�����a�
i�5�.ݽ�^��읞�Oߑ�i�]V s�A �JS�� ~�Y��1�2���Ӌ3����;���h��a��I�y�$��<���&�-X�!*戜LC�p�Gt���Z����&RA6?EH��&2����2��a��B�)p$�P��||��5K�
��
�C�f�?�䟆��@a����4�޸��s�(���lY�w���b�]k{��Szj���[;���j��$1R����ǆ��"׍U��/��	-RGh�!4�xⶢ�w�H�7�\eH ���
]j�;i'ɺ��Ez%��W��hQU�X]����,�u ��
�8L��F�]q��V
�ZBF�hǭ����%�_:������Q�8��)���ę����
�m�7��}S;$WO��1�A0�aJ�
}F�jnPl�s$�x2j��	A~�	�-��!�-R�:
�؋$��UTGa&&���S2ha#ʤ5ϗD-���"���XG��ԏ�TG��VpB\�:�����rI�� ԳY��X�$6Z�(��"���`�łuh1
7|&�1���;��}��N��掲�1�u��A�k��ݣT���Ց.�EU76��?�/lø@�q���k�?Q�&tH$�i!���S��%��
�'8a"�⌴�$�M�<�H�jVeW�~��r�*a>��zp��J%r���2�	RB�>��R���.�"1�^V+���f*1�Y��,��,R���?��xlǞ�5���T��]׵��9BiQY;ٔhM���R��ށm*{�h� �������M���.@P����N�UY�)�ry��C��	������	ݿ���	����d�5�M�>�?\�$���I�+94��[�'Q�T�0���T�M� .|��}z�&�H;���w����<��u�܏��F�$��hf��{��A�;�tfΆ��c�jsZ+�sc��;���;����2*�g �53ݡ���[8<Ip	�W�����X -<(O�I*@Ƅ �gx��F��q���i�*y��f:�m�c��Y����*��<U�*���E�Z�T3�|�I�A	�+�fq=1�Cɔ�F�-�����j�f�&c7�K>�t�_��l����cH+#�\��:EMtk�(H�96����dь���f~����0WB�B�'�%.���\���jIF�`U�seH[���d��W�_�5��ẄM��\.�fk,��I.�
��iq����)����7QE֋�Q��QO��z�p�#�L2<�J�)�K]�s�,g q�b/�Z�/[�W��ǻ��5Bgj+A� 4 2o@Y�De^.O��{��5�+PJZ����.�Br��o��-vb��<������Qa*̩��4�v��i��hQ�X ڔ�:((M]8%W@;Ь�,K�o�r���Ep�ۭ� �+�&��]�rYQ��w�:(-�]X�"}���-)�Dp>ب������{�wpt�λ'}��qzb~Ť~o@���qO�7ݩ5���jG�5	���Yב�ro0�ڍ�{.ރ�l�|�����P�q*ޡ���yE���U�mk"�<,{(������p�hڀ�M�r����������F���(DB�h>����pF��1�i"#�C�%�
����u�+��v�˝-x���'����K)�V;���UA��9kt�w�����/o&T���%Y���L]!b/�$QPM,-���;V�X��j-p��nL��ߤ�s �ګS%XL�/�ǀ]x�2�f�j������*ƱN�W��o��r�
�hl��h�,z=B�BbWsq5ﮏ�,?����Ho����6R�Ւ
�U ��F�t�����`ĨJRY�:��u�]F��;���\q�'1]G<�Tɦ<�Sc�:�r�底0��̵�`M�t,|8�"��,�W V�_�����_p�;�y���R�܍�8��/��E1��뫯�<�������-���'۷������X����=䭩�膭�a0̿23�Na���Ɵ��g�~���?���.>uߟ������w� ��=e����A�b�$�
�;/ov~��7Ϧ��>>���p�\|��;{�o�FA��������ӭ�x�f.^|���t����v���7�..�(~��Ct����߾�������w��?������z��ϼO7O��b�������|s���>�[O'×��7����������q��b����������0.�qw�槭OG�������E��Y��|��y�Ë��>ou5���\C����Ͼ�s7���`�-�}����K���K��f�|�e���8�6���k��0薞?�n�!���s��95ʆQ&�j�M�w�Dp��gW�,���P��	{a�o �.��ݒE�U���$�!_vSn2YDs�C~��yJ5�*�C q�L!�1)�6!/��;�\XuN����T&$�&zpJ�W�P�l=ӦZ�}mvv��^�Cg{18��u��G{��ao�mo�E
��/L�����L�����v�,y��&C<F�ӈ���
O{��%͜��������;8l��r��1�7�����Q<�4���wD�Sb!$�����؃����x�5Zս�]��ӡ�6�W7�1����[e�p�ϖ�F ���+3o4���#�w��o����O���k��l���1_+�\�i(��ఊ{
����S�[�V��tI
T?�G^8-�*��C\�=��M��VZ��vH8����������^�1a'1b���҆%J\,�֦��&0 �s|�����*&~~
�X(:4CYȳ�|iZ���J#��Z.ЬN�eu����FQ�T�ƨ�(�����Y�T����os�o�/�|����?9[e#�  