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
x���r�F2�L������\>D,�+e��
v����z�ĥ� 2B���&���=3	î��S�eI�����������X`�c�O����ۿ[~@C��!
��ܹ��7��|��'!����|���E8���Nf���i�#��	B
��E�K��e��l)�)~e�����x#
C>�a>�Qb��j���dlN���(����(s�"���:6%a�G=���7 h/���R�����sN��~PIy,��4�s ����~i�cr���U��"pÐ4���E
��}�������q_Kd
��'�>�36G��M
f��j��#�
�m��Q�I@-���^,�
�y6C���,$�B8�T�䨠����h�C6]�KM4]v��Ir��[gl� (��N� ��i���R�������fh���K���m�/��� ���U���"�����ƣ�廴Ꚍ5bf��B�1p� ��24�p��x�����xXʝ#���(�=�%P�|�5>��|�]��	p�@e�(F�YxBF�$q�"QDl�(Ӯ�ޝW��e�]��hw*��F��(�q�?	[0��0 �5�R8Ԉ�2��O�M7'�٪����������d��?����'�7/�4l� �`� �Q?1x�)	)��g�g�iޙp}q,c�>�	��◲�w%W�p7�s�jEZа*f����q���,�*�"uٷL�
B��0���_Gvw�Ye������#,�C)�9
�R#0)F&`�����G�-u�l�%�p6
�4�&��W���2��Ϯ_9�K"S�aC���C��E����nkր���"�.�L:��O��;O�T"��
�ݴF"�R��pӗ駍P��c�7�]�ri��g;P�"H�i���q�B��9�Ϲ��HI�g�DU9
��P�.��.�`P���kA9���JP:�����&�� 1����߁���Wŧ}L���eaB`5{�2�9��'ff��1�.��y�S�?ò�[�|�i����p#P7\�  ���s2��
�=���=Cj�+WcB
,�=��RLc�����
,�N�v4����a�r�r�K��]����yw
�J�	�F�m!�%wx�"p+}v0���/|�p,��@�L���R�Z@�i�9J�a����
�<�r�d�7�J��}���� )�o��vP,�0k�t�+����s^))ʧ�tRW	X
�و��	<!lד�*ì_a�ج4^q�rq�B���fq閑��H�%�lp�񅕤�|������gT&�.��������FJ��ԗ�W��^�������I!T*�F���_+�$k_��K�"[�e�%[�����E�jB����-� d��o�Zh��`�.��_� �n�,���ޮ��o��୞9,r �#鐫�\ͱ�Vr�
� 5S!Կa�vp�Aq�)�K���9|�Rʮ^�+d��8 di�K���za]UD+�w"
+
���6r݄V܎ƽ����c!�|�P�~ [�-����j@�Ȣ�k�{�I�Y���s�r���,�J0]<u��+��٠�'�	L<��٥y�����KYB�9�}��q�fp��@%�{v}݀' ^�`qPJ��n��#�`jnō��i��3�e��=����A��/�h�	�}-��l�K6�d ��Q�9�I-W�b��)k�y�G$��$}>C�
�C������8��� �/��(Nܠ��"��2k����������� (e����Sᥒ���A{�"��gB8����H�g�6t�BJ�j6�"�!�7�6B���>d�>FX!5������O�mr!,�����B�Xƶc��Q���J�}���9\�H��*�5�D��5MS�{DŤ�f`����1s����*��;�
�XP>߱$ݴz�#JBy�LDZO��6�-jhD�R>#v���V	�l�_��,�E�`C�]�CF��$�)h�Ho�SS�֧ߑgg3�f	�?�U�+��~UZ�8Kk��g��&7��
�
!��9��䧘S�n5�25�o���U�V�,%	�����m�*��|�h;�m��?�
��?�X��tG�P��ܴ�Pp�2Q�����w�My��֔�=�W�ƅ��\�q������дl�]%s��5]�Ƕ!�1�V5�u�	��%��^��x[I�]'���ݰ��Z�V�T�ȵqsiJHf�����YX�@]�d6�Ք���	�S��vk	)Ua��\��]&�;QM�۰��g��SBE�0�Yd����m��Ts)��qǫ�Q�_��Gh]P��D;:�f2�iU�����u�2�ޱλE�@L�4�R��V�3���t��7S)�3���;�`�厺�L_��\n`�h�HS�S3'�i�4�,%��ܕi����_S���s�!�f�?w�D�����$�Prx}<Nx9Q8,��z��:�A���J�֪��e��lw�f�@�[��;�-�So��N�x|P��V�Ӭ6/ˡ5���j���^��J�RV�-���U�̹�d2��5��p��I����#��Έ��D(,/U�<���>,�l��a����@�Ȯ49Ү��� ��@�)����_'��8Ce.L
8��C�]��ɨ���0�g%I�/_��O|{��5~tZ�p������99؆q 14��.����n3���\�K�鯝_����A<jP���A������uz�H���XR(x�=�h�N���7�w������շN�w�wo+�;�	?V����_�o�N�����ޜ�����ý�����b��Q����g��~��}h7���h�N>܏��OO��J�Ѫ������O���7��o/^Uή�f��~�Xys��{w�я�·#�qt�6g�GZ���4?�����.,{����+���b喝�o^�nk���ç���u���^O�J������sx�X�ퟴ?�Tꋓ����I���B9�f
"M��qpr�/:5]cr���M�5�����7�
��9MY�V4�Ω_�����#��a`�`�2��`+�:��l��P:@)��!�F|�K)v�3<�G��G�Ď(?�]aB~8pw����t��M�y�ZN�����s��U8�E!�V����Xl���7�DA���,�C
`꺦9���P�{�����©%PU<� Nԛ:���C�#�P��{�����ftZ��F�̸��>��F�zQ��#�
�P�_B�m�l�y�����O�-�@�M6�/>�Bz�%���%��,#�����4��7�N#��|?g�F��H<�|:�>��������g�LՄz�޲�`�g(�OЀf0��r�'�KG�D��ka=cĿ���>Bk*?��ة3ml�U��M?>pw���+�w��c��)'�%���F	\��-
���@�{t��D��j����'���� u���0�~`t(��P��֐>z��_1��
����M����/m�ز�V�a��-IW1� �V���Ӛ����w��T����.�L/���ɬ&�I�M@0��ӷ���ߟ�[�%��"���x�7  