#! usr/bin/python3
#########################################################################################
#       Program: wlcamera.py
#    Written By: George McGinn                
#                <gjmcginn@icloud.com>
#  Date Created: 11/25/2021
#
#   Description: Wildlife Cam Kit script to shoot still images from a wildlife/trail cam, 
#                like the Naturebytes camera system. Script will work with any PI camera.
#                Uses the PiCamera Python module instead of raspistill for greater control
#                over the imaging process.
#
# Version 1.0 - Created 11/25/2021
#
# CHANGE LOG
#########################################################################################
# 11/25/2021 GJM - New Program.
# 11/28/2021 GJM - Fixed syntax error with camera.resolution and added PIN 13 to Motion 
#                  Sensor detection. Also, due to the great power drain on the 256GB USB
#                  device, all images will go into Pictures.
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
logging.basicConfig(format="%(asctime)s %(message)s",filename="naturebytes_camera_log",level=logging.DEBUG)
logging.info("Naturebytes Wildlife Cam Kit started up successfully")
logging.info("Executing Program: wlcamera.py")
logging.info("----------------------------------------------------")

# Setup Sensor, Camera and Location to save Photos
camera = PiCamera()
sensor = MotionSensor(27)
save_location = "/home/pi/Pictures/"
logging.info("Save Location: /home/pi/Pictures/")

# Set some of the camera settings
camera.exposure_mode = 'auto'
camera.meter_mode = 'average'
camera.awb_mode = 'auto'
#camera.resolution = (3280, 2464)
camera.resolution = (2592, 1944)
logging.info("Exposure Mode: auto")
logging.info("Meter Mode: average")
logging.info("AWB Mode: auto")
logging.info("Resolution: 2592, 1944")
logging.info("----------------------------------------------------")


# Start PREVIEW and wait 5 seconds. Preview to stay active through entire execution
# NOTE: While the PI camera takes about 2 seconds to warm up, we wait 5 to make sure
# all auto exposure settings are properly implemented.
logging.info("Starting Camera preview")
camera.start_preview()
sleep(5)
logging.info("Camera preview started up successfully")
print("Camera Preview Started")

# Loop until camera is turned off or batteries die
try:
	while True:
		# Wait for PIR to detect motion, then continue
		logging.info("Waiting for a PIR trigger to continue")
		print("Waiting for PIR Trigger")
		sensor.wait_for_motion()
		logging.info("PIR trigger detected")
		print("PIR was triggered")

		# Set photo_name based on current date/time stamp & add save location
		filename = datetime.now().strftime("%H.%M.%S_%Y-%m-%d.jpg")
		photo_name = save_location + filename

		# Capture image to photo_name (image taken from active preview)
		logging.info("About to take a photo and save to the Pictures directory")
		print("Taking Photo")	
		camera.capture(photo_name)
		logging.info("Photo taken successfully and saved as %(show_photo_name)s", { "show_photo_name": photo_name })
		print("Photo taken")

		# Sleep for 2 seconds to let PIR Sensor settle before detecting a new target
		logging.info("Settling PIR Sensor")
		print("Settling PIR")
		sleep(2)
		logging.info("PIR Sensor is settled")
		print("PIR Settled")

except KeyboardInterrupt:
	logging.info("*** KeyboardInterrupt detected. Exiting program")
	sys.exit()

except:
	logging.info("*** ERROR: Error detected. Exiting program")
	sys.exit(2)


'''
camera.capture_sequence(['image%02d.jpg' % i for i in range(10)])


for i in range(5):
    sleep(5)
    camera.capture('/home/pi/Desktop/image%s.jpg' % i)

'''
