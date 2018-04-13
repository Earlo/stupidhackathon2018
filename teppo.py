from math import sqrt

class Tulppu():
	def __init__(self,x,y,w,h):
		self.box = (x,y,w,h)
		self.center = (x+w/2,y+h/2)
		self.disabled = False
		self.age = [0,0,0]

	def update(self, x,y,w,h):
		self.box = (x,y,w,h)
		self.center = (x+w/2,y+h/2)
	
	def isAlike(self, tep):
		self.age[0] += 10
		if (self.age[0] < 255):
			self.age[0] = 0
			self.age[1] += 1
			if (self.age[1] < 255):
				self.age[1] = 0
				self.age[2] += 1

		return self.box[2]/getDist(*self.center,*getCenter(*tep))

def getCenter(x,y,w,h):
	return (x+w/2,y+h/2)

def getDist(x1,y1,x2,y2):
	return sqrt( (x2 - x1)**2 + (y2 - y1)**2 )


