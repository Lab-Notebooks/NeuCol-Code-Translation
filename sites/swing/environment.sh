module load anaconda3/2023-01-11
module load nvhpc/23.3

# Set MPI_HOME by quering path loaded by site module
export MPI_HOME=$(which mpicc | sed s/'\/bin\/mpicc'//)

# Set NVHPC_HOME by quering path
export NVHPC_HOME=$(which nvcc | sed s/'\/bin\/nvcc'//)

# Add path
export PATH="/home/adhruv/.local/swing/anaconda3/2023-01-11/bin:$PATH"
