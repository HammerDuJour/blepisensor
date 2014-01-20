#!/bin/bash

if [ "$UID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

echo "Tested on kernel 3.10. You are using $(uname -r)."
read -p "Continue? [Yy] " -r
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    exit 1
fi

python -c 'import pexpect' &> /dev/null
if [ $? -eq 0 ]; then
  echo "pexpect module found"
else
  echo "Python module pexpect is required."
  read -p "Attempt to install pexepct? [Yy] " -r
  if [[ $REPLY =~ ^[Yy]$ ]]; then
    wget -nc http://pexpect.sourceforge.net/pexpect-2.3.tar.gz
    tar xzf pexpect-2.3.tar.gz
    cd pexpect-2.3
    python ./setup.py install
    cd ..
    #rm -rf pexpect-2.3
    #rm pexpect-2.3.tar.gz
  fi
fi

bluezver=$(dpkg-query -W bluez | awk '/bluez/ {print $NF;}')
echo "We require the Linux Bluetooth protocol stack, bluez."
echo "Tested with bluez version 5.12. You have $bluezver."
echo "Building / installing bluez takes a loooong time on the Pi."
read -p "Attempt to install / reinstall bluez 5.12? [Yy] " -r
if [[ $REPLY =~ ^[Yy]$ ]]; then
  wget -nc https://www.kernel.org/pub/linux/bluetooth/bluez-5.12.tar.xz
  tar xvf bluez-5.12.tar.xz
  apt-get install libusb-dev libdbus-1-dev libglib2.0-dev automake libudev-dev libical-dev libreadline-dev
  cd bluez-5.12
  ./configure --disable-systemd
  make
  make install
fi
