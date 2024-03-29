#!/bin/sh

# Calculate classpath.
export CLASSPATH=$0:/opt/opsware/twist/lib/ldapbp.jar:/opt/opsware/twist/lib/ldapssl.jar:/opt/opsware/bea/weblogic81/server/lib/weblogic.jar:/var/opt/opsware/twist/twist/stage/_appsdir_main_ear/libref/TwistCommon.jar:/var/opt/opsware/twist/twist/stage/_appsdir_fido_ear/entity/fido-entity.jar:/var/opt/opsware/twist/twist/stage/_appsdir_fido_ear/session/fido-session.jar:/opt/opsware/twist/lib/commons-logging.jar:/opt/opsware/twist/lib/opsware_common-latest.jar:/opt/opsware/twist/lib/spinclient-latest.jar:/opt/opsware/twist/lib/common-latest.jar:.

# Add some 7.8 classpaths (TODO: make this more elegant.)
export CLASSPATH=${CLASSPATH}:`echo /var/opt/opsware/twist/servers/twist/tmp/_WL_user/_appsdir_main_ear/*/libref/TwistCommon.jar`:`echo /var/opt/opsware/twist/servers/twist/tmp/_WL_user/_appsdir_fido_ear/*/entity/fido-entity.jar`:`echo /var/opt/opsware/twist/servers/twist/tmp/_WL_user/_appsdir_fido_ear/*/session/fido-session.jar`

# Calculate java binary
JAVA_BIN="`ls /opt/opsware/j*/bin/java | head -1`"
if ( [ \! -f "$JAVA_BIN" ]; ) then {
  echo $0: 'Unable to locate java interpreter. (Is this a SAS 6.x+ box with a twist on it?)'
  exit 1
} fi

# everything looks good, so lets fire it up.
exec "$JAVA_BIN" ExternalUserUtil "$@"

# If we get here, then exit with error.
exit 1

PK   uP;j)g`�   5    ExternalUserUtil.classUT	 ���JŅ�JUx �-'�Y	|T��?�f2�2y@x�#ۀ�CV�}XB�H����$�BF&3afD��}_�U��n�Պ(��Xm��Rm�k�j[��v�|��ޛ�$�@?���w�=��s�~���w�Q��[@�O��2/�/�A���x�̭p�������j/�\#�5�j|��~�
���:�<C�35����4���8�q��M�e��q���E㈴gk�Qڨƭ�4�kܦ�&Kh��8%��o�x��[5���9|���������M�5�H�5�D�K5�L�].�
Wz�*/-�ٿZ������KK�F�륽A���I�������"�"�[�|o�]�����wzi�й����
�n�GF�p���t
x@���%���%_���G<�����4~\�'������x����&/�x�����xx��R�N�O
�^!��
�i~F�������������	�I�y�~^���=���~*�g�����_�K���W�Ϋ����&�{]:���t����x�f��f~S�[�-h�x�]����B~�?��Ｔ�k��a!�xVƞ����N�?J���S9�g���=�/=��p���������j�/1�k�����/���HS�)��<M�4��)��<��4U KQ^Mb��55@S55HSE��)���TC45ԫ���5B��ƣFz�OS�x�ea�%5
�j�G���XM�Ӕ_S������c��&jj��&{�q^zO��S����bM���TSe�*�T����M������&C��0SS�45F����#�\M���|�<IS4�֣yT%S^4���_Ol����Z̊�xkk<���̆HlCEM|�&���~�º�*&��jk�L�B��I3�:�b~@����/�jX_�t��z&��X%�B�ԚP���#rӠUk��W��\^�d�����١͡�h�է��<�p�mu"�i�Z�b�Ufk[4�2��`�J4�,
%1���E�Xxq,��b6��ZAsa
��e��p$	:u�V3gؓLF�q3���"ޖ�J�B��F��|4b�R�.��I�8��L��I��U�$�n�Q�D
̛`Bv���C���D�� X�]�c5Y��'�0��`�G�ސ��jO�r	���K�yfl3�0{���XJ��B�QS�غ>.'��4<oE"�6"f���T���&�?0�/�pU�ØT��u�P���͍�"���&0e
��>��q(m5m\���f�ij��.�#�xEVP�$*�X2G(D�U1�+l�q�c0U�T�#�Z��i]�:��
�<*�ٔ�':*��8�P	N9�����ïY��@>v�iV��M�[���lKE�G�di�3�O��ڪ�$S 0$�����=}qtXr=�G5Q2�<,����>�4�a)���G�p�Q��J���8[\|�X��,V(p��LY��i0�Q���TK5,n�aM�>�J3�M�-ߢ����ǣ��p�6�-c�s�5��
�� �\,3;j��D$�=��asycs{��2_�o�r��"�ex�/�a^��Pf;��>ޞh2%n!���\g�y8\�I�'�q�Z��<j��NVKu�R�y�y��c��|ȡ����X����C�P�\4T�O�$��Z��f'��G�Κ�)�+�N%%��7���M\�D;V/S5�BY�	zqh̘:b��!%%���n����	����C!�>�ʛ�x��d80���)d��<�'��;z��q98bw��V(OeA~{$<o"Әޘ�H�9x���e����gH�<H����ɷ���]��b:ɒ�0����'ڐ�G2/HZ�����Z]�)ޢޖ��&�͑�f��9GmS����j���p�LJ���vSɘ (~@2�0�TmPʌ�m-�L��y4��a�:��&M-��`6t���d��b;�!�އY���,R��`E��NU+q����y��^�ݪ�d�G���y�*]�Vkt�V���u���	8C!YN8rr�c�9�{ԙ���Z�QgI�U�Pn`
h�A@�����lЪYF���uV���G�t���j/\��N��� ��f(|���oJ��U�ڤ�t��s)��҇�Y_�jr@���.�U�a*n�����V��ȥNC ��!��fX2	BQ�PUo����4�g�,�J�*�Rծ��\��-*�t�Q�]mU:��y�:Gb�lK��M��#�����p{[4"�>�{<�!E�#�_�r���*{�R��ՌF��˻����]}M](�"��a��Fj@"ZIH�4�����u	� M�K�!���D�#�b�-�r��py��\WW�s��C3����3�\�4�_af���bd���5)B�Qn�@LPl�E�>l�4E,*��8;��sM)dT�h+.��
{�x�u��^��#�-L$Bb<��Q��Q_���b��o��9��V����6ԋ�2FW��m��.�v0*x���13U�ze����ݎ���ia ��Tw��NuӨ\����\7C�`�\r��]� ���w�{��c��%�x�Ȳ y؏d��߫��$I�a�5L\l��1Dc����/�>��~UY���HLG ��jg5���a�lv�O<���S�V3ގ��?�x��Q�fc;R���']ݯ.vt�I��!˨�#�H��D�>�����Kl|�z.�~s$���].�cs��z'�� N$�i����'B�����T?CsQ #�����x4ߢ�ԃ(ۭ�5�G��t2�z��%����E(h
��y�\9�z�&^V�֣�1���Q���o��ے9��U�"�d�T�ձ���j͸�3�4��L5!5���!%I����fq��t���j���u��I�9��|�u�u'�G$�[�ǟ��-;��I��$[δ��(��j������� d���M�H�o�+��k⨒�C�{4%:�Rqg+`��ڶ�u��� V]��\W�$�d9E��q5�:w�'2re�<�~R���DΏ�z���P3���{#�r.KV�ֈ�"�凕@��ߘKԒ����Wg.�u�]V�bF�t^ ��'$C�'��`%7JZ҇��uq�P��fnȨT��5Lf���\ɋu����|���2Sh�E� 8*G�m��U����?��.��lmT��7�����d�=|\�*xy�و.(�u�ѐ��Cz\�A�'����$ny
�ĩ�C�L9򣢼"9�
b�G��67�[�fX�
�ps�gp�h�H�*���=���e6�F��H
�6S�TzT�u�<���kF���f��F�~V�^<��o��`�G�5� �"�jIf_�� �7Ţn��{�8]fFtϬ��
9��L����#��������s�G�9N����Çc�����[����G�v� ����@|����1P%��O�őD2e���[���q����=Q.� �s���kB���J��5ml�Z���P"�}�t���j������U-���W4;���� ބ Hy��}�v��du�Q�%��C�1� ��{R����̝�0.
��Ba�wd���Dbas��f��j��d{c������>Cɰ@��#}���F�����aS4.�H�Wu�9��Wi_�;|DA@j�3M뛙~�&��p��ʾ~#�oB�M��İ`T_��23���r.^0k�M�f2���:.p$.�I������ov�É�ko5�L<�)u�a�wm<!?�l����V�lcS�;��-����P�o�X¶���Ԣ�j��;�DR"��i� !6�6"c}f$<wԌm����~^��3f��0�l��}9�H��V;lu���g�Sp������Qn�g݄���P�Y��vY>'��!g��kH*
������u4ʉ�n�]�[�(KRՙ(ᶪE��%��(k]e�8�/�	��]�t���
��D4�I��lv��W%BM&�'E�hɳ6���<�ǰ��1�Ʒb�d��
Ƽ��\���N;�i:� �-r��lX�j�Üv�3?�iG:�ϙ?�iG�/iG�����z��P�"�*8���4�*��>F�
�G����'Fƙ'$9�
rөTD+�%��6����.r�)�w��8o7i
x�#�즁�� �(M�kJ�[�1�!iZ[,�Ì��6F�i$�Ȉ�8#u����kht��kh�1C��o��;�	V�X�7Q:����]�}�5̷������V�L:�6�[�+�o��u�q:{�D9m��=�ڐW��7�Д�7��������1��A3f�7��Y�c6�f�9�^c.`�1�~7�/��煉�}�ݴ ��m�	�\y.�M���ƻ3;��'`G4�Z'�2��GS��Ҵ��� ��N6�����) e�KӲ�T�I�fQjsQJ�(�>轮���M�a+����Q��.��OR�cLߢb��䢩4�� ��N�������TN
4�N�9�����Ia�
m��t�E�Q��Fz���i���L�55�G��>'DP��`:�Ϣ(7S+G)�Ij��i_J	��R0���W����w�|�t���Ej ]�ӥj8]�<�q��L/��j�t����t�"j�k�V���T/�cҴJڂ4�~4�Kc�x5it
�-���h"]O�t��&`s���B�A+*�>�%�o�k�r���E5 ����@Ik�ӂ��s�{�AQ��>�}4���K�8O��`�̖n�]��OӺ2�;Mg�A�g��r��� {�|�4}�Ę�?��cz�g�3���s��h,1f���Tb��Ř���s�S�����
2��'h���1�K�i�cl�$?&��^�1m�"�6�ԍyT���x??C-�5|
O!���$��@���F�=4��/uR��� �з����ax�#�]�J�R=F�n���0�.P�Cw�>`?�����~�>=C/ҳ�2�ަ��}F?�/�y$���~��9��_ ���y���/y6��U�:��7�4z��]n��8E��s�w|	}�W�G�
��o�?���G~�>�=�)��o8����W�!}ο�/�-�;N]��}q�S�|\�TňG���Ғ.j�U��b
F����E����E��dX��O��i���0c�9�O�w@���Jb�>J�����(����$�B,�rt�fd|�$�%����"��J�%�#_爦�
jt�C��i]�ՠ���M��ۨ"G�O<�p{"��H��K_S�y�Akхk�}>/�,� ��W���v���E�TtbL;�$b�蒧�
�t�3�k�x�H�"X�آ�oҥ�|�A�#�!ʡ"�hJ�q�.��<�N�t*�XM#ʖ��y8]�#�Ew�h����(Yv�|y�n��=���B/���<��D�6`9S������;'���1)���!H_6_����8.�C���Ij�c\g��
[�A�ϵ���.4`X��<�N�Y(����&��b,�d�ʕ
��.����d/]����\#{�<	���p���\�=G���6�c1&�XaqI)H�Oӵ�z&^f-u#Y�@!�x�c�ۨ ��'qF�׉�'�Z��8��,{�Q�n���]��`�>��� ;��e�wR��
W���
뿕Q=A�;���mp��Aa��e6��2�ސ��v�F�]t{�^���k��䗔�[��"��#�y�����nF�����P�.�{&J���#L�g쵉�������9�cx�o?�M�t2��n�6�H|�Jy�c����y5��5T��V�
���@_Og��#Ƶq]�&=�X�(�M���^��u��	ļ͈g(��E��U����RY��8�ވ1�ۙ\[r�y�ǔ쿛�%cN|��F���4= 2IӃ���q��wJ����'Q�r�l�U\�����@��F��p�+h�%|m��)���a�yǠ;�q��om���.���ԁ�*=�v��NB��p��v�w�`��iWm��h��FJ]�%��sRn�dG��l�)s����]�Q�ه���M|#4�u\ln�AB��$�NKy��i5�5|�˝�/w���Gl�����&P�1O���-׈�Z��س���5�k��'��Y�~�)�}�x�j�5�/�$�0��46����Hc�|����0��⓲����RX6��@)�m�����t�x�>K:��	{����J��=X�� �<������fr�^A${�~���+0�&�H�]H�}H�HwA��I�e��1z��i�~�M�+S���X�a�Zu���e��~���2X�K
����.z��~���:iT���H�vY߿����7���FU�������4�)1Z"��csB�����.7�3��b�k�ڔ��{b^�
�����`������w�ޟ�އ����]��.�J�w���F�0���0G�[m	�F���K�v6y6�:D�	d�l�o��?A=� ���W��s��0��������|��s���nTy�C��n�O�(7=�k�~��oT�����*��J��*y����p Q..���R�B���Qr��Qn�x��q
��w�IsE�y'B�h���.�ƌ�?�n�����C�tҌRKG�ý2P�?�N���%�E����*Ĵ,��T0l�n�c�㳬��}�����b�����������d���JP��|���e�����['_VM�&���e.Kی/�fCA�71��;�H����[:�ɲt����N_�cM����7�(��wjz�W��l=����VFR��Q�:�
�(�FS�Cj,�P�h���b5�NQ��j5��P��QM&SGUL�����R܄��Vhx��
�F��tzJ�E5�^V�5���R���ZL��*��ZB�Q'���r���U��תe|���M����r����(R�D�A�8��A��wa�bd���U�PK   uP;j)g`�   5   
         ��    ExternalUserUtil.classUT ���JUx  PK      Q       