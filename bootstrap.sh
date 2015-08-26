#!/bin/bash

echo "Started bootstrap."

# Installs the ViennaRNA tools suite. Includes RNA structure prediction and 
# ability to plot images of predicted structures, among other things.
apt-add-repository -y ppa:j-4/vienna-rna
apt-get -y update
apt-get -y install vienna-rna

# Installs the RNAstructure package.
# Alternatively, a GUI version can be downloaded here:
# http://rna.urmc.rochester.edu/RNAstructureDownload.html

# Help for the RNAstructure commands
# http://rna.urmc.rochester.edu/Text/index.html

cd /home/vagrant
wget http://rna.urmc.rochester.edu/RNAstructureLinuxTextInterfaces64bit.tgz
tar xvzf RNAstructureLinuxTextInterfaces64bit.tgz
rm RNAstructureLinuxTextInterfaces64bit.tgz

ln -s /vagrant/data /home/vagrant/data
ln -s /vagrant/utils /home/vagrant/utils

echo "Finished bootstrap."
