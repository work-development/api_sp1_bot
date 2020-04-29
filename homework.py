import os
import requests
import telegram
import time
from dotenv import load_dotenv

load_dotenv()


PRACTICUM_TOKEN = os.getenv("PRACTICUM_TOKEN")
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')


def parse_homework_status(homework):

    homework_name = homework['homework_name']
    if homework['status'] != 'approved':
        verdict = 'К сожалению в работе нашлись ошибки.'
    else:
        verdict = 'Ревьюеру всё понравилось, можно приступать к следующему уроку.'
    return f'У вас проверили работу "{homework_name}"!\n\n{verdict}'


def get_homework_statuses(current_timestamp):
    url = 'https://praktikum.yandex.ru/api/user_api/homework_statuses/'
    headers = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}
    params = {"from_date": current_timestamp}
    homework_statuses = requests.get(url = url, headers = headers, params = params)

    return homework_statuses.json()


def send_message(message):
    proxy = telegram.utils.request.Request(proxy_url='socks5://97.74.230.16:31178/')  #'https://51.15.165.185:5836'
    bot = telegram.Bot(token=TELEGRAM_TOKEN, request=proxy)

    return bot.send_message(chat_id = CHAT_ID, text=message)


def main():
    current_timestamp = int(time.time())  # начальное значение timestamp
    current_timestamp = 0
    while True:
        try:
            new_homework = get_homework_statuses(current_timestamp)
            if new_homework.get('homeworks'):
                send_message(parse_homework_status(new_homework.get('homeworks')[0]))
            current_timestamp = new_homework.get('current_date')  # обновить timestamp
            time.sleep(900)  # опрашивать раз в 15 минут

        except Exception as e:
            print(f'Бот упал с ошибкой: {e}')
            time.sleep(5)
            continue


if __name__ == '__main__':
    main()
