
from PyQt5.QtCore import pyqtSlot
from PyQt5.uic import loadUi
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
import socket
from threading import Thread


class ClientThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        #self.host = socket.gethostname()
        self.host = '127.0.0.1'
        self.port = 8765
        self.tcpClientA= None

    def run(self):
        host = self.host
        port = self.port
        BUFFER_SIZE = 200
        self.tcpClientA = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcpClientA.connect((host, port))
        self.tcpClientA.send('MsgFromTcpClientA'.encode(encoding='utf_8', errors='strict'))
        data = self.tcpClientA.recv(BUFFER_SIZE)
        print('recv data from server is => ', data.decode('utf-8'))
        self.tcpClientA.close()

class ClientThreadWindow(QMainWindow):
    def __init__(self):
        super(ClientThreadWindow, self).__init__()
        loadUi('clientTestForm.ui', self)
    @pyqtSlot()
    def on_pushButton_clicked(self):
        print('detect pushButton clicked')
        clientThread = ClientThread()
        clientThread.start()
        pass

app=QApplication(sys.argv)
widget = ClientThreadWindow()
widget.show()
sys.exit(app.exec_())

