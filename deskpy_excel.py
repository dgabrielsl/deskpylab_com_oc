import os
import sqlite3

from PyQt6.QtWidgets import QFileDialog, QMessageBox

import openpyxl
from openpyxl import Workbook
from openpyxl.styles import Border, Side, PatternFill, Alignment, Font

class Excel():
    def load_sysde(self):
        con = sqlite3.connect('sysde.db')
        cur = con.cursor()

        try:
            cur.execute('''
                CREATE TABLE sysde_hub(
                    IDENTIFICATION VARCHAR(25) UNIQUE,
                    PHONE VARCHAR(25),
                    EMAIL VARCHAR(50),
                    LINKED VARCHAR(15))
            ''')
        except: pass

        path = QFileDialog.getOpenFileName(filter=('*.xlsx'))
        path = path[0]

        self.statusbar.showMessage(f'Loading new Sysde workbook: «{path}»',5000)

        wb = openpyxl.load_workbook(path)
        ws = wb.worksheets[0]

        ws.delete_rows(1,4)
        # wb.save('C:/Users/gabriel.solano/Downloads/Sysde (openpyxl).xlsx')
        saved_copy = 'C:/Users/dgabr/Downloads/Sysde (openpyxl).xlsx'
        wb.save(saved_copy)

        for i in range(ws.max_column):
            i += 1
            if ws.cell(1,i).value == 'Fecha adición' or ws.cell(1,i).value == 'Fecha adicion': char_1 = ws.cell(1,i).column_letter
            if ws.cell(1,i).value == 'Identificación' or ws.cell(1,i).value == 'Identificacion': char_2 = ws.cell(1,i).column_letter
            if ws.cell(1,i).value == 'Email': char_3 = ws.cell(1,i).column_letter
            if ws.cell(1,i).value == 'Teléfono celular' or ws.cell(1,i).value == 'Telefono celular': char_4 = ws.cell(1,i).column_letter

        self.records = []

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
                self.records.append(line)

        for record in self.records:
            r = f'INSERT INTO sysde_hub VALUES ("{record[0]}", "{record[1]}", "{record[2]}", "{record[3]}")'
            try: cur.execute(r)
            except: pass

        con.commit()
        con.close()

        try: os.remove(saved_copy)
        except Exception as e: self.statusbar.showMessage(f'{e},10000')

        QMessageBox.information(
            self,
            'deskpy_excel',
            'La actualización de la base de datos de SYSDE se ha completado correctamente.\t\t',
            QMessageBox.StandardButton.Ok,
            QMessageBox.StandardButton.Ok)

    def load_book(self):
        wb_url = QFileDialog.getOpenFileName(filter=('*.xlsx'))
        wb_url = wb_url[0]

    def read_book(self):
        pass

    def write_book(self):
        pass