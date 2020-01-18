from qt_mod import QT_MOD
if QT_MOD == 'PySide2':
  from PySide2.QtWidgets import QWidget, QHBoxLayout, QSizePolicy, \
    QHeaderView, QTableView
  from PySide2.QtGui import QPainter
  from PySide2.QtCore import QDateTime, Qt
  from PySide2.QtCharts import QtCharts
  QtChart = QtCharts
  QChart = QtCharts.QChart
elif QT_MOD == 'PyQt5':
  from PyQt5.QtWidgets import QWidget, QHBoxLayout, QSizePolicy, QHeaderView, \
    QTableView
  from PyQt5.QtGui import QPainter
  from PyQt5.QtCore import QDateTime, Qt
  from PyQt5 import QtChart
  from PyQt5.QtChart import QChart

from tutor06_data_vis_table_model import CustomTableModel

class Widget(QWidget):

  def __init__(self, data):
    QWidget.__init__(self)
    self.model = CustomTableModel(data)
    # QTableView
    self.table_view = QTableView()
    self.table_view.setModel(self.model)  # to present data of model
    ## QTableView Headers
    resize = QHeaderView.ResizeToContents
    self.horizontal_header = self.table_view.horizontalHeader()
    self.vertical_header = self.table_view.verticalHeader()
    self.horizontal_header.setSectionResizeMode(resize)
    self.vertical_header.setSectionResizeMode(resize)
    self.horizontal_header.setStretchLastSection(True)
    # QChart
    self.chart = QChart()
    self.chart.setAnimationOptions(QChart.AllAnimations)
    self.AddSeries("Magnitude (Column 1)", [0, 1])
    # QChartView
    self.chart_view = QtChart.QChartView(self.chart)
    self.chart_view.setRenderHint(QPainter.Antialiasing)
    # Layout
    self.main_layout = QHBoxLayout()
    size = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
    ## Left Layout
    size.setHorizontalStretch(1)  # ratio of left
    self.table_view.setSizePolicy(size)
    self.main_layout.addWidget(self.table_view)
    ## Right Layout
    size.setHorizontalStretch(4)  # ratio of right
    self.chart_view.setSizePolicy(size)
    self.main_layout.addWidget(self.chart_view)

    self.setLayout(self.main_layout)

  def AddSeries(self, name, columns):
    # QLineSeries
    self.series = QtChart.QLineSeries()
    self.series.setName(name)
    for i in range(self.model.rowCount()):
      t = self.model.index(i, 0).data()  # <str>
      date_fmt = "yyyy-MM-dd HH:mm:ss.zzz"
      # use toMSecsSinceEpoch() rather toSecsSinceEpoch()
      x = QDateTime().fromString(t, date_fmt).toMSecsSinceEpoch()  # <int>
      y = float(self.model.index(i, 1).data())  # <str> to <float>
      if x > 0 and y > 0:
        self.series.append(x, y)
    self.chart.addSeries(self.series)
    # X-axis
    self.axis_x = QtChart.QDateTimeAxis()
    self.axis_x.setTickCount(10)
    self.axis_x.setFormat("MM-dd HH:mm")
    self.axis_x.setTitleText("Date")
    self.chart.addAxis(self.axis_x, Qt.AlignBottom)
    self.series.attachAxis(self.axis_x)
    # Y-axis
    self.axis_y = QtChart.QValueAxis()
    self.axis_y.setTickCount(10)
    self.axis_y.setLabelFormat("%.2f")
    self.axis_y.setTitleText("Magnitude")
    self.chart.addAxis(self.axis_y, Qt.AlignLeft)
    self.series.attachAxis(self.axis_y)
