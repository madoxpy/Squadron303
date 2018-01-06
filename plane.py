from pygame import *
import numpy as np
from random import *

green=(0,255,0)
greengrass=(1,166,17)
black=(0,0,0)
white=(255,255,255)
bluesky=(135,206,235)
red=(255,5,5)
bloodred=(138,7,7)
blue=(0,0,255)
darkblue=(0,0,139)


init()
window=display.set_mode((640,480))
clock = time.Clock()
Font=font.SysFont("arial",26)

cloudspic=[image.load("cloud01.png"),image.load("cloud02.png"),image.load("cloud03.png")]
bullet_pic=image.load("bullet.png")

def rot(pic,ang):
	orig_rect=pic.get_rect()
	rot_image=transform.rotate(pic,ang)
	rot_rect=orig_rect.copy()
	rot_rect.center=rot_image.get_rect().center
	rot_image=rot_image.subsurface(rot_rect).copy()
	return rot_image

class Bullet(object):
	def __init__(self):
		self.x=320
		self.y=240
		self.v=30
		x=mouse.get_pos()[0]-285
		y=mouse.get_pos()[1]-205
		self.aimx=-self.v*1.0*x/np.sqrt(x**2+y**2)
		self.aimy=-self.v*1.0*y/np.sqrt(x**2+y**2)
		print x,y
		
	def go(self,v):
		x=mouse.get_pos()[0]-285
		y=mouse.get_pos()[1]-205
		self.x=self.x-v*1.0*x/np.sqrt(x**2+y**2)-self.aimx
		self.y=self.y-v*1.0*y/np.sqrt(x**2+y**2)-self.aimy
	def draw(self):
		window.blit(bullet_pic,(self.x,self.y))


class Cloud(object):
	def __init__(self):
		self.x=randint(-1000,1000)
		self.y=randint(-1000,1000)
		self.size=randint(50,200)
		self.pic=choice(cloudspic)
		self.pic=transform.scale(self.pic,(self.size,self.size))
	
	def go(self,v):
		x=mouse.get_pos()[0]-285
		y=mouse.get_pos()[1]-205

		self.x=self.x-v*1.0*x/np.sqrt(x**2+y**2)
		self.y=self.y-v*1.0*y/np.sqrt(x**2+y**2)
		if self.x>1000:
			self.x=-1000
		if self.x<-1000:
			self.x=1000
		if self.y>1000:
			self.y=-1000
		if self.y<-1000:
			self.y=1000		
	def draw(self):
		window.blit(self.pic,(self.x,self.y))

class Plane(object):
	def __init__(self):
		self.pic=image.load("plane.png")
		self.pic=transform.scale(self.pic,(70,70))
		self.dir=0
	
	
	def go(self):
		x=mouse.get_pos()[0]-285
		y=mouse.get_pos()[1]-205
		if x>0:
			self.dir=90+np.arctan(1.0*y/x)/np.pi*180
		if x<0:
			self.dir=90+np.arctan(1.0*y/x)/np.pi*180+180
		if x==0 and y>=0:
			self.dir=180
		if x==0 and y<0:
			self.dir=0
		
	def draw(self):
		window.blit(rot(self.pic,-self.dir),(285,205))

class Game(object):
	def __init__(self):
		self.plane=Plane()
		self.rockets= []
		self.clouds=[]
		for i in range(80):
			self.clouds.append(Cloud())
		self.bullets=[]
		self.v=10
	def go(self):
		for bullet in self.bullets:
			bullet.go(self.v)
		
		self.plane.go()
		for rocket in self.rockets:
			rocket.go()
		for cloud in self.clouds:
			cloud.go(self.v)
	def draw(self):
		window.fill(bluesky)
		for cloud in self.clouds:
			cloud.draw()
		self.plane.draw()
		for rocket in self.rockets:
			rocket.draw()
		for bullet in self.bullets:
			bullet.draw()
	def shoot(self):
		self.bullets.append(Bullet())
		


end=False

game=Game()

while not end:
	for zet in event.get():
		if zet.type ==QUIT:
			end=True
	
	game.draw()
	game.go()
	if mouse.get_pressed()[0]:
		game.shoot()
	
	clock.tick(20)
	display.flip()