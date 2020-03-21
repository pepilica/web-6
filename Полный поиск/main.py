from io import BytesIO
import requests
from PIL import Image
import argparse
from get_coords import get_bbox


parser = argparse.ArgumentParser()
parser.add_argument('--spn', nargs=2, type=str)
parser.add_argument('address', nargs='+', type=str)
args = parser.parse_args()
spn = ','.join(args.spn)

if args.address:
    toponym_to_find = " ".join(args.address)
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": toponym_to_find,
        "format": "json"
    }

    response = requests.get(geocoder_api_server, params=geocoder_params)

    if not response:
        print('Wrong query')
        exit(0)

    json_response = response.json()
    toponym = json_response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]
    toponym_coodrinates = toponym["Point"]["pos"]
    info = toponym['boundedBy']['Envelope']
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")

    map_params = {
        "ll": ",".join([toponym_longitude, toponym_lattitude]),
        'spn': spn,
        "l": "map",
        "pt": ",".join([toponym_longitude, toponym_lattitude]),
        'bbox': get_bbox(info)
    }

    map_api_server = "http://static-maps.yandex.ru/1.x/"
    response = requests.get(map_api_server, params=map_params)

    Image.open(BytesIO(
        response.content)).show()
else:
    print('Wrong query')