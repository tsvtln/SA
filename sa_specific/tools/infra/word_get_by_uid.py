import sys
sys.path.append("/opt/opsware/agent/pylibs")
from coglib import wordclient

src = wordclient.wordFileRequestByUnitId( 135560751L, None, typed_unit=1, compute_md5=1, checkonly=0 )
wordclient.urlRetrieve( src, "/tmp/l1" )
