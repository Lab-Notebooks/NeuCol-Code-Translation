# Bash script for `jobrunner` to install

if [ ! -d "pepper" ]; then
        git clone https://gitlab.com/spice-mc/pepper.git --branch 43-add-kokkos-mcfm-interface pepper
fi
