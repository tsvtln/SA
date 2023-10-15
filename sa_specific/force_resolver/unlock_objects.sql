SET PAGESIZE;
SET LINESIZE 100;
SET FEEDBACK OFF;
SPOOL /usr/tmp/unlock_objects_worker.sql
SELECT 'EXEC LCREPPKG.BEGIN_TRANSACTION;'||CHR(10)||'UPDATE '||T.OWNER||'.'||T.TABLE_NAME||' SET CONFLICTING=''N'' WHERE CONFLICTING=''Y'';'||CHR(10)||'EXEC LCREPPKG.END\
_TRANSACTION;'||CHR(10)||'COMMIT;' FROM ALL_TABLES T, ALL_TAB_COLS C WHERE T.OWNER IN ('TRUTH','AAA') AND T.TABLE_NAME=C.TABLE_NAME AND T.OWNER=C.OWNER AND T.TABLE_NAME \
NOT LIKE '%_VW' AND C.COLUMN_NAME='CONFLICTING';
SPOOL OFF;
SET PAGESIZE 15000;
SET FEEDBACK ON;
@/usr/tmp/unlock_objects_worker.sql;
!rm /usr/tmp/unlock_objects_worker.sql;
EXIT;
