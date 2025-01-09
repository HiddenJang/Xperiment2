import os
import logging
from time import sleep

from openpyxl import Workbook
from openpyxl import load_workbook
from openpyxl.styles import colors
from openpyxl.styles import Border, Side
from openpyxl.styles import Font, Color
from openpyxl.styles import PatternFill

logger = logging.getLogger('Client UI.components.statistic_management.statistic')


class Statistic:
    """Формирование статистики и запись в файл xlsx"""
    columns = ("№  ", "Команды БК1", "Команды БК2", "ТМ/Коэфф. БК1", "ТБ/Коэфф. БК2", "ТБ/Коэфф. БК1", "ТМ/Коэфф. БК2",
               "Коэффициент БК1", "Коэффициент БК2", "Скриншот БК1", "Скриншот БК2", "Ссылка БК1", "Ссылка БК2",
               "Ставка БК1", "Результат БК1", "Банкрол БК1", "Ставка БК2", "Результат БК2", "Сумма голов", "Дата БК1",
               "Дата БК2")
    font = 'Calibri'
    font_size = 12

    def __init__(self, imitation: bool, event_data: list):
        self.imitation = imitation
        self.event_data = event_data

    #event: list, shotname_after: str, element_takecoeff: list, bet_size: int
    def insert_data(self): # получение данных о найденном событии из модуля GraphicalMODULE_1 функция tree_on_select
        if not os.path.exists(settings.STATS_DIR):
            os.mkdir(settings.STATS_DIR)

        if not os.path.exists(settings.STATS_FILE_NAME):
            wb = Workbook()
            ws_betting = wb.active
            ws_betting.title = "Ставки на деньги"
            for col in range(1, len(self.columns)+1):
                cell = ws_betting.cell(row=1, column=col, value=self.columns[col-1])

                # выравнивание по ширине ячейки
                cell.font = Font(name=self.font, size=self.font_size)
                len_cell = len(str(cell.value))
                new_width_col = len_cell * self.font_size ** (self.font_size * 0.01)
                ws_betting.column_dimensions[cell.column_letter].width = new_width_col

            ws_betting.column_dimensions['B'].width = 30
            ws_betting.column_dimensions['C'].width = 30

            ws_imitation = wb.copy_worksheet(ws_betting)
            ws_imitation.title = "Имитация ставок"

        else:
            for _ in range(5):
                try:
                    wb = load_workbook(settings.STATS_FILE_NAME)
                    break
                except BaseException as ex:
                    logger.info(f'Ошибка открытия файла статистики, {ex}')
                    if _ == 4:
                        logger.info(f'Не удалось получить доступ к файлу статистики, {ex}')
                        return
                    sleep(0.5)

        if self.imitation:
            ws = wb["Имитация ставок"]
        else:
            ws = wb["Ставки на деньги"]

        empty_row_num = len(ws['A']) + 1


        #     # стираем значения ИТОГО ранее занесенные в столбцы 15 и 18
        #     ws.cell(row=row, column=15).value = None
        #     ws.cell(row=row, column=18).value = None
        # # проверки наличия в файле стартовых банкролов 10000 в соответствующих столбцах и присвоение последних значений банкролов
        # for i in range(2, row+1):
        #     if ws.cell(row=i, column=16).value != None:
        #         bankrol_first = ws.cell(row=i, column=16).value
        #         l+=1
        #     if ws.cell(row=i, column=19).value != None:
        #         bankrol_second = ws.cell(row=i, column=19).value
        #         x+=1
        # if l == 0:
        #     bankrol_first = '10000'
        # if x == 0:
        #     bankrol_second = '10000'
        # ws.cell(row=row, column=1, value=row) # внесение в первый столбец номера строки
        # for i in range(0,len(event_data)-2):
        #     ws.cell(row=row, column=(i+2), value=event_data[i])  # обращаясь к листу записываем по координатам ячейки (row,column) значение (данные), 4 штуки - имя, цена, и т.д.
        # if element_takecoeff[0] == 'LEON':
        #     if 'leon.ru' in event[6]:
        #         ws.cell(row=row, column=8, value=element_takecoeff[1])
        #         ws.cell(row=row, column=10, value=shotname_after)
        #         ws.cell(row=row, column=14, value=bet_size)
        #         ws.cell(row=row, column=16, value=(float(bankrol_first)-bet_size))
        #     else:
        #         ws.cell(row=row, column=9, value=element_takecoeff[1])
        #         ws.cell(row=row, column=11, value=shotname_after)
        #         ws.cell(row=row, column=17, value=bet_size)
        #         ws.cell(row=row, column=19, value=(float(bankrol_second) - bet_size))
        # elif element_takecoeff[0] == 'MELBET':
        #     if 'melbet.ru' in event[6]:
        #         ws.cell(row=row, column=8, value=element_takecoeff[1])
        #         ws.cell(row=row, column=10, value=shotname_after)
        #         ws.cell(row=row, column=14, value=bet_size)
        #         ws.cell(row=row, column=16, value=(float(bankrol_first) - bet_size))
        #     else:
        #         ws.cell(row=row, column=9, value=element_takecoeff[1])
        #         ws.cell(row=row, column=11, value=shotname_after)
        #         ws.cell(row=row, column=17, value=bet_size)
        #         ws.cell(row=row, column=19, value=(float(bankrol_second)-bet_size))
        # elif element_takecoeff[0] == '1XBet':
        #     if '1xlite' in event[6]:
        #         ws.cell(row=row, column=8, value=element_takecoeff[1])
        #         ws.cell(row=row, column=10, value=shotname_after)
        #         ws.cell(row=row, column=14, value=bet_size)
        #         ws.cell(row=row, column=16, value=(float(bankrol_first) - bet_size))
        #     else:
        #         ws.cell(row=row, column=9, value=element_takecoeff[1])
        #         ws.cell(row=row, column=11, value=shotname_after)
        #         ws.cell(row=row, column=17, value=bet_size)
        #         ws.cell(row=row, column=19, value=(float(bankrol_second)-bet_size))
        # elif element_takecoeff[0] == 'BETBOOM':
        #     if 'betboom' in event[6]:
        #         ws.cell(row=row, column=8, value=element_takecoeff[1])
        #         ws.cell(row=row, column=10, value=shotname_after)
        #         ws.cell(row=row, column=14, value=bet_size)
        #         ws.cell(row=row, column=16, value=(float(bankrol_first) - bet_size))
        #     else:
        #         ws.cell(row=row, column=9, value=element_takecoeff[1])
        #         ws.cell(row=row, column=11, value=shotname_after)
        #         ws.cell(row=row, column=17, value=bet_size)
        #         ws.cell(row=row, column=19, value=(float(bankrol_second)-bet_size))
        # for i in range(len(event_data)-2,len(event_data)):
        #     ws.cell(row=row, column=(i+6), value=event_data[i])

        # asyncio.run(event_result(urls=event, row=row, bmaker=element_takecoeff[0]))
        wb.save(settings.STATS_FILE_NAME)

if __name__ == '__main__':
    from pathlib import Path
    BASE_DIR = Path(__file__).resolve().parent.parent
    class settings:
        STATS_DIR = BASE_DIR / "statistic"
        STATS_FILE_NAME = STATS_DIR / "statistic.xlsx"
    statistic = Statistic(imitation=False)
    statistic.insert_data()
else:
    from .. import settings