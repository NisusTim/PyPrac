from ctypes import *
lib = cdll.LoadLibrary("./libtest.so")
fun = lib.PrintHello
fun()
