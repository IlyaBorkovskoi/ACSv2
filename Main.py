import sys
from PyQt5.QtWidgets import QApplication


from Forms.main_window import MainWindow


# Запуск программы
apppost = QApplication(sys.argv)
ex = MainWindow()
ex.show()
sys.exit(apppost.exec_())
