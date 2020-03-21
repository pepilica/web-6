import requests
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('address', nargs='+', type=str)
args = parser.parse_args()

if args.address:
    toponym_to_find = " ".join(args.address)
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

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
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        'kind': 'district',
        "lang": "ru_RU",
        "geocode": toponym_coodrinates.replace(' ', ','),
        "format": "json"
    }
    response = requests.get(geocoder_api_server, params=search_params).json()
    try:
        print(response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]['name'])
    except IndexError:
        print("District can\'t be calculated")
else:
    print('Wrong query')