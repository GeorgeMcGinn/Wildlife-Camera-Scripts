# [Naturebytes Camera Software Enhancement](https://naturebytes.org/)

&nbsp;
# Table of Contents
1. [Preserving Existing Software/RPI OS](#Preserving)
2.  [Issues Faced With Existing Python Scripts](#ScriptIssues)
3.  [New Cam Software](#NewCamSoftware)
	* [wlCamera.py](#wlCamera)
	* [wlVideo.py](#wlVideo)
	* [wlMultiProcess.py](#wlMultiProcess)
4. [How to Install Software](#Install)
5. [Documents/Links](#Documentation)
6. [Links To Documentation](#Links)
&nbsp;
* * *
## Introduction
This is an unofficial repositiory for the Naturebytes Wildlife/Trail Camera. It presents new Python scripts based on my experiences with using the Naturebytes wildlife camera in the field.
&nbsp;

<a name="Preserving"></a>
# Preserving Existing Software/RPI OS

As soon as the new version of Debian Bullseye came out, it was apparent that two things affected the use of cameras in general. 

The first is that raspistill and raspivid no longer exists. They were removed from the new release of the Raspberry PI OS, named Bullseye, Release date: October 30th 2021, Kernel version: 5.10.

The second issue is that the Python module, PiCamera is no longer compatible with the new release of Bullseye. And as of Nov 25, 2021, there is no timetable on when changes to the Python PiCamera module will be updated and released to be compatible with the new Raspberry PI OS, or if the Raspberry PI will update their OS to make it compatible.

To use this script, you will need to either use the OS provided by Naturebytes (link below) or use the [Raspberry Pi OS (Legacy) with desktop](https://www.raspberrypi.com/software/operating-systems/#raspberry-pi-os-32-bit), provided by the Raspberry PI Foundation. (For more information on the Raspberry PI Legacy OS, you can check out: [“New” old functionality with Raspberry Pi OS (Legacy)](https://www.raspberrypi.com/news/new-old-functionality-with-raspberry-pi-os-legacy/))

You can still go to their website to download the OS you need from their [Naturebytes resource page.](https://naturebytes.org/2020/09/03/wildlife-cam-kit-resources/)
&nbsp;
<a name="ScriptIssues"></a>
# Issues Faced With Existing Python Scripts

The scripts that Naturebytes provides are great examples, but they do not work well in my experience. This has to do more with the hardware (camera and PIR sensor) than with the current script, which can be overcome.

In my field tests, I noticed the first time that I used it to capture birds at a feeder, the images captured caught nothing. No birds. No wildlife. 

The issues can be broken down into two main limitations of the hardware used:

The first, the camera needs to warn up, up to five seconds! And the second is false triggers from the PIR sensor. Or more exactly, the time a trigger is set and when the image is taken.

While you can also fine tune your PIR sensor via hardware, one other issue with the PIR is that it also needs time to turn itself to LOW before registering a new contact. I have included a document that shows how the PIR sensor works, how to tune it using hardware settings on the sensor itself.

When I shortened the time that raspistill needed to turn on and take an image, all my photos were blown out. I switched over to raspivid, and then I saw the image go from blown out to being perfectly exposed.

Even when I set the raspistill to first preview then take a photo, the camera needed to warm up before it could take good photos. And since wildlife does not stop and wait until your camera takes a photo, another method needed to be developed to overcome this.
&nbsp;
<a name="NewCamSoftware"></a>
# New Cam Software

The two Python scripts I provide take care of this warm-up period, and will fire the camera as soon as the PIR sensor is set to HIGH.

I accomplished this by switching over to the PiCamera module in Python. The script basically starts a preview on boot and keeps it on until you turn the camera off. This way, the camera warms up while the rest of the PI is finishing its boot. 

Since the image or video taken is based on the preview, the preview stays active. This allows the camera to immediately take a photo or start your video recording, and from the start when the exposure is correct.

While the technical documentation states that the PIR sensor needs 5 seconds to reset itself (From HIGH to LOW state), field testing it reveals that it needs only 2 seconds to reset itself in Python. By switching the jumper from no-repeat to repeat, you can speed up the time that the sensor stays active, and I have found that I can set the sleep value to 2 instead of 5 to settle the PIR sensor.

In fact, in the PiCamera Documentation by Dave Jones (Link below), all his examples use a 2-second reset or settling of the PIR Sensor from a HIGH to LOW state.

This repository will have additional scripts that will fine-tune the exposure based on the condition of the preview, but until then, these scripts will allow you to not only get the first images of a wildlife when it shows up, but the camera will continue to take images while the PIR sensor is still registering the animal (or human).

<a name="wlCamera"></a>
## <u>wlCamera.py</u>

This script uses PiCamera to detect PIR sensor activation and image capture. It is designed to take 5 images with a .05 second pause between each image when the PIR Sensor detects a source of infrared heat radiation based on the distance you set on the hardware itself. The steps executed by this script are:

1. Set up logging file to track the camera's progress and process from the time it is turned on. It will display the settings of the camera script, and then track whether or not the PIR sensor was activated, when photos were taken and the file names of each, whether it was sucessful, when the PIR sensor settles, and when it is ready to detect a new target. All entries are date/time stamped, with message numbers.
2. The script sets up the GPIO Pin location of the PIR sensor (based on the Naturebytes build, it is 27, not 13), the exposure and meter modes, auto white balance, image resolution, and save location for the images (default is: /home/pi/Pictures/).
3. Starts the Camera Preview and waits 5 seconds for the exposure settings to take effect. A log entry is recorded when the preview sucessfully starts.
4. The script then enters an infinite loop, where it waits for the PIR to detect infrared heat radiation motion. This is a wait-state, and the script holds until the PIR sensor detects infrared heat radiation.
5. As soon as detected, the script continues, where it sets the file name to the cuurent date and time of activation. Then the script takes 5 photos, each .05 seconds apart, and adds a sequence number (1-5) at the end of the datetime stamp. The default images taken is a .PNG file.
6. After the camera takes the 5th image, the scripts sleeps for 2 seconds to let the PIR Sensor settle. Then it loops back to where it waits for the PIR to detect infrared heat radiation motion. 

The camera continues on this loop until either: 1) An error is detected and the exception routine stops the camera; 2) The battery pack dies; or 3) You turn the camera off when you go to retrieve it.

Also of importance is that this script has been tuned to the jumper on the PIR Sensor is set into the HIGH Mode, which speeds up continuous detection of an infrared heat radiation source still present in the sensor's range.

<a name="wlVideo"></a>
## <u>wlVideo.py</u>

This script uses PiCamera to detect PIR sensor activation and video capture. It is designed to take 3 10-second videos with a .05 second pause between each recording when the PIR Sensor detects a source of infrared heat radiation based on the distance you set on the hardware itself. The steps executed by this script are (similar in design to wlCamera.py):

1. Set up logging file to track the camera's progress and process from the time it is turned on. It will display the settings of the camera script, and then track whether or not the PIR sensor was activated, when videos were taken and the file names of each, whether it was sucessful, when the PIR sensor settles, and when it is ready to detect a new target. All entries are date/time stamped, with message numbers.
2. The script sets up the GPIO Pin location of the PIR sensor (based on the Naturebytes build, it is 27, not 13), the exposure and meter modes, auto white balance, video resolution and framerate, and save location for the videos (default is: /home/pi/Videos/).
3. Starts the Camera Preview and waits 5 seconds for the exposure settings to take effect. A log entry is recorded when the preview sucessfully starts.
4. The script then enters an infinite loop, where it waits for the PIR to detect infrared heat radiation motion. This is a wait-state, and the script holds until the PIR sensor detects infrared heat radiation.
5. As soon as detected, the script continues, where it sets the file name to the cuurent date and time of activation. Then the script takes 3 10-second videos, each .05 seconds apart, and adds a sequence number (1-3) at the end of the datetime stamp. The default videos taken is a .h264 file.
6. After the camera takes the 5th image, the scripts sleeps for 2 seconds to let the PIR Sensor settle. Then it loops back to where it waits for the PIR to detect infrared heat radiation motion. 

The camera continues on this loop until either: 1) An error is detected and the exception routine stops the camera; 2) The battery pack dies; or 3) You turn the camera off when you go to retrieve it.

Also of importance is that this script has been tuned to the jumper on the PIR Sensor is set into the HIGH Mode, which speeds up continuous detection of an infrared heat radiation source still present in the sensor's range.

<a name="wlMultiProcess"></a>
## <u>wlMultiProcess.py</u>

This is an experimental script that allows your camera to take both still photos and videos at the same time when the PIR Sensor detects an infrared heat radiation source. This is accomplished by using the multi-processing rather than multi-threading.

While it is included here, it has not been thoroughly tested & debugged. Use it at your own risk. When it is ready, this mesage will change.
&nbsp;
<a name="Install"></a>
# How to Install Software

If you are using the Naturebytes system to run your Wildlife Cam, then there are two files that you need to copy from this repository:

`launch_nbcamera.sh` - The BASH script that launches the Python script at boot time
**wlCamera.py** - The Python script that is launched by the script above and runs the PIR sensor and camera.

After installing these scripts to their respective folders on your device, ensure that the wlCamera.py script points to the storage device that you wish to store your photos. By default, I have coded this script to put all photos taken into` /home/pi/Pictures/`.

If you want to take videos instead, replace wlCamera.py with wlVideo.py in `launch_nbcamera.sh`.

If you are installing a brand new Raspberry PI, you will need to download one of the Raspberry PI OS files that are Debian Buster or lower. One of the files linked below is an OS by Naturebytes, which already has the CRON task set up to execute the `launch_nbcamrea.sh` BASH script. There is a link below in Documents that will explain how to set up launch_nbcamera.sh on a boot of your PI.
&nbsp;
<a name="Documentation"></a>
 # Documents
 
 This distro has a directory called "Documents" that contain technical documentation on the cameras, sensors, and software manuals that are used in the Naturebytes wildlife cam.
 
 One document that is provided via the web is the [PiCamera Docmentation](https://picamera.readthedocs.io/en/release-1.13/).
 
 You can also download and install PiCamera from the source yourself. It is available on GitHub at: [Dave Jones - Waveform80/picamera](https://github.com/waveform80/picamera). Jones Software engineer at Canonical, developers of Ubuntu Linux.
 &nbsp;
 <a name="Links"></a>
 # Links To Documentation
 
 For those who do not wish to download the documents with the software, here are the links to all the documents provided:

- [Naturebytes Assembly Guide v4.4 (Current - Release 2021)](http://naturebytes.org/wp-content/uploads/2021/09/Manual-V4.4-reduced-size.pdf)
- [Naturebytes Assembly Guide v3 (Release: 2018)](http://naturebytes.org/wp-content/uploads/2020/08/Naturebytes-Assembly-Guide-v3-reduced.pdf)
- [Raspberry PI Camera Guide 2020 (Free Download)](https://magpi.raspberrypi.com/books/camera-guide)
- [Raspberry PI Official Camera Technical Documentation (Website)](https://www.raspberrypi.com/documentation/accessories/camera.html)
- [PiCamera - Technical Documentation (Website)](https://picamera.readthedocs.io/en/release-1.13/#)
- [PiCamera Technical Documentation (PDF)](https://buildmedia.readthedocs.org/media/pdf/picamera/release-1.13/picamera.pdf)
- [PIR Motion Sensor - Sunfounder](https://docs.sunfounder.com/projects/thales-kit/en/master/pir_motion_sensor.html)
- [PIR Sensor - Parallax](https://www1.parallax.com/sites/default/files/downloads/910-28027-PIR-Sensor-REV-A-Documentation-v1.4.pdf)
- [Adafruit PIR Sensor Documentation](https://cdn-learn.adafruit.com/downloads/pdf/pir-passive-infrared-proximity-motion-sensor.pdf)
- [Adding a Hardware/realtime clock to your Raspberry PI](https://thepihut.com/blogs/raspberry-pi-tutorials/17209332-adding-a-real-time-clock-to-your-raspberry-pi)
- [Setting Up a CRON on a Raspberry PI](https://raspberrytips.com/schedule-task-raspberry-pi/)
&nbsp;
&nbsp;
* * *
***Updated: 01/14/2022 18:18***
 
