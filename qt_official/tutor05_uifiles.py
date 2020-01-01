# python3 -m PyQt5.uic.pyuic -x <src.ui> -o <dst.py>
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from tutor05_mainwindow import Ui_MainWindow

class MainWindow(QMainWindow):
  def __init__(self):
    super(MainWindow, self).__init__()
    self.ui = Ui_MainWindow()
    self.ui.setupUi(self)

if __name__ == '__main__':
  app = QApplication(sys.argv)
  window = MainWindow()
  window.show()
  sys.exit(app.exec_())
