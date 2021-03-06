# -*- coding: utf-8 -*-

# screen /dev/ttyUSB0 57600

import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

#from  profils.develop.constantes import *

import marshal
import time
import lib.serie_simple
from time import sleep


serie1 = lib.serie_simple.SerieSimple("/dev/ttyUSB1", 9600, 5)
serie0 = lib.serie_simple.SerieSimple("/dev/ttyUSB0", 9600, 5)

#BAUDRATE : 9600, 57600

#ctes = ["0.0","0.0","0.0","0.0","0.0","0.0"]
#marshal.dump(ctes, open("constantes_asserv", 'wb'))
lastx = 0.0
lasty = 0.0

global dest
dest = "rien"

def recevoir ():
    a = ""
    b = ""
    try:
        a = serie0.lire()
    except:
        pass
    try:
        b = serie1.lire()
    except:
        pass
    return str(a)+str(b)

def envoyer(arg):
    global dest
    try:
        serie0.ecrire(arg)
    except:
        pass
    try:
        serie1.ecrire(arg)
    except:
        pass
    
    #enregistrement des constantes étalonnées
    
    #ctes = marshal.load(open("constantes_asserv","rb"))
    
    #if dest == "ctp":
        #ctes[0] = arg
    #elif dest == "ctd":
        #ctes[1] = arg
    #elif dest == "cti":
        #ctes[2] = arg
    #elif dest == "crp":
        #ctes[3] = arg
    #elif dest == "crd":
        #ctes[4] = arg
    #elif dest == "cri":
        #ctes[5] = arg
        
    #dest = arg    
    #marshal.dump(ctes, open("constantes_asserv", 'wb'))

def initialise():
    ctes = marshal.load(open("constantes_asserv","rb"))
    envoyer("ctp")
    envoyer(ctes[0])
    envoyer("ctd")
    envoyer(ctes[1])
    envoyer("cti")
    envoyer(ctes[2])
    envoyer("crp")
    envoyer(ctes[3])
    envoyer("crd")
    envoyer(ctes[4])
    envoyer("cri")
    envoyer(ctes[5])

def trace_err():
    while True:
        envoyer("eerT")
        logt = recevoir()
        
        envoyer("eerR")
        logr = recevoir()
        if logt == "END" or logr == "END":
            break
        print str(logt)+", "+str(logr)+" \n"
        
def attend_fin_goto():
    while recevoir() != "END":
        pass
    
            
#initialise()
while True :
    print "modifier ?"
    print "constantes de rotation.............r"
    print "constantes de translation..........t"
    print "entrer constantes indépendemment...c"
    print "afficher les constantes actuelles..a"
    print "lire coordonnées...................l"
    print "sortez moi d'ici !.................q"
    print "écoute sur la série................e"
    print "tourner de n tics................tou"
    print "translater de n tics.............tra"
    print "goto x y........................goto"
    
    choix = raw_input()
    if choix == "q":
        try:
            serie0.stop()
        except:
            pass
        try:
            serie1.stop()
        except:
            pass
        break
    elif choix == "r":
        print "constantes de rotation :"
        
        print "kp ?"
        buff = raw_input()
        envoyer("crp")
        envoyer(str(float(buff)))
        print "kd ?"
        buff = raw_input()
        envoyer("crd")
        envoyer(str(float(buff)))
        print "ki ?"
        buff = raw_input()
        envoyer("cri")
        envoyer(str(float(buff)))
        
    elif choix == "t":
        print "constantes de translation :"
        
        print "kp ?"
        buff = raw_input()
        envoyer("ctp")
        envoyer(str(float(buff)))
        print "kd ?"
        buff = raw_input()
        envoyer("ctd")
        envoyer(str(float(buff)))
        print "ki ?"
        buff = raw_input()
        envoyer("cti")
        envoyer(str(float(buff)))
        
    elif choix == "c":
        print "quelle constante modifier ?"
        print "de rotation.....r"
        print "de translation..t"
        choixC = raw_input()
        print "entrez q pour quitter"
        print "exemple : p 0.0"
        print "exemple : i 3"
        while True :
            buf = raw_input()
            if buf == "q":
                break
            envoyer("c"+choixC+buf[0])
            envoyer(str(float(buf[2:])))
        
    elif choix == "a":
        ctes = marshal.load(open("constantes_asserv","rb"))
        print "translation : kp="+ctes[0]+" kd="+ctes[1]+" ki="+ctes[2]
        print "rotation    : kp="+ctes[3]+" kd="+ctes[4]+" ki="+ctes[5]
        
    elif choix == "tou":
        buff = raw_input()
        envoyer("t")
        envoyer(str(float(buff)))
        trace_err()
        
    elif choix == "e":    
        while True:
            sleep(0.1)
            print recevoir()
                        
    elif choix == "tra":
        buff = raw_input()
        envoyer("d")
        envoyer(str(float(buff)))
        #trace_err()
        
    elif choix == "goto":
        buf1 = raw_input()
        buf2 = raw_input()
        envoyer("goto")
        envoyer(str(float(buf1)))
        envoyer(str(float(buf2)))
        trace_err()
        
    elif choix == "script":
        envoyer("goto")
        envoyer(str(float(210)))
        envoyer(str(float(0)))
        attend_fin_goto()
        
        envoyer("goto")
        envoyer(str(float(420)))
        envoyer(str(float(-820)))
        attend_fin_goto()
        
        envoyer("goto")
        envoyer(str(float(1540)))
        envoyer(str(float(-820)))
        attend_fin_goto()
        
        envoyer("goto")
        envoyer(str(float(1540)))
        envoyer(str(float(820)))
        attend_fin_goto()
        
        envoyer("goto")
        envoyer(str(float(1540)))
        envoyer(str(float(-820)))
        attend_fin_goto()
        
        envoyer("goto")
        envoyer(str(float(420)))
        envoyer(str(float(-820)))
        attend_fin_goto()
        
        envoyer("goto")
        envoyer(str(float(220)))
        envoyer(str(float(0)))
        attend_fin_goto()
        
        
        envoyer("t")
        envoyer(str(float(0.0)))
        attend_fin_mvt()
        
        envoyer("d")
        envoyer(str(float(-50.0)))
        attend_fin_mvt()
        
        
    elif choix == "l":
        while True:
            print "x ? y ? o (orientation) ? "
            print "b (pour lire en boucle), q (pour quitter)"
            choixL = raw_input()
            if choixL == "q":
                break
            elif choixL == "x":
                envoyer("ex")
                print recevoir()
            elif choixL == "y":
                envoyer("ey")
                print recevoir()
            elif choixL == "o":
                envoyer("et")
                print recevoir()
            elif choixL == "b":
                # err ? (erreurs sur trans, rot)"--- l (log) ? eo (orientation) ? "
                print "xy ? o (orientation) ? "
                choixB = raw_input()
                if choixB == "q":
                    break
                elif choixB == "o":
                    while True:
                        envoyer("eo")
                        try:
                            print str(float(recevoir())/1000)+" \n"
                        except:
                            pass
                elif choixB == "xy":
                    while True:
                        envoyer("ex")
                        logx = recevoir()
                        
                        envoyer("ey")
                        logy = recevoir()
                        print str(float(logx))+", "+str(float(logy))+" \n"
                elif choixB == "err":
                    trace_err()
                elif choixB == "l":
                    f = open("trace_x_y","w")
                    while True:
                        envoyer("ex")
                        logx = recevoir()
                        f.write("x = "+str(float(logx)-float(lastx))+" \t")
                        envoyer("ey")
                        logy = recevoir()
                        f.write("y = "+str(float(logy)-float(lasty))+"\n")
                        print "x = "+str(float(logx)-float(lastx))+" \t"+"y = "+str(float(logy)-float(lasty))+"\n"
                        lastx = logx
                        lasty = logy
                else:
                    while True:
                        envoyer(choixB)
                        print recevoir()