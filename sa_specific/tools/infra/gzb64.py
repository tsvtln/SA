import sys
import string
import base64
import gzip

if __name__=='__main__':
    if ( len(sys.argv) < 2 ):
        sys.stderr.write( "Usage: %s <file>\n" % sys.argv[0] )
        sys.exit(1)

    f = open( sys.argv[1], "r" )

    n = -1
    s = ""
    while ( n != 0 ):
        r = f.read( 4096 )
        s = s + r
        n = len(r)

    b64 = base64.encodestring( gzip.zlib.compress( s, 9 ) )

    sys.stdout.write( string.replace(b64, "\n", "") + "\n" )