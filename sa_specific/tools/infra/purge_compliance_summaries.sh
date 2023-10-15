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
x��;]s�Hr��.��S�Sy��NE�LC��uʌ鄢hIk��EreY�B���� E]���g�{f @R޽��nmb������g�����3��Y�>�����I4����g�X2�ّG��?
d�c���p��G�����h����;;�!�S%��F���%]�\Q�L;��a�\��DԎ���	�OkN��.<�A�/�� �O�?4
��!�r��O���F�.�N
�#313�B �2b;e��!9�跉k���f0�0/�h;/����͛��(&l�j!��ތ֜p���8�aܜ��Դ�s����c��-��UM�X^�Ş�{O�%-R�4��	զF��G�O
p0썉Q$�&�h�DA�
wq�`�$��H��D$��c�FU`�̤�����̺�+C��V��줧s҈t�L��	�
����8`��E:��N�mk����iw�V��3{��m�Ocϧ�i��i�Q߶����f�� �[{*��;ڴU6��N������7m�?���v�w��؉�҈��Y���ڗ�z�xΣuَOah�3ߩ� eh� G�̞�pL���:1�f��_߁"� �V���<��0=���z_#��]���8���	��!\�P	_�D��4�`��38΀A��i�o�{�:I"����JU��6���YFh���0	\b�,�/"��x0	80p\I4E�b�g��qf�~�ǅ�'ނ �=��؁�S#,q�0e�d9��`wJ� N67���)� r	�aaDt��$@�KI:KBKpT���t�sN8�H�F(xc"�� �N���hY���F�����E�d�*��`3����4�>� �	����j|P�\�P�fg��M�|�\юc:��(d��\HZ9���4���X]�����/p��d'o�	�����9K�2�B qCàiy� o�6�#u��:l�14�
��16*�~�����R��O+Ui�nb�z5����1��)ب��oS"Oƨ
Bi�0G!(��f��~ǉ�e��ď"�Ԅ�Iј
`:��1��U�&��Vg
lVp�%�H<u��%U"��(�7�uk�l��&�&�I=�� �/e?S��.KS*��Zfd.���I�aϔ�2�m<����2S�����k2�C��I/������Qȣ$&>��}�e�~�'��"�TU���y��|E��A�V�۞�Q>�K �ێ�(�4�=�R""�H��0�o���X�ȹ�8aA:�D��+[��]9���ʃG�q�����e:�%F!�f�5a4B��j�l�@��a�C�����N r-��[X.�|�☄��KE�������ˆ�^����>
m�q]��D �1�8�m��^0�R eΞ����.���M�W,���`o0��f�e�CG�9q>�ܔ�`0��eQ^ �-�L�9Jè`X[!0'�Ɍ�)�K2����jK,��K�ߨ0ⱹo�����9�T��B8���U��<?���a`2	kUڝ��/݊����eD9U���p~�4�� 73��ܠ|��ExD.;�Y��WfHo���-�*�e3��_���~��'RHmȓd�R�o��)��\B3R{V�@OO�Y�Q�������j�bv��Bjo���
�m$r�5"��Ȟ�#�g#Hq�o��,4q�$�4�e�U[b*rLeKv,��y�,�sܷ���s�����	��[@q� s��}�� 9sSe_B���� �C�R��*C���sQP`K��fιF�5�Z�.S#U�����o�.�@�"�$d��O Nˠ	~�|<?S'�ͼ��>wA҃����l��p'yY���9�5,(��ؠ����"��C�'M��@W
~Wg��G#%_ǋ�u��<�~�3�S?y�����ēA��"W���,�� ���02�j΋��?E�CN��)F21g�d�D��v+q�Cʨ��܎&-��)a�6�`�=�/�p���EBʠ�	�2-\ע��ܫ��`BT�Pl�g�I����>�9Pu����R�PaA�m�2��F�;.Rqx ۟�>��c9XK��$3�V�	�<���5��� 	Y�fu*P��c-mI-��NYj(�����Z�
�)i��v 8Ω)��f�md�c\��ͤ�]
�`�%�Ʒ�ݾ��i���y|v������L���┈��j��:R܈�;ՙ�:���a��a�Ƕ��0$t��s��*�.]xWH.��E�L����/2�VK�cۡ�tuعh�>�xr���7�y�&E�?��nMK����Ȕ��e-%|X�q�4�#��$,g�J��Ǒy�ZZ��GD����VF��07@�T�Q?e�.b̤ڪ�.�V@T<nn�g���40���N����$���
��9�\<�첖�a��m��!�F���f/���;;�&���F:���E�3�u��I���0o�q��rs��gĽ6q�(�%�j� f(�9璁� ��P6-J�E(���E)*�������`��6Jf�]4��]6´���_O-�������`��1a�WN�s$���$K�o�F�M�ڨI�2Ye�k�*
O��ԥ̉<*��jU�bf+��w�0	�VC���F����' ,�Ѵ��!�=�?�b�u��"y�Wc+&6�[��P��T߅^ �|>�WF���$of�yD5�Ȃ�QB*nT	���M�ql�;�Ϣ�����)��8��]�����_��"�
y���{�p��Q~�+�G�DEJ��!��`�`��W�(�|����l�c0�|�q`�`ѭM�ȇ�pB���A��o�F�	Н�ӓv�ӵ�ó���5u�}qa����M��'����A�䔏n���;����y������kuN��~�_��wέA��ĈY�(������3��8d��A&�
),x�p�W"���S ��JNV���C���M9$R�-�k��^�]<~a��/_~����Tk
	ҁ��Q���cI��d9��s����[�����lӄq-����%�`״��ċh1�F��
��\F�R�Z�	��[AA�eg�m�Qz#(���E���
ċ$<	^�k>>��p��$����$��nl�	p�Y���ٻV����3r�iK�uу����l��e"��T@�}tFbU��QD�Vm��ͽ�X?Z�(�5 �:������8R��L���קK���0,�GiBu���������/�E��G
�[�=�
u�>�1���e����y�=:�Y��v���a`���%���t�Lu�M5_�#.�ĥ��;�v��%>�FJf�"[(�h,�|���#M��]�ȷ��,���8MשR���?Sӂ�f��(��3��>sb��?�������1�Q �3��F�a�~��r�x�'�0��jX`>K���ʖo����NҸQ	6k*�"f�*d�[�����B��<�9���3�ћ%3:0� �����P�Hj2�=>��J{O���ϵ6Xb�6�CY��%I�M�LQ�[�Һ0aP��+�3r�kh~N����La�P���>
�AӆL��v`e�
�E�X�]!�z?)\/��.�r�r3�G�5�.��Ӱ��^�Qp^Eb�b�HFI dD�����MF�#F��N��u�PM� 1�_����"��2i�7�9�W�݃54
7�0(��<u��^l���uΗ��KƇ$��X��m� ^����B�QG�ꇥ=�q�o�pV��k���u%�e��
�&$Q���OȮ�y�sa�<2�
:a $&������r���mL�D��&&��_'����z���6�	�j}u����B�5�^�Q�y�+��<'���~WZ&:\�?*,ƾsVW4n7=��
]Iِ`�'8�]N憰�ۭ�}�Ö�A~��ޓ�u��on�
7�陪����P��z#Vh��f�(�����Q��eU^��P�f��Te�o�E^��)���Q�״Ql�,}S��"���b.4+A-Oۀ*�ĉ��¶ O.�����B�!TI�Jbq,�_��ߘ[R�Oִ�?�t�A�K��Ï�ɟ~�A��O,�l�C��eSۯ=a�@>��>�P�������y
�V�??�rw����k�;o�W�_>��W�?���Iu�x��{^wp9�{���w1{z��l���z��2�ع���^��x��x����0<�_�7_�g�߾=o���/�Sg8̃������?]���}�;�?��o���?�������?��/����W}{9���x1]��\�q�x�_MGo��������Ccu}~�?�~��)�{���"l�?|�ߝ|��oW�O�7�/�����O�7����JI2�t�H�r�a����҅�x��
�0]���V�!`��K��!�d:(����k:�0Z��r�����L;��FO���}OB� �cG�3��r�b2��z-)	��@�/q_�&���|%��ă?=6�cg�O�
޹a��xc��ˬ
���'L�o���D�@�H���i��2B�������(s�<���hT1�4חp/o�V��n_\[ÓSL߇����}tұ:�����!�0;�9�7��K�J�� 9��@�o�"�JJ2��pXٯ�1��O�z�`��fJh��zp|޻h�+���bT�nl������U�_���m�w�d?߅o
,���)|U^:�Z�V�[�A'�؀�o�0SS"��oL�J�������.om-����O����:�@-`�z�E�ӳ�ƕ��lm��f`k�M֏QB�1���%���ti��$Yy�!& �3��l������iq�XHr���{0<j �b�i�Q�pDT1ܴy!h��+��s�>��c�D�*f���(��O���O�n�f���;gܝ�A-M-U��Z���ȩ@s|A��N�ÿ$���puՏ  