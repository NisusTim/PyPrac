import importlib

if importlib.util.find_spec('PySide2') is not None:
  QT_MOD = 'PySide2'
elif importlib.util.find_spec('PyQt5') is not None:
  QT_MOD = 'PyQt5'
