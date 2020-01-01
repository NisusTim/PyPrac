# PyQt5 does not wrap the QUiLoader class but instead includes the uic module.
import sys
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication
from PySide2.QtCore import QFile

if __name__ == '__main__':
  app = QApplication(sys.argv)
  ui_file = QFile("tutor05_mainwindow.ui")
  ui_file.open(QFile.ReadOnly)
  loader = QUiLoader()
  window = loader.load(ui_file)
  ui_file.close
  window.show()
  sys.exit(app.exec_())
