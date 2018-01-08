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

res=[1280,960]

init()
window=display.set_mode(res)
clock = time.Clock()
Font=font.SysFont("arial",44)

cloudspic=[image.load("cloud01.png"),image.load("cloud02.png"),image.load("cloud03.png")]
bullet_pic=image.load("bullet.png")
rocket_pic=image.load("rocket.png")
rocket_pic=transform.scale(rocket_pic,(50,100))

def rot(pic,ang):
	orig_rect=pic.get_rect()
	rot_image=transform.rotate(pic,ang)
	rot_rect=orig_rect.copy()
	rot_rect.center=rot_image.get_rect().center
	rot_image=rot_image.subsurface(rot_rect).copy()
	return rot_image



class Rocket(object):
	def __init__(self):
		self.x=randint(-2000,2000)
		self.y=randint(-2000,2000)
		while self.x<res[0]/2+700 and self.x>res[0]/2-700 and self.y<res[1]/2+700 and self.y>res[1]/2-700:
			self.x=randint(-2000,2000)
			self.y=randint(-2000,2000)
		self.size=50
		self.rect=Rect(self.x-25,self.y-50,50,100)
		self.act=True
		self.v=1
	
	def go(self,v):
		x=mouse.get_pos()[0]-res[0]/2
		y=mouse.get_pos()[1]-res[1]/2
		self.x=self.x-v*1.0*x/np.sqrt(x**2+y**2)
		self.y=self.y-v*1.0*y/np.sqrt(x**2+y**2)
		if self.x>res[0]/2:
			self.x=self.x-self.v
		if self.x<res[0]/2:
			self.x=self.x+self.v		
		if self.y>res[1]/2:
			self.y=self.y-self.v
		if self.y<res[1]/2:
			self.y=self.y+self.v		
		self.rect=Rect(self.x-25,self.y-50,50,100)
	def draw(self):
		if self.act:
			#draw.rect(window,white,self.rect,1)
			window.blit(rocket_pic,(self.x-25,self.y-50))
		

class Bullet(object):
	def __init__(self):
		self.x=res[0]/2
		self.y=res[1]/2
		self.v=30
		x=mouse.get_pos()[0]-res[0]/2
		y=mouse.get_pos()[1]-res[1]/2
		self.aimx=-self.v*1.0*x/np.sqrt(x**2+y**2)
		self.aimy=-self.v*1.0*y/np.sqrt(x**2+y**2)
		self.rect=Rect(self.x,self.y,10,10)
		
	def go(self,v):
		x=mouse.get_pos()[0]-res[0]/2
		y=mouse.get_pos()[1]-res[1]/2
		self.x=self.x-v*1.0*x/np.sqrt(x**2+y**2)-self.aimx
		self.y=self.y-v*1.0*y/np.sqrt(x**2+y**2)-self.aimy
		self.rect=Rect(self.x,self.y,10,10)

	def draw(self):
		#draw.rect(window,white,self.rect,1)
		window.blit(bullet_pic,(self.x,self.y))


class Cloud(object):
	def __init__(self):
		self.x=randint(-2000,2000)
		self.y=randint(-2000,2000)
		self.size=randint(50,200)
		self.pic=choice(cloudspic)
		self.pic=transform.scale(self.pic,(self.size,self.size))
	
	def go(self,v):
		x=mouse.get_pos()[0]-res[0]/2
		y=mouse.get_pos()[1]-res[1]/2

		self.x=self.x-v*1.0*x/np.sqrt(x**2+y**2)
		self.y=self.y-v*1.0*y/np.sqrt(x**2+y**2)
		if self.x>2000:
			self.x=-2000
		if self.x<-2000:
			self.x=2000
		if self.y>2000:
			self.y=-2000
		if self.y<-2000:
			self.y=2000		
	def draw(self):
		window.blit(self.pic,(self.x,self.y))

class Plane(object):
	def __init__(self):
		self.pic=image.load("plane.png")
		self.pic=transform.scale(self.pic,(140,140))
		self.dir=0
		self.rect=Rect(res[0]/2-45,res[1]/2-45,90,90)
	
	def go(self):
		x=mouse.get_pos()[0]-res[0]/2
		y=mouse.get_pos()[1]-res[1]/2
		if x>0:
			self.dir=90+np.arctan(1.0*y/x)/np.pi*180
		if x<0:
			self.dir=90+np.arctan(1.0*y/x)/np.pi*180+180
		if x==0 and y>=0:
			self.dir=180
		if x==0 and y<0:
			self.dir=0
		
	def draw(self):
		#draw.rect(window,white,self.rect,1)
		window.blit(rot(self.pic,-self.dir),(res[0]/2-70,res[1]/2-70))

class Game(object):
	def __init__(self):
		self.plane=Plane()
		self.rockets= []
		self.clouds=[]
		for i in range(160):
			self.clouds.append(Cloud())
		self.bullets=[]
		self.rockets=[]
		for i in range(10):
			self.rockets.append(Rocket())		
		self.v=10
		self.gameover=False
		self.points=0.0
	def go(self):
		if not self.gameover:
			for bullet in self.bullets:
				bullet.go(self.v)

			self.plane.go()
			for rocket in self.rockets:
				rocket.go(self.v)
			for cloud in self.clouds:
				cloud.go(self.v)

			hit=[]
			for rocket in self.rockets:
				for bullet in self.bullets:
					if rocket.rect.colliderect(bullet.rect):
						rocket.x=randint(-2000,2000)
						rocket.y=randint(-2000,2000)

			for rocket in self.rockets:
				if rocket.rect.colliderect(self.plane.rect):
					self.gameover=True
			self.points=self.points+0.1
			
			if int(self.points*10)%100==0:
				for rocket in self.rockets:
					rocket.v=rocket.v+1

			
	def draw(self):
		window.fill(bluesky)
		for cloud in self.clouds:
			cloud.draw()
		self.plane.draw()
		for rocket in self.rockets:
			rocket.draw()
		for bullet in self.bullets:
			bullet.draw()
		if self.gameover:
			text = Font.render("Game Over",True,red)
			window.blit(text,(550,300))
		text = Font.render(str(self.points),True,red)
		window.blit(text,(0,0))
	def shoot(self):
		b=0
		for bullet in self.bullets:
			if bullet.x>0 and bullet.x<res[0] and bullet.y>0 and bullet.y<res[1]:
				b=b+1
		if b<=10:
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