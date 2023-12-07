import os
import sys
import sqlite3
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import Qt
from plyer import notification

os.system('cls')

class Main(QMainWindow, QWidget):
    def __init__(self):
        super().__init__()
        self.init()
        self.site()
        self.bd_settings()
        self.show()

    def init(self):
        # Main window guidelines.
        self.setWindowIcon(QIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ComputerIcon)))
        self.setWindowTitle('DeskPy - Control Operativa Cumplimiento')
        self.setMinimumWidth(768)
        self.setMinimumHeight(460)

        # Main menu.
        menu_bar = self.menuBar()
        menu_bar.setStyleSheet('color: #ff74c7; background: #201;')

        menu_file = menu_bar.addMenu('&Archivo')

        # End user session.
        self.menu_file_signout = QAction(QIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ComputerIcon)), '&Cerrar sesión', self)
        self.menu_file_signout.setShortcut('Ctrl+Q')
        self.menu_file_signout.setStatusTip('Devuelve a la pantalla de inicio de sesión.')
        self.menu_file_signout.triggered.connect(self.menu_events)
        self.menu_file_signout.setDisabled(True)
        menu_file.addAction(self.menu_file_signout)

        # Stop program.
        self.menu_file_off = QAction(QIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ComputerIcon)), '&Salir', self)
        self.menu_file_off.setShortcut('Alt+F4')
        self.menu_file_off.setStatusTip('Cierra la aplicación.')
        self.menu_file_off.triggered.connect(self.menu_events)
        menu_file.addAction(self.menu_file_off)

        menu_navg = menu_bar.addMenu('&Navegación')

        # Set up assignments.
        self.menu_navg_assign = QAction(QIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ComputerIcon)), '&Asignar solicitudes', self)
        self.menu_navg_assign.setShortcut('')
        self.menu_navg_assign.setStatusTip('Administrar asignación de solicitudes nuevas.')
        self.menu_navg_assign.triggered.connect(self.menu_events)
        self.menu_navg_assign.setDisabled(True)
        menu_navg.addAction(self.menu_navg_assign)

        # Assignments dashboard.
        self.menu_navg_mydashboard = QAction(QIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ComputerIcon)), '&Bandeja de asignaciones', self)
        self.menu_navg_mydashboard.setShortcut('')
        self.menu_navg_mydashboard.setStatusTip('Ver mis asignaciones diarias.')
        self.menu_navg_mydashboard.triggered.connect(self.menu_events)
        self.menu_navg_mydashboard.setDisabled(True)
        menu_navg.addAction(self.menu_navg_mydashboard)

        # Processing panel.
        self.menu_navg_processing = QAction(QIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ComputerIcon)), '&Procesamiento de solicitudes', self)
        self.menu_navg_processing.setShortcut('')
        self.menu_navg_processing.setStatusTip('Panel de trabajo de registros.')
        self.menu_navg_processing.triggered.connect(self.menu_events)
        self.menu_navg_processing.setDisabled(True)
        menu_navg.addAction(self.menu_navg_processing)

        menu_tools = menu_bar.addMenu('&Herramientas')

        # Load new data.
        self.menu_tools_dataload = QAction(QIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ComputerIcon)), '&Cargar datos', self)
        self.menu_tools_dataload.setShortcut('')
        self.menu_tools_dataload.setStatusTip('Carga datos a la base de datos desde Excel.')
        self.menu_tools_dataload.triggered.connect(self.menu_events)
        self.menu_tools_dataload.setDisabled(True)
        menu_tools.addAction(self.menu_tools_dataload)

        # Download reports.
        self.menu_tools_reports = QAction(QIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ComputerIcon)), '&Generar reportes', self)
        self.menu_tools_reports.setShortcut('')
        self.menu_tools_reports.setStatusTip('Generar y descargar reportes.')
        self.menu_tools_reports.triggered.connect(self.menu_events)
        self.menu_tools_reports.setDisabled(True)
        menu_tools.addAction(self.menu_tools_reports)

        menu_settings = menu_bar.addMenu('&Configuración')

        # User admin.
        self.menu_settings_users = QAction(QIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ComputerIcon)), '&Administrar usuarios', self)
        self.menu_settings_users.setShortcut('Ctrl+U')
        self.menu_settings_users.setStatusTip('Agregar, modificar y eliminar usuarios.')
        self.menu_settings_users.triggered.connect(self.menu_events)
        self.menu_settings_users.setDisabled(True)
        menu_settings.addAction(self.menu_settings_users)

        # My account settings.
        self.menu_settings_account = QAction(QIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ComputerIcon)), '&Mi cuenta', self)
        self.menu_settings_account.setShortcut('Shift+U')
        self.menu_settings_account.setStatusTip('Configurar mi cuenta.')
        self.menu_settings_account.triggered.connect(self.menu_events)
        self.menu_settings_account.setDisabled(True)
        menu_settings.addAction(self.menu_settings_account)

        menu_help = menu_bar.addMenu('&Ayuda')

        # Docs.
        self.tool_bar_docs = QAction(QIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ComputerIcon)), '&Documentación', self)
        self.tool_bar_docs.setShortcut('F1')
        self.tool_bar_docs.setStatusTip('Ir a la documentación.')
        self.tool_bar_docs.triggered.connect(self.menu_events)
        menu_help.addAction(self.tool_bar_docs)

        # GitHub.
        self.tool_bar_github = QAction(QIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ComputerIcon)), '&GitHub', self)
        self.tool_bar_github.setStatusTip('Ir al repositorio.')
        self.tool_bar_github.triggered.connect(self.menu_events)
        menu_help.addAction(self.tool_bar_github)

    def site(self):
        self.stacked_layout = QStackedLayout()

        self.w0 = QWidget()             # Login.
        self.w1 = QWidget()             # Home.
        self.w2 = QWidget()             # Assignments board.
        self.w3 = QWidget()             # Processing panel.
        self.w4 = QWidget()             # Download data.
        self.w5 = QWidget()             # User admin.
        self.w6 = QWidget()             # My profile.

        l0 = QVBoxLayout()

        h1 = QLabel('Control Operativa Cumplimiento')
        h1.setStyleSheet('margin-top: 60px; color: #fff; font-size: 20px;')
        h1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        l0.addWidget(h1)

        h2 = QLabel('Financiera Multimoney')
        h2.setStyleSheet('color: #aaa; font-size: 13px;')
        h2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        l0.addWidget(h2)

        href = QLabel('DeskPyL ↗')
        href.setStyleSheet('margin-bottom: 10px; color: #db0; font-size: 14px;')
        href.setCursor(Qt.CursorShape.PointingHandCursor)
        href.setAlignment(Qt.AlignmentFlag.AlignCenter)
        l0.addWidget(href)

        self.le_login_user = QLineEdit()
        self.le_login_user.setPlaceholderText('Username')
        self.le_login_user.setStyleSheet('margin: 5px 0; padding: 5px 12px; color: #333; background: #fff; border-radius: 12px;')
        self.le_login_user.setFixedWidth(375)
        self.le_login_user.setAlignment(Qt.AlignmentFlag.AlignCenter)
        l0.addWidget(self.le_login_user)

        self.le_login_passw = QLineEdit()
        self.le_login_passw.setPlaceholderText('Password')
        self.le_login_passw.setStyleSheet('margin: 5px 0; padding: 5px 12px; color: #333; background: #fff; border-radius: 12px;')
        self.le_login_passw.setFixedWidth(375)
        self.le_login_passw.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.le_login_passw.setEchoMode(QLineEdit.EchoMode.Password)
        l0.addWidget(self.le_login_passw)

        self.credentials_cache = QCheckBox('Recordar mis credenciales')
        self.credentials_cache.setStyleSheet('margin: 3px 0; color: #fff;')
        self.credentials_cache.setFixedWidth(160)
        self.credentials_cache.setCursor(Qt.CursorShape.PointingHandCursor)
        l0.addWidget(self.credentials_cache)

        self.get_logged = QPushButton('Ingresar')
        self.get_logged.setStyleSheet('margin: 5px 0; padding: 5px; background: #ff74c7; color: #333; border-radius: 12px;')
        self.get_logged.setFixedWidth(375)
        self.get_logged.setCursor(Qt.CursorShape.PointingHandCursor)
        self.get_logged.clicked.connect(self.menu_events)
        l0.addWidget(self.get_logged)

        l0.setAlignment(Qt.AlignmentFlag.AlignCenter)
        l0.addStretch()
        self.w0.setLayout(l0)

        l1 = QVBoxLayout()
        l1.addWidget(QLabel('Página de inicio.'))
        l1.addStretch()
        self.w1.setLayout(l1)

        l2 = QVBoxLayout()
        l2.addWidget(QLabel('Bandeja de asignaciones'))
        l2.addStretch()
        self.w2.setLayout(l2)

        l3 = QVBoxLayout()
        l3.addWidget(QLabel('Procesamiento de solicitudes'))
        l3.addStretch()
        self.w3.setLayout(l3)

        l4 = QVBoxLayout()
        l4.addWidget(QLabel('Descargar datos'))
        l4.addStretch()
        self.w4.setLayout(l4)

        l5 = QVBoxLayout()
        l5.addWidget(QLabel('Administración de usuarios'))
        l5.addStretch()
        self.w5.setLayout(l5)

        l6 = QVBoxLayout()
        l6.addWidget(QLabel('Mi perfil'))
        l6.addStretch()
        self.w6.setLayout(l6)

        self.stacked_layout.addWidget(self.w0)
        self.stacked_layout.addWidget(self.w1)
        self.stacked_layout.addWidget(self.w2)
        self.stacked_layout.addWidget(self.w3)
        self.stacked_layout.addWidget(self.w4)
        self.stacked_layout.addWidget(self.w5)
        self.stacked_layout.addWidget(self.w6)

        self.stacked_layout.setCurrentIndex(0)

        central_widget = QWidget()
        central_widget.setLayout(self.stacked_layout)
        self.setCentralWidget(central_widget)

        self.get_logged.setFocus()

        self.le_login_user.setText('system.gabriel.solano')
        self.le_login_passw.setText('root')


    def bd_settings(self):
        self.con1 = sqlite3.connect('settings.db')
        self.cur1 = self.con1.cursor()
        try:
            self.cur1.execute('''
                CREATE TABLE user_settings(
                    USER_LOGGED VARCHAR(99) UNIQUE,
                    USER_PASSWORD VARCHAR(99),
                    MAKE_ASSIGNMENTS BOOLEAN,
                    DOWNLOAD_REPORTS BOOLEAN,
                    LOAD_BOOK BOOLEAN,
                    ADMIN_USERS BOOLEAN,
                    LOAD_ENTRY BOOLEAN,
                    UPDATE_LOG BOOLEAN,
                    DELETE_LOG BOOLEAN)
                ''')
            record = f'INSERT INTO user_settings VALUES ("system.gabriel.solano", "root", 1, 1, 1, 1, 1, 1, 1)'
            self.cur1.execute(record)
            record = f'INSERT INTO user_settings VALUES ("admin.gabriel.solano", "220693", 1, 1, 1, 1, 1, 1, 1)'
            self.cur1.execute(record)
            record = f'INSERT INTO user_settings VALUES ("standard.user", "1230", 0, 0, 0, 0, 0, 1, 0)'
            self.cur1.execute(record)
        except: pass
        finally:
            self.con1.commit()
            self.con1.close()

    def menu_events(self):
        self.bt_sender = self.sender().text()
        self.user_logged = []

        if self.bt_sender == 'Ingresar':
            typed_data_user = self.le_login_user.text().lower()
            typed_data_pass = self.le_login_passw.text().lower()

            self.le_login_user.setStyleSheet('margin: 5px 0; padding: 5px 12px; color: #333; background: #fff; border-radius: 12px;')
            self.le_login_passw.setStyleSheet('margin: 5px 0; padding: 5px 12px; color: #333; background: #fff; border-radius: 12px;')


            if typed_data_user.strip() != '' and typed_data_pass.strip() != '':
                con = sqlite3.connect('settings.db')
                cur = con.cursor()
                req = cur.execute(f'SELECT * FROM user_settings')
                res = req.fetchall()

                for r in res:
                    if typed_data_user == r[0] and typed_data_pass == r[1]:
                        self.user_logged = list(r)
                        break

                print(self.user_logged)

                self.menu_file_signout.setDisabled(False)
                self.menu_navg_mydashboard.setDisabled(False)
                self.menu_navg_processing.setDisabled(False)
                self.menu_settings_account.setDisabled(False)

                if self.user_logged[2] == 1: self.menu_navg_assign.setDisabled(False)
                if self.user_logged[3] == 1: self.menu_tools_reports.setDisabled(False)
                if self.user_logged[4] == 1: self.menu_tools_dataload.setDisabled(False)
                if self.user_logged[5] == 1: self.menu_settings_users.setDisabled(False)

                con.close()

                self.le_login_user.setText('')
                self.le_login_passw.setText('')
                self.stacked_layout.setCurrentIndex(1)

            else:
                if typed_data_user.strip() == '': self.le_login_user.setStyleSheet('margin: 5px 0; padding: 5px 12px; color: #333; background: #eaa; border-radius: 12px;')
                if typed_data_pass.strip() == '': self.le_login_passw.setStyleSheet('margin: 5px 0; padding: 5px 12px; color: #333; background: #eaa; border-radius: 12px;')



        if self.bt_sender == '&Cerrar sesión':
            self.stacked_layout.setCurrentIndex(0)
            self.menu_file_signout.setDisabled(True)
            self.menu_navg_mydashboard.setDisabled(True)
            self.menu_navg_processing.setDisabled(True)
            self.menu_settings_account.setDisabled(True)
            self.menu_navg_assign.setDisabled(True)
            self.menu_tools_reports.setDisabled(True)
            self.menu_tools_dataload.setDisabled(True)
            self.menu_settings_users.setDisabled(True)
        elif self.bt_sender == '&Salir':
            pass
        elif self.bt_sender == '&Inicio':
            self.stacked_layout.setCurrentIndex(1)
        elif self.bt_sender == '&Bandeja de asignaciones':
            self.stacked_layout.setCurrentIndex(2)
        elif self.bt_sender == '&Procesamiento de solicitudes':
            self.stacked_layout.setCurrentIndex(3)
        elif self.bt_sender == '&Cargar datos':
            pass
        elif self.bt_sender == '&Generar reportes':
            self.stacked_layout.setCurrentIndex(4)
        elif self.bt_sender == '&Administrar usuarios':
            self.stacked_layout.setCurrentIndex(5)
        elif self.bt_sender == '&Mi cuenta':
            self.stacked_layout.setCurrentIndex(6)
        elif self.bt_sender == '&Documentación':
            pass
        elif self.bt_sender == '&GitHub':
            pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet("""
            QWidget{background: #333;}
        """)
    win = Main()
    sys.exit(app.exec())