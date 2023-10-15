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
x��Z{sۺr�}�S��π���д�$n�Fieٱ}�؎-�qt4�%�I�d��|�~���K��蹷��L�����]_��N��eJ�ОF���_���Mc;r;fɔ����/<q�����?��I[��������'GIJ��$���&�v��4

����	ټ�%є8�8�G$��p���5Dk���~i��Ɉ�/�;/,��	K(P3��|撌���I��3�1�g΄P.�{O�)K8��������@�L'l�;�%Qs����EJ-���d.'iDRde�<"�	MśCC�»��`����.�SPǉ�)ו)�;�n�j
��h�%��}��(��NΎ.��m��5g i�
��'~�H���2�v�ఀ�	c)1M����0��F@�kLP5�fL��M��쭴*`A��)�
;v��nU�=���C���|��I?/�ݙC���m�mO��]�h�	E�瓈L(�=�}吻ϫCn�y�.15��,�(�h���.�,��)�H�R�я��O�OC��5�n �7��չ�<2�J2B���M\1�+���R����xY(��#��S�.e���RE�R�^9N�
���F	�8w�1�
"`ǋt��VQ9Q�i��w�`l�1�@�	Á��G�q�9��fLӉ�!����A�-�ӑ�f��a��ڎ�t[��v� L�-#g�	(8XK3�;C򔴠!���-���D��f &c;�Sm2��|)�5�>@S� ����3Ҹ�[�i�� �p&O]X���<��l��(@7�g,Y "H8���׫x��,�~ Nj\�H���`+���N���*GΣ�}=����\����6D����leD��� ����4����sL^�U!{�%��7&�P!�����@��]��.��z��Z(A�I���Sa$��$G���!r�"� l*�k�|�S tq�A�\�d���c��#�t[*䉈C���Z��w_7����*�Q�F��W�#�%5}j�J���Eu�U�=��^�|$�MI+�+�!�C�Z7��q)&]�$�<?t}����!K��ق�	K���Z���H-'B�9�
�>�qF6E��d< P��MS;��\�����,�i���Ύ]�#	�� %�-ZdIHZ-��)$,F�B!L�A��)}`ؕ�� ��^�P'K�FAl	�ׁ��hЦ4�11���-�%-8�P�
��.��T"�2o#?���ͭM�7��I����fq��B	�l�ʩ��u` ��H�Y-�z��j�Kr}��-l���W���a��4�т
���d!}�{{�m�,�V�G�.��_ȅ�h�0�mgB���;�߶��`�c�_������Wz����@��j�S��W��~�z�DW�a� ;гV�u��3Xa�B9���5�+b��M�vpf�l-��1���j����k�6UȥsF�l�����V��$c.�ÛiېS���b�m�)���~�S: �7_t��A;HiQ�aR��)l[�
	)����_
�$I bl�*5�B�9�B&ԯt,e��ϸք��TI���ndb�dJ&��4H�
�ވ����u�&>�B���×�Z!*��0�k�B[���R�*����qDmTӽ*ތ c��e4��E�|�4�JRچ	�����4p�Ik���<Ƴ]�9�	hw�z��iM4r�ݎ�!5�=f��S?���������p3��Au�l�k&JCL��JX��*w�, A��2$���BG�-=���lčCtJ�(��T8��ED��ң�	x�1�'��ܞE�!�5|�E©���ɭM��丫�~��(K�_İ�T�^�U�q���T�"�F=l�:&lo���Z����i��9�.
$\�:r�U�&���[H�HS�p���,�l��-
\B�.3��A��K�nw�b
�TDh��7�&N������p�8�4�,��fl>�O��C]��aU��ȝ`WN��5sv�O��3�1�z�흼;�ߴ,�u@S�C�O`s�Z.�ڎx����Ɩ��8���A��n���Ï'�C�����e^D�!�	�)T�(-��\��q����֘/S�Y��O�`�ߝ�ޞ��<{�����9a��S醪��B']k�׼���g~)6���]X��Ϙ�[��_7ˠ���`w�S��)�osOB���^�� gV)q�ָd��mj�+�AaCNX�(A!�ٳ��U��蕢� .�c(�z8��`�;MaUKFi�nB�V�[q���a�*WRa/4�&���h��Cc��=ԥt��.�|�P�D	7�d�!��Y+�@�nr��-�,H/Ez����Q�@G{TC~<.��J �*_%��[�dH�d�b%G��J�yϦ#�'~cm�}l7�P��&��ϝM���Lc�V��U�N��.T1K(�Z�E�����J�CZ�� #�T�p�yڦ�C5��	��Wxkvi]q�ՠDn!gu�M.�[*aU����<V�7jr^��j>*,^��&������+�"�wK{%��װӽB7Ãi�C�LS|W: � �\��']�!�,��ay��Bt,m�R
S*"FσI�Wq�C{�>@׋H]_�*�ۖ�iK@�%���eJ���X���	U�����T��C���f27T�C��|!��]R���ئ�1J??.�=_S"�qĹ	 I�_$�Kt����U��ִ����&�k�s|:�;U�3>˸��S[~��_�%T�\OB����]�#7IBf -ǢJo{����GY|K���F)
3C���BU[-� ?������m��wV��[��@8���ۨ�%K��#���I4�� �)m�
_�/�o]�1�KOΪR�ĭa��Z	5^���B	���R�����H~	�2�(}k����(�{4e�(Y���Ա�+ys�3�߷l�(�x ��0�I�!�_@�__
�/D�*jT��-�0������_+�0�0���_���8B�� �^�*4���L|�-�G\%�@|P;zs)�pS4j�1�XI��
�[:���Y�����6�ې���<�]ʜ%�dW=R���� x���"����|��
�e�䥄KFgR7H���t�j�UJ|d�Z�ϋ�OC6
���~���T�i� l���*db�%�dE�"S�~�2�����^5*���=�Ӝ�����W	�X�PY�_����n���U�b���*���F�ka���р�MJ2H^I�+E�^�V�J�Ǻ��2����~�����4@�jB�UV��FKU�#���дz ���c�4?����$
��i��.���І?���A��Ui�����[��V�,(l`~���}>�&h%%<� �2�%"�:��M�Lė�
�:��x�*O	멫�ŷ�5zU�-�*	ƺ��Hs+k柟v�����P��/��8Yu�;��C�S�+l@T��(��U�����˞�Co-��溪���;9g�Y�d�x2G���'�G��Z�s�����CD����\5��v&H��c( ƿ��8��;����E���� �l[\	����X�W����N�U#^�AP����_��v��ι�<dLi�'40��Ȑ��3�B���_���s�f����ۻ÷����y9�����;����K���.wG�W;��a�����n��}w�|�������������w������O������h�n��>�L?=�|y��_N���~F/�]�7�}q��������1=ܻy���z�?���ݿ�??wn�]�y������d�=u����u��l2z�}5}C��,�޷7g���Ww�ϟ���G��h~4��ޛO;�'����b��ۻ�|�=\�ݾ�^�|���i-yFB(�
��(g{���A:�9�4�а�t�b��I��2�p\:M]7����d́V����H�,��#�vر.m�.fa����L�j��ބ��e���������7�`���؇_�Oi�L�v|~���9D*H�.So��Ĝ,���
��gC��k:�@Ey��)�g� ��e5�?�rm�RI%%� �*�BAM�!�{�h�j�+�� ���DaQw5�o����wv��|�o�������a���L����u�=��Zmq��=�8�#qí��/���%n��"	�-P�.����ʛ��������y������u��%�o~0�m�?t��-G�'��3�b�4��֖\��ۈK�A�A��)�8b0v~�tE�賈f��,�lP�ck�_�������E��y�RSјϕ�
�R��zL�$�ܴJ)��K>ds�%S�d=��L���q�)rVh4m������W��p�
�8�)�۰ۄ��7@|�P'�̨3!R ��:{~�V::�Gc�4�j/&f`��G@�,�|*���>�(P
,KXq�OxTT�<�e(�Ċ��S[%��1J-0���m��|�/����P��o  