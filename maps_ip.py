import requests
from PyQt5.QtGui import QPixmap
MAP_API_SERVER = "http://static-maps.yandex.ru/1.x/"
GEOKODER_API_SERVER = "http://geocode-maps.yandex.ru/1.x/"
ORGANIZATION_SEARCH_API_SERVER = "https://search-maps.yandex.ru/v1/"
import math
def lonlat_distance(a, b):

    degree_to_meters_factor = 111 * 1000
    a_lon, a_lat = a
    b_lon, b_lat = b

    radians_lattitude = math.radians((a_lat + b_lat) / 2.)
    lat_lon_factor = math.cos(radians_lattitude)

    dx = abs(a_lon - b_lon) * degree_to_meters_factor * lat_lon_factor
    dy = abs(a_lat - b_lat) * degree_to_meters_factor

    distance = math.sqrt(dx * dx + dy * dy)

    return distance <= 50


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


def get_object_postal_code(name):
    response = requests.get(GEOKODER_API_SERVER, params={
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": name,
        "format": "json"
    }).json()
    if not response:
        return None
    try:
        return response["response"]["GeoObjectCollection"][
            "featureMember"][0]["GeoObject"]["metaDataProperty"
                                             ]["GeocoderMetaData"]["Address"]["postal_code"]
    except Exception:
        return None


def search_organization(name):
    response = requests.get(ORGANIZATION_SEARCH_API_SERVER, params={
        "apikey": "12ecf2f5-4503-40ec-bd7d-fd704013dd32",
        "text": object_adress(name),
        "lang": "ru_RU",
        "type": "biz",
        "spn": "5,5",
        "ll": name}).json()
    if not response:
        return None
    for i in range(len(response["features"])): 
        adress = response["features"][i]["properties"]["CompanyMetaData"]["name"]
        coords = response["features"][i]["geometry"]["coordinates"]
        if lonlat_distance(list(map(float, name.split(","))), coords):
            return adress, coords