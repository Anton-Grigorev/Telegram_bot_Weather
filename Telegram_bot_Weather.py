import telebot                                  # Импорт модуля Telebot, который используется для создания и управления телеграм-ботом.
import requests                                 # Импорт модуля Requests, который используется для отправки HTTP-запросов.
import json                                     # Импорт модуля JSON, который используется для работы с данными в формате JSON.

# Создание объекта бота с использованием указанного токена.
bot = telebot.TeleBot(token='YOUR TOKEN')

# Ключ API для доступа к сервису OpenWeather (https://openweathermap.org/)
API_OpenWeather = 'YOUR API'


@bot.message_handler(commands=['start'])        # Обработчик команды /start
def start(message):
    # Отправка сообщения с приветствием и просьбой указать название города.
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name} {message.from_user.last_name}! 🤝\n'
                                      f'Напиши название города для показа данных о температуре')



@bot.message_handler(content_types=['text'])    # Обработчик текстовых сообщений
def get_city(message):
    # Получение названия города из сообщения пользователя и приведение к нижнему регистру.
    city = message.text.strip().lower()

    try:
        # Отправка HTTP-запроса к сервису OpenWeather для получения данных о погоде в указанном городе.
        response = requests.get(
            f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_OpenWeather}&units=metric&lang=ru')

        # Извлечение необходимых данных о погоде из JSON-ответа.
        temp = json.loads(response.content)['main']['temp']
        feels_like = json.loads(response.content)['main']['feels_like']
        temp_min = json.loads(response.content)['main']['temp_min']
        temp_max = json.loads(response.content)['main']['temp_max']
        pressure = json.loads(response.content)['main']['pressure']
        humidity = json.loads(response.content)['main']['humidity']
        visibility = json.loads(response.content)['visibility']
        description = json.loads(response.content)['weather'][0]['description']

        # Определение эмоджи в зависимости от описания погоды.
        def emoji(description):
            if description == 'пасмурно':
                return '⛅️'
            if description == 'облачно с прояснениями':
                return '🌤️'
            if description == 'небольшая облачность':
                return '🌤️'
            if description == 'ясно':
                return '☀️️'

    except KeyError:
        # Обработка исключения, если указанный город не найден.
        bot.reply_to(message, f'Неверное написание города - {city} 🙈')
    else:
        # Отправка сообщения с данными о погоде в указанном городе.
        bot.reply_to(message, f'Сейчас погода: {temp} градус(а)ов   🌡\n'
                              f'Ощущается как: {feels_like} градус(а)ов   🌡\n'
                              f'Минимальная температура: {temp_min} градус(а)ов   ↘️\n'
                              f'Максимальная температура: {temp_max} градус(а)ов   ⬆️\n'
                              f'Давление: {pressure}   🔴\n'
                              f'Влажность: {humidity}   💧\n'
                              f'Видимость: {visibility} метров   🔭\n'
                              f'Состояние: {description}  {emoji(description)}')



bot.polling(none_stop=True)                 # Запуск бота