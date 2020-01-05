# python3 tutor06_data_vis.py -f <*.csv>
import sys
import argparse  # accept and parse input from CLI
import pandas as pd
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QDateTime, QTimeZone
from tutor06_data_vis_window import MainWindow
from tutor06_data_vis_widget import Widget

def transform_date(utc, timezone=None):
  utc_fmt = "yyyy-MM-ddTHH:mm:ss.zzzZ"
  new_date = QDateTime().fromString(utc, utc_fmt)
  if timezone:
    new_date.setTimeZone(timezone)
  return new_date

def read_data(fname):
  df = pd.read_csv(fname)
  df = df.drop(df[df['mag'] < 0].index)  # remove wrong magnitudes
  magnitudes = df['mag']
  timezone = QTimeZone(b"Europe/Berlin")
  times = df['time'].apply(lambda x: transform_date(x, timezone))
  return times, magnitudes

if __name__ == '__main__':
  options = argparse.ArgumentParser()
  options.add_argument("-f", "--file", type=str, required=True)
  args = options.parse_args()
  data = read_data(args.file)

  app = QApplication(sys.argv)
  widget = Widget(data)
  window = MainWindow(widget)
  window.show()
  sys.exit(app.exec_())
