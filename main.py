import os
import sys
from pathlib import Path
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
        self.setMinimumWidth(1080)
        self.setMinimumHeight(480)
        # self.showMaximized()
        self.setWindowFlags(Qt.WindowType.WindowMaximizeButtonHint | Qt.WindowType.WindowMinimizeButtonHint)

        # Main menu.
        menu_bar = self.menuBar()
        menu_bar.setStyleSheet('color: #ff74c7; background: #201;')

        menu_file = menu_bar.addMenu('&Archivo')

        # Status bar.
        self.statusbar = self.statusBar()
        self.statusbar.showMessage('Credenciales requeridas', 5000)

        # End user session.
        self.menu_file_signout = QAction(QIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogOkButton)), '&Cerrar sesión', self)
        self.menu_file_signout.setShortcut('Ctrl+Q')
        self.menu_file_signout.setStatusTip('Devuelve a la pantalla de inicio de sesión.')
        self.menu_file_signout.triggered.connect(self.menu_events)
        self.menu_file_signout.setDisabled(True)
        menu_file.addAction(self.menu_file_signout)

        # Stop program.
        self.menu_file_off = QAction(QIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MessageBoxCritical)), '&Salir', self)
        self.menu_file_off.setShortcut('F12')
        self.menu_file_off.setStatusTip('Cierra la aplicación.')
        self.menu_file_off.triggered.connect(self.menu_events)
        menu_file.addAction(self.menu_file_off)

        menu_navg = menu_bar.addMenu('&Navegación')

        # Set up assignments.
        self.menu_navg_home = QAction(QIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DirHomeIcon)), '&Inicio', self)
        self.menu_navg_home.setShortcut('')
        self.menu_navg_home.setStatusTip('Ver la página de inicio.')
        self.menu_navg_home.triggered.connect(self.menu_events)
        self.menu_navg_home.setDisabled(True)
        menu_navg.addAction(self.menu_navg_home)

        # Set up assignments.
        self.menu_navg_assign = QAction(QIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DirHomeIcon)), '&Asignar solicitudes', self)
        self.menu_navg_assign.setShortcut('')
        self.menu_navg_assign.setStatusTip('Administrar asignación de solicitudes nuevas.')
        self.menu_navg_assign.triggered.connect(self.menu_events)
        self.menu_navg_assign.setDisabled(True)
        menu_navg.addAction(self.menu_navg_assign)

        # Assignments dashboard.
        self.menu_navg_mydashboard = QAction(QIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_FileDialogListView)), '&Bandeja de asignaciones', self)
        self.menu_navg_mydashboard.setShortcut('')
        self.menu_navg_mydashboard.setStatusTip('Ver mis asignaciones diarias.')
        self.menu_navg_mydashboard.triggered.connect(self.menu_events)
        self.menu_navg_mydashboard.setDisabled(True)
        menu_navg.addAction(self.menu_navg_mydashboard)

        # Processing panel.
        self.menu_navg_processing = QAction(QIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogResetButton)), '&Procesamiento de solicitudes', self)
        self.menu_navg_processing.setShortcut('')
        self.menu_navg_processing.setStatusTip('Panel de trabajo de registros.')
        self.menu_navg_processing.triggered.connect(self.menu_events)
        self.menu_navg_processing.setDisabled(True)
        menu_navg.addAction(self.menu_navg_processing)

        menu_tools = menu_bar.addMenu('&Herramientas')

        # Load new data.
        self.menu_tools_dataload = QAction(QIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogApplyButton)), '&Cargar datos', self)
        self.menu_tools_dataload.setShortcut('')
        self.menu_tools_dataload.setStatusTip('Carga datos a la base de datos desde Excel.')
        self.menu_tools_dataload.triggered.connect(self.menu_events)
        self.menu_tools_dataload.setDisabled(True)
        menu_tools.addAction(self.menu_tools_dataload)

        # Download reports.
        self.menu_tools_reports = QAction(QIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_FileDialogDetailedView)), '&Generar reportes', self)
        self.menu_tools_reports.setShortcut('')
        self.menu_tools_reports.setStatusTip('Generar y descargar reportes.')
        self.menu_tools_reports.triggered.connect(self.menu_events)
        self.menu_tools_reports.setDisabled(True)
        menu_tools.addAction(self.menu_tools_reports)

        menu_settings = menu_bar.addMenu('&Configuración')

        # User admin.
        self.menu_settings_users = QAction(QIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_VistaShield)), '&Administrar usuarios', self)
        self.menu_settings_users.setShortcut('Ctrl+U')
        self.menu_settings_users.setStatusTip('Agregar, modificar y eliminar usuarios.')
        self.menu_settings_users.triggered.connect(self.menu_events)
        self.menu_settings_users.setDisabled(True)
        menu_settings.addAction(self.menu_settings_users)

        # My account settings.
        self.menu_settings_account = QAction(QIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DesktopIcon)), '&Mi cuenta', self)
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

        self.color = '#ff74c7'
        self.base = '#201'

    def site(self):
        self.stacked_layout = QStackedLayout()

        self.w0 = QWidget()             # Login.
        self.w1 = QWidget()             # Home.
        self.w2 = QWidget()             # Assignments board.
        self.w3 = QWidget()             # Processing panel.
        self.w4 = QWidget()             # Download data.
        self.w5 = QWidget()             # Users admin.
        self.w6 = QWidget()             # My profile.
        self.w7 = QWidget()             # Set up assignments.

# PAGE: LOGIN
        l0 = QVBoxLayout()

        h1 = QLabel('Control Operativa Cumplimiento')
        h1.setStyleSheet('color: #fff; font-size: 20px;')
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
        href.setStatusTip('Ir al sitio web https://dgabrielsolo.github.io/deskpylab')
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

        self.display_passw = QCheckBox('Mostrar contraseña')
        self.display_passw.setStyleSheet('margin: 3px 0; color: #fff;')
        self.display_passw.setFixedWidth(160)
        self.display_passw.setCursor(Qt.CursorShape.PointingHandCursor)
        self.display_passw.clicked.connect(self.toggle_display_pasw)
        l0.addWidget(self.display_passw)

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
        self.w0.setLayout(l0)

# PAGE: HOME
        l1 = QVBoxLayout()

        def stl_h1_h2(self, h1, h2):
            h1.setStyleSheet('padding: 10px; background: #222; font-size: 20px; border-radius: 20px;')
            h2.setStyleSheet('padding: 5px; background: #222; color: #888; border-radius: 12px;')

        lgg1 = QHBoxLayout()
        lgg1.setAlignment(Qt.AlignmentFlag.AlignTrailing)
        self.l1_banner1 = QLabel('')
        self.l1_banner2 = QLabel('get : self(user().logged)')
        lgg1.addWidget(QLabel('DeskPyL'))
        lgg1.addWidget(self.l1_banner1)
        lgg1.addWidget(self.l1_banner2)
        l1.addLayout(lgg1)

        h1 = QLabel('Hola, bienvenido(a)')
        h1.setStyleSheet('margin-bottom: 30px; color: #fff; font-size: 15px;')
        h1.setAlignment(Qt.AlignmentFlag.AlignCenter)

        l1.addWidget(h1)

        shorcut1 = QPushButton('Bandeja de asignaciones')
        shorcut1.setCursor(Qt.CursorShape.PointingHandCursor)
        shorcut1.setObjectName('shorcut1')

        shorcut2 = QPushButton('Procesamiento de solicitudes')
        shorcut2.setCursor(Qt.CursorShape.PointingHandCursor)
        shorcut2.setObjectName('shorcut2')

        shorcut3 = QPushButton('Mi cuenta')
        shorcut3.setCursor(Qt.CursorShape.PointingHandCursor)

        wrapper1 = QHBoxLayout()
        wrapper1.addWidget(shorcut1)
        wrapper1.addWidget(shorcut2)
        wrapper1.addWidget(shorcut3)
        wrapper1.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        shorcut4 = QPushButton('Asignar solicitudes')
        shorcut4.setCursor(Qt.CursorShape.PointingHandCursor)

        shorcut5 = QPushButton('Cargar datos')
        shorcut5.setCursor(Qt.CursorShape.PointingHandCursor)

        shorcut6 = QPushButton('Generar reportes')
        shorcut6.setCursor(Qt.CursorShape.PointingHandCursor)

        shorcut7 = QPushButton('Administrar usuarios')
        shorcut7.setCursor(Qt.CursorShape.PointingHandCursor)

        wrapper2 = QHBoxLayout()
        wrapper2.addWidget(shorcut4)
        wrapper2.addWidget(shorcut5)
        wrapper2.addWidget(shorcut6)
        wrapper2.addWidget(shorcut7)
        wrapper2.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        shorcut8 = QPushButton('Documentación')
        shorcut8.setCursor(Qt.CursorShape.PointingHandCursor)
        shorcut8.setObjectName('shorcut8')

        shorcut9 = QPushButton('GitHub')
        shorcut9.setCursor(Qt.CursorShape.PointingHandCursor)
        shorcut9.setObjectName('shorcut9')

        wrapper3 = QHBoxLayout()
        wrapper3.addWidget(shorcut8)
        wrapper3.addWidget(shorcut9)
        wrapper3.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        l1.addLayout(wrapper1)
        l1.addLayout(wrapper2)
        l1.addLayout(wrapper3)
        l1.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.w1.setLayout(l1)

# PAGE: ASSIGNMENTS BOARD
        l2 = QVBoxLayout()

        lgg2 = QHBoxLayout()
        lgg2.setAlignment(Qt.AlignmentFlag.AlignTrailing)
        self.l2_banner1 = QLabel('')
        self.l2_banner2 = QLabel('get : self(user().logged)')
        lgg2.addWidget(QLabel('DeskPyL'))
        lgg2.addWidget(self.l2_banner1)
        lgg2.addWidget(self.l2_banner2)
        l2.addLayout(lgg2)

        l2.addWidget(QLabel('Bandeja de asignaciones'))
        l2.addStretch()
        self.w2.setLayout(l2)

# PAGE: PROCESSING PANEL
        l3 = QVBoxLayout()

        lgg3 = QHBoxLayout()
        lgg3.setAlignment(Qt.AlignmentFlag.AlignTrailing)
        self.l3_banner1 = QLabel('')
        self.l3_banner2 = QLabel('get : self(user().logged)')
        lgg3.addWidget(QLabel('DeskPyL'))
        lgg3.addWidget(self.l3_banner1)
        lgg3.addWidget(self.l3_banner2)
        l3.addLayout(lgg3)

        l3.addStretch()
        self.w3.setLayout(l3)

# PAGE: DOWNLOAD DATA
        l4 = QVBoxLayout()

        lgg4 = QHBoxLayout()
        lgg4.setAlignment(Qt.AlignmentFlag.AlignTrailing)
        self.l4_banner1 = QLabel('')
        self.l4_banner2 = QLabel('get : self(user().logged)')
        lgg4.addWidget(QLabel('DeskPyL'))
        lgg4.addWidget(self.l4_banner1)
        lgg4.addWidget(self.l4_banner2)
        l4.addLayout(lgg4)

        l4.addWidget(QLabel('Descargar datos'))
        l4.addStretch()
        self.w4.setLayout(l4)

# PAGE: USERS ADMIN
        l5 = QVBoxLayout()
        l5.setContentsMargins(30,30,30,30)

        lgg5 = QHBoxLayout()
        lgg5.setAlignment(Qt.AlignmentFlag.AlignTrailing)
        self.l5_banner1 = QLabel('')
        self.l5_banner2 = QLabel('get : self(user().logged)')
        lgg5.addWidget(QLabel('DeskPyL'))
        lgg5.addWidget(self.l5_banner1)
        lgg5.addWidget(self.l5_banner2)
        l5.addLayout(lgg5)

        h1 = QLabel('Administración de usuarios')
        h2 = QLabel('Control Operativa Cumplimiento')

        stl_h1_h2(self, h1, h2)

        h1.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        h2.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        wr = QVBoxLayout()
        wr.addWidget(h1)
        wr.addWidget(h2)
        l5.addLayout(wr)

        # Query assistant.
        w_a = QHBoxLayout()

        t = QLabel('Usuario')
        t.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight)
        t.setMaximumWidth(70)

        w_a.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignHCenter)
        w_a.addWidget(t)

        self.au_searchx = QComboBox()
        self.au_searchx.setPlaceholderText('Seleccione un usuario')

        self.stored_users = []

        try:
            con = sqlite3.connect('settings.db')
            cur = con.cursor()

            req = cur.execute(f'SELECT * FROM user_settings')
            res = req.fetchall()

            for r in res:
                self.stored_users.append(r[0])

            con.close()
        except: pass

        self.au_searchx.addItems(self.stored_users)

        self.au_searchx.setObjectName('au_searchx')
        self.au_searchx.setMinimumWidth(250)

        w_a.addWidget(self.au_searchx)

        self.au_make_query = QPushButton('Buscar')
        self.au_make_query.setStyleSheet(f'padding: 3px 20px; color: {self.base}; font-size: 12px; border-radius: 9px;')
        self.au_make_query.setCursor(Qt.CursorShape.PointingHandCursor)
        self.au_make_query.clicked.connect(self.manage_user_changes)

        w_a.setAlignment(Qt.AlignmentFlag.AlignLeft)
        w_a.addWidget(self.au_make_query)
        w_a.addStretch()
        l5.addLayout(w_a)

        w_b = QHBoxLayout()
        w_b_1 = QVBoxLayout()

        g = QHBoxLayout()
        l = QLabel('Nombre de usuario')
        l.setFixedWidth(150)
        g.addWidget(l)
        self.aule_username = QLineEdit()
        self.aule_username.setFixedWidth(200)
        g.addWidget(self.aule_username)
        self.aule_username.setStyleSheet(f'padding: 3px 10px; background: {self.color}; color: {self.base}; border-radius: 12px;')
        w_b_1.addLayout(g)

        g = QHBoxLayout()
        l = QLabel('Nueva contraseña')
        l.setFixedWidth(150)
        g.addWidget(l)
        self.aule_password = QLineEdit()
        self.aule_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.aule_password.setFixedWidth(200)
        self.aule_password.setStyleSheet(f'padding: 3px 10px; background: {self.color}; color: {self.base}; border-radius: 12px;')
        g.addWidget(self.aule_password)
        w_b_1.addLayout(g)

        g = QHBoxLayout()
        l = QLabel('Confirmar contraseña')
        l.setFixedWidth(150)
        g.addWidget(l)
        self.aule_password_2 = QLineEdit()
        self.aule_password_2.setEchoMode(QLineEdit.EchoMode.Password)
        self.aule_password_2.setFixedWidth(200)
        self.aule_password_2.setStyleSheet(f'padding: 3px 10px; background: {self.color}; color: {self.base}; border-radius: 12px;')
        g.addWidget(self.aule_password_2)
        g.setContentsMargins(0,0,0,15)
        w_b_1.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        w_b_1.addLayout(g)

        self.aule_passwordsfields_change_echomode = QCheckBox('Mostrar contraseña.')
        self.aule_passwordsfields_change_echomode.clicked.connect(self.disable_echomode_for_aule)
        w_b_1.addWidget(self.aule_passwordsfields_change_echomode)

        w_b_2 = QVBoxLayout()

        self.au_cb_1 = QCheckBox('Asignar solicitudes a otros usuarios')
        self.au_cb_2 = QCheckBox('Cargar datos nuevos')
        self.au_cb_3 = QCheckBox('Generar/descargar reportes')
        self.au_cb_4 = QCheckBox('Crear registros manualmente')
        self.au_cb_5 = QCheckBox('Editar todos los campos')
        self.au_cb_6 = QCheckBox('Administrar otros usuarios')

        w_b_2.addWidget(self.au_cb_1)
        w_b_2.addWidget(self.au_cb_2)
        w_b_2.addWidget(self.au_cb_3)
        w_b_2.addWidget(self.au_cb_4)
        w_b_2.addWidget(self.au_cb_5)
        w_b_2.addWidget(self.au_cb_6)

        w_b.addLayout(w_b_1)
        w_b.addLayout(w_b_2)
        w_b.addStretch()
        l5.addLayout(w_b)

        # Make CRUD's for users logs.
        w = QHBoxLayout()
        self.au_crud_saveit = QPushButton('Guardar/Actualizar')
        self.au_crud_delete = QPushButton('Eliminar')
        self.au_crud_saveit.setCursor(Qt.CursorShape.PointingHandCursor)
        self.au_crud_delete.setCursor(Qt.CursorShape.PointingHandCursor)
        w.addWidget(self.au_crud_saveit)
        w.addWidget(self.au_crud_delete)
        self.au_crud_saveit.setObjectName('au_crud-1')
        self.au_crud_delete.setObjectName('au_crud-2')
        self.au_crud_saveit.clicked.connect(self.make_au_crud_saveit)
        w.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        w.setContentsMargins(30,30,30,30)
        l5.addLayout(w)

        l5.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.w5.setLayout(l5)

# PAGE: MY PROFILE
        l6 = QVBoxLayout()

        lgg6 = QHBoxLayout()
        lgg6.setAlignment(Qt.AlignmentFlag.AlignTrailing)
        self.l6_banner1 = QLabel('')
        self.l6_banner2 = QLabel('get : self(user().logged)')
        lgg6.addWidget(QLabel('DeskPyL'))
        lgg6.addWidget(self.l6_banner1)
        lgg6.addWidget(self.l6_banner2)
        l6.addLayout(lgg6)

        l6.addWidget(QLabel('Mi perfil'))
        l6.addStretch()
        self.w6.setLayout(l6)

# PAGE: SET UP ASSIGNMENTS
        l7 = QVBoxLayout()

        lgg7 = QHBoxLayout()
        lgg7.setAlignment(Qt.AlignmentFlag.AlignTrailing)
        self.l7_banner1 = QLabel('')
        self.l7_banner2 = QLabel('get : self(user().logged)')
        lgg7.addWidget(QLabel('DeskPyL'))
        lgg7.addWidget(self.l7_banner1)
        lgg7.addWidget(self.l7_banner2)
        l7.addLayout(lgg7)

        l7.addWidget(QLabel('Asignar las solicitudes nuevas'))

        l7.addStretch()
        self.w7.setLayout(l7)

        self.stacked_layout.addWidget(self.w0)
        self.stacked_layout.addWidget(self.w1)
        self.stacked_layout.addWidget(self.w2)
        self.stacked_layout.addWidget(self.w3)
        self.stacked_layout.addWidget(self.w4)
        self.stacked_layout.addWidget(self.w5)
        self.stacked_layout.addWidget(self.w6)
        self.stacked_layout.addWidget(self.w7)

        self.stacked_layout.setCurrentIndex(0)

        central_widget = QWidget()
        central_widget.setLayout(self.stacked_layout)
        self.setCentralWidget(central_widget)

        self.get_logged.setFocus()

        self.le_login_user.setText('system.gabriel.solano')
        self.le_login_passw.setText('root')
        self.get_logged.click()
        self.menu_settings_users.trigger()

    def toggle_display_pasw(self):
        if self.display_passw.isChecked(): self.le_login_passw.setEchoMode(QLineEdit.EchoMode.Normal)
        else: self.le_login_passw.setEchoMode(QLineEdit.EchoMode.Password)

    def bd_settings(self):
        con = sqlite3.connect('settings.db')
        cur = con.cursor()
        try:
            cur.execute('''
                CREATE TABLE user_settings(
                    USER_LOGGED VARCHAR(99) UNIQUE,
                    USER_PASSWORD VARCHAR(99),
                    MAKE_ASSIGNMENTS BOOLEAN,
                    DOWNLOAD_REPORTS BOOLEAN,
                    LOAD_BOOK BOOLEAN,
                    ADMIN_USERS BOOLEAN,
                    LOAD_ENTRY BOOLEAN,
                    EDIT_UPD_USERS BOOLEAN)
                ''')
            record = f'INSERT INTO user_settings VALUES ("system.gabriel.solano", "root", 1, 1, 1, 1, 1, 1)'
            cur.execute(record)
            record = f'INSERT INTO user_settings VALUES ("paola.castro", "pca$tr0", 1, 1, 1, 1, 1, 1)'
            cur.execute(record)
        except Exception as e: print(e)

        con.commit()
        con.close()

    def menu_events(self):
        self.bt_sender = self.sender().text()
        self.user_logged = []
        self.success_log = False

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
                        self.global_username = r[0]
                        self.success_log = True
                        break

                if self.success_log:
                    self.menu_file_signout.setDisabled(False)
                    self.menu_navg_home.setDisabled(False)
                    self.menu_navg_mydashboard.setDisabled(False)
                    self.menu_navg_processing.setDisabled(False)
                    self.menu_settings_account.setDisabled(False)

                    if self.user_logged[2] == 1: self.menu_navg_assign.setDisabled(False)
                    if self.user_logged[3] == 1: self.menu_tools_reports.setDisabled(False)
                    if self.user_logged[4] == 1: self.menu_tools_dataload.setDisabled(False)
                    if self.user_logged[5] == 1: self.menu_settings_users.setDisabled(False)

                    self.le_login_user.setText('')
                    self.le_login_passw.setText('')
                    self.stacked_layout.setCurrentIndex(1)

                    self.l1_banner2.setText(self.global_username)

                else:
                    QMessageBox.warning(
                        self,
                        'DeskPyL',
                        'Por favor verifique los datos ingresados.\t\t\nUsuario o clave incorrecta.',
                        QMessageBox.StandardButton.Ok,
                        QMessageBox.StandardButton.Ok)
                    self.le_login_passw.setText('')

                con.close()
            else:
                if typed_data_user.strip() == '': self.le_login_user.setStyleSheet('margin: 5px 0; padding: 5px 12px; color: #333; background: #eaa; border-radius: 12px;')
                if typed_data_pass.strip() == '': self.le_login_passw.setStyleSheet('margin: 5px 0; padding: 5px 12px; color: #333; background: #eaa; border-radius: 12px;')

        if self.bt_sender == '&Cerrar sesión':
            self.stacked_layout.setCurrentIndex(0)
            self.menu_file_signout.setDisabled(True)
            self.menu_navg_home.setDisabled(True)
            self.menu_navg_mydashboard.setDisabled(True)
            self.menu_navg_processing.setDisabled(True)
            self.menu_settings_account.setDisabled(True)
            self.menu_navg_assign.setDisabled(True)
            self.menu_tools_reports.setDisabled(True)
            self.menu_tools_dataload.setDisabled(True)
            self.menu_settings_users.setDisabled(True)
            self.display_passw.setChecked(False)
            self.statusbar.showMessage('Credenciales requeridas', 3000)
            self.le_login_passw.setEchoMode(QLineEdit.EchoMode.Password)
        elif self.bt_sender == '&Salir':
            self.destroy()
            sys.exit(app.exec())
        elif self.bt_sender == '&Inicio':
            self.stacked_layout.setCurrentIndex(1)
            self.l1_banner2.setText(self.global_username)

        elif self.bt_sender == '&Bandeja de asignaciones':
            self.stacked_layout.setCurrentIndex(2)
            self.l2_banner2.setText(self.global_username)

        elif self.bt_sender == '&Procesamiento de solicitudes':
            self.stacked_layout.setCurrentIndex(3)
            self.l3_banner2.setText(self.global_username)

        elif self.bt_sender == '&Cargar datos':
            pass
        elif self.bt_sender == '&Generar reportes':
            self.stacked_layout.setCurrentIndex(4)
            self.l4_banner2.setText(self.global_username)

        elif self.bt_sender == '&Administrar usuarios':
            self.stacked_layout.setCurrentIndex(5)
            self.l5_banner2.setText(self.global_username)

        elif self.bt_sender == '&Mi cuenta':
            self.stacked_layout.setCurrentIndex(6)
            self.l6_banner2.setText(self.global_username)

        elif self.bt_sender == '&Asignar solicitudes':
            self.stacked_layout.setCurrentIndex(7)
            self.l7_banner2.setText(self.global_username)

        elif self.bt_sender == '&Documentación':
            pass
        elif self.bt_sender == '&GitHub':
            pass

    def disable_echomode_for_aule(self):
        if self.aule_passwordsfields_change_echomode.isChecked():
            self.aule_password.setEchoMode(QLineEdit.EchoMode.Normal)
            self.aule_password_2.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.aule_password.setEchoMode(QLineEdit.EchoMode.Password)
            self.aule_password_2.setEchoMode(QLineEdit.EchoMode.Password)

    def manage_user_changes(self):
        query = self.au_searchx.currentText()
        self.queued_user = []
        con = sqlite3.connect('settings.db')
        cur = con.cursor()
        req = cur.execute('SELECT * FROM user_settings')
        res = req.fetchall()
        for r in res:
            if r[0] == query:
                self.queued_user = list(r)
                break

        if len(self.queued_user) > 0:
            if self.queued_user[2] == 1: self.au_cb_1.setChecked(True)        # DISPLAYED_NAME: Asignar solicitudes a otros usuarios
            else: self.au_cb_1.setChecked(False)
            if self.queued_user[3] == 1: self.au_cb_2.setChecked(True)        # DISPLAYED_NAME: Cargar datos nuevos
            else: self.au_cb_2.setChecked(False)
            if self.queued_user[4] == 1: self.au_cb_3.setChecked(True)        # DISPLAYED_NAME: Generar/descargar reportes
            else: self.au_cb_3.setChecked(False)
            if self.queued_user[5] == 1: self.au_cb_4.setChecked(True)        # DISPLAYED_NAME: Crear registros manualmente
            else: self.au_cb_4.setChecked(False)
            if self.queued_user[6] == 1: self.au_cb_5.setChecked(True)        # DISPLAYED_NAME: Editar todos los campos
            else: self.au_cb_5.setChecked(False)
            if self.queued_user[7] == 1: self.au_cb_6.setChecked(True)        # DISPLAYED_NAME: Administrar otros usuarios
            else: self.au_cb_6.setChecked(False)

            self.aule_username.setText(self.queued_user[0])
            self.aule_password.setText(self.queued_user[1])
            self.aule_password_2.setText(self.queued_user[1])

            self.statusbar.showMessage(f'User «{self.queued_user[0]}» succesfully queued, ready to uptdate', 3000)

        else:
            self.au_searchx.showPopup()
            self.statusbar.showMessage('You must have to select an user up to consult', 3000)

        con.close()

    def make_au_crud_saveit(self):
        query = self.aule_username.text()

        self.queued_user = []

        con = sqlite3.connect('settings.db')
        cur = con.cursor()
        cur.execute('SELECT * FROM user_settings WHERE user_logged = ?', (query,))
        res = cur.fetchone()

        def check_up_valid_entries(self):
            self.is_valid_data = [0, 0, 0]

            aule_username = self.aule_username.text()
            aule_password = self.aule_password.text()
            aule_password_2 = self.aule_password_2.text()

        # Username check up.
            # If username have not minimum length:
            if len(aule_username) < 8: self.is_valid_data[0] = 1
            else: self.is_valid_data[0] = 0

        # Password check up.
            # If passwords are differents:
            if aule_password != aule_password_2: self.is_valid_data[1] = 1
            else: self.is_valid_data[1] = 0

            # If password have not minimum lenght:
            if len(aule_password) < 6 or len(aule_password_2) < 6: self.is_valid_data[2] = 1
            else: self.is_valid_data[2] = 0

            warning_msg = 'Por favor corrija los campos:\n'

            if self.is_valid_data[0] == 1: warning_msg += ('\nEl nombre de usuario debe ser igual o mayor a 8 letras.\t')
            if self.is_valid_data[1] == 1: warning_msg += ('\nLas contraseñas no coinciden.\t')
            if self.is_valid_data[2] == 1: warning_msg += ('\nLa clave de usuario debe contener al menos 6 letras.\t')

            if self.is_valid_data[0] == 1 or self.is_valid_data[1] == 1 or self.is_valid_data[2] == 1:
                QMessageBox.warning(
                    self,
                    'DeskPyL',
                    warning_msg,
                    QMessageBox.StandardButton.Ok,
                    QMessageBox.StandardButton.Ok)
            else:
                QMessageBox.warning(
                    self,
                    'DeskPyL',
                    f'Registro de usuario "{aule_username}" creado/actualizado correctamente.\t',
                    QMessageBox.StandardButton.Ok,
                    QMessageBox.StandardButton.Ok)

        check_up_valid_entries(self)

        if self.is_valid_data[0] == 0 and self.is_valid_data[1] == 0 and self.is_valid_data[2] == 0:
            if res == None:
                record = f'INSERT INTO user_settings VALUES ("{self.aule_username.text().lower()}", "{self.aule_password.text()}", {self.au_cb_1.isChecked()}, {self.au_cb_2.isChecked()}, {self.au_cb_3.isChecked()}, {self.au_cb_4.isChecked()}, {self.au_cb_5.isChecked()}, {self.au_cb_6.isChecked()})'
                cur.execute(record)

                self.au_searchx.clear()

                req = cur.execute(f'SELECT * FROM user_settings')
                res = req.fetchall()
                for r in res:
                    self.au_searchx.addItem(r[0])

                self.statusbar.showMessage(f'The user «{self.aule_username.text().lower()}» was created sucessfully!',5000)

            else:
                write = f'UPDATE user_settings SET user_logged = "{self.aule_username.text().lower()}", user_password = "{self.aule_password.text()}", make_assignments = {self.au_cb_1.isChecked()}, load_book = {self.au_cb_2.isChecked()}, download_reports = {self.au_cb_3.isChecked()}, load_entry = {self.au_cb_4.isChecked()}, edit_upd_users = {self.au_cb_5.isChecked()}, admin_users = {self.au_cb_6.isChecked()} WHERE user_logged = ?'
                cur.execute(write, (query,))

        con.commit()
        con.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet("""
        """)
    app.setStyleSheet(Path('user_admin.qss').read_text())
    win = Main()
    sys.exit(app.exec())