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
x��XS�H�{nJWw�a�����,? ��[re�Ą$l���R���-,����F��߯[[Nථ�e��t�|�uO�_�~c��h��Y���v�g1��f�bR��n�L
��W��������c�/��`GB�H+���hF�h#�O�L���	�U�d�$��LD\�{e��(V�K*X�I��������X�f��ص�g!�+<�n��e�b��{��K|д%M ����Ă	�2Q*��Z���Ѯ�o�ը7~��t'����^٨]~0`�{�1MM�O�$��-�����z,,�����DhZ���� �M�xa��=� � +ѰqCN�:�-�Z��0�M��PI*/�+{)�]���YK����.�ٍ�;�q7y}"���-\'�?�����հ��ض}s󴝪�j�#/����~c�kYp�>P s� ��_4P�0Z�.J�a��ȀAU����UW�w�S�bsa��Q�7�G�x��G��[
�@a�>a�k�݃�E66н�H�:6n	x~xp��
sX	�
8l~�KW��!��̷ᠸr���v'̝fc:
�@%�j)�2���1�f��s��=Wь*�H�9\�@U�>�.�Hn$X��)���:�Lp:c�ſ���y���������x4�aR�Q�U`1��qV�c*�L���DO�J�5L7��S���\7@p7t�<�}.%_4J�G�1i3D8�`m�6�1�פ�Z���p@���BR���H��W2��I1^�G֧9m!�����a�s4Z�Y��b���k3�f 3�dl�[rJ���ȣ$h��*K*�-c`��ۀ�g����+�ifٽ�bE>�p�:BD�"lɷU�s~�"�F��p$ˌ�L8�Ǡ���,�R ��d٧ʝ<�(/<(ҋ�ei� ������Y�)S0�K^���h��m��P/��J��
�r 8�a�</~��YIK)vu��l�s������rM��k����$�_˴�S)2�1�0`�{��V�V3O��"��ga�p�\��T)a�^�:ٖ��eYX�n~���4�|�jz~�i�tמ�ʓ�͞�Upyڤ�mi?�e!UP���;-�1d3\4YR�F��)���X�� �t'������Ȁ�*�^ğ��y���`�'a)vSv�m��G�@T�P��R����?��Ը���#�ij�aM/�1#��#R���Ⴡ��=���&6���8N�N�gC�H�|l7�,:r|�.I��Y-��)6p�
9���	#�1Ѹ��������%[�Y�NCfͨ�Z�k�]����B��|���v��
{{��v�9Y޶?�������c{y����dz��7�:��~sw�|����f[/�/v.���rpv���yл�G����� ڟ.������~w����v�;w0��<�ݺ�W�o_]}<9j��ovig������X^��c����N�ztٿe^w1Y�f^и��P���h�6������]#�:}���ӻ����M7-�,��tY�=����$������ڝd��U�b���W�
ɡM�Q�v���44�%%�^��	�c�L�F��J�k)��-�iZ��6��H�Vਟ8MSb�&��ݴ_�ڿ������Z����d��P��1l��pmH��_��>�V��7�3��l�ct�zmh0��0�Hp_v�.���t�a�����1� �8Q�hM�G�̆ď��`VH%��wj��V�3ln�4@(A����%Y%�.-M3<1��:�'T:S��ٕ�?8~w�����������9�vN:��D_/����*�
,��^၎������Ux���j�6핟^����YZ9��wO?����
�|�����&�uq\��ըY�ҵn���N�k/��(�`a��g���S��ª����s&���5aR��wPZ�Hl�)�l����jȅ�Mv��q�]
�8�sYG���hDC�˽z���	��ŉ�)V��ڵ�<��Z��JciP�wJ >gK�e����5���&䰘����m'��q? �&+��$�ck�9��
���~ԁ<C�+�mHc�Z�dߴ���q�h�M
s�WǍf�X�}<J��-��ik_��*`�Ά���:�����'<!�t  