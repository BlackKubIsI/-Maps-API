import requests
from PyQt5.QtGui import QPixmap
MAP_API_SERVER = "http://static-maps.yandex.ru/1.x/"
GEOKODER_API_SERVER = "http://geocode-maps.yandex.ru/1.x/"


def get_map_image(center_pos, map_size, map_type="map", size=(500, 450), pt=""):
    params = {"ll": f"{center_pos[0]},{center_pos[1]}",
              "l": map_type,
              "spn": f"{map_size[0]},{map_size[1]}",
              "size": f"{size[0]},{size[1]}",
              "pt": pt}
    response = requests.get(MAP_API_SERVER, params=params).content
    map = QPixmap()
    map.loadFromData(response)
    return map


def object_search(name):
    response = requests.get(GEOKODER_API_SERVER, params={
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": name,
        "format": "json"
    }).json()
    if not response:
        return None
    return list(map(float, response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]["Point"]["pos"].split()))


def object_adress(name):
    response = requests.get(GEOKODER_API_SERVER, params={
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": name,
        "format": "json"
    }).json()
    if not response:
        return None
    return response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]["metaDataProperty"
                                         ]["GeocoderMetaData"]["Address"]["formatted"]