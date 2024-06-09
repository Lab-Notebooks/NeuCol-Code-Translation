cd $MCFM_HOME/Bin

# Compile and install
#make clean || true
cmake -DCMAKE_Fortran_COMPILER=gfortran -DCMAKE_C_COMPILER=gcc -DCMAKE_CXX_COMPILER=g++  ..
make install

# ===> W- processes <===
# ===> W+ processes <===
./test -b u d~ ve e+
# Directories: W

# ===> W-j processes <===
# ===> W+j processes <===
./test -b u d~ ve e+ g
# Directories: W1jet

# ===> W-jj processes <===
# ===> W+jj processes <===
./test -b u d~ ve e+ g g
# Directories: W2jet, BDK, loop

# ===> Z processes <===
./test -b u u~ e- e+
# Directories: Z

# ===> Zj processes <===
./test -b u u~ e- e+ g
# Directories: Z1jet, loop

# ===> Zjj processes <===
./test -b u u~ e- e+ g g
# Directories: Z2jet, W2jet, BDK, loop

# ===> h (EFT) processes <===
./test -b -Pmodel=heft g g h
# Directories: ggH

# ===> h (SM) processes <===
./test -b g g h
# Directories: ggH

# ===> jjj processes <===
./test -b g g g g g
# Directories: ThreeJets

# ===> hjj (SM) processes <===
./test -b g g h g g 
# Directories: gghgg_dep
