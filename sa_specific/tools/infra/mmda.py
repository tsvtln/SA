#!/opt/opsware/bin/python -u

# Multimaster Mesh Database Analyzer (mmda)
#
# This program performs analysis on records from all databases in a multi-
# master mesh looking for record differences.  It can optionally synchronize
# any differences that are found.  This analysis is performed with awareness of
# the garbage collectors running on every database.
#
# It performs the following general high-level operations:
#
#  o Makes sure it is running on a multimaster central spin server.
#
#  o Makes sure that none of the GCs show error and have run recently.
#
#  o Makes sure that the GC windows are the same throughout the mesh.
#
#  o Operates with awareness of the execute of these GCs as follows.  It 
#    suspends all analysis and optional synchronization activities some time
#    before the GCs are scheduled to start.  (Say 5 minutes.)  It then resumes 
#    activities after all GCs have reported that they are complete.
#
#  o Collects a list of all replicated tables and puts them in dependency 
#    order.
#
#  o For each replicated table:
#
#    o Pulls down every ID and TRANS_ID for ever record for every database.
#
#    o Any diffs in ID or TRANS_ID marks the object as out of sync.
#
#    o Optionally, initiates a deep diff to locate diffs that do not meet the
#      above criteria.
#
#    o Optionally synhcronizes any records found to be different.
#
#      o Synchronizes record from core that is determined to be the origin of
#        the record by analysing the ID of the record.
#
#  o During this operation, multiple threads are opened to maximize data
#    throughput.
#
#  o A multilayer progress bar is displayed to show the status of multiple
#    concurrent analysis and processing.
#
# Design Notes:
#
# o Global multithreaded architecture with the following main threadgroups:
#
# o FindShalowDiffs() - Scans all databases and located differences due to
#   record existance and different trans_id's.  Produces record IDs that are
#   detected to be out of sync and a list of records for each table that need
#   deeper analysis.
#
# o FindDeepDiffs() - Consumes lists of records for each table that need to be
#   analyzed deeper in order to determine a difference.  Produces record IDs 
#   that are detected to be out of sync.  This thread is optional based on 
#   command line argument.
#
# o SyncRecords() - Consumes a list of record IDs that have been determined to
#   be out of sync.  Optionally synchronizes them across all databases.
#   Optionally outputs the record ID, along with the corresponding spin class
#   name, to an output file.  If the record is successfully synchronized, then
#   it is not printed to the output file.
#
# o Each of the main threadgroups may interact with the global progress display
#   to relate information about its progress.
#   
#------------------------------------------------------------------------------
#
#
#
#

# Figure out a name.
if ( __name__=='__main__' ):
    g_sName = sys.argv[0]
else:
    g_sName = __name__

def _Debug( sMsg ):
    sys.stderr.write( sMsg + "\r" )

class Options:
  def PrintUsage( self ):
        _Debug( """Multimaster Mesh Database Analyzer.

Usage: %s [-d] [-f so_out_file] [-s] [-v] [class ...]

Remarks:

Performs an  analysis across  all the  databases of a  multimaster mesh.   As a
result  it must be  executed on  the multimaster  central spin  so that  it can
directly access  every database  in the mesh.   It will analyse  the replicated
tables behind the specified classes, or  all relicated tables if no classes are
specified.  It can optionally send the  results of this analysis to a file.  It
can also optionally synchronize any differences that it found.

Standard output  contains a VT  rendered progress display only.   Debug message
and other errors that occur during the  operation of the tool.  As a result, it
is  suggested  that  standard error  be  redirected  to  a file  and  inspected
seperately for errors as follows:

  %s 2> out.err

This program  spins up multiple threads  to maximize throughput  to the several
databases.  For  example, if  deep analysis  is specified, it  will occur  in a
seperate  thread  with its  own  progress  structure.   As a  result,  multiple
progress bars can be visable at the same time.

Options:
 -d Perform deep analysis of each record of every class scanned.
 -f Send record differences to a file in the sync_objects.py format.  If "-s"
    is also specified, then record differences are only reported if an error
    occured preventing during the synchronization of the record.
 -s Synchronize any found differences.  Records are synchronized from the core
    that created the record.  The creator is located based upon the datacenter
    ID embedded inside of the record's ID field.  If the ID is a combination of
    other IDs, such as "120001-230002", then the leftmost ID is arbitrarily
    used to determine the "origonator" of the record.
 -v Verbosity level.

""" % ( g_sName, g_sName ) );


