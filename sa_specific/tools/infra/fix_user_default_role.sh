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
x��W�o�H�{����}��}^�lk<���(���	$d2�� C���nc�p�y�4��U�Hv�=�NQ�vUu=~�������M@��"{����om��%�����L"�-�4x���=.�,���&�c�o?����Q"�p�I��X����� �^�Jh�D���4i����YM�!�B��r�Z�X��_�^�T>ʚ$�i��uB�o\G!��!�CԌD<N�H䐌EG{�m�xY�RQZ%�`*מS?�
�~&�M"���m�! �$Jc� �$
��3ӳ�6��i��fL\�>�j¸H<K4���-Slb�ԕA�}g^�����1xL-d�t{C�
ԐߡfJ��V��|�ʾiR���Bu�F�E�9(���/�/��-�� JJCB	��zȿ��N �89T�k��b�W&�%�hf�.�'��B9�,�
f��'��	�4�;����`jS�սqu��:g���Y,<��J!2 �5v���o��X�*޳���Ճ����>���l���4yV	�h=yY
Բ�4&T�Ri��/���o/�=�R� T �2s��I��=	���$0т�Q�@w�ъ �B2�~�����D���i��i�u%��C'{� �]��'�j�T�ڙ�"Ti�q�P��K^�P!��,P��(��6Q
�xx�F�����r����:�28�X�\b��Um7l0y3��)��y���:����D	 ���5+�`P2֬�mY�j7�����m
62�,:�\���_�>�P$2���!N�`.P����"��@�!���IЁoL?�6K��7��O�τG=�������&ܥ��φ���$if�4TL|�fO������O믏����Ѹ�s�Sw��zk���'�����6��EoP�����~�t^�Դ�����ݗ��p�Y=8Wg�+���޽3}��>�TQs��'��~}zzS5:���k
�8�N�����Ӈ��չѼn�:�}2Z?�.�}8t����c�q~ԣ��#;�;KwYl�:\E�ȝ���9m>m�-�����0h��G��hv�񦫋ed8������n6��I�k�7'���I����P^ c! [h3�������%�U+
b�g*2J6�O@\�e2��r��(eM��nY�ٚY@U��|%�$�T��ؖ	S��Cr9���R뺼�*������e�[�3�=�b$d� %a��.�ӬWn�ğyVf@��@����hfy�r	�U�>��Ĩ/t�q�v4!��>N��x#�(�	
m��d�K1.\���՗�j(�KBpƛ���F�� Q��WW�Ir|pU���X���(,���s�Q���l.?���ݠ�i5�/���y�i�]�[��|�쯎���������&t��c�+X(ż{����#TjJ1���;�z�b���Q�;�wn��F���Sy
6�ˎ���N�x�̕ݩ�<�u�G#����H�c�T����ٗ�ނ[�;t ���.��z��n��B+e�EI2��|E6�	c� ʓ|F�����-�:���]?�R�y��_�w�"WYs�aw�P���k� n��\W_�+�zX��P�O�V!���%�;g�q��\����̒��c��dIDn��XfA4��%�"�o�����W$�	H�k(�w|���%G��v�ס���o�"5z!�<Өpk��db�,�-�%�(���QT�����l�wD��*!-�����A���  