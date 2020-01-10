from PySide2.QtWidgets import QApplication
from tutor07_expenses_window import MainWindow
from tutor07_expenses_widget import Widget

DATA = {"Water": 24.5, "Electricity": 55.1, "Rent": 850.0,
        "Supermarket": 230.4, "Internet": 29.99, "Bars": 21.85,
        "Public transportation": 60.0, "Coffee": 22.45, "Restaurants": 120}

if __name__ == '__main__':
  app = QApplication([])
  widget = Widget(DATA, app.quit)
  window = MainWindow(widget, app.quit)
  window.show()
  app.exec_()
