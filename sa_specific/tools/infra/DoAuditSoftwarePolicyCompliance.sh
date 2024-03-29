#!/bin/sh

##
# Program Overview:
#
# This program provides access to the OGSH under any SAS user with only a
# username.  It does this by generating a twist token for the user and using
# it to manually authenticate to the hub via the ".authenticate" special file.
# It then leverages the "ttlg" command to initiate the "normal" OGSH session.
# A twist token is an encrypted string of XML that contains a username, 
# userid, and other timing and type related information.  The token is 
# encrypted with a key that is generated from a deterministic psuedo random 
# number generator that is seeded with the twist's private key, 
# "twist-key.pem".  This RNG is implemented in java, so this script has an 
# embedded token generation  class that is emitted at runtime to "/tmp" and 
# executed with the local java interpreter.
#
# Currently, this script depends on the spin, via local spinwrapper libraries,
# to lookup the userid of the given username.  This dependency could be 
# removed by having this script accept the userid on the command line.
#
# Also, at the end of this script there is a note about how to obtain an OGSH
# session for a user despite the user lacking the "launchGlobalShell"
# permission.  This mechanism also bypasses OGSH auditing.
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

# Extract all arguments past the first as the command.
sCmd="`echo "$@"\  | perl -pe 's/^[^\s]+ //'`"

# Locate twist private key.
EINSTEIN_KEY_PATH="/var/opt/opsware/crypto/twist/twist-key.pem"
DARWIN_KEY_PATH="/var/lc/crypto/twist/twist-key.pem"
if ( [ -f "$EINSTEIN_KEY_PATH" ]; ) then {
  sKeyPath="$EINSTEIN_KEY_PATH"
} elif ( [ -f "$DARWIN_KEY_PATH" ]; ) then {
  sKeyPath="$DARWIN_KEY_PATH"
} else {
  echo $0: Could not locate twist private key on this system.
  exit 1
} fi

# Locate the python interpreter.
EINSTEIN_PYTHON_BIN="/opt/opsware/bin/python"
DARWIN_PYTHON_BIN="/lc/bin/python"
if ( [ -f "$EINSTEIN_PYTHON_BIN" ]; ) then {
  sPythonCmd="env PYTHONPATH=/opt/opsware/pylibs $EINSTEIN_PYTHON_BIN"
  sOgshEnvPath="/bin:/usr/bin:/usr/local/bin:/usr/sbin:/opt/opsware/ogfs/bin"
  sTtlgCmd="/opt/opsware/ogfs/bin/ttlg"
} elif ( [ -f "$DARWIN_PYTHON_BIN" ]; ) then {
  sPythonCmd="env PYTHONPATH=/lc/blackshadow $DARWIN_PYTHON_BIN"
  sOgshEnvPath="/bin:/usr/bin:/usr/local/bin:/usr/sbin:/opt/OPSWogfs/bin"
  sTtlgCmd="/opt/OPSWogfs/bin/ttlg"
} else {
  echo $0: Could not locate the opsware python interpreter on this system.
  exit 1
} fi

# Locate the java interpreter and required libraries.
# Locate the java interpreter and required libraries.
if ( [ -f "/opt/opsware/twist/lib/client/twistclient.jar" ]; ) then {
  sJavaCmd="/opt/opsware/j2sdk1.4/bin/java -classpath $0:/opt/opsware/twist/lib/client/twistclient.jar:/opt/opsware/twist/lib/twist.jar:/opt/opsware/twist/lib/common-latest.jar"
} elif ( [ -f "/cust/twist/lib/client/twistclient.jar" ]; ) then {
  sJavaCmd="/opt/opsware/j2sdk1.4/bin/java -classpath $0:/cust/twist/lib/client/twistclient.jar:/cust/twist/lib/twist.jar:/cust/twist/lib/common-latest.jar:/cust/twist/lib/commons-codec-1.3.jar"
} else {
  echo $0: Could not locate dependent twist jar libraries for the token generation step.
  exit 1
} fi

# Locate the openssl binary.
EINSTEIN_OPENSSL_BIN="/opt/opsware/bin/openssl"
DARWIN_OPENSSL_BIN="/lc/bin/openssl"
if ( [ -f "$EINSTEIN_OPENSSL_BIN" ]; ) then {
  sOpenSslCmd="$EINSTEIN_OPENSSL_BIN"
} elif ( [ -f "$DARWIN_OPENSSL_BIN" ]; ) then {
  sOpenSslCmd="$DARWIN_OPENSSL_BIN"
} elif ( [ -f "`which openssl`" ]; ) then {
  sOpenSslCmd="`which openssl`"
} else {
  echo $0: Could not locate an openssl binary on this system.
  exit 1
} fi

# Attempt to locate the user id of this user from the spin.
nUserID=`$sPythonCmd -c "from coglib import spinwrapper;import string;import sys;sys.stdout.write(string.replace(str(spinwrapper.SpinWrapper()._AAAAaaUser.getList(name='$sUserName')[0][0]),'L',''))"`

# If no user id was found.
if ( [ \! "$nUserID" ]; ) then {
  echo $0: "'"$sUserName"'": Could not locate the userid of this user from the spin.
  exit 1
} fi

# Attempt to generate a token for this user/userid.
sToken=`$sJavaCmd TokenFactory $sUserName $nUserID $sKeyPath`

# If token failed to be generated.
if ( [ \! "$sToken" ]; ) then {
  echo $0: Failed to generate token for username="'"$sUserName"'"/userid="'"$nUserID"'".
  exit 1
} fi

/opt/opsware/bin/python -c 'import sys;sys.path.append("/opt/opsware/pylibs");sys.path.append("/opt/opsware");from waybot.base import twistaccess;ta=twistaccess.getTwistServiceForIp("127.0.0.1");print ta.auditSoftwarePolicyCompliance(token=sys.argv[2], device=sys.argv[1], updateCompliance=1, fail=0)' $sDvcId $sToken

exit 0
PK    k�8/X�2  @    TokenFactory.classUT	 t��Gt��GUx �-'�W|[Wu��X����ؑ'JB��Mb;���
�iZ�Pb%��ZNR'mY~��X?*=%1[���]����c[�����]�����+0+۠�(ۀm��A��}O�eGi������s�=���9��g_}�
�IT`����]8��?q�Qßj����sCS��'ܸ�\8_���nT㒆)��VÌ.��f5<���5\q���J��4|ڍ��j����p�/�>���r�Y
_pc�S�_t�KʸKn�qɅ/�рK��W��W5<�F�s��B%������7��h��2�[�V÷��;�������
�X���{jxI�?i�g5��J|/U�e��
���ߔ����Jُ�_��4�؅�p�[Y��n��_ʈW��O��j�o
�����j����7^�kj�I���L�������).5h�Th�vK��Ti��%�n�I�ZZ���{H��3"��~�:MV�d�`iW[�k��{oh��G��>=�OD�c����'�ZU�d֌&��щ�A:2���u�����??
�#m� uw�N�}ј��L*5Y#�1̃�d$m�뭽��c�ɴ��g���(��hָyg0K�A}w*3揦��q�K%�̯�����d43�o�(Z>�{0�I�"��p[Mr�i���޾��5�
\����P/9+,���>���u�:�����+�6q(<�¡����-ܩ8�����}��\�d����?t�m 8t088��6�ŝ8���R����P��U}Qpϡ�fd�su}õyt���;�4¹İ��O��e��qZ�Ռ�����\T�B�Z
5/
�sO<7�c��P4K�)Us����x���z���K\�v����31#m�v����~%��5��������`S�}K�W��h2;��$�6tO��GR	g*�KI�5�3�	�۟53F4���odsf�
�#���u�%��k{b���#�\&f싫�/+�k���^������0KW<�W�:ލ���d�.k�M�A�ȘY�y:�5�O�-i�����Qf�.����tY/t�Qn�𼙅ȹd�.�d3ϱ���QC�̺1��M���)�G7��,|�L�!�%{ܫ^�Ш��{�.ͲF�����mj{F�+�99�/��Q�=O���y͛�|�qB���*�|fʗ5����hv�&�Fsɘ:�.-��� ��8D�ڶ�����d��e�.�eӮ-q�N��K��e�.o���(���Lܜ�S�\l�mb,Er<Q�!��(���kT��ų�(9�E�icDy�-���S8� ���]_
��Vܫ�aOG476n��)f��|�ޠ~��M��%]Z�&�=:΀��G}]n�,{����mt.����i×�1��m*��ZO���:Y�C�CV���2�/Y��:��;�ܪ�mҦK�t��S����v��%�u钐.� ��).ok٪K������\4�������>���S���KD�r��s9`������י��#:>��u9$�u�>��w��\��%GP��eP��rL�t�]j�n�!]���e�^�Hֵ������Q��a團.#���d0"<�u	O9&�D۽㦙��YZl��(��N�o�E���TNI�N��NnU����3�yf9!�q(3�bp����d4a쵧�N��R���w����l�eB%���hƟJ��Ϟ�f�9LZ��KW��z�O1e|���Ɣ�+Jx�W�q�����I��x}�EM:jy}���
�(�T��˶P"��Xxq���d�1�/!e��k܂7n�4
Z�o8־ �YS���P����>
�6��ͮ�D��n����.̭��m���f�� Y[�>��	�6�k����W/��51�Y�R�zm�KJ�WVuQ\^�]��]P�X����L�^�_s����R׮�Wz=;�M��5Y=Tu��F4vr UmX]��7:�n7�<�J��Z �'��.B�\����,MG3̱l�i��'F�rj��l�ĦB��Ʋt��^*�_�����L�us�l���d���,�����e��M7��z�l��*+����-VGX�f�IZK�(��0Θa�U/�KK*^J�,�ƌ*a{=�ݾ9O=񉉸]�0N���Q�����d�f�*T��2z��d��Y�#�*|g|��Ұmב�DT��;U֪JW�d���T��l,��P�%���.ȫ�xz\��t�K����[���K�v����u�P�geh��[|�͊r�qAF���!_�W�K�:�k�5���93�3�2�4;~Z�������W��?�[�Kg��?}��v�R9F�ܪ�X�MHX�U����`��YD�#�+���s�Pͧ�d_˧�T��J�mEt��/ѝ��������{I���� ��"z?�w�i�ѷb5�/�א��"�]�ԗ�n��a=�	�g%*T�M���j�S��.@��sK89��oq\�2�=p"L�>����������Ϣl��(?�8磨R+���#�m� ��p�4�͠2�<��,�z.`�,��Q�Y6O�j��|
+<u6Ks�Jrp+��UlF��6�2�w�=kf���i���Y7��԰�z}�s�E�Y�/����rv�y:�Fp�x�s��
y�����t�0<�a-F�9?�؅��IQj��M���S
�	���w24\�'�"�#`� H>·���"�$A�E�v�j^�a�I��o�l|F�wM�|I/����{P�`;ԗq^�=|�t�j�F}�,����0*MtHw�C�&ϖ�C8k9O%Ԣ����@|��ܠ����Q�}+�lo�#4�1�{���v�[H�����l�vΞu��~	;��ඌ|+�a���4嗴P�K����g�v=
/g7[�j��ٝ��p{�SxK��[9�@@����س�*��[���ڋK�KI�z�-�e��wUޥ��nsu�\��j
k��\�6W��ƫ7-d�)0m�e�e^}�B�e6S����B����
�<^�W����B�Ǟ)��:�r�|�|�=w���k�堭e�w��^�e�=�E7���k��z��;�>/3�vB!�������򮚇�C��񣬳c2|>By#Σ	����KHwa
Lc3L��XUg	ҧ	�+x��'�)Z�i|���,^�3x	���x��R��_�U����W���V� ������2�o�0�%���r/^�w�;D���bᕟ6�����೺qKSs������h��q�H�[$�P��y� T��bN�=��
7�`8��xW�?�ʛʼ�eMWf�[����pz���'�c
�^��|
G.�[��)h��s���kw�+.QC�KT��:봲6F�Υe;��>�|�5��Q?dX~�����+�O?���SV���������WY�^�۩�~Q��!��>��j8��Q���
8�ϰ'6�N�('��2��@���O!~Ë�o.�ߜ7��e}����������ōZ��ZѱI��"V���.�8(5�e���|xGI��qs���vY8�/���/����e�ۅY�?UJ&X�hr�����:8e%�vY�U�
�K6�C�J���UZ�Iq+�*^7�z������}\��uY���PK    k�8/X�2  @   
         ��    TokenFactory.classUT t��GUx  PK      M   w    