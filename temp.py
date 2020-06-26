import sys
import glob
import serial.tools.list_ports
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
                             QGridLayout,
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

        # Widgets
        self.l_feedback = QLabel("Placeholder")
        self.pb_connect = QPushButton("Connect")
        self.pb_send_fr = QPushButton("Send FR")
        self.pb_disconnect = QPushButton("Disconnect")
        self.cb_drop_down = QComboBox()
        self.ports = list(serial.tools.list_ports.comports())
        self.port = self.ports[0] # TODO: this should be dynamic
        for p in self.ports: # TODO: Put in thread
            self.cb_drop_down.addItem(f"{p.name}: {p.manufacturer}") 

        # Add widgets to layout
        self.layout.addLayout(self.get_top_widget_layout())
        self.layout.addWidget(self.get_bottom_groups())

        # Set layout
        self.setLayout(self.layout)

    def get_top_widget_layout(self):
        layout = QGridLayout()

        self.l_feedback.setMaximumHeight(30)
        italic = QFont()
        italic.setItalic(True)
        self.l_feedback.setFont(italic)
        
        self.pb_connect.setMaximumWidth(100)
        self.pb_send_fr.setMaximumWidth(100)
        self.pb_disconnect.setMaximumWidth(100)
        
        self.pb_connect.clicked.connect(self.connect)
        self.pb_send_fr.clicked.connect(self.send_fr)
        self.pb_disconnect.clicked.connect(self.disconnect)

        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 0)
        layout.setColumnStretch(2, 0)
        layout.setColumnStretch(3, 0)
        layout.setColumnStretch(4, 1)

        layout.addWidget(QLabel("Port Name"),0,1)
        layout.addWidget(self.cb_drop_down,0,2)
        layout.addWidget(self.l_feedback,0,3)
        layout.addWidget(self.pb_connect,1,2)
        layout.addWidget(self.pb_send_fr,2,2)
        layout.addWidget(self.pb_disconnect,3,2)

        return layout

    # TODO: Move this into control stuff
    @pyqtSlot()
    def connect(self):
        print("Connecting device")

    @pyqtSlot()
    def disconnect(self):
        print("Disconnecting device")

    @pyqtSlot()
    def send_fr(self):
        print("Sending FR")

    def get_bottom_groups(self):
        groupBox = QGroupBox("Firmware Update")
    
        vbox = QVBoxLayout()
        vbox.addWidget(filedialog())
        
        hbox = QHBoxLayout()
        hbox.addWidget(self.gb_device())
        hbox.addWidget(self.gb_fw_file())
        # hbox.addStretch(1)
        vbox.addLayout(hbox)
        groupBox.setLayout(vbox)

        return groupBox

    def gb_device(self):
        groupBox = QGroupBox("Device")
        layout = QGridLayout()
        labels = {"Device Type:": self.port.manufacturer, 
                  "Device Variant:": "n/a", 
                  "Device Serial:": self.port.serial_number, 
                  "Firmware Version:": "n/a", 
                  "Bootloader Edition:": "n/a", 
                  "Bootloader FW Version:": "n/a"}

        i = 0
        for key, val in labels.items():
            label = QLabel(key)
            label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            layout.addWidget(label, i, 0)
            layout.addWidget(QLabel(val), i, 1)
            i += 1

        groupBox.setLayout(layout)
        return groupBox
    
    def gb_fw_file(self):        
        groupBox = QGroupBox("Firmware File")
        layout = QGridLayout()
        labels = ["Device Type:", 
                  "Device Variant:", 
                  "", 
                  "Firmware Version:", 
                  "Bootloader Edition:", 
                  "Bootloader FW Version:"]

        for i in range(len(labels)):
            label = QLabel(labels[i])
            label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            layout.addWidget(label, i, 0)
            if labels[i]:
                layout.addWidget(QLabel("n/a"), i, 1)

        groupBox.setLayout(layout)
        return groupBox

    
class filedialog(QWidget):
    def __init__(self, parent = None):
        super(filedialog, self).__init__(parent)
        
        layout = QGridLayout()
        layout.setRowStretch(0, 1)
        layout.setRowStretch(1, 0)
        layout.setRowStretch(2, 0)
        layout.setRowStretch(3, 1)

        layout.addWidget(QLabel("FW File Name"), 1, 0)

        self.contents = QTextEdit()
        self.contents.setMaximumHeight(25)
        layout.addWidget(self.contents, 2, 0)
        self.btn = QPushButton("Open File")
        self.btn.clicked.connect(self.getfile)
        layout.addWidget(self.btn, 2, 1)
        self.program = QPushButton("Program Device")
        self.program.clicked.connect(self.program_device)
        layout.addWidget(self.program, 3, 1)
        self.setLayout(layout)
        

    def program_device(self):
        print("programming device")

    @pyqtSlot()    
    def getfile(self):
        fname, _ = QFileDialog.getOpenFileName(self, 'Open file', 
                                               '~/',"Image files (*.* *.gif)")
        self.contents.setText(fname)

class Tab2(QWidget):
    def __init__(self):
        super().__init__()

class Tab3(QWidget):
    def __init__(self):
        super().__init__()

class Tab4(QWidget):
    def __init__(self):
        super().__init__()        
        
class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = "GUI"
        self.left = 0
        self.top = 0
        self.width = 640
        self.height = 480
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.gui = GUI(self)

        self.setCentralWidget(self.gui)

        self.show()

class GUI(QWidget):

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)


        # Create tabs
        self.tabs = QTabWidget()
        self.tabs.resize(300,200)

        tab1 = Tab1()
        tab2 = Tab2()
        tab3 = Tab3()
        tab4 = Tab4()
        self.tabs.addTab(tab1, "Devices")
        self.tabs.addTab(tab2, "Configuration")
        self.tabs.addTab(tab3, "PID Controller")
        self.tabs.addTab(tab4, "Monitor")
        
        # tab1.setLayout(tab1.layout)

        # Set tabs to GUI
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
