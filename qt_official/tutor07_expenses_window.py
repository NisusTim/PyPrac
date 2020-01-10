from PySide2.QtWidgets import QMainWindow, QAction
from PySide2.QtCore import Slot

class MainWindow(QMainWindow):

  def __init__(self, widget, app_quit):
    QMainWindow.__init__(self)
    self.kAppQuit = app_quit
    self.setCentralWidget(widget)
    self.setWindowTitle("Expenses Tool")
    # Menu
    self.menu = self.menuBar()
    self.file_menu = self.menu.addMenu("File")
    exit_action = QAction("Exit", self)
    exit_action.setShortcut("Ctrl+Q")
    # exit_action.triggered.connect(self.close)  # connect QMaindWindow.close()
    exit_action.triggered.connect(self.Exit)  # connect QApplication.quit()
    self.file_menu.addAction(exit_action)
    # Window dimensions
    geometry = (800, 600)
    self.resize(*geometry)

  @Slot()
  def Exit(self):
    self.kAppQuit()
