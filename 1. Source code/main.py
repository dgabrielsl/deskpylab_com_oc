import os
import sys
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import Qt
from plyer import notification

os.system('cls')

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init()
        self.site()
        self.show()

    def init(self):
        # Main window guidelines.
        self.setWindowIcon(QIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ComputerIcon)))
        self.setWindowTitle('DeskPy - Control Operativa Cumplimiento')
        self.setMinimumWidth(1080)
        self.setMinimumHeight(768)

        # Main menu.
        menu_bar = self.menuBar()

        menu_file = menu_bar.addMenu('&Archivo')

        # End user session.
        menu_file_signout = QAction(QIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ComputerIcon)), '&Cerrar sesión', self)
        menu_file_signout.setShortcut('Ctrl+Q')
        menu_file_signout.setStatusTip('Devuelve a la pantalla de inicio de sesión.')
        menu_file_signout.triggered.connect(lambda:print(self.sender().text()))
        menu_file.addAction(menu_file_signout)

        # Stop program.
        menu_file_off = QAction(QIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ComputerIcon)), '&Salir', self)
        menu_file_off.setShortcut('Alt+F4')
        menu_file_off.setStatusTip('Cierra la aplicación.')
        menu_file_off.triggered.connect(lambda:print(self.sender().text()))
        menu_file.addAction(menu_file_off)

        menu_tools = menu_bar.addMenu('&Herramientas')

        # Load new data.
        menu_tools_dataload = QAction(QIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ComputerIcon)), '&Cargar datos', self)
        menu_tools_dataload.setShortcut('F2')
        menu_tools_dataload.setStatusTip('Carga datos a la base de datos desde Excel.')
        menu_tools_dataload.triggered.connect(lambda:print(self.sender().text()))
        menu_tools.addAction(menu_tools_dataload)

        # Download reports.
        menu_tools_reports = QAction(QIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ComputerIcon)), '&Generar reportes', self)
        menu_tools_reports.setShortcut('F3')
        menu_tools_reports.setStatusTip('Generar y descargar reportes.')
        menu_tools_reports.triggered.connect(lambda:print(self.sender().text()))
        menu_tools.addAction(menu_tools_reports)

        # Data FAQ.
        menu_tools_datafaq = QAction(QIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ComputerIcon)), '&Consultas rápidas', self)
        menu_tools_datafaq.setShortcut('F4')
        menu_tools_datafaq.setStatusTip('Consultas frecuentes.')
        menu_tools_datafaq.triggered.connect(lambda:print(self.sender().text()))
        menu_tools.addAction(menu_tools_datafaq)

        menu_settings = menu_bar.addMenu('&Configuración')

        # User admin.
        menu_settings_users = QAction(QIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ComputerIcon)), '&Administrar usuarios', self)
        menu_settings_users.setShortcut('Ctrl+U')
        menu_settings_users.setStatusTip('Agregar, modificar y eliminar usuarios.')
        menu_settings_users.triggered.connect(lambda:print(self.sender().text()))
        menu_settings.addAction(menu_settings_users)

        # My account settings.
        menu_settings_account = QAction(QIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ComputerIcon)), '&Mi cuenta', self)
        menu_settings_account.setShortcut('Shift+U')
        menu_settings_account.setStatusTip('Configurar mi cuenta.')
        menu_settings_account.triggered.connect(lambda:print(self.sender().text()))
        menu_settings.addAction(menu_settings_account)

        # Toolbar tools for each user.
        tool_bar = QToolBar()
        tool_bar.setMovable(False)
        self.addToolBar(tool_bar)

        # Admin ads.
        tool_bar_ads = QAction(QIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ComputerIcon)), '&Avisos', self)
        tool_bar_ads.setShortcut('Alt+A')
        tool_bar_ads.setStatusTip('Ver mis tareas asignadas.')
        tool_bar_ads.triggered.connect(lambda:print(self.sender().text()))
        tool_bar.addAction(tool_bar_ads)

        # My own tasks.
        tool_bar_faq = QAction(QIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ComputerIcon)), '&Mis tareas', self)
        tool_bar_faq.setShortcut('Alt+H')
        tool_bar_faq.setStatusTip('Ver mis tareas asignadas.')
        tool_bar_faq.triggered.connect(lambda:print(self.sender().text()))
        tool_bar.addAction(tool_bar_faq)

        # Reports and informs.
        tool_bar_reports = QAction(QIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ComputerIcon)), '&Datos', self)
        tool_bar_reports.setShortcut('Alt+R')
        tool_bar_reports.setStatusTip('Reportes e informes de tareas.')
        tool_bar_reports.triggered.connect(lambda:print(self.sender().text()))
        tool_bar.addAction(tool_bar_reports)

        # Notepad.
        tool_bar_notes = QAction(QIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ComputerIcon)), '&Mis apuntes', self)
        tool_bar_notes.setShortcut('Alt+N')
        tool_bar_notes.setStatusTip('Ver mis notas.')
        tool_bar_notes.triggered.connect(lambda:print(self.sender().text()))
        tool_bar.addAction(tool_bar_notes)

        menu_help = menu_bar.addMenu('&Ayuda')

        # Docs.
        tool_bar_docs = QAction(QIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ComputerIcon)), '&Documentación', self)
        tool_bar_docs.setShortcut('F1')
        tool_bar_docs.setStatusTip('Ver mis notas.')
        tool_bar_docs.triggered.connect(lambda:print(self.sender().text()))
        menu_help.addAction(tool_bar_docs)

        # GitHub.
        tool_bar_github = QAction(QIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ComputerIcon)), '&GitHub', self)
        tool_bar_github.setStatusTip('Ver mis notas.')
        tool_bar_github.triggered.connect(lambda:print(self.sender().text()))
        menu_help.addAction(tool_bar_github)

        # About.
        tool_bar_about = QAction(QIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ComputerIcon)), '&Acerca De', self)
        tool_bar_about.setStatusTip('Ver mis notas.')
        tool_bar_about.triggered.connect(lambda:print(self.sender().text()))
        menu_help.addAction(tool_bar_about)

    def site(self):
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet("""
            # Drop styles here...
        """)
    win = Main()
    sys.exit(app.exec())