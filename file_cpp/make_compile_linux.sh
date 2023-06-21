#! /usr/bin/bash
cd $PWD

echo Clearing up old executables and object code.....

echo Compiling library code.....
g++ -c -o modules.o modules.cpp -libstdc++fs -std=c++20
ar rcs libmodules.a modules.o
echo Setting up.....
mkdir static
mv libmodules.a static
echo Compiling and running program.....
g++ -o runner_cpp runner_cpp.cpp -O3 -I./ -L./static/ -lmodules
./runner_cpp