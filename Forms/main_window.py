from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import (
    QLabel,
    QDesktopWidget, QHBoxLayout,
)
from PyQt5.QtWidgets import (
    QWidget,
    QPushButton,
)

# Импорт всех форм для открытия из главного окна
from Forms.access_schedule import AccessSchedule
from Forms.employee import Employees
from Forms.event import Event
from Forms.access_point import AccessPoint
from Forms.post import Post
from Forms.access_accounting import AccessAccounting


# Главное окно, содержит навигационную панель
# для перехода по формам
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        # Тут вся инициализация главного окна
        # вызываем функции помощники
        self.create_main_window()
        self.create_form_buttons()


    def create_main_window(self):
        # Создаём окошко
        self.setGeometry(100, 100, 700, 500)
        self.setFixedSize(700,500)
        self.setWindowTitle("Система контроля и управления доступом")
        self.lbl = QLabel("    Система контроля \nи управления доступом", self)
        self.lbl.setFont(QFont("Times", 15))
        self.lbl.move(330, 40)
        hbox = QHBoxLayout(self)
        pixmap = QPixmap("mm.png")
        lbl = QLabel(self)
        lbl.setPixmap(pixmap)
        hbox.addWidget(lbl)
        self.setLayout(hbox)



        # Ставим окно в центр
        qt_rectangle = self.frameGeometry()
        central_point = QDesktopWidget().availableGeometry().center()
        qt_rectangle.moveCenter(central_point)
        self.move(qt_rectangle.topLeft())

    def create_form_buttons(self):
        # кнопка перехода в Сотрудники
        self.button = QPushButton("Сотрудники", self)
        self.button.resize(150, 40)
        self.button.move(50, 50)
        self.button.clicked.connect(self.employees_clicked)

        self.button = QPushButton("Должности", self)
        self.button.resize(150, 40)
        self.button.move(50, 120)
        self.button.clicked.connect(self.post_clicked)

        # кнопка перехода в График доступа
        self.button = QPushButton("График доступа", self)
        self.button.resize(150, 40)
        self.button.move(50, 190)
        self.button.clicked.connect(self.access_schedule_clicked)

        # кнопка перехода в Учет доступа
        self.button = QPushButton("Учет доступа", self)
        self.button.resize(150, 40)
        self.button.move(50, 260)
        self.button.clicked.connect(self.access_ac_clicked)

        # кнопка перехода в Точка доступа
        self.button = QPushButton("Точки доступа", self)
        self.button.resize(150, 40)
        self.button.move(50, 330)
        self.button.clicked.connect(self.access_point_clicked)

        # кнопка перехода в События
        self.button = QPushButton("События", self)
        self.button.resize(150, 40)
        self.button.move(50, 400)
        self.button.clicked.connect(self.event_clicked)

        # кнопка выход
        self.btn = QPushButton("Выход", self)
        self.btn.resize(150, 40)
        self.btn.move(500, 400)
        self.btn.clicked.connect(self.close_main_window_clicked)

    # Закрыть окно
    def close_main_window_clicked(self):
        self.close()

    # Кнопка перехода в Должности
    def post_clicked(self):
        self.PW = Post(self)
        self.PW.show()
        self.hide()

    # Кнопка перехода в График доступа
    def access_schedule_clicked(self):
        self.ASW = AccessSchedule(self)
        self.ASW.show()
        self.close()

    # Кнопка перехода в точки доступа
    def access_point_clicked(self):
        self.APW = AccessPoint(self)
        self.APW.show()
        self.close()

    # Кнопка перехода в События
    def event_clicked(self):
        self.EW = Event(self)
        self.EW.show()
        self.close()

    # Кнопка перехода в Сотрудники
    def employees_clicked(self):
        self.EPW = Employees(self)
        self.EPW.show()
        self.close()
    #Кнопка перехода в Учет доступа
    def access_ac_clicked(self):
        self.AAW = AccessAccounting(self)
        self.AAW.show()
        self.close()
