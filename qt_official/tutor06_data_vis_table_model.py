from qt_mod import QT_MOD
if QT_MOD == 'PySide2':
  from PySide2.QtCore import QAbstractTableModel, QModelIndex, Qt
  from PySide2.QtGui import QColor
elif QT_MOD == 'PyQt5':
  from PyQt5.QtCore import QAbstractTableModel, QModelIndex, Qt
  from PyQt5.QtGui import QColor

class CustomTableModel(QAbstractTableModel):

  def __init__(self, data=None):
    QAbstractTableModel.__init__(self)
    self.LoadData(data)

  def LoadData(self, data):
    self.input_dates = data[0].values
    self.input_magnitudes = data[1].values
    self.column_count = 2
    self.row_count = len(self.input_magnitudes)

  def columnCount(self, parent=QModelIndex()):
    return self.column_count

  def rowCount(self, parent=QModelIndex()):
    return self.row_count

  def data(self, index, role=Qt.DisplayRole):
    column = index.column()
    row = index.row()

    if role == Qt.DisplayRole:
      if column == 0:
        raw_date = self.input_dates[row]
        # <QDateTime> to <str>
        date = raw_date.toString("yyyy-MM-dd HH:mm:ss.zzz")
        return date
      elif column == 1:
        return "{:.2f}".format(self.input_magnitudes[row])
    elif role == Qt.BackgroundRole:
      return QColor(Qt.white)
    elif role == Qt.TextAlignmentRole:
      return Qt.AlignRight
    return None

  def HeaderData(self, section, orientation, role):
    if role != Qt.DisplayRole:
      return None
    if orientation == Qt.Horizontal:
      return ("Date", "Magnitude")[section]
    else:
      return "{}".format(section)
