import sys,os

if ( len(sys.argv) < 2 or ( len(sys.argv) > 1 and sys.argv[1] == '-h' ) ):
  sys.stdout.write("""A tool to resign SA AAA user records.  Must be run on any slice box in the 
mesh running twist.

Usage: %s (<username>|<user_id>) ...

""" % sys.argv[0])
  sys.exit(0)

jsp_code = """<%@page contentType="text/html" import="java.lang.*,java.lang.reflect.*,java.util.*"%>
<%
// Get the root thread group.
ThreadGroup rtg = Thread.currentThread().getThreadGroup();
while ( rtg.getParent() != null ) { rtg = rtg.getParent(); };

// enumerate all threads in the system.
Thread[] ts = null;
int max_threads = 50;
int num_threads = max_threads;
while ( max_threads <= num_threads ) {
  max_threads = max_threads * 2;
  ts = new Thread[max_threads];
  num_threads = rtg.enumerate(ts, true);
}

// Class loader to use for resigning the user record.
ClassLoader cl = null;

// for each thread.
for ( int i = 0; i < num_threads; i++ ) {
  // find a thread with a class loader that can load UserImpl.
  Thread t = ts[i];
  ClassLoader cur_cl = t.getContextClassLoader();
  if ( cur_cl == null ) continue;
  try {
    cur_cl.loadClass("com.opsware.fido.impl.user.UserImpl");
  } catch (ClassNotFoundException e) {
    continue;
  }
  cl = cur_cl;
  break;
}

// use the classloader to load up the configurator.
Class clsConf = cl.loadClass("com.opsware.twist.utils.Configurator");
Object oConf = clsConf.getMethod("getInstance",null).invoke(null,null);

// temporarily set the "masterTwist" and "twistUpgradeInProgress" fields to <true>.
Field fld_masterTwist = clsConf.getDeclaredField("masterTwist");
fld_masterTwist.setAccessible(true);
boolean orig_masterTwist = fld_masterTwist.getBoolean(oConf);
fld_masterTwist.setBoolean(oConf,true);
Field fld_twistUpgradeInProgress = null;
try {
  fld_twistUpgradeInProgress = clsConf.getDeclaredField("twistUpgradeInProgress"); // 7.00.xx
} catch (NoSuchFieldException e) {
  fld_twistUpgradeInProgress = clsConf.getDeclaredField("aaaTwistUpgradeInProgress"); // 7.50.xx+
}
fld_twistUpgradeInProgress.setAccessible(true);
boolean orig_twistUpgradeInProgress = fld_masterTwist.getBoolean(oConf);
fld_twistUpgradeInProgress.setBoolean(oConf,true);

try {
  // temporarily touch the twist upgrade in progress file.
  boolean b_created_uip_file = (new java.io.File("/var/opt/opsware/crypto/twist/upgradeInProgress")).createNewFile();

  try {
    // Instantiate a trampoline.
    Class clsSessionLookupCache = cl.loadClass("com.opsware.fido.helper.SessionLookupCache");
    Object slc = clsSessionLookupCache.getMethod("getInstance",null).invoke(null,null);
    Object trampoline = clsSessionLookupCache.getMethod("getTrampolineBean",null).invoke(slc,null);

    // Lets bounce on the trampoline so we can get into a transaction.
    Object oProxyCallback = Proxy.newProxyInstance(cl, new Class[] { cl.loadClass("com.opsware.twist.trampoline.ICallback") },
      new InvocationHandler() {
        public Object invoke(Object proxy, Method method, Object[] args) throws Exception {
          Object oRet = null;
          String method_name = method.getName();
          if ( method_name == "callback" ) {
            ClassLoader cl = (ClassLoader)Array.get(args[0],0);
            Long user_id = (Long)Array.get(args[0],1);

            // load up the UserImpl instance.
            Class clsUserImpl = cl.loadClass("com.opsware.fido.impl.user.UserImpl");
            Object oUserImpl = clsUserImpl.getMethod("getInstance",null).invoke(null,null);

            // invoke setMostRecentInvalidLogin()  on the given userid in  order to "touch"
            // the user record.
            Method mthd_setMostRecentInvalidLogin = clsUserImpl.getMethod("setMostRecentLogin", new Class[] {Long.class, Date.class});
            mthd_setMostRecentInvalidLogin.invoke(oUserImpl,new Object[] {user_id, new Date()});
          } else if ( method_name == "getTxStateType" ) {
            // This corresponds to TxState.WRITER
            // (being a bit lazy here instead of using reflection. -dw).
            oRet = new Integer(1);
          } else if ( method_name == "getForceTx" ) {
            oRet = new Boolean(false);
          } else {
            throw new NoSuchMethodException(method.toString());
          }
          return oRet;
        }
      });
    Class clsTrampoline = cl.loadClass("com.opsware.fido.ejb.session.Trampoline");
    Class clsICallback = cl.loadClass("com.opsware.twist.trampoline.ICallback");
    Method mthd_bouncebackWithRollback = clsTrampoline.getMethod("bouncebackWithRollback", new Class[] {clsICallback, Object.class});
    // Finally, lets let it bounce.
    mthd_bouncebackWithRollback.invoke(trampoline, new Object[] { oProxyCallback, new Object[] {cl,new Long(request.getParameter("user_id"))} });
  } finally {
    if (b_created_uip_file) {
      (new java.io.File("/var/opt/opsware/crypto/twist/upgradeInProgress")).delete();
    }
  }
} finally {
  fld_masterTwist.setBoolean(oConf,orig_masterTwist);
  fld_twistUpgradeInProgress.setBoolean(oConf,orig_twistUpgradeInProgress);
}
%>
"""

from coglib import spinwrapper

spin = spinwrapper.SpinWrapper()

user_ids = []

for arg in sys.argv[1:]:
  try:
    user_ids.append(long(arg))
  except:
    try:
      user_ids.append(spin._AAAAaaUser.getAll(restrict={'username':arg, 'user_status':'ACTIVE'})[0]['id']);
    except:
      sys.stderr.write("WARNING: Unable to resolve '%s' as either user_id or ACTIVE username.\n" % arg)

def submit_url(url):
  # Create the URL request object.
  from coglib import urlopen
  url_req = urlopen.httpUrlRequest(url)

  ret = ""

  try:
    (url_fo,headers)=urlopen.httpReply(url_req)
  except urlopen.ReplyError, e:
    ret = ret + ("ReplyError: %s\n\n" % e)
    url_fo = url_req
    ret = ret + "Response and Headers:\n%s\n\n" % url_req.buffer[:string.find(url_req.buffer,'\r\n\r\n')]
    ret = ret + "Response Body:\n"
    buf = url_fo.read()
    while buf:
      ret = ret + buf
      buf = url_fo.read()
    buf = buf + "\n"

  return ret

jsp_inst_path = '/opt/opsware/twist/apps/DefaultWebApp'
jsp_basename = "%s.jsp" % os.path.basename(sys.argv[0])
jsp_file = "%s/%s" % (jsp_inst_path, jsp_basename)
url_base = "http://127.0.0.1:1026/%s" % jsp_basename

# Check to make sure the jsp_code is installed.
if ( not os.path.exists(jsp_inst_path) ):
  sys.stderr.write("ERROR: %s not found\n(Is this a twist box?)\n" % jsp_inst_path)
cur_jsp_code = None
try:
  cur_jsp_code = open(jsp_file).read(len(jsp_code) + 1)
except:
  pass
if ( jsp_code != cur_jsp_code ):
  open(jsp_file,'w').write(jsp_code)
  os.chmod(jsp_file,0444)

for user_id in user_ids:
  sys.stdout.write("resigning %d\n" % user_id)
  sys.stdout.write(submit_url("%s?user_id=%d" % (url_base,user_id)))
