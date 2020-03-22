import requests
import os
import pygame
from random import choices


pygame.init()
cities = ['Альметьевск', 'Москва', 'Нью-Йорк', "Токио", "Филадельфия", "Санкт-Петербург",
          "Казань", 'Рим', 'Набережные Челны', 'Калькутта', 'Макао']

geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
map_api_server = "http://static-maps.yandex.ru/1.x/"


def get_picture():
    city = choices(cities)
    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": city,
        "format": "json"
    }

    response_toponym = requests.get(geocoder_api_server, params=geocoder_params)

    json_response = response_toponym.json()
    toponym = json_response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]
    toponym_coodrinates = toponym["Point"]["pos"]
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")

    spn = choices(list(map(lambda a: a * 0.001, range(1, 201))))[0]
    map_params = {
        "l": "sat",
        'spn': str(spn) + ',' + str(spn),
        'll': str(toponym_longitude) + ',' + str(toponym_lattitude),
        'size': '600,450'
    }

    response = requests.get(map_api_server, params=map_params)
    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)
    return city


screen = pygame.display.set_mode((600, 450))
city = get_picture()[0]
map_file = "map.png"
image = pygame.image.load(map_file)
screen.blit(image, (0, 0))
pygame.display.flip()
running = True
current = 0
is_solved = False
while running:
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            running = False
        if i.type == pygame.KEYDOWN:
            if i.key == pygame.K_SPACE:
                if not is_solved:
                    font = pygame.font.Font(None, 50)
                    text = font.render(city, 1, (0, 0, 0))
                    screen.blit(text, (600 // 2 - text.get_width() // 2, 450 // 2 - text.get_height() // 2))
                    is_solved = True
                else:
                    city = get_picture()[0]
                    image = pygame.image.load(map_file)
                    screen.blit(image, (0, 0))
                    os.remove("map.png")
                    is_solved = False
    pygame.display.flip()
pygame.quit()
