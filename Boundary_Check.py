# This function creates a hexagonal shape from the ends of the field 
# and masks the intended features out of it. Edge detection and 
# extreme point approximation techniques are used.
def Boundary_Check(image):
    import numpy as np
    import cv2
    import imutils
    lower = np.array([250,250,250]) 
    upper = np.array([255,255,255])
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    mask = image.copy()
    gray = cv2.GaussianBlur(gray, (5,5), 0)
    gray = cv2.bilateralFilter(gray,9,75,75)
    edged = cv2.Canny(gray, 30, 150)
    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_NONE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]
    extLeftPrev = (544,0)
    extRightPrev = (0,0)
    extTopPrev = (232,0)
    
    if (len(cnts) > 0):
        for c1 in cnts:
            approximate = cv2.approxPolyDP(c1,0.002*cv2.arcLength(c1,True),True)
            if (len(approximate)< 15):
                extLeft = tuple(c1[c1[:, :, 0].argmin()][0])
                extRight = tuple(c1[c1[:, :, 0].argmax()][0])
                                    
                if (extLeftPrev[0] > extLeft[0]):
                    extLeftPrev = extLeft
                if (extRightPrev[0] < extRight[0]):
                    extRightPrev = extRight
        for c2 in cnts:
            extLeft = tuple(c2[c2[:, :, 0].argmin()][0])
            extRight = tuple(c2[c2[:, :, 0].argmax()][0])

            if ((extLeft == extLeftPrev)and(extRight == extRightPrev)):
                extTop = tuple(c2[c2[:, :, 1].argmin()][0])   
                extTopPrev = extTop

    extLeftBottom = (extLeftPrev[0],544)
    extRightBottom = (extRightPrev[0],544)
    polygon = np.array([extLeftPrev,extLeftBottom,extRightBottom,extRightPrev,extTopPrev])
    polygon = polygon.reshape((-1,1,2))
    cv2.fillPoly(mask,[polygon],[255,255,255])
    mask = cv2.inRange(mask,lower,upper)
    residual = cv2.bitwise_and(image,image, mask= mask)
	
    return residual