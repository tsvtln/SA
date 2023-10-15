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
x��Y�R�F�M6��mվ@�Ȕ�[؆!����� a�P��Զ{�%��m�&O�/���nY6�M��T���O�s�\�n�v�'����?H�ۯξV�w���w*�P�����=�J&����39H�,g��3�g2��� ��\dI� �#��LNT����<�a�$c�$�'1ky/�;6��xK��b��yΔ<&,�e��G;���N.���2��I���y�B��ʩ��Z�1Mk���2]R�K#�C�A�9���w��M�haM��W��h�^���LD_d�̈́��[��۫/W[����J"�I�E5W�?V*��2�y�q67�P�^�
�_�ُ�Za�n�I2�ĵFc,�&�a��8��)��V������e�`ҕ���VD�:��NVk5�V�"�)W
��ȇY�R�|Я��b̺!�iU���%����=�U�����V�c�Yb��$N�Ąy���#H��ZE�	�D	�
 �#�D�1$�Yb̴]3Ugsk���Z̿�������E5?�>�����Sy������ҧd�8����s��h��.1Y��!F4C�-dN���*]"�3���ƻ$e������"�A���\ϓ	�v*�.�5�b?�����w�������$�r�`�1�����4�u�&�&��HD&(E<BM�z"w�7G�������8u֪U�ԙ[�2�R"7C��՚���ã�k͠^�a��Ξ2���M���Г�{�xŠ�\���!���=g.����<��J�X�uc���f��8d�z�h]��/�S{L�zJSO*<�d�Jwˊ��P����Vw��b��ۚ1�%�,~���9���Ǩ�>�;�����M���i�Ϟ-,TPKܠ���V���ٞ��U��5D��>�������OX{9��5����Ij�k���]�Gˎ^P�P��
;Β^�� a$�x�B3'xi�xN�a��}�a�A�4�i�D�zz
�BЎL�>�v2H�χ���D�2P���#�g�98>�bA���E�+a�i$)��D)-c T��P����~
�C��S
��,U7��I��P��|q'b>�X�آ��J�T]���U���6A�N<*���<mD�"g��d>�1�֣d�5���`�2E*Y����Y���� (�0/z<�'�F��(�
�1�d���Ղ%��i'�%Aڄ<�3���X���=���A�7��~#��d�u��ȧ�I�ɓT�{c#�̳=a0,�>�z>
�hI�� �3]P�+!0�5֡���қ���;P�z�x(Х2��"�z��p�H
�0�/�[�
d��Ѣb
�L��"�C�iab")v�p�*��Jz�&�����R6�7���XQdj�ΘAp%E�� �Y ��H%��!�~��"L�f�T����m��L��#�2�0A���x̣��H���7*u�;M��bW�fG���!�z0}�s��J4�i0��4�5٘��aV�ܥth*�W����:z�O?7X/2P?݈��#�i-�<@�rk`��u�=��_��8�_���t⇣���I��c�m�j[��_CZ�a��{1�P�d�#rE4ͫ�N��I+�ΌN8��dT�@�6���9�f�6�;�`�)7S�Q`�2#7"M�wi�;5�(lA71d�3�J��t/wT�gc�]Q�kX�	
K�Ud�^(���}ACŲa�P�*�h�V�G�e��{X裭����$��0��H���-�]j	�4�H����SAc�o=F�2g<M���5]UĈGC��L3F��t@�+�Py����x�}6�\��K�f�u���@oWG����7`��������փp�);<f<u�Ԫs�{$�
�s��m5�����S�[�p̨�0B砊�۾���"N((2�nG4]�m�J!�c�i���
$.��RC�Jb��ׁ��e&���.$2�!�"�?���Ӑ�6�Yn��̶��=�����%ua���I���\�P��b1Ӓ-x~P
�ǥ�aJ���~_�D���J�u]6I����)a(94V��\G�4L
�[/0�`��a9B��K���H�_Ґ�k˃�v�y��Dj�5ڞȺ�8@�%�\��F��A�C��	����|aol��X6�K�.�L;��s�i��CŪS�	�ӱ��
����0���.3��T�(i����y��~�<�jtX�LM�g����Z	���Y�jSS�Ud%TU�ilv��N3�1VGp� ��P��;.��nM�}�N��)��`7�ѳޜ3E
Q>2�nʯ����
����"�r�����~Ŭ)
�5��t��(B5���V�R��Xxm� �/��6�k6���8�ǉ}1ȸ��5k�A�i����lOAA$�)  �
q�F��(�y���!o1�&i�,RD�Oe#�olZ��0�J]��ѧ�D�k������c$	��!%kot=W��U ���C_a�9:���x4��.�b��]zXwe@�I��
P�A���a[Cɠ��6�o�e���7]�UpFd��ݑrk�,I	�QҞ*�{�f����>	�}����ן|��@�p*�d�>����%<Y����~;w��G�E����>����~�sq�\��ixʡIW�~���,�l\��~�t��z�i���n��??�����\��~�;<���ퟜ5�ɽ���՛���p�xp����h��b2���9~.n���c�sy�~y�<K�oFj��b��nu���up�a�����q��t_,�zy���O[���|o����֫C�1>����wz�|�Y:���Ob'<�G��P������R���x6��o�O^ܶ&Go�˳ݛ����Io�@v���d������K�_�L�wWN.���&+�^n���~�onTX& �X�j�э���?�T�.Mx�(Σ���# ����\9�Z�)y;u� F�2���R�y#�L���3��:S-�*�.Ev�"�1MYPQ�D-��D����-ta,W"N{�R
��z���[�fd�/�a�F'Cމ��Z{�Z���h0���ɛ���r�>ܩ��4�� �__+���2IE���z��<��%�g/��&�>W������}v�f�?�pvz�����?��w�v^���-&�ʥW_ZrM�Ҫ�O%w99���'lQ�~j����������<�ٷDV��,�_��;�:=�^��P��2�F�)�:���<�N��՚�ئ���ZH����$�#wf{uv5�VmX5��װ�����F�w�
f�q2C�ˀ�)��_g�1���+�t��}�W]�ua�3zҟ�Lq�c��,������t�b��dgs��ϴ[�Y�P��>u�mhid�Ih�fB]3�	<�Q0����O���3#Q�
�k�x��{�ooRK3�!�e�A��/�y=(��ZA�`��k�8��KVWv聻����tk��r��J�^������J)pV�9�����R�����o�J��
  