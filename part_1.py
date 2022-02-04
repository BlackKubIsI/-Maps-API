import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtGui import QPixmap
from maps_ip import get_map_image

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(200, 200, 500, 500)
        self.settings()
    
    def settings(self):
        self.map = QLabel(self)
        self.map.setGeometry(0, 0, 500, 500)
        self.map.setPixmap(get_map_image((37.6156, 55.7522), (0.1, 0.1)))

app = QApplication(sys.argv)
main = MainWindow()
main.show()
sys.exit(app.exec())