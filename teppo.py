from math import sqrt

class Tulppu():
	def __init__(self,x,y,w,h):
		self.box = (x,y,w,h)
		self.center = (x+w/2,y+h/2)
		self.disabled = False
		self.age = 255

	def update(self, x,y,w,h):
		self.age += 25
		self.box = (x,y,w,h)
		self.center = (x+w/2,y+h/2)
	
	def isAlike(self, tep):
		d = getDist(*self.center,*getCenter(*tep))
		if d > 0:
			return sqrt((self.box[2])**2 + (self.box[3])**2)/d
		else:
			return 1.0

	def getCol(self):
		return [self.age%255,max(0,(self.age-255)%255),max(0,(self.age-255*2)%255)]

	def grow(self):
		self.age = self.age - 0

	def isDead(self):
		return self.age < 0

def getCenter(x,y,w,h):
	return (x+w/2,y+h/2)

def getDist(x1,y1,x2,y2):
	return sqrt( (x2 - x1)**2 + (y2 - y1)**2 )


