import base64
import struct
import sys

import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi


class MainWindow(QMainWindow):
    _IMAGE_SCALER = 4
    _PRESS_W_VALUE = 1

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
        if button == 'stringHcRadio':
            value = bytearray.fromhex(self.stringEdit.text())
            data = struct.pack('>3B', 9, 0, 0)
            for i in range(len(value) // 2):
                data += struct.pack(
                    '>3B', 10, value[i * 2], value[i * 2 + 1]
                )
            if len(value) % 2 == 1:
                data += struct.pack('>3B', 10, value[-1], 0)
            else:
                data += struct.pack('>3B', 10, 0, 0)
            data = base64.b64encode(data)
        else:
            value = self.valueBox.value()
            if button == 'forwardRadio' and value:
                data = base64.b64encode(
                    struct.pack(
                        '>3B', 1, min(value, 255),  max(0, value - 255)
                    )
                )
            elif button == 'backwardRadio' and value:
                data = base64.b64encode(
                    struct.pack(
                        '>3B', 2, min(value, 255),  max(0, value - 255)
                    )
                )
            elif button == 'hardRadio' and value:
                vector = 0 if value < 0 else 1
                data = base64.b64encode(
                    struct.pack('>3B', 3, abs(value),  vector)
                )
            elif button == 'softRadio' and value:
                vector = 0 if value < 0 else 1
                data = base64.b64encode(
                    struct.pack('>3B', 4, abs(value),  vector)
                )
            elif button == 'velocityRadio' and value:
                data = base64.b64encode(
                    struct.pack('>3B', 5, 0,  value)
                )
            elif button == 'cameraRadio':
                data = base64.b64encode(
                    struct.pack('>3B', 6, value,  0)
                )
            elif button == 'servoRadio':
                data = base64.b64encode(
                    struct.pack('>3B', 7, value,  0)
                )
        requests.get('http://10.8.0.3:8080/send_command', params={'cmd': data})

    def _signal_stop(self):
        data = base64.b64encode(
                struct.pack('>3B', 255, 255, 255)
            )
        requests.get('http://10.8.0.3:8080/send_command', params={'cmd': data})


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
