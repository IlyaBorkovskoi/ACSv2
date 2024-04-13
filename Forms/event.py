from PyQt5.QtWidgets import (
    QTableWidget,
    QMessageBox,
    QLabel,
    QDesktopWidget,
)
from PyQt5.QtWidgets import QTableWidgetItem, QWidget, QPushButton, QLineEdit

from db_connection import DBConnection


# Класс Событие
class Event(QWidget):
    def __init__(self, menu_window: QWidget):
        super().__init__()
        self.menu_window = menu_window
        self.db = DBConnection()

        # параметры окна
        self.setGeometry(100, 100, 1000, 600)
        self.setWindowTitle("События")
        self.tb = EventTB(self)

        # Окно по центру
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

        # поле идентификатор
        self.lbl = QLabel("Номер:", self)
        self.lbl.move(600, 70)
        self.ide = QLineEdit(self)
        self.ide.resize(150, 40)
        self.ide.move(700, 60)
        # поле наименование события
        self.lbl = QLabel("Наименование:", self)
        self.lbl.move(600, 120)
        self.en = QLineEdit(self)
        self.en.resize(150, 40)
        self.en.move(700, 110)
        # поле описание
        self.lbl = QLabel("Описание:", self)
        self.lbl.move(600, 170)
        self.d = QLineEdit(self)
        self.d.resize(150, 40)
        self.d.move(700, 160)
        # кнопка добавить запись
        self.btn = QPushButton("Добавить", self)
        self.btn.resize(150, 40)
        self.btn.move(700, 220)
        self.btn.clicked.connect(self.ins)
        # кнопка редактировать
        self.btn = QPushButton("Редактировать", self)
        self.btn.resize(150, 40)
        self.btn.move(700, 270)
        self.btn.clicked.connect(self.upentry)
        # кнопка удалить запись
        self.btn = QPushButton("Удалить", self)
        self.btn.resize(150, 40)
        self.btn.move(700, 320)
        self.btn.clicked.connect(self.dels)
        # кнопка выход
        self.btn = QPushButton("Выход", self)
        self.btn.resize(150, 40)
        self.btn.move(700, 420)
        self.btn.clicked.connect(self.close_clicked)
        # кнопка Главное меню
        self.btn = QPushButton("Главное меню", self)
        self.btn.resize(150, 40)
        self.btn.move(700, 370)
        self.btn.clicked.connect(self.menu_clicked)

    # обновить таблицу и поля
    def upd(self):
        self.db.conn.commit()
        self.tb.updt()
        self.ide.setText("")
        self.en.setText("")
        self.d.setText("")

    # добавить таблицу новую строку
    def ins(self):
        ide, en, d = self.ide.text(), self.en.text(), self.d.text()
        try:
            self.db.cur.execute(
                "insert into EVENT (EVENTID,EVENTNAME,DESCRIPTION) values (?,?,?)",
                (ide, en, d),
            )
            QMessageBox.about(self, " ", "Данные добавлены")
        except:
            QMessageBox.about(self, "Ошибка", "Данные не добавлены")
            pass
        self.upd()

    # Редактировать строку
    def upentry(self):
        ide, en, d = self.ide.text(), self.en.text(), self.d.text()
        self.db.cur.execute(
            "update EVENT set EVENTNAME=?,DISCRIPTION=? where EVENTID=?", (en, d, ide)
        )
        try:
            QMessageBox.about(self, " ", "Данные изменены")
        except:
            QMessageBox.about(self, "Ошибка", "Данные не изменены")
        self.db.conn.commit()

    # удалить из таблицы строку
    def dels(self):
        try:
            ide = int(self.ide.text())  # идентификатор строки
            QMessageBox.about(self, " ", "Данные удалены")
        except:
            QMessageBox.about(self, "Ошибка", "Данные не удалены")
            return
        self.db.cur.execute("delete from EVENT where EVENTID=?", (ide,))
        self.upd()

    # Закрыть окно
    def close_clicked(self):
        self.close()

    # Переход в главное меню
    def menu_clicked(self):
        self.menu_window.show()
        self.close()


# Класс  таблица Должностей
class EventTB(QTableWidget):
    def __init__(self, wg):
        self.wg = wg  # запомнить окно, в котором эта таблица показывается

        self.db = wg.db

        super().__init__(wg)
        self.setGeometry(10, 10, 560, 500)
        self.setColumnCount(3)
        self.verticalHeader().hide()
        self.updt()  # обновить таблицу
        self.setEditTriggers(QTableWidget.NoEditTriggers)  # запретить изменять поля
        self.cellClicked.connect(
            self.cellClick
        )  # установить обработчик щелча мыши в таблице

    # обновление таблицы
    def updt(self):
        self.clear()
        self.setRowCount(0)
        self.setHorizontalHeaderLabels(
            ["Номер", "Наименование", "Описание"]
        )  # заголовки столбцов
        self.db.cur.execute("select * from EVENT order by EVENTNAME")
        rows = self.db.cur.fetchall()
        i = 0
        for elem in rows:
            self.setRowCount(self.rowCount() + 1)
            j = 0
            for t in elem:  # заполняем внутри строки
                self.setItem(i, j, QTableWidgetItem(str(t).strip()))
                j += 1
            i += 1
        self.resizeColumnsToContents()

    # обработка щелчка мыши по таблице
    def cellClick(self, row, col):  # row - номер строки, col - номер столбца
        self.wg.ide.setText(self.item(row, 0).text())
        self.wg.en.setText(self.item(row, 1).text().strip())
        self.wg.d.setText(self.item(row, 2).text().strip())
