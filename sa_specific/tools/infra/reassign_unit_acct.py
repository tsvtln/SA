
# ./py_build pylibs/io.py pylibs/loglib.py pylibs/dblib.py reassign_unit_acct.py

import sys,string,types
import io,dblib

def usage():
  io.out("""Usage: %s <from_acct> [<to_acct>]

  This utility will reassign the account of all units currently directly
  assigned to the account <from_acct> to the account given by <to_acct>.  If
  <to_acct> is not given, then the account "UNKNOWN" is used.  These accounts
  can be specified using either the account ID, name, or display name.

  This is useful when attempting to delete a customer and it is assigned to
  many packages.

""" % sys.argv[0])


def resolve_acct_arg(cur, acct_arg):
  """Returns a list of tuples, [(<acct_id>, <acct_name>, <display_name>) ...], for 
an account given by <acct_arg> which can be either the account ID, name, or display
name.
"""
  try:
    acct_arg = long(acct_arg)
  except:
    pass
  if ( type(acct_arg) == types.LongType ):
    cur.execute("select acct_id, acct_name, display_name from accounts where acct_id=:1", (acct_arg,))
  else:
    acct_arg = string.replace(acct_arg, "%", "\\%")
    acct_arg = string.replace(acct_arg, "*", "%")
    cur.execute("select acct_id, acct_name, display_name from accounts where lower(acct_name) like lower(:1) or lower(display_name) like lower(:1)", (acct_arg,))
  return cur.fetchall()

def main(argv):
  if ( (len(argv) == 0) or (len(argv) > 2) ):
    usage()
    sys.exit(1)

  from_acct_arg = argv[0]
  to_acct_arg = "UNKNOWN"

  if ( len(argv) > 1 ):
    to_acct_arg = argv[1]

  dblib.init()
  cur = dblib.get_cursor()

  from_acct_recs = resolve_acct_arg(cur, from_acct_arg)
  if ( len(from_acct_recs) == 0 ):
    io.err("%s: No matching account found.\n" % from_acct_arg)
    sys.exit(1)
  from_acct_rec = from_acct_recs[0]

  to_acct_recs = resolve_acct_arg(cur, to_acct_arg)
  if ( len(to_acct_recs) == 0 ):
    io.err("%s: No matching account found.\n" % to_acct_arg)
    sys.exit(1)
  to_acct_rec = to_acct_recs[0]

  # Begin a LCREP transaction.
  cur.callproc("LCREPPKG.BEGIN_TRANSACTION")

  # Grab the transaction id.
  cur.execute("select LCREPPKG.currentTransactionId from dual")
  tran_id = cur.fetchall()[0][0]

  # Execute the reassignment.
  cur.execute("update units set acct_id = :1 where acct_id = :2", (to_acct_rec[0], from_acct_rec[0]))

  # If record where updated.
  if ( cur.rowcount > 0 ):
    # Let the user know what have just done.
    io.out("Transcation %d has been prepared to reassign %d package%sfrom account \"%s\"(%s\\%d) to account \"%s\"(%s\\%d).\n" % (tran_id, cur.rowcount, (cur.rowcount==1 and " " or "s "), from_acct_rec[2], from_acct_rec[1], from_acct_rec[0], to_acct_rec[2], to_acct_rec[1], to_acct_rec[0]))

    # Ask the user if they would like to commit this transcation.
    io.out("Do you wish to commit this transaction? (y/n)\n")
    answer = sys.stdin.readline()[0]
    if ( answer in "Yy" ):
      io.out("Committing transaction %d.\n" % tran_id)
      io.out("(Note: This transaction ID can be used later to reverse this operation if so desired.)\n")
      cur.callproc("LCREPPKG.END_TRANSACTION")
      cur.execute("commit")
    else:
      io.out("Cancelling reassignment.\n")
      cur.execute("rollback")
  else:
    io.out("No unit records currently assigned to account \"%s\"(%s\\%d).\n" % (from_acct_rec[2], from_acct_rec[1], from_acct_rec[0]))
    cur.execute("rollback")

if ( __name__ == "__main__" ):
  main(sys.argv[1:])
