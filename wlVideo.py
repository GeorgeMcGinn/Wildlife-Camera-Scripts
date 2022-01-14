#! usr/bin/python3
#########################################################################################
#       Program: wlVideo.py
#    Written By: George McGinn                
#                <gjmcginn@icloud.com>
#  Date Created: 11/30/2021
#
#   Description: Wildlife Cam Kit script to shoot videos from a wildlife/trail cam, 
#                like the Naturebytes camera system. Script will work with any PI camera.
#                Uses the PiCamera Python module instead of raspistill for greater control
#                over the imaging process.
#
# Version 1.0 - Created 11/25/2021
#
# CHANGE LOG
#########################################################################################
# 11/30/2021 GJM - New Program.
#########################################################################################
#  Copyright (C) 2021 by George McGinn.  All Rights Reserved.
#########################################################################################
#

from gpiozero import MotionSensor
from picamera import PiCamera
from datetime import datetime
from time import sleep
import sys
import logging


# Logging all of the camera's activity to the "naturebytes_camera_log" file.
start_datetimestamp = datetime.now().strftime("%m/%d/%Y at %H:%M:%S")
logging.basicConfig(format="%(asctime)s %(message)s",filename="naturebytes_camera_log",level=logging.DEBUG)
logging.info("Naturebytes Wildlife Cam Kit started up successfully")
logging.info("Executing Program: wlVideo.py")
logging.info("Camera started at:  %(show_datetime_stamp)s", { "show_datetime_stamp": start_datetimestamp })
logging.info("----------------------------------------------------")

# Setup Sensor, Camera and Location to save Photos
camera = PiCamera()
sensor = MotionSensor(27)
save_location = "/home/pi/Videos/"
logging.info("Save Location: %s" % save_location)

# Set some of the camera settings
camera.exposure_mode = 'auto'
camera.meter_mode = 'average'
camera.awb_mode = 'auto'
camera.framerate = 30
camera.resolution = (1640, 1232)

# Display Camera Setting in Log File
logging.info("Exposure Mode: auto")
logging.info("   Meter Mode: average")
logging.info("     AWB Mode: auto")
logging.info("   Frame Rate: 30")
logging.info("   Resolution: 1640x1232")
logging.info("----------------------------------------------------")

# Start PREVIEW and wait 5 seconds. Preview to stay active through entire execution
# NOTE: While the PI camera takes about 2 seconds to warm up, we wait 5 to make sure
# all auto exposure settings are properly implemented.
logging.info("Starting Camera preview")
camera.start_preview()
sleep(5)
logging.info("Camera preview started up successfully")

# Loop until camera is turned off or batteries die
try:
	while True:
		# Wait for PIR to detect motion, then continue
		logging.info("Waiting for a PIR trigger to continue")
		sensor.wait_for_motion()
		logging.info("PIR trigger detected")

		# Set photo_name based on current date/time stamp & add save location
		filename = datetime.now().strftime("%H.%M.%S_%Y-%m-%d")

		# Capture a burst of 3 videos of 10 seconds each in intervals of .05 seconds to video_name (image taken from active preview)
		logging.info("About to take a series of videos and save them to the Videos directory")
		for i in range(3):
			video_name = save_location + filename + ("-%s.h264" % i+1)
			camera.start_recording(video_name)
			camera.wait_recording(10)
			camera.stop_recording()
			logging.info("Video shot successfully and saved as %(show_video_name)s", { "show_video_name": video_name })
			sleep(0.05)

		# Sleep for 2 seconds to let PIR Sensor settle before detecting a new target
		logging.info("Settling PIR Sensor")
		sleep(2)
		logging.info("PIR Sensor is settled")

except KeyboardInterrupt:
	logging.info("*** KeyboardInterrupt detected. Exiting program")
	sys.exit()

except:
	logging.info("*** ERROR: Error detected. Exiting program")
	sys.exit(2)
