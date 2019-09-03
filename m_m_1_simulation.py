import numpy as np
import Queue
import random
import math

class Evenement:
	def __init__(self):
		self.date=0
		self.type_event=""
		self.file_evenement=Queue.PriorityQueue(maxsize=0)
	
	def addEvent(self,date,type_event):
		e=Evenement()		
		e.date=date
		e.type_event=type_event
		self.file_evenement.put(e)

	def getEvent(self):
		e=self.file_evenement.get()
		return e

	def delExp_landa(self):
		m=1./9
		return -m*math.log(random.random())

	def delExp_mu(self):
		m=1./10
		return -m*math.log(random.random())

class Simulation:
	def __init__(self):
		self.temps=[]
		self.etat=0
		self.t=0
		self.B=10
		self.e=Evenement()
		self.tmax=100
		for i in range(self.B+1):
			self.temps.append(0)
		
	def simulation(self):
		dt=self.e.delExp_landa()
		self.e.addEvent(self.t+dt,"Arrivee")
		while self.t<self.tmax :
			event=self.e.getEvent()
			ot=self.t
			self.t=event.date
			self.temps[self.etat]=self.temps[self.etat]+self.t-ot
			if event.type_event=="Service":
				self.etat=self.etat-1
				if self.etat > 0 :
					self.e.addEvent(self.t+self.e.delExp_mu(),"Service")
			if event.type_event=="Arrivee":
				if self.etat < self.B:
					self.etat=self.etat+1
				self.e.addEvent(self.t+self.e.delExp_landa(),"Arrivee")
				if self.etat == 1 :
					self.e.addEvent(self.t+self.e.delExp_mu(),"Service")
	def afficherResultat(self):
		j=0
		for i in self.temps:
			j+=1
			print("etat ",j,"=",i)

s=Simulation()
s.simulation()
s.afficherResultat()
				
			
		
	
	
	
