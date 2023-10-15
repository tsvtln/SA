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
x��V�n�H�='�_��^�lǜÊ���'�$$�!����ml���f5o���6gf��J)Vw_U}Ue�e�������Mǈg�����l�F�[�X���~��v�0�b&�ҡ�D��]lr��$Z�H�s;=�9Ίogf��t�#"g�h���?�l��f0��e��D���{xJ�uE�k9�eO� ��xVA#-�
����<�ƋAq����V����8n�ո0�� �$*�~����ݻM�� �Q
�d�c�����+�]g$�8r�1Ǎ�BAg����Z�r��<�6����2jv���IYv'^+�5o'��u[+<8��s�T��n�f��˧��j��,��]�ug���~�F}�����V�=�eU�=U}nچ�uB?���~�r���tw���%7���D���/~ך����+�dZn�egB���y�t��U7.��Q-�yW��NNgŤ�x����R�=�k�-��b]�&7}lג�ɪ��-��T'�n��e]�^1c0B6Ԧ��0%�ʟd�]ZB�D��M®�T�lR�I2�E���I���x�"H������yl�#P�CB|>��f��4t���J+��~G
�S��-	�	1�$"g,.2�]<���<��ذe��V[A4$�c�*K����b:�o�K��]��q)ف�#웈C�/�r�c��r��+�1��: �I��	�9��
B��"��+���,�N����>%�ȷzz]��t�w���zY��뛆�P����%���9t�:�7�!�� N>YŬ�P7������g�!�P(	Y
��o�̌۰�MTh�:��CK�K*�A�&t�Aķ,%$�	�2v���p�Rr�)�A����xP��G7�� ��
����0���hQl��ط�	|%2�o?&�1�a���C�3��ι�����="!v3��#��>�(��I;�n;��������mvA3_*3
��"|�,Y.�
�ϥ&��LA[
���k ���]g���زl�(�#sv|}q��VZA���=c�;�e@�;ֶ60�Ǹ�� ��j��j7���
���
���!�fS�����`t�}��t��*`����^;��g'�����\����Lx  