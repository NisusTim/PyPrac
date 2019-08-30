import os  # os.getcwd()
from os import listdir  # listdir()
from os.path import isfile, join
import sys  # sys.platform

def get_cwd():
  cwd = os.getcwd()
  print(cwd)
  return cwd

def list_file_cwd(cwd):
  ls = listdir(cwd)
  print(ls)
  return ls

def list_file_path_cwd(cwd):
  ls_path = [join(cwd, f) for f in listdir(cwd) if isfile(join(cwd, f))]
  print(ls_path)
  return ls_path

def is_file(file_path):
  file_exist = isfile(file_path)
  print(file_exist)
  return file_exist

def os_name():
  os_name = os.name
  print(os_name)
  return os_name

def platform_name():
  platform = sys.platform
  print(platform)
  return platform

def platform_show():
  platform = platform_name()
  if platform.startswith('win'):
    print('Windows')
  elif platform.startswith('linux') or platform.startswith('cygwin'):
    print('Linux or Windows/Cygwin')
  elif platform.startswith('darwin'):
    print('Mac OS')
  else:
    raise EnvironmentError("Unsupported platform")

if __name__ == '__main__':
  '''
  cwd = get_cwd()
  ls = list_file_cwd(cwd)
  ls_path = list_file_path_cwd(cwd)
  f = '{0}/{1}'.format(cwd, ls[0])
  is_file(f)
  os_name()
  platform()
  '''
  platform_show()
