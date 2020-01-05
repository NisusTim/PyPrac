from PyQt5.QtWidgets import QMainWindow, QAction, qApp

class MainWindow(QMainWindow):

  def __init__(self, widget):
    QMainWindow.__init__(self)
    self.setWindowTitle("Earthquakes information")
    self.setCentralWidget(widget)
    # Menu
    self.menu = self.menuBar()
    self.file_menu = self.menu.addMenu("File")
    exit_action = QAction("Exit", self)
    exit_action.setShortcut("Ctrl+Q")
    exit_action.triggered.connect(self.close)
    self.file_menu.addAction(exit_action)
    # Status Bar
    self.status = self.statusBar()
    self.status.showMessage("Data loaded and plotted")
    # Window dimensions
    geometry = qApp.desktop().availableGeometry(self)
    self.setFixedSize(geometry.width() * 0.8, geometry.height() * 0.7)
