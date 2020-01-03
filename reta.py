import numpy as np
import cv2 
import time
import math
from visual import *
import visual as vs   # for 3D panel 
import wx   # for widgets


capture = cv2.VideoCapture(0)



## Funcao Usando Limiarizacao por Otsu para detectar apenas a reta do jogo:
def Otsu_Lim(img):
    img1 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(img1,(5,5),0)
    ret,thr_otsu = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    #cv2.imshow('thershold',thr_otsu)
    return thr_otsu 
    
def coordenada(img,img1):
    canny = cv2.Canny(img, 50, 255)
    result = cv2.findContours(canny,cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    cont,hierarchy = result if len(result) == 2 else result[1:3]
    if len(cont) > 0:
        areas = [cv2.contourArea(c) for c in cont]
        max_index = np.argmax(areas)
        cont_max = cont[max_index]
        M = cv2.moments(cont[max_index])
        area = cv2.contourArea(cont[max_index])
        x,y,w,h = cv2.boundingRect(cont[max_index])
        cv2.rectangle(img1,(x,y),(x+w,y+h),(0,255,0),2)
        # Desenhar Reta
        rows,cols = img.shape[:2]

        [vx,vy,x,y] = cv2.fitLine(cont[max_index], cv2.DIST_L2,0,0.01,0.01)
        lefty = int((-x*vy/vx) + y)
        righty = int(((cols-x)*vy/vx)+y)
        cv2.line(img1,(cols-1,righty),(0,lefty),(255,0,0),2)
        line_y1 = righty
        line_y2 = lefty
        #cv2.imshow('contorno',canny)
        #if (M['m00'] != 0):
         #       cx = int(M['m10']/M['m00'])
          #      cy = int(M['m01']/M['m00'])
           #     cv2.circle(frame,(cx,cy),8,(0,255,105),3)
            #    return (cx,cy,area)
        return(x,y,w,h)


'''
ball = sphere (color = color.green, radius = 1.0, make_trail=True, retain=200)
ball.pos = (10,10,4)
ball.trail_object.radius = 0.05
ball.mass = 1.0
ball.p = vector (0.15, 2.0, 0)
# Criando parede no ambiente virtual:
ball_00 = sphere (color = color.green, radius = 2)
ball_01 = sphere (color = color.blue, radius = 2)
ball_10 = sphere (color = color.red, radius = 2)
ball_11 = sphere (color = color.white, radius = 2)
ball_00.pos = (0,0,0)
ball_01.pos = (0,40,0)
ball_10.pos = (38,0,0)
ball_11.pos = (38,40,0)
        
wallR = box (pos=( 0 , 38/2, 0), size=(3.0, 38.0 , 10.0),  color = color.red)
wallL = box (pos=( 38 , 38/2, 0), size=(3.0, 38.0 , 10.0),  color = color.red)
wallB = box (pos=( 38/2 , 0, 0), size=(38.0, 3.0 , 10.0),  color = color.red)
wallT = box (pos=( 38/2 , 38 , 0), size=(38.0, 3.0 , 10.0),  color = color.red)

wallJ = box (pos=( 38/2 , 38/2 , -7.0), size=(38.0, 38.0 , 4.0),  color = color.red)


'''
dt = 0.5
t=0.0
ball_10 = sphere(color = color.green, radius = 1,make_trail=True, retain=200)
ball_10.trail_object.radius = 0.05
ball_10.mass = 1.0
ball_10.p = vector (0.0, +1.4 , 0)
ball_10.pos = (10,10,0)
wallR = box(pos=(0,0,0), size=(10.0, 1.0, 10.0),  color = color.red)
#ball_11 = sphere (color = color.white, radius = 2)
while True:
        rate(100)
        _,img = capture.read()
        pressed_key = cv2.waitKey(1) & 0xFF
        height,width = img.shape[:2]
        # Vou utilizar apenas um segmento da imagem:
        img1 = img[100:500, 100:500]
        
        he,wi = img1.shape[:2]
        # Temos que pegar apenas a reta branca:
        reta_white = Otsu_Lim(img1)
        # Pegar as coordenadas:
        x,y,w,h= coordenada(reta_white,img1)
        cv2.circle(img1,(x,y),1,(0,0,255),5)
        cv2.circle(img1,(x+w/2,y),1,(0,0,255),5)
        cv2.circle(img1,(x,y+h/2),1,(0,255,200),5)
        cv2.circle(img1,(x,y-h/2),1,(0,1000,100),5)
        cv2.circle(img1,(x-w/2,y),1,(0,100,255),5)
        x1 = x/10
        y1 = y/10
        ## Ainda nao atualizei o tamanho do retangulo
        print(wallR.pos)
        wallR.pos = (x1,40 - y1,0)
        
        # Tem que ajeitar os if para colidir somente com a parde, tem
        # que ajeitar as duas paredes para o desenho
        # Melhorar a deteccao de apenas o traco Branco
        rate(100)
        t = t + dt
        ball_10.pos = ball_10.pos + (ball_10.p/ball_10.mass)*dt
        print("ball_posi: ",ball_10.pos)
        if not (wallR.pos.x > ball_10.x > -wallR.pos.x):
            ball_10.p.x = -ball_10.p.x
        if not (wallR.pos.y > ball_10.y > -wallR.pos.y):
            ball_10.p.y = -ball_10.p.y

        
        
        cv2.imshow('img1',img1)
        if pressed_key == ord("z"):
                break



cv2.destroyAllWindows()
capture.release()
