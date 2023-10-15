#!/usr/bin/python
#
#  open parallel rosh connections to multiple servers at once
#
#

import os, sys, getopt, fcntl, select

## Functions
#############

def usage():
    print "usage: %s [arguments] [-c|-s] <list_of_machines>" % (sys.argv[0])
    print
    print "   [-l] : Username to connect as (default: root)"
    print "   [-m] : Max number of child processes to run at once"
    print "   [-c] : Command to execute (Can't be used with -s)"
    print "   [-s] : Script (+args) to execute (Can't be used with -c)"
    print "   [-p] : Turn padding off"
    print "   [-v] : Verbose output"
    print "\nExamples:\n"
    print '   # multirosh -m 20 -c "ps auxw" server1 server2 server3'
    print '   # multirosh -m 20 -s "./test.py -arg arg" server1 server2 server3'
    print '   # /bin/ls -1 /opsw/Server/@/* | xargs multirosh -p20 -c "df -k"'
    sys.exit(1)

def mkNonBlocking(fd):
    flags = fcntl.fcntl(fd, fcntl.F_GETFL)
    fcntl.fcntl(fd, fcntl.F_SETFL, flags | os.O_NDELAY)

def rosh(machine, username, cmd, is_script, pad_length):
    rosh_cmd = "/opsw/bin/rosh -l %s -n %s" % (username, machine)
    out_line = ''
    err_line = ''
    outeof = 0
    erreof = 0

    if is_script:
        rosh_cmd = rosh_cmd + " -s %s" % (cmd)
    else:
        rosh_cmd = rosh_cmd + " %s" % (cmd)

    p_stdin, p_stdout, p_stderr = os.popen3(rosh_cmd)
    p_stdin.close()

    #mkNonBlocking(p_stdout.fileno())
    #mkNonBlocking(p_stderr.fileno())

    while 1:
        read = select.select([p_stdout,p_stderr],[],[])
        if p_stdout in read[0]:
            out_line = p_stdout.readline()
        if p_stderr in read[0]:
            err_line = p_stderr.readline()
        if out_line == '':
            outeof = 1
        else:
            sys.stdout.write("%*s: %s\n" % (pad_length, machine, out_line.strip()))
            out_line = ''
        if err_line == '':
            erreof = 1
        else:
            sys.stderr.write("\033[1m%*s! %s\033[0;0m\n" % (pad_length, machine, err_line.strip()))
            err_line = ''
        if outeof and erreof:
            break
        #select.select([],[],[],.1)

    return(p_stdout.close())

def main():
    validargs = ['command=', 'parallel=', 'verbose', 'script=']

    try:
        optlist, machines = getopt.getopt(sys.argv[1:], 'c:l:m:ps:v', validargs)
    except:
        print "exception"
        usage()

    opt_username = "root"
    opt_command = ''
    opt_maxprocs = 1
    opt_padding = 1
    opt_script  = 0
    opt_verbose = 0
    opt_switch = 0
    pad_length = 0

    for opt, val in optlist:
        if opt in ("-c", "--command"):
            if opt_switch:
                print "ERROR: Options -s and -c are mutually exclusive.\n"
                usage()                
            opt_command = val
            opt_switch = 1

        if opt in ("-s", "--script"):
            if opt_switch:
                print "ERROR: Options -s and -c are mutually exclusive.\n"
                usage()
            opt_command = val
            opt_script = 1
            opt_switch = 1

        if opt in ("-l", "--username"):
            opt_username = val

        if opt in ("-m", "--maxprocs"):
            opt_maxprocs = int(val)

        if opt in ("-v", "--verbose"):
            opt_verbose = 1
            
        if opt in ("-p", "--padding"):
            opt_padding = 0

    if not opt_command or len(machines) < 0:
        usage()

    children = []
    is_child = 0

    if opt_padding:
        for host in machines:
            if len(host) > pad_length:
                pad_length = len(host)

    for host in machines:
        ## fork a new child if we have space for more
        if len(children) <= opt_maxprocs:
            pid = os.fork()

            if pid:
                if opt_verbose:
                    print "INFO: forked worker process: HOST=%s, PID=%s, CMD=%s" % (host, pid, opt_command)
                children.append(pid)
            else:
                is_child = 1
                break

        ## remove any finished child processes from the pid list
        while len(children) >= opt_maxprocs:
            for child_pid in children:
                pid, e =  os.wait()
                del children[children.index(pid)]

    if is_child:
        ret = rosh(host, opt_username, opt_command, opt_script, pad_length)
    else:
        ## stick around until the last child process is finished
        while len(children) > 0:
            for child_pid in children:
                pid, e =  os.wait()
                del children[children.index(pid)]

        return 0

## Main
########

if __name__ == "__main__":
    sys.exit(main())