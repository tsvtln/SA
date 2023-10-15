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
x���s��9i��?�?o�z�rB<��jR2�m��9w~A����$+�]���\��~�J2����L[{��~������k���ǎ������q���_�m�m���^Lm�r�Y����~�����YƂd7>$��),QXcۡCۙTĀ�(N��E4MK�� ꎆP��w4��]S��cRY�q%�<|iǴ"ɲՌ|�xB䙔r�naO�i�lT�>�L� UȎT:�S��GL��Cť�
K�@�
���%��T����r�3�4"�nv�!ɏ��R�l &�rJJ�#�� ��?������w�ͣpJ�DsI`^��[ڣ:����:Ηg
᳑%p����N����Y�7��B�B+�e[O�J�T�$��!eN�SR���.'N#Vx������xBD�Y���o�*�ך�j��
X���2���f���R�'CtE[<�4�8u�Dw�a��{���	��8��y�SȨ��H���DAޔ|�qݑ ��`r�'s��"?}>
�iz&2����J��b*����Ĝ�>ӈEA��{�9
㙍4��2ْL8Z>��Nt����8omY�9�s�{�@�`�KßH�aD����uS��z�-�i� �g>@�����Ӌ&I�=(!	BHY*�A_��	2�1a�1�%T� e��v����'�"24���<�,\�ʘ|&.Z��dY��U�U����p��|�)��;�I�9�C ܐw{�s ��ᨮAd����	L��9;t�b
�M/tBD�eN���|T�#��	j�	�cA y���f�J�d3S˹���2J�Ee)��6��]E��%�"I�w��AkԲ���}c�}���1E|����D�+I4��L�r���bJ��,��u�A}���&kL�ȐR�d��8r��2`�hT@��}�@V+�!�pyv���O��D���K���Ͻ�빎��u��w�5fv�=;0h#}l=q�Z��0~���=��D?�~�L;'�I��b��{W�?���W�/��Qr�NWǗ��'�ӻ�����n�l�����qu�.oG'�g'n���ף�m�����޸��]���Ok�n���9�~/b�����������]���A�kw7�I��{~ͮFӷ���3��^��ބ�݅���\�v���]o�_������y-�9�(n�G�����<w���x�Gﮫ�����������Y��6&o�W���j���3�RK�k���6������d���5�0]�ǘr�e8����ê�ꚷj�tE����^�dj��µc�����
"9Qr,��('�����)����Q(�Ĵ�r�Ȟ�AIf�؇��Њ�>Z��
���Gp�)H�.SWd���4u�]rЬCgh=��c�V���D)ZJ-
��5�k�-�5Ä�Pw�T���ZD��_�d�}o�T���([�q�L��֔��zvc���xd�.���с��}���:�vO:G�l�I�����V"�U
v#�_����̇e��`a�^*��6���kDSro���nz��Og�^�t�������K�)E)�2/=��%�Z4����QH}-E
	3,�
�2�:��N�خ�|��λԚ0{!o�[衔@)�4�iaǩ�Xŷh�lp;P�z��� �5]
�Aph =�v`1ު�Q�XDL�X� �h����Ǟ��rm�Ӏ��
��%�䌐>�ghuv��
F�_� MK�����tx5�X��x$�c*3�gV�bˇō��Tā:C�O>7����
H�m���� �ƚ� =7��u��� �9XjAn�J�/�����n��%v�������_����������g;?  