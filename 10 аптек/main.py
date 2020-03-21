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
        "featureMember"][0]["GeoObject"]
    toponym_coodrinates = toponym["Point"]["pos"]
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")

    search_params = {
        "apikey": "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3",
        "text": "аптека",
        "lang": "ru_RU",
        "ll": toponym_coodrinates.replace(' ', ','),
        "type": "biz"
    }

    response_pharmacy = requests.get(search_api_server, params=search_params).json()
    points = []
    for number in range(10):
        organization = response_pharmacy["features"][number]
        org_name = organization["properties"]["CompanyMetaData"]["name"]
        org_address = organization["properties"]["CompanyMetaData"]["address"]
        org_hours = organization["properties"]["CompanyMetaData"]['Hours']
        point = organization["geometry"]["coordinates"]
        org_point = "{0},{1}".format(point[0], point[1])
        if 'Availabilities' in org_hours.keys():
            if 'TwentyFourHours' in org_hours['Availabilities'][0].keys():
                points.append(org_point + ',pmgns')
            else:
                points.append(org_point + ',pmbls')
        else:
            points.append(org_point + ',pmgrs')
        print(number)
        print('Name: ' + org_name)
        print('Address: ' + org_address)
        print('Working hours: ' + org_hours['text'])
        print(
            'Distance: ' + '%.1f' % (lonlat_distance([point[0], point[1]], map(float, toponym_coodrinates.split(' '))))
            + 'метров')
        print('---------------')
    map_params = {
        "l": "map",
        "pt": '~'.join([",".join([toponym_longitude, toponym_lattitude])] + points)
    }
    map_api_server = "http://static-maps.yandex.ru/1.x/"
    response = requests.get(map_api_server, params=map_params)

    Image.open(BytesIO(
        response.content)).show()
else:
    print('Wrong query')