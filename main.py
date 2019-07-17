#coding:utf-8
import random,time,pygame
from pygame.locals import *

pygame.init()
btex,btey=1230,924
io = pygame.display.Info()
mtex,mtey=io.current_w,io.current_h
tex,tey=mtex-50,mtey-100
def rx(x): return int(x/btex*tex)
def ry(y): return int(y/btey*tey)

fenetre=pygame.display.set_mode([tex,tey])
pygame.display.set_caption("Simulation d'un course de vélo")
pygame.key.set_repeat(100,90)
font1=pygame.font.SysFont("Arial",ry(15))
font2=pygame.font.SysFont("Arial",ry(20))
font3=pygame.font.SysFont("Arial",ry(25))
font4=pygame.font.SysFont("Arial",ry(30))
font5=pygame.font.SysFont("Arial",ry(35))
font6=pygame.font.SysFont("Arial",ry(40))

def rr(a,b): return random.randint(a,b)
def rcl(): return (rr(50,200),rr(50,200),rr(50,200))

dim="images/"
itete=[]
iyeux=[]
inez=[]
ibouches=[]
icheveux=[]
ibarbes=[]
for x in range(12): itete.append( "tete"+str(x+1)+".png" )
for x in range(5): iyeux.append( "yeux"+str(x+1)+".png" )
for x in range(3): inez.append( "nez"+str(x+1)+".png" )
for x in range(3): ibouches.append( "bouche"+str(x+1)+".png" )
for x in range(14): icheveux.append( "cheveux"+str(x+1)+".png" )
for x in range(25): ibarbes.append( "barbe"+str(x+1)+".png" )


tym=ry(150)
timg=rx(100)
max_endurance=500000

im_m_jaune=pygame.transform.scale( pygame.image.load(dim+"m_jaune.png"), [timg,timg] )

voy=["a","e","y","u","i","o"]
con=["z","r","t","p","q","s","d","f","g","h","j","k","l","m","w","x","c","v","b","n"]
prsts=["cvcv","cvccvc","ccvv","vccvc","ccvcvc","cvcvc","cvvc","vccv"]
def crea_nom():
    nom=""
    for x in range(2):
        nbl=0
        for l in random.choice(prsts):
            if l=="v": a=random.choice(voy)
            else: a=random.choice(con)
            if nbl==0: a=a.upper()
            nom+=a
            nbl+=1
        if x==0: nom+=" "
    return nom

def crea_mape():
    e=10000
    mape=[[0,e,"plat"]]
    dc="plat"
    for x in range(random.randint(400,1000)):
        tps=["descente","plat","montee"]
        f=random.randint(10,1000)
        dc=random.choice(tps)
        mape.append( [e,e+f,dc] )
        e+=f
    return mape

def rtn_note(perso):
    note=0
    note+=perso.endurance_tot/max_endurance*100.
    note+=perso.vitesse_max/65*100.
    note+=perso.vitesse_max_montee/58.5*100.
    note+=perso.vitesse_max_descente/97.5*100.
    note+=perso.acc/1*100.
    note+=perso.acc_montee/2.25*100.
    note+=perso.acc_descente/3.75*100.
    note+=(120-perso.tmesprint)/120.*100.
    note=int(note/8)
    if note <= 25: classe="bronze"
    elif note <= 50: classe="argent"
    elif note <= 75: classe="or"
    elif note <= 90: classe="platine"
    else: classe="diamant"
    return note,classe

class Equipe:
    def __init__(self):
        self.nom=crea_nom().split(" ")[0]
        self.persos=[]
        self.cl1=rcl()
        self.cl2=rcl()
        self.cl3=rcl()

pays=["France","USA","Belgique","Allemagne","Canada","Espagne","Portugal","Luxembourg","Angleterre","Finlande","Rep. Tchèque","Russie","Chine","Afrique du Sud","Algérie","Syrie","Zimbabwe","Bresil","Argentine","Australie","Congo","Groenland","Nouvelle Zélande","Mexique","Inde","Suède","Pays-Bas","Autriche","Suisse","Italie","Pologne","Roumanie","Turquie","Colombie","Bolivie","Pérou","Vénézuela","Chili","Paraguay","Libie","Egypte","Iran","Arabie","Kazakhstan","Turkménistan"]
class Perso:
    def __init__(self,equipe):
        self.nom=crea_nom()
        self.equipe=equipe
        self.age=random.randint(20,50)
        self.endurance_tot=rr(1000,max_endurance)
        self.endurance=self.endurance_tot
        self.vitesse_max=rr(25,65)
        self.vitesse_max_montee=rr(40,90)*self.vitesse_max/100
        self.vitesse_max_descente=rr(110,150)*self.vitesse_max/100
        self.acc=rr(1,100)/100.
        self.acc_montee=rr(40,90)*self.acc/100.
        self.acc_descente=rr(110,150)*self.acc/100.
        self.tmesprint=random.randint(30,120)
        self.note,self.classe=rtn_note(self)
        self.vitesse_actuelle=0.
        self.px=random.randint(0,100)
        self.py=random.randint(0,tym)
        self.dbg=time.time()
        self.tbg=0.05
        self.fini=False
        self.rect=None
        self.place=0
        self.pays=random.choice(pays)
        self.img_t=pygame.transform.scale(pygame.image.load(dim+random.choice(itete)).convert_alpha(),[timg,timg])
        self.img_y=pygame.transform.scale(pygame.image.load(dim+random.choice(iyeux)).convert_alpha(),[timg,timg])
        self.img_n=pygame.transform.scale(pygame.image.load(dim+random.choice(inez)).convert_alpha(),[timg,timg])
        self.img_b=pygame.transform.scale(pygame.image.load(dim+random.choice(ibouches)).convert_alpha(),[timg,timg])
        self.img_c=pygame.transform.scale(pygame.image.load(dim+random.choice(icheveux)).convert_alpha(),[timg,timg])
        self.img_ba=pygame.transform.scale(pygame.image.load(dim+random.choice(ibarbes)).convert_alpha(),[timg,timg])
        self.img=pygame.Surface([timg,timg])
        self.img.fill((250,250,250))
        self.img.blit(self.img_t,[0,0])
        self.img.blit(self.img_y,[0,0])
        self.img.blit(self.img_n,[0,0])
        self.img.blit(self.img_b,[0,0])
        self.img.blit(self.img_c,[0,0])
        self.img.blit(self.img_ba,[0,0])
        self.issprint=False
        self.dsprint=0
        self.tsprint=0
        self.is_m_jaune=False
        self.tps_tour_total=0
        self.t_begin=0
        self.t_end=0
        self.terrain="plat"
    def update(self,mape,finis):
        if time.time()-self.dbg>=self.tbg and not self.fini:
            if self.endurance>self.endurance_tot: self.endurance=self.endurance_tot
            self.dbg=time.time()
            tp=""
            for m in mape:
                if self.px>=m[0] and self.px < m[1]: tp=m[2]
            if tp=="montee":
                decc=0.2
                acc=self.acc_montee
                vitmax=self.vitesse_max_montee
                pente=1.5
                self.terrain="montee"
            elif tp=="descente":
                decc=0.05
                acc=self.acc_descente
                vitmax=self.vitesse_max_descente
                pente=0.5
                self.terrain="descente"
            else:
                self.terrain="plat"
                decc=0.1
                acc=self.acc
                pente=1
                vitmax=self.vitesse_max
                if random.randint(1,10000)==1 and time.time()-self.dsprint>=self.tmesprint:
                    self.issprint=True
                    self.dsprint=time.time()
                    self.tsprint=random.randint(5,30)
            if self.issprint:
                if time.time()-self.dsprint>=self.tsprint:
                    self.issprint=False
                    self.dsprint=time.time()
                vitmax*=2
                acc*=2
                pente*=2
            self.py+=random.randint(-1,1)
            if self.py<0: self.py=0
            if self.py>tym: self.py=tym
            if self.vitesse_actuelle<0: self.vitesse_actuelle=0
            if random.randint(1,4)!=1 and self.vitesse_actuelle<vitmax:
                if self.endurance<=0:
                    self.vitesse_actuelle+=acc/3.
                else:
                    self.vitesse_actuelle+=acc
                    self.endurance-=acc*pente
            if self.vitesse_actuelle>vitmax: self.vitesse_actuelle-=2
            self.px+=self.vitesse_actuelle
            if self.px>=mape[len(mape)-1][1]:
                self.t_end=time.time()
                self.fini=True
                self.px+=100000-(len(finis)*300)
                self.vitesse_actuelle=0
                finis.append(self)
        return finis

tp_classes=["bronze"  ,"argent"     ,"or"       ,"platine"  ,"diamant"]
cl_classes=[(92,37,19),(209,209,209),(255,213,0),(76,53,140),(0,251,255)]

tp_terrains=["descente","plat","montee"]
cl_terrains=[(200,220,200),(120,120,120),(100,75,75)]

def aff(eqs,mape,menu,fps,pause,sel,classement):
    fenetre.fill((0,0,0))
    if menu==0:
        pygame.draw.rect(fenetre,(100,100,100),(0,0,tex,tey-ry(500)),0)
        xx,yy=rx(100),ry(25)
        tx=rx(700)
        ty=tym
        pygame.draw.rect(fenetre,(80,80,80),(xx,yy,tx,ty),0)
        ttx=mape[len(mape)-1][1]
        pts=[]
        p=0.
        for m in mape:
            pts.append([m[0],p])
            if m[2]=="plat": c=0
            elif m[2]=="descente": c=-0.005
            else: c=0.005
            p+=c*(m[1]-m[0])
            pts.append([m[1],p])
        pygame.draw.rect(fenetre,(0,0,0),(xx,yy,tx,ty),1)
        for e in eqs:
            for p in e.persos:
                if not p.fini:
                    t=ry(5)
                    if sel==p: t=ry(10)
                    cl=e.cl1
                    if p.is_m_jaune: cl=(255,255,0)
                    p.rect=pygame.draw.circle(fenetre,cl,(xx+int(p.px/ttx*tx),yy+p.py),t,0)
                    pygame.draw.circle(fenetre,(0,0,0),(xx+int(p.px/ttx*tx),yy+p.py),t,1)
        xx,yy=rx(100),ry(250)
        for x in range(len(pts)-2):
            p1=pts[x]
            p2=pts[x+1]
            pygame.draw.line(fenetre,(20,20,20),(xx+int(p1[0]/ttx*tx),yy+p1[1]),(xx+int(p2[0]/ttx*tx),yy+p2[1]),2)
        xx,yy=rx(0),tey-5*ry(100)
        tx,ty=tex/2,ry(100)
        bts=[]
        for x in range(10):
            p=classement[x]
            if sel==None: bts.append( pygame.draw.rect(fenetre,(100,75,10),(xx,yy,tx,ty),0) )
            else: pygame.draw.rect(fenetre,(100,75,10),(xx,yy,tx,ty),0)
            pygame.draw.rect(fenetre,(0,0,0),(xx,yy,tx,ty),1)
            fenetre.blit( p.img , [xx,yy])
            fenetre.blit( font1.render(p.nom,True,(255,255,255)) , [xx+rx(105),yy+ry(5)] )
            fenetre.blit( font2.render(p.classe,True,cl_classes[tp_classes.index(p.classe)]) , [xx+rx(105),yy+ry(25)] )
            fenetre.blit( font2.render(p.pays,True,(255,255,255)) , [xx+rx(205),yy+ry(5)] )
            fenetre.blit( font2.render(p.equipe.nom,True,p.equipe.cl1) , [xx+rx(205),yy+ry(25)] )
            fenetre.blit( font4.render(str(x+1),True,(255,255,255)) , [xx+tx-rx(30),yy+ry(15)] )
            if p.issprint: fenetre.blit( font2.render("sprint",True,(255,55,155)) , [xx+rx(355),yy+ry(5)] )
            if p.fini:
                fenetre.blit( font2.render("fini",True,(255,250,50)) , [xx+rx(355),yy+ry(25)] )
                if x>0: fenetre.blit( font2.render("-"+str(classement[0].t_end-p.t_end)[:5]+" sec",True,(250,250,250)) , [xx+rx(405),yy+ry(25)] )    
            if p.is_m_jaune: fenetre.blit( img_m_jaune , [xx+rx(220),yy] )
            yy+=ty
            if x==4:
                xx+=tex/2
                yy-=ty*5
        if sel!=None:
            xx,yy=rx(0),ry(350)
            tx,ty=tex,tey-yy
            pygame.draw.rect(fenetre,(20,20,20),(xx,yy,tx,ty),0)
            fenetre.blit( pygame.transform.scale(sel.img,[timg*2,timg*2]) , [xx,yy])
            fenetre.blit( font2.render(sel.nom,True,(255,255,255)) , [xx+rx(205),yy+ry(20)] )
            fenetre.blit( font3.render(sel.classe,True,cl_classes[tp_classes.index(sel.classe)]) , [xx+rx(205),yy+ry(80)] )
            pl=str(classement.index(sel)+1)
            pcl=(255,255,255)
            if pl=="1":
                pl+="er"
                pcl=(240, 216, 2)
            elif pl=="2":
                pl+="nd"
                pcl=(180,180,180)
            elif pl=="3":
                pl+="eme"
                pcl=(89, 57, 29)
            else: pl+="eme"
            fenetre.blit( font5.render(pl,True,pcl) , [xx+tx-rx(300),yy+ry(20)] )
            fenetre.blit( font2.render(sel.pays,True,(255,255,255)) , [xx+rx(505),yy+ry(20)] )
            fenetre.blit( font2.render("equipe : "+sel.equipe.nom,True,sel.equipe.cl1) , [xx+rx(505),yy+ry(100)] )
            pygame.draw.rect(fenetre,(255,255,255),(xx+rx(205),yy+ry(180),rx(500),ry(15)),0)
            pygame.draw.rect(fenetre,(0,100,255),(xx+rx(205),yy+ry(180),int(sel.endurance/sel.endurance_tot*rx(500)),ry(15)),0)
            pygame.draw.rect(fenetre,(0,0,0),(xx+rx(205),yy+ry(180),rx(500),ry(15)),1)
            fenetre.blit( font1.render("endurance",True,(0,0,0)) , [xx+rx(400),yy+ry(179)] )
            fenetre.blit( font3.render("vitesse : "+str(sel.vitesse_actuelle)[:5]+" km/h",True,(255,255,255)) , [xx+tex-rx(400),yy+ry(100)] )
            if sel.issprint: fenetre.blit( font3.render("sprint",True,(255,13,155)) , [xx+tex-rx(400),yy+ry(150)] )
            if sel.terrain=="plat": pygame.draw.line(fenetre,(255,255,255),(xx+tex-rx(100),yy+ry(100)),(xx+tex-rx(20),yy+ry(100)),1)
            elif sel.terrain=="montee": pygame.draw.line(fenetre,(255,255,255),(xx+tex-rx(100),yy+ry(120)),(xx+tex-rx(20),yy+ry(80)),1)
            else: pygame.draw.line(fenetre,(255,255,255),(xx+tex-rx(100),yy+ry(80)),(xx+tex-rx(20),yy+ry(120)),1)
            fenetre.blit( font1.render("vitesse maximale : "+str(sel.vitesse_max)[:5]+" km/h",True,(255,255,255)) , [xx+rx(20),yy+ry(250)] )
            fenetre.blit( font1.render("vitesse maximale montée : "+str(sel.vitesse_max_montee)[:5]+" km/h",True,(255,255,255)) , [xx+rx(20),yy+ry(270)] )
            fenetre.blit( font1.render("vitesse maximale descente : "+str(sel.vitesse_max_descente)[:5]+" km/h",True,(255,255,255)) , [xx+rx(20),yy+ry(290)] )
            fenetre.blit( font1.render("accélération : "+str(sel.acc)[:5]+" km/h",True,(255,255,255)) , [xx+rx(20),yy+ry(310)] )
            fenetre.blit( font1.render("accélération montée : "+str(sel.acc_montee)[:5]+" km/h",True,(255,255,255)) , [xx+rx(20),yy+ry(330)] )
            fenetre.blit( font1.render("accélération descente : "+str(sel.acc_descente)[:5]+" km/h",True,(255,255,255)) , [xx+rx(20),yy+ry(350)] )
            fenetre.blit( font1.render("endurance : "+str(int(sel.endurance))+" / "+str(int(sel.endurance_tot)),True,(255,255,255)) , [xx+rx(20),yy+ry(370)] )
            fenetre.blit( font1.render("temps total course : "+str(sel.tps_tour_total)+" sec",True,(255,255,255)) , [xx+rx(20),yy+ry(390)] )
    fenetre.blit( font2.render("fps : "+str(fps),True,(255,13,50)) , [rx(15),ry(15)])
    pygame.display.update()
    return bts


def main_etape(eqs):
    mape=crea_mape()
    menu=0
    pause=False
    sel=None
    encour=True
    fps=0
    finis=[]
    for e in eqs:
        for p in e.persos:
            p.px=0
            p.endurance+=p.endurance_tot/4
            if p.endurance>p.endurance_tot: p.endurance=p.endurance_tot
            p.issprint=False
            p.t_begin=time.time()
    while encour:
        t1=time.time()
        for e in eqs:
            for p in e.persos:
                if not pause: finis=p.update(mape,finis)
        classement=[]
        prs=[]
        nbfini=0
        for e in eqs:
            for p in e.persos:
                prs.append(p)
                if p.fini: nbfini+=1
        if nbfini>=len(prs)-1: encour=False
        classement=sorted(prs, key=lambda p: p.px, reverse=True) 
        bts=aff(eqs,mape,menu,fps,pause,sel,classement)
        for event in pygame.event.get():
            if event.type==QUIT: exit()
            elif event.type==KEYDOWN:
                if event.key==K_ESCAPE: exit()
                elif event.key==K_q: exit()
                elif event.key==K_SPACE: pause=not pause
                elif event.key==K_LEFT:
                    if sel!=None and classement.index(sel)<len(classement)-1: sel=classement[classement.index(sel)+1]
                elif event.key==K_RIGHT:
                    if sel!=None and classement.index(sel)>0: sel=classement[classement.index(sel)-1]
            elif event.type==MOUSEBUTTONUP:
                pos=pygame.mouse.get_pos()
                sel=None
                for e in eqs:
                    for p in e.persos:
                        if p.rect!=None and p.rect.collidepoint(pos):
                            sel=p
                            break
                for b in bts:
                    if b.collidepoint(pos):
                        sel=classement[bts.index(b)]
                        break
                        
        t2=time.time()
        tt=t2-t1
        if tt!=0: fps=int(1./tt)
    
    
    

def main():
    eqs=[]
    for x in range(15): eqs.append( Equipe() )
    for e in eqs:
        for x in range(15):
            e.persos.append( Perso(e) )
    for x in range(10):
        main_etape(eqs)
        prs=[]
        for e in eqs:
            for p in e.persos:
                p.tps_tour_total+=t_end-t_begin
                p.is_m_jaune=False
                prs.append(p)
        classement=sorted(prs, key=lambda p: p.tps_tour_total, reverse=True) 
        classement[0].is_m_jaune=True
        



main()










