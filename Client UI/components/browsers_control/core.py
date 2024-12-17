import logging
from PyQt5 import QtCore

from .. import settings
from .webdriver import Driver
from importlib import import_module

logger = logging.getLogger('Client UI.components.browsers_control.core')


class BrowserControl:
    diag_signal = QtCore.pyqtSignal(str)
    bet_params = dict

    def start(self):
        control_modules_list = self.__get_control_modules()
        for control_module in control_modules_list:
            pass


        # driver_dict = Driver(settings.BOOKMAKERS.get('leon')).get_driver()
        # webdriver = driver_dict.get("driver")
        # self.render_diagnostics(driver_dict.get("status"))

    @staticmethod
    def __get_control_modules() -> list:
        """Получение списка доступных модулей управления вебстраницами букмекеров"""
        module_list = []
        for bkmkr_name in settings.BOOKMAKERS.keys():
            try:
                module = import_module(f'.browsers_control.websites_control_modules.{bkmkr_name}', package='components')
            except BaseException as ex:
                logger.error(ex)
                continue
            module_list.append(module)
        return module_list



if __name__ == '__main__':
    pass
