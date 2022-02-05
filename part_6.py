import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QRadioButton, QLineEdit, QPushButton
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from maps_ip import get_map_image, object_search


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(200, 200, 600, 450)
        self.map_size = [0.1, 0.1]
        self.map_center = [37.6156, 55.7522]
        self.map_type = "map"
        self.metka = []
        self.settings()

    def settings(self):
        self.map = QLabel(self)
        self.map.setGeometry(0, 0, 500, 450)
        self.update_map_image()
        self.btn_map = QRadioButton(self)
        self.btn_map.setText("Схема")
        self.btn_map.setGeometry(500, 10, 90, 30)
        self.btn_sat = QRadioButton(self)
        self.btn_sat.setText("Спутник")
        self.btn_sat.setGeometry(500, 60, 90, 30)
        self.btn_skl = QRadioButton(self)
        self.btn_skl.setText("Гибрид")
        self.btn_skl.setGeometry(500, 110, 90, 30)
        self.btn_map.clicked.connect(self.btn)
        self.btn_sat.clicked.connect(self.btn)
        self.btn_skl.clicked.connect(self.btn)
        self.search = QLineEdit(self)
        self.search.setGeometry(500, 350, 90, 30)
        self.search_btn = QPushButton(self, text="Search")
        self.search_btn.setGeometry(500, 400, 90, 30)
        self.search_btn.clicked.connect(self.search_f)

    def search_f(self):
        name = self.search.text()
        new_coords = object_search(name)
        if new_coords is not None:
            self.map_center = new_coords
            self.metka += [
                f"{new_coords[0]},{new_coords[1]},pmvvm{len(self.metka) + 1}"]
            self.update_map_image()

    def btn(self):
        if self.btn_map.isChecked():
            self.map_type = "map"
        if self.btn_sat.isChecked():
            self.map_type = "sat"
        if self.btn_skl.isChecked():
            self.map_type = "sat,skl"
        self.update_map_image()

    def update_map_image(self):
        self.map.setPixmap(get_map_image(
            self.map_center, self.map_size, map_type=self.map_type, pt="~".join(self.metka)))
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
