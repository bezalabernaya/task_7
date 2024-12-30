import requests
import datetime
from dateutil import tz
from database import DateBase
API_key = 'f44eef61e43ffa3eaa3fa6e4ced549e4'


def start():
    print('Привет! Вас мучает вопрос в чем выйти на улицу? Посмотрим, чем я смогу помочь!\n'
          '1 - Погода за окном\n'
          '2 - Погода в городе N\n'
          '3 - История запросов\n'
          '4 - Завершение работы\n')

    option = input()

    if option == '1':
        start_1()
    elif option == '2':
        print('Введите название интересующего Вас города')
        start_2()
    elif option == '3':
        print("Введите количество запросов, которое вы хотели бы увидеть")
        start_3()
    elif option == '4':
        print('До встречи!😘')
    else:
        print("Введите корректное значение")
        return start()


def start_1():
    city = get_city_by_ip()
    lat, lon, city_tr = get_lan_lon_by_city(city)
    output(get_weather_by_lon_lan(lat, lon, city_tr))
    return start()


def start_2():
    try:
        city = input()
        lat, lon, city_tr = get_lan_lon_by_city(city)
        output(get_weather_by_lon_lan(lat, lon, city_tr))
    except Exception:
        print('Похоже такого города нет, побробуйте другое название')
        return start_2()
    else:
        return start()


def start_3():
    try:
        num = int(input())
        with database as db:
            db.select_data(num=num)
    except ValueError:
        print('Введите целое число или цифру')
        return start_3()
    except IndexError:
        print(f"Введите значение от 1 до {database.history_len}\n")
        return start_3()
    else:
        return start()


def get_city_by_ip():
    response = requests.get(f"http://ip-api.com/json/").json()
    return response["city"]


def get_lan_lon_by_city(city):
    response = requests.get(f'http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=5&appid={API_key}').json()
    return response[0]["lat"], response[0]["lon"], response[0]["local_names"]["ru"]


def get_weather_by_lon_lan(lat, lon, city):
    response = requests.get(
    f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_key}&units=metric&lang=ru').json()

    temperature = str(response['main']['temp'])
    feels_like = str(response['main']['feels_like'])
    weather = str(response['weather'][0]['description'])
    wind_speed = str(response['wind']['speed'])
    date = datetime.datetime.now(tz=tz.tzlocal()).strftime("%Y-%m-%d %H:%M:%S %z")

    weather_info = [date, city,  weather, temperature, feels_like, wind_speed]
    with database as db:
        db.insert_data(info=weather_info)

    return weather_info


def output(info):
    print(f'''Текущее время: {info[0]}
Название города: {info[1]}
Погодные условия: {info[2]}
Текущая температура: {info[3]} градусов по цельсию
Ощущается как: {info[4]} градусов по цельсию
Скорость ветра: {info[5]} м/c\n''')


if __name__ == "__main__":
    database = DateBase()
    with database as db:
        db.create_table()
    start()