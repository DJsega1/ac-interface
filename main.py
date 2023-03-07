import base64
import requests
import struct
import sys

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi


class MainWindow(QMainWindow):
    _IMAGE_SCALER = 4
    _PRESS_W_VALUE = 1
    _commands = {
        'cameraRadio': 'asddasadsadsdas',
        'servoRadio': 'rotate servo',
        'velocityRadio': 'set velocity',
        'softRadio': 'soft turn',
        'hardRadio': 'hard turn',
        'forwardRadio': (0x01, 'value', 'value'),
    }  # mapping radio button: command to send

    def __init__(self):
        super().__init__()
        loadUi('static/new.ui', self)
        self._init_ui()

    def _init_ui(self):
        src = QPixmap('static/default.png')
        src = src.scaled(src.size() * self._IMAGE_SCALER)
        self.imageLabel.setPixmap(src)
        self.imageButton.clicked.connect(self._signal_image)
        self.sendButton.clicked.connect(self._signal_send)
        self.stopButton.clicked.connect(self._signal_stop)
        self.setWindowTitle('Robot Control Interface')

    def _signal_image(self):
        src = QPixmap('static/image.jpg')
        src = src.scaled(src.size() * self._IMAGE_SCALER)
        self.imageLabel.setPixmap(src)

    def _signal_send(self):
        button = self.radioGroup.checkedButton().objectName()
        value = self.valueBox.value()
        if button == 'forwardRadio' and value:
            data = base64.b64encode(
                struct.pack('>3B', 1, min(value, 255),  max(0, value - 255))
            )
        elif button == 'backwardRadio' and value:
            data = base64.b64encode(
                struct.pack('>3B', 2, min(value, 255),  max(0, value - 255))
            )
        elif button == 'hardRadio' and value:
            data = base64.b64encode(
                struct.pack('>3B', 3, abs(value),  value // abs(value))
            )
        elif button == 'softRadio' and value:
            data = base64.b64encode(
                struct.pack('>3B', 4, abs(value),  value // abs(value))
            )
        elif button == 'velocityRadio' and value:
            data = base64.b64encode(
                struct.pack('>3B', 5, 0,  value)
            )
        elif button == 'cameraRadio' and value:
            data = base64.b64encode(
                struct.pack('>3B', 6, value,  0)
            )
        elif button == 'servoRadio' and value:
            data = base64.b64encode(
                struct.pack('>3B', 7, value,  0)
            )
        requests.get('http://10.8.0.3:8080/send_command', params={'cmd': data})

    def _signal_stop(self):
        print(3)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
