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


class AccessAccounting(QWidget):
    def __init__(self, menu_window: QWidget):
        super().__init__()

        self.menu_window = menu_window
        self.db = DBConnection()

        # параметры окна
        self.setGeometry(100, 100, 1000, 520)
        self.setFixedSize(1000, 520)
        self.setWindowTitle("Учет доступа")
        self.tb = AccessAccountingTb(self)

        # Окно по центру
        qt_rectangle = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        qt_rectangle.moveCenter(center_point)
        self.move(qt_rectangle.topLeft())

        #Оформление
        self.tb.setStyleSheet("""
                            background-color: white;
                """)

        self.setStyleSheet("""
                            * {
                                background-color: rgb(223, 235, 250);
                                }
                            .QPushButton {
                                background-color: rgb(171, 204, 249); 
                                }
                            .QPushButton:hover {
                                background-color: rgb(207, 203, 249)
                                }
                            .QLineEdit {
                                background-color: white;
                                border: 1px solid black;
                                border-radius: 10px;
                                }
                        """)

        # поле идентификатор
        self.lbl = QLabel("Номер:", self)
        self.lbl.move(520, 70)
        self.idaa = QLineEdit(self)
        self.idaa.resize(150, 40)
        self.idaa.move(610, 60)

        # поле сотрудник
        self.lbl = QLabel("Сотрудник:", self)
        self.lbl.move(520, 120)
        self.ei = QLineEdit(self)
        self.ei.resize(150, 40)
        self.ei.move(610, 110)

        # поле дни недели
        self.lbl = QLabel("Точка доступа:", self)
        self.lbl.move(520, 170)
        self.pi = QLineEdit(self)
        self.pi.resize(150, 40)
        self.pi.move(610, 160)

        # поле время входа
        self.lbl = QLabel("Событие:", self)
        self.lbl.move(520, 220)
        self.evi = QLineEdit(self)
        self.evi.resize(150, 40)
        self.evi.move(610, 210)

        # поле время выхода
        self.lbl = QLabel("Дата:", self)
        self.lbl.move(520, 270)
        self.dt = QLineEdit(self)
        self.dt.resize(150, 40)
        self.dt.move(610, 260)
        # поле время выхода
        self.lbl = QLabel("Время:", self)
        self.lbl.move(520, 320)
        self.t = QLineEdit(self)
        self.t.resize(150, 40)
        self.t.move(610, 310)

        # кнопка добавить запись
        self.btn = QPushButton("Добавить", self)
        self.btn.resize(150, 40)
        self.btn.move(800, 60)
        self.btn.clicked.connect(self.ins)

        # кнопка редактировать
        self.btn = QPushButton("Редактировать", self)
        self.btn.resize(150, 40)
        self.btn.move(800, 120)
        self.btn.clicked.connect(self.upentry)

        # кнопка удалить запись
        self.btn = QPushButton("Удалить", self)
        self.btn.resize(150, 40)
        self.btn.move(800, 180)
        self.btn.clicked.connect(self.dels)

        # кнопка Главное меню
        self.btn = QPushButton("Главное меню", self)
        self.btn.resize(150, 40)
        self.btn.move(800, 240)
        self.btn.clicked.connect(self.go_back_to_menu)

        # кнопка выход
        self.btn = QPushButton("Выход", self)
        self.btn.resize(150, 40)
        self.btn.move(800, 470)
        self.btn.clicked.connect(self.close_clicked)

    #Вернуться на главное меню
    def go_back_to_menu(self):
        self.menu_window.show()
        self.close()

    # обновить таблицу и поля
    def upd(self):
        self.db.conn.commit()
        self.tb.updt()
        self.idaa.setText("")
        self.ei.setText("")
        self.pi.setText("")
        self.evi.setText("")
        self.dt.setText("")
        self.t.setText("")

    # добавить таблицу новую строку
    def ins(self):

        try:
            idaa, ei, pi, evi, dt, t = (
                self.idaa.text(),
                self.ei.text(),
                self.pi.text(),
                self.evi.text(),
                self.dt.text(),
                self.t.text()
            )
            self.db.cur.execute(
                "insert into ACCESSACCOUNTING (ACCOUNTINGID,EMPLOYEEID,POINTID,EVENTID,ACDATE,ACTIME) values (?,?,?,?,?,?)",
                (idaa, ei, pi, evi, dt, t)
            )
            QMessageBox.about(self, " ", "Данные добавлены!")
        except:
            QMessageBox.about(self, "Ошибка!", "Данные не добавлены, повторите попытку")
            pass
        self.upd()

    # Редактировать строку
    def upentry(self):
        try:
            idaa, ei, pi, evi, dt, t = (
                self.idaa.text(),
                self.ei.text(),
                self.pi.text(),
                self.evi.text(),
                self.dt.text(),
                self.t.text()
            )
            self.db.cur.execute(
                "update ACCESSACCOUNTING set EMPLOYEEID=?, POINTID=?,EVENTID=?,ACDATE=?,ACTIME=? where ACCOUNTINGID=?",
                (ei, pi, evi, dt, t, idaa),
            )
            self.db.conn.commit()
            self.tb.updt()
            self.idaa.setText("")
            self.ei.setText("")
            self.pi.setText("")
            self.evi.setText("")
            self.dt.setText("")
            self.t.setText("")
            QMessageBox.about(self, " ", "Данные изменены!")
        except:
            QMessageBox.about(self, "Ошибка!", "Данные не изменены, повторите попытку")
        self.db.conn.commit()

    # удалить из таблицы строку
    def dels(self):
        try:
            idaa = int(self.idaa.text())
            self.db.cur.execute("delete from ACCESSACCOUNTING where ACCOUNTINGID=?", (idaa,))# идентификатор строки
            QMessageBox.about(self, " ", "Данные удалены")
        except:
            QMessageBox.about(self, "Ошибка!", "Данные не удалены")
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
class AccessAccountingTb(QTableWidget):
    def __init__(self, wg):
        self.wg = wg  # запомнить окно, в котором эта таблица показывается
        self.db = wg.db

        super().__init__(wg)
        self.setGeometry(10, 10, 481, 500)
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
            ["Номер", "Сотрудник", "Точка доступа", "Событие", "Дата", "Время"]
        )
        self.db.cur.execute("select * from ACCESSACCOUNTING")
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
        self.wg.idaa.setText(self.item(row, 0).text())
        self.wg.ei.setText(self.item(row, 1).text().strip())
        self.wg.pi.setText(self.item(row, 2).text().strip())
        self.wg.evi.setText(self.item(row, 3).text().strip())
        self.wg.dt.setText(self.item(row, 4).text().strip())
        self.wg.t.setText(self.item(row, 5).text().strip())
