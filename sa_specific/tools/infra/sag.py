
##
# sag Program Overview:
#
# Server Automation Gatherer - sag
#
# Tool to gather the logs, thread dumps, or diagnostics from arbitrary
# HPSA components on arbitrary servers across the mesh at one time.
#

# python native libs.
import sys, os

# python non-native libs.
import io, log, util

g_exename = os.path.basename(sys.argv[0])

def usage():
  io.out("""Server Automation Gatherer

  Utility to gather  logs, thread dumps, and diagnostics  from multiple servers
  across the mesh at one time.  Can be executed from any infrastrcture or slice
  server in the mesh.  It obtains this  data by connecting to the agents of the
  various target servers via the opswgw mesh.

  By default, the results are dumped to a file named "sag-<date>.pkl.gz".  This
  compressed pickle file contains a series of packets that describe the results
  for the component  data requested from the various  target servers specified.
  This is to  help make transporting the results easier.  Sag  can also be used
  to demultiplex this stream into a set of files in a directory for analysis.

Usages:

%(g_exename)s [<target>] [-e <cmd_args> [e-]] [-c <components>] [-w <what>] [-f] [-t]
    [-o <outfile>] [-k <cert>] [-b] [-h]

%(g_exename)s -l

%(g_exename)s <infile> ...

  [<target>]: [-r <realms>|-gw <nodes>|-d <py_dvc_id_list_expr>|
               -i <realmful_ips>]
     If unspecified  then all infrastructure, slice, and  sattelite devices are
     targetted.

  -r <realms>
     Comma  seperated list  of  core or  satellite  gw realms.   Every core  or
     satellite server in the specified <realms> will be targetted.

  -gw <nodes>
     Comma  seperated  list  of core  or  satellite  gw  nodees.  The  core  or
     satellite servers running the specified gateway <nodes> will be targetted. 
     (I'm not sure this argument is worth the effort to impliment.)

  -d <py_dvc_id_list_expr>
     A python spinwrapper  expression that evaluates to a  list of devicve ids.
     Examples:

       o "[1230001]"
       o "spin.Device.getIDList()"

  -i <realmful_ips>
     Comma seperated list of realmful IP addresses to target.

  [-e <cmd_args> [e-]]
     Will execute  the command  and arguments given  by <cmd_args>  against the
     target servers.  The  literal "e-" can be added  so that multiple commands
     can be issued.  If "e-" is not sent, then all arguments after "-e" will be
     assumed to be part of the <cmd_args>.  Examples:

     # Get the date from every infra, slice, and sat devices in the mesh:
     %(g_exename)s -e date

     # Get the date and uptime from  every infra, slice, and sat devices in the
     # mesh:
     %(g_exename)s -e date e- -e uptime

     (If you want  to send "e-" as  a real command argument, then  escape it by
     putting a  "\\" in  front of  it.  (Watch out  for interferance  with shell
     escaping.))

  [-c <components>]
     Comma seperated  List of  components for which  to gather, such  as: spin,
     way, word, twist, agent, vault,  etc.  If unspecified, then all components
     are queried.

  [-w <what>]
     Comma  seperated  list  of  items  to gather.   Valid  values  are:  logs,
     threaddump, and diags.  If unspecified then "diags" is assumed.

  [-t]
     Send results to terminal. 

  [-f]
     Send results to file.  (This is the default.)

  [-o <outfile>]
     Will  save the  results  to the  file  given by  <filename>.  Otherwise  a
     filename will generated of the form "sag-<date>.pkl.gz".

  [-h]
     Displays this help message.  (Default option if no options are specified.) 

  [-k <cert>]
     Specify and alternative client cert to use.  Default is
     "/var/opt/opsware/crypto/spin/spin.srv"

  [-b]
     Bypass gateway mesh and reach out to agents directly.
     (TODO: Add logic to detect when agent is in current slice's realm
     and automatically bypass gw mesh.)

  -l
     List all core  and satellite gw realms and the  device IPs associated with
     those gw realms.

  <infile>
     Will demultiplex the data previously  captured in the file <filename> to a
     set  of files  in a  directory named  after <filename>,  into  the current
     directory.
""" % globals())

def main():
  argv = sys.argv[1:]

  # Argument variables.
  gw = ("127.0.0.1", 3001)

  while (argv):
    arg = shift(argv)
    if ( arg == "-e" ):
      ## collect command line args.
      pass
  usage()
  return 0

if ( __name__ == "__main__" ):
  sys.exit(main())