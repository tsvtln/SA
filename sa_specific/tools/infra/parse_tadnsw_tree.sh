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
x��X�n���d��Y��7�e`��i�𱱲@�-�=��cdY�lJ�$�b�.'��y�T5�+�vw��UWuɿ���tޱ�ԧ����+��}#`T�岕�J�k���w�93�8a�2,L�rgF%��d0j�%r�y6�8��n�r��-i�i5:�r5���r����Δj���`"���T!�^03x	�X굫B����^4B��TgI�}�מ���qyDˣ�P�{�&�����i�8�x"�ٖ�z���z>��X���z���P��ɑ�@�x��\���QW�ʵb��8 �zJ|t��VL8%w����'h9���V18��Vo�k�h����:4�ٶ��b�k}�nH�f�S��J׍F��Y�o��T��j��h�`�����=�tˏ(g��hw.�_�q���U�~������vݱP�C�<\��#��˪D>��PVN.��IT�lrѾfc.�ͻ�5�z_s�@��{������#�ɕ��dQ���cse�.�v xN��,-:����%A(?c#���F���s�Ptl�qq=N�C��#G��^㖷��*p8UXz�jOl��%�vA-IԵ���N�%��J(�r���j�mI�RWAv��'Y��\:PP^�Sp�&�=AH����~��@��Kߒ~J32D���$	@��� �r�#Z G��V�����=�C@�7��2`��6;�Ѣk�+9�	�x>�v�����sL�	[�$[c�N�<���8�;R�
��
���ap<؄	�
��bk5,p�<q�H�q�������*B\���mc!x=���$a�f�
���*Oc��K�-\�0'�|��uD4L�y�g�H��@:�>]Y*9
Ґ�(1f�TM�a��L��Ğ#���ن��I�[�^�I�N���1���7\����}�`+h�d�0��դM'���k`mR��z�^��� طt3�x�\N�`��AI����7:��ѧ�a� 7��=�qo���1�|p�ɔ�3���T}�:C�jo�'�:[�W}x�sD�~Xz�ToW/�Ǧm^���O��U�q�k�f/Z�������;�v�����?�����������۬����í�)�N��>���l�+M���7{Z_^6r�Z�Y��N�w��Ӯ�;�p�{��.��K��Q��_�����ړ_���3�er�2V�Z�j��23��\w������2ә]����<��5>��Ne2?;�?z���3\�,��}��}�?����Ѿh=?�����b������J c" ��!L�g��Kc���̇�� C�(nʘ��EC��2��*om˪L��j
j���$(U>���6u,$�J����VF@3�w�L$��N�����p�@��.��ĥ0%�'�X��M23F�v���X;J�U$̧�c+�๴tؿþK�7�S�/�O�=؋q!�>��s����1�7��6�L9<iECIȀ6�\*i�K��?S	[�َ��o/x���	<WL�Ѝ"?��R�~W�Y�ӮUJ���M���k��m�i	�x����� /K.J.��P87Ҿ�E*~u0<�
���|*�#��vw�(&EhƁ�z�Z���خ�a��;��Säʗ$U��7p�Y*Y�S��Ot��zN����s<���v���+t�-g��p	S�D�{�&��WJ�
X���rL��,�f��g)���
����S�eW�툗���+n
�nl�����M��G��S����KW�"2(��p��s�֏9�X��X���]$�q]�TK��U"`D�U�!ڐ��0�(mj�c�
df8����>� �6|�DxH1�$Q�Tba��t�ĩQc��L���1X���Y1�0v ����ˇ>�Q`9%���!��u�š�z���B�?��x  