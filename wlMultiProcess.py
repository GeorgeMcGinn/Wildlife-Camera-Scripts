from multiprocessing import Process
from picamera import PiCamera
from datetime import datetime
from time import sleep
import sys
import logging
    
    
def take_photos():
	# Capture a burst of 10 images in intervals of .05 seconds to photo_name (image taken from active preview)
	logging.info("About to take a series of photos and save them to the Pictures directory")
	for i in range(10):
		photo_name = save_location + filename + ("-%s.png" % i+1)
		camera.capture(photo_name, format=png)
		logging.info("Photo taken successfully and saved as %(show_photo_name)s", { "show_photo_name": photo_name })
		sleep(0.05)
	logging.info("*** take_photos process ended.")

def take_videos():
	# Capture a burst of 3 videos of 5 seconds each in intervals of .05 seconds to video_name (image taken from active preview)
	logging.info("About to take a series of videos and save them to the Videos directory")
	for i in range(3):
		video_name = save_location + filename + ("-%s.h264" % i+1)
		video.start_recording(video_name)
		video.wait_recording(5)
		video.stop_recording()
		logging.info("Video shot successfully and saved as %(show_video_name)s", { "show_video_name": video_name })
		sleep(0.05)
	logging.info("*** take_videos process ended.")

if __name__ == "__main__":
	# Logging all of the camera's activity to the "naturebytes_camera_log" file.
	start_datetimestamp = datetime.now().strftime("%m/%d/%Y at %H:%M:%S")
	logging.basicConfig(format="%(asctime)s %(message)s",filename="naturebytes_camera_log",level=logging.DEBUG)
	logging.info("Naturebytes Wildlife Cam Kit started up successfully")
	logging.info("Executing Program: wlcamera.py")
	logging.info("Camera started at:  %(show_datetime_stamp)s", { "show_datetime_stamp": start_datetimestamp })
	logging.info("----------------------------------------------------")

	# Setup Sensor, Camera and Location to save Photos
	camera = PiCamera()
	video = PiCamera()
	sensor = MotionSensor(27)

	# Setup Save Locations for Photos and Videos
	save_photo = "/home/pi/Pictures/"
	logging.info(" Save Photo Location: %s" % save_photo)
	save_video = "/home/pi/Videos/"
	logging.info(" Save Video Location: %s" % save_video)

	# Set and Display Camera settings
	camera.exposure_mode = 'auto'
	camera.meter_mode = 'average'
	camera.awb_mode = 'auto'
	camera.resolution = (3280, 2464)
	logging.info("Camera Settings")
	logging.info("Camera Exposure Mode: auto")
	logging.info("   Camera Meter Mode: average")
	logging.info("     Camera AWB Mode: auto")
	logging.info("   Camera Resolution: 3280 x 2464")
	logging.info("----------------------------------------------------")

	# Set and Display Video settings
	video.exposure_mode = 'auto'
	video.meter_mode = 'average'
	video.awb_mode = 'auto'
	video.framerate = 30
	video.resolution = (1640, 1232)
	logging.info("Video Settings")
	logging.info(" Video Exposure Mode: auto")
	logging.info("    Video Meter Mode: average")
	logging.info("      Video AWB Mode: auto")
	logging.info("    Video Frame Rate: 30")
	logging.info("    Video Resolution: 1640x1232")
	logging.info("----------------------------------------------------")

	sleep(2)

	# Loop until camera is turned off or batteries die
	try:
		while True:
			# Wait for PIR to detect motion, then continue
			logging.info("Waiting for a PIR trigger to continue")
			sensor.wait_for_motion()
			logging.info("PIR trigger detected")

			# Set photo_name based on current date/time stamp & add save location
			filename = datetime.now().strftime("%H.%M.%S_%Y-%m-%d")
			#photo_name = save_location + filename

			# Set up the List of Processes in jobs and start them
			jobs = []
			p = multiprocessing.Process(target=take_photos)
			jobs.append(p)
			p.start()
			p = multiprocessing.Process(target=take_videos)
			jobs.append(p)
			p.start()

			# Iterate through the list of jobs and remove one that are finished, checking every second.
			while len(jobs) > 0:
				jobs = [job for job in jobs if job.is_alive()]
				sleep(.1)

			##Process(target=take_photos).start()
			##Process(target=take_videos).start()

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
