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
x��W�r�H�=f�W��j5�@
�e�no�:lڸ�v���6M(
���I���=~�y��ԁ��=��B����/�2K��h�7#�k:㿶�冾�baQ)��1ǒ�Em;�r���ۖυ��7�Q���?Z����|��$b!"d̃�A�"bBq�pD�p��>ɥ"�bE,V|!��5��;鳦+
w�F|h`ݤ�`��WI����GSH'�Hss�4�-�UȖ �/ RZ������y�	T=�ds.���	��~��S/�~���@������"��"��q�.�VӘ�3�o�S
�rGd���5s����P����e���!T+4x_�`߯��&�A3˦�UK�H4��-��É�E���7�(����Ֆ��󐈉푬����	I"[9����V���x�����#��|�Ņ�V�� D�@�J����Ă�6,i�A�L�7	$%��izTXC��P6'�
���4���%�¡�����	d�9�Klj�=" �;��UW"Q{��xY��֓HH��$�Ҁe� �u���=r�<���JA��g<�1\��>ZX�YU����9;9?UW�y��͈x:y���d+#?+�ː7s��� aF"�^3�^�,D�%q�I(8���b����Չ�B���1H^��t�q���\$��6S�6z�o���]�H��=%��'���R+�^���������!�A�[�@�aO_v97��h�xh�� �䅞��4���Sմ��z�{��I|m6�Ժ ЉC�S�2��|Q���v��/*Ѷ�e���N�A*���C%՟�u���tsS��%c/�$0�Rï�����k�h2��aDN٢��9	$��I$
�^�K	�$e���m%ZX~HWi���Y���h�°/�=��1���o<�87����P���0x���{P�q����q:��]^���׹���6�p.jMwr�Ώ���s�h]����Ǻ�s1z���4���.fw���ũ�S���ۿk��}.���p*��nG7�ϥZ�y���v���n'��������C�~^/7ic�v~_�x"n��;�O�u�g�w��u���ԛ�^��;����vڣ�������?ɻ��p��;��MޟOÚ��xrG�����ݿ���5���j�����b���	ɨM�������/�R_��Q�B�
�a�
�Dh�L�Ⱄp����m�PٰٜZ�B{9x�'�s��m[.��*��0��3��;X�;��	R���L=f��1���#��+1{�~�3a���	Ma�់��g��yq]���l��V
�`\��^�A�쉤}�u+���u�}�-�¡��Cҳ
3�pORh�#�Q4��`+��Zr�#>*f̨��j����<��%@����퓳#�u�n5��֧��ɡu�l�6� -�<{R���
�B� J�KLh?�'^ᢐ�W�q�����B>R��m�����-\ܶ���/j�fAe�$f�Wm��&i�B��Z��S����iv�����$N����A�ko��6h������W@f)����1G��g��X�p0��8����Ko
h��4�e�Q|1��}�[������<W���[�R��\v�q
��B[�D"�|�f�e�J��r�����`��{1��i%dX0A%Q���q��Ih�mN
Bv!%1��e_�$�
#�`M���� �8�Q&��`��n*?�|�"��0r��̢��1X�N�)�����T��X�V����>�P���&Z��k����g�  