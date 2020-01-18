import sys
from PyQt5.QtWidgets import QApplication, QDialog, QLineEdit, QPushButton, \
  QVBoxLayout

class Form(QDialog):

  def __init__(self, parent=None):
    super(Form, self).__init__(parent)
    # self.setWindowTitle("My Form")
    self.edit = QLineEdit("Write my name here")
    self.button = QPushButton("Show Greetings")
    layout = QVBoxLayout()
    layout.addWidget(self.edit)
    layout.addWidget(self.button)
    self.setLayout(layout)
    self.button.clicked.connect(self.Greetings)

  def Greetings(self):
    print("Hello %s" % self.edit.text())

if __name__ == '__main__':
  app = QApplication(sys.argv)
  form = Form()
  form.show()
  sys.exit(app.exec_())
