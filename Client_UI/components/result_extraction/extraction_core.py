import logging

from PyQt5 import QtCore
from PyQt5.QtCore import QObject, QThread, QSettings

from ..browsers_control import result_parsers_sync

logger = logging.getLogger('Client_UI.components.result_extraction.extraction_core')


class ResultExtractor(QObject):
    """Класс получение результатов событий, на которые сделаны ставки"""
    diag_signal = QtCore.pyqtSignal(str)
    finish_signal = QtCore.pyqtSignal(dict)

    def __init__(self, extraction_classes: dict, active_bets_list: QSettings, control_settings: dict) -> None:
        super(ResultExtractor, self).__init__()
        self.extraction_classes = extraction_classes
        self.active_bets_list = active_bets_list
        self.active_bets_data = {x: self.active_bets_list.value(x) for x in self.active_bets_list.allKeys()}  # вид данных active_bets_urls=str(bookmaker$$url)
        self.control_settings = control_settings
        self.all_extracted_results = {}

    def start_extraction_modules(self) -> None:
        """Запуск методов извлечения результатов"""
        try:
            for pars_method_name, pars_class in self.extraction_classes.items():

                if QThread.currentThread().isInterruptionRequested():
                    message = "Процесс получения результатов по сделанным ставкам прерван пользователем"
                    logger.info(message)
                    self.diag_signal.emit(message)
                    self.finish_signal.emit({})
                    return

                message = f"Получение данных о результатах событий ({pars_method_name})"
                logger.info(message)
                self.diag_signal.emit(message)

                ResultExtractionClass = getattr(result_parsers_sync, pars_class)

                if pars_method_name == 'SELENIUM':
                    ResultExtractionClass.page_load_timeout = self.control_settings['timeouts']['result_page_load_timeout']

                results = ResultExtractionClass(self.active_bets_data, self.diag_signal).start()

                if not results:
                    continue

                self.all_extracted_results.update(results)
                finished = self.__process_results(results)
                if finished:
                    self.finish_signal.emit(self.all_extracted_results)
                    return

            self.finish_signal.emit(self.all_extracted_results)

        except BaseException as ex:
            logger.error(ex)

    def __process_results(self, results: dict) -> bool | None:
        """Оценка полноты полученных результатов"""

        for result_key in results.keys():
            try:
                self.active_bets_list.remove(result_key)
            except BaseException as ex:
                logger.info(ex)

        if not self.active_bets_list.allKeys():
            message = "Завершен процесс получения данных о результатах событий с ранее размещенными ставками. " \
                      "Данные получены по всем сделанным ставкам"
            logger.info(message)
            self.diag_signal.emit(message)
            return True

