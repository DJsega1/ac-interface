import sys

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QSpinBox
from PyQt5.uic import loadUi


class MainWindow(QMainWindow):
    command_value = None
    now_spin = None

    def __init__(self):
        super().__init__()
        loadUi('static/main.ui', self)
        self.init_ui()

    def init_ui(self):
        pic = QPixmap('static/default.png')
        self.imageLabel.setPixmap(pic)
        self.imageButton.clicked.connect(self.signal_image)
        self.sendButton.clicked.connect(self.signal_send)
        self.stopButton.clicked.connect(self.signal_stop)
        self.radioGroup.buttonClicked.connect(self.radio)

    def signal_image(self):
        print(1)

    def signal_send(self):
        if self.command_value:
            print(self.command_value)

    def signal_stop(self):
        print(3)

    def radio(self, button):
        if self.now_spin:
            self.now_spin.setEnabled(False)
        command_name = button.text()

        # [:-5] for removing 'Radio' suffix and appending 'Box' suffix
        spin_name = button.objectName()[:-5] + 'Box'

        # find SpinBox by objectName
        self.now_spin = self.findChild(QSpinBox, spin_name)
        self.now_spin.setEnabled(True)

        # TODO spinbox slots
        self.command_value = (command_name, self.now_spin.value())


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
