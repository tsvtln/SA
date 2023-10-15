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
x���s����^{)��?�S&��Sd��;�p3�q�y:α	��
���]��s�{�ow��v�v�� ���~��ş�ѳ�%�<�}ϗ,^�e�3��#O,��c�W������ﾋ�Y��nyi���`Q2��|�%wg�ltj�m.�t)�5�5
��v���d��'����D��x�kF^��Nq!�yŨ��G^y�	'sE� �{"��4I�'�*d\t?_XゔD���~ݢ�+�_�mۓ�W$�P��t	"BJfъ&dt�� Y\ �A҄�ty�@�	1�B�a�sv.�-�K|�eqD}I$ <L��O�@�0wMPc�2�mF9�rPMm�1���KO ����;M$�O��<��2�̷R�PӺ _
��
i�A�q���Hp[W���z�|�N3�\A	�!�4��ٚDY'c��FNF�(�(���;�bک� �-�m��{��f�m�G{���������£b=5C��2d��K��F���݄���f(����ж�B��$HYnd��~���9�)n�R*��H"�G2�,Hm���+IKC������Y�l'����et�۰L�;<��es��4\�!�|-���jVs �s@�=VH�vD_	CD4����D	����ŉ�1�0��i��izM�S�M@��)�L���e����Hs@&�?^rv:$5ED/D0p$�_a"
I���S��f�1C3�1.�.UQ������:丌�1w�����9�w�����hiح�=�Քa�3�
[�Zgg�����ӂЪՠ����A(���IC�AL��P%2s���S�:���j�w�%�IM��l�I�2ks�-4��!q��>�� �c44�ĳ�,��o�.�i}	9nM
�dT,Y��+���~Ʉ����DT)U���-�6a�̷tĿOJ��r[��kʐ*��؅,0r���P��Nrzy�]��5�p�E�K!���d+���	��D�Ρd��hJ�~��fhVSaF�V��<_�gS��4�}"��
5�TJ+�)�'��Gqpl����'�pF!�,N�n�JRi3U���UkB�8j��B�����$$��`cC�8�;�Ƥ�-�y�όi�\�t��ِ�e��m��<a�,vf���\c_�����"�lȧW��`��[F��e���|x��}�m%����T��	Ry�z�z��'HOa��
�Ң�y�LcN��������v�Ok�D�輅� !)�������T�/�����؝O}�D32��W�a�aLVNW� ��1� e��`��	���@��qY��/B!���N���D�ʀ�!O��й˅�?E�\D���HZe� F���$E&��`{�A���R�O�[�M(�B���}��L\H�Ƞ�l�`��KE��@�.|����}�n�&�7�/���zk�͒!ѕߖ�m7OĚ1HK�@ƪ|V�({�
�� �nU�K��S+�����
c�r���������}	���s"+.-��T��*	��Key�+I;���Z�nO�A@ٸ��-���m�Y����SoL��w��`dH�-i���+n�0�����?�(6O�?f��=��)��&@���&�;�7���[����S�#�<k0��j`���xTK ���.��_1���>�#([��4�9� m�2��ՙH�a$N��L�>]�dA�j(���-��隑�$]�>z�^rLi} E�}8� \�L<9K� �%J� b`O�ދ����b�iAM5�0�Gx�i�?��!���"d�r��`i9�҂_�{�:�ɐ�����K���ET��T�/�z����fV����=�Vx<E�շ&7�KN�hT�5˓�a<{5,� y��g���]5���#��Q���-+$����`?L�'��Q�2Y�.D��>�e�e�ų�~غx�G+�wyw1����Ѝ�/�Ɋ���SPh:x�3��L�@�:}}������m��e��W��?��WQ$����r���?������}x�~}��\̿���nupu�Y�o�/��;GI4�Lo����Qzt��7��O���Z�~��4�F�a����W������o~��?j��Ӄ�����s�)�
�~>��y�w�w=���~�v�~Ժ����pz�3���}���hm�?�7�������c:;�G���*��}jޞ߸��f�18�\�N7������O_�����DXצ��ë���R(�&Ե���
ۧ�
g[n*��SepӀ��Ѱ��6��=�`���+���[�П¶�X+��WK����(K�qH�;Y�(Ŕ\S�P�FJ!t_"_�/�eD�Y����m�c�/����% A��*��K��p�1wڻr2ޖq
"f�Ш����r[^_�	�n>ԴQ^�p�s���<���E�Խ
���8�d�F�;wtc������3�
�'Gλ����s�?=~sznQ�Z����2�`i�)�9:����WlQ/��m�lMP�z�(���o?!XM[3�~q=�x������0ף�� -R�6˼^<������Ȥ]r�LRe��YQ�"�7���v�x�����-��V�D�z��6v�ɯ�Ab$��c#_�î����0O}>�4f|0K����w��;҃�b�1�by�(pKr:���F�rs�� ��?�k�e�	!~9��
>�w����� ��#M�8h?0:s=}��z!Q|�Z���Ė
��!^L!�/ln�7K��0?♴JWq�
 h���z遻������}�wH�g�v-��J��J�Uq��V7 ���n����o�
�H�
  