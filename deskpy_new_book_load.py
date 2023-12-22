import os

from PyQt6.QtWidgets import QFileDialog

import openpyxl
from openpyxl import Workbook
from openpyxl.styles import Border, Side, PatternFill, Alignment, Font

class Excel():
    def load_book(self):
        workbook = QFileDialog.getOpenFileName(filter=('*.xlsx'))
        print(workbook[0])

    def read_book(self):
        pass

    def write_book(self):
        pass