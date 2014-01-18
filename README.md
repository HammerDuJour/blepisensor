blepisensor
===========

Acquire, log, and publish sensor data over BLE with the Raspberry Pi

**Dependencies**

* bluez 5.4 or higher
* pexpect

Building bluez
--------------

This depends on having the correct build of bluez to get the right gatttool version. *You need a kernel version higher than 3.5.*

Instructions below taken from [ mike.saunby.net](http://mike.saunby.net/2013/04/raspberry-pi-and-ti-cc2541-sensortag.html)

*Check kernel version*

    uname -r

*get a recent bluez version from http://www.bluez.org/*

	wget https://www.kernel.org/pub/linux/bluetooth/bluez-5.4.tar.xz
*extract*

	tar xvf bluez-5.4.tar.xz

*get the necessary libs*

	apt-get install libusb-dev libdbus-1-dev libglib2.0-dev automake libudev-dev libical-dev libreadline-dev

*systemd is not needed, see later*

*configure and build SW:*

	cd bluez-5.4
	./configure --disable-systemd
	make
	make install

*Then I even had to copy gatttool manually into the /usr/local/bin dir*

	cp attrib/gatttool /usr/local/bin/

Installing pexpect
------------------

Download the package from sourceforge

    wget http://pexpect.sourceforge.net/pexpect-2.3.tar.gz

Extract and install the module

    tar xzf pexpect-2.3.tar.gz
    cd pexpect-2.3
    sudo python ./setup.py install
