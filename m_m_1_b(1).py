#from numpy.random import *
from pylab import *
import numpy as np
import matplotlib.pyplot as plt
import Queue
import random
import math

#Partie1   
class Event:
    def __init__(self,date=0,type_event=""):
        self.date=date
        self.type_event=type_event
    def __repr__(self):
        return str(self.date)+" "+self.type_event

def afficher_liste(Lev):
    for e in Lev:
        print(e)
        
def AddEvent(Lev,date,type_event):
    Lev.append(Event(date,type_event))
    
def AddEvent_v2(Lev,ev):
    Lev.append(ev)

#si la liste est trie dans l'ordre decroissante(selon la date)
def GetEvent_v1(Lev):
    return Lev[-1]

#sinon
def GetEvent_v2(Lev):
    k=0
    for i in range(1,len(Lev)):
        if Lev[i].date<Lev[k].date :
            k=i
    return Lev.pop(k)

def DefExp_Lamda(Lamda):
    return -math.log(random.random())/9

def DefExp_Mu(Mu):
    return -math.log(random.random())/10
 

def simulateur(B=10, lamda=9, Mu=10, tmax=1000):
    Temps=[0]*(B+1)
    Lev=[]
    etat=0
    t=0
    dt=DefExp_Lamda(lamda)
    AddEvent(Lev,t+dt,"Arrivees")
    while t < tmax:
        e=GetEvent_v2(Lev)
        ot=t
        t=e.date
        Temps[etat]=Temps[etat]+t-ot
        if e.type_event=="Service":
            etat-=1
            if etat> 0:
                AddEvent(Lev,t+DefExp_Mu(Mu), "Service")
        if e.type_event=="Arrivees":
            if etat<B:
                etat+=1
            AddEvent(Lev,t+DefExp_Lamda(lamda), "Arrivees")
            if etat==1:
                AddEvent(Lev,t+DefExp_Mu(Mu), "Service")
    return Temps
    
#Q1
def Pk_N_bar(k,tmax,B=10):
    Temps=simulateur(tmax=tmax,B=B)
    s=0
    #n bar
    for i in range(len(Temps)):
        s+=i*Temps[i]/tmax
    return (Temps[k]/tmax,s)#pk , nbar

#Q2
def tracer2(tmax_min=100,tmax_max=23000,n=20):#exp 100,1000000,20
    T=linspace(tmax_min,tmax_max,n)
    
    F_P10_N_bar=[]
    F_N_bar=[]
    F_P10=[]
    i=0
    for tmax in T:
        F_P10_N_bar.append(Pk_N_bar(10,tmax))
        F_N_bar.append(F_P10_N_bar[i][1])
        F_P10.append(F_P10_N_bar[i][0])
        i+=1

    plot(T, F_N_bar)
    title("N_bar=f(Temp)")
    xlabel("Temp")
    ylabel("N_bar")
    show()
    plot(T, F_P10)
    xlabel("Temp")
    ylabel("p10")
    title("p10=f(Temp)")
    show()
    tracer_R_bar()  

#Q3
def tracer_R_bar():
    B=list(range(10,230,10))
    R_bar=[]
    PR=[]
    for b in B:
        L=Pk_N_bar(b,1000,b)
        R_bar.append(L[1]/(1-L[0]))
        PR.append((0.1)*((0.9)**b/(1-0.9**(b+1))))
    
    plot(B, R_bar)
    
    xlabel("B")
    ylabel("R(bar)")
    title("R(bar)=f(B)")
    show()
    plot(B, PR)
    xlabel("B")
    ylabel("PR")
    title("PR=f(B)")

    show()


def afficher_Q1():
    tmax=1000
    Temps=simulateur(tmax=1000,B=10)
    s=0
    #n bar
    print("Temps=",Temps)
    for i in range(len(Temps)):
        s+=i*Temps[i]/tmax
        print("probabilite de ",i,"= ",Temps[i]/tmax)
    print("N_bar= ",s)


afficher_Q1()
tracer2()
