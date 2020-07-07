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
        
        self.table_widget = MyTableWidget(self)
        self.setCentralWidget(self.table_widget)
        
        self.show()
    
class MyTableWidget(QWidget):
    
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        
        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tab4 = QWidget()
        self.tabs.resize(300,200)
        
        # Add tabs
        self.tabs.addTab(self.tab1,"Devices")
        self.tabs.addTab(self.tab2,"Configuration")
        self.tabs.addTab(self.tab3,"PID Controller")
        self.tabs.addTab(self.tab4,"Monitor")
        # ______________________________________________________________________
        
        # Create first tab       
        self.tab1.layout = QVBoxLayout() # Main layout
        self.top_layout = QHBoxLayout() # Top half
        self.tab1.layout.addLayout(self.top_layout) # Add top half to main
        self.top_right_layout = QVBoxLayout() # Right side of top layout

        # Drop down menu
        self.l_drop_down_label = QLabel("Port Name")
        self.top_layout.addWidget(self.l_drop_down_label)
        self.cb_drop_down = QComboBox()
        self.cb_drop_down.addItem("test1") # TODO: serial devices
        self.cb_drop_down.addItem("test2")
        self.cb_drop_down.move(50, 250)
        self.top_layout.addWidget(self.cb_drop_down)

        # Label
        self.connect_feedback = QLineEdit("placeholder")
        self.connect_feedback.setEnabled(False)
        self.top_right_layout.addWidget(self.connect_feedback)
        
        # Buttons
        self.pb_connect = QPushButton("Connect")
        self.pb_connect.clicked.connect(self.connect)
        self.top_right_layout.addWidget(self.pb_connect)

        self.pb_send_fr = QPushButton("Send FR")
        self.pb_send_fr.clicked.connect(self.send_fr)
        self.top_right_layout.addWidget(self.pb_send_fr)
        
        self.pb_disconnect = QPushButton("Disconnect")
        self.pb_disconnect.clicked.connect(self.disconnect)
        self.top_right_layout.addWidget(self.pb_disconnect)
        # ______________________________________________________________________

        group = self.gb_fw_update()
        self.tab1.layout.addWidget(group)

        self.top_layout.addLayout(self.top_right_layout)
        self.tab1.setLayout(self.tab1.layout)

        # Tab 2 ________________________________________________________________
        
        # Create first tab       
        self.tab2.layout = QHBoxLayout() # Main layout
        self.left_layout = QVBoxLayout() # Left layout
        self.right_layout = QVBoxLayout() # Right layout
        self.tab2.layout.addLayout(self.left_layout)
        self.tab2.layout.addLayout(self.right_layout)
        labels = ["UART Magnitude",
                  "Target Source",
                  "Inst Current Limit (mA)"]
        
        servo = ["Upper Valid Bound (\u03BCs)",
                 "Lower Valid Bound (\u03BCs)",
                 "Upper 100 Bound (\u03BCs)",
                 "Lower 100 Bound (\u03BCs)",
                 "Upper 0 Bound (\u03BCs)",
                 "Lower 0 Bound (\u03BCs)",
                 "Acceptable Dead Time (ms)"]

        analogue = ["Analogue Input Mode",
                    "Upper 100 Bound",
                    "Lower 100 Bound",
                    "Upper 0 Bound",
                    "Lower 0 Bound"]

        bold = QFont()
        bold.setBold(True)

            
        self.left_layout.addLayout(self.config_row(labels))
        
        header = QLabel("Servo Input Settings")
        header.setFont(bold)
        self.left_layout.addWidget(header)
        self.left_layout.addLayout(self.config_row(servo))

        header = QLabel("Analogue Input Settings")
        header.setFont(bold)

        self.left_layout.addWidget(header)
        self.left_layout.addLayout(self.config_row(analogue))

        # Right side ___________________________________________________________
        btn_str = ["Read Configs",
                    "Write Configs",
                   "Save Configs",
                   "Restore Configs",
                   "Restore Defaults",
                   "Factory Reset"]

        for bs in btn_str:
            pb = QPushButton(bs)
            if bs == "Write Configs":
                hbox = QHBoxLayout()
                cb = QCheckBox()
                l = QLabel("Write to All")
                hbox.addWidget(pb)
                hbox.addWidget(cb)
                hbox.addWidget(l)
                self.right_layout.addLayout(hbox)
            else:
                self.right_layout.addWidget(pb)
                



            
        self.tab2.setLayout(self.tab2.layout)

        # ______________________________________________________________________
        
        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    def config_row(self, labels):
        vbox = QVBoxLayout()
        for l in labels:
            hbox = QHBoxLayout()
            label = QLabel(l)
            spin = QSpinBox()
            check = QCheckBox()
            hbox.addWidget(label)
            hbox.addWidget(spin)
            hbox.addWidget(check)
            vbox.addLayout(hbox)
        return vbox
        

    def gb_fw_update(self):
        groupBox = QGroupBox("Firmware Update")
        
        file_dialog = filedialog()
        device = self.gb_device()
        fw_file = self.gb_fw_file()

        vbox = QVBoxLayout()
        vbox.addWidget(file_dialog)
        
        hbox = QHBoxLayout()
        hbox.addWidget(device)
        hbox.addWidget(fw_file)
        # hbox.addStretch(1)
        vbox.addLayout(hbox)
        groupBox.setLayout(vbox)

        return groupBox

    def gb_device(self):
        groupBox = QGroupBox("Device")
        vbox = QVBoxLayout()
        labels = ["Device Type:", 
                  "Device Variant:", 
                  "Device Serial:", 
                  "Firmware Version:", 
                  "Bootloader Edition:", 
                  "Bootloader FW Version:"]

        for l in labels:
            hbox = QHBoxLayout()
            label = QLabel(l)
            label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            hbox.addWidget(label)
            hbox.addWidget(QLabel("n/a"))
            
            vbox.addLayout(hbox)

        groupBox.setLayout(vbox)
        return groupBox

    def gb_fw_file(self):        
        groupBox = QGroupBox("Firmware File")
        vbox = QVBoxLayout()
        labels = ["Device Type:", 
                  "Device Variant:", 
                  "", 
                  "Firmware Version:", 
                  "Bootloader Edition:", 
                  "Bootloader FW Version:"]

        for l in labels:
            hbox = QHBoxLayout()
            label = QLabel(l)
            label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            hbox.addWidget(label)
            if l:
                hbox.addWidget(QLabel("n/a"))
            
            vbox.addLayout(hbox)

        groupBox.setLayout(vbox)
        return groupBox
        
    @pyqtSlot()
    def connect(self):
        print("Connecting device")

    @pyqtSlot()
    def disconnect(self):
        print("Disconnecting device")

    @pyqtSlot()
    def send_fr(self):
        print("Sending FR")                

class filedialog(QWidget):
    def __init__(self, parent = None):
        super(filedialog, self).__init__(parent)
        
        vbox = QVBoxLayout()
        vbox.addWidget(QLabel("FW File Name"))
        layout = QHBoxLayout()
        vbox.addLayout(layout)
        self.contents = QTextEdit()
        layout.addWidget(self.contents)
        self.btn = QPushButton("...")
        self.btn.clicked.connect(self.getfile)
        layout.addWidget(self.btn)
        self.program = QPushButton("Program Device")
        self.program.clicked.connect(self.program_device)
        layout.addWidget(self.program)
        self.setLayout(vbox)
        

    def program_device(self):
        print("programming device")
        
    def getfile(self):
        fname, _ = QFileDialog.getOpenFileName(self, 'Open file', 
                                               '~/',"Image files (*.* *.gif)")
        self.contents.setText(fname)
		            
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
    
