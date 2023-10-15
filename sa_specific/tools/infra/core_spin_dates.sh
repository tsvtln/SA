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
x��V[o�FN�mw�>�uJ��:�,U�R�[B��
	�����1�����T��{�6riU���s��7g���;�����7���}���"b���~�c�iX��7�f?>����˛�=;
<d���� �H�,#�$�2Q�%s3���X�4N="IB�l��X�ӵ�J�ef�:X���S�٨���0ns�/#ʉ�k`����$��}��[�W?���b�C٢,tql��#�Hs�ȩ%�Tb�(�H1��Ġ!�Ȗ���`wN�)�Or�q���^N���$��BuEA���T�_"I�H2GV@��� ��ς~�!HFO�H�P#��"+ʕ"��<�S����Fv){c#Za<��D�x��jrEV�ő�l�B��l�[�ڟEm�zI��,Z�<�G�Xh��V�"�K3�Q�"�5�0�;$!
|D���2F�bYܪ�D���b��!
� 
��}۝3GM(	h$9���y���!^>΋��Q�?!�0O����\ؚ�	0�H7�M��Q��[�Ӄ�=!�r�X͛�-��HI�eԷE0 �EO
c�
�E���m���{{�� ��Z�4�MͩK4z�`W{�)�C�&��C��h�`��G��L.V_����}���6��~��uu٧�?T[��OWg�^�3mvo���i�f������O�r/���z����|ڹ��w�҇�B/�M�|7�nW��W�j�u�t�^����a�]|\_�Vk�k�n�����9������f��ȼ�v�{O�Vk�,�E��U���q����C�~V�W��]�1�ή��Y���g��j�����s��v�s׮6����j�ܸ}(��O��QΠM�cF�G�vC!u�"6t��ψ0��:��")��E9 G��wNˑ1A*C�_釘�s�Xc�6
8���|�|6�_�LK��$���1��������8H"r �"kN��%�	��<�MG?J�ݩ±"&�a+M��tU�J6��9�x�a�t8B'OsC�a̝ x�}%�G�C�1>g��JU��jB�Ea$	**����?7�#�-�h�Tc"A#�4���J�=0j��
�{��5�S��n�[��e�mA�8����3	�e0�Ɋ�����W~���ő�P.�i
O�m�jR��:Q�=趮>��ݖ,��n�Z.6�򚦆�0.3y�*���r���AJ�Q� A��B�*OCÝ/����:�8�,���H����u��}AG�.�wd,܈�0��F�$"v�s�vS��\�+P��n0Ʈ᳓Bҝ���c�[�����[0�e�.Ҡ
)
��d)r�g����U�n��zGt��5�F�a� �H�&7yG�֯������P��BΙp��\ԹAm��x�l��@�i(j�����I���,W�,�S����B�.��"h�E�1�v:;a�7����7{7����6�  