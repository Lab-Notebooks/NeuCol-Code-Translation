# Shell script for deploying the code-translation engine. This
# script executes job.target defined in Jobfile.

# Set environment variable for local python module path. This will
# be inserted into sys path in python files
export LOCAL_PYMODULE_PATH="$PWD:$LOCAL_PYMODULE_PATH"

# Execute torchrun command and deploy job.target
python3 $JobWorkDir/job.target
