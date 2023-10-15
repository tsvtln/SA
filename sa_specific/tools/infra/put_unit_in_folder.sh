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
x��Wio�FM�4)?�l��:�(��e˷lI�e� V�R�Eq).u�A�{gy�p��@����웙7�_f?Ƚ���T���ُ_f?�~s�:w,_�ՠ�N������/��K=��	�G�H�c���ص���]�x���l�=�jt:�N�F<�zL�:�l�R:��Gky����}�����<�ʅ|����@2��#�/
�Ƌ����Q�, ��|��}e�Y>���cRF{}���D����/GD{(���31
YY�\ {�-�צ�8�:,�j��DZ��}"�e�c @d>S6�����1�O� �=�|�Q�,ņ�r���ɠJ埍��8�#��]����F�'�>F�<��Q(���)	R9]~���YoS���s���F(	�U��6}� dӿ7�����C�h�Ѩ�=����qL�M��#��iB�^Y��,�	o7�a�@%]eQPI�l˙�~���SR[՛:?�<�F!6#�oc|A�P۰0u�j��PL�"�I�V��ZoBƾAG�A8R�7	�2��AщM�H���C(�������V� nH�?L� �^����M1�f�t?�ڜ�YXf)�jmK��$;�3��}�I��u�a��y�O��:*@*%r���0i�-��7�vh�;���˾e��Ֆ1���q�����ݛn�pR<����q��Ţ��;��>�s5�����V��U�Gk�+�
����ëB�պi�Z��uz��w���gG��e�����`�P==a�Nߘ|hv����~/�����"7խB������0כ��c�vVW�]�1��Ϯ���e���Z5�n�'w�<�k�ԹkW�A��}�_j�>�+�3'$�6�o�)�Aؖ��Z6�� *�oap09�	Ot.�{L�d��[̊dE48� ���C|o��Ěj�5pH�Q�������\����ȇq�$ڄ7#����H"a�x����9�ۍ�h�������� ��jw��(D�E"���h�m��M����=��>��E7�M
�����(S\�J��n��iB�hVC��KM]�O�(��䃍�2�2�%�,,�:���:!�,�j�wr�P�7�n�QS/��'u��j�Ϛ
HK4��W�߻rϋ� �%��|��Q�@���BJ����
�<B�(%Sros���	1���R{�m]]��ݖĝ�j�qm��9�,�� j�I�(mϳ��Hqm%4B#�FxY4��I�4��ݡ����5U�L� E�I��S�:�AM^��1��ˡ�KЉֹ:�����"�5�n��U�U�av���I��KDzw
�>���]&o3
��"/|�*q_�1��I?.��
	����p��!����=$�f%X3QdG���	���84���>��)�
@�)k��6nL�V@1���G;��0����F#��\�MEHꅗ�F�k���l��@1���U�ur>{���~~�+�^a�  