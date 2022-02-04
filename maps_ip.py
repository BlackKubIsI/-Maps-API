import requests
from PyQt5.QtGui import QPixmap
MAP_API_SERVER = "http://static-maps.yandex.ru/1.x/"

def get_map_image(center_pos, map_size, map_type="map"):
    params = {"ll": f"{center_pos[0]},{center_pos[1]}",
              "l": map_type,
              "spn": f"{map_size[0]},{map_size[1]}"}
    response = requests.get(MAP_API_SERVER, params=params).content
    map = QPixmap()
    map.loadFromData(response)
    return map 