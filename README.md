# RPiNDVI
Raspberry PI NDVI Code

This is some simple example code using OpenCV on a Raspberry Pi with the Raspbery Pi NoIR camera to display live NDVI images.

## Requirements:
* `picamera` (see https://picamera.readthedocs.org/en/release-1.10/#)
* OpenCV 2
* [Raspberry Pi NoIR camera](https://www.raspberrypi.org/products/pi-noir-camera/)

## Usage:
Simply run the `ndvi.py` script. This will display a window with four panes, showing the individual bands of the image plus
a calculated NDVI image. This _should_ all run in real-time (or near-real-time), depending on the speed of your Pi.

Press `ESC` to exit, or `s` to save a copy of the input image from the camera.
