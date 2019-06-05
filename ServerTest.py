import sys
from PyQt5.QtCore import pyqtSlot
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication, QMainWindow
import socket
from threading import Thread

class ServerThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.tcpServer = None


    def run(self):
        TCP_IP = '0.0.0.0' #Set 0.0.0.0 as IP, so welcome  open everybody to connect.
        TCP_PORT = 8765
        BUFFER_SIZE = 500
        self.tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.tcpServer.bind((TCP_IP, TCP_PORT))
        threads = []
        self.tcpServer.listen(4)

        while True:
            print("Multithreaded Python server : Waiting for connections from TCP clients...")
            (client, (ip, port)) = self.tcpServer.accept()
            newthread = ClientThread(ip, port, client)
            newthread.start()
            threads.append(newthread)

        for t in threads:
            t.join()


class ClientThread(Thread):
    global serverThread
    def __init__(self, ip, port,client ):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.client = client
        print("[+] New server socket thread started for " + ip + ":" + str(port))


    def run(self):
        #(conn, (self.ip, self.port)) = serverThread.tcpServer.accept()

        while True:
            recvdata = self.client.recv(2048)
            print('ServerTest.py: ClientThread recvdata = ', recvdata.decode("utf-8"))
            server_log_msg = r"{}:{} recv {}".format(self.ip, self.port, recvdata.decode("utf-8"))
            self.client.send(  r"logged the server_log_msg={}".format(server_log_msg).encode(encoding='utf_8', errors='strict') )
            break









class ServerThreadWindow(QMainWindow):
    def __init__(self):
        super(ServerThreadWindow, self).__init__()
        loadUi('serverTestForm.ui', self)
        self.pushButton.clicked.connect(self.on_pushButton_clicked)

    @pyqtSlot()
    def on_pushButton_clicked(self):
        print('detect pushButton clicked on Server')
        pass


serverThread = None
if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = ServerThreadWindow()
    widget.show()
    serverThread = ServerThread()
    serverThread.start()
    sys.exc_info(app.exec_())

