import json, requests


def load_data(filepath):
    file = requests.get(filepath)
    return json.loads(file.text, encoding='UTF-8')['features']


def get_biggest_bar(data):
    biggest = data[0]
    max_seats_count = biggest['properties']['Attributes']['SeatsCount']
    for bar in data:
        if bar['properties']['Attributes']['SeatsCount'] > max_seats_count:
            max_seats_count = bar['properties']['Attributes']['SeatsCount']
            biggest = bar
    return biggest


def get_smallest_bar(data):
    smallest = data[0]
    smallest_seats_counter = smallest['properties']['Attributes']['SeatsCount']
    for bar in data:
        if bar['properties']['Attributes']['SeatsCount'] < smallest_seats_counter:
            smallest_seats_counter = bar['properties']['Attributes']['SeatsCount']
            smallest = bar
    return smallest


def get_closest_bar(data, longitude, latitude):
    closest = data[0]
    smallest_distance = calc_coordinate_distance(longitude,
                                                 latitude,
                                                 closest['geometry']['coordinates'][0],
                                                 closest['geometry']['coordinates'][1])

    for bar in data:
        current_distance = calc_coordinate_distance(longitude,
                                                    latitude,
                                                    bar['geometry']['coordinates'][0],
                                                    bar['geometry']['coordinates'][1])
        if current_distance < smallest_distance:
            smallest_distance = current_distance
            closest = bar
    return closest


def calc_coordinate_distance(x1,y1,x2,y2):
    # for simplicity, the distance is calculated by the Pythagorean theorem:
    distance = ((x1-x2)**2 + (y1-y2)**2)**0.5
    return distance


if __name__ == '__main__':
    bars_list = load_data(
        'https://devman.org/media/filer_public/95/74/957441dc-78df-4c99-83b2-e93dfd13c2fa/bars.json'
    )
    while True:
        try:
            user_longitude = float(input('Введите текущую долготу: \n'))
            user_latitude = float(input('Введите текущую широту: \n'))
            print()
            break
        except ValueError:
            print("Неверный формат координат, повторите ввод")

    biggest_bar = get_biggest_bar(bars_list)
    print("Самый большой бар - {}\nАдрес:{}\n".format(
        biggest_bar['properties']['Attributes']['Name'],
        biggest_bar['properties']['Attributes']['Address']
    ))

    smallest_bar = get_smallest_bar(bars_list)
    print("Самый маленький бар - {}\nАдрес: {}\n".format(
        smallest_bar['properties']['Attributes']['Name'],
        smallest_bar['properties']['Attributes']['Address']
    ))

    closest_bar = get_closest_bar(bars_list, user_longitude, user_latitude)
    print("Ближайший бар - {}\nАдрес: {}\n".format(
        closest_bar['properties']['Attributes']['Name'],
        closest_bar['properties']['Attributes']['Address']
    ))


