from PySide2.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, \
  QTableWidget, QPushButton, QLineEdit, QTableWidgetItem, QHeaderView, QLabel
from PySide2.QtCore import Slot, Qt
from PySide2.QtCharts import QtCharts
from PySide2.QtGui import QPainter

class Widget(QWidget):

  def __init__(self, data, app_quit):
    QWidget.__init__(self)
    self.kAppQuit = app_quit
    self.items = 0
    self.is_plotted = False
    # UI
    ## Left: QTableWidget
    self.table = QTableWidget()
    self.table.setColumnCount(2)
    self.table.setHorizontalHeaderLabels(["Description", "Price"])
    self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    ## Right: QChartView, QLineEdit, QPushButton
    self.chart_view = QtCharts.QChartView()
    self.chart_view.setRenderHint(QPainter.Antialiasing)
    self.desc_line = QLineEdit()
    self.price_line = QLineEdit()
    self.add_btn = QPushButton("Add")
    self.clear_btn = QPushButton("Clear")
    self.quit_btn = QPushButton("Quit")
    self.plot_btn = QPushButton("Plot")
    self.add_btn.setEnabled(False)  # disable add_btn by default
    # Signals and Slots
    self.quit_btn.clicked.connect(self.QuitApplication)
    self.add_btn.clicked.connect(self.AddElement)
    self.plot_btn.clicked.connect(self.PlotData)
    self.clear_btn.clicked.connect(self.ClearTable)
    ## Input Validation
    self.desc_line.textChanged[str].connect(self.CheckDisable)
    self.price_line.textChanged[str].connect(self.CheckDisable)
    # Layout
    ## Right
    self.r_layout = QVBoxLayout()
    self.r_layout.setMargin(10)
    self.r_layout.addWidget(self.chart_view)
    self.r_layout.addWidget(QLabel("Description"))
    self.r_layout.addWidget(self.desc_line)
    self.r_layout.addWidget(QLabel("Price"))
    self.r_layout.addWidget(self.price_line)
    self.r_layout.addWidget(self.add_btn)
    self.r_layout.addWidget(self.plot_btn)
    self.r_layout.addWidget(self.clear_btn)
    self.r_layout.addWidget(self.quit_btn)
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
      desc_item = QTableWidgetItem(desc)
      price_item = QTableWidgetItem("{:.2f}".format(price))
      price_item.setTextAlignment(Qt.AlignRight)
      self.table.insertRow(self.items)
      self.table.setItem(self.items, 0, desc_item)
      self.table.setItem(self.items, 1, price_item)
      self.items += 1

  @Slot()
  def QuitApplication(self):
    self.kAppQuit()

  @Slot()
  def CheckDisable(self, s):
    if self.desc_line.text() and self.price_line.text().isdigit():
      self.add_btn.setEnabled(True)
    else:
      self.add_btn.setEnabled(False)

  @Slot()
  def AddElement(self):
    desc = self.desc_line.text()
    price = self.price_line.text()
    self.desc_line.setText("")
    self.price_line.setText("")
    new_data = {desc: float(price)}
    self.FillTable(new_data)
    if self.is_plotted:
      self.PlotData()

  @Slot()
  def ClearTable(self):
    self.table.setRowCount(0)  # clear the content of QTableWidget
    self.items = 0

  @Slot()
  def PlotData(self):
    # Get data from QTableWidget, save to QPieSeries and plot QChart
    series = QtCharts.QPieSeries()
    for i in range(self.table.rowCount()):
      text = self.table.item(i, 0).text()
      number = float(self.table.item(i, 1).text())
      series.append(text, number)

    chart = QtCharts.QChart()
    chart.addSeries(series)
    chart.legend().setAlignment(Qt.AlignLeft)
    self.chart_view.setChart(chart)
    self.is_plotted = True
