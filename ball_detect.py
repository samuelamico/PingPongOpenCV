import numpy as np
import cv2
import time
import math
from visual import *
import visual as vs   # for 3D panel 

import wx   # for widgets

capture = cv2.VideoCapture(1)

def nothing(x):
	pass

####### TRACKBAR #########
#cv2.namedWindow('bar')
#cv2.createTrackbar('R','bar',0,255,nothing)
#cv2.createTrackbar('G','bar',0,255,nothing)
#cv2.createTrackbar('B','bar',0,255,nothing)
#cv2.createTrackbar('R1','bar',0,255,nothing)
#cv2.createTrackbar('G1','bar',0,255,nothing)
#cv2.createTrackbar('B1','bar',0,255,nothing)

def rescale_frame(capturing, wpercent=50, hpercent=50):
    width = int(capturing.shape[1] * wpercent / 100)
    height = int(capturing.shape[0] * hpercent / 100)
    return cv2.resize(capturing, (width, height), interpolation=cv2.INTER_AREA)

def roi_seg(img,hsv):
        #r = cv2.getTrackbarPos('R','bar')
        #g = cv2.getTrackbarPos('G','bar')
        #b = cv2.getTrackbarPos('B','bar')
        #r1 = cv2.getTrackbarPos('R1','bar')
        #g1 = cv2.getTrackbarPos('G1','bar')
        #b1 = cv2.getTrackbarPos('B1','bar')

        r = 247
        g = 145
        b =  99
        r1 = 255
        g1 = 255
        b1 = 131
                
        low_limit = np.array([b,g,r])     # color (99,145,247)
        upper_limit = np.array([b1,g1,r1]) # color (131,255,255)
        # filtro anti-ruido
        mask2 = cv2.inRange(hsv,low_limit,upper_limit)
        res = cv2.bitwise_and(img,img,mask=mask2)
        
        kernel = np.ones((20,20),np.uint8)                  # destruindo os ruidos
        res1 = cv2.morphologyEx(res,cv2.MORPH_OPEN,kernel)
        #cv2.imshow('Segmentando_cor',res1)
        return res1


def filtragem(frame):
	blurred = cv2.GaussianBlur(frame,(11,11),0)
	errosion = cv2.erode(blurred,(11,11),1)
	#cv2.imshow('filter',errosion)
	hsv = cv2.cvtColor(errosion,cv2.COLOR_BGR2HSV)
	roi = roi_seg(frame,hsv)
	return roi

def contorno(white_img,frame):
        ret1,thr = cv2.threshold(white_img, 127, 255, cv2.THRESH_BINARY)
        #cv2.imshow('thr',thr) use issoo aki <----------------
        canny = cv2.Canny(white_img, 50, 255)
        #cv2.imshow('canny',canny)
	# depois tente aplicar contorno no canny
	#ret1,thr = cv2.threshold(white_img, 127, 255, cv2.THRESH_BINARY)
        result = cv2.findContours(canny,cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
        cont,hierarchy = result if len(result) == 2 else result[1:3]
        #cv2.imshow('Canny',canny)
        if len(cont) > 0:
                areas = [cv2.contourArea(c) for c in cont]
                max_index = np.argmax(areas)
                cont_max = cont[max_index]
                M = cv2.moments(cont[max_index])
                area = cv2.contourArea(cont[max_index])
                if (M['m00'] != 0):
                        cx = int(M['m10']/M['m00'])
                        cy = int(M['m01']/M['m00'])
                        cv2.circle(frame,(cx,cy),8,(0,255,105),3)
                        return (cx,cy,area)
        return (0,0,0)


ball = sphere (color = color.green, radius = 0.4)
ball.mass = 1.0
ball.pos = (0,0,0)

ball_1 = sphere (color = color.blue, radius = 0.4)
dt = 0.5
t=0.0


def axes( frame, colour, sz, posn ): # Make axes visible (of world or frame).
                                     # Use None for world.   
    directions = [vs.vector(sz,0,0), vs.vector(0,sz,0), vs.vector(0,0,sz)]
    texts = ["X","Y","Z"]
    posn = vs.vector(posn)
    for i in range (3): # EACH DIRECTION
       vs.curve( frame = frame, color = colour, pos= [ posn, posn+directions[i]])
       vs.label( frame = frame,color = colour,  text = texts[i], pos = posn+ directions[i],
                                                                    opacity = 0, box = False )

axes( None, color.white, 3, (-11,6,0))


while True:
        rate(100)
        _,img = capture.read()
        pressed_key = cv2.waitKey(1) & 0xFF
        frame = rescale_frame(img)
        height,width = frame.shape[:2]
        roi = filtragem(frame)
        ### draw contorno e pegar o centroide:
        cv2.imshow('Segmentando_cor',roi)
        (x1,y1,area) = contorno(roi,frame)
        r = math.sqrt(area/math.pi)
        #cv2.imshow('frame',frame)

        # Convertendo para o Mundo virtual
        t = t + dt
        print(x1,y1)
        ball_1.pos = (x1/100,y1/100,0)
        ball_1.radius = r/100





        
        if pressed_key == ord("z"):
                break



cv2.destroyAllWindows()
capture.release()
