// To build:
// export CLASSPATH=/opt/opsware/da/webapps/arm/WEB-INF/classes:`echo /opt/opsware/da/webapps/arm/WEB-INF/lib/*.jar | perl -pe 's/ /:/g'`:.
// /opt/opsware/jdk1.6/bin/javac da_sapassword.java

// To Execute:
// /opt/opsware/jdk1.6/bin/java da_sapassword [<new_password>]

import org.hibernate.Session;
import com.hp.arm.dao.GlobalConfigurationDAO;
import com.hp.arm.persist.entity.GlobalConfiguration;
import com.hp.arm.persist.util.HibernateUtil;
import com.hp.arm.persist.util.Wrapped;
import com.hp.arm.persist.util.TransactionWrapper;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class da_sapassword {
    static public void main(String[] asArgs) {
        String a_new_pass = null;
        if ( asArgs.length > 0 ) {
	    a_new_pass = asArgs[0];
	}
	final String new_pass = a_new_pass;
	Logger LOG = LoggerFactory.getLogger(da_sapassword.class);
	TransactionWrapper wrapper = new TransactionWrapper(LOG);

	wrapper.wrap(new Wrapped() {
		public Object doWork(Session session) {
		    try {
			//Session session = HibernateUtil.getSessionFactory().getCurrentSession();
			GlobalConfiguration gc = (GlobalConfiguration)new GlobalConfigurationDAO().list(session).get(0);
			System.out.println("current password: " + gc.getSa().getPassword());
			//System.out.println("lockversion: " + gc.getLockVersion());
			if ( new_pass != null ) {
			    System.out.println("Changing password to: " + new_pass);
			    gc.getSa().setPassword(new_pass);
			    //gc.setLockVersion(0);
			    session.save(gc);
			}
		    } catch (Exception e) {
			System.out.println("Caught Exception:");
			e.printStackTrace();
		    }
		    return null;
		}
	    });
    }
}
