from PySide2.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, \
  QTableWidget, QTableWidgetItem, QHeaderView, QLineEdit, QPushButton, QLabel

class Widget(QWidget):

  def __init__(self, data):
    QWidget.__init__(self)
    self.items = 0
    # QTableWidget
    self.table = QTableWidget()
    self.table.setColumnCount(2)
    self.table.setHorizontalHeaderLabels(["Description", "Price"])
    self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    self.description = QLineEdit()
    self.price = QLineEdit()
    self.add = QPushButton("Add")
    self.clear = QPushButton("Clear")
    self.quit = QPushButton("Quit")
    self.plot = QPushButton("Plot")
    self.add.setEnabled(False)
    # Layout
    ## Right
    self.r_layout = QVBoxLayout()
    self.r_layout.setMargin(10)
    self.r_layout.addWidget(QLabel("Description"))
    self.r_layout.addWidget(self.description)
    self.r_layout.addWidget(QLabel("Price"))
    self.r_layout.addWidget(self.price)
    self.r_layout.addWidget(self.add)
    self.r_layout.addWidget(self.plot)
    self.r_layout.addWidget(self.clear)
    self.r_layout.addWidget(self.quit)
    ## Left
    self.layout = QHBoxLayout()
    ## Whole
    self.layout.addWidget(self.table)
    self.layout.addLayout(self.r_layout)
    self.setLayout(self.layout)
    self.FillTable(data)

  def FillTable(self, data=None):
    data = self.data if not data else data
    for desc, price in data.items():
      self.table.insertRow(self.items)
      self.table.setItem(self.items, 0, QTableWidgetItem(desc))
      self.table.setItem(self.items, 1, QTableWidgetItem(str(price)))
      self.items += 1
