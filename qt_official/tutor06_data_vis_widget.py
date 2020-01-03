from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QAction, QApplication, QHBoxLayout, QHeaderView, \
  QMainWindow, QSizePolicy, QTableView, QWidget
from tutor06_data_vis_table_model import CustomTableModel

class Widget(QWidget):

  def __init__(self, data):
    QWidget.__init__(self)
    self.model = CustomTableModel(data)
    # QTableView
    self.table_view = QTableView()
    self.table_view.setModel(self.model)  # to present data of model
    ## QTableView Headers
    self.horizontal_header = self.table_view.horizontalHeader()
    self.vertical_header = self.table_view.verticalHeader()
    self.horizontal_header.setSectionResizeMode(QHeaderView.ResizeToContents)
    self.vertical_header.setSectionResizeMode(QHeaderView.ResizeToContents)
    self.horizontal_header.setStretchLastSection(True)
    # Layout
    self.main_layout = QHBoxLayout()
    size = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
    ## Left Layout
    size.setHorizontalStretch(True)
    self.table_view.setSizePolicy(size)
    self.main_layout.addWidget(self.table_view)

    self.setLayout(self.main_layout)
