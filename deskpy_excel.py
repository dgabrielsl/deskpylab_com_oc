import os

from PyQt6.QtWidgets import QFileDialog, QMessageBox

import openpyxl
from openpyxl import Workbook
from openpyxl.styles import Border, Side, PatternFill, Alignment, Font

class Excel():
    def load_sysde(self):
        path = QFileDialog.getOpenFileName(filter=('*.xlsx'))
        path = path[0]

        wb = openpyxl.load_workbook(path)
        ws = wb.worksheets[0]

        ws.delete_rows(1,4)
        # wb.save('C:/Users/gabriel.solano/Downloads/Sysde (openpyxl).xlsx')
        wb.save('C:/Users/dgabr/Downloads/Sysde (openpyxl).xlsx')

        # mc = ws.max_column
        # x = ws.cell(1,107).value
        # y = ws.cell(1,107)

        for i in range(ws.max_column):
            i += 1
            if ws.cell(1,i).value == 'Fecha adición' or ws.cell(1,i).value == 'Fecha adicion': char_1 = ws.cell(1,i).column_letter
            if ws.cell(1,i).value == 'Identificación' or ws.cell(1,i).value == 'Identificacion': char_2 = ws.cell(1,i).column_letter
            if ws.cell(1,i).value == 'Email': char_3 = ws.cell(1,i).column_letter
            if ws.cell(1,i).value == 'Teléfono celular' or ws.cell(1,i).value == 'Telefono celular': char_4 = ws.cell(1,i).column_letter

        # print(ws[char_1+'2'].value)
        # print(ws[char_2+'2'].value)
        # print(ws[char_3+'2'].value)
        # print(ws[char_4+'2'].value)

        # print(f'ws.max_row: {ws.max_row}')

        writelines = []

        for i in range(int(ws.max_row) + 1):
            if i > 1:
                line = []
                insert = f'{ws[char_2+str(i)].value}'
                insert = insert.replace('-','')
                line.append(str(insert))
                line.append(str(f'{ws[char_4+str(i)].value}'))
                line.append(f'{ws[char_3+str(i)].value}'.lower())
                insert = f'{ws[char_1+str(i)].value}'
                insert = insert.split(' ')
                insert = insert[0]
                line.append(insert)
                writelines.append(line)

        print(f'len(writelines): {len(writelines)}')
        for wl in writelines:
            print(wl)

        QMessageBox.information(
            self,
            'deskpy_excel',
            f'load_workbook({path[:50]}) successfully...\t\t\n{len(writelines)} new registres were added/updated.\t\t',
            QMessageBox.StandardButton.Ok,
            QMessageBox.StandardButton.Ok)

    def load_book(self):
        wb_url = QFileDialog.getOpenFileName(filter=('*.xlsx'))
        wb_url = wb_url[0]

    def read_book(self):
        pass

    def write_book(self):
        pass