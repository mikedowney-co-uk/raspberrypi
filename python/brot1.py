# First attempt at full screen drawing with pygame
# Does the mandelbrot set

import pygame,sys
from pygame.locals import *

SCREENW = 480
SCREENH = 320
ITER = 255

pygame.init()
DISPLAYSURF = pygame.display.set_mode([SCREENW,SCREENH],pygame.FULLSCREEN)

cx=0.5
cy=0.0
scale = 1.75

pstep = 2.0*scale/SCREENW

def calculate_pixel(x,y):
	c_real = (x - SCREENW / 2) * pstep - cx
	c_imag = (y - SCREENH / 2) * pstep - cy
	counter = 0
	z_real = 0
	z_imag = 0

	while True:
		z_real1 = z_real * z_real - z_imag * z_imag + c_real
		z_imag1 = 2 * z_real * z_imag + c_imag
		z_real = z_real1		
		z_imag = z_imag1
		dist = z_real * z_real + z_imag * z_imag
		counter = counter + 1
		if(dist > 4):
			return counter
		if(counter > ITER):
			return 0

def byte_to_col(c):
	r = (c * 8) % 255
	g = (c * 64) % 255
	b = c
	return (r,g,b)

tf = pygame.font.Font('freesansbold.ttf', 32)

def showText(x,y,text, fg=(255,0,0),bg=(0,0,255)):
	textobj = tf.render(text,True,fg,bg)
	textrect = textobj.get_rect()
	textrect.center(x,y)
	DISPLAYSURF.blit(textobj, textrect)

showText(240,160,"Mandelbrot")

for y in range(SCREENH):
	pixObj = pygame.PixelArray(DISPLAYSURF)
	for x in range(SCREENW):
		c = calculate_pixel(x,y)
		pixObj[x][y] = byte_to_col(c)
	del pixObj
	pygame.display.update() 

while True: # main game loop
	for event in pygame.event.get():
		if event.type == KEYUP:
			pygame.quit()
			sys.exit()