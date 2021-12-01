#!/bin/sh
# launch_nbcamera.sh
# navigate to home directory, then to this directory, then execute python script, then back home
# on the Pi3 we can block wifi and bluetooth by default as they are known to interfere with the PIR when activated
sudo hwclock -s
cd /
cd home/pi/Naturebytes/Scripts/
python3 wlCamera.py
cd /
