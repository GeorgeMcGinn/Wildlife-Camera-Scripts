# [Naturebytes Camera Software Enhancement](https://naturebytes.org/)

This is an unofficial repositiory from the Naturebytes website. It both preserves the current state of source and Raspberry PI operating systems, as well as presents new Python scripts based on my experiences with using the Naturebytes game/trail camera in the field.

## Preserving Existing Software/RPI OS

As soon as the new version of Debian Bullseye came out, it was apparent that two things affected the use of cameras in general. 

The first is that raspistill and raspivid no longer exists. They were removed from the new release of the Raspberry PI OS, named Bullseye, Release date: October 30th 2021, Kernel version: 5.10.

The second issue is that the Python module, PiCamera is no longer compatible with the new release of Bullseye. And as of Nov 25, 2021, there is no timetable on when changes to the Python PiCamera module will be updated and released to be compatible with the new Raspberry PI OS, or if the Raspberry PI will update their OS to make it compatible.

So in this repository, I have provided the last release of Debian Buster that does support raspistill/raspivid and PiCamera, along with several of Naturebytes' own OS.

You can still go to their website to download the OS you need from their [Naturebytes resource page.](https://naturebytes.org/2020/09/03/wildlife-cam-kit-resources/)

## Issues Faced With Existing Python Scripts

The scripts that Naturebytes provides are great examples, but they do not work well in my experience. This has to do more with the hardware (camera and PIR sensor) than with the current script, which can be overcome.

In my field tests, I noticed the first time that I used it to capture birds at a feeder, the images captured caught nothing. No birds. No wildlife. 

The issues can be broken down into two main limitations of the hardware used:

The first, the camera needs to warn up, up to five seconds! And the second is false triggers from the PIR sensor. Or more exactly, the time a trigger is set and when the image is taken.

While you can also fine tune your PIR sensor via hardware, one other issue with the PIR is that it also needs time to turn itself to LOW before registering a new contact. I have included a document that shows how the PIR sensor works, how to tune it using hardware settings on the sensor itself.

When I shortened the time that raspistill needed to turn on and take an image, all my photos were blown out. I switched over to raspivid, and then I saw the image go from blown out to being perfectly exposed.

Even when I set the raspistill to first preview then take a photo, the camera needed to warm up before it could take good photos. And since wildlife does not stop and wait until your camera takes a photo, another method needed to be developed to overcome this.


## New Cam Software

The two Python scripts I provide take care of this warm-up period, and will fire the camera as soon as the PIR sensor is set to HIGH.

I accomplished this by switching over to the PiCamera module in Python. The script basically starts a preview on boot and keeps it on until you turn the camera off. This way, the camera warms up while the rest of the PI is finishing its boot. 

Since the image or video taken is based on the preview, the preview stays active. This allows the camera to immediately take a photo or start your video recording, and from the start when the exposure is correct.

While the technical documentation states that the PIR sensor needs 5 seconds to reset itself (From HIGH to LOW state), field testing it reveals that it needs only 2 seconds to reset itself in Python. By switching the jumper from no-repeat to repeat, you can speed up the time that the sensor stays active, and I have found that I can set the sleep value to 2 instead of 5 to settle the PIR sensor.

In fact, in the PiCamera Documentation by Dave Jones (Link below), all his examples use a 2-second reset or settling of the PIR Sensor from a HIGH to LOW state.

This repository will have additional scripts that will fine-tune the exposure based on the condition of the preview, but until then, these scripts will allow you to not only get the first images of a wildlife when it shows up, but the camera will continue to take images while the PIR sensor is still registering the animal (or human).


## How to Install Software

If you are using the Naturebytes system to run your Wildlife Cam, then there are two files that you need to copy from this repository:

**launch_nbcamera.sh** - The BASH script that launches the Python script at boot time
**wlCamera.py** - The Python script that is launched by the script above and runs the PIR sensor and camera.

After installing these scripts to their respective folders on your device, ensure that the wlCamera.py script points to the storage device that you wish to store your photos. By default, I have coded this script to put all photos taken into ***/home/pi/Pictures/***.

If you are installing a brand new Raspberry PI, you will need to download one of the Raspberry PI OS files that are Debian Buster or lower. One of the files linked below is an OS by Naturebytes, which already has the CRON task set up to execute the launch_nbcamrea.sh BASH script.


 ## Documents
 
 This distro has a directory called "Documents" that contain technical documentation on the cameras, sensors, and software manuals that are used in the Naturebytes wildlife cam.
 
 One document that is provided via the web is the [PiCamera Docmentation](https://picamera.readthedocs.io/en/release-1.13/)
 
 You can also download and install PiCamera from the source yourself. It is available on GitHub at: [Dave Jones - Waveform80/picamera](https://github.com/waveform80/picamera). Jones Software engineer at Canonical, developers of Ubuntu Linux.
 
 
 ## Links To Documentation
 
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
