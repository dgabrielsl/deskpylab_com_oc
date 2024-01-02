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
                    IDENT VARCHAR(25) UNIQUE,
                    EMAIL VARCHAR(50),
                    PHONE VARCHAR(25))
                ''')
        except: pass

        path = QFileDialog.getOpenFileName(filter=('*.xlsx'))
        path = path[0]

        self.statusbar.showMessage(f'Loading new Sysde workbook: «{path}»',9000)

        wb = openpyxl.load_workbook(path)
        ws = wb.worksheets[0]

        ws.delete_rows(1,4)

        saved_copy = path
        saved_copy = saved_copy.split('/')
        saved_copy.pop()
        saved_copy = '/'.join(saved_copy)
        saved_copy = f'{saved_copy}/temp_copy.xlsx'

        wb.save(saved_copy)

        for i in range(ws.max_column):
            i += 1
            if ws.cell(1,i).value == 'Identificación' or ws.cell(1,i).value == 'Identificacion': char_1 = ws.cell(1,i).column_letter
            if ws.cell(1,i).value == 'Email': char_2 = ws.cell(1,i).column_letter
            if ws.cell(1,i).value == 'Teléfono celular' or ws.cell(1,i).value == 'Telefono celular': char_3 = ws.cell(1,i).column_letter

        self.records = []

        for i in range(int(ws.max_row) + 1):
            if i > 1:
                line = []

                # Identification:
                insert = f'{ws[char_1+str(i)].value}'
                insert = insert.replace('-','')
                line.append(str(insert))

                # E-mail:
                line.append(f'{ws[char_2+str(i)].value}'.lower())

                # Phone:
                line.append(str(f'{ws[char_3+str(i)].value}'))

                self.records.append(line)

        for record in self.records:
            r = f'INSERT INTO sysde_hub VALUES ("{record[0]}", "{record[1]}", "{record[2]}")'
            try: cur.execute(r)
            except Exception as e: pass

        con.commit()
        con.close()

        try: os.remove(saved_copy)
        except Exception as e: pass

        QMessageBox.information(
            self,
            'deskpy_excel',
            'La actualización de la base de datos de SYSDE se ha completado correctamente.\t\t',
            QMessageBox.StandardButton.Ok,
            QMessageBox.StandardButton.Ok)

    def load_book(self):
        wb_url = QFileDialog.getOpenFileName(filter=('*.xlsx'))
        wb_url = wb_url[0]

        con = sqlite3.connect('hub.db')
        cur = con.cursor()

        try:
            cur.execute('''
                CREATE TABLE customers(
                    HELPDESK VARCHAR(10) UNIQUE,
                    IDENTIFICATION VARCHAR(20),
                    DOCUMENT VARCHAR(10),
                    CODE VARCHAR(10),
                    CLASS_CASE VARCHAR(100),
                    STATUS VARCHAR(20),
                    PRODUCT VARCHAR(20),
                    INCOME_SOURCE VARCHAR(300),
                    WARNING_AMOUNT VARCHAR(20),
                    CUSTOMER_PROFILE VARCHAR(200),
                    DEADLINE VARCHAR(20),
                    NOTIF_TYPE VARCHAR(20),
                    CONTACT_TYPE VARCHAR(20),
                    CUSTOMER_ANSWER VARCHAR(200),
                    ASSIGNED_TO VARCHAR(50),
                    AUTHOR VARCHAR(50),
                    RESULT VARCHAR(100),
                    UPDATED VARCHAR(20),
                    CHANGES_LOG VARCHAR(3000))
                ''')
        except Exception as e: pass

        wb = openpyxl.load_workbook(wb_url)
        ws = wb.worksheets[0]

        helpdesk = ''
        identification = ''
        document = ''
        code = ''
        class_case = ''
        status = ''
        product = ''
        income_source = ''
        warning_amount = ''
        customer_profile = ''
        deadline = ''
        notif_type = ''
        contact_type = ''
        customer_answer = ''
        assigned_to = ''
        author = ''
        result = ''
        updated = ''
        changes_log = ''
        fname = ''

        for i in range(ws.max_column):
            i += 1
            value = ws.cell(1,i).value.lower()
            value = value.replace('á','a').replace('é','e').replace('í','i').replace('ó','o').replace('ú','u').replace(':','').replace('.','')

            if value.__contains__('#'): helpdesk = ws.cell(1,i).column_letter
            if value.__contains__('cedula'): identification = ws.cell(1,i).column_letter
            if value.__contains__('pagare'): document = ws.cell(1,i).column_letter
            if value.__contains__('codigo de cliente'): code = ws.cell(1,i).column_letter
            if value.__contains__('tipo de caso'): class_case = ws.cell(1,i).column_letter
            if value.__contains__('estado'): status = ws.cell(1,i).column_letter
            if value.__contains__('producto'): product = ws.cell(1,i).column_letter
            if value.__contains__('origen de fondos'): income_source = ws.cell(1,i).column_letter
            if value.__contains__('monto de la alerta'): warning_amount = ws.cell(1,i).column_letter
            if value.__contains__('perfil del cliente'): customer_profile = ws.cell(1,i).column_letter
            if value.__contains__('fecha de prorroga'): deadline = ws.cell(1,i).column_letter
            if value.__contains__('tipo de notificacion'): notif_type = ws.cell(1,i).column_letter
            if value.__contains__('tipo de contacto'): contact_type = ws.cell(1,i).column_letter
            if value.__contains__('respuesta del cliente'): customer_answer = ws.cell(1,i).column_letter
            if value.__contains__('asignado a'): assigned_to = ws.cell(1,i).column_letter
            if value.__contains__('autor'): author = ws.cell(1,i).column_letter
            if value.__contains__('resultado de gestion'): result = ws.cell(1,i).column_letter
            if value.__contains__('actualizado'): updated = ws.cell(1,i).column_letter
            if value.__contains__('asunto'): fname = ws.cell(1,i).column_letter

        self.customers = []

        for i in range(int(ws.max_row) + 1):
            if i > 1:
                line = []

                # HelpDesk / Don't clear.
                insert = f'{ws[helpdesk+str(i)].value}'
                line.append(insert)

                # Identification / Clear: \s - . ,
                insert = f'{ws[identification+str(i)].value}'
                insert = insert.strip().replace('-','').replace('.','').replace(',','')
                line.append(insert)

                # Document
                insert = f'{ws[document+str(i)].value}'
                line.append(insert)

                insert = f'{ws[code+str(i)].value}'
                line.append(insert)
                
                insert = f'{ws[class_case+str(i)].value}'
                line.append(insert)
                
                insert = f'{ws[status+str(i)].value}'
                line.append(insert)
                
                insert = f'{ws[product+str(i)].value}'
                line.append(insert)
                
                insert = f'{ws[income_source+str(i)].value}'
                line.append(insert)
                
                insert = f'{ws[warning_amount+str(i)].value}'
                line.append(insert)
                
                insert = f'{ws[customer_profile+str(i)].value}'
                line.append(insert)
                
                insert = f'{ws[deadline+str(i)].value}'
                line.append(insert)
                
                insert = f'{ws[notif_type+str(i)].value}'
                line.append(insert)
                
                insert = f'{ws[contact_type+str(i)].value}'
                line.append(insert)
                
                insert = f'{ws[customer_answer+str(i)].value}'
                line.append(insert)
                
                insert = f'{ws[assigned_to+str(i)].value}'
                line.append(insert)
                
                insert = f'{ws[author+str(i)].value}'
                line.append(insert)
                
                insert = f'{ws[result+str(i)].value}'
                line.append(insert)
                
                insert = f'{ws[updated+str(i)].value}'
                line.append(insert)
                
                insert = f'{ws[fname+str(i)].value}'
                line.append(insert)

                self.customers.append(line)

        for customer in self.customers:
            print(customer)

        con.commit()
        con.close()

    def read_book(self):
        pass

    def write_book(self):
        pass