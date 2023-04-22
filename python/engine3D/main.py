import pygame as pg
from random import *
import numpy
import math
from numpy import sin, cos
import time





# window dimensions
width = 250
height = 250



global n
n =0



# Grid Color
gcol = 25
color = (gcol, gcol, gcol)

# scaling factor
factor = 25 # eg. 10 pixels == 1 unit



class Camera:
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0
global yaw, roll, pitch, master
yaw = 0
roll = 0
pitch = 0
master = 0


xrange = range(int(width/-2), int((width/2)-1))
yrange = range(int(height/-2), int((height/2)-1))

cam = Camera()

fz = 10
fd = 2

screen = pg.display.set_mode((width, height))
clock = pg.time.Clock()

dx = int(width/2)
dy = int(height/2)-1

def main():

    

    running = True
    matrix = [[0 for x in range(width)] for y in range(height)]
    
    for x in xrange: # -125 - 125
        x = x/factor
        for y in yrange:
            y = y/factor
            
            
            z = mfunction(x, y)
            #print(y, int(dy-y*factor))
            matrix[int(x*factor+dx)][int(dy-y*factor)] = z




    while running:
        global yaw, pitch, roll, master
        #drawGrid()
        #start = time.perf_counter()
        a = cos(yaw)*cos(pitch)
        b = cos(yaw)*sin(pitch)*sin(roll)-sin(yaw)*cos(roll)
        c = cos(yaw)*sin(pitch)*cos(roll)+sin(yaw)*sin(roll)
        d = sin(yaw)*cos(pitch)
        e = sin(yaw)*sin(pitch)*sin(roll)+cos(yaw)*cos(roll)
        f = sin(yaw)*sin(pitch)*cos(roll)-cos(yaw)*sin(roll)
        g = -sin(pitch)
        h = cos(pitch)*sin(roll)
        i = cos(pitch)*cos(roll)
        
        #finish = time.perf_counter()
        #print((finish-start)*1000000)


        

        screen.fill((0,0,0))
     

        # loop through all pixels in window
        for x in xrange:
            x = x/factor
            for y in yrange:
                y = y/factor
                #start = time.perf_counter()

                z = matrix[int(x*factor+dx)][int(dy-y*factor)]

                newx = x*a+y+b+z+c
                newy = x*d+y*e+f*z
                newz = x*g+y*h+i*z
                #print(newz)

                newx = int(newx*factor)+dx
                newy = dy-int(newy*factor)

                #print(newz)
                #(newz+fd)*fz
                #if newz > 255:
                #    rgb = (200, 0, 0)
               # if newz < 0:
                #    rgb = (0, 200, 0)
              #  else:
                #    rgb = (0, 0, newz)
                
                rgb = (0, 0, (newz+1)*50)
                
                
                screen.set_at((newx,newy), rgb)
                finish = time.perf_counter()
                #print((finish-start)*1000000)
                #exit()
                




        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False


        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            yaw -= 0.1
        if keys[pg.K_RIGHT]:
            yaw += 0.1
        pg.display.flip()

        #yaw += 0.05
        #pitch += 0.05
        #roll += 0.05

        #clock.tick(1000)




def mfunction(x, y=None):


    z=numpy.sin(x)

    return z


def transform(x, y, z):
    global master
    point = numpy.matrix(f'{x};{y};{z}')



    newpoint = numpy.dot(master, point)


    



    newx = newpoint.item(0)
    newy = newpoint.item(1)
    newz = newpoint.item(2)

    return (newx, newy, newz)







def drawGrid():
    screen.fill((0, 0, 0))
    # Grid Lines
    for x in range(0, width-1, factor):
        for y in range(0, height-1):
            screen.set_at((x,y), color)
        
    for y in range(0, height-1, factor):
        for x in range(0,width-1):
            screen.set_at((x,y), color)
        
    
    # Axis Lines
    for x in range(0, width-1):
        screen.set_at((x, int(height/2)), (100, 0, 0))
    for y in range(0, height-1):
        screen.set_at((int(width/2), y), (0, 100, 0))

    



if __name__ == '__main__':
    main()