from pylab import *
import random 


alpha=5
beta=10
landa=9
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

def DefExp_Beta(beta=10):
    return -math.log(random.random())/beta

def DefExp_Alpha():
    return -math.log(random.random())/alpha

listeonoff=[]
Lon=[]
compArriees=0


def sporadicite(B=10, lamda=9, Mu=10, tmax=1000,beta=10):
    nbr_cl_servie=0
    Temps=[0]*(B+1)
    Lev=[]
    etat=0
    t=0
    ton=0 
    toff=0
    tonoff=0
    dt=DefExp_Lamda()
    Lon.append(dt)
    x=DefExp_Alpha()
    ton=ton+x   
    AddEvent(listeonoff,tonoff+x,"ON")  
    event=listeonoff[0]
    AddEvent(Lev,t+dt,"Arrivees")
    compArriees=1
    tonoff=tonoff+event.date
    
    while t < tmax:
        s=len(listeonoff)
        if listeonoff[s-1].type_event=="ON" :
            AddEvent(Lev,t+DefExp_Lamda(),"Arrivees")        
            while t<tonoff :              
                e=GetEvent_v2(Lev)
                ot=t
                t=e.date
                Temps[etat]=Temps[etat]+t-ot                
                if e.type_event=="Service":
                    if etat!=0:
                        etat-=1
                        nbr_cl_servie+=1
                    if etat> 0:
                        AddEvent(Lev,t+DefExp_Mu(), "Service")                        
                if e.type_event=="Arrivees":
                    if etat<B:
                        etat+=1
                    dt=DefExp_Lamda()
                    AddEvent(Lev,t+dt, "Arrivees")
                    compArriees+=1
                    Lon.append(dt)                    
                    if etat==1:
                        AddEvent(Lev,t+DefExp_Mu(), "Service")                       
            x=DefExp_Beta(beta)
            toff=toff+x
            AddEvent(listeonoff,tonoff+x,"OFF")
            tonoff=listeonoff[s].date            
        else : 
            while t<tonoff:
                
                if etat==0 : t=tonoff
                else :
                    if etat!=0:
                        etat=etat-1
                        nbr_cl_servie+=1
                    if etat> 0:
                        AddEvent(Lev,t+DefExp_Mu(), "Service")
                        e=GetEvent_v2(Lev)
                        t=e.date                                    
            x=DefExp_Alpha()
            ton+=x
            AddEvent(listeonoff,t+x,"ON")
            s=len(listeonoff)
            tonoff=listeonoff[s-1].date
    return Temps,compArriees,ton,toff,nbr_cl_servie

def Q1():
    ############Calcule de beta#############
    L=sporadicite(tmax=1000,B=10)
    compArriees=L[1]
    Ton=0
    compOn=1
    compOff=1
    Toff=0
    lamda_on=0
    for i in range(len(listeonoff)):
        if listeonoff[i].type_event=="ON":
            Ton+=listeonoff[i].date
            compOn+=1
        else:
            Toff+=listeonoff[i].date
            compOff+=1
    Ton=Ton/(compOn-1)
    Toff=Toff/(compOff-1)
    
    #beta=(Ton+Toff)/Ton
    beta=(L[2]+L[3])/L[2]
    for i in range(len(Lon)):
        lamda_on+=Lon[i]
    lamda_on=lamda_on/len(Lon)
    #lamda_on=sum(Lon)/len(Lon)


    print("Ton= ",Ton,"- Toff= ",Toff)
    print("Beta=",beta)
    print("Nombre de clients qui arrives= ",compArriees)
    return beta,lamda_on

def som_proba_nombreclientsmoyen(tmax=1000):
    Temps=sporadicite(tmax=1000,B=10)[0]
    somP=0
    somCl=0
    for i in range(len(Temps)):
        somP+=Temps[i]/tmax
        somCl+=i*Temps[i]/tmax
    return somP,somCl
    

def afficher_Q1():
    tmax=1000
    T=sporadicite(tmax=1000,B=10)
    Temps=T[0]
    s=0
    print("Temps=",Temps)
    #n bar
    for i in range(len(Temps)):
        print("probabilite de ",i,"= ",Temps[i]/tmax)
        s+=Temps[i]/tmax
        
    print("N_bar= ",s)
    #Q1()

def PR(beta=10):
    tmax=1000
    T=sporadicite(tmax=1000,B=10,beta=beta)
    Temps=T[0]
    proba_10_ON=Temps[10]/tmax
    PR=proba_10_ON
    return PR

def N_bar(tmax,B=10,beta=10):
    Temps=sporadicite(tmax=tmax,B=B,beta=beta)[0]
    s=0
    for i in range(len(Temps)):
        s+=i*Temps[i]/tmax
    return s

def R_bar(beta):
    Nbar=N_bar(tmax=1000,B=10,beta=beta)
    Rbar=(Nbar*(alpha+beta))/(landa*beta)
    return Rbar

def tracer_R_bar():
    beta=linspace(9,200,6)
    Y=[R_bar(x) for x in beta]
    plot(beta, Y)
    title("R_bar=f(beta)")
    xlabel("beta")
    ylabel("R_bar")
    show()
def tracer_PR():
    Tbeta=linspace(9,200,5)
    Y=[PR(x) for x in Tbeta]
    plot(Tbeta, Y)
    title("PR=f(beta)")
    xlabel("beta")
    ylabel("PR")
    show()
    
afficher_Q1()
L=som_proba_nombreclientsmoyen()
lamda_on=Q1()[1]
A_bar=L[0]*9
print("pratique=",A_bar)
theorique=(landa*beta)/(alpha+beta)
print("theorique=",theorique)
nbr_cl_servie=sporadicite(tmax=1000,B=10)[4]
print(nbr_cl_servie)
