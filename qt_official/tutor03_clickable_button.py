import sys
from PyQt5.QtWidgets import QApplication, QPushButton
from PyQt5.QtCore import pyqtSlot

@pyqtSlot()
def say_hello():  # to "say_hello()" slot
  print("Button clicked, Hello!")

app = QApplication(sys.argv)
button = QPushButton("Click me")
button.clicked.connect(say_hello)  # "clicked" signal
button.show()
app.exec_()
