#!/bin/bash

#takes down your bt device and puts it back up again before running tag tracker
#not meant for production, but useful while testing.
sudo hciconfig hci0 down
sudo hciconfig hci0 up
./tagTracker.py 
