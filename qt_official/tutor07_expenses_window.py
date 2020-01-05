from PySide2.QtWidgets import QMainWindow, QAction
from PySide2.QtCore import Slot

class MainWindow(QMainWindow):

  def __init__(self, app, widget):
    QMainWindow.__init__(self)
    self.setWindowTitle("Expenses Tool")
    self.setCentralWidget(widget)
    self.app = app
    # Menu
    self.menu = self.menuBar()
    self.file_menu = self.menu.addMenu("File")
    exit_action = QAction("Exit", self)
    exit_action.setShortcut("Ctrl+Q")
    # exit_action.triggered.connect(self.close)
    exit_action.triggered.connect(self.Exit)
    self.file_menu.addAction(exit_action)
    # Window dimensions
    geometry = (800, 600)
    self.resize(*geometry)

  @Slot(bool)
  def Exit(self, checked):
    self.app.quit()
