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
x��Zs�F��=7dݏ���"���o�k�z�R[��m�
C"PP���~_����I��T�`zz��~� ����}��ďo��7�z�_j�^ڿ�A�n���[�^���߯n�þ7��gW���7O�[O�9������~��O�(M��O�ʟ�_;�]ʮ8fB�w����<
�QW<��&&��"%T�E�c�D>�"���Y.�M���d0��;]�NGE�i,����Dei}�D�#pԒ?�R���"H3G���D��+đ�N@��y�O�	�t~,�,���*���Ig,���<��2�b�O�2�Y"",?Ę���B��K�%R䋩$Řq���	X2t@�Ά H2ˉ�%f*}ɂ�B�r���3���4��'\ы&{2��c9�Zd�Ng��C��
�Y4R!N�$��y��'\�PN�i��K���r1��0O��������<��Td,ne�|��be��fmb�Ɏ�Dʟ�U+���g��i/�<��d������UH�����~�~� WJ3��*.��
��}�����Y�$̣�,�3?�}?�\F�<��a�9��|�I?�e�l�m6�cDY����x"�"E> �&���.]`
-����rVLj7�] �!/��ei����R�f@�S?��Ρ-��8X��PH��0�[���(���T�I��4J��'��8�_c���n��f�K�!�m"�E��ˍ+��-�-�
�~��tABo+���N��|x:
��V��"�d�(N�+������C���������	&B������j�e�ͳY>
��=� ԗ�9�-� ���Y�`����d�I$��0$]��ʑR3w�E����	�
e*=u��}������X ���"��bM9��|x��
j�=�BQ�rJ=�T�����F9ąh^�dn�/7�[W�_C?�r[l�ٜH�����)�r�����.f��f(>H<�#�lR�;�Hh�����"qv�݋����P��?Tm� F���+��	�{��J��� /$==,6�]A1��7��>�Bz���X5K�e.
#5�N���BN�$V�ɓ٤O�m 
��L̔t�,��yl�6֊�`���t��_ 4��L��|��X�9���{�2.�f��W��{E���?У\���?�Q?����%v<��i�뻦�	"�(9u6���O]�J��f��e��0�rQMI�p���8�A4 ��߰o1`���Hx�{��KW�#���4 \�6��=:�[�Y$iҁ��@�)g��������BQ�J������pPr����a��A<��1z�=N�cb�g+L*̩ը<���e���D�.���DΗ̢�$Bj�#��&����I�/`+�m(WZZ��X��,qJ䴢{��u<nO��)W' 367���ǔ�t��Q.r�e��?���h6to�i���l�ڐq4e���$\���d���ɾ�7��⩰��5��0�+jm.��4�TRI5���dR�I�[M/s,��p�L9ԁ'Pv�<m[��'����OGo����c���4��m�(��F�V"�u�l�"熲?�L7pN��{t�N��r�=�)�+��q^�#v�jH_�&_��䎖��"�ZW�m^^k5���&�֬�� ��䏭T�S��ǣ ����W�J�C�S�o��P��X��d�i{)&�bJ�(L�i�]�3�.�B
�cʁ�>vF��c��W"����1��-.aT\S��cbW����*�"� f�0C���n��԰Z��plk|�Tړ�Q\��>����!�� �(l��̊f����)�1�%�h�Al62��2莵�e�'�eDo鞁� J��
���|�+��xE����^�.�5P��gi'B���[���8��w�D9�
�F�����5��*���z��c{���?99:��-S�� G����a����Mi�`S9�b�2�u΄���R�Y�^��@��dd�͞K]��J�%օc���

a�ΰڶ���<��b65K��0yL`�D;G����G ����3ma��î��akW1��	��:ڑI�Ue��5���(�M�гKn,֔��Z�
�N���u���7�����e���Ѵ�aM<�ii���Z��6sC�i�o�F幚��Y���\�.?,3�*�V:��/S.�6`<vj-]��|�2�*�,���+QK9˴��g0K�å�J��noy�R�%ڤ��+C�H�d��;ڙ���U��T��#*J�tY�D�U�m��:MQz���
)v"w�~��^�c���t�y�z��
z���g��Y�^�sj��2�����w�i�S�I�,T�;\n7�{�A����Zc��#J4<�_���(�����T��e����I�)�6�b{�A�5$�Rҥ��خx|�����X�� �l���s�%���Z�U*��nul�&��^���ZASC�MM�鸐��]��ڧ�ڤ�zkݵwݵS�a��������qV�P4�q�{�;�Ș:eR��+�U��U������u�(�m�ه�ľ�x'>��p[>��_եŭ�uŰ��8���Mg6����˓���`���.� {M��Ѐ��˺j;�U�#�U<����.�G0A{�W�+خ{�j��������NԜ�~g�R>t��O���i|�S�k�(ģ�c'�uN�_͒L�P��gf/T�s1S�Jڪa��[K7mt�n��u[����Ng��
�]�յ�Ȼ쀻fQd�@�@,}�Zi[�����iߏ�p
���NL�I�)��.Q�������q�ǽ9��\[L�<4��޶��V��N�Ej�JޔAHէ�g�S�
�x�g�+��P�<#��X����K�&E�H��д�2�����D*B(鉮�f�?�������xh�*W��g?�ɪP�w��������NIZ@�����?����*U���Wz�^����_�����(�|��R���|��>���������8���jç�|<riz͛��#r�} &S�"]�G���m����h%�����gWt�G[?>��j1��Z#�vsE�3��:�[ıc�WǇ��omh��[΁>��5�x/o�n'��~I�ɖ�o��)�6�;`d*
�hB׫���&#1b:G(�6kAV���Ά��#nm �PډI�LF�W�v�}L�2�6̷�
�
ã6�|�K�k~�SkKk�k�Ey�K ���0��?6��a��r���ʻ���IqGa��d�m�=�,ke.�y����}���׫����Qm�E�NKq/E�
�P�,/ݪb��G���"W����Us�/��jK'�t��P�^zX;��OmN}���%z�����Ӱ��y鐞6Ν?���{��zc�y�Րgu����Y��͛���ys����e�y����_����4����*'8��q,�.�ȏ�/q�w�W͡Wr��蓦����9�n��~�￝_�>�����ӟ?��Q��f���ݛ�����������֏;����˳��n_\|Z�?���
�w������`�����tg|�^|�4�x����f���d���M��峋���������������ŧ��ޏ��cr1�m�����z��ԟ�]����vt�>	�͋��|�٨�r�|�����xz���t�.�|�7�y���C:|s��on����Ǎ������b�a����qo�����ŋ��_6�[���]`�@���}%_<����c�:xğMn(�
��5
?��D��X؏Zo˱�m&��Ph�G�i
�냇_\����"��h�ޏQRVRRƞK�`�i>�uE8�Ӣ�L�C��ޓHM�<�+l����W��@h���o<�{|z+K/�.�[�t*z�8�j��35�j�����kʛM	P�{,�ݦ>��L����T��O:��O����O{������ގ����p��=��}��g�I@�)D�S�ߘBy���¤D��dP�M���(Wa�ټ"
[[--�}~���D�4h���?��?��H(�=dr�6��P:����i�W[�6��D�'/�U���[�����]�`�r�ROU��m���0�7�Y�/dܦW|�	Y���.�C�JWubK_~����׊t2�lL�Dmo�]�v���V\Ej(�V�L�S=�s鴸��w!���Z�۬R�6���z@]#d\�^����r������7]�˰q�5�@&��@�ȟHhY�0�g=������M!!Ai��.<�0нba
� ^�,�D�0u)?Ԉ�:j
7t��k����K��ר���{*�M�^&�4f��r&�  