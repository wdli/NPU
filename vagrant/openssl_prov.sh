#!/bin/sh
#
# This installs openssl 1.0.2 on this VM
#


echo "Fetching Openssl 1.0.2 tar ball..."
wget http://openssl.org/source/openssl-1.0.2.tar.gz

echo "Unpacking..."
[ ! -f openssl-1.0.2.tar.gz ] && { echo "No openssl tar file found!"; exit; }
tar xvf openssl-1.0.2.tar.gz

[ ! -d openssl-1.0.2 ] && { echo "No openssl-1.0.2 directory found!"; exit; }
cd openssl-1.0.2

echo "config..."
./config

echo "make..."
make

echo "install..."
sudo make install

echo "checking..."
[ ! -d /usr/local/ssl ] && { echo "Install might have failed!"; exit; }

echo "All Done!"

