from PyQt5.QtWidgets import (
    QTableWidget,
    QMessageBox,
    QLabel,
    QDesktopWidget,
)
from PyQt5.QtWidgets import QTableWidgetItem, QWidget, QPushButton, QLineEdit

from db_connection import DBConnection



# Класс Должности
class Post(QWidget):
    def __init__(self, menu_window: QWidget):
        super().__init__()
        self.menu_window = menu_window
        self.db = DBConnection()

        # параметры окна
        self.setGeometry(100, 100, 600, 520)
        self.setFixedSize(600, 520)
        self.setWindowTitle("Должности ")
        self.tb = Post_tb(self)
        # Окно по центру
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

        # Оформление
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

        # здесь идентификатор
        self.lbl = QLabel("Номер:", self)
        self.lbl.move(310, 70)
        self.idp = QLineEdit(self)
        self.idp.resize(150, 40)
        self.idp.move(390, 60)
        # здесь название должности
        self.lbl = QLabel("Должность:", self)
        self.lbl.move(310, 120)
        self.pn = QLineEdit(self)
        self.pn.resize(150, 40)
        self.pn.move(390, 110)
        # кнопка добавить запись
        self.btn = QPushButton("Добавить", self)
        self.btn.resize(150, 40)
        self.btn.move(390, 160)
        self.btn.clicked.connect(self.ins)
        # кнопка редактировать
        self.btn = QPushButton("Редактировать", self)
        self.btn.resize(150, 40)
        self.btn.move(390, 210)
        self.btn.clicked.connect(self.upentry)
        # кнопка удалить запись
        self.btn = QPushButton("Удалить", self)
        self.btn.resize(150, 40)
        self.btn.move(390, 260)
        self.btn.clicked.connect(self.dels)
        # кнопка выход
        self.btn = QPushButton("Выход", self)
        self.btn.resize(150, 40)
        self.btn.move(390, 450)
        self.btn.clicked.connect(self.close_clicked)
        # кнопка Главное меню
        self.btn = QPushButton("Главное меню", self)
        self.btn.resize(150, 40)
        self.btn.move(390, 310)
        self.btn.clicked.connect(self.menu_clicked)

    # обновить таблицу и поля
    def upd(self):
        self.db.conn.commit()
        self.tb.updt()
        self.idp.setText("")
        self.pn.setText("")

    # добавить таблицу новую строку
    def ins(self):
        try:
            idp, pn = self.idp.text(), self.pn.text()
            self.db.cur.execute(
                "insert into post (postid,postname) values (?,?)", (idp, pn)
            )
            QMessageBox.about(self, " ", "Данные добавлены!")
        except:
            QMessageBox.about(self, "Ошибка!", "Данные не добавлены, попробуйте попытку")
            pass
        self.upd()

    # Редактировать строку
    def upentry(self):
        try:
            idp, pn = (
                self.idp.text(),
                self.pn.text(),
            )
            self.db.cur.execute(
                "update POST set POSTNAME=? where POSTID=?",
                (pn, idp),
            )
            self.db.conn.commit()
            self.tb.updt()
            self.idp.setText("")
            self.pn.setText("")
            QMessageBox.about(self, " ", "Данные изменены!")
        except:
            QMessageBox.about(self, "Ошибка!", "Данные не изменены, повторите попытку")


    # удалить из таблицы строку
    def dels(self):
        try:
            idp = int(self.idp.text())  # идентификатор строки
            self.db.cur.execute("delete from post where postid=?", (idp,))
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





# Класс таблица Должностей
class Post_tb(QTableWidget):
    def __init__(self, wg):
        self.wg = wg  # запомнить окно, в котором эта таблица показывается
        self.db = wg.db

        super().__init__(wg)
        self.setGeometry(10, 10, 280, 500)
        self.setColumnCount(2)
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
        self.setHorizontalHeaderLabels(["Номер", "Должность"])  # заголовки столбцов
        self.db.cur.execute("select * from post order by postname")
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
        self.wg.idp.setText(self.item(row, 0).text())
        self.wg.pn.setText(self.item(row, 1).text().strip())



