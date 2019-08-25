def Blue_Ball_Detection(image):
    # Import the necessary packages
    import time
    import cv2
    import imutils
    import numpy as np

    # User variables
    area_max = 200000
    area_min = 350
    apx_min = 15
    apx_max = 550
    threshold_value = 25
    arg_prev = 0
    s_left = 235
    s_right = 290
    s4_thresh = 180
    s3_thresh = 320
    s2_thresh = 490
    s1_thresh = 510
    # Define range of blue color in HSV
    lower_blue = np.array([75,35,35])  
    upper_blue = np.array([135,255,235])
    # Camera is mounted upside down, so flip the image
    # Convert BGR to HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    # Bitwise-AND mask and original image
    residual = cv2.bitwise_and(image,image, mask= mask)
    # Contour Detection
    # Convert the residual image to gray scale
    gray = cv2.cvtColor(residual, cv2.COLOR_BGR2GRAY)
    # Blur the image to eliminate high frequency noise 
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    # Threshold the image to map blue values to white
    threshold = cv2.threshold(gray, threshold_value, 255, cv2.THRESH_BINARY)[1]
    # Find the contours
    contours = cv2.findContours(threshold, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    # Use the first or second element depending on opencv version 
    contours = contours[0] if imutils.is_cv2() else contours[1]
    # Define parameters to track the closest ball to the reference point
    prev_distance = 600000
    closest_cX = 0
    closest_cY = 0
    # Loop over the contours
    for c in contours:
        approximate = cv2.approxPolyDP(c,0.0005*cv2.arcLength(c,True),True)
        area = cv2.contourArea(c)
        if (area>area_min)&(area < area_max)&(len(approximate)>apx_min)&(len(approximate)<apx_max):
            # Compute the center of the contour
            M = cv2.moments(c)
            # The if there to avoid dividing by 0 errors.
            if (M["m00"] == 0):
                M["m00"]=1
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            distance = (abs(cX - 254)**2) + (abs(544-cY)**2)
            # Update the values if the next contour is closer
            if (distance < prev_distance):#and(cY < 510) :
                prev_distance = distance
                closest_cX = cX
                closest_cY = cY
            
    if (closest_cX == 254):
       closest_cX = 255
	   
    Arct = np.arctan((544-closest_cY) / (closest_cX - 254)) / np.pi
    # Decide to turn or go straight
    if (closest_cX == 0):
        operation = "nbx"
    elif ((closest_cX > s_left) and (closest_cX < s_right)): 
        if (closest_cY < s4_thresh): 
            operation = "s4x"
        elif (closest_cY < s3_thresh):
            operation = "s3x"
        elif (closest_cY < s2_thresh):
            operation = "s2x"
        elif (closest_cY < s1_thresh):
            operation = "s1x"
        else:
            operation = "rcx"
    elif(Arct < 0):
        if (Arct > -1/8):
            operation = "l3x"
        elif (Arct > -3.2/8):
            operation = "l2x"
        else:
            operation = "l1x"
    else:
        if (Arct < 1/8):
            operation = "r3x"
        elif (Arct < 3.2/8):
            operation = "r2x"
        else:
            operation = "r1x"
    return operation