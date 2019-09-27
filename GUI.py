from web_scraping import CoursePage
from PyQt5.QtWidgets import QWidget, QApplication, QDesktopWidget
import sys


QUARTER = {'fall': '92',
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())

    # cp = CoursePage("2019", "92", "34414")
    # cp.refresh()
    # print(cp.get_restrictions())
