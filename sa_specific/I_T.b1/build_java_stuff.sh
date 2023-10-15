#!/bin/sh

spin_db_password="`/opt/opsware/bin/python -c 'import sys,os;os.chdir(\"/opt/opsware/spin\");sys.path.append(\"/opt/opsware/pylibs\");import spinconf;spinconf.initLocal();sys.stdout.write(spinconf.get(\"spin.db.password\"))'`"

table_id_fetcher_java="TableIdFetcher.java"

if { [ "$spin_db_password" ]; } then {
  perl -pi -e 's/("spin",")[^"]*(")/\1'"$spin_db_password"'\2/g' "$table_id_fetcher_java"
  echo "Patched $table_id_fetcher_java"
} else {
  echo "Unable to obtain spin password."
} fi

CLASSPATH=".:`echo /opt/opsware/oracle_instantclient/instantclient*/lib/classes12.jar | head -1`"
export CLASSPATH

echo "Compiling $table_id_fetcher_java"

`echo /opt/opsware/*/bin/javac | head -1` "$table_id_fetcher_java"

echo "Done"
