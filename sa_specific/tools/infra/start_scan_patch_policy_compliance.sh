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
x��V�o�Fn�mw�b�je�8�H���Y	��&$�`�5�c<��p8R����!��0s���o�5���[�����7��Z~ח�7��}#��t�0p�f��.žI���oXd.e|��d�����~��^}�
�� ��L�bƴ0�0%I�ъ�Qg2:�V���&����[���+�+F"{d�~�֦A��{4Ά��H�����/$	G3��{0\��g��9�檛�E �KZ�͇��G�$�x v�D�7Ad��Y����ơ.A*r��
�z�J(2W�K�P�l�:�A~�y��㕜j ��P	�g<2��ٿ��vgH�e$5�1�q�R3h�W�D0�$
�N�>�O��\-�
��'_`�&���n2����0�!?���R�Ȭ�C|NM�%��! ʎo��!����)"�2,�| ���&"����Pu�7�0���NF�VA��`*4@(^�&v]U�bWLኩ
�&�5��B*�#
���AsW 1��L ����E�Gjƣ �����06� [$*/����	�Z�4�CͅK4G�����ҩƨ?�����P2DϞ�i��������u����l���������޶W�x����K���{�Uj��u�*v����O��`oF�M�sc>�>��Q�����5�����V�+��퇖c����j'xz�nx�޸mTڸUn���+���ů���Ԝ/N�xӛ���^;�g��`;�gZ+����-�����/�ӓ�}0�l���r������;�8����Q�ފ��w�A���t����)��6��3R=�������խ�
�"b(�T&Y�H�pM�P��mY�ɖ���@��(�
��¶iآ�@C������_̤t��%��t��@<@��P6��Xb%"�Y+"��4�(f��y"cu���;�:b!1�
[)A$ΥgE�V?1WO]2>��L��u�q
�R� �J�
�w�#��	��IB4���ff$���Ы���G[��3UUt@"��F��;��rgh4�W/��C�׾h��WM��n5oZ���U���2�RV@�'[.
�k_�7�><.O�	�����C{�gGBLʼ�U:�^��S�A*�A�M�b��_�ԐƐ�Lٍ*��U�?�T�(	H��`�>;�ȃ�rl��a�N��o�������APJH�Ot�ȟ*�U����r�(g/aV��T��#F �n0Ů��R�$v��<VIq�a��7�U=�ॺL=�1�E��>�.�̐�O�zq�t����W���3<B9�/Z��%<4��Ml�P5�*xBa�'�L�頔4��id�����p�D	�H�]`�g����qc5��FV̀���d��z	tB�R�/�}/1�,D�!��%��O+�O?��  