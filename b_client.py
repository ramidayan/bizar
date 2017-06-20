import md5
import socket
import threading

import time


class Client (object):

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def start(self):
        try:
            print('connecting to ip %s port %s' % (ip, port))
            # Create a TCP/IP socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((ip, port))
            print('connected to server')
            # send receive example
            msg = sock.recv(1024)
            print('received message: %s' % msg.decode())
            sock.sendall('Hello this is client, send me a job'.encode())
            # msg = sock.recv(1024)

            #implement here your main logic

            # while True:
            self.handleServerJob(sock)

        except socket.error as e:
            print(e)

    def cpu_num(self):
        """ return number of 'cpu' in this computer """
        try:
            import multiprocessing

            return multiprocessing.cpu_count()
        except (ImportError, NotImplementedError):
            pass

    def thread_func(self, first, end, check):
        found = False
        for i in range(first, end):
            if md5.new(str(i)).hexdigest() == check:
                found = True
                break
        print found
        return found

    def handleServerJob(self, serverSocket):
        n = self.cpu_num()
        data = serverSocket.recv(1024)
        start_check = int(data[0:10])
        end_check = int(data[10:17])
        check_num = data[17:]
        print data + ' ' + str(start_check) + ' ' + str(end_check) + ' ' + check_num
        print n
        for i in range(n):
            t = threading.Thread(target=self.thread_func, args=(start_check, start_check + (end_check / n), check_num))
            t.start()
            start_check += (end_check / n) + 1
        t.join()

#implement your logic here E.G

#recived range of numbers to check from server

#seperate job to several threads (as number of cores)

#if a thread found the password tell that to the server

# else return and wait for another job

if __name__ == '__main__':
    ip = '127.0.0.1'
    port = 220
    c =Client(ip, port)
    c.start()