import socket
import threading
import time


class Server(object):
    def __init__(self, ip, port, hash):
        self.ip = ip
        self.port = port
        self.hash = hash
        self.startNum = '0000000000'
        self.END_NUM = '1000000'

    def start(self):
        try:
            print('server startin up on ip %s port %s' % (self.ip, self.port))
            # Create a TCP/IP socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.bind((ip, port))
            sock.listen(1)
            while True:
                print("waiting for a new client")
                clientSocket, client_address = sock.accept()
                print('new client entered')
                # send receive example
                clientSocket.sendall('Hello this is server'.encode())
                msg = clientSocket.recv(1024)
                print('received message: %s' % msg.decode())
                # implement here your main logic
                client_handler = threading.Thread(
                    target=self.handleClient,
                    args=(clientSocket,)
                    # without comma you'd get a... TypeError: handle_client_connection() argument after * must be a sequence, not _socketobject
                )
                client_handler.start()
                # self.handleClient(clientSocket)
        except socket.error as e:
            print(e)

    def handleClient(self, clientSock):
        print "I'm here"
        msgToSend = self.startNum + self.END_NUM + self.hash
        clientSock.send(msgToSend)
        request = clientSock.recv(1024)
        print 'Received {}'.format(request)
        clientSock.send('ACK!')
        clientSock.close()

        # implement your logic here
        # E.G
        # create a thread to handle this client connection and return
        # to handle more inside connections
        #in the new thread:
        # send to client the hash and a range of numbers to check
        # if a client found the password close all connections and quit
        # else give the client another range of numbers to check


if __name__ == '__main__':
    ip = "127.0.0.1"
    port = 220
    hash = 'EC9C0F7EDCC18A98B1F31853B181330'
    s = Server(ip, port, hash)
    s.start()
