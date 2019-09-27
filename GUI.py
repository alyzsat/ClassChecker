from PyQt5.uic.properties import QtGui

from web_scraping import CoursePage
from datetime import date
from PyQt5.QtWidgets import QWidget, QApplication, QDesktopWidget, QLineEdit, QLabel, QHBoxLayout, QVBoxLayout, \
    QPushButton, QComboBox, QCheckBox, QTextBrowser
from PyQt5.QtCore import QRect
import sys


QUARTERS = {'fall': '92',
            'winter': '03',
            'spring': '14',
            'summer session 1': '25',
            'summer session 2': '76',
            '10-wk summer': '39'
            }


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'ClassChecker'
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(self.title)
        self.set_dimensions()
        self.show()
        self.create_layout()

    def create_layout(self):
        hbox = QHBoxLayout()
        self.left_vbox = QVBoxLayout()
        self.right_vbox = QVBoxLayout()
        hbox.addLayout(self.left_vbox)
        hbox.addLayout(self.right_vbox)
        self.setLayout(hbox)

        self.create_left()
        self.create_right()


    def create_left(self):
        self.create_cc_section()
        self.create_year_section()
        self.create_quarter_section()
        self.create_restr_section()
        self.create_button_section()
        self.left_vbox.addStretch()

    def create_right(self):
        info_box = QTextBrowser()
        self.right_vbox.addWidget(info_box)


    def set_dimensions(self):
        """Sets the size of the window in proportion to the screen resolution"""
        # Get screen resolution
        desktop_size = QDesktopWidget().screenGeometry()
        h = desktop_size.height()
        w = desktop_size.width()

        # Determine screen dimensions
        self.height = h / 1.5
        self.width = w / 1.5

        # Set the size of the window
        self.setGeometry((w-self.width)/2, (h-self.height)/2, self.width, self.height)

    def create_cc_section(self):
        cc_hbox = QHBoxLayout()
        label = QLabel("Type Course Code:")
        self.cc_line_edit = QLineEdit()

        cc_hbox.addWidget(label)
        cc_hbox.addWidget(self.cc_line_edit)
        self.left_vbox.addLayout(cc_hbox)

    def create_year_section(self):
        year_hbox = QHBoxLayout()
        label = QLabel("Select Year:")
        self.year_combobox = QComboBox()

        year = date.today().year
        for yr in range(year, year - 4, -1):
            self.year_combobox.addItem(str(yr))

        year_hbox.addWidget(label)
        year_hbox.addWidget(self.year_combobox)
        self.left_vbox.addLayout(year_hbox)

    def create_quarter_section(self):
        quarter_hbox = QHBoxLayout()
        label = QLabel("Select Quarter:")
        self.quarter_combobox = QComboBox()

        for q in QUARTERS:
            self.quarter_combobox.addItem(q.capitalize())

        quarter_hbox.addWidget(label)
        quarter_hbox.addWidget(self.quarter_combobox)
        self.left_vbox.addLayout(quarter_hbox)

    def create_restr_section(self):
        restr_vbox = QVBoxLayout()
        label = QLabel("Select Restriction(s):")
        self.restr_N = QCheckBox("N")
        self.restr_L = QCheckBox("L")
        self.restr_A = QCheckBox("A")
        restr_vbox.addWidget(label)
        restr_vbox.addWidget(self.restr_N)
        restr_vbox.addWidget(self.restr_L)
        restr_vbox.addWidget(self.restr_A)
        self.left_vbox.addLayout(restr_vbox)

    def create_button_section(self):
        button_hbox = QHBoxLayout()
        self.start_button = QPushButton("Start Checking")
        self.stop_button = QPushButton("Stop")
        button_hbox.addWidget(self.start_button)
        button_hbox.addWidget(self.stop_button)
        self.left_vbox.addLayout(button_hbox)
        



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())

    # cp = CoursePage("2019", "92", "34414")
    # cp.refresh()
    # print(cp.get_restrictions())
