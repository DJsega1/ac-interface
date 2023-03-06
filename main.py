import sys

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi


class MainWindow(QMainWindow):
    _IMAGE_SCALER = 4
    _commands = {
        'cameraRadio': 'rotate camera',
        'servoRadio': 'rotate servo',
        'velocityRadio': 'set velocity',
        'softRadio': 'soft turn',
        'hardRadio': 'hard turn',
        'speedRadio': 'set speed'
    }  # mapping radio button: command to send

    def __init__(self):
        super().__init__()
        loadUi('static/new.ui', self)
        self._init_ui()

    def _init_ui(self):
        src = QPixmap('static/default.png')
        src = src.scaled(src.size() * self._IMAGE_SCALER)
        self.imageLabel.setPixmap(src)
        self.imageButton.clicked.connect(self.signal_image)
        self.sendButton.clicked.connect(self.signal_send)
        self.stopButton.clicked.connect(self.signal_stop)
        self.setWindowTitle('Robot Control Interface')

    def signal_image(self):
        src = QPixmap('static/image.jpg')
        src = src.scaled(src.size() * 4)
        self.imageLabel.setPixmap(src)

    def signal_send(self):
        button = self.radioGroup.checkedButton()
        value = self.valueBox.value()
        if button and value:
            command = self._commands[button.objectName()]
            print(command, value)

    def signal_stop(self):
        print(3)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
