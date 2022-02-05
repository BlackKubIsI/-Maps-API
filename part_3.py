import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from maps_ip import get_map_image


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(200, 200, 500, 450)
        self.map_size = [0.1, 0.1]
        self.map_center = [37.6156, 55.7522]
        self.settings()

    def settings(self):
        self.map = QLabel(self)
        self.map.setGeometry(0, 0, 500, 450)
        self.update_map_image()

    def update_map_image(self):
        self.map.setPixmap(get_map_image(self.map_center, self.map_size))
        self.update()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageDown:
            self.map_size = list(map(lambda x: min(x * 2, 5), self.map_size))
            self.update_map_image()
        if event.key() == Qt.Key_PageUp:
            self.map_size = list(
                map(lambda x: max(x / 2, 0.001), self.map_size))
            self.update_map_image()
        if event.key() == Qt.Key_Left:
            self.map_center[0] = max(
                self.map_center[0] - self.map_size[0] * 2, -180 + self.map_size[0] * 2 - 0.00001)
            self.update_map_image()
        if event.key() == Qt.Key_Right:
            self.map_center[0] = min(
                self.map_center[0] + self.map_size[0] * 2, 180 - self.map_size[0] * 2 + 0.00001)
            self.update_map_image()
        if event.key() == Qt.Key_Down:
            self.map_center[1] = max(
                self.map_center[1] - self.map_size[1] * 2, -90 + self.map_size[1] * 2 - 0.00001)
            self.update_map_image()
        if event.key() == Qt.Key_Up:
            self.map_center[1] = min(
                self.map_center[1] + self.map_size[1] * 2, 90 - self.map_size[1] * 2 + 0.00001)
            self.update_map_image()


app = QApplication(sys.argv)
main = MainWindow()
main.show()
sys.exit(app.exec())
