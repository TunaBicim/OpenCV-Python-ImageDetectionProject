from picamera.array import PiRGBArray
from picamera import PiCamera
import serial
import cv2
import time
from Blue_Ball_Detection_Contour import Blue_Ball_Detection
from Red_Ball_Detection_Contour import Red_Ball_Detection
from Basket_Detection_Contour import Basket_Detection
from Boundary_Check import Boundary_Check

ser = serial.Serial('/dev/ttyUSB0',9600)

camera = PiCamera()
camera.awb_mode = 'fluorescent' # Options: auto,fluorescent,flash
camera.resolution = (544, 544)
camera.hflip = True
camera.vflip = True
rawCapture = PiRGBArray(camera, size=(544, 544))

# Allow the camera to warm up
time.sleep(0.1)

while True:
    state = ser.readline()
    rawCapture.truncate(0)
    state = state.decode('utf-8')
	# Depending on the received message find the needed feature
    if (state == "findball_1_b\n"): 
        camera.capture(rawCapture, format="bgr")
        image = rawCapture.array
        image = Boundary_Check(image)
        operation = Blue_Ball_Detection(image)
        operation = 'm1_'+ operation
        operation = operation.encode('utf-8')
        ser.write(operation)
        
    elif (state == "findball_2_b\n"):
        camera.capture(rawCapture, format="bgr")
        image = rawCapture.array
        image = Boundary_Check(image)
        operation = Blue_Ball_Detection(image)
        operation = 'm2_'+ operation
        operation = operation.encode('utf-8')
        ser.write(operation)
        
    elif (state == "findball_1_r\n"):
        camera.capture(rawCapture, format="bgr")
        image = rawCapture.array
        image = Boundary_Check(image)
        operation = Red_Ball_Detection(image)
        operation = 'm1_'+ operation
        operation = operation.encode('utf-8')
        ser.write(operation)
        
    elif (state == "findball_2_r\n"):
        camera.capture(rawCapture, format="bgr")
        image = rawCapture.array
        image = Boundary_Check(image)
        operation = Red_Ball_Detection(image)
        operation = 'm2_'+ operation
        operation = operation.encode('utf-8')
        ser.write(operation)
        
    elif (state=="findbasket_1\n"):
        camera.capture(rawCapture, format="bgr")
        image = rawCapture.array
        operation = Basket_Detection(image)
        operation = 'm1_'+ operation
        operation = operation.encode('utf-8')
        
        ser.write(operation)
    elif (state=="findbasket_2\n"):
        camera.capture(rawCapture, format="bgr")
        image = rawCapture.array
        operation = Basket_Detection(image)
        operation = 'm2_'+ operation
        operation = operation.encode('utf-8')
        ser.write(operation)
        
    else:
        print("Error")