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
x��is��u7�d'ʟ�h���ⰇY��`�x<3���jZ-�B���~�/�k��q�r�R����o����;����������&㘳�oXDL�a|��x�'�)������w�G<N0Y�,f:��O%;
<�:�($��s�2t��g b��^�c?�>�N�)��pB#�a�i����7CI�Emd�����/h]�Ѱ� EG����]�M,�HM9V����c#�G�i5Q��|�( �W�	l�#��	�Qi�D0��
�<�j�+��"�H�����Q�3&p�z8T3#��z�	��[52�4=�UӤ�@�ǁ8u�1_Ʌ�q�b��}g��* �
]��H~��@���˞52�����ݫD����������H��\��(3\G�W_��Q�Lßk�����À��R���'�.�I�jB�
}���l7�l�[BC��� �
8��o��@IY�$I\3n+nl"�SU�"j	�D-վ�_}�:@�����\�d��Fއ�;`XČ(a�q�9nQjØR��W��0���/�(�SjJ�տ��Vt%�y0�~w���s�7�v�k��H��86}�Q(��&Ix�wP�H�T��2�/-.0�`LK�H�)��2�3R(��kr�)��W� Ϊh�l�z��a
�[��7��K��TY�L֓���5�!���l���Z�	D�6�TU.W�%�/�::)�*��"%�Qt�}s3z4ZC���a�X�<������gp(�{�<��u�@�#�;s�\�z��R5��DC4_���ܪ����y�j0!&�3�Oj�Ux��^�1�A,�<��]7�z�w=���%�<��^ߴ �tȷ���H��[C�;ҦP{E���ېN-�λ�Mv��Up/I��G�R�n�-��o���`�^���됅KuGl�]�4����q(�b�O�I�����/�E�j3o����l6�}�il���{Ջۋޠ��i�o���E�C�*v�Ǔ�O���>�<�W��Ul�N�Ξ<t*o�K���X��ýw�=;�.7:�������N���釷�7W����J����y��%����]��pJ拓���euֳuѳ��p;䥓��8����c|�,��ן���|�<=Y�Ӌ�3�\������4�|���8�����n�W�o����c��<��\��o���������k`XT��25�In,�:\4Cf���
��n)�[��J<$�G+>�& &�
�@!����5���e�� ,Y���5�d�x��b*n(�)��@�r����x@	��ԁo�AI��|�N�׀AC�c(U	�MJ�m:�(Yq<q�V9��湎P1��,�LǾ��G3B�g@����j5ń��`&
�[!,G/Hh��zz@��$Q�D�o�034V���\~<7���~�i~j\\��V�ݺj�CXP��IG�G"�9���0rD@'�,W^�o,�|x\��������H�I�7sE��}�s����w��~��(�wB��0a�1�2SvoE˗�����^J"$H}�V�����I9&@��B���@MףrM�(?�� E|F��Ґ���
�*X�!���Rg+!�G*|��GG�
�@�L�k��^�o���<VIq�aG�g�U�؞R�t��}���Hy�n�.�������F9$�1X��pi��3L<B9�������:J�&�T�P�!���'�L1��Th�o�D�G�p�X!N�C�3�A��kw
=G~Y�0\D'��ԣHHg!��!�!2� K��2�Z��;BjY�I,-��2�Ua�'  