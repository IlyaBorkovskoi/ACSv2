from PyQt5.QtWidgets import (
    QTableWidget,
    QMessageBox,
    QLabel,
    QDesktopWidget,
)
from PyQt5.QtWidgets import QTableWidgetItem, QWidget, QPushButton, QLineEdit

from db_connection import DBConnection


# Класс Должности
class AccessPoint(QWidget):
    def __init__(self, menu_window: QWidget):
        super().__init__()
        self.menu_window = menu_window
        self.db = DBConnection()

        # параметры окна
        self.setGeometry(100, 100, 700, 520)
        self.setFixedSize(700, 520)
        self.setWindowTitle("Точки доступа")
        self.tb = AccessPointTB(self)
        # Окно по центру
        qt_rectangle = self.frameGeometry()
        central_point = QDesktopWidget().availableGeometry().center()
        qt_rectangle.moveCenter(central_point)
        self.move(qt_rectangle.topLeft())
        # self.btn.clicked.connect(self.menu_clicked)
        # поле идентификатор
        self.lbl = QLabel("Номер:", self)
        self.lbl.move(420, 70)
        self.idap = QLineEdit(self)
        self.idap.resize(150, 40)
        self.idap.move(520, 60)
        # поле название точки
        self.lbl = QLabel("Наименование:", self)
        self.lbl.move(420, 120)
        self.pn = QLineEdit(self)
        self.pn.resize(150, 40)
        self.pn.move(520, 110)
        # поле помещение
        self.lbl = QLabel("Помещение:", self)
        self.lbl.move(420, 170)
        self.r = QLineEdit(self)
        self.r.resize(150, 40)
        self.r.move(520, 160)
        # кнопка добавить запись
        self.btn = QPushButton("Добавить", self)
        self.btn.resize(150, 40)
        self.btn.move(520, 220)
        self.btn.clicked.connect(self.ins)
        # кнопка редактировать
        self.btn = QPushButton("Редактировать", self)
        self.btn.resize(150, 40)
        self.btn.move(520, 270)
        self.btn.clicked.connect(self.upentry)
        # кнопка удалить запись
        self.btn = QPushButton("Удалить", self)
        self.btn.resize(150, 40)
        self.btn.move(520, 320)
        self.btn.clicked.connect(self.dels)
        # кнопка выход
        self.btn = QPushButton("Выход", self)
        self.btn.resize(150, 40)
        self.btn.move(520, 470)
        self.btn.clicked.connect(self.close_clicked)
        # кнопка Главное меню
        self.btn = QPushButton("Главное меню", self)
        self.btn.resize(150, 40)
        self.btn.move(520, 370)
        self.btn.clicked.connect(self.menu_clicked)

    # обновить таблицу и поля
    def upd(self):
        self.db.conn.commit()
        self.tb.updt()
        self.idap.setText("")
        self.pn.setText("")
        self.r.setText("")

    # добавить таблицу новую строку
    def ins(self):
        try:
            idap, pn, r = self.idap.text(), self.pn.text(), self.r.text()
            self.db.cur.execute(
                "insert into ACCESSPOINTS (POINTID,POINTNAME,ROOM) values (?,?,?)",
                (idap, pn, r),
            )
            QMessageBox.about(self, " ", "Данные добавлены!")
        except:
            QMessageBox.about(self, "Ошибка!", "Данные не добавлены, повторите попытку")
            pass
        self.upd()

    # Редактировать строку
    def upentry(self):
        try:
            idap, pn, r = (
                self.idap.text(),
                self.pn.text(),
                self.r.text(),
            )
            self.db.cur.execute(
                "update ACCESSPOINTS set POINTNAME=?, ROOM=? where POINTID=?",
                (pn, r, idap),
            )
            self.db.conn.commit()
            self.tb.updt()
            self.idap.setText("")
            self.pn.setText("")
            self.r.setText("")
            QMessageBox.about(self, " ", "Данные изменены")
        except:
            QMessageBox.about(self, "Ошибка", "Данные не изменены, повторите попытку")

    # удалить из таблицы строку
    def dels(self):
        try:
            idap = int(self.idap.text())  # идентификатор строки
            QMessageBox.about(self, " ", "Данные удалены")
            self.db.cur.execute("delete from ACCESSPOINTS where POINTID=?", (idap,))
        except:
            QMessageBox.about(self, "Ошибка", "Данные не удалены")
            return
        self.upd()

    # Закрыть окно
    def close_clicked(self):
        self.close()

    # Переход в главное меню
    def menu_clicked(self):
        self.menu_window.show()
        self.close()


# Класс  таблица Должностей
class AccessPointTB(QTableWidget):
    def __init__(self, wg):
        self.wg = wg  # запомнить окно, в котором эта таблица показывается
        self.db = wg.db
        super().__init__(wg)
        self.setGeometry(10, 10, 380, 500)
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
            ["Номер", "Точка доступа", "Помещение"]
        )  # заголовки столбцов
        self.db.cur.execute("select * from ACCESSPOINTS order by POINTNAME")
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
        self.wg.idap.setText(self.item(row, 0).text())
        self.wg.pn.setText(self.item(row, 1).text().strip())
        self.wg.r.setText(self.item(row, 2).text().strip())
