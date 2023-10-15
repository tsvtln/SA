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
x��;kW�Hv�Mfw�s�%��o�b9�3F`�ݻ�`n`�L3�GG�ʶY2*��=�'2?(��C*Ɇf'�3��Tu���}T�����u���
"g�����ׄ����ɢ u\�K����;�xN����n￵���q�߾��`2���ĬAX�ш�ͼ�AR�L�zQ�{���3�52v�;2�2]��8"M���@f4a��C5��c7%��	<�$�a�������ˏ��E�8��M��RD�ʬ�z� ��
&�a�2cOC7F&
b�A�=��Nv�F�(&�W��|��d4�*�aB��_A�����뗯���aeq�&�*����b>� �����\(��)����A��UW��v��\XRi���B<���Y4��j�qMα�iY�d�4��zcs
Rs�_��9Z���i�HL���1�i�D� ��e$�s2�Mk�'�$�����梲0�:C�m
���r�� 	L6v@B�x ��G �c��1�r4 o)I�@	���ӲDW���H�r.��\�,zR��kN����2�K}h���_k�F�zfϓ ����<36�!M�
Bh��o�P�U��9B��A�MF�sG�X��D��!تL`�>���~T��P���1*y�Ժ�}��`�������`B�����R�t�9!K��e���Cr@�@�
��j�5������n�����)>5���7g�e�������-xl��mx��w�D����/a���A�m��M����m����%Z�a[6l�_$5��9�/�+rB:�2�x�� "e�l0�	��t����A��P"�j�oH���.X�]f3�7��5�ΝbPr�8a�������A�B��1�9�l)���rq3s"�����03�@vH����[t򪻳�]Ű[�h>��5$ufx!�br¥@.M�/D����y���K"wBmBzS�as��=`mtM��8�8u�C3W�`��X��C4��NDG�B:b:�\S�K����������b����4&"�sx�Pt�B��fy��Μ��C���wb�#�0�A��L�� J-`�I�#�Z��� �a^�]YO⾕H��� �V�4�!�)�iȹb4����ҍ�I��Bd�(d�;&�+�
�I�掠0�G=���W:�պS�`�Z_�=>i�������<D�I�4���]���(�j���pa{�+�SҪ�����6t���Z�����a�N���q߀K���Ʌ�7m�Jb�3�C�$�*�A,HΩ����u&���^�l׻ς�[e���%�T���ʩŊ~�c]��I�qm�K�%�̱>����Y�i��v��
B�=/�0�	��
^B�/�eJk`�9��ˀB��Ռ�ˡx�������qBC(�
�����+��RW.Pn~��yƠ��n=f��0~�۫��Q�YD.SBAp4�ġ�k=_�����b���o������|��f��X^����Mr����lrM1�_#�*ܱ�&�6@�H�E:np���:�4o��� �|���2�5H�8+�]�g�XϠ��t�6��?Ý��i�ú�G����.���Ř�H�07^��M�>�)�O/�1gp�S
���OS���f�&��#eQ
)�L>�x��;�8b.&�-���a�ɻ�%+n�#Z��́\�2���N����)
� ��:y<V�1�_m`�s� ���iJg]�����Io)��	Zq�:�g��"wzr��z����
�(d �5Z��9��"��=A	�@�F�"tyv�7em�D�w~�V���ͽ�����0<��9K\/ļ�o�x�]�a��^�F��|��rX����D?�v=8fC�/;`a4�p�ۆ���� 0�;�gR ���O�M=c�C�B���ɒ�/Ķm�#�( �J(Qv8�Q��<��,�3yX�y�7�g�߸����H<�2@y҇x:͒)n��v#:&���J�x�G�L`/@b�d?�7{��y� �a��1�
^ 	9��(�� �D�� ��1�zrc-��P�Q:/8��U��${P�	�m?^<�4H����j�'Ux[!f�(�;"��td4^�H�
C�,?�ad*��9nf	��M�^���dIT$��M[vZ\���A
u H�2�mW�4��*X8C����!a�s_���A6��z��&���W�lS��Z����E��}�Q�<>���"�374�*4�-HD6��7�Zu��%��b�*L� ����c�0��u4�ܸ*�h�P�V�r(���n��P5��X,KQT�8�N�*����eiH�(�
Л:�%NV�w���c�7�߲/��'RÔ3R��b�˧�\W��k�X�1�
g��lF>.[��b
�3�)��qt+��TX^��y��	s�!��vO�������oBbn���W6�9�*_�dI)��F�M(	p���8���\g�-jC��1� W&���!P�y����D!�u������g)tT�kCL��1��{_�M��"=�f������D c�N�3 ���F�
Pf�����ܢ�[��Tu��a�� H�Y��!�,�01��'�)�3�e#�*tp�U����\�$�J�P&�OȞo�N(#C��!��G;b���V�i���A���{��0LV���������A�O
�Ց�N���?~߫	9�0)ʹ�e��� ��w�(p;�R �
�Gt�^���3��.�BU�̶�n�b�&\�Ӻ�R�5��`�̐C�B�"C��}� ��ZŮ�o/�9S͂7��3F��
3j,���$�C���
j�����qi$޼A$�����\Ӽ� �]��IA��shA�����U��;�+�l�$�r5�|���ܻ�;-բ��;-*�m����[J��硜�*�E�.���4��A+\�N���j:T���ܠ�V���-����Y4��TV�*���A�7"���]|�dE�H� �A�!�#D�d�c�
W�œI�r��.HzP�!<_
yd��,;.�A�
4�JH��@�t�
��#����I@W
~G�Cw������j�!�T�v�<Î��+-�<�e��-�|
��K_�"6�V��?V[/d��]���y��w<�H&�l���J;���j�ʓ�s%c����]5� f�m����`Ǯ̣E���8��U�u��^�<�㄂<;��Z���f0l
S0N$RRJ�@�sv��(/�4Vܴ����?:�<`9X�²�&@F
	�<��.z
�iЄ,@�Z8X��r�D)O��:~�����Y�#C˶�l��OO�%�Qdd`cܼub�d�
��+~��ʷ�W���)��	_����|IT�W/>�k��,I`H� g��	˙L6$ax�,L�)8��}F�Ĉb���ÊAy�(H������V�U�$d5�_�����<��t���ħ�����0�ē��_��
��y���=�{gb��\B� �P��d��M�~*���@��,e/�K���W:�����pya�A��y2eY� �j�(�՟y@>�q��*<��C�4%WZ��7��
�K{W��
���w��-2�F%'�� �����qo<��[vI����xd�!�ϕ$l��s�O�>

���w<?5�I+'T<>�.y魝���D\"�Ƀ����ØUW(����-�f��R_���boN� B�La0`�AlO�En
�ߗŁ��)���bJ�j�� o�1wD���x�
�
q���5�z��줱x��_��(K�0Hd�aΏ��8�Ru=Y�}���� ��_�G�+]������,q?��e�TzT�yu������D@Hq}���rLqg"3�R/���4�`^B�.�l"�Wnr]	:��Ş��<`ǸEe"!�w"-�ī�L
#�#Ȍ1,�Y�~�FLmBY�(W�}�SRo����F���"k�k�� �(��r�Z�|\
挐"��$Es$�ؕj}�
�F��tC��|4�r�*y�<��>�A������ቬ��e���
|l/Cَ��rP���rʢj+ܚ&J��F>
5~s��u���5�?L>���_%�(��u0�;��n�y(����
��UŔ7q�%�e2�)gŭ<~m�7��ũjm���o`K'v�a��(M��@�=�T�\Ahg�ޞ;��§"��� ���}�p�yM$0ѨUA�d`_��K��u��dxW��b���L�1��H-�!����*����*��e��D��Ia4��D��zA*ثbhD�0,^a���?�:ٿ蝃r#���7���u�Ğer���^�����_tO/q���Ԕ["��;�>O�C������/F��C+��O��*ArYz?�@�	�]��M�PnFsg��Ͳ�&�I�O�>K&������8�%A��O>2��s1��Ŵ��*6�pS��E�\���3J>A��SyƩ��1O�����E
�LP�O!���J] @��u�;?�3��Ϧ??��u~��G�%�Q�T��v:M�M������ZRcs�b���1�{��&��ֲ�B���B:�/�q�͏����,k� &�8�DJ�Uc�����Q/5�01�GAd���0�w/Ŧ���uh~Xh���}NP�S��ZϽ���ze�uC^.4}���R07$��o�P�c(*��4�ק��a� ���B�G�C����
�|	
%�>�ʅv#��!
]Z��9B(<���YN@:������u=G�����Wd(��k2uf�s� �)p��9��Rze@iƮO���w��?�>��G�g��GHP�2����@r[�Q�3��^� �����뽝��x1�^��/��؝_A��{4�.w��W[�A��o��k���o�O>o�n����b�q�v������?
�Z/϶�⽻{���䧇ׯϚݣ���ػ��O����u���/?���Mw�t�u��^}x�����]����|�}�۾t��Ot�?��g�?h^?\�[����ͫ�w��������ٻ������������Q0������O[��?��׋ŏ�W�ϻ�ūO/�ׯ~��թU4���&U������^�'���f<
Bja��S|�<�Y�����
ǈn��
��m6L4
h��}=2P��q�?�nO}ش|MpSBA��X{w�F�(?şSQ6�.DW���`n� ~���ue�+��N�`��\v]��H:и�AHoڭmq���� X_^�j�����	�YXʬ���� O(9�V�Ѓ����p/k�ІZ�]�;���]������9ﺇ����Qo�m� �E,A�j�W���S�Y3�#��'�ƶGtQSiAE�xE$��j*���o�#�!��������w�G���J�1�����Z�Ԫ�=�oH�UP�Db������z魶����݂*.RI�O��o ؆�>)�=b@�^zc�F�V�d��L���,��(�#D��Uly��+���k������c@��c ��0y�<S������`7���Z����h����MaS"��k�}�ڰ[}�څ)I\,�a)�S~�8�a��ȩP��E�
������/@P�t.,5
\�YD��S�g��&O�:�|XR�!s1e%F�F�.�����ݸ����?�&�L  