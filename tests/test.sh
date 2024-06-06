cd $MCFM_HOME/Bin
make clean
cmake -DCMAKE_Fortran_COMPILER=gfortran -DCMAKE_C_COMPILER=gcc -DCMAKE_CXX_COMPILER=g++  ..
make install
./test -b u d~ ve e+
