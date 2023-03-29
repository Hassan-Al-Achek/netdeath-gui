import json
import subprocess
import sys
import ctypes
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QCheckBox, QTextEdit,
                             QGridLayout, QToolBar, QStatusBar, QTabWidget, QVBoxLayout, QHBoxLayout,
                             QGroupBox, QFrame, QSplitter, QScrollBar, QMessageBox, QInputDialog)
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
                    exec_file, state4 = QInputDialog.getText(self, "Executable Name ", "Specify the executable file name")

                    if state4:
                        create_mal_shortcut(self, shortcut_name, fake_pdf_link, exec_file)

    def executeCommands(self):
        commands = [
            "help",
            "banner",
            "shortcut",
            "scan <target_address>",
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
            scan_result = scan(self.getLineText().split()[1])
            self.clearLineText()
            tree_text = print_table(scan_result)
            self.setOutText(tree_text)
        elif self.getLineText() == "shortcut":
            self.setup_shoot_cut()

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
