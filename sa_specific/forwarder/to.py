import socket,asyncore
import sys
import os

class file_wrapper:
    # here we override just enough to make a file
    # look like a socket for the purposes of asyncore.
    def __init__(self, fdi, fdo):
        self.fdi = fdi
        self.fdo = fdo
        self._fileno = fdi.fileno()

    def recv(self, size):
        return self.fdi.readline(size)
#        return apply(os.read, (self.fd,)+args)

    def write(self, str):
        return os.write(self.fdo.fileno(), str)

    def close(self):
        return None
#        return self.fdi.close() or self.fdo.close()

    def fileno(self):
        return self.fdi.fileno()

class file_dispatcher(asyncore.dispatcher):
    def __init__(self, fdi, fdo):
        asyncore.dispatcher.__init__(self)
        self.connected = 1
        # set it to non-blocking mode
#        flags = fcntl.fcntl (fd, FCNTL.F_GETFL, 0)
#        flags = flags | FCNTL.O_NONBLOCK
#        fcntl.fcntl (fd, FCNTL.F_SETFL, flags)
        self.set_file(fdi, fdo)
	from_remote_buffer = ''

    def set_file(self, fdi, fdo):
        self.socket = file_wrapper(fdi, fdo)
        self.add_channel()

class receiver(file_dispatcher):
    def __init__(self,fdi,fdo):
        file_dispatcher.__init__(self,fdi,fdo)
        self.from_remote_buffer=''
        self.to_remote_buffer=''
        self.sender=None

    def handle_connect(self):
        pass

    def handle_read(self):
        read = self.recv(4096)
        # print '%04i -->'%len(read)
        self.from_remote_buffer = self.from_remote_buffer + read

    def writable(self):
        return (len(self.to_remote_buffer) > 0)

    def handle_write(self):
#        sent = self.send(self.to_remote_buffer)
        sent = self.write(self.to_remote_buffer)
        # print '%04i <--'%sent
        self.to_remote_buffer = self.to_remote_buffer[sent:]

    def handle_close(self):
        self.close()
        if self.sender:
            self.sender.close()


class sender(asyncore.dispatcher):
    def __init__(self, receiver, remoteaddr,remoteport):
        asyncore.dispatcher.__init__(self)
        self.receiver=receiver
        receiver.sender=self
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((remoteaddr, remoteport))

    def handle_connect(self):
        pass

    def handle_read(self):
        read = self.recv(4096)
        # print '<-- %04i'%len(read)
        self.receiver.to_remote_buffer = self.receiver.to_remote_buffer + read

    def writable(self):
        return (len(self.receiver.from_remote_buffer) > 0)

    def handle_write(self):
        sent = self.send(self.receiver.from_remote_buffer)
        # print '--> %04i'%sent
        self.receiver.from_remote_buffer = self.receiver.from_remote_buffer[sent:]

    def handle_close(self):
        self.close()
        self.receiver.close()

if __name__=='__main__':
    while 1:
        sender(receiver(sys.stdin, sys.stdout),"google.com",80)
        asyncore.loop()
