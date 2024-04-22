from PyQt5.QtWidgets import (
    QTableWidget,
    QMessageBox,
    QLabel,
    QDesktopWidget,
)
from PyQt5.QtWidgets import (
    QTableWidgetItem,
    QWidget,
    QPushButton,
    QLineEdit,
)

from db_connection import DBConnection


class AccessSchedule(QWidget):
    def __init__(self, menu_window: QWidget):
        super().__init__()

        self.menu_window = menu_window
        self.db = DBConnection()

        # параметры окна
        self.setGeometry(100, 100, 1000, 520)
        self.setWindowTitle("График доступа")
        self.tb = Access_schedule_tb(self)

        # Окно по центру
        qt_rectangle = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        qt_rectangle.moveCenter(center_point)
        self.move(qt_rectangle.topLeft())

        # поле идентификатор
        self.lbl = QLabel("Номер:", self)
        self.lbl.move(520, 70)
        self.idas = QLineEdit(self)
        self.idas.resize(150, 40)
        self.idas.move(610, 60)

        # поле сотрудник
        self.lbl = QLabel("Сотрудник", self)
        self.lbl.move(520, 120)
        self.ei = QLineEdit(self)
        self.ei.resize(150, 40)
        self.ei.move(610, 110)

        # поле дни недели
        self.lbl = QLabel("Дни недели", self)
        self.lbl.move(520, 170)
        self.wd = QLineEdit(self)
        self.wd.resize(150, 40)
        self.wd.move(610, 160)

        # поле время входа
        self.lbl = QLabel("Время входа", self)
        self.lbl.move(520, 220)
        self.et = QLineEdit(self)
        self.et.resize(150, 40)
        self.et.move(610, 210)

        # поле время выхода
        self.lbl = QLabel("Время выхода", self)
        self.lbl.move(520, 270)
        self.ext = QLineEdit(self)
        self.ext.resize(150, 40)
        self.ext.move(610, 260)

        # кнопка добавить запись
        self.btn = QPushButton("Добавить", self)
        self.btn.resize(150, 40)
        self.btn.move(800, 60)
        self.btn.clicked.connect(self.ins)

        # кнопка редактировать
        self.btn = QPushButton("Редактировать", self)
        self.btn.resize(150, 40)
        self.btn.move(800, 125)
        self.btn.clicked.connect(self.upentry)

        # кнопка удалить запись
        self.btn = QPushButton("Удалить", self)
        self.btn.resize(150, 40)
        self.btn.move(800, 190)
        self.btn.clicked.connect(self.dels)

        # кнопка Главное меню
        self.btn = QPushButton("Главное меню", self)
        self.btn.resize(150, 40)
        self.btn.move(800, 260)
        self.btn.clicked.connect(self.go_back_to_menu)

        # кнопка выход
        self.btn = QPushButton("Выход", self)
        self.btn.resize(150, 40)
        self.btn.move(800, 450)
        self.btn.clicked.connect(self.close_clicked)

    def go_back_to_menu(self):
        self.menu_window.show()
        self.close()

    # обновить таблицу и поля
    def upd(self):
        self.db.conn.commit()
        self.tb.updt()
        self.idas.setText("")
        self.ei.setText("")
        self.wd.setText("")
        self.et.setText("")
        self.ext.setText("")

    # добавить таблицу новую строку
    def ins(self):
        idas, ei, wd, et, ext = (
            self.idas.text(),
            self.ei.text(),
            self.wd.text(),
            self.et.text(),
            self.ext.text(),
        )
        try:
            self.db.cur.execute(
                "insert into ACCESSSCHEDULE (SCHEDULEID,EMPLOYEEID,ACWEEKDAY,ENTRYTIME,EXITTIME) values (?,?,?,?,?)",
                (idas, ei, wd, et, ext),
            )
            QMessageBox.about(self, " ", "Данные добавлены")
        except:
            QMessageBox.about(self, "Ошибка", "Данные не добавлены")
            pass
        self.upd()

    # Редактировать строку
    def upentry(self):
        idas, ei, wd, et, ext = (
            self.idas.text(),
            self.ei.text(),
            self.wd.text(),
            self.et.text(),
            self.ext.text(),
        )
        self.db.cur.execute(
            "update ACCESSSCHEDULE set EMPLOYEEID=?, ACWEEKDAY=?,ENTRYTIME=?,EXITTIME=? where SCHEDULEID=?",
            (ei, wd, et, ext, idas),
        )
        self.db.conn.commit()
        self.tb.updt()
        self.idas.setText("")
        self.ei.setText("")
        self.wd.setText("")
        self.et.setText("")
        self.ext.setText("")
        try:
            QMessageBox.about(self, " ", "Данные изменены")
        except:
            QMessageBox.about(self, "Ошибка", "Данные не изменены")

    # удалить из таблицы строку
    def dels(self):
        try:
            idas = int(self.idas.text())  # идентификатор строки

        except:
            QMessageBox.about(self, "Ошибка", "Данные не удалены")
            return
        self.db.cur.execute("delete from ACCESSSCHEDULE where SCHEDULEID=?", (idas,))
        self.upd()
        QMessageBox.about(self, " ", "Данные удалены")

    # Закрыть окно
    def close_clicked(self):
        self.close()

    # Переход в главное меню
    def menu_clicked(self):
        self.menu_window.show()
        self.close()


# Класс  таблица График доступа
class Access_schedule_tb(QTableWidget):
    def __init__(self, wg):
        self.wg = wg  # запомнить окно, в котором эта таблица показывается
        self.db = wg.db

        super().__init__(wg)
        self.setGeometry(10, 10, 481, 500)
        self.setColumnCount(5)
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
            ["Номер", "Сотрудник", "День недели", "Время входа", "Время выхода"]
        )
        self.db.cur.execute("select * from ACCESSSCHEDULE")
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
        self.wg.idas.setText(self.item(row, 0).text())
        self.wg.ei.setText(self.item(row, 1).text().strip())
        self.wg.wd.setText(self.item(row, 2).text().strip())
        self.wg.et.setText(self.item(row, 3).text().strip())
        self.wg.ext.setText(self.item(row, 4).text().strip())
