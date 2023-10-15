import sys
import thread
import string

sys.path.append("/opt/opsware/pylibs")
sys.path.append("/cust/usr/blackshadow")

from coglib import urlopen

ctx_lock = thread.allocate_lock()
_ctx = None
_noSSL = 0

def _getCTX():
        if _noSSL:
                return None
        from coglib import certmaster
        ctx_lock.acquire()
        global _ctx
        if _ctx is None:
                _ctx = certmaster.getContextByName('spin','spin.srv','opsware-ca.crt')
        ctx_lock.release()
        return _ctx

def _readFromUrl(url_str, ctx, connect_timeout, read_timeout, write_timeout):
#        global gwcache
        if ctx:
                url_str = 'https://%s' % (url_str,)
        else:
                url_str = 'http://%s' % ( url_str, )
#        try:
#                return gwcache.get(url_str)
#        except KeyError, e:
#        try:
        (url_obj,headers)=urlopen.httpReply(urlopen.httpUrlRequest(url_str,ctx=ctx,connect_timeout=connect_timeout,read_timeout=read_timeout,write_timeout=write_timeout))
#        except:
#                _oopsText(url_str)
#                return []
        info_arr = None
        try:
                info_str = ''
                add_str = url_obj.read()
                while add_str:
                        info_str = info_str + add_str
                        add_str = url_obj.read()
                info_arr = string.split(info_str,'\n')
        finally:
                url_obj.close()
#        gwcache.put(url_str, info_arr)
        return info_arr



(cto, rto, wto) = (60, 60, 60)
(gw_node_name, gw_ip, gw_aport) = ("foobar", "localhost", 8085)

# Try to read full information from the gateway mesh
url_str = '%s:%s/linkTable' % (gw_ip, gw_aport)
lsdb = ""
#try:
lsdb = eval(_readFromUrl(url_str, _getCTX(), cto, rto, wto)[0])
sys.stdout.write( "%s\n" % lsdb )
#except:
#	sys.stdout.write("Unable to update GW conf from %s:%s\n" % (gw_ip, gw_aport))

