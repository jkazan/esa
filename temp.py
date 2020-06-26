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
        # Main layout
        self.layout = QVBoxLayout() 

        # Widgets
        self.l_feedback = QLabel("Placeholder")
        self.pb_connect = QPushButton("Connect")
        self.pb_send_fr = QPushButton("Send FR")
        self.pb_disconnect = QPushButton("Disconnect")
        self.cb_drop_down = QComboBox()
        self.ports = self.get_ports()
        self.current_port = self.ports[0] if self.ports else "" # TODO: this should be dynamic

        # Add widgets to layout
        self.layout.addLayout(self.get_top_widget_layout())
        self.layout.addWidget(self.get_bottom_groups())

        # Set layout
        self.setLayout(self.layout)

    def get_ports(self):
        ports = list(serial.tools.list_ports.comports())
        if ports:
            for p in ports: # TODO: Put in thread
                self.cb_drop_down.addItem(f"{p.name}: {p.manufacturer}")
        else:
            self.cb_drop_down.addItem("none")

        return ports

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
        self.l_feedback.setText("Device connected")

    @pyqtSlot()
    def disconnect(self):
        self.l_feedback.setText("Device disconnected")
        
    @pyqtSlot()
    def send_fr(self):
        self.l_feedback.setText("Sending FR")

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
        labels = {"Device Type:": self.port.manufacturer if self.ports else "n/a", 
                  "Device Variant:": "n/a", 
                  "Device Serial:": self.port.serial_number if self.ports else "n/a", 
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
        # Main layout
        layout = QHBoxLayout()

        # Widgets/Layouts
        self.write_all_checkbox = QCheckBox()
        config_layout = self.get_config_layout()
        handle_config_group = self.get_handle_config_group()

        # Add widgets to layout
        layout.addLayout(config_layout)
        layout.addStretch(1)
        layout.addWidget(handle_config_group)

        # Set layout
        self.setLayout(layout)

    def read_configs(self):
        print("read_configs")
    
    def write_configs(self):
        if self.write_all_checkbox.isChecked():
            print("write all configs")
        else:
            print("write not all configs")
    
    def save_configs(self):
        print("save_configs")
    
    def restore_configs(self):
        print("restore_configs")
    
    def restore_defaults(self):
        print("restore_defaults")
    
    def factory_reset(self):
        print("factory_reset")

        
    def get_handle_config_group(self):
        group_box = QGroupBox("Handle Configs")
        right_vbox = QVBoxLayout()
        right_vbox.addStretch(1)

        buttons = {"Read Configs":self.read_configs,
                   "Write Configs":self.write_configs,
                   "Save Configs":self.save_configs,
                   "Restore Configs":self.restore_configs,
                   "Restore Defaults":self.restore_defaults,
                   "Factory Reset":self.factory_reset}

        for key, value in buttons.items():
            pb = QPushButton(key)
            right_vbox.addWidget(pb)
            pb.clicked.connect(value)

            if key == "Write Configs":
                hbox = QHBoxLayout()
                l = QLabel("Write to All")
                hbox.addStretch(1)
                hbox.addWidget(self.write_all_checkbox)
                hbox.addWidget(l)
                hbox.addStretch(1)
                right_vbox.addLayout(hbox)

        right_vbox.addStretch(1)
        group_box.setLayout(right_vbox)

        return group_box



    def get_config_layout(self):
        # Layoputs and group box
        left_grid = QGridLayout()
        # Left side
        labels = {"UART Magnitude": "",
                  "Target Source": "",
                  "Inst Current Limit (mA)": "",
                  "Servo Input Settings": "header",
                  "Upper Valid Bound (\u03BCs)": "",
                  "Lower Valid Bound (\u03BCs)": "",
                  "Upper 100 Bound (\u03BCs)": "",
                  "Lower 100 Bound (\u03BCs)": "",
                  "Upper 0 Bound (\u03BCs)": "",
                  "Lower 0 Bound (\u03BCs)": "",
                  "Acceptable Dead Time (ms)": "",
                  "Analogue Input Settings": "header",
                  "Analogue Input Mode": "",
                  "Upper 100 Bound": "",
                  "Lower 100 Bound": "",
                  "Upper 0 Bound": "",
                  "Lower 0 Bound": ""}

        bold = QFont()
        bold.setBold(True)

        idx = 0
        for key, value in labels.items():
            if value == "header":
                left_grid.setRowStretch(idx, 1)
                header = QLabel(key)
                header.setFont(bold)
                left_grid.addWidget(header)
            else:
                labels[key] = ConfigTrio(key)
                left_grid.addWidget(labels[key].get_label(), idx, 0)
                left_grid.addWidget(labels[key].get_spinbox(), idx, 1)
                left_grid.addWidget(labels[key].get_checkbox(), idx, 2)

            idx += 1

        return left_grid

class ConfigTrio():
    def __init__(self, label):
        self.label = QLabel(label)
        self.spinbox = QSpinBox()
        self.checkbox = QCheckBox()

    def get_label(self):
        return self.label
        
    def get_spinbox(self):
        return self.spinbox

    def get_checkbox(self):
        return self.checkbox
                
        
class Tab3(QWidget):
    def __init__(self):
        super().__init__()
        # Main layout
        layout = QHBoxLayout()

        # Widgets
        self.error_ppm = QLineEdit()
        self.e_P = QLineEdit()
        self.e_I = QLineEdit()
        self.e_D = QLineEdit()
        self.e_target_magnitude = QLineEdit()
        self.e_target_speed = QLineEdit()
        self.e_actual_magnitude = QLineEdit()
        self.e_pid_output_magnitude = QLineEdit()
        
        self.prescaler = QLineEdit()
        self.P = QLineEdit()
        self.I = QLineEdit()
        self.D = QLineEdit()
        self.I_lim = QLineEdit()
        self.acc_lim = QLineEdit()
        self.max_step_change = QLineEdit()

        self.target_source = QLineEdit()
        self.uart_magnitude = QLineEdit()

        self.read_configs = QPushButton("Read Configs")
        self.write_configs = QPushButton("Write Configs")
        self.write_all_checkbox = QCheckBox()
        self.save_configs = QPushButton("Save Configs")
        self.restore_configs = QPushButton("Restore Configs")
        self.restore_defaults = QPushButton("Restore Defaults")
        self.factory_reset = QPushButton("Facotry Reset")

        # Header font
        self.bold = QFont()
        self.bold.setBold(True)
        # Add widgets to layout
        layout.addLayout(self.get_left_layout())
        # layout.addStretch(1)
        layout.addLayout(self.get_center_layout())
        layout.addLayout(self.get_right_layout())

        # Set layout
        self.setLayout(layout)

    def get_left_layout(self):
        layout = QVBoxLayout()
        top_grid = QGridLayout()
        bottom_grid = QGridLayout()

        header1 = QLabel("PID Controller Error Values")
        header1.setFont(self.bold)
        layout.addWidget(header1)
        
        top_widgets = {"Error (pulses/min)": self.error_ppm,
                       "Proportional": self.e_P,
                       "Integral": self.e_I,
                       "Differential": self.e_D,}
        
        bottom_widgets = {"Target Magnitude": self.e_target_magnitude,
                          "Target Speed (pulses/min)": self.e_target_speed,
                          "Actual Speed (pulses/min)": self.e_actual_magnitude,
                          "PID Output Magnitude": self.e_pid_output_magnitude}

        i = 0
        for label, widget in top_widgets.items():
            top_grid.addWidget(QLabel(label), i, 0)
            top_grid.addWidget(widget, i, 1)
            i += 1

        layout.addLayout(top_grid)

        header2 = QLabel("Feedback and Control Values")
        header2.setFont(self.bold)
        layout.addWidget(header2)

        i = 0
        for label, widget in bottom_widgets.items():
            bottom_grid.addWidget(QLabel(label), i, 0)
            bottom_grid.addWidget(widget, i, 1)
            i += 1

        layout.addLayout(bottom_grid)

        return layout

    def get_center_layout(self):
        layout = QVBoxLayout()
        top_grid = QGridLayout()
        bottom_grid = QGridLayout()

        header1 = QLabel("PID Controller Gain and Limit Settings")
        header1.setFont(self.bold)
        layout.addWidget(header1)
        
        top_widgets = {"Prescaler": self.prescaler,
                       "Proportional": self.P,
                       "Integral": self.I,
                       "Differential": self.D,
                       "Integral Limit": self.I_lim,
                       "Acceleration Limit": self.acc_lim,
                       "Max Step Change": self.max_step_change}
        
        bottom_widgets = {"Target Source": self.target_source,
                          "UART Magniture": self.uart_magnitude}

        i = 0
        for label, widget in top_widgets.items():
            top_grid.addWidget(QLabel(label), i, 0)
            top_grid.addWidget(widget, i, 1)
            i += 1

        layout.addLayout(top_grid)

        header2 = QLabel("Input Control Settings")
        header2.setFont(self.bold)
        layout.addWidget(header2)

        i = 0
        for label, widget in bottom_widgets.items():
            bottom_grid.addWidget(QLabel(label), i, 0)
            bottom_grid.addWidget(widget, i, 1)
            i += 1

        layout.addLayout(bottom_grid)

        return layout

    def get_right_layout(self):
        pass
    
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


        # Create takey
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
