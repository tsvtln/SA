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
x��Vko�Hm�ծ?�O����Q]�J�`K% 4$ip	P��16��gx8����c� i��J�4s�gνw�/˧���F�n:[��e����iꡋ�D]�����'�C4��2���LQ&�0$��ר~(R{��ky�u�f,����ҩZ��b�X(��9Ap,$#��2$Rq4[��TF���xn�23X1u9�ȢF����� l�|��d�aW|�Ƈ��[������hd�0�ioz�u\����P\�M���m����)(L���%;f=�� �v\��׳@9��\_%pa�3Մ0�� �$*.����u�J@���(���]���P9�Lf�C����:�ק�8�D.�����f޸����=�}�il���kՋ��V�����RuQ�l���w_~�a]��Ⱥju��|�wzw�t�)��.hAs����л�V���F�s۶
M�~P-�������ջF�c�����p;o\^�;`-N��щ1_�{xӟ���Y��g:��v�
e{Z�k�;ܼ�_.����ig��Iyy��;�ts�ֻ���b��j�X�ި�hǕ��Ơrvw_�K��18!;j�����ɟd�]���q���I�6"�ʩM"1IJ�,��b.���آ"�-1@*��;���mNAm�d@b>|�G$�{,��R�J�?P�&�� QBLʆ ��K"��E���'��́o�z��
q�N�׀%�c�*����\:��pc���%�Z�<A��� 1���"¾�`��/�j���g�2*?>i����PuF�� �s��:
B��\Ԉ`S>9p����L�_;Q�6���Ĳ��M����޿�������q~��[�v�}eI������\&�Y�8�d�xA���&}�n�-_'��RIJ!<�w�{�̈́�P�;�w�?v���A�=���b�{�
��z�J���/@�RR�����Y�$A��Z>8���G;�^�:��qm��������(!�d9���X��
�<_��L(m+�s�L>��=� �3��S��>���$|fKF,� |��v�����/���S���'�e���s�	?u���L�+������P��? =�@V�
�yT�Î�g!�8�4�!<pI�3��sp��2h��;�� ��>�x'zTnf�2��
�)��G�!��*d�r�Ã�Ox�(����$X>Ӟg���o�.�u��#4��  