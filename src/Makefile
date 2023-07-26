##
## Compile multi object
##

FLAGS_GCC = -fPIC -Wall -Wextra -O3
FLAGS_CPP = -fPIC -Wall -Wextra

build: clean-all gpu directory meminfo cpu cpuid link

##
## C file
##

gpu:
	gcc gpu.c -c $(FLAGS_GCC)

directory:
	gcc directory.c -c $(FLAGS_GCC)

meminfo:
	gcc meminfo.c -c $(FLAGS_GCC)

cpu:
	gcc cpu.c -c $(FLAGS_GCC)

##
## C++ file
##
cpuid:
	g++ cpuid.cpp -c $(FLAGS_CPP)

##
## Link object
##
link:
	g++ *.o -shared -o libRKM.so $(FLAGS_GCC)

clean:
	rm -rf *.o

clean-all:
	rm -rf *.o *.so