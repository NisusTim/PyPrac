import sys
from PyQt5.QtWidgets import QApplication, QLabel

app = QApplication(sys.argv)
# app = QApplication([])  # pass no arg
label = QLabel("hello, world")
# label = QLabel("<font color=red size=40>Hello World!</font>")  # HTML
label.show()
app.exec_()
