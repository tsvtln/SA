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
  if ( [ \( -f $CUR_PY_BIN \) -o \( $(($IDX+1)) -eq $NUM_PY_PROFS \) ] ) then
    eval CUR_PY_ENV=\$PY_ENV${IDX}
    exec env ${CUR_PY_ENV} "$CUR_PY_BIN" -c 'import zlib,base64;eval(compile(zlib.decompress(base64.decodestring("eJxVjkEKwjAQRfc9hWSVQAwWiitzAHfuSykxGSU0NiETRT29k2JBd/Pmz3+Mv6WYywZfKCPKd/BniSXfbZH25O0UoBkvs6ZYmXx99O1AHHREhcUUTpno93WnY4J5YQKFABNB2HaE6YxjAJIsXnWfk7ETZ4cjk3SawTjeCdHvhv/mdi1WxWt03hb9/UmFaBzy+q1yYOMtZUDkq43qQogGHibwGvoAfFX0jIZah9yyQf6SZPAEy6j5AW6DXz0=")),"py_loader0","exec"))' "$0" "$@"
  fi
  IDX=$(($IDX+1))
done

# We should not get here, but if we do, go ahead and exit.
exit 1
x��Vko�Hm�ծ��_����Q\�J�`K$ChH�$$����16���<�U��ޱq�d��J���s���⵨�����-~���Q�
v�04���ҋ������W��a�hL93�]��SǞ�L��:�A@B��Q}_$wa�O��2t�EA-�/�>��k�B�#��8�D"r�'B"��U}Be��q��id��H^�vDD^�xJj�E� �m��O[ذ)���޶t�dY� M�l�H,B�ėA���82/�/.��\r<��wH����l�m�����nَ���Y����e���?S�b��A����_o�)�`)�T�;�>w���Zؑ��Bۛr�T{�P�XM�ڤr����l޺\ϔ�;S�Z���[eݷ��Ai��n<ߜu�µ����J�y�a�;�C��jU���мlv.�|ó���d�.}�)�~c�������T�7E�ݾkY���ϯ����������Ҹn�ڸUlf��9�����c�7<�g�r�{3�4�+k�w
�����BٚT��7�E1�\EC�t�8./n��Y۞��V�b~�/�·ت��Y�;J+��>(����C�.<aFg�l�M��`J*��vD�w�!"S�aېP*�6�� )�"�����b�O6D��ޡ��qQ��,cj]3! ��~���qH���[+�x��5-��Q�#J�1Y�b0IH޳��X���D.���oSG�%C���*0�D�MP� ;��K�/�
�/#<qȨV*�Q�)�	@���=a�@0S����b�Ea ��4�LSK��<%�� s��:���g.rH�!﹊��L�[١���ڜ�"�h
��˩ֻS{�ӆv���7�f�ռl�BY�{d�:�7�1k�� N�D����r^��Y���cvB�$�����13n�fT�z���kTڃ�M�`��/YJHb�e*<�J���CI��NR�eI��)+q�x��:xN�8��ŵq���Т�"F	�Ǖ�{8�eN˞_���a��	y��
b&}���!�O�K$�V`��ͣ�BR����¬bɈeģ�.�v��0���!�`
Y�{dͰ,���.1a�Nt�iX%`�_1�P�
4����Hb�J�n�4�̹���,���84�0IsƂ?r.� ���Zf�~wK�A�PڅmEO���l�Bfv��0%��4�ޔ��_���%܇s�v_���oԷ�|���;ѯK�o�DF�  