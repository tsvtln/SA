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
x��:�r�F������b�K�LB/[)qC�Q[�cI�#�L�� 0$`� �E�)��u��  ����V]�Ee��<�{��=�z����c/J�q\�������O�8����oE�q$���]�٪�����o�y��`O���l}uu��z�Q��v�E�3�i�Y���Nƽ�M��K�^6g���a�����~�(M�O�u�G_�	;;�=j2�	<v>�X;����H�<Mc�b�yCΦ6��y4�9��Nc.X����(¨����Os�s`�%8g~:�$�-M������s?L�!�#'͆+@��+�/WַV�y�#�!�4�� E#J�9��4�W�=P���	�qlt�v�,Is.�t�7<�2q�n6��+�!����O�����D���E�x�
��Qߝ�b7�����Ԣ7��c� ��p&����f_�u�8NO�i��E���`��m�s�VA\��%ʯHߋF�s7��+���$%I��dg�O��A�E�I��L�E=u�g��z�9>O���'�����G�(���'���<`2���yf�x��5�'5��M�F`���s%Vͩ��cw�z�p�v�[�μl(Z�i�����!ڊ�p!�'�3��upG��pfY�sK�*ϲ*�X�%��6X<��Lt@�ْ��B�:s����ɞ	�������[>ғ
�$��3/K�{�>9<8|�O���f��8��X���P_�^���F*K�I�k�����$r/����.�Y3��v�.c��Q��0v�.O�	��AO^
U��L�}�\�/F�3C���'��"�f��n�n���ųq��3 \� ��5��l�N�4X6M��E8a�N�!R�>M�	�ρJ�;���;�q��r=�:�|�&�,��l�!9!4+4ed���yd���e0���zI �	'���@�s�]s\n�#�i@(,�呓�&�y� �ʓkv|y�tx�>�o���>T��'!֛�b%la�%�i�?
������ �+��� �)��?����	�ƫ!��᣶�
��5�9ʜ�$��������,� @�}`�)h���N��$ �X!V�@���t��B�-C�I6g�oA"%�6z�&n�dQ�&�Y��1���z�L��hP��֚����߯֟b珻��'�K��v�L$��K�#)�W	�X" \e��2�{�1,��*
Q�4��K�Ag(�i�YTh�����5dg�Ҙr�	�"�b
jJ@��v��$邚�� E8����!���R�t�yc�ޔ�H�%��#y`4���(@�,�[����"���K��4��~������7������-N�"�tD�_�$z�Uf��8��O}g2�
hx�:�mD�h�~��!��Z���'���KJ�/Cj����ګ�s�.`��8-�O��W�}�0�_��_ou�]����8��1?�t4�r��X����
6Si���t��^�=�s%��r�iQp�dFj
Z��L��p��s ����>8|���E����P
��/�[X���$������zU���(���"D�ʊ�y��u`r�`�	9`10��"��Xe�h�J�T�a?���]8�������3�3v?�V
"$�P�u�Sa
p\O�kY�ِ�aL��p��ĕlku�ʇ�?�Ư:�ﰮ���\ɺ6k�8n���Lb6��d
~��#J4pr�U� �
��2�O.~ef��䳚*��ȒU�����Z'����̒kh$�ZÂÄ��,&Wͺ��h
p����?&6���|��F �j��/�cU4�P�A2 �}�#;gX_gÔy!�T�x厁ߠg�Q&�㔲�J�,��?X#���:���*�^�Y\���[5��`�Z���D,K'<)�+�%E`�ϻXgt�ze��%Fu�S�M��Pb$"��u���:(��2�Ҷ��\��~i[�ŵ��eU�*i�$�
=��R<��[0gw6q�Eg�wx�R���%n���I_`�ߒp�i��������R:��'����7"�9�Z�&�!ni��ہWƂ�j�jC�W��I��.w���o��ڛtPM M�Z�!-�}Q	�A�%ԺI�^��Z��<�htcC+��J�nla�N6��Q?{���0T�ӾK=.8��
���P9W��pʣ���ς)�'������_$D�
���O�L@-
`J(�[��P�˄��\���2���O�'�g�>_#ra-��ƥr%������;k1��[[���[-t|�I%�N�	w��28�@�svr~����o�9�qw��v���\��[;�����V�M	��Q�X���=��阶���ZOX[�I��Uߞ�2CqSZ+3�Z�޷��j2�O�5��c���7��!I%����ꬳ�Vk��k�F{����6{�����/���c������h���%��&���u�:��7N!�t�Z-��Š��v�^
�5��0���O�&��"�af|��	����S�e�<�j�t���+-0���NN@�93w����4,%6�V�$�AD���2�B���P�@z��/:�=J�qM���:M��7��sK���/J�jT�W�: %gbJ�$�*���1�q�T�9B6�Fe�H�Aɳ[�J�l�x��`���h�j�j^��,�O#��sCVTx�ݧ�3��n�ŝ�FS�w�Td��n�k,6H��s��Y5������v�}�'Zk�"e�fc�W89�QR5.�1`�Xc�A��4�A�X�A��տ�Z��/%�4K
���E-rR2�>h����]�p�y�&1Շ�$$ZrP�J���;�e��i��,Y�A,\�C�N�	�M!B<Ŝ��W5X��_<�����f��h^6w`X`���\���.
��(�ѨuE���4g��'��Y���*�l=G��&�c9O$8�O�����[m:�1���!,wp���_YZ4�)\{�H�JvT¢��u4@U��QO?p�Rt����l������B�,v����m�=��j�V{���:�ۉ*����`��y*1�J����k�2rwzr�A����K3��y6/�c:���ɰ�]R�(pȘ���:?BՉdZ&�nd+��Ė�1�Thu.`���:({$d�~D9Dz"�-��9��s�|�f)=+���u����v��<TZ-$�ʩy�%s�s"���ڸ
�~���.�L�
�[�cl8�"4���ن�s����l�`w�a�B�u�A{��������U�v3CE@)�����|/���q� �?�H�ڇ�z�xQ,/=f��!p��aLk�KР�����xGx��y�=���wC�S@UС�"�����U�9��J�A!� 0
�'	�����
����/�`N������b�X���3�[�p��Ҿ�QH)i�vH��u;�֎���hG�P�������ej��U���_�^m��p%�[�CѴ�g��T*9��er�B�@)[�NWź���?o��|�ސl���u�F�S5,V�(����'�K���p�B���~�dUW��iQ����b߉S!��;t���?�!��D��6KU�r�R����?�Z��^���KE��%�n�a�4"�@�1w��Q�(- �A���2l����\�$��Т
���꯹wn��t����_���w�q��ۛ�>����>�?���������E�_�����|t���|�0�;;9[����V��_6���޼���>
���V������i����y�=���.�o�������'{�~~6Iҭ�����ۗ�޽non��{{��7��o���b0�~�����h�ԛ�}�;��ux�2�����|u#�o���_{�_�ϯ��G��O绣�W����?{s���?�~>��[���������|��������/��ڿ���`{���ݽ?�{��{��zt��ͻ����tޒ�  