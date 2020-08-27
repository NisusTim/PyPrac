CC      	:= gcc
py_conf   := $(shell python3-config --cflags --ldflags) -lpython3.8
exe 			:= main
cy_src 		:= hello_world.pyx
tmp_dir   := build/temp.linux-x86_64-3.8
tmp_src   := $(cy_src:.pyx=.c)
tmp_obj 	:= $(addprefix $(tmp_dir)/, $(cy_src:.pyx=.o))

all: $(exe)
	./$(exe)

$(exe): main.c $(tmp_obj)
	$(CC) main.c $(tmp_obj) $(py_conf) -fPIC -o $(exe)

$(tmp_obj): $(cy_src)
	python3 setup.py build_ext -i

.PHONY: clean
clean:
	rm -rf build/ __pycache__/
	rm -f $(exe) $(tmp_src) $(cy_src:.pyx=.h) *.so $(cy_src:.pyx=.html)
