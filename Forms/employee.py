import sys
import fdb
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QApplication,
    QTableWidget,
    QMessageBox,
    QLabel,
    QDesktopWidget,
)
from PyQt5.QtWidgets import QTableWidgetItem, QWidget, QPushButton, QLineEdit

from db_connection import DBConnection


# Класс Сотрудники
class Employees(QWidget):
    def __init__(self, menu_window: QWidget):
        super().__init__()
        self.menu_window = menu_window
        self.db = DBConnection()

        # параметры окна
        self.setGeometry(100, 100, 1200, 600)
        self.setWindowTitle("Сотрудники")
        self.tb = Employees_tb(self)
        # Окно по центру
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

        # поле идентификатор
        self.lbl = QLabel("Номер:", self)
        self.lbl.move(700, 85)
        self.idem = QLineEdit(self)
        self.idem.resize(150, 40)
        self.idem.move(800, 80)
        # поле Должность
        self.lbl = QLabel("Должность:", self)
        self.lbl.move(700, 135)
        self.pi = QLineEdit(self)
        self.pi.resize(150, 40)
        self.pi.move(800, 130)
        # поле Фамилия
        self.lbl = QLabel("Фамилия:", self)
        self.lbl.move(700, 185)
        self.ln = QLineEdit(self)
        self.ln.resize(150, 40)
        self.ln.move(800, 180)
        # поле Имя
        self.lbl = QLabel("Имя:", self)
        self.lbl.move(700, 235)
        self.fn = QLineEdit(self)
        self.fn.resize(150, 40)
        self.fn.move(800, 230)
        # поле Отчество
        self.lbl = QLabel("Отчество:", self)
        self.lbl.move(700, 285)
        self.mn = QLineEdit(self)
        self.mn.resize(150, 40)
        self.mn.move(800, 280)
        # поле Ключ
        self.lbl = QLabel("Ключ:", self)
        self.lbl.move(700, 335)
        self.k = QLineEdit(self)
        self.k.resize(150, 40)
        self.k.move(800, 330)
        # кнопка добавить запись
        self.btn = QPushButton("Добавить", self)
        self.btn.resize(150, 40)
        self.btn.move(1000, 80)
        self.btn.clicked.connect(self.ins)
        # кнопка редактировать
        self.btn = QPushButton("Редактировать", self)
        self.btn.resize(150, 40)
        self.btn.move(1000, 160)
        self.btn.clicked.connect(self.upentry)
        # кнопка удалить запись
        self.btn = QPushButton("Удалить", self)
        self.btn.resize(150, 40)
        self.btn.move(1000, 240)
        self.btn.clicked.connect(self.dels)
        # кнопка Главное меню
        self.btn = QPushButton("Главное меню", self)
        self.btn.resize(150, 40)
        self.btn.move(1000, 320)
        self.btn.clicked.connect(self.menu_clicked)

        # кнопка выход
        self.btn = QPushButton("Выход", self)
        self.btn.resize(150, 40)
        self.btn.move(1000, 500)
        self.btn.clicked.connect(self.close_clicked)

        # обновить таблицу и поля
    def upd(self):
        self.db.conn.commit()
        self.tb.updt()
        self.idem.setText("")
        self.pi.setText("")
        self.ln.setText("")
        self.fn.setText("")
        self.mn.setText("")
        self.k.setText("")

    # добавить таблицу новую строку
    def ins(self):
        try:
            idem, pi, ln, fn, mn, k = (
                self.idem.text(),
                self.pi.text(),
                self.ln.text(),
                self.fn.text(),
                self.mn.text(),
                self.k.text(),
            )
            self.db.cur.execute(
                "insert into EMPLOYEES (EMPLOYEEID,POSTID,EMPLASTNAME,EMPFIRSTNAME,MIDLNAME,EMPKEY) values (?,?,?,?,?,?)",
                (idem, pi, ln, fn, mn, k),
            )
            QMessageBox.about(self, " ", "Данные добавлены!")
        except:
            QMessageBox.about(self, "Ошибка!", "Данные не добавлены2, повторите попытку")
            pass
        self.upd()

    # Редактировать строку
    def upentry(self):
        try:
            idem, pi, ln, fn, mn, k = (
                self.idem.text(),
                self.pi.text(),
                self.ln.text(),
                self.fn.text(),
                self.mn.text(),
                self.k.text(),
            )
            self.db.cur.execute(
                "update EMPLOYEES set POSTID=?,EMPLASTNAME=?,EMPFIRSTNAME=?,MIDLNAME=?,EMPKEY=? where EMPLOYEEID=?",
                (pi, ln, fn, mn, k, idem),
            )
            self.db.conn.commit()
            self.tb.updt()
            self.idem.setText("")
            self.pi.setText("")
            self.ln.setText("")
            self.fn.setText("")
            self.mn.setText("")
            self.k.setText("")
            QMessageBox.about(self, " ", "Данные изменены!")
        except:
            QMessageBox.about(self, "Ошибка!", "Данные не изменены, повторите попытку")
        self.db.conn.commit()

    # удалить из таблицы строку
    def dels(self):
        try:
            idem = int(self.idem.text())  # идентификатор строки
            self.db.cur.execute("delete from EMPLOYEES where EMPLOYEEID=?", (idem,))
            QMessageBox.about(self, " ", "Данные удалены!")
        except:
            QMessageBox.about(self, "Ошибка!", "Данные не удалены, повторите попытку")
            return
        self.upd()


    # Закрыть окно
    def close_clicked(self):
        self.close()

    # Переход в главное меню
    def menu_clicked(self):
        self.menu_window.show()
        self.close()


# Класс  таблица График доступа
class Employees_tb(QTableWidget):
    def __init__(self, wg):
        self.wg = wg  # запомнить окно, в котором эта таблица показывается
        self.db = wg.db

        super().__init__(wg)
        self.setGeometry(10, 10, 660, 500)
        self.setColumnCount(6)
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
            ["Номер", "Должность", "Фамилия", "Имя", "Отчество", "Ключ"]
        )
        self.db.cur.execute("select * from EMPLOYEES order by EMPLASTNAME")
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
        self.wg.idem.setText(self.item(row, 0).text())
        self.wg.pi.setText(self.item(row, 1).text().strip())
        self.wg.ln.setText(self.item(row, 2).text().strip())
        self.wg.fn.setText(self.item(row, 3).text().strip())
        self.wg.mn.setText(self.item(row, 4).text().strip())
        self.wg.k.setText(self.item(row, 5).text().strip())
