import sys
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtWidgets import (QMainWindow,
                             QApplication,
                             QPushButton,
                             QWidget,
                             QAction,
                             QTabWidget,
                             QVBoxLayout,
                             QHBoxLayout,
                             QComboBox,
                             QLineEdit,
                             QLabel,
                             QGroupBox,
                             QFileDialog,
                             QTextEdit,
                             QSpinBox,
                             QCheckBox)

class Tab1(QWidget):
    
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout() # Main layout
        self.layout.addLayout(self.com_buttons())
        
        self.setLayout(self.layout)
        
    def com_buttons(self):
        vbox = QVBoxLayout()
        vbox.setSpacing(10);

        connect = QPushButton("Connect")        
        send_fr = QPushButton("Send FR")
        disconnect = QPushButton("Disconnect")
        connect.setMaximumWidth(100)
        send_fr.setMaximumWidth(100)
        disconnect.setMaximumWidth(100)
        vbox.addWidget(connect)
        vbox.addWidget(send_fr)
        vbox.addWidget(disconnect)

        connect.clicked.connect(self.connect)
        send_fr.clicked.connect(self.send_fr)
        disconnect.clicked.connect(self.disconnect)        

        return vbox
        
    @pyqtSlot()
    def connect(self):
        print("Connecting device")

    @pyqtSlot()
    def disconnect(self):
        print("Disconnecting device")

    @pyqtSlot()
    def send_fr(self):
        print("Sending FR")                
        
        
class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'GUI'
        self.left = 0
        self.top = 0
        self.width = 640
        self.height = 480
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        self.table_widget = GUI(self)
        self.setCentralWidget(self.table_widget)
        
        self.show()
    
class GUI(QWidget):
    
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        
        
        # Create tabs
        self.tabs = QTabWidget()
        self.tabs.resize(300,200)
        
        tab1 = Tab1()
        self.tabs.addTab(tab1, "Devices")
        tab1.setLayout(tab1.layout)

        # Set tabs to GUI
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
		            
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
    
