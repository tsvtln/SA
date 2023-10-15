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
x��V	o�H�����a�Y�*��+�"[*BB��!� B�`��/<�aV���sf��VZh��;���a�=S�>�����G�7}nS���1i���z�GŁEf?/Xl�6����/�_���kg����1G,a*�>�`�E���"؊�#?&|�ģ#&g����A
�H�E�Y�{�P�\B(�i��l0<&��%C��eR�=z7g$6y8%�{�D;�A~vbGV�+���ġ��8�\aF��"|IǖE�8F�c�6&�#�m/�E.��:R�B񭖇op��8��S6�{tš�l"\d��#sr��T�`�U�YIb�%�b�ą���_�O�K5d�բ��#��c�bO]CT��X����C����Q�n�!7�ϓi�v9����v۟��e�R�֛μ�LWWm#��6:�beZ��ٹ��.���(w{ɲ���[�v����3�7�o��FX�.X���W��]Ao6�e�(+�n�;�yӻ���k�j�&n�{��~s���3}���Ϭɴ���΄����]�|���.ϗ�Q%g����N^�
I��#���Yiv���t��Z��s���\��[I�{����FR��ѻ��u��y%�R��OL��O���bAv�Gq��Dlc�%��Hl���/����|�-�2Y�(ׯ�C�x<�=�c�t  :m,� ���@K��?P�%��1��%A!���䵈��9�#K��1��|�-W?J�����E8J"q/m۩igk���#��bi��O1� b�p7d�AG�'�hLƙ���Y��jBD���f �0<�i����ّ��\D"���a����S�(r�g֌�f���4/j�G��n֛��m�ҒN����{&CQ,�d�EB��B�.��q��07�3)����w����es4��u�w�Zz����n"�����2���W�L�����;H�e$L9X(G�S��d�ym��i�����<fE��S�]����x��0�q�I��A����;�<�$�8�:�N~f�}�"�5��#��Q|���^��ئ�vbo{p��})Lm�r�4�DQ�Y
,�#a�ݨ�[�l�;���� B��P`��? =�@�hV�-�q4i�R�qq���8t�x�L8�s�� �gm��~�wK�I@Q=�lEO�-�l�Bd1�@���gAmjҮ^D���tx�$��3�OH�s�oo�'x�  