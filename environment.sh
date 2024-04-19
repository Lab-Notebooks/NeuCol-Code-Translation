# Bash file to load modules and set environment
# variables for compilers and external libraries

# Set project home using realpath
# of current directory
export PROJECT_HOME=$(realpath .)

# Set SiteHome to realpath of SiteName
SiteHome="$PROJECT_HOME/sites/$SiteName"

# Load modules from the site directory
source $SiteHome/environment.sh

export CODELLAMA_HOME="$PROJECT_HOME/software/codellama/Llama"
export MODEL_HOME="$PROJECT_HOME/models"
export FLASHX_HOME="$PROJECT_HOME/software/flashx/Flash-X"

# Output information to stdout
echo "---------------------------------------------------------------------------------------"
echo "Execution Environment:"
echo "---------------------------------------------------------------------------------------"
echo "PROJECT_HOME=$PROJECT_HOME"
echo "SITE_HOME=$SiteHome"
echo "MPI_HOME=$MPI_HOME"
echo "NVHPC_HOME=$NVHPC_HOME"
echo "CODELLAMA_PATH=$CODELLAMA_HOME"
echo "MODEL_HOME=$MODEL_HOME"
echo "FLASHX_HOME=$FLASHX_HOME"
echo "---------------------------------------------------------------------------------------"
