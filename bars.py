import json, sys, os


def load_data(file_path):
    if not os.path.exists(file_path):
        return None
    with open(file_path, 'r', encoding='UTF-8') as file:
        file_content = file.read()
    try:
        return json.loads(file_content)['features']
    except json.JSONDecodeError:
        return None


def get_seats_count(bar):
    return bar['properties']['Attributes']['SeatsCount']


def get_biggest_bar(bars):
    biggest_bar = max(bars, key=get_seats_count)
    return biggest_bar


def get_smallest_bar(bars):
    smallest_bar = min(bars, key=get_seats_count)
    return smallest_bar


def get_coordinates(bar):
    return bar['geometry']['coordinates']


def calc_distance(bar, user_longitude, user_latitude):
    """for simplicity, the distance is calculated by the Pythagorean theorem:"""
    long_distance = get_coordinates(bar)[0] - user_longitude
    lat_distance = get_coordinates(bar)[1] - user_latitude
    distance = (long_distance**2 + lat_distance**2)**0.5
    return distance


def get_closest_bar(bars, longitude, latitude):
    return min(bars, key=lambda x: calc_distance(x, longitude, latitude))


def get_bars_short_info(bar):
    return '{}\nРасположен по адресу: {}\n'.format(
        bar['properties']['Attributes']['Name'],
        bar['properties']['Attributes']['Address']
    )


if __name__ == '__main__':
    if len(sys.argv) == 2:
        file_path = sys.argv[1]
    else:
        file_path = 'bars.json'

    if load_data(file_path):
        bars = load_data(file_path)
    else:
        exit('Файл не найден или имеет недопустимый формат')

    print('Самый большой бар: ' + get_bars_short_info(get_biggest_bar(bars)))

    print('Самый маленький бар: '  + get_bars_short_info(get_smallest_bar(bars)))

    choice = input('Хотите узнать где находиться ближайший бар? (да\\нет):\n').lower()
    if choice not in ['д', 'да', 'y', 'yes']:
        exit()

    coordinates = [input('Введите координату долготы:\n'),
                   input('Введите координату широты:\n')]
    try:
        coordinates = list(map(float, coordinates))
        print('Ближайший к вам бар: ' +
              get_bars_short_info(get_closest_bar(bars, coordinates[0], coordinates[1]))
              )
    except ValueError:
        exit('Неверный формат координат.')
