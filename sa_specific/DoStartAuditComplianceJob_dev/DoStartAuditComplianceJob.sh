#!/bin/sh

##
# Program Overview:
#
# This program invokes the method "PatchPolicy.startAuditComplianceJob()" from
# the twist.  This method is only available in SAS 5.x.
#
# Currently, this script depends on the spin, via local spinwrapper libraries,
# to lookup the userid of the given username.  This dependency could be 
# removed by having this script accept the userid on the command line.
#

if ( [ "$2" ]; ) then {
  sUserName="$1"
  sDvcId="$2"
} elif ( [ "$1" ]; ) then {
  sUserName="detuser"
  sDvcId="$1"
} else {
  echo Usage: $0 '[<username>] <dvc_id>'
  exit 1
} fi

# Locate twist private key.
DARWIN_KEY_PATH="/var/lc/crypto/twist/twist-key.pem"
if ( [ -f "$DARWIN_KEY_PATH" ]; ) then {
  sKeyPath="$DARWIN_KEY_PATH"
} else {
  echo $0: 'Could not locate twist private key on this system.  (Requires SAS 5.x.)'
  exit 1
} fi

# Locate the python interpreter.
DARWIN_PYTHON_BIN="/lc/bin/python"
if ( [ -f "$DARWIN_PYTHON_BIN" ]; ) then {
  sPythonCmd="env PYTHONPATH=/lc/blackshadow $DARWIN_PYTHON_BIN"
} else {
  echo $0: 'Could not locate the opsware python interpreter on this system.  (Requires SAS 5.x.)'
  exit 1
} fi

# Locate the java interpreter and required libraries.
if ( [ -f "/cust/twist/lib/client/twistclient.jar" ]; ) then {
  sJavaCmd="`ls /cust/j*/bin/java | head -1` -classpath $0:/cust/twist/lib/client/twistclient.jar:/cust/twist/lib/twist.jar:/cust/twist/lib/common-latest.jar:/cust/twist/lib/commons-codec-1.3.jar:/cust/twist/twist/stage/_appsdir_main_ear/session/patchmgmt-session.jar:/cust/bea/weblogic81/server/lib/weblogic.jar:/cust/twist/lib/opsware_common-latest.jar:/cust/twist/lib/spinclient-latest.jar"
} else {
  echo $0: 'Could not locate dependent twist jar libraries for the token generation step.  (Requires SAS 5.x.)'
  exit 1
} fi

# Attempt to locate the user id of this user from the spin.
nUserID=`$sPythonCmd -c "from coglib import spinwrapper;import string;import sys;sys.stdout.write(string.replace(str(spinwrapper.SpinWrapper()._AAAAaaUser.getList(name='$sUserName')[0][0]),'L',''))"`

# If no user id was found.
if ( [ \! "$nUserID" ]; ) then {
  echo $0: "'"$sUserName"'": Could not locate the userid of this user from the spin.
  exit 1
} fi

# Attempt to invoke the GetDeviceInfo class using the user/userid for the given device id.
$sJavaCmd DoStartAuditComplianceJob $sDvcId $sUserName $nUserID $sKeyPath

exit 0
PK    ��8�*��L  �  !  DoStartAuditComplianceJob$1.classUT	 �AH+<HUx     uP]KA=��n���QD����\a�ԃ���:��:+��ҿ*(�����F�ޙù�����
@;6RX��D)�r�Yl1��xP�n"�{�P�Έϸp5t�FK5<a�����
#}�̩TҜ1T���Z�!���БJ\M�Is/ �<�9�Z(��pé�eiwé�EKƛ�a�pmΧi��xH�|qz�x5�yd�e���Z=f C����̀G���K�ko$|�����
'ќk�����n�7��2vK���I����i���T�8�ⓠ�`�{�n����V?zF��D�34I}k_�=�1��?!���:"��¢�J,Jhra��PK    ��8.FjB�	  8    DoStartAuditComplianceJob.classUT	 �AH+<HUx     �W	|W���fgv3%��Д�.�Y�]H��K��$�
IH�����$���YffC"b��Q���^�Q���t	 ��-+�x�ֻZ�g����f6aI6���7�}﻿���̹O���v"%`@��Ct\H��.��a
�|��u/E��C�}(�.���=^ş{9ӫE�-�5\h/��Z���:����E����x#�ć{E��o�[E��u�M��\���E<ę����û��w�x���|}@�{E��3�_����E|Pć�x��A-y�Q|�G�ǋ/�~">�	���1|JħE���aG|h��x��&?+"���
8��	���	�p�1�͝q���ϋ��+�EO0�'R�i��A9����`�e�Z/ì&N�rZ���f�
kV�b�	�9y�KM�eK)����~%a1�r6�@PO��eC	�e+�T����b���[9�UO���6�T��S�j��������ӓD-mR5�%3Э�rw��J��1,
��_]�Gr"�pj0:P�NO��D~wȪF�:��rO=N�KB
��צg���^��,���,ٰ�f��U��S��%�F�;�%<)�,�����z=�%�J�{O�.���6S���0�nH����
��C��n$y޵L*Ey�}9%k
CnRMK�;��0��G�����^�X���ezz��-����I�sH�*�����a��f#Nk������4��
	�ķ$<�EU	��w$|ߓp�'�~ �x��8jv��� ������J�����U(���	���~��sR`�]<sr�H��ϑM�����y@O$2��$3<�@\�w*ܧ��5�g�᮲=��W��~��1ķ�r/1N�
���`�KM�	�fL���%7�i�n�V�Nex���K����'/H�3�"��%HM*��w�C�?9�_e}���E�)=!��tӊ�\Q���y�ҝ�{�D�_K��mMq:�����5K���	K7�%��a�7����R\���HŔ�".I��S��p"�É��H'"SqB��1G.����rQ���䢅�eQ���Gc2�jVO�^����I���t:X1����#�[b&HL���M���c^�� ��N���Y�����3�*��aޤ�� ��FU�,Q7S��,�͡��UV��D��)�*L9�V4���d���DK�Nմ�Æ��s/J��hn�K�4)Z��7��q(�3,+@�WN��䷹M��l�yrœ�Y#�H���t�9��C�x�T�)tM�����i\�>)���N)t�j��Iҹ T�׌'��'�k�ۣ���S<ʮ��"m���*D��N+��9����+t�q�r��Qmc��@D�Wr�<e���u����ði)��t��92�m%��y`�8_I���|�����!�P�MV��v�_��Yk�ߺ���kcCGW���
tN�VBɈk���%Iщ��C��*�jtg�t���7�R�-����9n�����H���v���ɿ�vy0&5���`L:W�z�s7�PzI�bl��Ɖ_�lաB���I̶&~�)w2���4��
�
��&:g�e�&��UoZ6Lř<ꍼ�����t{��]�WWN�1�����e^���8ܥi�M���vCN(XD���rC��V`���+Q���+V;�V�4�w8��z2N
��0Md=6���%r��K�S=a6
ado�͛tx��lQ�8|�8��,JN��q��p%G �E���Q��8
�<D9��O��xf�ge���lz��,�8re\�ܑ+������r�,��rs�䲨؏.�uͮ5£��*s"U\b�(�/����G�y���t����Gi��8�/Nfh��/�YY>��E؏�㾼��%8�I�����*w��z�>���5���,��<��ʢr?���������#���W;�W��W=�N�T�]��"�¼�0��J2_A�ɇ�'�w�(٬�q��	�)IpS�(��*���X|��7B�g�E�6��2ڲӶ*�S5Boe�l�
���O� @��E]姯�r�H��/�y��� 5����<C��P<�%xK��0+E5���ln`�p�E-��6��d����Q�N����hd��.��H��� ک��8�����|xLx�Gp���,nv�"v�4��5��⚖���(V����������K�ƈo-/���.���h�p��Q�VQ|x=�N=7��ܐE�l�jꠂ4CKL��O��W��v�ELt��y+Dj�G�i<Û)�e�,���b���)=���K�<Oe��)�q�-��=�ħ[S�A�z<7Q��T�xJf��O�RN@rA�B�S�p�F�Z-�}�
i��K���E3�8=�b7i��42x��M3DHA���.ej���F�F�N�ձ<JX�ig�`EW Oy؊��c?���G{
��PK    ��8��V2  @    TokenFactory.classUT	 �AH^:HUx     �W|[�U��X����ؑ'J�TI��vl+?�MN���+�e�r�:i���D�*=%�ʠl�l�`����l�clˏ�v������U����[�u�6����{ߓe�Q���?��=��s��|Ϲ�=��ӗ�J��G.��E��e���T�G��35���Z�8>��8�ĹJ��'�r�5L��i5̨�OcV�3�\�e�?��Jç]�>���i��Ϫ��j�+'�����y��E'�����B������v������������5|���x�F�7����������%5|ǅ��?h��*|�S���I�?��T��x�
���h�W
����w
?T�~T�z�OÏ��z�e��B���xU��D�~�����?.�����+M�p�5��A��d�S�4q���I�K*ĩM�JM\.�]�jM�:�ƅq�UK�4q��S�rFDV��R��J��,�nw����v�
�=�#'#�x$9���Xr�MPݙJf�H�<��������@�s8�h����i0lu��g0u�H�D�TfR��ьa0&�i#*Xg�u��L�͔/�E_��EɌD��M;�hj��zR�q_$�N�h*��e>���Ē�̤���h�`߁@�&B�4�BM�]�����v0��G�<��YiI���u��'�5�w��^������`$*�C]�C�m��{0�9�uMVj�����C����<��p��K�'�!X��7���a��9W74^���IWjzbI#�K����H\�,c$�Sʯf�$]��x�����(�j�yQ�*vǒ1sq1N�Eñ�$Qa�R=�hI	�5\��+W�^����kGKA�85�f�a��W�:#iyٺ��9�06�8��x���$�c�LB�aC����o4��u�����4���<���
ܾ��1"	��?F67�T��H���o(q)�����s�S�L��S�_V�V%����
���0KW,�S�:ދ���e�.��[胨�1�>�T,k��0&[���.�0"�N]���N��N��r��H�y3�s�]6�&�c�%:rcc�:]�uC4���z�)�K7�z-��L�$!�%{�<�A�Ф�fuz�.-�Fp]�1��Ԏ��|w*sb�`}gA�X,YB���lj��&ÛK�<�)o�0�>ax'"�	���%��Z���O��x��n��?��-:���l��L��@�);��N]n�]�� �,G��21s�J�sщ��x��D��9Ac>��m5�����Ʋ�(9�F�icTy�mxP�I�b����Ӯ���x;��񈊅�3��0��3���^��oR�u�&>��.mr���n�A�c���.7�Z�=���v:�Fz�ɴ�M����6��f��'�Z�]�����a�V{S��MV�C�΀��[t�U�u�N�t���<��8e�.��e�`5>�孭[t�^�P���&s�Q��c�/�qvrL�	�YN�|.l�f����3ZydPǇ��.后��u�.e�+�8����]��N�S�ܥ�3��1��#,݋�z�Z�Ý����Y8�{�2���eTX*��o<id��[���vτi��>u�V0�
;��q��HK$��)I����ͭj��k�#u��,��f#��[N��Ù�$�=�46ʉ���*�y}��r�㺜�M��U�o���d|�����S��1�IKpq�*rV��q#��O�aݽ���`E���Za�����|��N>����Z�P����%
&��Ӳ-�H�2^�����ElȟKH�%�*��ƃ;&M��8�v,�d�T�,32T�����¦�?���2�$����1�s�"v�}oĮ��9@֕0��O+*���sMu��r��1�&� \�B[�nsI	�̪.�����v�<�K�>��I�k��PR@u^��x�odG�鲻&���I�ވDOf"�
�/���Eg��F��X�[\
�w�"��"υ��m���t$�����\,>j�S���b�8� 6Z�7��K�^�� ~
:����0���-����ӳ�:�W��q�
�n,�b�<+UV���9A[����-�-����Qd9h�6CV�^��,�T���]��U�4�z��}s0�0zc�x̮W��'��[ߘ������|�_3Q���X=��Q2��,�~��U�+6ndi��k��"�L��+T֪JW�d"��T��l*��`�%���-ȫ�XzBݧt�K����[���K�v����u���24��-~�fE9ִ #ވWᇐ/�����m�N�,D
�c_�L���L*͎��m���+u���������ٽ@�O�����T��/�*$�a#� �c�F�,�%$m�kI��;a5��;T�i�����T��F�Et��/�]��������{H����$��"z�w�h�ѷ`5�+�א��"�=�T_f���7���O8�Vq��69 ��_�W}�,*f����\�ǥ(�؋
�(�����E�.�9���,ʆ��1��MS�x�j��[x��B�r���T�Z����A�y,�E��4j�˦�n�B��Oa���fi)�XI�ѽ���蘁�f^�{/`�{���m�<�������5��^/�\wr�O�a����x��~܌j��,.`}���f��87��c䜀1��	ʤ(gx8�$��1�^�������Ä��̓�G�{�����/_e�+U��Z����ǆg�7��M����h��h���C}�5��=�cg�4�f�HM��Qi�Cz�B7�7�Y�9*q��t�}�zh�ꃨ�1ux���`%��-x�?νG
�oC���z����K`��^;�m��\�
.��'��
�nHS~I+�=d�ϣ�wLa�c�pv�5����]y ��~��5����<US��u��n���K����K�y	sq���Գ��-�p�\B�ګ�,��������PX[�US�겹j=��y!Sm�)`3-�,��2-����}���rP`�-���=z=oם갅��Lq��W,G��Pş]ug��RdW����𬠖�+���g��a�{��M}�!O�4����af�F(�W6y�~�U�U�{8~�u�cL���K(o�94�<��{�nL!�i�b�)�4��,A��}O���>Ek>���3x��Kx/��x��U|A*���K�
_�u��4�ق�
_�>|]��M���n|[��K�.|�hT�[,����F6_���i���R隷�he�m�:H�[$�P��y� T��aN�����`�;�/{��=��˛�<�e͗g�[��	U�n�Wx*MOa��<��)�;Io�8�pԯ��!���i�u��D
/.Q�
����(;���{����֨�F��a��3��>��O�OY����sJ�^c%z爐�D%���ƿϪQ�_^��*����p���S��p�q2���Ә�{��bg�!������-y��Yַbk��m||!�K\��*\':6J5Z�͊�ۤ�}�a¢�6>��)U>nj�\�]���BS����DSٶ&�6a��*%q����/Bk���K	;���*�҆u�)�С�
%nK�)�u�x��	��y�v}�`t��^�~�z���� PK    ��8�*��L  �  ! 
         ��    DoStartAuditComplianceJob$1.classUT �AHUx  PK    ��8.FjB�	  8   
         ���  DoStartAuditComplianceJob.classUT �AHUx  PK    ��8��V2  @   
         ���  TokenFactory.classUT �AHUx  PK        �    