import requests
import logging

logger = logging.getLogger('Client UI.components.telegram_sender')


class TelegramSender:
    """Класс включения и взаимодействия с телеграмм-ботом"""
    message_switch = False

    @staticmethod
    def send_text(text: str) -> None:
        """Отправка текста"""
        if TelegramSender.message_switch:
            try:
                token = "5619069193:AAGNIzLkQUo7mX4aglRXRnvc904C_4jbqCM" #токен бота
                chat_id = "@Python_test_g" #айди или ссылка-приглашение группы в телеграм
                url_req = "https://api.telegram.org/bot" + token + "/sendMessage" + "?chat_id=" + chat_id + "&text=" + text
                requests.get(url_req)
            except Exception as ex:
                logger.info(f'Ошибка отправки текстового сообщения в телеграмм, {ex}')

    @staticmethod
    def send_photo(pngPath: str) -> None:
        """Отправка скриншотов"""
        if TelegramSender.message_switch:
            try:
                token = "5619069193:AAGNIzLkQUo7mX4aglRXRnvc904C_4jbqCM"  # токен бота
                chat_id = "@Python_test_g"  # айди или ссылка-приглашение группы в телеграм
                request_url = "https://api.telegram.org/bot" + token + "/sendMediaGroup"
                params = {"chat_id": chat_id, "media":"""[{"type": "photo", "media": "attach://random-name-1"}]"""}
                files = {"random-name-1": open(f"{pngPath}", "rb")} # ссылка на локальный файл
                requests.post(request_url, params=params, files=files)
            except Exception as ex:
                logger.info(f'Ошибка отправки скриншота в телеграмм, {ex}')

    @staticmethod
    def send_xlsx(xlsxPath: str) -> None:
        """Отправка Excel-файлов"""
        if TelegramSender.message_switch:
            try:
                token = "5619069193:AAGNIzLkQUo7mX4aglRXRnvc904C_4jbqCM"  # токен бота
                chat_id = "@Python_test_g"  # айди или ссылка-приглашение группы в телеграм
                request_url = "https://api.telegram.org/bot" + token + "/sendMediaGroup"
                params = {"chat_id": chat_id, "media":"""[{"type": "document", "media": "attach://random-name-1"}]"""}
                files = {"random-name-1": open(f"{xlsxPath}", "rb")} # ссылка на локальный файл
                requests.post(request_url, params=params, files=files)
            except Exception as ex:
                logger.info(f'Ошибка отправки статистики (xlsx) в телеграмм, {ex}')

    @staticmethod
    def bot_state(var: bool) -> None:
        """Установка разрешения на отправку сообщений"""
        TelegramSender.message_switch = var
        if var:
            logger.info('Включена отправка сообщений в телеграм')
            TelegramSender.send_text('Interaction with telegram is enabled. Standing by...')
        else:
            logger.info('Выключена отправка сообщений в телеграм')
            TelegramSender.send_text('App turned off')
