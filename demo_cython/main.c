#include <stdio.h>
#include <Python.h>
#include "hello_world.h"

int main(void)
{
  PyImport_AppendInittab("hello_world", PyInit_hello_world);
  Py_Initialize();
  PyImport_ImportModule("hello_world");

  printf("  <main.c>: before invoking api\n");
  hello_world();
  printf("  <main.c>: after invoking api\n");

  Py_Finalize();
}
