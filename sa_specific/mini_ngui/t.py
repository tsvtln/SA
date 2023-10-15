import io, os, sys

mystdout = os.fdopen(io.slip_fd(1,2),'w')

sys.stdout.write("stdout write\n")
sys.stderr.write("stderr write\n")
mystdout.write("mystdout write\n")
