import requests
import logging
import urllib

logger = logging.getLogger('Client UI.components.telegram_message_service')


class TelegramService:
    """Класс включения и взаимодействия с телеграмм-ботом"""
    messages_on = False
    token = ""  # токен бота
    group_id = ""  # айди или ссылка-приглашение группы в телеграм

    @staticmethod
    def send_text(text: str) -> None:
        """Отправка текста"""
        if TelegramService.messages_on:
            try:
                text_url = "https://api.telegram.org/bot" + TelegramService.token + \
                           "/sendMessage" + "?chat_id=" + TelegramService.group_id + "&text=" + text
                requests.get(text_url)
            except BaseException as ex:
                logger.info(f'Ошибка отправки текстового сообщения в телеграмм: {ex}')

    @staticmethod
    def send_photo(img_path: str) -> None:
        """Отправка скриншотов"""
        if TelegramService.messages_on:
            try:
                media_url = "https://api.telegram.org/bot" + TelegramService.token + "/sendMediaGroup"
                params = {"group_id": TelegramService.group_id,
                          "media": """[{"type": "photo", "media": "attach://random-name-1"}]"""}
                files = {"random-name-1": open(img_path, "rb")}
                requests.post(media_url, params=params, files=files)
            except BaseException as ex:
                logger.info(f'Ошибка отправки скриншота в телеграмм: {ex}')

    @staticmethod
    def send_xlsx(xlsx_path: str) -> None:
        """Отправка Excel-файлов"""
        if TelegramService.messages_on:
            try:
                media_url = "https://api.telegram.org/bot" + TelegramService.token + "/sendMediaGroup"
                params = {"group_id": TelegramService.group_id,
                          "media": """[{"type": "document", "media": "attach://random-name-1"}]"""}
                files = {"random-name-1": open(xlsx_path, "rb")}
                requests.post(media_url, params=params, files=files)
            except BaseException as ex:
                logger.info(f'Ошибка отправки статистики (xlsx) в телеграмм: {ex}')

    @staticmethod
    def turn_on(state: bool) -> None:
        """Установка разрешения на отправку сообщений"""
        TelegramService.messages_on = state
        if state:
            logger.info('Включена отправка сообщений в телеграм')
            TelegramService.send_text('Interaction with telegram is enabled. Standing by...')
        else:
            logger.info('Выключена отправка сообщений в телеграм')
            TelegramService.send_text('App turned off')
