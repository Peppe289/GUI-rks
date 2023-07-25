##
## Compile multi object
##

FLAGS = -fPIC -Wall -Wextra

build: gpu directory meminfo cpu cpuid link

##
## C file
##

gpu:
	gcc gpu.c -c $(FLAGS)

directory:
	gcc directory.c -c $(FLAGS)

meminfo:
	gcc meminfo.c -c $(FLAGS)

cpu:
	gcc cpu.c -c $(FLAGS)

##
## C++ file
##
cpuid:
	g++ cpuid.cpp -c $(FLAGS)

##
## Link object
##
link:
	g++ *.o -shared -o libRKM.so $(FLAGS)

clean:
	rm -rf *.o *.so