import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

from Forms.main_window import MainWindow

# Запуск программы
app = QApplication(sys.argv)
app.setWindowIcon(QIcon('mw.png'))
ex = MainWindow()
ex.show()
sys.exit(app.exec_())
