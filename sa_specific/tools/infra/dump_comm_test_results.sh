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
x��:kS�Ȗww������j����B.�0U��O�?B�ǥ��6V�%!�3������Ԓ
�lvI������n}��m���r}s8w�:���\��,fB�Čh������F?őm:������ݿ?	������/�"����ظytCþt�[��:����x�,�N-�VQ:#�غ���PbU��	�Iu�	�TU�t���d�;����9��	<����\���oy
X����n��nH^�|G^�-i�f/1�y��ȼv�m�u꿒j�:QND┑�r=��M�5�q��$sJ�)p��
���&h,ꐕ�����$7�)���_�
T��X�

2��"�� ���n���M�2���ք�S����K��1�
u2j��2�����(^L=j' eL̈f ���Y,�6��XS�V� ~�e�П2u��"�)6�2��L�
�`_���3��[F�"�8��;stB	���;�s}
D� ��`-B�SA+c���q�Hɜ�"������L�),9�Y�ACQ*�u�6��zC�n�̍
4L"���?�8��6�Q��i�N�o�:�A� �W��Ψ��=�?o���:m��^I��>_��4��1���(!,��d�&�DQ����������sBjJ�bh;�a�]��+�^��e��1���.z=��y;�s'���睋�P�9d|������N�Ͼ:�p�C�3�s���:f�7�̑��__/�V�?4ϻ���u�8�ҙ^����=�;��?�����)~��݋��s�\]��f�	3�6���Ք�n[b �]W���(ۻΰuqk�N
TW`]��Mi}S�1��"�;o�=nB�:T��^�s�G�f�߿苩�ʻ+�ɖ�z���0u�S̰�!��t�i�z�S�ް��5�rz8�O�j]��ڠ3.���:Ʃ�%dz�r3�a)ۊn�ǵ���9��3�,�"�&>�>e	�KcC�'G	&d�������0��י�����N���uD�B �(�&"�l"B�Bm�\'�����W��fO�Da��|��ƍ�:�,�b�MQ�S�����t?wN�ZM�1��kN&��g9��v��r3��3 ��qc"������c��<�g��WR� �L{��o%��������E�9R��K����*��(p�j@^���d�BF�:��~UZ5*��b�#�o1)��:N����W�pYf�眈�>J�	R� ��C��ՆXM'B�5R�)	��\�
�K+���ʵi ��d�|IK<�
(k�P/'_���U.B��޶�9uL�
ٖ�ijp��蔰�H�4�Ԧ/ ����^��U/�d ��h�Oc̩U+�>������ )��s/�P��Ա`�Q�tE'�1�8��`ٿ�OʮO��������c��GA4��D���P�%t׶��ܛ93sq�y�����ٺ���eY��L�x��q�kHz��옯dN��
K���L�Y���Ӳ�j.0�iв��>9�>diV�0E����FB�G����:xqC����uO����V.|;=i]	�B#����<x�h�̹% в9W�ϝ�aGt�S-Х��M�cM�C)^$�l���6#f���L�;��� �6+���"�i���OZ^�t�Ő��&s)��$�Qq�aڐ�iT
��?.E&�P@}�N�'�����Hz6lP�<n��vo�(��.�\�׷�<��I��>#-r}N�T�ǩ]i��@mX�[��L����q�г��
�D�,�����D���Ɠ/�Mä@�^\�(X๎\1� ��A�9����t �n]��ަ]Y���s�̦�+�	^`9�3if00A��+$�x{�jC�uqZ��¥��a6�t�!	Ip�B��9���4/.W��������M��ɵ͌/�P#���ԁ��Mv6cZ3` D�,���O���Y.��SsØ�O+����nd���
>���hyK�m�� �t}R��hU�
�Rvv�n��F�Q�� �� �
8nw��n�(`g<�
��bJ1��;Z���qcG+��z�{;�_lߡ��b����W"�=�ZUH�X2v���E��Ў)k<�d��u�[q�klb�e4�Dny�e���n�TЛ45@������5f�A^����]�� �+�lkl�|�t4C�x+uW�-d�չ�@N��z��#c�	Co���Y	�=���7	��1PbɁ&y���#̍M�иRY�`�1�r�j9�:'�ik�g�s=������w��if}"�,�%f���q1�0T$EL �8�����f >�J�?@
�95!�D�Q���������(�P��"�K�,��k/2_~�j��	[��Ӑ���$�E��/�!V����
a�%�����zNHhűp�,�����a���|�L�wpLaN���
,�ʴvbA	�z�_kL�/���c����Ӣ�v���'w<�,����_�	Y3�C�)��eRf�~��
oxr� �0���]TO�+�SȚ��F�d��6 �@l؆�Lu4�`̍�E�5+""���[{4����O��xF�Ȍ�G
޸?�6��/鑟��yN-Ǩ�1?���洬��X`����j
��јLm�۝����s� ���g��/{�����2�<��#j�[F�ZF&��D-�e̟�i���K<5��et�m��0����K���s֭��<q���2�R"}p�B.#�Df�)��h�r�+e���xX
 G@ǡg��t'���D�ȷ��WC,~A-';���%O���D��!�Z�X�]�
~l��0�ʤ�Z%`VY}�U���6���w_5&X4*��֫�<VtH0e�4f��/Ae��UE/�O� ��X�e�;����Qɜva�܏/��'��[(G������"}OP�Kx7^0��'U�t�p�
�+�=�w���.{�HYiMA�7�ȇ:���#X���)�U��4�e-f)'�qL(�)KvjvUx�S �*B-")�}������?k��;Q�Iƍ�=P�^���:�8��Z�<k4��0��:`E4;�O5�;)Yʕ��I��b:� ʹ-���x[�����nmHײ��D���Y��!?��'�F:Z�=�h�-cڰ���]����T�7	3�jz��O�A��u%�(�����xb���@D<W�N��q��5_	�5���T!i$O#�X\}R�T���^SR�OAvr�k��m�����q�e��D�Y�g+��
ٕ�rg|��-�ϝ���6�E�\�h��~,�F���O���%�e̟9Qˀ�dc��(�Ϲ��IN�7��е���	�D�2�Im����\x��T����3w���"m?�6�/��ꡡ5H�%׉�l��TI+��2y�!�yH�Q\\ha%&�t���ןX�&U�
����=��lEN�)�e[a*�@6̿UZ�P8X������d�,�d��4ٗ����lo�}�Qo��H	�&�F���
��[�c@x4�8�paE���G(r��O�2
5?:�y4�G�����=|�r�y����П������Օ�&����r��}x7�zng�������ٻ\<�r~tu�^}��o]�w������l��t��Em�����>_/>=_ԛ��������\�ׇ������m�M�����9�~�����f��:�χ��ۃ��~�-��~~��p����UR;�O��F��֛��/w����y�yԾ�;<��ܼ;u��w�As��S�K��5?^�?̎�/���ї�ͫ�����I�dtԊ0-��ߣ��d�	�CN��Dա�
i"�8q(78v;�G���V
�>PF+��O���$�2�;�k�d ��ȝ��{�
P*~�֚S��&H1�W��x
#�E��Y�X�_�q�CP��*��N/ʹɵ	�}�Vչ���2��z��?�W� b�N息���S "��bH�eMu吰��6������fa��]�v(�jx���F���]^�oFݳ�9쏆��7�y�]�e�N;����E
�Q��B���J��>}HpA��q�<a�Jz�T��n�o��+i/ғ�~A0EX3�ry=<��]6��J$���d>�)H�T�5�r\ɞ�+�{��C&�9�$�6��$�2.�Uvm�*F�lPʏ?�4ط�J����nE�b�X��H�j:�N�۽E�h��f����C7�8=qg���`�b,������D�c��q�!}ni �sxp|��P�� Ď�j�'�q:�+�V�������C�LX��y1�|�J�;#Q�a:6��a��kf�*�j��R���"]=��� ���X���Y�3�7{*����U%�t[�u���,N��<��N��e� �#��&  