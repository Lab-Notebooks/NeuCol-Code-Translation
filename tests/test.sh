cd $MCFM_HOME/Bin

# Compile and install
make clean || true
cmake -DCMAKE_Fortran_COMPILER=gfortran -DCMAKE_C_COMPILER=gcc -DCMAKE_CXX_COMPILER=g++  ..
make install

./test -b u d~ ve e+ # Directories: W (converted)
./test -b u d~ ve e+ g # Directories: W1jet
./test -b u d~ ve e+ g g # Directories: W2jet, BDK, loop
./test -b u u~ e- e+ # Directories: Z (converted)
./test -b u u~ e- e+ g # Directories: Z1jet, loop
./test -b u u~ e- e+ g g # Directories: Z2jet, W2jet, BDK, loop
./test -b -Pmodel=heft g g h # Directories: ggH (converted)
./test -b g g h # Directories: ggH (converted)
./test -b g g g g g # Directories: ThreeJets
./test -b g g h g g # Directories: gghgg_dep
