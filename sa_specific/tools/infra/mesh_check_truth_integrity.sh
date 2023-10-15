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
x��Wyo���v��,?B���" �0�d;.�Bt�r�Ĳ%E�U��C�/qF�s���=�썳-P��x�o~������+���b�����w�a���J8�6�]�,�2��O?���Q"��Q�
fO�$�6Q��f:�g��'��RM"$�0{���6{t#-�b0��@�~�\F�Bj�(��с�quR*�@��jI��8��<wZ��lbE,�L�r��L���Է�?��gfs�<�*�����'���I�Љއ�(#$�4bf�\HoSA[x��\.Ԙq��/
T��RS���玢�a ��&�n���W��.�,^˖�#�&F@}&O��)��gJt�l+��'�Re!k$��y��q�
��[��f,d0�'�lcx���4R=�O-JffM��cō����(���\(����ۭs`��TK8���mhhl�&A�XH�x"I@��8��U��M��sF�fjFh�M0�� �t��5�A� �z?]TeG����e��U+��t��%��(B^?��~8Q��:|40=���4�H�e}O+R��.�c}G���׼T#=�a�JRZH�n�<o ��@&��XE+�(=�f{+Ϲ�h*�	P0�
�j黸�a��{���d"�F�@v�Cd�P�LԿ� �|��~�E#`��󹖂K�Mǜ�	L�E�LcQ`Ma�T����C7@�����WBw9"QKOZ��,�CIbg/tBX-����B���|��pN��鼾G�?�X]�LeL��O|(E�������__~�5k��`��\+|�4���G(
{Q0�����P1�b�=�����o?���ͼqsk�gΨ������xlt�U?Yl/���'�3��-��7�r�<~�q}:�O6�U�we���ۿ��ݣwוa�\���ý�=;��6��ێc��(ώG����w�7W���Q�vN����K~����;��s�8���`�ZVw�˾�VGۑ�;ӳ��?����Ͳ��_��byr��	g]w��X�
���2�|��Y��ا��^�����5F���J]yƌ���Ԧ�M)g�'�`k�f�G1��-�S�)W3�t�b�����{۲&�-3aU�!�I�J�)l�� ��a$�y[OY9��nfʒ�I����p�$����1W�&@��Z1�h�U0s���>������7��2ӵa+H�\zi_0ho%��c���1���� 1J�Bo��E��/�zD���;\}~��f��e� T�u��~���m��@U
B��X�v�0�ʍKT�wo4�����v8趛����e�hu;��N��^u�G*�{��J\��iz{)/p�����mu�'T���s{��7(&�l@����{���t�� p�	��/IjD��e��FG
vҢ��_��N��zp<���̔�&h=��	p�5���� ����R"��uÀƉ.�#���bQ��
�PиMW�O��J[0�w/�R�x��]��b��Ċ��ݛ�ko�L��O�Q����
bY�P���ੳ
>.v00�_1��n����H�be�tH�G�|�Fa�	��p�w-�@����:,�9w�2��+��nN�0���75Η����X�3�7X�N�<��ԥ"_0mRG�;<�����$s/䟇������c��J�����  