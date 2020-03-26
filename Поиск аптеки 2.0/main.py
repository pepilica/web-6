from io import BytesIO
import requests
from PIL import Image
import argparse
from get_coords import get_bbox
from distance import lonlat_distance


parser = argparse.ArgumentParser()
parser.add_argument('--spn', nargs=2, type=str)
parser.add_argument('address', nargs='+', type=str)
args = parser.parse_args()
if args.spn:
    spn = ','.join(args.spn)
else:
    spn = '0,0'

if args.address:
    toponym_to_find = " ".join(args.address)
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
    search_api_server = "https://search-maps.yandex.ru/v1/"

    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": toponym_to_find,
        "format": "json"
    }

    response_toponym = requests.get(geocoder_api_server, params=geocoder_params)

    if not response_toponym:
        print('Wrong query')
        exit(0)

    json_response = response_toponym.json()
    toponym = json_response["response"]["GeoObjectCollection"][
        "featureMember"]
    if toponym:
        toponym_coodrinates = toponym[0]["GeoObject"]["Point"]["pos"]
        toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")

        search_params = {
            "apikey": "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3",
            "text": "аптека",
            "lang": "ru_RU",
            "ll": toponym_coodrinates.replace(' ', ','),
            "type": "biz"
        }

        response_pharmacy = requests.get(search_api_server, params=search_params).json()
        if response_pharmacy['features']:
            organization = response_pharmacy["features"][0]
            org_name = organization["properties"]["CompanyMetaData"]["name"]
            org_address = organization["properties"]["CompanyMetaData"]["address"]
            org_hours = organization["properties"]["CompanyMetaData"]
            point = organization["geometry"]["coordinates"]
            org_point = "{0},{1}".format(point[0], point[1])
            print('Name: ' + org_name)
            print('Address: ' + org_address)
            if 'Hours' in org_hours:
                print('Working hours: ' + org_hours['Hours']['text'])
            else:
                print('Working hours: ?')
            print(
                'Distance: ' + '%.1f' % (lonlat_distance([point[0], point[1]]
                                                         , map(float, toponym_coodrinates.split(' '))))
                + 'метров')
            print('---------------')

            map_params = {
                "l": "map",
                "pt": ",".join([toponym_longitude, toponym_lattitude]) + '~' + org_point
            }

            map_api_server = "http://static-maps.yandex.ru/1.x/"
            response = requests.get(map_api_server, params=map_params)

            Image.open(BytesIO(
                response.content)).show()
        else:
            print('Not found')
    else:
        print('Wrong query')
else:
    print('Wrong query')