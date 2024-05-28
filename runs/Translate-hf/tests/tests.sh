# Shell script for deploying the code-translation engine. This
# script executes job.target defined in Jobfile.

# Execute torchrun command and deploy job.target
python3 $JobWorkDir/job.target
