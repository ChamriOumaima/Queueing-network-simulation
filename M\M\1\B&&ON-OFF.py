import random
import math

#Partie 2  
class Event:
    def __init__(self,date=0,type_event=""):
        self.date=date
        self.type_event=type_event
    def __repr__(self):
        return str(self.date)+" "+self.type_event

def AddEvent(Lev,date,type_event):
    Lev.append(Event(date,type_event))
    

def GetEvent_v2(Lev):
    k=0
    for i in range(1,len(Lev)):
        if Lev[i].date<Lev[k].date :
            k=i
    return Lev.pop(k)

def DefExp_Lamda():
    return -math.log(random.random())/9

def DefExp_Mu():
    return -math.log(random.random())/10

def DefExp_Beta():
    return -math.log(random.random())/10

def DefExp_Alpha():
    return -math.log(random.random())/5
 

def sporadicite(B=10, lamda=9, Mu=10, tmax=1000):
    Temps=[0]*(B+1)
    Lev=[]
    etat=0
    t=0
    dt=DefExp_Lamda()
    ton=0 
    toff=0
    tonoff=0
    listeonoff=[]
    x=DefExp_Alpha()
    ton=ton+x
    listeonoff.append(Event(tonoff+x,"ON"))
    event=listeonoff[0]
    AddEvent(Lev,t+dt,"Arrivees")
    tonoff=tonoff+event.date
    
    while t < tmax:
        s=len(listeonoff)
        if listeonoff[s-1].type_event=="ON" :
            while t<tonoff :
                e=GetEvent_v2(Lev)
                ot=t
                t=e.date
                Temps[etat]=Temps[etat]+t-ot
                if e.type_event=="Service":
                    etat-=1
                    if etat> 0:
                        AddEvent(Lev,t+DefExp_Mu(), "Service")
                if e.type_event=="Arrivees":
                    if etat<B:
                        etat+=1
                    AddEvent(Lev,t+DefExp_Lamda(), "Arrivees")
                    if etat==1:
                        AddEvent(Lev,t+DefExp_Mu(), "Service")
            x=DefExp_Beta()
            toff=toff+x
            listeonoff.append(Event(tonoff+x,"OFF"))
            tonoff=listeonoff[s-1].date

        else : 
            while t<tonoff:
                if etat==0 : t=tonoff
                else :
                    etat=etat-1
                    AddEvent(Lev,t+DefExp_Mu(), "Service")
                    t=t+DefExp_Mu()
            
            x=DefExp_Alpha()
            ton+=x
            listeonoff.append(Event(t+x,"ON"))
            s=len(listeonoff)
            tonoff=listeonoff[s-1].date

    return Temps

def afficher_Q1():
    tmax=1000
    Temps=sporadicite(tmax=1000,B=10)
    s=0
    #n bar
    print("Temps=",Temps)
    for i in range(len(Temps)):
        s+=i*Temps[i]/tmax
        print("probabilite de ",i,"= ",Temps[i]/tmax)
    print("N_bar : le nombre moyen de client dans le systeme : ",s) 
    landa=9.0
    beta=10
    print("A_bar : le debit moyen des arrivees :",landa/beta) 
    print("R_bar : le temps moyen de reponse :", s/9) 

afficher_Q1()