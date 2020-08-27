from PySide2.QtWidgets import QMainWindow, QAction

class MainWindow(QMainWindow):

  def __init__(self):
    QMainWindow.__init__(self)
    # Menu
    self.menu = self.menuBar()
    self.file_menu = self.menu.addMenu("File")
    exit_act = QAction("Exit", self)
    exit_act.setShortcut("Ctrl+Q")
    exit_act.triggered.connect(self.close)
    self.file_menu.addAction(exit_act)

  def AddMenu()
