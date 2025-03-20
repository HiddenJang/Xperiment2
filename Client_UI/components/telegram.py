import requests
import logging

logger = logging.getLogger('Client_UI.components.telegram')


class TelegramService:
    """Класс включения и взаимодействия с телеграм-ботом"""
    messages_on = False
    token = ""  # токен бота
    group_id = ""  # айди или ссылка-приглашение группы в телеграм

    @staticmethod
    def send_text(text: str, finishing: bool = False) -> None:
        """Отправка текста"""
        if TelegramService.messages_on or finishing:
            try:
                text_url = "https://api.telegram.org/bot" + TelegramService.token + \
                           "/sendMessage" + "?chat_id=" + TelegramService.group_id + "&text=" + text
                requests.get(text_url)
            except BaseException as ex:
                logger.info(f'Ошибка отправки текстового сообщения в telegram: {ex}')

    @staticmethod
    def send_photo(img_path: str) -> None:
        """Отправка скриншотов"""
        if TelegramService.messages_on:
            try:
                media_url = "https://api.telegram.org/bot" + TelegramService.token + "/sendMediaGroup" + \
                            "?chat_id=" + TelegramService.group_id + \
                            "&media=%5B%7B%22type%22%3A+%22photo%22%2C+%22media%22%3A+%22attach%3A%2F%2Frandom-name-1%22%7D%5D"
                files = {"random-name-1": open(f"{img_path}", "rb")}
                requests.post(media_url, files=files)
            except BaseException as ex:
                logger.info(f'Ошибка отправки скриншота в telegram: {ex}')

    @staticmethod
    def send_xlsx(xlsx_path: str) -> None:
        """Отправка Excel-файлов"""
        if TelegramService.messages_on:
            try:
                media_url = "https://api.telegram.org/bot" + TelegramService.token + "/sendMediaGroup" + \
                            "?chat_id=" + TelegramService.group_id + \
                            "&media=%5B%7B%22type%22%3A+%22document%22%2C+%22media%22%3A+%22attach%3A%2F%2Frandom-name-1%22%7D%5D"
                files = {"random-name-1": open(f"{xlsx_path}", "rb")}
                requests.post(media_url, files=files)
            except BaseException as ex:
                logger.info(f'Ошибка отправки статистики (xlsx) в telegram: {ex}')

    @staticmethod
    def turn_on(state: bool) -> None:
        """Установка разрешения на отправку сообщений"""
        TelegramService.messages_on = state
        if state:
            logger.info('Включена отправка сообщений в telegram')
            TelegramService.send_text('Включена отправка сообщений в telegram')
        else:
            logger.info('Выключена отправка сообщений в telegram')
            TelegramService.send_text('Выключена отправка сообщений в telegram', finishing=True)
