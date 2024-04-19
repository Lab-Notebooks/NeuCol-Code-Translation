# Bash script for `jobrunner` to install

if [ ! -d "mcfminterface" ]; then
	git clone git@github.com:NeuCol/mcfminterface.git --branch main mcfminterface
fi
