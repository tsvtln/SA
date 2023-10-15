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
x��Vo�H����+�T���Wʉ��d	Iڄ;�{�
~�5���~�~��]uw�!�wg�����Y_�$�o\l{���W*G1�L��X�������-~����`�7����ѻ�%?��k����JAY����g��F�Ɣ�G
pdI8�g��_;�����0�6� �Dr�'0NWE��P�C(m/B��)9E�)���$��K���Y'D���R@�Q�?*������	�"�Q5sCg;�ʘ��d��0���c��(�d,��0V$�6�%c��pm��b�4�I;������lR��R��J���� ��OI���.��
x��TE^n)W�m~\��	:����u{S��na�
����
�"���[�:��KǉQ
�r��釈�b9�|��X�y��d�b��[XY�V�x}t����OE�k�s��.���jF��r�T�"�5V��gmR?�yr�y���7�|�`�
��{���}ێ�厹����eO-��m�A�6���Q�ϵ�V�� ^͛V��(5=��dN���ǻ��7�+ZܧM�qW�;������x~���'��7r�Y��v}����W��������D��k=�Vf�etV֪�v���G�5i�T�7���J<��
���⤶����{��\��y�T�]
�Ո�{��v�v\�}�������B�	�I��7���O>�v�w�![��^CH���$3I
�i�X;�X ��,��A>�J�edX�5���A/�4��J�ǽC-��sVL�MaM�G��fBr��"cI��'r�Ԇ��8�-	p�N�'#�6a)%�ؾ�b�l��@�e�'�Vkct�����-~~�⠳@?^��LSKȀ�[K
E������"��ɞ����D����dAK��X(tZS��z�)��9oj��˫���[7�sHK�5w��r�b����M�
�fs?ЂY���Ǖ1�!_�S
/���>03.S3'�wJ��++��Jk�	��G�"ⳋe;���q(9���TwQ� ~��J�����7�X��:
v��)�\�ۯ��"� 8J�]���qK��������ᨐO�2���9��x����Atǟ`G��Y9�N���d����
b뻃��>���T8TL�"+|���e����	�u�@G�
���+���DMc���!��a%X�PG��O-� �i�����Bc6p��Vs	&`�[�r(�C�Lă4����eS/��`2���7�LF�P��������ܧsv��}-�,�?E�_  