import json


def load_data(file_path):
    with open(file_path, 'r', encoding='UTF-8') as f:
        return json.loads(f.read())['features']


def parse_seats_count(bar):
    return bar['properties']['Attributes']['SeatsCount']


def get_biggest_bar(bars):
    biggest_bar = max(bars, key=parse_seats_count)
    return biggest_bar


def get_smallest_bar(bars):
    smallest_bar = min(bars, key=parse_seats_count)
    return smallest_bar


def get_coordinates(bar):
    return bar['geometry']['coordinates']


def calc_distance(bar, user_point):
    """for simplicity, the distance is calculated by the Pythagorean theorem:"""
    long_distance = get_coordinates(bar)[0] - user_point[0]
    lat_distance = get_coordinates(bar)[1] - user_point[1]
    distance = (long_distance**2 + lat_distance**2)**0.5
    bar['distance'] = distance
    return bar


def get_closest_bar(bars, longitude, latitude):
    for bar in bars:
        calc_distance(bar, (longitude, latitude))
    return min(bars, key=lambda bar: bar['distance'])


if __name__ == '__main__':
    file_path = 'bars.json'
    bars = load_data(file_path)
    print('Самый большой бар - {}\nРасположен по адресу:{}\n'.format(
        get_biggest_bar(bars)['properties']['Attributes']['Name'],
        get_biggest_bar(bars)['properties']['Attributes']['Address']
    )

    )
    print('Самый маленький бар - {}\nРасположен по адресу:{}\n'.format(
        get_smallest_bar(bars)['properties']['Attributes']['Name'],
        get_smallest_bar(bars)['properties']['Attributes']['Address']
    ))

    choice = input('Хотите узнать где находиться ближайший бар? (да\\нет):\n').lower()
    if choice not in ['д', 'да', 'y', 'yes']:
        exit()
    while True:
        coordinates = [input('Введите координату долготы:\n'),
                       input('Введите координату широты:\n')]
        try:
            coordinates = list(map(float, coordinates))
            print('Ближайший к вам бар - {}\nРасположен по адресу:{}\n'.format(
                get_closest_bar(bars, coordinates[0], coordinates[1])['properties']['Attributes']['Name'],
                get_closest_bar(bars, coordinates[0], coordinates[1])['properties']['Attributes']['Address']
            ))
            break
        except ValueError:
            print("Неверный формат координат, повторите ввод")
